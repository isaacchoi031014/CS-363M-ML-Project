# Project Design: League of Legends Win Prediction

## 1. Describe the dataset

We plan to use the League of Legends (LoL) SOLO-Q Ranked Games dataset. LoL is a competitive multiplayer game in which two teams (blue and red) compete to destroy the opposing team's base. The provider of the dataset describes it as containing approximately 25,000 Platinum-level ranked solo-queue matches.

Each row in the dataset is a snapshot of a match, beginning at minute 10 and continuing at two-minute intervals. The data consists of blue-team combat and objective statistics, differences in resources between the teams, and the eventual match outcome. Multiple rows thus describe the same match at different times, and matches are distinguished through `gameId`. This structure allows us to evaluate both early-game prediction and how predictive information develops during a match.

## 2. How many records does the dataset have?

The dataset contains 242,572 snapshots (rows/records) from 24,912 distinct matches. The snapshots are repeated observations of matches, rather than 242,572 independent games.

## 3. How many features does the dataset have? List or describe a few of them

The data has 59 columns, consisting of 55 game-statistics fields, snapshot time (`frame`), match identifier (`gameId`), final match duration (`gameDuration`), and the outcome label (`hasWon`). Not all columns will be used as prediction features.

Some important game-statistics fields include:

- `goldDiff`: gold difference between blue and red.
- `expDiff`: experience difference between teams.
- `champLevelDiff`: difference in average champion level.
- `kills`, `deaths`, and `assists`: blue-team combat statistics.
- Objective counters, such as `killedWaterDrake` and `lostElderDrake`.
- Turret and structure counters, such as `lostBotBaseTurret` and `destroyedMidInhibitor`.

## 4. What can you try to predict in this dataset?

We will predict whether the blue team ultimately wins, using information available while the match is still in progress. Our primary prediction time will be minute 14. We will investigate whether objective control and changes in gold and experience advantage improve predictions beyond economic advantage alone. We will also compare predictions at minutes 10, 18, and 20.

The results could support match analysis by identifying which observed advantages are most informative and examining situations where teams overcome an early deficit.

## 5. What kind of ML problem are you doing? Is this a labeled dataset appropriate for supervised classification or regression?

Our main ML problem is supervised binary classification, based on the label `hasWon`. Every snapshot/record has the label `hasWon`, where 1 indicates a blue-team win and 0 indicates a loss. At the match level, the dataset has 12,539 blue wins and 12,373 blue losses, making the classes approximately balanced.

## 6. Provide a link to the dataset

We downloaded the dataset from [Kaggle: League of Legends SOLO-Q Ranked Games](https://www.kaggle.com/datasets/bobbyscience/league-of-legends-soloq-ranked-games?resource=download).

## 7. Briefly describe a plan

We will validate timestamps and field meanings, remove redundant features, and explore resource advantages, objectives, and comeback patterns. We will engineer combat and objective differences and changes in advantage over time, using only information available at the prediction time.

We plan to compare logistic regression, a decision tree, and a random forest against simple baselines. We will use an 80% training / 20% test split by match, with cross-validation within the training portion, keeping snapshots of the same match together. We will tune the models and evaluate their classification accuracy and win probabilities.

As we expect the data to require limited cleaning, we will conduct deeper data exploration and feature engineering via K-means clustering of early-game states. We will interpret the results and prediction errors in our final notebook and presentation.
