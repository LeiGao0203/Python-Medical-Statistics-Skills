#!/usr/bin/env python3
"""Create a notebook from the bundled scaffold templates."""

import argparse
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a medical statistics notebook scaffold.")
    parser.add_argument("--kind", choices=("experiment", "tutorial"), required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--out", required=True, help="Output .ipynb path")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    script_dir = Path(__file__).resolve().parent
    template_path = script_dir.parent / "assets" / f"{args.kind}-template.ipynb"
    out_path = Path(args.out)

    with template_path.open("r", encoding="utf-8") as handle:
        notebook = json.load(handle)

    notebook["cells"][0] = {
        "cell_type": "markdown",
        "metadata": {},
        "source": [f"# {args.title}\n"],
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(notebook, handle, ensure_ascii=False, indent=2)
        handle.write("\n")

    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
