"""Shared cross-validation and scoring helpers (same protocol as notebook 02).

All snapshots of a match stay in one fold (grouped by ``gameId``). Losses are
reported as positive numbers (lower is better).
"""

import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.model_selection import GridSearchCV, StratifiedGroupKFold, cross_validate

SEED = 42

cv = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=SEED)
scoring = {
    "accuracy": "accuracy",
    "roc_auc": "roc_auc",
    "log_loss": "neg_log_loss",
    "brier": "neg_brier_score",
}
LOWER_IS_BETTER = {"log_loss", "brier"}
METRIC_COLS = ["accuracy", "accuracy_sd", "roc_auc", "log_loss", "brier"]


def _positive(raw_scores):
    return {m: -v if m in LOWER_IS_BETTER else v for m, v in raw_scores.items()}


def cv_scores(model, data, cols, target="hasWon", group="gameId"):
    """Per-fold scores for a model with fixed hyperparameters."""
    result = cross_validate(
        model, data[cols], data[target], groups=data[group], cv=cv, scoring=scoring, n_jobs=-1
    )
    return _positive({m: result[f"test_{m}"] for m in scoring})


def tune(model, grid, data, cols, target="hasWon", group="gameId"):
    """Grid search with grouped CV; the best setting is chosen by log loss."""
    search = GridSearchCV(
        model, grid, cv=cv, scoring=scoring, refit="log_loss",
        n_jobs=-1, return_train_score=True,
    )
    search.fit(data[cols], data[target], groups=data[group])
    i = search.best_index_
    scores = {
        m: np.array([search.cv_results_[f"split{k}_test_{m}"][i] for k in range(cv.get_n_splits())])
        for m in scoring
    }
    return search, _positive(scores)


def summarize(model_name, feature_set, scores, params=None, **extra):
    """One results-table row: mean of each metric across folds."""
    row = {"model": model_name, "features": feature_set}
    row.update({m: v.mean() for m, v in scores.items()})
    row["accuracy_sd"] = scores["accuracy"].std()
    row["params"] = params or {}
    # Per-fold scores; folds are identical across feature sets, so they can be paired
    row["fold_accuracy"] = scores["accuracy"].tolist()
    row["fold_log_loss"] = scores["log_loss"].tolist()
    row.update(extra)
    return row


class GoldLeadRule(ClassifierMixin, BaseEstimator):
    """Baseline: predict the training win rate of teams ahead (goldDiff > 0) or not ahead."""

    def fit(self, X, y):
        ahead = np.asarray(X["goldDiff"]) > 0
        y = np.asarray(y)
        self.classes_ = np.array([0, 1])
        self.p_ahead_ = y[ahead].mean()
        self.p_not_ahead_ = y[~ahead].mean()
        return self

    def predict_proba(self, X):
        p = np.where(np.asarray(X["goldDiff"]) > 0, self.p_ahead_, self.p_not_ahead_)
        return np.column_stack([1 - p, p])

    def predict(self, X):
        return (self.predict_proba(X)[:, 1] >= 0.5).astype(int)
