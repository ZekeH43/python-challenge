"""PyBank regression and edge-case tests; no third-party dependencies."""
import csv
import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from pybank import DEFAULT_DATA, analyze_budget, format_summary, main


class TestPyBank(unittest.TestCase):
    def write_budget(self, rows, header=("Date", "Profit/Losses")):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / "budget.csv"
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(header)
            writer.writerows(rows)
        return path

    def test_original_dataset(self):
        result = analyze_budget(DEFAULT_DATA)
        self.assertEqual(result.months, 86)
        self.assertEqual(result.net_total, 38382578)
        self.assertAlmostEqual(result.average_change, -2315.1176470588234)
        self.assertEqual(
            (result.greatest_increase_month, result.greatest_increase),
            ("Feb-2012", 1926159),
        )
        self.assertEqual(
            (result.greatest_decrease_month, result.greatest_decrease),
            ("Sep-2013", -2196167),
        )

    def test_month_to_month_changes_include_negative_and_zero(self):
        budget = self.write_budget([
            ("Jan", -10), ("Feb", -30), ("Mar", -30), ("Apr", -5)
        ])
        result = analyze_budget(budget)
        self.assertEqual(result.months, 4)
        self.assertEqual(result.net_total, -75)
        self.assertAlmostEqual(result.average_change, 5 / 3)
        self.assertEqual((result.greatest_increase_month, result.greatest_increase), ("Apr", 25))
        self.assertEqual((result.greatest_decrease_month, result.greatest_decrease), ("Feb", -20))

    def test_ties_use_first_occurrence(self):
        budget = self.write_budget([("Jan", 1), ("Feb", 4), ("Mar", 7)])
        result = analyze_budget(budget)
        self.assertEqual(result.greatest_increase_month, "Feb")
        self.assertEqual(result.greatest_decrease_month, "Feb")

    def test_missing_columns(self):
        budget = self.write_budget([("Jan", 100)], header=("Wrong", "Columns"))
        with self.assertRaisesRegex(ValueError, "CSV must contain"):
            analyze_budget(budget)

    def test_fewer_than_two_months(self):
        for rows in [[], [("Jan", 100)]]:
            with self.subTest(rows=rows):
                with self.assertRaisesRegex(ValueError, "At least two"):
                    analyze_budget(self.write_budget(rows))

    def test_invalid_amount(self):
        with self.assertRaisesRegex(ValueError, "row 3"):
            analyze_budget(self.write_budget([("Jan", 100), ("Feb", "invalid")]))

    def test_missing_month(self):
        with self.assertRaisesRegex(ValueError, "Missing month"):
            analyze_budget(self.write_budget([("Jan", 100), ("", 200)]))

    def test_output_format(self):
        output = format_summary(analyze_budget(DEFAULT_DATA))
        self.assertIn("Total Months: 86", output)
        self.assertIn("Total: $38,382,578", output)
        self.assertIn("Average Change: $-2,315.12", output)
        self.assertIn("Feb-2012 ($1,926,159)", output)
        self.assertIn("Sep-2013 ($-2,196,167)", output)


if __name__ == "__main__":
    unittest.main()
