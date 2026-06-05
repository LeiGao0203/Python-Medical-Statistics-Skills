---
name: "medical-stat-python-subgroup-analysis"
description: "Use for medical literature statistics in Python when estimating subgroup effects, testing interaction terms, and preparing forest-plot-ready estimates."
---

# Python Subgroup Analysis Skill

## When to use

- Evaluate whether treatment effects differ across clinically defined subgroups.
- Fit interaction terms rather than relying only on within-subgroup p-values.
- Prepare subgroup estimates and confidence intervals for forest plots.

## When not to use

- Subgroups were chosen after inspecting outcomes without clear exploratory labeling.
- Sample sizes or event counts are too small for stable subgroup estimates.
- Multiple testing and interaction interpretation are not addressed.

## Python dependencies

Use Python-native libraries for this workflow: `pandas`, `numpy`, `statsmodels`, `matplotlib`, `seaborn`.

## Data and assumptions

- Subgroups are pre-specified and clinically meaningful.
- Interaction terms are interpreted on the model's scale.
- Each subgroup has enough data to estimate effects.
- Forest plots distinguish estimates from formal interaction tests.

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

# df contains: outcome, treatment, age_group, baseline_score
model = smf.ols("outcome ~ treatment * C(age_group) + baseline_score", data=df).fit()
print(model.summary())

rows = []
for subgroup, part in df.groupby("age_group"):
    subgroup_model = smf.ols("outcome ~ treatment + baseline_score", data=part).fit()
    estimate = subgroup_model.params["treatment"]
    ci_low, ci_high = subgroup_model.conf_int().loc["treatment"]
    rows.append({"subgroup": subgroup, "estimate": estimate, "ci_low": ci_low, "ci_high": ci_high})
forest_ready = pd.DataFrame(rows)
print(forest_ready)
```

## Reporting guidance

Report the analysis population, missing-data handling, method variant, effect estimate, confidence interval when available, test statistic or model summary, p-value, and any assumption checks or limitations. Use clinical units and clinically meaningful labels rather than raw column names.
