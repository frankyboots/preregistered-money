# Scene spec 07 — the ledger

Status: SPEC (Phase B). Template: pinned `ledger` (style spec §4.7) + `meta:aggregate-rows`.

## Scene Identity

- Scene ID: `scene-07`
- Working title: ledger
- Window: **162.06–205.47s** (beat-07, `audio/timing/beat-map.json`; speech 162.13–204.20, hold 204.20–205.47)
- Output format: 1920×1080, 24fps, draft quality (Phase C)
- Source composition: `composition/scene-07.html`
- Render output: `renders/scene-07.mp4`

## User Intent

- Objective: the scoreboard is the product — one table, one row per prereg
  (ID, hypothesis, date sealed, verdict, headline OOS number, link), aggregate
  rows above it (total preregs, verdict counts, confirmation rate vs. a null
  baseline), and the composite row below — dormant until the first pin.
- Tone: plain, procedural, neutral. A product tour of an empty product: the
  layout, not a result.
- Must communicate: the pinned ledger layout; that every row and count on
  screen is an example, labeled on screen; that verdict cells carry the verdict
  colors and nothing else does; that the composite exists but is dormant, and
  the label says so.
- Must not feel like: a results reveal, a leaderboard with winners, a SaaS
  dashboard.

## Inputs

- Narration: beat-07, `narration.md` (86 words).
- Cue source: `audio/timing/words.json` (master sha256 `4cfb0cb0…`).
- Data inputs: **none — no real number appears in this scene.** The three
  example rows, the three aggregate values, and the null-baseline annotation
  are pinned placeholder strings: `PR-0000-000`-style IDs (never a real PR
  number — `spec.md` beat-sheet citation note), example metrics, all labeled
  `example` / `examples` on screen in annotation type (citation: `spec.md`
  Number citations row "Ledger example rows (beat 7)"). No results or
  scoreboard data exists yet; nothing is computed in the composition.
- Corner bug: standard, fades in at scene open (200ms).

## Visual Direction

- Background: `--ink`.
- Layout (1920×1080), all x from the left edge:
  1. **Title zone** (top-left under the bug): `the scoreboard` (Inter 600,
     `--fs-title`, `--paper`, baseline y≈112) + definition
     `the product` (mono `--fs-anno`, `--paper-dim`, same baseline,
     x≈490).
  2. **Aggregate block** (above the table, per the committed narration):
     section rule (1px `--paper-dim`, x 80–1840, y=148). Rows mono
     `--fs-table`, labels `--paper-dim` / values `--paper`:
     - row 1 (baseline y≈176): `preregs: 3`, `example` box (mono
       `--fs-anno`, `--paper-dim`, boxed) at its right (x≈330).
     - row 2 (baseline y≈210): `confirmed: 1  falsified: 1  inconclusive: 1`
       (the three verdict words in their verdict colors, counts `--paper`).
     - row 3 (baseline y≈244): `confirmation rate vs. null: 1/3`.
     - annotation (baseline y≈276): `null baseline: the fraction random
       strategies pass by chance` (mono `--fs-anno`, `--paper-dim`).
  3. **Ledger table** (pinned §4.7, x 80–1840): header JetBrains Mono
     uppercase `--paper-dim` letterspaced (`--fs-anno`), baseline y≈312,
     `--paper-dim` rule below (y=328). Columns — PR ID x 80–320 · hypothesis
     x 320–820 · date sealed x 820–1020 · verdict x 1020–1260 · OOS
     x 1260–1420 · link x 1420–1840. Three rows, 56px each (pinned), y
     328–384, 384–440, 440–496; cell text mono `--fs-table`, `--paper`
     except the verdict cell:
     - row 1: `PR-0000-000` · `trend carries OOS` · `2026-01-01` ·
       `confirmed` (`.v-confirmed`) · `+3.4%` · `results/PR-0000-000`
     - row 2: `PR-0000-001` · `carry beats its costs` · `2026-01-15` ·
       `falsified` (`.v-falsified`) · `−1.2%` · `results/PR-0000-001`
     - row 3: `PR-0000-002` · `momentum survives costs` · `2026-02-01` ·
       `inconclusive` (`.v-inconclusive`) · `+0.8%` · `results/PR-0000-002`
     Ruled per `setpieces.css` `.ledger` (1px `--paper-dim` header rule; cell
     rules `--paper-dim` at 35%).
  4. **Composite row** (pinned, last row of the table): 2px `--paper` rule
     above (y=496), row y 496–552, distinguished by the rule not color (§4.7).
     First cell `composite` (mono `--fs-table`, `--paper`); remaining cells
     empty (rules only). Dormant label within the row under the hypothesis
     column (x≈340, baseline y≈528): `dormant — no pins yet` (mono
     `--fs-anno`, `--paper-dim`).
  5. **Annotation** (below the table, left x=80, baseline y≈596):
     `all rows are examples` (mono `--fs-anno`, `--paper-dim`).
- Colors: `--paper` / `--paper-dim` base; **verdict colors appear only in the
  three verdict cells** (and the three matching words in aggregate row 2) —
  `--confirmed`, `--falsified`, `--inconclusive` via the pinned classes. No
  amber (nothing is pending in this scene). P&L rule untouched: no
  red/green for deltas — the OOS cells are plain `--paper` mono.
- Typography: all table data + aggregate values JetBrains Mono `--fs-table`;
  annotations, header, labels mono `--fs-anno`; title Inter 600 `--fs-title`.
- Motion: draw (600ms) for the table frame + header (frame-level, §5.1 rule
  2); reveal (200ms — the table-row verb, §5.2) for each column unit,
  aggregate row, annotation, and the composite row; reveal (250ms) for title
  and definition. No roll (values are table cells, not hero numbers), no
  stamp. Nothing after the last word.
- Open state: at window start the frame is ink + corner bug only — the table
  is named on its word ("One table,"), so nothing pre-exists.

## Beat Timeline

Times are word starts from `words.json`; visual completes within ≤250ms
unless noted.

| Time | Word (narration, words.json) | Visual action | Required proof |
|---|---|---|---|
| 162.06 | — | open: ink, corner bug fades in; no scene elements | first frame |
| 162.30 | `scoreboard` | title `the scoreboard` reveals | t=162.55 |
| 163.40 | `product.` | definition `the product` reveals | t=163.65 |
| 165.54 | `table,` | ledger frame + column headers draw (600ms; lands t=166.14, 248ms after word end, noted) | t=166.14 frame + header complete |
| 167.44 | `prereg` | PR ID column reveals — all three row cells as one unit (200ms) | t=167.64 |
| 169.64 | `hypothesis,` | hypothesis column reveals (200ms) | t=169.84 |
| 170.78 | `seal` | date sealed column reveals (200ms — "seal date") | t=170.98 |
| 171.80 | `verdict,` | verdict column reveals (200ms; the only colored cells) | t=172.00 |
| 172.76 | `out-of-sample` | OOS column reveals (200ms) | t=172.96 |
| 174.36 | `link` | link column reveals (200ms) | t=174.56 |
| 177.62 | `examples` | annotation `all rows are examples` reveals under the table | t=177.87 |
| 181.74 | `aggregate` | section rule (1px) above the aggregate block reveals | t=181.99 |
| 183.14 | `Total` | aggregate row 1 `preregs: 3` + `example` box reveal as a unit (250ms) | t=183.39 |
| 184.50 | `confirmed,` | aggregate row 2 `confirmed: 1  falsified: 1  inconclusive: 1` reveals (250ms) | t=184.75 |
| 188.18 | `confirmation` | aggregate row 3 `confirmation rate vs. null: 1/3` reveals (250ms) | t=188.43 |
| 191.14 | `fraction` | annotation `null baseline: the fraction random strategies pass by chance` reveals | t=191.39 |
| 196.08 | `composite,` | composite row reveals (2px `--paper` rule + `composite` cell, 200ms) | t=196.33 |
| 202.30 | `dormant,` | label `dormant — no pins yet` reveals in the composite row | t=202.55 |
| 204.20 | (speech ends) | final hold — nothing moves (earned hold, §5.1 rule 5) | t=204.80 = final state |
| 205.47 | — | hard cut to scene-08 | t=205.46 stable |

Cue-keying notes: title keys to `scoreboard` (first word); definition to
`product.`; the frame+header to `table,` ("One table,") — frame-level,
permitted to pre-exist its cells (§5.1 rule 2). The six columns reveal on the
narration's own enumeration — `prereg` (a row's identity is its PR ID),
`hypothesis,`, `seal` ("seal date"), `verdict,`, `out-of-sample`, `link`.
Pinned §4.7's "rows reveal one at a time" governs rows the narration names
one by one; here the narration names the *columns*, so the column unit is the
reveal unit, in the narration's order (the pinned 200ms row verb is kept).
RESOLVED (owner, 2026-09-13): the column reading is accepted — ratified by
style-spec 1.1.1, which makes the narration's enumeration the reveal unit
(row-unit stays the default). `all rows are examples` keys to `examples`; the aggregate
block to `aggregate` (rule first, rows as named: `Total`, `confirmed,` — the
first of the three counted verdicts, `confirmation`); the null definition to
`fraction`; the composite row to `composite,` and its dormant label to
`dormant,` ("Until the first pin, it is dormant, and the label says so").
The `ID,` word (168.78) re-names the same column already revealed on
`prereg` — no second element, so no second cue.

Change floor: 42.07s continuous speech (162.13–204.20, no gap >3s), 17 state
changes — per 10s span: 7 (162.1–172.1), 4 (172.1–182.1), 4 (182.1–192.1), 1
(192.1–202.1), 1 (202.1–204.20) ✓. No pre-naming ✓ (empty open; every element
on its word; the `example` box is a label revealed with the first aggregate
row it qualifies).

## Continuity

- First frame: ink + corner bug only (hard cut from scene-06's final frame:
  the two charts → empty ledger frame).
- Last frame: full ledger — title + `the product`; aggregate block (rule,
  three rows, null annotation, `example` box); 3×6 example table with colored
  verdict cells; composite row under the 2px rule with `dormant — no pins
  yet`; `all rows are examples` annotation.
- Transition in: hard cut from scene-06 (the bar's rule — pre-registered,
  always drawn — meets the record that stores it: the ledger).
- Transition out: hard cut to scene-08 (the disclaimer card; its spec opens
  from ink).
- Carryover frames: none.

## QA Checklist

- Final-frame proof: **t=204.80** — full ledger settled as above; nothing
  moves.
- Boundary proofs: t=162.55 (title), t=163.65 (definition), t=166.14 (frame +
  header), t=167.64 (PR ID col), t=169.84 (hypothesis), t=170.98 (date),
  t=172.00 (verdict), t=172.96 (OOS), t=174.56 (link), t=177.87 (examples
  annotation), t=181.99 (section rule), t=183.39 (agg 1 + box), t=184.75
  (agg 2), t=188.43 (agg 3), t=191.39 (null annotation), t=196.33 (composite
  row), t=202.55 (dormant label), t=205.46 (hold stable to cut).
- Caption proof: lowest element is the `all rows are examples` annotation
  (baseline y≈596, descender ≈602); the bottom 132px band (from y=948) is
  empty.
- Audio sync: frame by end of "table," (165.86 — the 600ms draw lands
  166.14, +248ms noted); PR ID column by end of "prereg" (167.94); verdict
  column by end of "verdict," (172.25); OOS by end of "out-of-sample"
  (173.36); link by end of "link" (174.56, exact); examples annotation by
  end of "examples" (178.26); agg row 1 by end of "Total" (183.39, exact);
  agg row 2 by end of "confirmed," (185.11); agg row 3 by end of
  "confirmation" (188.76); null annotation by end of "fraction" (191.60);
  composite row by end of "composite," (196.56); dormant label by end of
  "dormant," (202.72).
- Known risks: (1) ~~column-unit reveals vs pinned §4.7 "rows one at a
  time"~~ — resolved: owner accepted the column reading 2026-09-13;
  style-spec 1.1.1 ratifies the column unit when the narration enumerates
  columns. (2) Width
  fits — longest hypothesis 302px in a 500px column; null annotation ≈779px
  from x=80; `results/PR-0000-000` ≈245px in a 420px column: verify in probe.
  (3) Verdict colors are the only chromatic pixels besides none —
  `scan_theme_colors.py` must show `--confirmed`/`--falsified`/
  `--inconclusive` confined to the three verdict cells and the three matching
  aggregate-row-2 words; no amber anywhere. (4) `−` glyph (U+2212) in
  `−1.2%` — verify JetBrains Mono renders it; fallback is ASCII `-`. (5)
  Two example labels (`example` box by aggregate row 1, `all rows are
  examples` under the table) — verify they read as one labeling system, not
  redundancy. (6) Aggregate row 2 verdict words colored while the counts are
  `--paper` — verify the split-color line renders cleanly at 24px.
- Acceptance: lint 0 errors; final-frame proof matches layout; the pinned
  `.ledger` set-piece classes (header style, 56px rows, verdict classes,
  composite 2px rule) are used — no ad-hoc table CSS; `PR-0000-00x` IDs
  byte-identical to the placeholder convention; both `example` labels
  present; no real PR number or results-doc path in the scene;
  `scan_theme_colors.py` clean.
