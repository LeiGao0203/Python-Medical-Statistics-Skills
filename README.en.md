# Python Medical Statistics Skills

[中文](README.md)

Python Medical Statistics Skills is a collection of AI coding agent skills for medical statistics and Python data analysis. The project uses a generic `SKILL.md` structure, so it can be used by Codex and by other coding agents that support skill directories.

## Project Identity

This project provides medical research oriented statistical method guidance, Python analysis workflows, script templates, and Jupyter notebook workflows. It is designed to help agents support data checks, statistical modeling, result tables, visualization, and reproducible analysis.

The recommended Python stack includes:

- `pandas`
- `numpy`
- `scipy`
- `statsmodels`
- `scikit-learn`
- `lifelines`
- `matplotlib`
- `seaborn`

## Contents

- `basic-stats`: Basic statistical method skills, including t-tests, chi-square tests, ANOVA, correlation analysis, nonparametric tests, ROC, and sample size estimation.
- `advanced-stats`: Advanced statistical method skills, including logistic regression, multivariable regression, survival analysis, and PCA.
- `literature-stats`: Literature and study-design oriented skills, including propensity score matching and subgroup analysis.
- `python-script`: Plain Python script workflow for reproducible medical statistics analysis.
- `jupyter-notebook`: Jupyter notebook workflow for exploration, teaching, and reporting.
- `example`: Runnable example project.

## Recommended Workflows

- Use `python-script` to create reproducible plain Python analysis scripts for formal analysis, batch runs, and version control.
- Use `jupyter-notebook` to create exploratory analyses, tutorial notebooks, or experiment records.
- Call method-specific skills according to the research question, such as `basic-stats/ttest`, `advanced-stats/logistic-reg`, or `advanced-stats/survival`.

## Example

`example/lung-cancer` provides a fully synthetic lung cancer risk analysis example. The workflow covers data checks, Table 1, t-test, logistic regression, ROC/AUC, and figure generation, making it a practical smoke test for the project medical statistics analysis workflow.

From the repository root, install the example dependencies first and then run the analysis:

```bash
python3 -m pip install -r requirements.txt
python3 example/lung-cancer/analysis/analysis.py
```

## Install

For Codex, the default target is `${CODEX_HOME:-$HOME/.codex}/skills`:

```bash
curl -fsSL https://raw.githubusercontent.com/LeiGao0203/Python-Medical-Statistics-Skills/main/install.sh | bash
```

For other coding agents, set `AGENT_SKILLS_DIR` to the agent skill directory:

```bash
curl -fsSL https://raw.githubusercontent.com/LeiGao0203/Python-Medical-Statistics-Skills/main/install.sh | AGENT_SKILLS_DIR=/path/to/agent/skills bash
```

## License

Original workflow, tooling, examples, and documentation in this project are licensed under [Apache-2.0](LICENSE). Adapted method guidance is licensed under CC BY-SA 4.0 where applicable; see [NOTICE](NOTICE) for details.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.
