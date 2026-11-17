"""Reproducible, standard-library solution for the historical PyBank exercise."""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path


DEFAULT_DATA = Path(__file__).resolve().parent / "PyBank" / "budget_data.csv"


@dataclass(frozen=True)
class BudgetSummary:
    months: int
    net_total: int
    average_change: float
    greatest_increase_month: str
    greatest_increase: int
    greatest_decrease_month: str
    greatest_decrease: int


def analyze_budget(csv_path: str | Path) -> BudgetSummary:
    """Analyze month-to-month profit/loss changes in a well-formed CSV.

    A valid CSV has the Date and Profit/Losses columns and at least two months.
    The change associated with each month is measured against the *prior* month.
    """
    records: list[tuple[str, int]] = []
    with Path(csv_path).open("r", newline="", encoding="utf-8-sig") as source:
        reader = csv.DictReader(source)
        if reader.fieldnames is None or not {"Date", "Profit/Losses"}.issubset(
            reader.fieldnames
        ):
            raise ValueError("CSV must contain Date and Profit/Losses columns")
        for row_number, row in enumerate(reader, start=2):
            month = (row.get("Date") or "").strip()
            raw_value = (row.get("Profit/Losses") or "").strip()
            if not month:
                raise ValueError(f"Missing month in CSV row {row_number}")
            try:
                amount = int(raw_value)
            except ValueError as error:
                raise ValueError(
                    f"Invalid profit/loss in CSV row {row_number}: {raw_value!r}"
                ) from error
            records.append((month, amount))

    if len(records) < 2:
        raise ValueError("At least two months are required to calculate changes")

    changes = [
        (current_month, current_value - previous_value)
        for (_, previous_value), (current_month, current_value)
        in zip(records, records[1:])
    ]
    maximum = max(changes, key=lambda item: item[1])
    minimum = min(changes, key=lambda item: item[1])

    return BudgetSummary(
        months=len(records),
        net_total=sum(value for _, value in records),
        average_change=sum(value for _, value in changes) / len(changes),
        greatest_increase_month=maximum[0],
        greatest_increase=maximum[1],
        greatest_decrease_month=minimum[0],
        greatest_decrease=minimum[1],
    )


def format_summary(summary: BudgetSummary) -> str:
    return "\n".join(
        [
            "Financial Analysis",
            "----------------------------",
            f"Total Months: {summary.months}",
            f"Total: ${summary.net_total:,}",
            f"Average Change: ${summary.average_change:,.2f}",
            (
                f"Greatest Increase in Profits: {summary.greatest_increase_month} "
                f"(${summary.greatest_increase:,})"
            ),
            (
                f"Greatest Decrease in Profits: {summary.greatest_decrease_month} "
                f"(${summary.greatest_decrease:,})"
            ),
        ]
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze PyBank monthly profit/loss.")
    parser.add_argument(
        "csv_file",
        nargs="?",
        type=Path,
        default=DEFAULT_DATA,
        help="Optional budget CSV path (defaults to the repository's PyBank dataset)",
    )
    args = parser.parse_args()
    print(format_summary(analyze_budget(args.csv_file)))


if __name__ == "__main__":
    main()
