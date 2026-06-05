# Synthetic Lung Cancer Risk Analysis Example

This example is a fully synthetic lung cancer risk analysis workflow. It does not use an external clinical dataset, so it avoids dataset licensing constraints and can be run reproducibly from a clean checkout.

The script creates `example/lung-cancer/data/synthetic_lung_cancer.csv` when it is missing, then reloads it for analysis. The generated dataset contains demographic, exposure, symptom, and clinical-risk variables such as age, sex, smoking pack-years, COPD history, asbestos exposure, family history, chronic cough, and unintentional weight loss. The binary `lung_cancer` outcome is simulated from a fixed logistic-risk model with a deterministic random seed.

The analysis covers:

- Dataset shape, missingness, and outcome counts.
- Table 1 summaries by lung cancer status.
- Welch t-test for smoking pack-years by lung cancer status.
- Multivariable logistic regression with odds ratios and confidence intervals.
- ROC AUC estimation and ROC curve plotting.
- Exported CSV tables and PNG figures under `example/lung-cancer/analysis/outputs/`.

## Run

Install dependencies from the repository root:

```bash
python3 -m pip install -r requirements.txt
```

Run the example:

```bash
python3 example/lung-cancer/analysis/analysis.py
```

The generated synthetic dataset is saved under `example/lung-cancer/data/`. Analysis outputs are saved under `example/lung-cancer/analysis/outputs/tables/` and `example/lung-cancer/analysis/outputs/figures/`.
