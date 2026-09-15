# Verifying against public references

Source availability and parsing recipes for the class of task: verify a
pinned dataset's values/convention against a published reference. Findings are
checked at use-time — the table below is a *starting* map, not a guarantee.

## Known reference map (checked 2026-09, re-verify when used)

| Quantity | Authority | Free access? | Notes |
|---|---|---|---|
| LBMA Gold Price (daily AM/PM fixes, USD) | lbma.org.uk / IBA | **No** — historical tabulated data is IBA-licensed (MyLBMA portal); license contact required | Not a dead end — see below |
| LBMA Gold Price (published fix listings) | sdbullion.com `/gold-prices-<YYYY>` | **Yes** | Per-year HTML pages, one table of daily AM/PM fixes (AM and PM columns, `Month D, YYYY` rows). Regex-parseable; ~1.5 MB/year. Same for `/silver-prices-<YYYY>` |
| LBMA Gold Price (daily AM/PM fixes, USD) | FRED `LBMA_GOLDPM` / `LBMA_GOLDAM` | **No — series removed from FRED** | The series IDs redirect to FRED's IBA-data-removal notice (confirmed in a real browser, not a bot-wall artifact). Don't spend a retry cycle on FRED for LBMA fixes; go straight to the published fix listings |
| Long-run gold annual/monthly (World Bank Pink Sheet lineage) | eco3min, metalcharts, NMA PDF | Yes, but secondary | Fine for cross-checks; not the fix itself |

## Parsing sdbullion year pages (stdlib only)

```python
import re, html, datetime as dt
MON = {name.lower(): i for i, name in enumerate(
    ["January","February","March","April","May","June","July",
     "August","September","October","November","December"], 1)}
rows = re.findall(r'<tr[^>]*>(.*?)</tr>', text, flags=re.S)
for r in rows:
    tds = [html.unescape(re.sub(r'<[^>]+>', '', t)).strip()
           for t in re.findall(r'<td[^>]*>(.*?)</td>', r, flags=re.S)]
    m = re.match(r'^([A-Za-z]+)\s+(\d{1,2}),\s*(\d{4})$', tds[0])
    if not m or m.group(1).lower() not in MON: continue
    d = dt.date(int(m.group(3)), MON[m.group(1).lower()], int(m.group(2)))
    prices = [float(x.replace(',', ''))
              for x in re.findall(r'\$([\d,]+\.?\d*)\s*oz',
                                  ' '.join(tds[1:]))]
    # prices = [AM fix, PM fix] (PM may be missing on some rows)
```

Fetch with a browser User-Agent header; ~250 rows/year; month-end reference =
the fix on the month's last trading day in the listing (compare the listing's
last date against the calendar — months end on trading days, not on the 31st).

## The three checks (what a good verification establishes)

1. **Value-date convention** — does the candidate column track the reference
   at month ends? (Confirms e.g. that a bar's `close` is the month-end value.)
2. **Row-date convention** — what do the row dates actually denote? For
   TradingView monthly bars: the month's *first trading day* (day-of-month
   always 1–4). The value date is end-of-month; the row date is a bar label.
3. **Continuity** — does each month's `open` equal the previous month's
   `close`? Across all usable months, with the max gap and its date recorded
   (large gaps should land in known crash/recovery months — a gap in an
   unexplained month is a red flag to chase, not a statistic to absorb).

## Judgment rules

- **Normal-month tolerance:** ≤ ~0.5% per month confirms the convention.
- **Extreme-month divergence:** a bounded deviation in a single
  extreme-volatility month (e.g. a TV spot vs. LBMA fix gap in the most
  volatile month in 50 years) is a documented limitation, not an automatic
  failure — state the magnitude, the cause class (non-authority spot
  reference), and the scope in which it is immaterial.
- **License walls are not source absences.** Check the whole row of the
  reference map (secondary published sources) before concluding a quantity
  is unobtainable.
- **Do not switch the pinned source because other free sites diverge.**
  Every free gold site republishes its own historical feed — different
  timestamp or reference conventions — so they agree within tolerance in
  calm months and diverge in violent ones. That is the same phenomenon as
  the pinned source's own divergence, not evidence the pinned source is
  worse. A switch is justified only by authority (a licensed mirror, or a
  stable free mirror of the authority itself), never by one site's number
  looking closer; and per the methodology a switch is a *new dataset* — new
  manifest, new checksum, re-verification — never a silent substitution,
  especially once the quantity has entered a sealed run.
- **Verification binds to the pinned sha256.** A re-download re-verifies;
  the manifest section says so, and the checksum pin — not the section — is
  the arbiter.
