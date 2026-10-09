# Dataset

Source: [Kaggle: League of Legends SOLO-Q Ranked Games](https://www.kaggle.com/datasets/bobbyscience/league-of-legends-soloq-ranked-games?resource=download), provided by `bobbyscience`.

The original CSV was downloaded from Kaggle and extracted unchanged to `raw/lol_ranked_games.csv`. It is 38,679,427 bytes (about 36.9 MiB). This file is intended to be committed with the project so teammates receive the same dataset when they clone. Only processed data is ignored within `data/`.

## Verified on import

| Check | Result |
| --- | ---: |
| Snapshot rows | 242,572 |
| Columns, including identifiers and target | 59 |
| Distinct matches (`gameId`) | 24,912 |
| Blue wins, counted once per match | 12,539 |
| Blue losses, counted once per match | 12,373 |
| Empty or whitespace-only cells | 0 |
| Duplicate (`gameId`, `frame`) pairs | 0 |
| Matches with inconsistent `hasWon` labels | 0 |

Observed `frame` values are 10 through 56 in increments of 2. The selected prediction frames contain these numbers of snapshots, with one snapshot per eligible match:

| Frame | Snapshots |
| --- | ---: |
| 10 | 24,912 |
| 14 | 24,716 |
| 18 | 23,430 |
| 20 | 22,632 |

These checks confirm the proposal's dataset counts. Field interpretation and further exploration remain team project work. Keep the original CSV unchanged and save any derived datasets in `processed/`.

## File identity

SHA-256 for `raw/lol_ranked_games.csv`:

```text
09c75afd71f43e3d41474f6f7d629485455489b53e363167bf574ab965a0a210
```

Compare this checksum when confirming that teammates are using the same dataset version.
