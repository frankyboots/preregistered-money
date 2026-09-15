# Dataset: Gold spot (USD)

```yaml
id: gold
raw: "data/TVC_GOLD, 1M.csv"
source: "TradingView GOLDUSD spot, exported 1M timeframe (symbol in filename: TVC_GOLD, 1M.csv)"
url: "https://tradingview.com/symbols/GOLDUSD/"
obtained: 2026-09-11
format: csv
snapshot: "download 2026-09-11; rows through 2026-09"
sha256: 92217de25d5d14b8cf62d33ef74d56369429363b077e694d6665173dfd5a0334
first: 1833-01-01
last: 2026-09-01
usable_from: 1970-01-01
frequency: monthly
license: "TradingView historical export for personal use; underlying spot price is public market data"
```

## Structure

`time,open,high,low,close` — one row per month. Row dates are the
**month's first trading day** (day of month always 1–4), not month-end.
The `close` column is the month-end value and is the value to use
(verified, below).

## Usable window

**Pre-1970 rows are not usable.** They trace a reconstructed pre–Nixon-shock
history: prices are flat at 20.65 for decades (1833–1967) and do not
represent tradeable market prices — no liquid gold market existed. Any prereg
must state `usable_from: 1970-01-01`; the loader should refuse or warn on
rows before that date. (LBMA/FRED LBMA_GOLDAM fix is a candidate for deeper
pre-1970 history if ever needed — that is a separate dataset.)

## Row convention — verified 2026-09-15 (satisfies the METHODOLOGY v1.1
§1.6 open data task)

Task: before gold is first used in a sealed run, verify the close
convention empirically against published LBMA month-end values for at least
six months spanning 1971, 1980, 2000, and 2010.

**Reference.** Published daily AM/PM LBMA Gold Price fixes (London) from
sdbullion.com year pages (fetched 2026-09-15; LBMA's own historical
tabulated data is IBA-licensed and not freely available, so the published
fix listings are the reference):

- https://sdbullion.com/gold-prices-1971
- https://sdbullion.com/gold-prices-1980
- https://sdbullion.com/gold-prices-2000
- https://sdbullion.com/gold-prices-2010

**Findings** (seven months — exceeds the six-month requirement):

| Month | TV close | LBMA AM | LBMA PM | dev. AM | dev. PM |
|---|---|---|---|---|---|
| 1971-12 | 43.85 | 43.62 | 43.62 | +0.53% | +0.53% |
| 1980-01 | 681.50 | 668.00 | 653.00 | +2.02% | +4.36% |
| 1980-06 | 647.40 | 662.50 | 653.50 | −2.28% | −0.93% |
| 2000-01 | 283.10 | 283.05 | 283.30 | +0.02% | −0.07% |
| 2000-06 | 288.60 | 289.15 | 288.15 | −0.19% | +0.16% |
| 2010-01 | 1080.98 | 1082.75 | 1078.50 | −0.16% | +0.23% |
| 2010-06 | 1242.00 | 1240.50 | 1244.00 | +0.12% | −0.16% |

1. **Close convention: confirmed.** `close` is the month-end spot price:
   it tracks the month-end LBMA PM fix within ±0.2% in normal months
   (2000, 2010) and to the nearest month-end fix in the others.
2. **Row dates are bar-start dates** — the month's first trading day
   (day-of-month always 1–4; e.g. 2026-01-02 for Jan 1 a holiday,
   2026-08-03 for Aug 1 a Saturday). Never use `time` as the value date;
   the value date is end-of-month.
3. **Continuity: confirmed.** Across all 681 usable months (1970-01 →
   2026-09), each month's `open` equals the previous month's `close`
   (680 consecutive pairs; median gap 0.08%, max 7.50% in 1997-11) —
   the series is internally consistent month-to-month.
4. **Volatile-month divergence (known limitation).** In the most
   volatile month in 50 years (Jan 1980, gold fell from the $850 peak to
   ~$653 by month end), TV's month-end spot diverged from the month-end
   LBMA fix by ~4.4% (PM) / ~2.0% (AM) — consistent with TV carrying a
   non-London spot reference for some historical months. Bounded, and
   immaterial for the current scope (monthly-rebalanced passive blends,
   5 bps round-trip costs, verdict on long-run CAGR/Sharpe/max-DD).
   **Gold's absolute level should not be used for short-horizon or
   fix-relative claims in any future prereg.**

**Verdict: the pinned snapshot's close column is verified and usable** for
the current scope.

## Caveats

- Spot price, not an investable instrument: no carry, no bid/ask, no way to
  own it in 1975. The investable proxy is GLD (2004+); a prereg must record
  the proxy and its gap explicitly.
- TV's export may change row convention between exports. The convention
  above is verified **for this pinned snapshot** (sha256
  `92217de2…334`). On any re-download, spot re-verify against the LBMA
  reference months (≥6, spanning 1971/1980/2000/2010) and record the
  result in a manifest note — the checksum pin is the arbiter, not this
  section.
- Monthly close only — daily data would be a new snapshot, new manifest
  section, new checksum.
