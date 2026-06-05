---
name: "medical-stat-python-chisq"
description: "Use for medical statistics in Python when testing associations between categorical variables with pandas crosstabs and scipy chi-square or Fisher exact methods."
---

# Python Chi-Square Skill

## When to use

- Test association between two categorical clinical variables.
- Compare event proportions across treatment or exposure groups.
- Create contingency tables for manuscript-ready baseline or outcome reporting.

## When not to use

- Expected cell counts are too small for chi-square; use Fisher exact for small 2x2 tables.
- The endpoint needs covariate adjustment; use logistic regression.
- Rows are paired or repeated observations; use a paired categorical method.

## Python dependencies

Use Python-native libraries for this workflow: `pandas`, `numpy`, `scipy`, `seaborn`.

## Data and assumptions

- Observations are independent.
- Categories are mutually exclusive and correctly coded.
- Expected counts are adequate for chi-square approximation.
- For sparse 2x2 tables, Fisher exact is preferred.

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

# df contains columns: treatment_group, response
observed = pd.crosstab(df["treatment_group"], df["response"])
chi2, p_value, dof, expected = stats.chi2_contingency(observed)
print(observed)
print(f"chi2={chi2:.3f}, df={dof}, p={p_value:.4f}")

if observed.shape == (2, 2) and (expected < 5).any():
    odds_ratio, fisher_p = stats.fisher_exact(observed)
    print(f"Fisher exact OR={odds_ratio:.3f}, p={fisher_p:.4f}")
```

## Reporting guidance

Report the analysis population, missing-data handling, method variant, effect estimate, confidence interval when available, test statistic or model summary, p-value, and any assumption checks or limitations. Use clinical units and clinically meaningful labels rather than raw column names.
