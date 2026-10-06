"""Local command line analysis of a user-supplied order CSV."""

import argparse
import json
from pathlib import Path

from .analysis import analyze_orders, load_orders


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="foodhub-analyze")
    parser.add_argument("csv", type=Path, help="Path to an authorized order CSV")
    parser.add_argument("--output", type=Path, help="Save aggregate metrics as JSON")
    parser.add_argument("--charts", type=Path, help="Save three PNG charts in this directory")
    args = parser.parse_args(argv)
    try:
        frame = load_orders(args.csv)
        result = analyze_orders(frame)
        rendered = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(rendered, encoding="utf-8")
            print(f"Saved {args.output}")
        else:
            print(rendered)
        if args.charts:
            from .charts import save_charts
            for path in save_charts(frame, args.charts):
                print(f"Saved {path}")
        return 0
    except (FileNotFoundError, ValueError) as exc:
        parser.exit(2, f"error: {exc}\n")
