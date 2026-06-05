---
name: "medical-stat-python-sample-size"
description: "Use for medical statistics in Python when planning power or sample size with statsmodels.stats.power for t-tests, proportions, or ANOVA."
---

# Python Sample Size Skill

## When to use

- Estimate sample size for planned medical studies.
- Compute achieved power for simple designs.
- Translate clinically meaningful differences into standardized effect sizes.

## When not to use

- Complex clustered, adaptive, survival, or noninferiority designs require specialized methods.
- Inputs are not clinically justified or are based only on desired significance.
- Regulatory or protocol work needs a statistician-approved calculation plan.

## Python dependencies

Use Python-native libraries for this workflow: `numpy`, `statsmodels`.

## Data and assumptions

- Primary endpoint, allocation ratio, alpha, power, and effect size are pre-specified.
- Effect sizes come from clinically meaningful differences or reliable prior data.
- Dropout, missingness, and design effects are added after base sample size calculation.
- One-sided versus two-sided testing is justified.

## Standard workflow

1. Confirm the clinical question, endpoint, exposure or grouping variable, and analysis population.
2. Load data with `pandas`, check missingness, coding, outliers, and clinically impossible values.
3. Choose the method variant that matches the design and assumptions.
4. Run the Python analysis with transparent preprocessing and deterministic settings where relevant.
5. Inspect diagnostics, assumption checks, and sensitivity analyses before interpreting estimates.
6. Save tables and figures that can be reproduced from the same script or notebook.

## Minimal Python example

```python
from statsmodels.stats.power import TTestIndPower

analysis = TTestIndPower()
# Cohen's d = clinically meaningful mean difference / pooled SD
n_per_group = analysis.solve_power(effect_size=0.5, alpha=0.05, power=0.8, ratio=1.0, alternative="two-sided")
print(f"Required sample size per group: {n_per_group:.1f}")
```

## Reporting guidance

Report the analysis population, missing-data handling, method variant, effect estimate, confidence interval when available, test statistic or model summary, p-value, and any assumption checks or limitations. Use clinical units and clinically meaningful labels rather than raw column names.
