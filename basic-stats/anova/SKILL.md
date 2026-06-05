---
name: "medical-stat-python-anova"
description: "Use for medical statistics in Python when comparing a continuous endpoint across three or more groups with statsmodels ANOVA workflows."
---

# Python ANOVA Skill

## When to use

- Compare a continuous endpoint across three or more independent clinical groups.
- Evaluate a categorical exposure with multiple levels in an OLS model.
- Support post-hoc comparisons after an overall group effect is tested.

## When not to use

- The outcome is binary, ordinal, count, or time-to-event.
- Repeated measures or clustered observations require mixed models.
- Severe non-normality or variance heterogeneity makes nonparametric or robust methods more appropriate.

## Python dependencies

Use Python-native libraries for this workflow: `pandas`, `numpy`, `statsmodels`, `scipy`, `seaborn`.

## Data and assumptions

- Continuous outcome with independent observations.
- Approximately normal residuals within model groups.
- Reasonably homogeneous variances or a justified robust alternative.
- Group coding is categorical and reference levels are clinically meaningful.

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
import statsmodels.api as sm
from statsmodels.formula.api import ols

# df contains columns: dose_group, ldl_change
model = ols("ldl_change ~ C(dose_group)", data=df).fit()
anova_table = sm.stats.anova_lm(model, typ=2)
print(anova_table)

print(model.summary())
```

## Reporting guidance

Report the analysis population, missing-data handling, method variant, effect estimate, confidence interval when available, test statistic or model summary, p-value, and any assumption checks or limitations. Use clinical units and clinically meaningful labels rather than raw column names.
