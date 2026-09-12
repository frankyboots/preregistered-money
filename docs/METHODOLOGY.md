# Methodology

**v1.1 — 2026-09-12.** Preregs sealed on or after this
date play under this contract.

`CONCEPT.md` is the *why*: brand, product, integrity rules. This document is
the **operational contract in between** — the mechanical detail behind
CONCEPT §2, pinned to concrete defaults that every prereg inherits by
silence, precise enough that a third party can verify a sealed run from the
published record alone (prereg + results + this doc + the repo).

It is **versioned**. A sealed prereg is immutable, so the rules it was
judged under must be too: every prereg's frontmatter carries
`methodology: <sha>` — the SHA of the last commit that touched this file at
or before the seal commit (compute it at seal time:
`git rev-list -1 HEAD -- docs/METHODOLOGY.md`). Methodology changes are new
commits, never retroactive against sealed preregs — the same append-only
discipline as the composite recipe (CONCEPT §11).

## 0. Precedence

1. **The sealed prereg** — its spec, its data, its bar. This is the commitment.
2. **This methodology** — defaults the prereg inherits by silence.
3. **Engine defaults** — implementation behavior; a bug if it disagrees, not a choice.

A prereg overrides this document by explicit statement (e.g. *"Costs: 10 bps
round trip, not the v1 default — wider assumed spreads for the 2020–22
regime"*). This document does not override a sealed prereg, ever: a sealed
prereg is judged under the version it cites. If a methodology change would
invalidate a premise of an earlier prereg, that is a **new prereg** — not a
re-judgment of the old one.

### Change log

The git history of this file is the SHA record (`git log --follow
docs/METHODOLOGY.md`); the table below is the human summary.

| Version | Date | Summary |
|---|---|---|
| v1.0 | 2026-09-12 | Initial: data policy, execution convention, cost model v1, metric definitions, default split, menu selection, null-baseline interface, config hash + run log, verdict mechanics |
| v1.1 | 2026-09-12 | Standard per-decade attribution table required in every results doc (§4.1); decades soft context by default, pre-registerable as criteria |

---

## 1. Data policy

### 1.1 Approved sources

All sources are $0 and public (CONCEPT §11.2). Adding a source is a new
manifest in `research/data/` + a new checksum pin — never a silent
substitution.

| Dataset | id | Frequency | Usable window | Role | Manifest |
|---|---|---|---|---|---|
| Shiller "Irrational Exuberance" monthly data | `shiller_ie_data` | monthly | 1871.01 → (observation cutoff) | SPX price + total-return, 10Y bonds, CPI, GS10, CAPE | `research/data/datasets/shiller_ie_data.md` |
| FRED FEDFUNDS (via TradingView export) | `fed_funds` | monthly | 1954-07 → | Risk-free reference rate | `research/data/datasets/fed_funds.md` |
| TradingView GOLDUSD spot | `gold` | monthly | **1970-01 →** (never earlier) | Gold spot, USD/oz | `research/data/datasets/gold.md` |

Later expansions (FRED DGS10 / DFII10, LBMA pre-1970 gold fix, daily bars)
are new datasets, each with its own manifest and caveats.

### 1.2 Snapshot contract

The single source of truth for how raw files are pinned is
`data/README.md` + `research/data/verify.py` — not restated here. The one
rule that carries into every prereg:

> A prereg pins the exact raw snapshots it ran against (sha256 per file, in
> frontmatter and in the config hash, §6.1). A re-download is a **new
> snapshot** — new file name, new checksum, manifest note — never an
> overwrite of a file a sealed prereg pinned.

### 1.3 Observation cutoff

- A month's row is usable only once its calendar month has fully closed.
- **Default: the usable window ends at the last fully closed month before
  the seal date.** Sealed 2026-09-12 → data through 2026-08.
- The cutoff is **frozen at seal**. The verdict run uses exactly the
  snapshots and window pinned in the prereg. A refreshed snapshot is a new
  run (a CI drift check, §6.2) — never the verdict run.
- Rationale: this is the mechanical form of "no look-ahead" at the data
  level. It automatically excludes Shiller's estimate-flagged final rows and
  any intra-month revision.
- A prereg may declare a *shorter* window (earlier `usable_to`, later
  `usable_from`) — never a longer one.

### 1.4 Proxy policy

The verdict runs on the **full historical (index/spot) era** — the long
window is the point of the three-asset study. The investable era is a
mandatory sensitivity analysis in every results doc:

| Asset | Index-era series | Investable proxy | Proxy inception |
|---|---|---|---|
| SPX | Shiller total-return index | SPY | 1993-01 |
| 10Y | Shiller 10Y total-return history (DFII10 lineage) | TLT | 2002-07 |
| Gold | Gold spot (no carry) | GLD | 2004-11 |

- Fee drag applies in **both** eras: the index era assumes ownership through
  the proxy. Conservative by default; a prereg may override with a stated
  justification.
- Gold is spot without carry or bid/ask — a known limitation, recorded per
  prereg, not a footnote.
- Every proxy caveat (ETF vs. underlying, price vs. total return, fee drag,
  duration mismatch) is documented in the prereg's Data section (CONCEPT §7).

### 1.5 Universe and survivorship

- Current scope: a **fixed three-asset universe**. No selection was made, so
  there is no survivorship or point-in-time-membership problem to solve —
  preregs still state this explicitly in their Data section, so the claim is
  on the record.
- Adding or changing the universe is a **new prereg** (or a methodology
  version bump, if the change is a standing rule). Expansion to equities
  (later phase) carries its own point-in-time membership rule, written in
  that prereg before sealing.

### 1.6 Caveats every prereg must carry

Each prereg's Data section lists, per dataset used:

1. the series and era used (index-era vs. investable era, proxy named);
2. any source caveat that bites this specific run (Shiller estimate rows,
   pre-1980 Fed-funds regime, gold row conventions);
3. the data's known limitations as *stated weaknesses* (CONCEPT §1).

**Open data task (tracked, pre-first-PR):** the TradingView gold export
mixes row conventions (some mid-month rows, closes described as
"month-end"). Before gold is first used in a sealed run, verify the close
convention empirically against published LBMA month-end values for at least
six months spanning 1971, 1980, 2000, and 2010, and record the result in
the gold manifest.

---

## 2. Execution and no look-ahead

### 2.1 Default timing convention

- **Decision:** end of month M, using only rows for months ≤ M.
- **Execution:** at the close of month M.
- **Attribution:** new weights first earn from month M+1; trade cost is
  charged to nav at the close of M (§3.2).
- A prereg requiring a different convention (e.g., intra-month or daily
  execution) must declare it at seal — and the data to support it.

### 2.2 Engine look-ahead safeguards

- Loaders slice each series to (usable window, decision month). The engine
  cannot see rows dated after the decision month.
- **Look-ahead canary test:** mutating data strictly after month M must
  leave the output byte-identical. This is a unit test, run in CI.
- No wall-clock time in the research path. No randomness without a recorded
  seed (the null baseline's generator is the only sanctioned random
  component, §5.5).
- Loaders refuse rows outside a dataset's usable window (gold: rows before
  1970).

---

## 3. Cost model (v1)

### 3.1 Standard costs (inherited by silence)

| Item | Default | Notes |
|---|---|---|
| Commission | $0 | Megacap ETFs |
| Spread + slippage | **5 bps round trip** (2.5 bps per side) | Charged on ETF trades at each rebalance |
| Fee drag — SPY | 10 bps/yr | Current expense ratio 0.0945%, rounded up |
| Fee drag — TLT | 15 bps/yr | Current expense ratio 0.15% |
| Fee drag — GLD | 40 bps/yr | Current expense ratio 0.40% |
| Borrow / financing | n/a | No leverage in initial scope |

Cost values are constants in v1. A prereg may declare a **cost function of
month** (regime-dependent spreads) if it specifies the function fully at
seal; a bare "lower costs in some years" is not a specification.

### 3.2 Application (order is normative)

Per month t, with `w_t` the weights decided at the close of t:

1. **Earn** — hold the weights chosen at the close of t−1 through month t:
   `nav_t^pre = nav_{t-1} × (1 + r_t(w_{t-1}) − fee(w_{t-1})/12)`
   where `r_t` is the month-t total return of the portfolio and
   `fee(w)` the weighted annual fee drag.
2. **Rebalance** — at the close of t, trade to `w_t`:
   `TO_t = ½ Σ_i |w_{i,t} − w_{i,t-1}|`
   `nav_t = nav_t^pre × (1 − TO_t × c_rt)` with `c_rt = 5 bps`.

`w_t` first earns from month t+1. Costs are deducted **before** any metric
is computed; metrics in §4 are all net.

**The engine refuses to start a run with no cost block in the config.** A
cost block may set values to zero only with a documented justification in
the prereg — and a strategy that only works with zero costs is falsified by
definition (CONCEPT §2.5).

### 3.3 Turnover (definition)

- **One-way turnover** at rebalance t: `TO_t = ½ Σ_i |w_{i,t} − w_{i,t-1}|`
  (weights sum to 1 in the initial scope; a cash sleeve is an explicit
  weight when gross exposure < 1).
- **Annual turnover**: sum of `TO_t` over the months in the year. Reported
  in every results doc, consumed by the cost model, and the referent for any
  prereg's turnover-band criterion.

### 3.4 Overrides

A prereg overrides by declaring a full cost block in its config (captured in
the config hash, §6.1) plus a one-line justification in the Costs section.
Partial overrides ("default except slippage") are not allowed — the block is
complete or it is the v1 default.

---

## 4. Metrics

All metrics are computed on the **net nav** (fees + trade costs deducted),
monthly, unless a prereg says otherwise. Formulas here are normative — a
third party recomputing from the published nav gets the published number.

| Metric | Definition |
|---|---|
| CAGR | `(nav_end / nav_start)^(12/N) − 1`, N = number of months |
| Volatility | `std(r_t − rf_t, ddof=1) × √12` |
| Sharpe | `mean(r_t − rf_t) / std(r_t − rf_t, ddof=1) × √12` |
| Max drawdown | `max_t (1 − nav_t / max_{s≤t} nav_s)` |
| Calmar | `CAGR / MaxDD` (soft) |
| Excess CAGR | `CAGR − benchmark CAGR`, same window |
| Turnover | per §3.3 |
| Cost drag | `Σ TO_t × c_rt`, reported annualized |

**Risk-free rate.** `rf_t = FEDFUNDS_t / 100 / 12` (the series is in
percent, annualized). Before 1954-07 (FEDFUNDS start) `rf_t = 0`, and the
results doc flags any metric that spans that boundary.

**Benchmark.** Whatever the frozen benchmark (the output of PR-2026-001)
names, computed on the same series, same window, same cost model. Every
prereg after the benchmark study judges against the frozen benchmark —
never against whichever asset did well (CONCEPT §3).

**Capacity.** Reference AUM: $100k. Results report the round-trip spread
cost in dollars at that AUM for the observed turnover, plus a one-line
liquidity statement (none in current scope; any prereg introducing a less
liquid instrument must state the constraint explicitly).

**Required in every results doc.** Both eras: index-era (the verdict era)
and investable-era (sensitivity, per §1.4); the per-decade table (§4.1);
and, for each pre-registered
criterion: the threshold, the observed value, pass/fail.

### 4.1 Per-decade attribution (required)

The three assets have never shared a regime — 1970s stagflation, the 80s
bond bull market, 2000s equity stagnation, the 2022 triple drawdown — and
aggregate OOS numbers hide *which* regime produced the result. So every
results doc carries a per-decade table, emitted by the engine and
reproduced verbatim.

- **Rows:** calendar decades spanning the prereg's usable window. For the
  current three-asset scope (window from 1970) the standard rows are the
  1970s through the 2020s.
- **Partial decades** — the first or last row, or any window truncation —
  are labeled with their month count: `2020s (78 months)`.
- **Table A — strategy:** CAGR, volatility, Sharpe, max drawdown per
  decade, on the net nav.
- **Table B — asset reference:** CAGR per asset per decade, under the
  same cost model and fee drag. This is the regime read: which assets
  worked and which died in each row, and the backdrop the strategy's
  numbers sit against.
- **Decades are context, not judgment.** Decade-level performance is soft
  by default. A prereg may preregister decade-level criteria at seal (e.g.
  "max drawdown in any full decade ≤ Y%"); they enter the criteria table
  as hard or soft, and the scoreboard labels that bar "extended."
- **Partial decades never qualify as criteria.** A 78-month window is not
  a decade, and a criterion on it would overfit an arbitrary slice.
- **No regime detection.** Calendar decades are fixed — arbitrary, but
  preregistered and identical for everyone. Data-driven regime
  segmentation is a *strategy* (its own prereg), not a method.
- The investable-era sensitivity analysis (§1.4) stays aggregate: it is a
  proxy-validity check, not a regime study.
- The per-decade tables do not go on the scoreboard (one headline line
  per PR there); full decade detail lives in the results doc and the
  verdict video.

---

## 5. Analysis protocol

### 5.1 Default split

- **In-sample:** usable-window start → 1999-12.
- **Out-of-sample:** 2000-01 → observation cutoff.

Chosen to cover dot-com, GFC, the zero-rate era, and post-2010, and to sit
close to the investable era. A prereg may declare its own split **at seal**
— arbitrary but preregistered is the whole point. The split is part of the
config hash.

### 5.2 Walk-forward (only when a prereg declares parameter estimation)

- Fit window F (default 60 months), out-of-sample step S (default 12
  months), expanding or rolling as declared.
- Refits use only data ≤ the refit month; OOS months are never visible to
  the fitting step (enforced by the same slicing as §2.2).
- The verdict series is the stitched OOS nav.

### 5.3 Menu selection

When a prereg evaluates K candidate configurations — the benchmark study's
core case — it must preregister **one deterministic selection rule**: a
function of (candidates, metrics, windows) → selection, including tie
breaks. "Best of K by eye" is not a rule. The benchmark study's rule lives
in PR-2026-001; the requirement lives here. Comparing losers to the winner
after selection is allowed only as post-hoc-labeled analysis (CONCEPT §2.4).

### 5.4 Multiple comparisons

Every prereg declares K — the number of candidate configurations evaluated
before the selection rule (K = 1 for a single configured strategy). The
null baseline (§5.5) is the published reference for what fraction of
random strategies passes the bar; the scoreboard tracks cumulative
confirmation rates against it as the archive grows. The null baseline is
always defined against the *default* criteria set: a prereg with
extended criteria (e.g. decade-level hard criteria, §4.1) is judged under
its own bar and its confirmations are labeled as such, not
rate-comparable with the default bar.

### 5.5 Null baseline

- **Purpose:** the published number for "what fraction of random strategies
  passes our bar through the identical pipeline."
- **Interface (fixed here; generator spec is a Phase 0 deliverable):**
  - *Identical pipeline:* same engine, same cost model, same metric
    definitions, same verdict mechanics, and the same observation cutoff as
    the real preregs sealed in the same month.
  - *Generator:* random strategies drawn from a published distribution
    over the same asset set and frequency, specified in its own versioned
    doc (`docs/NULL_BASELINE.md`, sealed once the engine is ready).
  - *Batch:* N = 1,000 random strategies per batch (default; overridable
    per methodology version); one batch per calendar month in which verdicts
    are published.
  - *Reporting:* null pass rate (hard criteria) and the distribution of
    headline metrics (Sharpe, CAGR, max DD), on the scoreboard beside the
    real rate.
- Until the first null batch is published, the scoreboard reports
  "null baseline: pending."

---

## 6. Runs, config hash, audit

### 6.1 Config hash

`config_hash = sha256(canonical_json(config))` where canonical JSON =
sorted keys, no whitespace, UTF-8. The config object:

```json
{
  "pr": "PR-2026-001",
  "prereg_blob": "<git blob sha of the sealed prereg doc at the seal commit>",
  "strategy": { "…all strategy parameters, fully expanded…": "…",
                "composite_placement": "…" },
  "data": {
    "shiller_ie_data": {"snapshot": "<sha256 of raw file>",
                        "usable_from": "1871.01", "usable_to": "2026.08"},
    "fed_funds":     {"snapshot": "…", "usable_from": "…", "usable_to": "…"},
    "gold":          {"snapshot": "…", "usable_from": "1970.01", "usable_to": "…"}
  },
  "costs": {"model": "v1", "overrides": {}},
  "analysis": {"scheme": "fixed-split", "in_sample_to": "1999.12",
               "walk_forward": null},
  "engine_commit": "<git sha of research/backtest/ at run time>"
}
```

- `prereg_blob` = `git rev-parse <seal_commit>:docs/preregistrations/<file>`.
  It is recorded in the **results doc**, never backfilled into the prereg —
  a sealed doc cannot contain its own seal (same discipline as the seal
  SHA).
- A result counts toward the scoreboard only if the config hash matches the
  sealed spec exactly (CONCEPT §2.3). Any difference, however small, is a
  new prereg — or a flagged amendment if the difference is a documented
  correction of an error that never affected the run.

### 6.2 Run log

Append-only, one JSON object per line, at
`research/strategies/<slug>/runs.jsonl`:

```json
{"run_id": "PR-2026-001-r001", "ts": "2026-10-02T14:00:00Z",
 "type": "verdict", "config_hash": "…",
 "data": {"shiller_ie_data": "<sha256>", "…": "…"},
 "engine_commit": "…",
 "output": "research/strategies/<slug>/out/r001/",
 "status": "ok", "notes": ""}
```

- `type`: `verdict` | `rerun` | `null`.
- CI re-runs append `rerun` entries and diff outputs against the published
  run; drift is published as an incident (CONCEPT §5).
- Past entries are never rewritten; corrections are new lines.

### 6.3 Verdict mechanics

- The results doc's frontmatter is machine-readable:
  `pr_id, seal_sha, config_hash, run_id, methodology, verdict, date`.
- The results doc contains a **criteria table**: every pre-registered
  criterion, marked hard/soft, with threshold, observed value, and
  pass/fail.
- Verdict assignment:
  - every hard criterion met → **CONFIRMED**
  - any hard criterion failed → **FALSIFIED**
  - the run failed for data/execution reasons (engine bug, missing data,
    snapshot gap) → **INCONCLUSIVE** with the reason; re-runnable under new
    run IDs, judged against the *original* criteria
- A third party must be able to assign the verdict from the results doc
  alone (CONCEPT §3). If they can't, the results doc is incomplete and the
  verdict stands as INCONCLUSIVE until it is.
- Verdicts are assigned by the research agent and reviewed by the owner
  (CONCEPT §11, team split); the results doc records who assigned it.

### 6.4 Amendments

After sealing, a prereg doc is edited **only** in its `## Amendments`
section. Permitted kinds:

1. factual or typographical corrections (including spec numbers that never
   affected the run — the config hash is the arbiter);
2. data-availability notes;
3. clarifications that do not change what was run or the bar.

If the intended change alters what was run or the bar, it is a **new
prereg**, not an amendment. Amendments commit as
`docs(prereg): PR-YYYY-NNN amendment — <reason>` with the justification in
the body (research-commit skill, ceremony rule 4).

---

## 7. What this document does not cover

- **Composite recipe** — its own sealed, versioned spec (CONCEPT §11).
- **The prereg template** — `docs/templates/PR_TEMPLATE.md`, drafted after
  two or three real preregs have settled the shape (CONCEPT §4).
- **The null-baseline generator** — Phase 0 deliverable, its own versioned
  doc.
- **Video production** — `videos/VIDEO_CONCEPT.md`.
- **The data-file contract** — `data/README.md` + `verify.py` are the
  single source of truth; this document references, not restates.
- **Per-hypothesis detail** — that is the prereg itself.
