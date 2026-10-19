---
name: model-evaluation
description: "Rigorously evaluate ML models across classification, regression, and detection metrics, preventing data leakage and benchmarking inference latency."
---

# Machine Learning Model Evaluation Protocol

Use this skill when designing validation strategies, evaluating model checkpoints, analyzing error distributions, or preparing production deployment benchmarks.

## Validation Strategy & Data Leakage Prevention

1. **Temporal & Group Splitting**:
   - For time-series or sequential data: **never** use random shuffle splits. Use rolling-window cross-validation or temporal out-of-time splits.
   - For multi-session/patient/user data: use `GroupKFold` on subject IDs to ensure no subject appears in both train and test splits.
2. **Preprocessing Pipeline Isolation**:
   - Fit scalers, encoders, and feature selectors **only** on the training fold (`fit_transform` on train, `transform` on validation/test). Fitting preprocessing transformations on the entire dataset is a catastrophic data leakage bug.

## Metric Selection

### Classification
- **Imbalanced Classes**: Never rely on raw accuracy. Evaluate **Precision-Recall AUC (PR-AUC)**, **F1-Score (macro/weighted)**, and **Matthews Correlation Coefficient (MCC)**.
- **Cost-Sensitive Decision Thresholds**: Calibrate probabilities with isotonic regression or Platt scaling. Tune decision thresholds based on real-world misclassification penalties (e.g. false negative vs false positive costs).

### Regression
- Report multiple complementary metrics:
  - **MAE**: Robust to outliers.
  - **RMSE**: Penalizes large deviations heavily.
  - **MAPE / sMAPE**: For scale-independent reporting.
  - Residual plot analysis: check for heteroscedasticity and non-zero mean residuals.

### Production Latency Benchmarking
- Measure latency at **P50**, **P95**, and **P99** percentiles across at least 1,000 iterations after warm-up runs.
- Measure memory footprint (peak VRAM and system RSS) under realistic batch sizes.
