# FoodHub Delivery Operations Analysis

A compact Python case study of food delivery demand, delivery times, ratings, and an illustrative commission rule. It rebuilds an exploratory course exercise as a clear, reproducible analysis with checked calculations and a business interpretation. This is descriptive analysis, not a prediction system or a live FoodHub service.

## Visual snapshot

These figures were generated with Matplotlib from the 1,898-order dataset. The repository contains aggregate charts, not the source CSV. Explore all four figures and their interpretation in the [results gallery](docs/results.md#visual-gallery).

![Horizontal bar chart of the top eight cuisines, with American at 584 orders and Japanese at 470](assets/cuisine-demand.svg)

![Boxplots of delivery times for weekday and weekend orders; the mean is 28.34 versus 22.47 minutes](assets/delivery-time.svg)

## Questions

- Which cuisines account for the most orders, including on weekends?
- How do mean delivery times differ between the weekday and weekend groups?
- What share of orders exceed 60 minutes from preparation through delivery?
- How many customers leave no rating, and which restaurants meet an example promotion rule?
- What commission would the stated tier schedule produce on these orders?

## Run locally

Python 3.10+ is required. Obtain an authorized copy of the order dataset and save it under `data/foodhub_order.csv`. The original course CSV is not distributed here; its redistribution license has not been established. The analysis expects the nine fields documented in [data and methods](docs/methods.md). The tiny dataset under `tests/fixtures/` is invented solely to exercise the code.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
foodhub-analyze data/foodhub_order.csv --output results/summary.json --charts results/charts
python -m unittest discover -s tests -v
```

You can run `foodhub-analyze tests/fixtures/orders.csv --charts results/charts` without the private dataset. `data/` and `results/` are ignored by Git. The JSON and generated charts remain local unless you choose to share them.

To rebuild the four SVG figures displayed here using an authorized copy of the source CSV, run `python scripts/build_gallery.py data/foodhub_order.csv` after installation. This writes the aggregate figures to `assets/`; inspect them before committing changes. The six-row test fixture is suitable for checking the code, but its charts do not represent the checked findings below.

## Checked findings from the provided dataset

The project owner's 1,898-order CSV produced the aggregate findings in [results](docs/results.md). In particular, **American cuisine has 415 weekend orders**. The original rendered assignment reported 1,351 because it counted every weekend order after creating a Boolean comparison. We corrected the computation and independently checked the new results against the supplied CSV.

The findings are one dataset's descriptive patterns. They do not establish that changing driver staffing, promotions, or rating incentives would cause improvements. Dataset provenance and reuse rights should be confirmed before distributing row-level records.

## Project structure

| Path | Purpose |
| --- | --- |
| `src/foodhub_analysis/` | Validated loader, aggregate metrics, chart generation, CLI |
| `notebooks/walkthrough.ipynb` | Output-free analysis walkthrough using the package |
| `tests/fixtures/orders.csv` | Six invented orders for offline tests |
| `docs/methods.md` | Definitions, assumptions, and limits |
| `docs/results.md` | Checked aggregate findings and business interpretation |
| `assets/*.svg` | Reproducible aggregate figures featured in the README and results page |
| `scripts/build_gallery.py` | Rebuild the four portfolio figures from an authorized dataset |

The code here was written for this standalone case study. The original assignment template, rendered HTML, and source CSV are excluded. No license is asserted for the course materials or source dataset.
