# day3-stats-toolkit
# Wakala Plus: Agent Deposit Statistics Toolkit

Day 3 project. Wakala Plus runs a network of M-Pesa agents around Nairobi, Thika, Machakos and Nakuru. Its risk team watches daily deposit figures per agent, where unusually high or low days can mean fraud, a float shortage or a data-entry error. This toolkit gives them a small statistics library they can read line by line. Every calculation is written from first principles in plain Python, and NumPy is used only afterwards to verify the results.

## Project structure

```
day3-stats-toolkit/
├── stats_toolkit.py
├── test_stats_toolkit.py
├── data/agent_deposits.csv
├── output/stats_report.txt
├── requirements.txt          # numpy (verification only), pytest
└── README.md
```

## How to run

Requires Python 3.9 or newer.

```bash
git clone https://github.com/NantegeJosephine/day3-stats-toolkit.git
cd day3-stats-toolkit
python -m venv .venv
.venv\Scripts\activate            # Windows (Mac/Linux: source .venv/bin/activate)
pip install -r requirements.txt
```

**Generate the report.** It is printed to the screen and saved to `output/stats_report.txt`:

```bash
python stats_toolkit.py
```

**Run the unit tests:**

```bash
python -m pytest -v
```

## What is implemented

| Part | Description |
|---|---|
| `load_column` | Reads one CSV column and returns the valid floats plus `(row_number, raw_value)` pairs for every rejected value. |
| `mean`, `median`, `mode` | Written without the `statistics` module or NumPy. `mode` returns a list, because several values can tie. |
| `variance`, `std_dev` | Support the sample (n − 1) and population (n) formulas through a `sample` argument. |
| `quartiles`, `iqr_outliers` | Quartiles by linear interpolation, and outlier detection with IQR fences. `iqr_outliers` returns the IQR, both fences and the outlying values. |
| `StatisticsAnalyzer` | Wraps one column. It has `from_csv`, `summary()`, `without_outliers()` and `report()`. The data is sorted once and cached, and `without_outliers()` returns a new analyzer. |
| `compare_with_numpy` | The only place NumPy is imported. It reports MATCH or MISMATCH per statistic using `math.isclose`, never `==`. |

## Data analysed

`data/agent_deposits.csv` has two numeric columns, and each is analysed separately by its own `StatisticsAnalyzer`:

- `transactions`
- `daily_deposits_kes`

## Choices and decisions

### What counts as invalid

The data is typed by agents into a phone app. A value is **rejected and never guessed or repaired** when it is:

| Raw value | Decision | Reason shown in the report |
|---|---|---|
| Blank or whitespace only | Reject | missing |
| Text that is not a number (e.g. `abc`) | Reject | not a number |
| `nan` or `inf` | Reject | not finite |

Surrounding spaces are accepted. Any other finite number, including zero, negative or very large values, is accepted as data. Whether such a day is suspicious is a judgement for the risk team, and the IQR method flags extreme values for review.

Row numbers count the header as row 1, so the first data row is row 2. Every rejected value is listed with its row, raw value and reason, for each column, in `output/stats_report.txt`. Rejected values are excluded from every statistic.

### Sample or population variance

The toolkit uses the **sample formula (n − 1)** by default. The data is a slice of an ongoing process and not every day the agents will ever work, and the risk team wants to estimate how variable the figures are in general. Dividing by n would understate the spread of a small sample. Both formulas are available through the `sample` argument. `variance` raises a `ValueError` for a single value under the sample formula, and `std_dev` returns 0.0 for a single value.

### Quartile method

Quartiles use **linear interpolation**. The position of quantile `p` in the sorted data is `(n − 1) × p`, and a position between two values is interpolated between them. This is the default method of `numpy.percentile` (Hyndman and Fan type 7), so the NumPy comparison is like for like. A different method, such as the median-of-halves method, gives slightly different Q1 and Q3 values and would show up as a MISMATCH.

### Outliers

A value is an outlier if it is below `Q1 − k × IQR` or above `Q3 + k × IQR`. The default is `k = 1.5`, the usual convention, and `k` must not be negative.

### Mode when every value appears once

`mode` returns an empty list `[]` when every value appears exactly once, because a "mode" that lists every value carries no information. When several values tie for the highest count, all of them are returned, sorted.

## Results

`output/stats_report.txt` is regenerated every time `python stats_toolkit.py` runs, so it always matches the current code. For each column it shows:

- the statistics for all valid data and with outliers removed, side by side in the same report,
- the IQR fences and the outlying values,
- every rejected row with its reason,
- the NumPy verification, with MATCH or MISMATCH for each statistic,
- a short note for the risk team on what the outliers might mean.

### What the outliers might mean for the risk team

An outlying day is a signal to look closer, not evidence of wrongdoing. A very high figure could point to fraud, a large legitimate lump sum, or a typing error with an extra digit. A very low one could point to a float shortage, a closed agent or a missing entry. The risk team should first check the agent and date of each flagged day against the source records before drawing a conclusion.

## NumPy verification

`compare_with_numpy` recomputes the mean, median, mode, variance, standard deviation and quartiles with NumPy and compares each with a tolerance. The two usual causes of a MISMATCH are the variance formula (NumPy needs `ddof=1` to match the sample formula) and the quartile method (NumPy's default is linear interpolation). Both are matched by design, so every statistic is expected to show MATCH. The latest result is at the end of the report.

## Unit tests

`test_stats_toolkit.py` uses small inputs that can be checked by hand, not the dataset. The tests cover empty input, odd and even lengths, ties in the mode, sample versus population variance, outlier detection and rejected values. Run them with `python -m pytest -v`.

## Assumptions

- Values in `daily_deposits_kes` are in KES.
- The CSV has a header row.
- Each numeric column is analysed across all of its rows together.
- The statistics describe this dataset only. They do not explain causes.

## Tech used

Python 3 standard library (`csv`, `math`, `pathlib`), NumPy (verification only) and pytest.
