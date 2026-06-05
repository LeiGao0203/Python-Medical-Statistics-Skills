---
name: "medical-stat-python-correlation"
description: "Use for medical statistics in Python when measuring association between two continuous or ordinal variables with Pearson or Spearman correlation."
---

# Python Correlation Skill

## When to use

- Quantify association between two continuous biomarkers or measurements.
- Use Spearman correlation for monotonic ordinal or non-normal relationships.
- Prepare correlation estimates with confidence intervals and scatterplots.

## When not to use

- The goal is prediction, adjustment, or causal estimation; use regression.
- The association is nonlinear without a monotonic relationship.
- Repeated measures from the same patient require clustered or mixed methods.

## Python dependencies

Use Python-native libraries for this workflow: `pandas`, `numpy`, `scipy`, `matplotlib`, `seaborn`.

## Data and assumptions

- Pairs of observations are independent.
- Pearson correlation assumes an approximately linear relationship.
- Spearman correlation evaluates monotonic rank association.
- Outliers and missingness have been inspected.

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
from scipy import stats

# df contains columns: bmi, fasting_glucose
pairs = df[["bmi", "fasting_glucose"]].dropna()
pearson_r, pearson_p = stats.pearsonr(pairs["bmi"], pairs["fasting_glucose"])
spearman_r, spearman_p = stats.spearmanr(pairs["bmi"], pairs["fasting_glucose"])
print(f"Pearson r={pearson_r:.3f}, p={pearson_p:.4f}")
print(f"Spearman rho={spearman_r:.3f}, p={spearman_p:.4f}")
```

## Reporting guidance

Report the analysis population, missing-data handling, method variant, effect estimate, confidence interval when available, test statistic or model summary, p-value, and any assumption checks or limitations. Use clinical units and clinically meaningful labels rather than raw column names.
