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

`time,open,high,low,close` — one row per month (some rows mid-month, e.g.
`1968-06-03`). `close` = month-end spot price in USD/oz.

## Usable window

**Pre-1970 rows are not usable.** They trace a reconstructed pre–Nixon-shock
history: prices are flat at 20.65 for decades (1833–1967) and do not
represent tradeable market prices — no liquid gold market existed. Any prereg
must state `usable_from: 1970-01-01`; the loader should refuse or warn on
rows before that date. (LBMA/FRED LBMA_GOLDAM fix is a candidate for deeper
pre-1970 history if ever needed — that is a separate dataset.)

## Caveats

- Spot price, not an investable instrument: no carry, no bid/ask, no way to
  own it in 1975. The investable proxy is GLD (2004+); a prereg must record
  the proxy and its gap explicitly.
- TV's export may change row convention between exports (mid-month rows);
  checksum-pin each snapshot.
- Monthly close only — daily data would be a new snapshot, new manifest
  section, new checksum.
