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

1. Define the endpoint, primary comparison, alpha, target power, allocation ratio, and planned test before calculating sample size.
2. Justify the clinically meaningful effect size from prior literature, pilot data, or clinical consensus.
3. Choose the statsmodels power class that matches the design, such as TTestIndPower for two independent means.
4. Adjust for dropout, unequal allocation, clustering, repeated measures, or design effects when the planned design requires it.
5. Report every assumption clearly so reviewers can reproduce and challenge the calculation.

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
