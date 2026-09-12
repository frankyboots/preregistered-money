# Preregistered Money

**One paragraph.** A YouTube channel + public GitHub repo where we research trading strategies the way a clinical trial is run: every hypothesis is written down, sealed with a git commit, and judged against pre-registered criteria *before* we look at the full results. Backtests, code, data configs, agent prompts, and the video production pipeline are all public. The deliverable is not any single strategy — it is a multi-year public **scoreboard** of hypotheses that were confirmed, falsified, or came out inconclusive, plus the aggregate record of the strategies we decide to actually trade (see *Pinning*, §5).

It is also a personal record: the channel documents one quant's journey in public — starting from an analysis of the owner's own long-term portfolio and iterating from there. Every analysis, strategy, and verdict is the next chapter.

The name is the method. Preregistration is borrowed from clinical trials and psychology, where it exists to stop researchers from quietly re-running analyses until something "works." Quant backtesting has the same failure mode, at industrial scale. We make the discipline the brand.

---

## 1. The core idea

### What preregistration fixes

Backtest research is corrupted by *researcher degrees of freedom*: pick a different window, add a filter, change a cost assumption, drop a bad year — repeat until the Sharpe looks good. Nobody (including us, honestly) can keep a perfect mental ledger of every variation tried. Preregistration replaces the mental ledger with an immutable, timestamped, public record:

1. **Before** running the decisive backtest, the hypothesis, data spec, strategy spec, cost model, and *pass criteria* are written into a preregistration doc.
2. That doc is committed to git and **sealed** — the commit SHA becomes the timestamp and the seal (git is the notary).
3. Results are published in separate commits that reference the seal. Anyone can diff the preregistration against the final run config and verify nothing moved.
4. The verdict is decided by the pre-registered criteria, not by how the results *look*.

### What it does NOT fix (we say this out loud, every results video)

- **Backtest ≠ live.** Preregistration stops *data snooping*; it does not close the gap between the model and the market. Costs, fills, liquidity, and regime shifts all still bite.
- **Overfitting upstream.** Model choice, data cleaning, feature selection — all decisions made *before* sealing — can bake in overfitting. Preregistration narrows the snooping surface, it doesn't eliminate it.
- **Multiple comparisons at the archive level.** As the archive grows, some confirmations will be luck. We address this head-on with a **null baseline** (see scoreboard): we periodically run random strategies through the identical pipeline and publish what fraction passes our bar *by chance*. Our real confirmation rate is only meaningful against that number.
- **Data limitations.** Point-in-time correctness, survivorship bias, and data vendor quirks are recorded per preregistration and treated as a stated weakness, not a footnote.

---

## 2. The rules (integrity rules)

Boring, mechanical, enforced by CI where possible:

1. **One prereg per hypothesis.** The prereg names the exact strategy config, data, and bar. Running a different config requires a *new* prereg (or a flagged amendment).
2. **Sealed docs are append-only.** After sealing, edits go into an `## Amendments` section with a justification. The git history is the audit trail; we never rewrite it.
3. **No silent re-runs.** All backtest runs are logged (config hash → output). A result only counts toward the scoreboard if it matches the sealed config exactly.
4. **Post-hoc analysis is labeled post-hoc.** If results suggest something new, that something gets *its own* prereg before its results count for anything. This is the most important rule — it's how we convert failures into the next hypothesis without contaminating the scoreboard.
5. **Costs are never optional.** Every backtest includes commissions, spread, slippage (modeled), and borrowing/fees where applicable. A strategy that only works with zero costs is falsified by definition.
6. **No look-ahead.** Data is consumed as-of the strategy's decision time; universe membership is point-in-time; we document exactly how (or that we fail to) handle delistings/survivorship.
7. **Falsification is a success state.** A strategy that fails its bar is published, post-mortemed, and celebrated. The channel's credibility is built on what we *didn't* fudge.
8. **Reproducible everything.** Pinned data snapshots, pinned dependency versions, a CI job that re-runs the latest prereg end-to-end. If a viewer can't reproduce a number, we treat it as a bug.

---

## 3. Preregistration protocol

### Lifecycle

```
DRAFT  →  SEALED  →  RUN  →  VERDICT
                          ├─ CONFIRMED   (met every pre-registered criterion)
                          ├─ FALSIFIED   (failed any hard criterion)
                          └─ INCONCLUSIVE (data/execution problems; re-runnable)
```

- **SEALED** happens at a commit; the SHA is recorded in the doc and on the scoreboard.
- **Verdicts are decided by the criteria, not by vibes.** The criteria section must be complete enough that a third party can assign the verdict from the published results alone.
- **PIN** (optional, confirmed strategies only): a dated commit in which the owner decides to actually trade the strategy. Pinned strategies enter the composite, tracked forward from the pin date (see §5).
- **Withdrawn** (rare): allowed only for non-research reasons (data vendor died, legal issue). Withdrawals are public and explained.

### IDs

`PR-YYYY-NNN` — e.g. `PR-2026-001`. Monotonic, no gaps, no reuse.

### Special case: the benchmark study

Benchmark selection is itself a degree of freedom — a strategy measured against whichever yardstick it beats most easily has been snooped on, just as quietly. So the first artifact is a prereg of its own: a **benchmark study** (PR-2026-001) with the question pre-registered — of passive allocations across SPX, 10-year Treasuries, and gold (single assets and fixed blends), which is the long-term yardstick for this portfolio, and on what pre-registered criteria. Candidate set, data windows, and selection criteria are sealed *before* the selection happens. The chosen allocation is **frozen at seal**: any change is a new study, a new PR. Every later alpha strategy is judged against the frozen benchmark — never against whichever asset happened to do well.

---

## 4. Preregistration document (schema)

Every prereg contains, in order:

| Section | Contents |
|---|---|
| **ID / meta** | ID, date sealed, seal SHA, owner(s), status |
| **Hypothesis** | One sentence, falsifiable. ("A trend signal across SPX / TLT / GLD, rebalanced monthly, beats the selected passive benchmark out-of-sample after costs.") |
| **Mechanism** | Why we expect it to work (or what we're testing if we're uncertain). |
| **Data** | Universe, asset list rule, period, frequency, sources, point-in-time treatment, survivorship handling, known data caveats. |
| **Strategy spec** | Signals, entry/exit, position sizing, rebalance schedule, constraints. Exact, parameterized, no ambiguity. |
| **Costs & frictions** | Commission, spread, slippage model, borrow/fees, execution assumptions. |
| **Benchmark** | What it must beat (and on which metrics). |
| **Pass criteria** | Pre-registered thresholds: in-sample and out-of-sample metrics (e.g., OOS Sharpe > X, max DD < Y, turnover in Z band, capacity estimate). Explicitly which are *hard* (fail = falsified) and which are *soft* (context). |
| **Analysis protocol** | Train/test split or walk-forward scheme, multiple-comparisons notes, exact run procedure. |
| **Falsification notes** | What evidence would change our minds about the mechanism, even if the bar is met. |
| **Amendments** | (Append-only, post-seal) |

A machine-readable frontmatter block (YAML) mirrors the key fields so the scoreboard and CI can parse preregs without an LLM in the loop.

> The formal fill-in template will live at `docs/templates/PR_TEMPLATE.md` once we've done two or three real ones and settled the shape.

---

## 5. The scoreboard (the actual product)

The scoreboard is a generated artifact (script + CI, checked into the repo, rendered as the channel's homepage and as a recurring video segment):

- **Table**: every PR with ID, hypothesis (one line), date sealed, verdict, headline OOS numbers, link to results doc + video.
- **Aggregate stats**: total preregs, confirmed / falsified / inconclusive, **confirmation rate vs. null baseline** (random-strategy pass rate through the same pipeline).
- **The composite (pinned strategies only)**: an aggregate curve of *pinned* strategies, computed by a fixed, published recipe, tracked forward from each strategy's pin date. This is the "track record" the name promises — the strategies the owner has decided to actually trade. Until the first pin, the composite is dormant.
- **Re-runs**: CI re-executes a sample of sealed preregs on a schedule; any drift between published and re-run results is published as an incident.

### Pinning

A *pin* is a recorded, dated act (git commit, `PIN-YYYY-NNN` ID, linked to a prereg) in which the owner decides to actually trade a strategy — paper or live, recorded in the pin. Rules:

- Only **confirmed** strategies can be pinned; the bar for entry into the composite is a preregistered confirmation.
- Pinned strategies enter the composite, tracked forward from the pin date — the composite is a live record, not a backtest.
- Pinning is discretionary: a confirmed strategy may be left unpinned (noted on the scoreboard). Unpinning is allowed, recorded, and requires a published rationale.
- Early on, the composite is deliberately quiet — no first pin, no composite. The early content is the journey: the portfolio analysis, the first strategy, the process.

The scoreboard is the multi-year asset. Individual strategies come and go; the archive of *preregistered hypotheses + honest outcomes* is unique, compounding, and impossible to replicate quickly by anyone else.

---

## 6. Repository layout

```
preregistered-money/
├── docs/
│   ├── CONCEPT.md              # this file
│   ├── METHODOLOGY.md         # expanded rules, cost models, data policy
│   ├── preregistrations/      # PR-YYYY-NNN.md (one per hypothesis)
│   ├── results/               # PR-YYYY-NNN-results.md (references the seal)
│   └── templates/
├── research/
│   ├── backtest/              # small in-house backtest engine (transparent, testable)
│   ├── data/                  # loaders, manifests, snapshot pins (no raw dumps)
│   └── strategies/            # one package per PR, config-driven
├── agents/                    # agent definitions + prompts used in research & production
├── videos/
│   └── <video-slug>/          # hyperframes composition (HTML/CSS/JS) + build log
├── scoreboard/
│   ├── build.py               # regenerates the scoreboard from prereg+result docs
│   └── SCOREBOARD.md          # generated; do not hand-edit
└── .github/workflows/         # CI: re-runs, scoreboard build, video render
```

Raw data generally does not live in the repo — data *manifests* (source, version, checksum, download recipe) do, so snapshots are reproducible without shipping gigabytes.

---

## 7. Tech stack

**Research**
- Python; small **in-house backtest engine** (vectorized, explicit costs, walk-forward support) — deliberately small so every line is explainable in a process video and no black-box library can hide look-ahead.
- pandas/polars; data starts with fully public, $0 sources for the initial three-asset universe: **SPX** (index history; SPY as the investable proxy), **10-year Treasuries** (FRED: DGS10 yield, DFII10 total-return index for pre-ETF history; TLT as the investable proxy), **gold** (LBMA fix via FRED for long history; GLD as the investable proxy). Every proxy caveat (ETF vs. underlying, price vs. total return, fee drag, duration mismatch) is documented per prereg. Crypto, FX, and single-stock equities are later expansions, not the initial scope.

**Video**
- **HyperFrames** (open-source, agent-driven HTML→MP4): agents write plain HTML/CSS/JS compositions; headless browser captures frames; FFmpeg encodes. Deterministic — same input, same pixels — which matters for a channel whose brand is reproducibility.
- Simple style: data-forward, minimal motion, our own restrained palette/type. Fully faceless — no on-camera presence; voiceover by **ElevenLabs v3** TTS.
- Each video = one repo directory: composition + data inputs + build log, so every published frame is regenerable from the repo.

**Ops**
- GitHub Actions: pinned env, reproducible backtest re-runs, scoreboard regeneration, video renders.
- Everything MIT-licensed (code) / CC-BY (content) unless a later doc says otherwise.

---

## 8. Content model

### Series

1. **Portfolio** (journey episodes) — the spine of the channel: the ongoing analysis of the owner's long-term portfolio — what's in it, what the data says, what changes and why. Every portfolio decision that becomes a tradable hypothesis ends in a prereg. The channel opens here: the first artifact is the **benchmark study** — a long-term analysis of SPX, 10-year Treasuries, and gold to select the passive benchmark (preregistered as PR-2026-001, see §3) — and the first strategy is a tactical one within the same three asset classes, targeting alpha against the selected benchmark.
2. **Seal** (preregistration episode) — present a new hypothesis: the mechanism, the data, the bar it must clear, the falsification notes. Ends with the commit being sealed on camera (literally). ~8–15 min.
3. **Verdict** (results episode) — the run, the numbers against the pre-registered bar, the scoreboard update, and an honest read on what the result actually means. Falsified strategies get the same production value — and a **post-mortem** segment on what the mechanism got wrong. ~10–20 min. A confirmed strategy may end with the pin decision, on screen. **Verdict videos are self-sufficient**: they open with a short recap of the preregistration (hypothesis, the pre-registered bar, seal date + SHA) so a viewer who never saw the seal episode understands the whole exchange; the seal episode and prereg doc are linked in the description.
4. **Build log** (process episodes) — the agents, the backtest engine, data pipelines, video tooling. This is the "build in public" half of the brand: we show how the machine that produces this channel works, including its failures.
5. **Meta** — methodology deep-dives (multiple testing, the null baseline, cost models, point-in-time data), archive retrospectives, "state of the scoreboard" milestones.

### Cadence (starting proposal)

- 2 new preregs sealed per month; verdicts land 4–8 weeks after sealing (keeps the seal meaningful — no same-day results).
- 1–2 videos/week, mixed: new seals, verdicts, build logs.
- The scoreboard rebuilds on every merge to main.
- Early phase: cadence follows the journey — portfolio-analysis episodes and the first strategy's development take priority over the 2-per-month seal rate, which ramps up once the pipeline is proven.

---

## 9. Multi-year plan

**Phase 0 — Foundation (months 1–2).** Repo, backtest engine + unit tests, data manifests, prereg template, scoreboard generator, one hyperframes pipeline producing a real (simple) video. The first public artifact is the **benchmark study** (PR-2026-001): the long-term analysis of SPX, 10-year Treasuries, and gold that selects the passive benchmark; the first strategy preregs emerge from it, alongside a methodology video explaining the rules.

**Phase 1 — The first ledger (months 3–12).** Steady cadence; target ~15–25 sealed preregs, first verdicts published, null baseline computed. The **first strategy** — a tactical one within the same three asset classes, targeting alpha against the selected benchmark — is developed end-to-end from the portfolio analysis; if it confirms, it becomes the **first pin** and the composite goes live. Until then, content stays journey-first: portfolio analysis, strategy development, process. Goal: the scoreboard is recognizable and the archive has both wins *and* losses.

**Phase 2 — Depth (year 2+).** Harder data (equities with point-in-time handling), richer strategy classes (multi-asset, regime-conditioned), the pinned composite extends from paper to live trading so the record goes beyond the backtest, deeper meta-analysis of the archive. The channel becomes a public research dataset as much as a YouTube channel.

**The end-state claim we can actually make:** "Here is a public, auditable record of N preregistered quant hypotheses, how many survived, what the survivors did out-of-sample, and what the pinned subset has done since — every step reproducible from this repo."

---

## 10. Honest limitations (standing disclaimer, on every video)

- Educational content, not investment advice.
- Backtest results are estimates under stated assumptions; live performance will differ, possibly badly.
- Preregistration controls data snooping; it does not control overfitting in pre-seal choices, data quality, or market regime change.
- Past performance (including preregistered, costed, out-of-sample past performance) is the weakest predictor in finance.

---

## 11. Open questions (iterate on these)

**Resolved (September 2026):** starting point is the owner's personal long-term portfolio analysis, iterating from there; the composite tracks *pinned* strategies only, where pinning is the owner's recorded decision to trade; production is fully faceless with ElevenLabs v3 voiceover; initial universe is **SPX, 10-year Treasuries, gold** — the opening study is a long-term analysis of these three asset classes for **selecting a passive benchmark**, and the first active strategies target **alpha against the selected benchmark** while staying within the three asset classes; **team split** is a non-concern: one owner plus hermes agent profiles, with the research/video separation mechanical — a fresh agent in a separate session loading a different skill is a different agent, so the video agent never touches the run config; **bar calibration** is empirical — pass criteria get felt out over the first handful of seal→verdict cycles, with the null baseline as the published reference.

Still open:

1. **Composite recipe.** Direction forming (September 2026): *risk-weighted* (inverse-vol) across pinned sleeves, with composite-level vol-targeted leverage — gross exposure scaled up/down to a target realized vol, within a band, excess in cash/T-bills. Strategies are designed to be complementary and to *nest within one another*, so the composite is a tree of sleeves (frozen passive base + pinned tactical sleeves), not a flat list. Split of judgment: Sharpe governs the *pin* (membership — discretionary, prereg-confirmed, recorded); rolling vol governs *sizing* (mechanical, in the recipe). Paper tracking at the first pin; live from Phase 2 (§9). The recipe itself is a Phase 0 deliverable: a versioned, sealed spec — changes are new versions, append-only, never retroactive. Open parameters: target vol, exposure band, vol-estimation window, rebalance frequency, per-sleeve weight cap, and whether the frozen passive base sits inside the composite or alongside it. Schema note: the strategy spec carries an explicit *composite placement* field (sleeve, intended role, interaction with siblings).
2. **Data budget.** What will we actually spend on data in year 1? (Leaning: $0 — public sources only; the three-asset stack fits this.)
3. **Naming/branding details.** Channel art, handle, whether "The Ledger" / "the scoreboard" gets an official name.

---

## 12. Non-goals

- No prop-trading P&L chasing, no signal-selling, no paid "alpha" tiers — the scoreboard is the product and it stays free and public.
- No high-frequency or latency-sensitive strategies (the data and backtester won't support honest backtests of them; out of scope).
- No live trading advice, no managed accounts, no "DM us for the strategy."
- No content we can't reproduce from the repo. If it's not in the repo, it didn't happen.
- Early phase: nothing outside SPX / 10-year / gold. Scope expansion is a published, dated decision — not drift.
