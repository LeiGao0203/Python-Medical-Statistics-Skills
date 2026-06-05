---
name: "medical-stat-python-ps-matching"
description: "Use for medical literature statistics in Python when estimating treatment effects in observational studies with propensity scores and nearest-neighbor matching."
---

# Python Propensity Score Matching Skill

## When to use

- Estimate propensity scores for treatment assignment in observational medical data.
- Perform nearest-neighbor matching and assess covariate balance.
- Prepare matched cohort summaries for manuscripts.

## When not to use

- Treatment assignment is randomized and matching is unnecessary.
- Important confounders are missing or measured after treatment.
- There is poor overlap or positivity violation between treatment groups.

## Python dependencies

Use Python-native libraries for this workflow: `pandas`, `numpy`, `statsmodels`, `scikit-learn`, `matplotlib`, `seaborn`.

## Data and assumptions

- All key confounders are measured before treatment.
- Treatment groups have sufficient propensity score overlap.
- Matching method, caliper, replacement, and estimand are pre-specified.
- Balance is checked after matching before outcome analysis.

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
from sklearn.neighbors import NearestNeighbors

# df contains: treated (0/1), age, sex, severity, outcome
ps_model = smf.logit("treated ~ age + sex + severity", data=df).fit(disp=False)
df = df.assign(propensity=ps_model.predict(df))

treated = df[df["treated"] == 1]
controls = df[df["treated"] == 0]
nn = NearestNeighbors(n_neighbors=1).fit(controls[["propensity"]])
distances, indices = nn.kneighbors(treated[["propensity"]])
matched_controls = controls.iloc[indices.ravel()].copy()
matched = pd.concat([treated.reset_index(drop=True), matched_controls.reset_index(drop=True)], keys=["treated", "control"])
print(matched.groupby(level=0)["propensity"].describe())
```

## Reporting guidance

Report the analysis population, missing-data handling, method variant, effect estimate, confidence interval when available, test statistic or model summary, p-value, and any assumption checks or limitations. Use clinical units and clinically meaningful labels rather than raw column names.
