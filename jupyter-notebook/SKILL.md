---
name: "python-jupyter-notebook"
description: "Use when the user asks to create, scaffold, or edit Jupyter notebooks (`.ipynb`) for Python medical statistics experiments, exploratory analyses, or tutorials. Prefer the bundled templates and run `scripts/new_notebook.py` to generate a clean starting notebook."
---

# Python Jupyter Notebook Skill

Create, scaffold, and edit Jupyter notebooks for Python medical statistics experiments, exploratory analyses, and tutorials. Prefer the bundled templates so notebooks start with a consistent structure, clear metadata, and reusable quality checks.

## When to use

Use this skill when the user asks for:

- A Jupyter notebook, `.ipynb` file, tutorial notebook, or exploratory analysis.
- Iterative statistical experiments where intermediate inspection matters.
- Teaching material that benefits from narrative cells, examples, and plots.
- Editing or extending an existing Python medical statistics notebook.

## Decision tree

- If the user asks for a reproducible command-line script or explicitly rejects notebooks, use the `python-script` skill.
- If the user asks for exploratory analysis, experiments, visual walkthroughs, or tutorials, use this skill.
- If the notebook will later become production analysis, keep cells ordered so the work can be converted into `analysis.py`.

## Scaffold

Create experiment notebooks with:

```bash
python "$CODEX_HOME/skills/jupyter-notebook/scripts/new_notebook.py" --kind experiment --output analysis.ipynb
```

Create tutorial notebooks with:

```bash
python "$CODEX_HOME/skills/jupyter-notebook/scripts/new_notebook.py" --kind tutorial --output tutorial.ipynb
```

If `$CODEX_HOME` is unavailable, resolve the skill directory first and run the same `scripts/new_notebook.py` helper from that location.

## Workflow

1. Choose `experiment` for exploratory medical statistics work and `tutorial` for teaching-oriented notebooks.
2. Scaffold with `scripts/new_notebook.py` before adding analysis-specific content.
3. Keep notebooks executable from top to bottom with imports, data loading, cleaning, analysis, visualization, and interpretation in order.
4. Use Python dependencies that fit the task, commonly `pandas`, `numpy`, `scipy.stats`, `statsmodels`, `scikit-learn`, `lifelines`, `matplotlib`, and `seaborn`.
5. Save important outputs outside the notebook when needed, especially figures, tables, fitted model summaries, and derived datasets.
6. Validate by running the notebook end to end or using the repository's notebook execution workflow when available.

## References

- `references/notebook-structure.md` for expected notebook organization.
- `references/experiment-patterns.md` for experiment-oriented analysis flow.
- `references/tutorial-patterns.md` for tutorial narrative and examples.
- `references/quality-checklist.md` before considering a notebook complete.
