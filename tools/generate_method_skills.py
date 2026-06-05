#!/usr/bin/env python3
"""Generate MVP Python medical statistics method skills from the catalog."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "tools" / "method_catalog.json"
REQUIRED_KEYS = {
    "path",
    "name",
    "title",
    "description",
    "use",
    "skip",
    "dependencies",
    "assumptions",
    "example",
}
STRING_KEYS = {"path", "name", "title", "description", "example"}
OPTIONAL_STRING_KEYS = {"reporting"}
LIST_KEYS = {"use", "skip", "dependencies", "assumptions", "workflow"}


def yaml_quote(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def bullet_list(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def validate_list_of_strings(item: dict[str, object], key: str) -> None:
    value = item.get(key)
    if not isinstance(value, list) or not value:
        raise TypeError(f"{item.get('path', '<unknown>')} {key} must be a non-empty list")
    if not all(isinstance(part, str) and part.strip() for part in value):
        raise TypeError(f"{item.get('path', '<unknown>')} {key} must contain only non-empty strings")


def validate_item(item: dict[str, object]) -> None:
    missing = sorted(REQUIRED_KEYS - set(item))
    if missing:
        raise KeyError(f"catalog item missing required keys: {', '.join(missing)}")

    for key in STRING_KEYS:
        value = item[key]
        if not isinstance(value, str) or not value.strip():
            raise TypeError(f"{item.get('path', '<unknown>')} {key} must be a non-empty string")

    for key in OPTIONAL_STRING_KEYS:
        if key in item and (not isinstance(item[key], str) or not item[key].strip()):
            raise TypeError(f"{item.get('path', '<unknown>')} {key} must be a non-empty string")

    for key in LIST_KEYS:
        if key in item:
            validate_list_of_strings(item, key)

    relative_path = Path(str(item["path"]))
    if relative_path.is_absolute() or ".." in relative_path.parts:
        raise ValueError(f"Refusing unsafe path: {relative_path}")
    if relative_path.name != "SKILL.md":
        raise ValueError(f"{relative_path} must end in SKILL.md")
    if "```" in str(item["example"]):
        raise ValueError(f"{relative_path} example must not contain fenced code markers")


def workflow_steps(item: dict[str, object]) -> str:
    default_steps = [
        "Confirm the clinical question, endpoint, exposure or grouping variable, and analysis population.",
        "Load data with `pandas`, check missingness, coding, outliers, and clinically impossible values.",
        "Choose the method variant that matches the design and assumptions.",
        "Run the Python analysis with transparent preprocessing and deterministic settings where relevant.",
        "Inspect diagnostics, assumption checks, and sensitivity analyses before interpreting estimates.",
        "Save tables and figures that can be reproduced from the same script or notebook.",
    ]
    steps = item.get("workflow", default_steps)
    return "\n".join(f"{index}. {step}" for index, step in enumerate(steps, start=1))


def render_skill(item: dict[str, object]) -> str:
    validate_item(item)

    dependency_text = ", ".join(f"`{dependency}`" for dependency in item["dependencies"])

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

{workflow_steps(item)}

## Minimal Python example

```python
{item["example"]}
```

## Reporting guidance

{item.get("reporting", "Report the analysis population, missing-data handling, method variant, effect estimate, confidence interval when available, test statistic or model summary, p-value, and any assumption checks or limitations. Use clinical units and clinically meaningful labels rather than raw column names.")}
"""


def load_catalog() -> list[dict[str, object]]:
    with CATALOG_PATH.open(encoding="utf-8") as file:
        catalog = json.load(file)

    if not isinstance(catalog, list):
        raise TypeError("method_catalog.json must contain a JSON array")
    for item in catalog:
        validate_item(item)
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
