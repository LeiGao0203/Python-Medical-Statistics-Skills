#!/usr/bin/env python3
"""Create a clean starter Jupyter notebook from bundled templates."""

from __future__ import annotations

import argparse
import json
import uuid
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a starter notebook.")
    parser.add_argument("--kind", choices=["experiment", "tutorial"], required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--out", required=True)
    return parser.parse_args()


def template_path(kind: str) -> Path:
    root = Path(__file__).resolve().parents[1]
    return root / "assets" / f"{kind}-template.ipynb"


def ensure_cell_ids(cells: list[dict]) -> list[dict]:
    updated = []
    for cell in cells:
        copied = dict(cell)
        copied.setdefault("id", uuid.uuid4().hex[:8])
        updated.append(copied)
    return updated


def update_title(notebook: dict, title: str) -> dict:
    notebook = dict(notebook)
    cells = list(notebook.get("cells", []))
    if not cells:
        cells = [{"cell_type": "markdown", "metadata": {}, "source": []}]
    cells = ensure_cell_ids(cells)
    first = dict(cells[0])
    first.setdefault("id", uuid.uuid4().hex[:8])
    first["cell_type"] = "markdown"
    first["source"] = [f"# {title}\n"]
    cells[0] = first
    notebook["cells"] = cells
    return notebook


def main() -> None:
    args = parse_args()
    source = template_path(args.kind)
    notebook = json.loads(source.read_text(encoding="utf-8"))
    notebook = update_title(notebook, args.title)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(notebook, ensure_ascii=False, indent=2) + "
", encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
