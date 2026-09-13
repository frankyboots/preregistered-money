# Scene spec 06 — the bar

Status: SPEC (Phase B). Template: `meta:bar-chart`.

## Scene Identity

- Scene ID: `scene-06`
- Working title: bar
- Window: **128.57–162.06s** (beat-06, `audio/timing/beat-map.json`; speech 128.61–160.78, hold 160.78–162.06)
- Output format: 1920×1080, 24fps, draft quality (Phase C)
- Source composition: `composition/scene-06.html`
- Render output: `renders/scene-06.mp4`

## User Intent

- Objective: what a pre-registered bar is — a cost-adjusted number to reach,
  drawn last on the chart, identically whether the strategy passes or fails:
  same chart, same bar; the curve's position relative to the line is the
  story.
- Tone: plain, procedural, neutral. A rule, not a result.
- Must communicate: draw order (series, then the bar last); the tag's value
  is an example, labeled on screen; and that the two charts differ only in
  where the curve ends relative to the line.
- Must not feel like: a result reveal, a win/loss celebration, a SaaS
  dashboard.

## Inputs

- Narration: beat-06, `narration.md` (71 words).
- Cue source: `audio/timing/words.json` (master sha256 `4cfb0cb0…`).
- Data inputs: **none — no real number appears in this scene.** The bar tag
  `bar: ≥ 6.0% OOS CAGR` is the pinned example string of style spec §4.4,
  labeled `example` on screen (citation: `spec.md` Number citations row
  "Bar tag example (beat 6)"; placeholder rule per
  `video-intake-and-storyboard`). Chart axes carry no tick labels — a scaled
  exemplar chart would invent data.
- Corner bug: standard, fades in at scene open (200ms).

## Visual Direction

- Background: `--ink`.
- Layout (1920×1080):
  1. **Title zone** (top-left under the bug): `the bar` (Inter 600,
     `--fs-title`, `--paper`) + definition line `a number to reach, after
     costs` (mono `--fs-anno`, `--paper-dim`).
  2. **Chart A** (left, main): plot x 120–960, y 240–700. Axes `--paper-dim`
     1px (left + bottom), 3 horizontal gridlines at 40% opacity, no tick
     labels. Cost-adjusted series: `--paper` 3px solid, a rising curve with
     one mid dip (authoring choice), from bottom-left (≈y 660) to endpoint
     **(900, 380)** — 100px **above** the bar. Bar: solid `--seal-amber`
     3px horizontal line at **y=480**, x 120–960, drawn last after the
     series (§6.2). Tag above it at the right end (right-aligned x=960,
     y≈452): `bar: ≥ 6.0% OOS CAGR` (mono `--fs-anno`, `--paper`); `example`
     label (mono `--fs-anno`, `--paper-dim`, boxed) directly above the tag
     (right-aligned x=960).
  3. **Chart B** (right, small — the beat sheet's "second small chart"):
     plot x 1160–1840, y 320–640, same axis style, no tick labels. Series:
     **the same curve as A, translated down** to fit the smaller plot —
     endpoint **(1780, 560)**, 80px **below** the bar. Bar: same
     `--seal-amber` 3px line at **y=480** (the same screen height as A's bar
     — "same bar" literally), x 1160–1840, drawn last. Tag: same string
     `bar: ≥ 6.0% OOS CAGR` right-aligned x=1840, y≈452; no second
     `example` box (the label is established once in A; the bar is the same
     value — duplication would clutter).
  4. **Annotations**: `no results document exists yet` (mono `--fs-anno`,
     `--paper-dim`) centered under chart A (y≈740); direct labels near the
     endpoints — `above` (A, right-aligned ending x≈880, y≈352) and `below`
     (B, right-aligned ending x≈1750, y≈586), mono `--fs-anno`,
     `--paper-dim` (§6.3: labels near objects).
  5. **Tagline** (centered x=960, y≈872): `and that is the story` (Inter
     400, `--fs-body`, `--paper`).
- Colors: series `--paper`; the only amber is the two bar lines
  (`--seal-amber`, §4.4); axes/gridlines/annotations `--paper-dim`.
  **No verdict colors**: "passes or fails" is narrated but nothing is judged
  here — the chart stays neutral (§6.6); verdict colors appear only in the
  verdict card and the scoreboard cells.
- Typography: data (tag, annotations) JetBrains Mono `--fs-anno`; title
  Inter 600 `--fs-title`; tagline Inter 400 `--fs-body`.
- Motion: reveal (250ms, 12px slide-up) for title, definition, tag, example
  box, annotations, tagline; draw (600ms) for both frames/axes; draw
  (800ms) for series A; draw (600ms) for series B; draw (400ms, pinned,
  §5.2) for both bar lines. No roll, no stamp. Nothing after the last word.
- Open state: at window start the frame is ink + corner bug only — the
  charts are named on their words ("The chart draws…"), so nothing
  pre-exists.

## Beat Timeline

Times are word starts from `words.json`; visual completes within ≤250ms
unless noted.

| Time | Word (narration, words.json) | Visual action | Required proof |
|---|---|---|---|
| 128.57 | — | open: ink, corner bug fades in; no scene elements | first frame |
| 128.78 | `bar,` | title `the bar` reveals | t=129.03 |
| 130.18 | `number` | definition `a number to reach, after costs` reveals | t=130.43 |
| 133.12 | `chart` | chart A frame + axes draw (600ms; frame, not data) | t=133.72 |
| 133.96 | `cost-adjusted` | chart A series draws left→right (800ms; lands 8ms after word end, noted) | t=134.76 series complete |
| 135.98 | `bar,` | chart A bar line draws (400ms, pinned; lands 140ms after word end, noted) | t=136.38 bar complete |
| 140.30 | `tag` | tag `bar: ≥ 6.0% OOS CAGR` reveals above bar A's right end | t=140.55 |
| 140.90 | `example` | `example` box reveals above the tag | t=141.15 |
| 145.46 | `yet.` | annotation `no results document exists yet` reveals under chart A | t=145.71 |
| 151.86 | `chart,` | chart B frame + axes draw (600ms) | t=152.46 |
| 152.64 | `same` | chart B series draws (600ms — the verb minimum; same curve, translated down; lands 330ms after word start, noted) | t=153.24 series complete |
| 152.96 | `bar.` | chart B bar line draws (400ms, pinned) — starts deferred at 153.30 to keep series-before-bar order (§6.2; lands 153.70, 460ms after word start, noted) | t=153.70 bar complete |
| 156.72 | `ends` | direct labels reveal as a unit: `above` at A's endpoint, `below` at B's endpoint | t=156.97 |
| 160.40 | `story.` | tagline `and that is the story` reveals | t=160.65 |
| 160.78 | (speech ends) | final hold — nothing moves (earned hold, §5.1 rule 5) | t=161.40 = final state |
| 162.06 | — | hard cut to scene-07 | t=162.05 stable |

Cue-keying notes: title keys to `bar,` (first word); definition to `number`
("a number to reach"); series A to `cost-adjusted`; bar A to the second
`bar,` (the draw-order sentence — "then the bar, an amber line, last"); tag
to `tag`; example box to `example`. Chart B cues key to the "Same chart,
same bar." pair — frame to `chart,`, series to `same`, bar to `bar.`; that
pair is the narration's naming of the second chart. `above` / `below` are
never spoken — they key to `ends` ("where the curve **ends** relative to
the line"), per the on-screen-label rule.

Change floor: 32.17s continuous speech (128.61–160.78, no gap >3s), 13
state changes — per 10s span: 5 (128.6–138.6), 3 (138.6–148.6), 4
(148.61–158.61), 1 (158.61–160.78) ✓. No pre-naming ✓ (empty open; every
element on its word).

## Continuity

- First frame: ink + corner bug only (hard cut from scene-05's final frame:
  the settled seal → empty chart frame).
- Last frame: two charts — A with the series ending above its amber bar,
  tag + `example`; B with the same curve ending below its bar; `above` /
  `below` labels; `no results document exists yet`; tagline.
- Transition in: hard cut from scene-05 (the seal's rule applied to a bar:
  pre-registered, always drawn — the cut carries it).
- Transition out: hard cut to scene-07 (the ledger; its spec opens from
  ink).
- Carryover frames: none.

## QA Checklist

- Final-frame proof: **t=161.40** — both charts settled, both bars, tags,
  labels, annotation, tagline; nothing moves.
- Boundary proofs: t=134.76 (series A complete), t=136.38 (bar A),
  t=140.55 (tag), t=141.15 (example box), t=145.71 (results-doc annotation),
  t=152.46 (B frame), t=153.24 (B series), t=153.70 (B bar), t=156.97
  (above/below), t=160.65 (tagline), t=162.05 (hold stable to cut).
- Caption proof: lowest elements are the tagline (y≈872, descender ≈887)
  and the annotation (y≈740); the bottom 132px band (from y=948) is empty.
- Audio sync: definition by end of "number" (130.46); series A by end of
  "cost-adjusted" (134.68, +8ms noted); bar A by t=136.38 (pinned 400ms —
  140ms after end of "bar," (136.24), noted); tag by end of "tag" (140.64);
  example box by end of "example" (141.44); B bar by t=153.70 (named from
  "bar." 152.96; the deferral is the pinned draw order); above/below by end
  of "ends" (157.24); tagline by end of "story." (160.78).
- Known risks: (1) Chart A right-side stack — endpoint (900, 380) vs
  `above` label (y≈352) vs `example` box (y≈424–444, x 850–960) vs tag
  (y≈430–452): ≥40px vertical gaps, verify in probe; tag width (20 chars ×
  ≈13.2px ≈ 264px, spanning x 696–960) vs the curve passing that x range —
  verify no overlap. (2) Bars at the pinned 400ms complete after their
  naming word ends (A: +140ms) — pinned verb parameter overrides the
  ≤250ms guideline; verify in probe the draw still reads as "the bar draws
  last." (3) B series at 600ms (verb minimum) + B bar deferred to 153.30 —
  verify the pair reads as same-chart/same-bar, not lag. (4) No tick labels
  — verify no axis numbers render (the exemplar chart is unscaled). (5) `≥`
  glyph in the tag — verify JetBrains Mono renders it; fallback is `>=`.
- Acceptance: lint 0 errors; final-frame proof matches layout; tag string
  on screen byte-identical to style spec §4.4's example text; `example`
  label present; the only amber pixels are the two bar lines
  (`scan_theme_colors.py` clean); no verdict colors; no other number in the
  scene.
