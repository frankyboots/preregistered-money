# Dataset: Fed funds effective rate (FRED FEDFUNDS)

```yaml
id: fed_funds
raw: "data/FRED_FEDFUNDS, 1M.csv"
source: "FRED series FEDFUNDS, exported from TradingView (symbol FEDFUNDS, 1M timeframe)"
url: https://fred.stlouisfed.org/series/FEDFUNDS
exported_via: "https://tradingview.com — chart export, symbol in filename: FRED_FEDFUNDS, 1M.csv"
obtained: 2026-09-11
format: csv
snapshot: "download 2026-09-11; rows through 2026-08"
sha256: dd331063f7d6979b63861de1bde293bf1d57410cb661c60ead900dc39c79f8ab
first: 1954-07-01
last: 2026-08-01
frequency: monthly
license: "FRED public data; no restriction on use, source attribution"
```

## Structure

`time,close` — one row per month, `time` = month-end convention, `close` =
effective fed funds rate in **percent** (e.g. `3.63` = 3.63%).

## Role in the project

Risk-free reference rate for the three-asset universe (SPX / 10Y / gold) —
the cost side of the benchmark study and the discount rate in any valuation
work.

## Caveats

- Monthly average of the daily effective rate; intra-month moves invisible.
- FRED is point-in-time stable for this series (historical months don't
  revise), but a re-export is still a new file — checksum-pin each snapshot.
- Pre-1970 values are pre-Volcker; usable as a rate, but regime comparisons
  across 1980 should be flagged in any prereg that spans it.
