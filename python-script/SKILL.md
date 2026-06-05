---
name: "python-script"
description: "Use when the user asks for Python scripts (`.py`), command-line Python workflows, reproducible medical statistics analysis scripts, or explicitly says they do not want notebooks. Create top-to-bottom Python analysis scripts using pandas, scipy, statsmodels, scikit-learn, lifelines, matplotlib, and seaborn as needed."
---

# Python Script Skill

Create reproducible Python medical statistics workflows as scripts that can be run from the command line. Prefer a single `analysis.py` for focused analyses; use a larger `analysis/` layout only when the task naturally needs separate modules, reusable helpers, configuration, or multiple outputs.

## When to use

Use this skill when the user asks for:

- A `.py` file, command-line workflow, or script-first analysis.
- A reproducible medical statistics pipeline that should run top to bottom.
- Batch processing, scheduled work, or analysis that should not depend on notebook state.
- A script instead of a notebook, including explicit requests such as "do not use Jupyter".

## Default output shape

For most requests, create:

```text
analysis.py
```

For larger analyses, create:

```text
analysis/
├── analysis.py
├── data/
├── outputs/
└── src/
```

Keep the entry point clear. `analysis.py` should load data, validate inputs, run the analysis, save outputs, and print a concise completion summary.

## Workflow

1. Clarify inputs, endpoints, grouping variables, covariates, and expected outputs when they are not already specified.
2. Build a top-to-bottom structure: imports, constants/paths, data loading, cleaning, validation, statistical analysis, visualization, and output writing.
3. Use the right dependencies for the analysis: `pandas`, `numpy`, `scipy.stats`, `statsmodels`, `scikit-learn`, `lifelines`, `matplotlib`, and `seaborn` as needed.
4. Save reproducible outputs under `outputs/`, such as cleaned data, model summaries, tables, figures, and logs.
5. Make the script runnable from a clean shell with the command that matches the chosen layout:

```bash
# Single-file layout
python analysis.py

# Larger project layout, run from the parent folder
python analysis/analysis.py
```

6. Validate the script by running the matching command and fixing any runtime, path, import, or output errors.

## Style

- Keep script state explicit: no hidden notebook variables, implicit working-directory assumptions, or interactive-only steps.
- Prefer named functions for repeated work, but keep short one-off analyses readable from top to bottom.
- Use deterministic seeds for simulations, resampling, train/test splits, and model workflows.
- Print compact progress messages and final output paths.
- Use `argparse` when users need configurable input files, output directories, or analysis options.
