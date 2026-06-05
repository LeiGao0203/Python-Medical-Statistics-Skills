---
name: "medical-stat-python-multi-reg"
description: "Use for medical statistics in Python when modeling continuous clinical outcomes with multivariable statsmodels OLS regression."
---

# Python Multiple Linear Regression Skill

## When to use

- Estimate adjusted associations with a continuous outcome.
- Control for pre-specified confounders in an OLS model.
- Report beta coefficients, confidence intervals, and residual diagnostics.

## When not to use

- Outcome is binary, count, ordinal, or time-to-event.
- Repeated measures or clustered data require mixed or generalized estimating equations.
- Important nonlinear relationships are present but not modeled.

## Python dependencies

Use Python-native libraries for this workflow: `pandas`, `numpy`, `statsmodels`, `matplotlib`, `seaborn`.

## Data and assumptions

- Continuous outcome with approximately linear predictor relationships.
- Independent observations.
- Residuals are reasonably homoscedastic and approximately normal for inference.
- Covariates are selected based on clinical reasoning or a pre-specified analysis plan.

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
import statsmodels.formula.api as smf

# df contains columns: quality_score, treatment, age, baseline_score
model = smf.ols("quality_score ~ treatment + age + baseline_score", data=df).fit()
print(model.summary())
print(model.conf_int())
```

## Reporting guidance

Report the analysis population, missing-data handling, method variant, effect estimate, confidence interval when available, test statistic or model summary, p-value, and any assumption checks or limitations. Use clinical units and clinically meaningful labels rather than raw column names.
