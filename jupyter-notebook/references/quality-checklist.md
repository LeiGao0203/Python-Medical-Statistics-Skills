# Quality Checklist

Use this checklist before publishing, teaching from, or committing a notebook.

## Structure

- The title describes the analysis or lesson clearly.
- The objective or learning goals are stated before code begins.
- Imports are centralized and easy to rerun.
- The notebook can run from a clean kernel from top to bottom.

## Statistical Quality

- The target population, variables, and outcome definitions are explicit.
- Assumptions are documented before the relevant analysis.
- Missing data and exclusions are described.
- Estimates include appropriate uncertainty measures where applicable.
- Conclusions stay within the limits of the design and data.

## Reproducibility

- Paths are relative or configurable.
- Random processes use fixed seeds.
- External data requirements are documented.
- Generated outputs are named and reproducible.

## Privacy and Review

- No protected health information appears in code, markdown, outputs, or filenames.
- Example data is synthetic, public, or de-identified.
- Large outputs and transient files are not committed.
- The final notebook has been rendered or reopened to confirm valid JSON.
