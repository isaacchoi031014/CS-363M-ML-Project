# League of Legends Win Prediction

CS 363M machine learning project using ranked solo-queue match snapshots to predict whether the blue team wins. Our primary prediction time is minute 14, with comparisons at minutes 10, 18, and 20.

See [design.md](design.md) for the project proposal and [MEETING_AGENDA.md](MEETING_AGENDA.md) for the next team meeting. The raw dataset and a minimal loading notebook are ready; analysis and model implementation will begin with the team.

## Repository layout

```text
.
├── design.md             # Project proposal
├── MEETING_AGENDA.md     # Meeting checklist and task ownership
├── requirements.txt      # Pinned Python dependencies
├── requirements-lock.txt # Tested dependency versions (used as constraints)
├── data/
│   ├── README.md         # Dataset source, verified counts, and checksum
│   ├── raw/              # Original downloaded dataset (keep unchanged)
│   └── processed/        # Cleaned data and engineered features
├── notebooks/            # Starter notebook, experiments, and final notebook
├── src/                  # Reusable preprocessing, feature, and model code
├── models/               # Saved trained models
└── reports/
    └── figures/          # Plots for the final report and presentation
```

Empty folders contain `.gitkeep` files so Git can track them. The original CSV is included with the project. Processed data, saved models, and local Python environments are ignored by Git.

## Local setup

Use Python 3.12 and run these commands from the repository root:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip check
python -m jupyter lab
```

On Windows PowerShell, use `py -3.12 -m venv .venv` to create the environment and `.venv\Scripts\Activate.ps1` to activate it, then run the same install, check, and Jupyter commands.

Dependencies are pinned in `requirements.txt`, which automatically applies the dependency constraints in `requirements-lock.txt`. The environment was verified with Python 3.12.1 on macOS; other operating systems may need additional platform-specific dependencies. Each teammate creates their own `.venv`.

Open [notebooks/01_data_exploration.ipynb](notebooks/01_data_exploration.ipynb) and run all cells. In VS Code, select `.venv/bin/python` as the notebook interpreter (Windows: `.venv\Scripts\python.exe`). The notebook only imports packages, loads the CSV, and displays its shape and first few rows.

## Dataset

The original CSV is at `data/raw/lol_ranked_games.csv` and is no longer ignored by Git. Once it is committed and pushed with the project, teammates will receive it when they clone; no separate download is needed. See [data/README.md](data/README.md) for its source, verified counts, and checksum. Keep the original file unchanged.

The starter notebook supports running from either the repository root or `notebooks/`. Keep paths relative to the project rather than using a teammate's absolute file path. Put reusable code in `src/` as it becomes useful.

## First working session

- Confirm everyone can open Jupyter and access the same dataset files.
- Review the [initial data checks](data/README.md), then inspect field meanings, timestamp units, and any remaining data-quality issues.
- Run the starter notebook together and use the [meeting agenda](MEETING_AGENDA.md) to assign initial tasks.
- Agree on a shared random seed and keep package versions consistent using the pinned requirements.
- Build the minute-14 cohort and reserve an 80% training / 20% test split by `gameId` before fitting preprocessing or models.

## Modeling rules

- Predict `hasWon` using only information available at or before the selected prediction time. Confirm how `frame` maps to minutes before selecting snapshots.
- Use `gameId` to group and split matches, not as a predictor. Keep every snapshot from a match in the same split or cross-validation fold.
- Exclude `gameDuration` from prediction features because final match duration is unavailable during a match. Keep `hasWon` separate as the target.
- Compute changes in advantage using only earlier snapshots from the same match.
- Fit preprocessing, feature selection, and K-means on training data only, including within cross-validation. Tune on the training portion and reserve the test set for final evaluation.
- Compare simple baselines with logistic regression, a decision tree, and a random forest. Document how filtering to later prediction times changes the eligible matches.

## Team workflow

Use a branch for each task and agree on notebook ownership to avoid merge conflicts. Include the original CSV in the initial commit; keep extra downloads, virtual environments, and generated model/data files out of commits. Clear exploratory notebook outputs before committing to keep reviews readable. Save presentation material in `reports/` and selected plots in `reports/figures/`.
