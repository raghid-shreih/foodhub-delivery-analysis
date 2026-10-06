"""Rebuild the checked chart gallery from an authorized private CSV.

Run from the repository root: python scripts/build_gallery.py data/foodhub_order.csv
"""

import argparse
from pathlib import Path

from foodhub_analysis.analysis import load_orders
from foodhub_analysis.charts import save_gallery


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv", type=Path)
    parser.add_argument("--output", type=Path, default=Path("assets"))
    args = parser.parse_args()
    for path in save_gallery(load_orders(args.csv), args.output):
        print(path)


if __name__ == "__main__":
    main()
