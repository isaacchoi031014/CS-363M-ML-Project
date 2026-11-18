# Final evaluation findings

The preferred minute-14 model selected before test inspection was **Logistic regression**. After refitting on 19,723 training matches, it achieved **77.19% accuracy**, **0.8596 ROC AUC**, **0.4634 log loss**, and **0.1529 Brier score** on 4,927 reserved test matches. Its training-selection CV log loss was 0.4705.

The four-model comparison and probability diagnostics are in the tables and figures above. Calibration curves describe reliability; no calibrator was fitted on test data. Final configurations remain those frozen before evaluation.

## Error patterns for the CV-preferred model at minute 14

There were 1,124 errors, including 55 wrong predictions with confidence at least 90%.

- Absolute gold difference <1,000: 401 errors / 999 matches (40.1% error rate).
- Absolute gold difference 1,000–<3,000: 520 errors / 1,683 matches (30.9% error rate).
- Absolute gold difference ≥3,000: 203 errors / 2,245 matches (9.0% error rate).

There were 106 matches where blue led by at least 3,000 gold but lost, and 97 where blue trailed by at least 3,000 gold but won. These outcome reversals are distinct from model errors: some reversals may have been predicted correctly.

## Representative model errors

- Match 4542619089: predicted blue-win probability 0.015, actual outcome blue win, gold difference -8,376, experience difference -6,493, dragon difference -2.
- Match 4521071452: predicted blue-win probability 0.020, actual outcome blue win, gold difference -7,109, experience difference -8,187, dragon difference -1.
- Match 4401337188: predicted blue-win probability 0.021, actual outcome blue win, gold difference -7,277, experience difference -7,647, dragon difference -1.

These recorded states support descriptive case analysis, not a causal explanation of unobserved gameplay events. Later-minute comparisons change the eligible cohort; the common-survivor table provides an additional conditional comparison.

## Submission handoff

Combine notebooks 01–05 into one submission organized as Introduction → Exploration & Preprocessing → Modeling → Results & Analysis. Include final model choices, the four-model test table, ROC/confusion/calibration plots, representative errors, and limitations. Ensure the final notebook regenerates required inputs from the raw CSV, then restart and Run All to verify reproducibility while preserving the frozen choices.
