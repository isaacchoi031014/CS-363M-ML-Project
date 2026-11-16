"""Feature engineering for any prediction minute.

Every feature for minute ``t`` uses only snapshots of the same match at or
before ``t``. Only matches still in progress at ``t`` are kept
(``gameDuration`` is recorded in milliseconds).
"""

import numpy as np
import pandas as pd

LANES = ["Top", "Mid", "Bot"]
TIERS = ["Outer", "Inner", "Base", "Nexus"]
DRAKES = ["Fire", "Water", "Air", "Earth", "Elder"]

# Columns that are identifiers, the target, unavailable during a match, or
# replaced by an engineered version.
NON_FEATURES = [
    "gameId", "gameDuration", "frame", "hasWon",
    "wardsPlaced",   # heavy-tailed; replaced by logWardsPlaced
    "isFirstBlood",  # 1 once any kill happens, regardless of team
]

FEATURE_DEFINITIONS = {
    # Objective and combat summaries at minute t
    "dragonDiff": "Dragons taken by blue minus dragons taken by red",
    "blueDragons": "Dragons taken by blue (progress toward dragon soul)",
    "redDragons": "Dragons taken by red (progress toward dragon soul)",
    "heraldDiff": "Rift Heralds taken by blue minus red",
    "baronDiff": "Barons taken by blue minus red",
    "elderDiff": "Elder dragons taken by blue minus red",
    "outerTurretDiff": "Outer turrets destroyed by blue minus lost by blue",
    "innerTurretDiff": "Inner turrets destroyed by blue minus lost by blue",
    "baseTurretDiff": "Base turrets destroyed by blue minus lost by blue",
    "nexusTurretDiff": "Nexus turrets destroyed by blue minus lost by blue",
    "totalTurretDiff": "All turrets destroyed by blue minus lost by blue",
    "inhibitorDiff": "Inhibitors destroyed by blue minus lost by blue",
    "killDeathDiff": "Blue kills minus blue deaths",
    "killShare": "Smoothed share of all kills that blue has: (kills + 1) / (kills + deaths + 2)",
    "assistsPerKill": "Blue assists per blue kill (team-fight participation)",
    "wardDiff": "Enemy wards blue destroyed minus blue wards destroyed by red",
    "logWardsPlaced": "log(1 + wards placed by blue); tames extreme ward counts",
    # Trajectory features from snapshots at minutes 10, 12, ..., t
    "goldChange2": "Gold difference now minus 2 minutes ago",
    "goldChange4": "Gold difference now minus 4 minutes ago",
    "expChange4": "Experience difference now minus 4 minutes ago",
    "killDeathChange4": "Kill-death difference now minus 4 minutes ago",
    "goldSlope": "Least-squares slope of gold difference per minute since minute 10",
    "expSlope": "Least-squares slope of experience difference per minute since minute 10",
    "maxGoldLead": "Largest blue gold lead seen so far",
    "minGoldLead": "Smallest blue gold lead (largest deficit) seen so far",
    "goldVolatility": "Standard deviation of 2-minute gold-difference changes",
    "leadChanges": "Number of times the gold lead switched teams",
}

OBJECTIVE_FEATURES = list(FEATURE_DEFINITIONS)[:17]
TRAJECTORY_FEATURES = list(FEATURE_DEFINITIONS)[17:]

# Notebook 01's engineered features, for a like-for-like baseline
NOTEBOOK01_FEATURES = [
    "dragonDiff", "killDeathDiff", "outerTurretDiff", "goldChange4", "expChange4",
]


def eligible_snapshots(raw, minute):
    """One row per match still in progress at the given minute."""
    rows = raw.loc[raw["frame"].eq(minute) & raw["gameDuration"].gt(minute * 60_000)]
    return rows.reset_index(drop=True)


def _sum(df, cols):
    return df[cols].sum(axis=1)


def objective_features(snap):
    """Objective, combat, and vision summaries from the minute-t snapshot."""
    out = pd.DataFrame(index=snap.index)

    blue_drakes = _sum(snap, [f"killed{d}Drake" for d in DRAKES])
    red_drakes = _sum(snap, [f"lost{d}Drake" for d in DRAKES])
    out["dragonDiff"] = blue_drakes - red_drakes
    out["blueDragons"] = blue_drakes
    out["redDragons"] = red_drakes
    out["heraldDiff"] = snap["killedRiftHerald"] - snap["lostRiftHerald"]
    out["baronDiff"] = snap["killedBaronNashor"] - snap["lostBaronNashor"]
    out["elderDiff"] = snap["killedElderDrake"] - snap["lostElderDrake"]

    for tier in TIERS:
        out[f"{tier.lower()}TurretDiff"] = (
            _sum(snap, [f"destroyed{lane}{tier}Turret" for lane in LANES])
            - _sum(snap, [f"lost{lane}{tier}Turret" for lane in LANES])
        )
    out["totalTurretDiff"] = out[[f"{t.lower()}TurretDiff" for t in TIERS]].sum(axis=1)
    out["inhibitorDiff"] = (
        _sum(snap, [f"destroyed{lane}Inhibitor" for lane in LANES])
        - _sum(snap, [f"lost{lane}Inhibitor" for lane in LANES])
    )

    out["killDeathDiff"] = snap["kills"] - snap["deaths"]
    out["killShare"] = (snap["kills"] + 1) / (snap["kills"] + snap["deaths"] + 2)
    out["assistsPerKill"] = snap["assists"] / snap["kills"].clip(lower=1)
    out["wardDiff"] = snap["wardsDestroyed"] - snap["wardsLost"]
    out["logWardsPlaced"] = np.log1p(snap["wardsPlaced"])
    return out[OBJECTIVE_FEATURES]


def trajectory_features(raw, snap, minute):
    """How the advantage developed from minute 10 up to minute t."""
    if minute < 14:
        raise ValueError("Trajectory features need snapshots at minute 10, 12, and 14 or later.")

    history = raw.loc[raw["gameId"].isin(snap["gameId"]) & raw["frame"].le(minute)].copy()
    history["killDeath"] = history["kills"] - history["deaths"]
    wide = history.pivot(index="gameId", columns="frame")
    gold, exp, kd = wide["goldDiff"], wide["expDiff"], wide["killDeath"]

    expected_frames = list(range(10, minute + 1, 2))
    if list(gold.columns) != expected_frames or gold.isna().any().any():
        raise ValueError("Every match needs a snapshot at each minute from 10 to t.")

    centered = np.asarray(gold.columns, dtype=float)
    centered -= centered.mean()

    out = pd.DataFrame(index=gold.index)
    out["goldChange2"] = gold[minute] - gold[minute - 2]
    out["goldChange4"] = gold[minute] - gold[minute - 4]
    out["expChange4"] = exp[minute] - exp[minute - 4]
    out["killDeathChange4"] = kd[minute] - kd[minute - 4]
    out["goldSlope"] = gold.to_numpy() @ centered / (centered**2).sum()
    out["expSlope"] = exp.to_numpy() @ centered / (centered**2).sum()
    out["maxGoldLead"] = gold.max(axis=1)
    out["minGoldLead"] = gold.min(axis=1)
    out["goldVolatility"] = gold.diff(axis=1).std(axis=1)
    signs = np.sign(gold.to_numpy())
    out["leadChanges"] = (signs[:, 1:] * signs[:, :-1] < 0).sum(axis=1)

    aligned = out.reindex(snap["gameId"])
    aligned.index = snap.index
    return aligned[TRAJECTORY_FEATURES]


def build_features(raw, minute):
    """Return (table, groups) for the given prediction minute.

    ``table`` has one row per eligible match: gameId, hasWon, raw features, and
    engineered features. ``groups`` maps a group name to its feature columns.
    Trajectory features are only built for minute 14 or later.
    """
    snap = eligible_snapshots(raw, minute)
    raw_cols = [c for c in raw.columns if c not in NON_FEATURES]

    parts = [snap[["gameId", "hasWon"] + raw_cols], objective_features(snap)]
    groups = {"raw": raw_cols, "objective": OBJECTIVE_FEATURES, "trajectory": []}
    if minute >= 14:
        parts.append(trajectory_features(raw, snap, minute))
        groups["trajectory"] = TRAJECTORY_FEATURES

    table = pd.concat(parts, axis=1)
    if table.isna().any().any():
        raise ValueError("Engineered features contain missing values.")
    return table, groups
