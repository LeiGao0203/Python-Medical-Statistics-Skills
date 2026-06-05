"""Deterministic synthetic lung cancer risk analysis example."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.formula.api as smf
from scipy import stats
from sklearn.metrics import roc_auc_score, roc_curve


SEED = 20260605
N_PATIENTS = 600

ANALYSIS_DIR = Path(__file__).resolve().parent
EXAMPLE_DIR = ANALYSIS_DIR.parent
DATA_DIR = EXAMPLE_DIR / "data"
DATA_PATH = DATA_DIR / "synthetic_lung_cancer.csv"
OUTPUT_DIR = ANALYSIS_DIR / "outputs"
TABLES_DIR = OUTPUT_DIR / "tables"
FIGURES_DIR = OUTPUT_DIR / "figures"


def ensure_directories() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)


def sigmoid(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-x))


def generate_synthetic_lung_cancer_data(path: Path) -> pd.DataFrame:
    rng = np.random.default_rng(SEED)

    age = np.clip(rng.normal(64, 10, N_PATIENTS).round(), 40, 88).astype(int)
    sex = rng.choice(["Female", "Male"], size=N_PATIENTS, p=[0.48, 0.52])
    smoking_status = rng.choice(
        ["Never", "Former", "Current"],
        size=N_PATIENTS,
        p=[0.34, 0.40, 0.26],
    )

    pack_years = np.zeros(N_PATIENTS)
    former = smoking_status == "Former"
    current = smoking_status == "Current"
    pack_years[former] = rng.gamma(shape=3.0, scale=8.0, size=former.sum())
    pack_years[current] = rng.gamma(shape=4.0, scale=9.0, size=current.sum())
    pack_years = np.clip(pack_years + rng.normal(0, 2.0, N_PATIENTS), 0, 95).round(1)

    copd = rng.binomial(1, sigmoid(-2.7 + 0.035 * pack_years + 0.018 * (age - 60)))
    asbestos_exposure = rng.binomial(1, 0.10 + 0.06 * (sex == "Male"))
    family_history = rng.binomial(1, 0.15, N_PATIENTS)
    chronic_cough = rng.binomial(1, sigmoid(-2.1 + 0.018 * pack_years + 0.55 * copd))
    weight_loss = rng.binomial(1, sigmoid(-2.6 + 0.012 * (age - 60) + 0.45 * chronic_cough))

    risk_linear_predictor = (
        -5.2
        + 0.035 * (age - 60)
        + 0.045 * pack_years
        + 0.55 * (smoking_status == "Former")
        + 0.95 * (smoking_status == "Current")
        + 0.70 * copd
        + 0.65 * asbestos_exposure
        + 0.55 * family_history
        + 0.65 * chronic_cough
        + 0.85 * weight_loss
    )
    lung_cancer_probability = sigmoid(risk_linear_predictor)
    lung_cancer = rng.binomial(1, lung_cancer_probability)

    df = pd.DataFrame(
        {
            "patient_id": np.arange(1, N_PATIENTS + 1),
            "age": age,
            "sex": sex,
            "smoking_status": smoking_status,
            "smoking_pack_years": pack_years,
            "copd": copd,
            "asbestos_exposure": asbestos_exposure,
            "family_history": family_history,
            "chronic_cough": chronic_cough,
            "weight_loss": weight_loss,
            "lung_cancer": lung_cancer,
        }
    )
    df.to_csv(path, index=False)
    return df


def load_or_create_data() -> pd.DataFrame:
    if not DATA_PATH.exists():
        generate_synthetic_lung_cancer_data(DATA_PATH)
    return pd.read_csv(DATA_PATH)


def print_data_checks(df: pd.DataFrame) -> None:
    print("Dataset shape:", df.shape)
    print("\nMissing values by column:")
    print(df.isna().sum().to_string())
    print("\nOutcome counts:")
    print(df["lung_cancer"].value_counts().sort_index().to_string())


def create_table1(df: pd.DataFrame) -> pd.DataFrame:
    continuous_vars = ["age", "smoking_pack_years"]
    binary_vars = [
        "copd",
        "asbestos_exposure",
        "family_history",
        "chronic_cough",
        "weight_loss",
    ]
    categorical_vars = ["sex", "smoking_status"]

    rows: list[dict[str, object]] = []

    for variable in continuous_vars:
        for outcome, group in df.groupby("lung_cancer"):
            rows.append(
                {
                    "variable": variable,
                    "level": "mean_sd",
                    "lung_cancer": outcome,
                    "n": group[variable].notna().sum(),
                    "summary": f"{group[variable].mean():.2f} ({group[variable].std(ddof=1):.2f})",
                }
            )

    for variable in binary_vars:
        for outcome, group in df.groupby("lung_cancer"):
            count = int(group[variable].sum())
            percent = 100 * count / len(group)
            rows.append(
                {
                    "variable": variable,
                    "level": "1",
                    "lung_cancer": outcome,
                    "n": len(group),
                    "summary": f"{count} ({percent:.1f}%)",
                }
            )

    for variable in categorical_vars:
        counts = (
            df.groupby(["lung_cancer", variable], observed=True)
            .size()
            .reset_index(name="count")
        )
        denominators = df.groupby("lung_cancer", observed=True).size().to_dict()
        for row in counts.itertuples(index=False):
            percent = 100 * row.count / denominators[row.lung_cancer]
            rows.append(
                {
                    "variable": variable,
                    "level": getattr(row, variable),
                    "lung_cancer": row.lung_cancer,
                    "n": denominators[row.lung_cancer],
                    "summary": f"{row.count} ({percent:.1f}%)",
                }
            )

    table1 = pd.DataFrame(rows)
    table1.to_csv(TABLES_DIR / "table1_by_lung_cancer.csv", index=False)
    return table1


def run_welch_ttest(df: pd.DataFrame) -> pd.DataFrame:
    exposed = df.loc[df["lung_cancer"] == 1, "smoking_pack_years"]
    unexposed = df.loc[df["lung_cancer"] == 0, "smoking_pack_years"]
    result = stats.ttest_ind(exposed, unexposed, equal_var=False)

    ttest_table = pd.DataFrame(
        [
            {
                "variable": "smoking_pack_years",
                "mean_lung_cancer_1": exposed.mean(),
                "mean_lung_cancer_0": unexposed.mean(),
                "mean_difference": exposed.mean() - unexposed.mean(),
                "t_statistic": result.statistic,
                "p_value": result.pvalue,
                "n_lung_cancer_1": exposed.shape[0],
                "n_lung_cancer_0": unexposed.shape[0],
            }
        ]
    )
    ttest_table.to_csv(TABLES_DIR / "ttest_smoking_pack_years.csv", index=False)
    return ttest_table


def fit_logistic_regression(df: pd.DataFrame):
    formula = (
        "lung_cancer ~ age + smoking_pack_years + C(sex) + "
        "C(smoking_status) + copd + asbestos_exposure + "
        "family_history + chronic_cough + weight_loss"
    )
    model = smf.logit(formula, data=df).fit(disp=False)

    conf = model.conf_int()
    odds_ratios = pd.DataFrame(
        {
            "term": model.params.index,
            "odds_ratio": np.exp(model.params.values),
            "ci_low": np.exp(conf[0].values),
            "ci_high": np.exp(conf[1].values),
            "p_value": model.pvalues.values,
        }
    )
    odds_ratios.to_csv(TABLES_DIR / "logistic_regression_or.csv", index=False)
    return model, odds_ratios


def compute_roc(df: pd.DataFrame, model) -> pd.DataFrame:
    predicted_probability = model.predict(df)
    auc = roc_auc_score(df["lung_cancer"], predicted_probability)
    fpr, tpr, thresholds = roc_curve(df["lung_cancer"], predicted_probability)

    roc_summary = pd.DataFrame(
        [
            {
                "model": "multivariable_logistic_regression",
                "roc_auc": auc,
                "n": df.shape[0],
                "events": int(df["lung_cancer"].sum()),
            }
        ]
    )
    roc_summary.to_csv(TABLES_DIR / "roc_auc.csv", index=False)

    roc_points = pd.DataFrame(
        {
            "threshold": thresholds,
            "sensitivity": tpr,
            "specificity": 1 - fpr,
            "false_positive_rate": fpr,
            "true_positive_rate": tpr,
        }
    )
    roc_points.to_csv(TABLES_DIR / "roc_curve_points.csv", index=False)
    return roc_summary


def save_figures(df: pd.DataFrame, model) -> None:
    sns.set_theme(style="whitegrid")

    plt.figure(figsize=(7, 5))
    sns.boxplot(
        data=df,
        x="lung_cancer",
        y="smoking_pack_years",
        palette="Set2",
    )
    plt.xlabel("Lung cancer")
    plt.ylabel("Smoking pack-years")
    plt.title("Smoking Pack-Years by Lung Cancer Status")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "smoking_pack_years_boxplot.png", dpi=150)
    plt.close()

    predicted_probability = model.predict(df)
    auc = roc_auc_score(df["lung_cancer"], predicted_probability)
    fpr, tpr, _ = roc_curve(df["lung_cancer"], predicted_probability)

    plt.figure(figsize=(6, 6))
    plt.plot(fpr, tpr, label=f"AUC = {auc:.3f}", color="#1f77b4", linewidth=2)
    plt.plot([0, 1], [0, 1], linestyle="--", color="gray", linewidth=1)
    plt.xlabel("False positive rate")
    plt.ylabel("True positive rate")
    plt.title("ROC Curve for Lung Cancer Risk Model")
    plt.legend(loc="lower right")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "roc_curve.png", dpi=150)
    plt.close()


def main() -> None:
    ensure_directories()
    df = load_or_create_data()

    print_data_checks(df)
    create_table1(df)
    run_welch_ttest(df)
    model, _ = fit_logistic_regression(df)
    roc_summary = compute_roc(df, model)
    save_figures(df, model)

    print("\nROC AUC:")
    print(roc_summary.to_string(index=False))
    print("\nSaved outputs:")
    print(f"- Tables: {TABLES_DIR}")
    print(f"- Figures: {FIGURES_DIR}")


if __name__ == "__main__":
    main()
