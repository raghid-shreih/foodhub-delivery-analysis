import csv
import tempfile
import unittest
from pathlib import Path

from foodhub_analysis.analysis import analyze_orders, load_orders
from foodhub_analysis.charts import save_charts

FIXTURE = Path(__file__).parent / "fixtures" / "orders.csv"


class AnalysisTests(unittest.TestCase):
    def test_aggregate_metrics_and_exclusive_commission_tiers(self):
        report = analyze_orders(load_orders(FIXTURE))
        self.assertEqual(report["orders"], 6)
        self.assertEqual(report["weekend_top_cuisine"], {"name": "American", "orders": 2})
        self.assertEqual(report["delivery_by_day"]["Weekday"], {"orders": 3, "mean_minutes": 23.67})
        self.assertEqual(report["orders_over_60_minutes"], {"count": 2, "share": 0.3333})
        self.assertEqual(report["unrated_orders"], {"count": 2, "share": 0.3333})
        self.assertEqual(report["orders_over_20_dollars"], {"count": 2, "share": 0.3333})
        self.assertEqual(report["estimated_commission_dollars"], 16.0)
        self.assertEqual(report["promotion_candidates"], [])

    def test_duplicate_orders_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "duplicate.csv"
            with FIXTURE.open(newline="") as source:
                rows = list(csv.reader(source))
            rows.append(rows[1])
            with path.open("w", newline="") as output:
                csv.writer(output).writerows(rows)
            with self.assertRaisesRegex(ValueError, "Duplicate order_id"):
                load_orders(path)

    def test_charts_are_written(self):
        with tempfile.TemporaryDirectory() as directory:
            paths = save_charts(load_orders(FIXTURE), directory)
            self.assertEqual(len(paths), 3)
            self.assertTrue(all(path.stat().st_size > 1000 for path in paths))


if __name__ == "__main__":
    unittest.main()
