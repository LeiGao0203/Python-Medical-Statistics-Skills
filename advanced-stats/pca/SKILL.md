---
name: "medical-stat-python-pca"
description: "Use for medical statistics in Python when reducing correlated biomarkers, questionnaire items, or feature sets with standardized scikit-learn PCA."
---

# Python PCA Skill

## When to use

- Reduce many correlated continuous measurements into principal components.
- Explore biomarker or questionnaire structure before downstream modeling.
- Create explained-variance summaries and component loading tables.

## When not to use

- Variables are mostly categorical or on incomparable coding scales without preprocessing.
- The goal is supervised prediction; use a supervised modeling workflow.
- Interpretability of original variables is more important than dimension reduction.

## Python dependencies

Use Python-native libraries for this workflow: `pandas`, `numpy`, `scikit-learn`, `matplotlib`, `seaborn`.

## Data and assumptions

- Features are numeric and measured before outcomes when used for prediction.
- Variables are standardized before PCA unless scale intentionally carries meaning.
- Missing data are handled before fitting PCA.
- Component interpretation is checked against loadings and clinical context.

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
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

features = ["marker_a", "marker_b", "marker_c", "marker_d"]
X = df[features].dropna()
X_scaled = StandardScaler().fit_transform(X)

pca = PCA(n_components=2, random_state=0)
scores = pca.fit_transform(X_scaled)
loadings = pd.DataFrame(pca.components_.T, index=features, columns=["PC1", "PC2"])
print(pca.explained_variance_ratio_)
print(loadings)
```

## Reporting guidance

Report the analysis population, missing-data handling, method variant, effect estimate, confidence interval when available, test statistic or model summary, p-value, and any assumption checks or limitations. Use clinical units and clinically meaningful labels rather than raw column names.
