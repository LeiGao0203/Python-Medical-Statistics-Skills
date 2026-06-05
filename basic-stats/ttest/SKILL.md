---
name: "medical-stat-python-ttest"
description: "Use for medical statistics in Python when comparing continuous outcomes between two groups, paired pre/post measurements, or one-sample means using scipy t-test workflows."
---

# Python T-Test Skill

## When to use

- Compare a continuous medical outcome between two independent groups.
- Analyze paired measurements such as baseline and follow-up values.
- Estimate and report mean differences with confidence intervals when assumptions are reasonable.

## When not to use

- Outcome is ordinal, highly skewed, or dominated by outliers without a robust plan.
- There are more than two groups; use ANOVA or a regression model instead.
- The design requires covariate adjustment, clustering, or repeated-measures modeling.

## Python dependencies

Use Python-native libraries for this workflow: `pandas`, `numpy`, `scipy`, `statsmodels`, `seaborn`.

## Data and assumptions

- Continuous outcome measured on a comparable scale.
- Independent observations for independent-sample tests.
- Approximately normal residuals within groups, especially for small samples.
- Use Welch's test when group variances are not assumed equal.

## Standard workflow

1. Confirm the clinical question, endpoint, exposure or grouping variable, and analysis population.
2. Load data with `pandas`, check missingness, coding, outliers, and clinically impossible values.
3. Choose the method variant that matches the design and assumptions.
4. Run the Python analysis with transparent preprocessing and deterministic settings where relevant.
5. Inspect diagnostics, assumption checks, and sensitivity analyses before interpreting estimates.
6. Save tables and figures that can be reproduced from the same script or notebook.

## Minimal Python example

```python
import numpy as np
import pandas as pd
from scipy import stats

# df contains columns: treatment_group, systolic_bp
active = df.loc[df["treatment_group"] == "active", "systolic_bp"].dropna()
control = df.loc[df["treatment_group"] == "control", "systolic_bp"].dropna()

result = stats.ttest_ind(active, control, equal_var=False)
mean_diff = active.mean() - control.mean()
print(f"Welch t-test mean difference: {mean_diff:.2f}")
print(f"t={result.statistic:.3f}, p={result.pvalue:.4f}")
```

## Reporting guidance

Report the analysis population, missing-data handling, method variant, effect estimate, confidence interval when available, test statistic or model summary, p-value, and any assumption checks or limitations. Use clinical units and clinically meaningful labels rather than raw column names.
