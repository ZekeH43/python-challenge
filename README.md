# Python Challenge — PyBank Financial Analysis

A beginner-friendly Python portfolio exercise based on a historical financial-analysis assignment. It reads monthly profit/loss records from a CSV file and calculates the net result, average month-to-month change, and dates of the largest increase and decrease.

## Run the project

Only Python 3.10+ is needed; the new command-line implementation uses the standard library.

From the repository root:

```bash
python pybank.py
```

Use your own CSV with columns `Date,Profit/Losses`:

```bash
python pybank.py path/to/budget.csv
```

The command works independently of the shell's current working directory when using the default file. Data is read from [PyBank/budget_data.csv](PyBank/budget_data.csv). For a custom file, provide an explicit path.

## Reproducible original-dataset results

| Metric | Result |
| --- | ---: |
| Months | 86 |
| Total profit/loss | $38,382,578 |
| Average monthly change | -$2,315.12 |
| Greatest increase | Feb-2012 (+$1,926,159) |
| Greatest decrease | Sep-2013 (-$2,196,167) |

The first month has no preceding month, so averages and increase/decrease rankings use **85 changes** rather than 86.

## Run tests

```bash
python -m unittest discover -s tests -v
```

Tests check the original CSV totals, negative/zero changes, invalid inputs, and consistent formatting. A GitHub Actions workflow also runs the tests under Python 3.11 and 3.12.

## Source coursework and next steps

- [Original PyBank notebook](PyBank/main.ipynb/main.ipynb) is intentionally preserved as a learning artifact.
- The `PyRamen/main.ipynb` file is empty in the original repository; **PyRamen is not implemented** here.
- Older duplicate notebooks and checkpoints remain historical artifacts; new work should use `pybank.py`.

**Technical skills shown:** CSV parsing, input validation, functions, immutable data classes, testing, command-line interfaces, and financial calculations. No financial API, paid dependency, or production deployment is required.
