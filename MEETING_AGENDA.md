# First Working Session

Goal: everyone can run the starter notebook, understands the dataset structure, and leaves with an assigned task.

## Before the meeting

- [ ] Commit and push the project setup, including `data/raw/lol_ranked_games.csv`.
- [ ] Each teammate clones the repo, creates a Python 3.12 environment, and installs `requirements.txt`.
- [ ] Each teammate runs `notebooks/01_data_exploration.ipynb` and sees 242,572 rows and 59 columns.
- [ ] Read `design.md` and the initial checks in `data/README.md`.

## Agenda (30 minutes)

1. **Setup check (5 minutes):** confirm everyone can run the notebook using their `.venv`.
2. **Dataset review (10 minutes):** discuss `gameId`, `frame`, `hasWon`, and which fields are available during a match. Review why `gameDuration` is excluded from predictors.
3. **Assign work (10 minutes):** choose an owner for each task below and agree on notebook ownership.
4. **Agree on the next deliverable (5 minutes):** confirm the random seed, due date, and next meeting.

## Initial tasks

| Task | Expected result | Owner |
| --- | --- | --- |
| Validate field meanings and timestamps | Notes on units, redundant fields, and remaining data-quality issues | TBD |
| Explore resource advantages and objectives | A few labeled plots and observations | TBD |
| Prepare the minute-14 cohort and match split | One row per eligible match; disjoint 80% training / 20% test match IDs | TBD |
| Plan baselines and evaluation | Agreed simple baseline, classification metric, and probability metric | TBD |

## Decisions to record together

- Shared random seed: TBD (suggestion: `42`).
- Notebook owner(s): TBD.
- First milestone due date: TBD.
- Next meeting: TBD.

First milestone: understand the columns and prepare the minute-14 dataset with a reproducible split by match. Keep the test set reserved for final evaluation.
