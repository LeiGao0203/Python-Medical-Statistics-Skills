# %% [markdown]
# # Lung Cancer Survey — Comprehensive Medical Statistical Analysis
# 
# **Dataset**: Kaggle Lung Cancer Survey (309 observations, 16 variables)  
# **Outcome**: LUNG_CANCER (YES/NO)  
# **Analysis**: Descriptive statistics, chi-square tests, t-test/nonparametric tests,
# multivariable logistic regression, ROC/AUC analysis

# %% Imports and Configuration
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn.metrics import roc_auc_score, roc_curve
from sklearn.model_selection import cross_val_predict, StratifiedKFold
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Reproducibility
np.random.seed(42)
plt.rcParams.update({
    "figure.dpi": 150,
    "savefig.dpi": 300,
    "font.size": 10,
    "axes.titlesize": 12,
    "figure.figsize": (8, 6),
})

# Output directories
SCRIPT_DIR = Path(__file__).resolve().parent
EXAMPLE_DIR = SCRIPT_DIR.parent
BASE_DIR = SCRIPT_DIR / "outputs" / "kaggle_survey"
TABLE_DIR = BASE_DIR / "tables"
FIG_DIR = BASE_DIR / "figures"
TABLE_DIR.mkdir(parents=True, exist_ok=True)
FIG_DIR.mkdir(parents=True, exist_ok=True)

print("Output directories created:")
print(f"  Tables: {TABLE_DIR}")
print(f"  Figures: {FIG_DIR}")

# %% Data Loading and Cleaning
DATA_PATH = EXAMPLE_DIR / "data" / "survey lung cancer.csv"
df_raw = pd.read_csv(DATA_PATH)

print(f"Raw dataset: {df_raw.shape[0]} rows × {df_raw.shape[1]} columns")
print(f"Columns: {df_raw.columns.tolist()}")

# Fix trailing spaces in column names
df_raw.columns = df_raw.columns.str.strip()

# Recode binary variables: original 1=NO, 2=YES → 0/1
binary_vars = [
    "SMOKING", "YELLOW_FINGERS", "ANXIETY", "PEER_PRESSURE",
    "CHRONIC DISEASE", "FATIGUE", "ALLERGY", "WHEEZING",
    "ALCOHOL CONSUMING", "COUGHING", "SHORTNESS OF BREATH",
    "SWALLOWING DIFFICULTY", "CHEST PAIN",
]

df = df_raw.copy()
for col in binary_vars:
    df[col] = df[col].map({1: 0, 2: 1})

# Recode outcome: YES=1, NO=0
df["LUNG_CANCER_BIN"] = df["LUNG_CANCER"].map({"YES": 1, "NO": 0})

# Recode gender: M=1, F=0
df["GENDER_BIN"] = df["GENDER"].map({"M": 1, "F": 0})

print(f"\nMissing values:\n{df.isnull().sum()[df.isnull().sum() > 0]}")
if df.isnull().sum().sum() == 0:
    print("  No missing values detected.")

print(f"\nOutcome distribution:")
print(df["LUNG_CANCER"].value_counts())
print(f"\nAge range: {df['AGE'].min()} – {df['AGE'].max()}, Mean: {df['AGE'].mean():.1f}")

# %% Data Validation
# Verify recoding
print("=== Data Validation ===")
print(f"Binary variables range check (should be 0/1):")
for col in binary_vars:
    unique_vals = sorted(df[col].unique())
    status = "✓" if unique_vals == [0, 1] else "✗"
    print(f"  {status} {col}: {unique_vals}")

print(f"\nOutcome coding: {sorted(df['LUNG_CANCER_BIN'].unique())}")
print(f"Gender coding: {sorted(df['GENDER_BIN'].unique())}")
print(f"N(Lung Cancer=YES): {df['LUNG_CANCER_BIN'].sum()}, N(NO): {(df['LUNG_CANCER_BIN']==0).sum()}")

# %% Table 1: Descriptive Statistics by Lung Cancer Status
def compute_table1(df, group_col, binary_vars, continuous_vars):
    """Generate Table 1 with descriptive statistics stratified by group."""
    groups = df[group_col].unique()
    groups.sort()
    
    rows = []
    
    # Sample size row
    for g in groups:
        n = df[df[group_col] == g].shape[0]
        rows.append({"Variable": "N", "Group": g, "Value": str(n)})
    
    # Continuous variables: mean ± SD
    for var in continuous_vars:
        for g in groups:
            subset = df.loc[df[group_col] == g, var].dropna()
            rows.append({
                "Variable": var,
                "Group": g,
                "Value": f"{subset.mean():.1f} ± {subset.std():.1f}",
                "Mean": subset.mean(),
                "SD": subset.std(),
                "Median": subset.median(),
            })
    
    # Binary variables: n (%)
    for var in binary_vars:
        for g in groups:
            subset = df.loc[df[group_col] == g, var].dropna()
            n_yes = subset.sum()
            pct = 100 * n_yes / len(subset)
            rows.append({
                "Variable": var,
                "Group": g,
                "Value": f"{int(n_yes)} ({pct:.1f}%)",
                "n_yes": int(n_yes),
                "pct": pct,
            })
    
    return pd.DataFrame(rows)

table1_long = compute_table1(
    df, group_col="LUNG_CANCER",
    binary_vars=["GENDER_BIN"] + binary_vars,
    continuous_vars=["AGE"],
)

# Pivot for a readable format
table1_pivot = table1_long.pivot(index="Variable", columns="Group", values="Value")
table1_pivot = table1_pivot[["NO", "YES"]]  # order columns

# Reorder rows logically
var_order = ["N", "AGE", "GENDER_BIN"] + binary_vars
table1_pivot = table1_pivot.reindex(var_order)

# Rename for clinical labels
label_map = {
    "N": "N",
    "AGE": "Age, mean ± SD",
    "GENDER_BIN": "Male sex, n (%)",
    "SMOKING": "Smoking, n (%)",
    "YELLOW_FINGERS": "Yellow fingers, n (%)",
    "ANXIETY": "Anxiety, n (%)",
    "PEER_PRESSURE": "Peer pressure, n (%)",
    "CHRONIC DISEASE": "Chronic disease, n (%)",
    "FATIGUE": "Fatigue, n (%)",
    "ALLERGY": "Allergy, n (%)",
    "WHEEZING": "Wheezing, n (%)",
    "ALCOHOL CONSUMING": "Alcohol consuming, n (%)",
    "COUGHING": "Coughing, n (%)",
    "SHORTNESS OF BREATH": "Shortness of breath, n (%)",
    "SWALLOWING DIFFICULTY": "Swallowing difficulty, n (%)",
    "CHEST PAIN": "Chest pain, n (%)",
}
table1_pivot.index = table1_pivot.index.map(lambda x: label_map.get(x, x))
table1_pivot.columns = ["No Lung Cancer", "Lung Cancer"]

print("=== Table 1: Baseline Characteristics ===")
print(table1_pivot.to_string())
table1_pivot.to_csv(TABLE_DIR / "table1_descriptive.csv")
print(f"\nSaved: {TABLE_DIR / 'table1_descriptive.csv'}")

# %% Chi-Square Tests for Categorical Variables
print("=== Chi-Square / Fisher Exact Tests ===")
chi2_results = []

all_categorical = ["GENDER_BIN"] + binary_vars

for var in all_categorical:
    observed = pd.crosstab(df[var], df["LUNG_CANCER_BIN"])
    chi2, p_value, dof, expected = stats.chi2_contingency(observed)
    
    # Use Fisher exact for 2x2 tables with small expected counts
    method = "Chi-square"
    if observed.shape == (2, 2) and (expected < 5).any():
        _, p_value = stats.fisher_exact(observed)
        method = "Fisher exact"
    
    # Compute proportions in each group
    prop_cancer = df.loc[df["LUNG_CANCER_BIN"] == 1, var].mean()
    prop_no_cancer = df.loc[df["LUNG_CANCER_BIN"] == 0, var].mean()
    
    chi2_results.append({
        "Variable": label_map.get(var, var),
        "Prop_LungCancer": f"{prop_cancer:.3f}",
        "Prop_NoLungCancer": f"{prop_no_cancer:.3f}",
        "Test": method,
        "Chi2": f"{chi2:.3f}" if method == "Chi-square" else "—",
        "df": dof if method == "Chi-square" else "—",
        "p_value": p_value,
        "p_formatted": f"{p_value:.4f}" if p_value >= 0.0001 else "<0.0001",
        "Significant": "Yes" if p_value < 0.05 else "No",
    })

chi2_df = pd.DataFrame(chi2_results)
print(chi2_df[["Variable", "Prop_LungCancer", "Prop_NoLungCancer", "Test", "p_formatted", "Significant"]].to_string(index=False))
chi2_df.to_csv(TABLE_DIR / "chi_square_tests.csv", index=False)
print(f"\nSaved: {TABLE_DIR / 'chi_square_tests.csv'}")

# %% T-Test / Nonparametric Test for Age
print("=== Age Comparison Between Groups ===")

age_cancer = df.loc[df["LUNG_CANCER_BIN"] == 1, "AGE"].dropna()
age_no_cancer = df.loc[df["LUNG_CANCER_BIN"] == 0, "AGE"].dropna()

print(f"Lung Cancer (n={len(age_cancer)}): Mean={age_cancer.mean():.1f}, SD={age_cancer.std():.1f}, Median={age_cancer.median():.1f}")
print(f"No Lung Cancer (n={len(age_no_cancer)}): Mean={age_no_cancer.mean():.1f}, SD={age_no_cancer.std():.1f}, Median={age_no_cancer.median():.1f}")

# Normality check (Shapiro-Wilk)
_, p_norm_cancer = stats.shapiro(age_cancer)
_, p_norm_no = stats.shapiro(age_no_cancer)
print(f"\nShapiro-Wilk normality: Cancer p={p_norm_cancer:.4f}, No Cancer p={p_norm_no:.4f}")

# Welch's t-test
t_stat, t_pvalue = stats.ttest_ind(age_cancer, age_no_cancer, equal_var=False)
mean_diff = age_cancer.mean() - age_no_cancer.mean()
print(f"\nWelch t-test: t={t_stat:.3f}, p={t_pvalue:.4f}, Mean diff={mean_diff:.2f}")

# Mann-Whitney U (nonparametric alternative)
u_stat, u_pvalue = stats.mannwhitneyu(age_cancer, age_no_cancer, alternative="two-sided")
print(f"Mann-Whitney U: U={u_stat:.1f}, p={u_pvalue:.4f}")

# Save age comparison results
age_results = pd.DataFrame([{
    "Variable": "Age",
    "Cancer_Mean_SD": f"{age_cancer.mean():.1f} ± {age_cancer.std():.1f}",
    "NoCancer_Mean_SD": f"{age_no_cancer.mean():.1f} ± {age_no_cancer.std():.1f}",
    "Mean_Difference": f"{mean_diff:.2f}",
    "Welch_t": f"{t_stat:.3f}",
    "Welch_p": f"{t_pvalue:.4f}",
    "MannWhitney_U": f"{u_stat:.1f}",
    "MannWhitney_p": f"{u_pvalue:.4f}",
    "Shapiro_p_cancer": f"{p_norm_cancer:.4f}",
    "Shapiro_p_no_cancer": f"{p_norm_no:.4f}",
}])
age_results.to_csv(TABLE_DIR / "age_ttest_results.csv", index=False)
print(f"\nSaved: {TABLE_DIR / 'age_ttest_results.csv'}")

# %% Figure 1: Age Distribution Boxplot
fig, ax = plt.subplots(figsize=(7, 5))
sns.boxplot(data=df, x="LUNG_CANCER", y="AGE", palette=["#4ECDC4", "#FF6B6B"], ax=ax)
sns.stripplot(data=df, x="LUNG_CANCER", y="AGE", color="black", alpha=0.3, size=3, jitter=True, ax=ax)
ax.set_xlabel("Lung Cancer Status")
ax.set_ylabel("Age (years)")
ax.set_title("Age Distribution by Lung Cancer Status")

# Annotate with test result
sig_text = f"Welch t-test: p = {t_pvalue:.4f}" if t_pvalue >= 0.0001 else "Welch t-test: p < 0.0001"
ax.text(0.5, 0.97, sig_text, transform=ax.transAxes, ha="center", va="top", fontsize=9,
        bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow", alpha=0.8))

plt.tight_layout()
plt.savefig(FIG_DIR / "fig1_age_boxplot.png", bbox_inches="tight")
plt.close()
print(f"Saved: {FIG_DIR / 'fig1_age_boxplot.png'}")

# %% Multivariable Logistic Regression
print("=== Multivariable Logistic Regression ===")

# Prepare predictors — use all risk factors
predictor_cols = ["AGE", "GENDER_BIN"] + binary_vars

# Create analysis dataframe with clean column names (no spaces for formula)
df_model = df[predictor_cols + ["LUNG_CANCER_BIN"]].copy()
df_model.columns = [c.replace(" ", "_") for c in df_model.columns]
predictor_cols_clean = [c.replace(" ", "_") for c in predictor_cols]

# Fit logistic regression using statsmodels
formula = "LUNG_CANCER_BIN ~ " + " + ".join(predictor_cols_clean)
print(f"Formula: {formula}\n")

model = smf.logit(formula, data=df_model).fit(disp=0)
print(model.summary2())

# Extract odds ratios with 95% CI
params = model.params
conf = model.conf_int()
or_df = pd.DataFrame({
    "Variable": params.index,
    "Coefficient": params.values,
    "OR": np.exp(params.values),
    "OR_CI_low": np.exp(conf.iloc[:, 0].values),
    "OR_CI_high": np.exp(conf.iloc[:, 1].values),
    "p_value": model.pvalues.values,
})

# Remove intercept for reporting
or_df = or_df[or_df["Variable"] != "Intercept"].reset_index(drop=True)

# Add formatted columns
or_df["OR_formatted"] = or_df.apply(
    lambda r: f"{r['OR']:.2f} ({r['OR_CI_low']:.2f}–{r['OR_CI_high']:.2f})", axis=1
)
or_df["p_formatted"] = or_df["p_value"].apply(
    lambda p: f"{p:.4f}" if p >= 0.0001 else "<0.0001"
)
or_df["Significant"] = or_df["p_value"].apply(lambda p: "Yes" if p < 0.05 else "No")

# Map back to readable labels
var_label_map = {c.replace(" ", "_"): label_map.get(c, c) for c in predictor_cols}
var_label_map["AGE"] = "Age (per year)"
var_label_map["GENDER_BIN"] = "Male sex"
or_df["Label"] = or_df["Variable"].map(var_label_map)

print("\n=== Odds Ratios ===")
print(or_df[["Label", "OR_formatted", "p_formatted", "Significant"]].to_string(index=False))

or_df.to_csv(TABLE_DIR / "logistic_regression_ORs.csv", index=False)
print(f"\nSaved: {TABLE_DIR / 'logistic_regression_ORs.csv'}")

# Model fit statistics
print(f"\nModel fit: AIC={model.aic:.1f}, BIC={model.bic:.1f}")
print(f"Pseudo R²: {model.prsquared:.4f}")
print(f"Log-likelihood: {model.llf:.2f}")

model_fit = pd.DataFrame([{
    "AIC": model.aic,
    "BIC": model.bic,
    "Pseudo_R2": model.prsquared,
    "Log_Likelihood": model.llf,
    "N": int(model.nobs),
    "Converged": model.mle_retvals["converged"],
}])
model_fit.to_csv(TABLE_DIR / "logistic_model_fit.csv", index=False)

# %% Figure 2: Forest Plot of Odds Ratios
fig, ax = plt.subplots(figsize=(8, 7))

# Sort by OR for visual clarity
or_plot = or_df.sort_values("OR", ascending=True).reset_index(drop=True)
y_pos = range(len(or_plot))

# Plot point estimates and CIs
ax.errorbar(
    or_plot["OR"], y_pos,
    xerr=[or_plot["OR"] - or_plot["OR_CI_low"], or_plot["OR_CI_high"] - or_plot["OR"]],
    fmt="o", color="darkblue", ecolor="steelblue", elinewidth=2, capsize=4, markersize=6,
)

# Reference line at OR=1
ax.axvline(x=1, color="red", linestyle="--", linewidth=1, alpha=0.7)

ax.set_yticks(list(y_pos))
ax.set_yticklabels(or_plot["Label"])
ax.set_xlabel("Odds Ratio (95% CI)")
ax.set_title("Forest Plot: Adjusted Odds Ratios for Lung Cancer")
ax.set_xlim(left=0)

# Add OR text annotations
for i, row in or_plot.iterrows():
    idx = or_plot.index.get_loc(i)
    ax.text(
        ax.get_xlim()[1] * 0.92, idx,
        f"{row['OR']:.2f} ({row['OR_CI_low']:.2f}–{row['OR_CI_high']:.2f})",
        va="center", ha="right", fontsize=7, color="gray",
    )

plt.tight_layout()
plt.savefig(FIG_DIR / "fig2_forest_plot_OR.png", bbox_inches="tight")
plt.close()
print(f"Saved: {FIG_DIR / 'fig2_forest_plot_OR.png'}")

# %% ROC / AUC Analysis
print("=== ROC / AUC Analysis ===")

# Predicted probabilities from the fitted model
y_true = df_model["LUNG_CANCER_BIN"].values
y_pred_prob = model.predict(df_model[predictor_cols_clean])

# Training AUC (apparent performance)
auc_train = roc_auc_score(y_true, y_pred_prob)
fpr, tpr, thresholds = roc_curve(y_true, y_pred_prob)
print(f"Apparent AUC (training): {auc_train:.4f}")

# Cross-validated AUC (internal validation)
from sklearn.linear_model import LogisticRegression

X = df_model[predictor_cols_clean].values
y = df_model["LUNG_CANCER_BIN"].values

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
lr_sklearn = LogisticRegression(max_iter=1000, random_state=42)
y_cv_prob = cross_val_predict(lr_sklearn, X, y, cv=cv, method="predict_proba")[:, 1]
auc_cv = roc_auc_score(y, y_cv_prob)
fpr_cv, tpr_cv, thresholds_cv = roc_curve(y, y_cv_prob)
print(f"Cross-validated AUC (5-fold): {auc_cv:.4f}")

# Optimal threshold (Youden's J)
j_scores = tpr - fpr
optimal_idx = np.argmax(j_scores)
optimal_threshold = thresholds[optimal_idx]
optimal_sens = tpr[optimal_idx]
optimal_spec = 1 - fpr[optimal_idx]
print(f"\nOptimal threshold (Youden's J): {optimal_threshold:.4f}")
print(f"  Sensitivity: {optimal_sens:.4f}")
print(f"  Specificity: {optimal_spec:.4f}")

# ROC table
roc_table = pd.DataFrame({
    "Threshold": thresholds,
    "Sensitivity": tpr,
    "Specificity": 1 - fpr,
    "Youden_J": tpr - fpr,
})
roc_table.to_csv(TABLE_DIR / "roc_threshold_table.csv", index=False)

# AUC summary
auc_summary = pd.DataFrame([{
    "AUC_apparent": auc_train,
    "AUC_cross_validated_5fold": auc_cv,
    "Optimal_threshold": optimal_threshold,
    "Sensitivity_at_optimal": optimal_sens,
    "Specificity_at_optimal": optimal_spec,
}])
auc_summary.to_csv(TABLE_DIR / "auc_summary.csv", index=False)
print(f"\nSaved: {TABLE_DIR / 'roc_threshold_table.csv'}")
print(f"Saved: {TABLE_DIR / 'auc_summary.csv'}")

# %% Figure 3: ROC Curve
fig, ax = plt.subplots(figsize=(7, 7))

# Training ROC
ax.plot(fpr, tpr, color="darkblue", linewidth=2, label=f"Apparent AUC = {auc_train:.3f}")

# Cross-validated ROC
ax.plot(fpr_cv, tpr_cv, color="darkorange", linewidth=2, linestyle="--",
        label=f"5-fold CV AUC = {auc_cv:.3f}")

# Reference line
ax.plot([0, 1], [0, 1], color="gray", linestyle=":", linewidth=1, label="Reference (AUC = 0.5)")

# Mark optimal point
ax.scatter([fpr[optimal_idx]], [tpr[optimal_idx]], color="red", s=100, zorder=5,
           label=f"Optimal (Sens={optimal_sens:.2f}, Spec={optimal_spec:.2f})")

ax.set_xlabel("1 − Specificity (False Positive Rate)")
ax.set_ylabel("Sensitivity (True Positive Rate)")
ax.set_title("ROC Curve: Logistic Regression Model for Lung Cancer Prediction")
ax.legend(loc="lower right", fontsize=9)
ax.set_xlim([-0.02, 1.02])
ax.set_ylim([-0.02, 1.02])
ax.set_aspect("equal")
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(FIG_DIR / "fig3_roc_curve.png", bbox_inches="tight")
plt.close()
print(f"Saved: {FIG_DIR / 'fig3_roc_curve.png'}")

# %% Summary
print("\n" + "=" * 60)
print("ANALYSIS COMPLETE")
print("=" * 60)
print(f"\nDataset: {DATA_PATH.name}")
print(f"N = {len(df)} observations")
print(f"Outcome: Lung Cancer YES={df['LUNG_CANCER_BIN'].sum()}, NO={(df['LUNG_CANCER_BIN']==0).sum()}")
print(f"\nKey findings:")
print(f"  • Age comparison: Welch t p={t_pvalue:.4f}")
sig_vars = chi2_df[chi2_df["p_value"] < 0.05]["Variable"].tolist()
print(f"  • Significant chi-square variables ({len(sig_vars)}): {', '.join(sig_vars[:5])}{'...' if len(sig_vars) > 5 else ''}")
sig_or = or_df[or_df["p_value"] < 0.05]
print(f"  • Significant logistic regression predictors ({len(sig_or)}):")
for _, row in sig_or.iterrows():
    print(f"      {row['Label']}: OR={row['OR']:.2f} (p={row['p_value']:.4f})")
print(f"  • Model AUC: {auc_train:.3f} (apparent), {auc_cv:.3f} (5-fold CV)")

print(f"\nOutputs saved to:")
print(f"  Tables: {TABLE_DIR}")
for f in sorted(TABLE_DIR.glob("*.csv")):
    print(f"    • {f.name}")
print(f"  Figures: {FIG_DIR}")
for f in sorted(FIG_DIR.glob("*.png")):
    print(f"    • {f.name}")
