---
name: "medical-stat-python-roc"
description: "Use for medical statistics in Python when evaluating diagnostic or prediction scores with ROC curves, AUC, sensitivity, and specificity."
---

# Python ROC Analysis Skill

## When to use

- Evaluate discrimination of a biomarker, risk score, or classifier for a binary clinical outcome.
- Estimate AUC and decision thresholds.
- Create ROC plots and threshold tables for reports.

## When not to use

- The outcome is time-to-event without a fixed prediction horizon.
- Calibration or clinical utility is the primary question.
- Class labels or score direction are uncertain.

## Python dependencies

Use Python-native libraries for this workflow: `pandas`, `numpy`, `scikit-learn`, `matplotlib`, `seaborn`.

## Data and assumptions

- Binary outcome is coded consistently as 0/1 or false/true.
- Higher scores should correspond to higher event risk, or direction is explicitly reversed.
- Evaluation data are independent of model training data when reporting performance.
- AUC uncertainty or validation strategy is documented for manuscripts.

## Standard workflow

1. Confirm the clinical question, endpoint, exposure or grouping variable, and analysis population.
2. Load data with `pandas`, check missingness, coding, outliers, and clinically impossible values.
3. Choose the method variant that matches the design and assumptions.
4. Run the Python analysis with transparent preprocessing and deterministic settings where relevant.
5. Inspect diagnostics, assumption checks, and sensitivity analyses before interpreting estimates.
6. Save tables and figures that can be reproduced from the same script or notebook.

## Minimal Python example

```python
import pandas as pd
from sklearn.metrics import roc_auc_score, roc_curve

# df contains columns: disease_status (0/1), risk_score
y_true = df["disease_status"].astype(int)
y_score = df["risk_score"]

auc = roc_auc_score(y_true, y_score)
fpr, tpr, thresholds = roc_curve(y_true, y_score)
roc_table = pd.DataFrame({"threshold": thresholds, "sensitivity": tpr, "specificity": 1 - fpr})
print(f"AUC={auc:.3f}")
print(roc_table.head())
```

## Reporting guidance

Report the analysis population, missing-data handling, method variant, effect estimate, confidence interval when available, test statistic or model summary, p-value, and any assumption checks or limitations. Use clinical units and clinically meaningful labels rather than raw column names.
