---
name: "medical-stat-python-nonparametric"
description: "Use for medical statistics in Python when continuous or ordinal outcomes need rank-based scipy tests such as Mann-Whitney U, Wilcoxon, or Kruskal-Wallis."
---

# Python Nonparametric Tests Skill

## When to use

- Compare skewed continuous or ordinal outcomes between independent groups.
- Analyze paired non-normal measurements with Wilcoxon signed-rank.
- Compare three or more independent groups with Kruskal-Wallis.

## When not to use

- The clinical question needs adjusted estimates or covariate control.
- The outcome is binary or categorical.
- Large sample parametric models with diagnostics are more informative for the target estimand.

## Python dependencies

Use Python-native libraries for this workflow: `pandas`, `numpy`, `scipy`, `seaborn`.

## Data and assumptions

- Observations are independent unless using paired Wilcoxon.
- Rank-based tests compare distributions and may not be simple median tests.
- Groups are defined before looking at outcomes.
- Ties and zero differences are handled consistently.

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

# df contains columns: treatment_group, pain_score
treated = df.loc[df["treatment_group"] == "treated", "pain_score"].dropna()
control = df.loc[df["treatment_group"] == "control", "pain_score"].dropna()

mw = stats.mannwhitneyu(treated, control, alternative="two-sided")
print(f"Mann-Whitney U={mw.statistic:.1f}, p={mw.pvalue:.4f}")

# For three groups:
groups = [g["pain_score"].dropna() for _, g in df.groupby("dose_group")]
kw = stats.kruskal(*groups)
print(f"Kruskal-Wallis H={kw.statistic:.3f}, p={kw.pvalue:.4f}")
```

## Reporting guidance

Report the analysis population, missing-data handling, method variant, effect estimate, confidence interval when available, test statistic or model summary, p-value, and any assumption checks or limitations. Use clinical units and clinically meaningful labels rather than raw column names.
