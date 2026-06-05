---
name: "medical-stat-python-logistic-reg"
description: "Use for medical statistics in Python when modeling binary clinical outcomes with statsmodels logistic regression and reporting odds ratios."
---

# Python Logistic Regression Skill

## When to use

- Model binary outcomes such as response, complication, or mortality.
- Estimate adjusted odds ratios for exposures and covariates.
- Assess interaction terms or subgroup effects on the log-odds scale.

## When not to use

- Outcome is common and risk ratios are required without approximation.
- Events are too sparse for the number of predictors.
- Data are clustered or longitudinal without a plan for correlated outcomes.

## Python dependencies

Use Python-native libraries for this workflow: `pandas`, `numpy`, `statsmodels`, `scikit-learn`, `seaborn`.

## Data and assumptions

- Binary outcome is correctly coded.
- Predictors are pre-specified and clinically meaningful.
- Continuous predictors have plausible functional form on the logit scale.
- No severe separation, collinearity, or overfitting.

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
import statsmodels.formula.api as smf

# df contains columns: remission, treatment, age, baseline_score
model = smf.logit("remission ~ treatment + age + baseline_score", data=df).fit()
params = model.params
conf = model.conf_int()
odds_ratios = np.exp(params)
ci = np.exp(conf)
summary = pd.DataFrame({"OR": odds_ratios, "CI_low": ci[0], "CI_high": ci[1], "p_value": model.pvalues})
print(summary)
```

## Reporting guidance

Report the analysis population, missing-data handling, method variant, effect estimate, confidence interval when available, test statistic or model summary, p-value, and any assumption checks or limitations. Use clinical units and clinically meaningful labels rather than raw column names.
