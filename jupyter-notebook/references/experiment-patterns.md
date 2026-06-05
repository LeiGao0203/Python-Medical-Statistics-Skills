# Experiment Patterns

Use experiment notebooks for reproducible analysis work where the main product is evidence, not instruction.

## Recommended Flow

1. Title and objective
2. Study question and estimand
3. Data source and cohort definition
4. Pre-specified analysis plan
5. Data loading and validation
6. Primary analysis
7. Sensitivity checks
8. Results summary and limitations

## Medical Statistics Conventions

- Write the hypothesis before inspecting outcomes.
- Define the analysis population, exclusions, and missing-data handling.
- Separate descriptive statistics from inferential models.
- Report effect estimates with uncertainty intervals, not only p-values.
- Keep transformations traceable and avoid overwriting raw inputs.

## Reproducibility Notes

- Record package versions when results may depend on numerical routines.
- Use deterministic seeds for simulation, bootstrapping, or resampling.
- Store derived outputs under a clearly named output directory.
- Make assumptions visible near the code that relies on them.
