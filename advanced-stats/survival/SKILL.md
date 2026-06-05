---
name: "medical-stat-python-survival"
description: "Use for medical statistics in Python when analyzing time-to-event outcomes with lifelines Kaplan-Meier and Cox proportional hazards workflows."
---

# Python Survival Analysis Skill

## When to use

- Estimate survival curves for time-to-event clinical outcomes.
- Fit Cox proportional hazards models for adjusted hazard ratios.
- Report censoring-aware estimates and survival probabilities.

## When not to use

- Follow-up time or censoring status is unavailable or unreliable.
- Competing risks are central and require competing-risk methods.
- Proportional hazards are clearly violated without a planned alternative.

## Python dependencies

Use Python-native libraries for this workflow: `pandas`, `numpy`, `lifelines`, `matplotlib`, `seaborn`.

## Data and assumptions

- Time origin, event definition, and censoring rules are defined.
- Censoring is non-informative conditional on included covariates.
- Cox models assume proportional hazards unless time-varying effects are modeled.
- Follow-up units are consistent across records.
- Categorical Cox covariates are encoded before fitting.

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
from lifelines import CoxPHFitter, KaplanMeierFitter

# df contains columns: followup_months, event, treatment, age
kmf = KaplanMeierFitter()
for group, part in df.groupby("treatment"):
    kmf.fit(part["followup_months"], event_observed=part["event"], label=str(group))
    print(kmf.survival_function_.tail(1))

cox_df = pd.get_dummies(df[["followup_months", "event", "treatment", "age"]], columns=["treatment"], drop_first=True)
cph = CoxPHFitter()
cph.fit(cox_df, duration_col="followup_months", event_col="event")
cph.print_summary()
```

## Reporting guidance

Report the analysis population, missing-data handling, method variant, effect estimate, confidence interval when available, test statistic or model summary, p-value, and any assumption checks or limitations. Use clinical units and clinically meaningful labels rather than raw column names.
