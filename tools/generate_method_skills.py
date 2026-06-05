#!/usr/bin/env python3
"""Generate MVP Python medical statistics method skills from the catalog."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "tools" / "method_catalog.json"


def yaml_quote(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def bullet_list(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def render_skill(item: dict[str, object]) -> str:
    dependencies = item["dependencies"]
    if not isinstance(dependencies, list):
        raise TypeError(f"{item['path']} dependencies must be a list")

    dependency_text = ", ".join(f"`{dependency}`" for dependency in dependencies)

    return f"""---
name: {yaml_quote(str(item["name"]))}
description: {yaml_quote(str(item["description"]))}
---

# {item["title"]}

## When to use

{bullet_list(item["use"])}

## When not to use

{bullet_list(item["skip"])}

## Python dependencies

Use Python-native libraries for this workflow: {dependency_text}.

## Data and assumptions

{bullet_list(item["assumptions"])}

## Standard workflow

1. Confirm the clinical question, endpoint, exposure or grouping variable, and analysis population.
2. Load data with `pandas`, check missingness, coding, outliers, and clinically impossible values.
3. Choose the method variant that matches the design and assumptions.
4. Run the Python analysis with transparent preprocessing and deterministic settings where relevant.
5. Inspect diagnostics, assumption checks, and sensitivity analyses before interpreting estimates.
6. Save tables and figures that can be reproduced from the same script or notebook.

## Minimal Python example

```python
{item["example"]}
```

## Reporting guidance

Report the analysis population, missing-data handling, method variant, effect estimate, confidence interval when available, test statistic or model summary, p-value, and any assumption checks or limitations. Use clinical units and clinically meaningful labels rather than raw column names.
"""


def load_catalog() -> list[dict[str, object]]:
    with CATALOG_PATH.open(encoding="utf-8") as file:
        catalog = json.load(file)

    if not isinstance(catalog, list):
        raise TypeError("method_catalog.json must contain a JSON array")
    return catalog


def main() -> int:
    for item in load_catalog():
        relative_path = Path(str(item["path"]))
        if relative_path.is_absolute() or ".." in relative_path.parts:
            raise ValueError(f"Refusing unsafe path: {relative_path}")

        target = ROOT / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render_skill(item), encoding="utf-8")
        print(f"Wrote {relative_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
