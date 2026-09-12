# Dataset: Shiller "Irrational Exuberance" monthly data

```yaml
id: shiller_ie_data
raw: data/ie_data.xls
source: "Robert J. Shiller, 'Stock Market Data Used in Irrational Exuberance' (Princeton University Press, 2000/2005/2015, updated)"
url: https://shillerdata.com/
obtained: 2026-09-11
format: xls (legacy binary Excel; sheet 'Data')
snapshot: "as printed in the spreadsheet at download; last row 2026-09"
sha256: 044196dafe44c3030b2facbdea023975b3f6aa68b4e52f8f9bafc403e19589c1
first: 1871.01
last: 2026.09
frequency: monthly
license: "Free to download for personal/educational use (site terms); attribution to Shiller"
```

## Structure

- Sheet **`Disclaimer`** — attribution text, ignore.
- Sheet **`Data`** — header block in rows 1–8 (merged, two-row column
  headers), data in **rows 9–1877** (1869 monthly rows, `Date` column is a
  fractional year `YYYY.MM`), footer note in the final row.

Key columns (A–V): `Date`, `P` (S&P Comp. price), `D` (dividend), `E`
(earnings), `CPI`, `Date Fraction`, `GS10` (long rate), plus real/dividend/
price/TR indices, P/E10, CAPE, CAPE ratio, TR-CAPE, excess CAPE, and annualized
real-return series for stocks, 10Y bonds, and the stock–bond spread.

## Caveats

- SPX **price** level, not total return — the TR columns carry total-return
  history; a prereg must say which it uses.
- The spreadsheet is a snapshot, not a feed: Shiller updates it; a re-download
  is a new snapshot (see `data/README.md`).
- CAPE/earnings fields are `'NA'` as strings in early rows — parse defensively.
- Footer notes in the sheet record estimated values in the most recent rows
  (CPI / GS10 estimates) — check the last rows of a fresh download.
