# Scene spec 02 — the failure mode (loop diagram)

Status: SPEC (Phase B). Template: `meta:loop-diagram`.

## Scene Identity

- Scene ID: `scene-02`
- Working title: loop-diagram
- Window: **2.69–27.86s** (beat-02, `audio/timing/beat-map.json`; speech 2.76–26.58, hold 26.58–27.86)
- Output format: 1920×1080, 24fps, draft quality (Phase C)
- Source composition: `composition/scene-02.html`
- Render output: `renders/scene-02.mp4`

## User Intent

- Objective: name quant backtesting's failure mode — quietly re-running until
  something "works" — and end on the unresolvable state: three identical runs,
  one survivor, no label for which is real.
- Tone: plain, unforgiving, no drama.
- Must communicate: the loop is defensible at every step, and the ledger is
  missing, so the survivor is indistinguishable.
- Must not feel like: a horror story, a rant, a stock-footage montage.

## Inputs

- Narration: beat-02, `narration.md` (57 words).
- Cue source: `audio/timing/words.json` (master sha256 `4cfb0cb0…`).
- Data inputs: **none. No number appears in this scene.** (No result values —
  "identical runs" is conveyed by identical bar glyphs, not digits.)
- Corner bug: standard, fades in at scene open (200ms).

## Visual Direction

- Background: `--ink`.
- Two states, one transition:
  1. **The loop** — one horizontal monospace chain, centered vertically:
     `run → nothing → re-run → nothing → re-run …` — nodes are plain mono text
     (`--fs-body`, `--paper`), arrows `--paper-dim` (draw verb, left→right).
     The trailing `…` carries "and so on" — the loop is not finite. `nothing`
     is the on-screen name for a run that "loses" (the loss words in the
     narration are *loses* / *something else* — "nothing" itself is never
     spoken, so nodes key to those words). Annotations land under the chain,
     mono `--fs-anno`, `--paper-dim`, one per "change" the narration lists.
  2. **The final state** — on "Three identical runs" the loop fades to 40%
     opacity and settles up; below it, three identical run lines (mono,
     identical `▮` bar glyphs — visually the same, no digits):
     `run 1 ▮▮▮▮▮▮▮▮`, `run 2 ▮▮▮▮▮▮▮▮`, `run 3 ▮▮▮▮▮▮▮▮`. One line carries a
     small `survivor` tag (mono, `--paper-dim`, boxed). Below: the annotation
     `no label for which is real`.
- Colors: `--paper` + `--paper-dim` only. No verdict colors (nothing is judged
  here), no amber.
- Typography: everything in this scene is JetBrains Mono (data machine).
  Title is Inter 400 30px `--paper-dim` (prose, top-left under the bug).
- Motion: reveal (250ms, 12px slide-up) for nodes/annotations; draw (600ms)
  for arrows; fade (200ms) for the loop dim. No stamp, no roll, no loops.

## Beat Timeline

Times are word starts from `words.json`; visual completes within ≤250ms unless noted.

| Time | Word (narration, words.json) | Visual action | Required proof |
|---|---|---|---|
| 2.69 | — | open: ink, corner bug fades in; blank diagram area | first frame |
| 2.98 | `failure` | title "the failure mode" reveals | t=3.00 |
| 5.02 | `backtest` | node `run` types in (mono, ~100ms/char) | t=5.10 |
| 6.64 | `loses` | arrow draws (600ms); node `nothing` reveals (250ms) | t=7.20 both in |
| 8.56 | `window,` | annotation `change: window` (under the chain) | t=8.80 |
| 9.46 | `filter,` | annotation `change: +filter` | t=9.70 |
| 10.08 | `run` | arrow draws; node `re-run` types in | t=10.50 |
| 11.46 | `something` | second arrow draws; second node `nothing` reveals (the next loss) | t=11.90 |
| 11.78 | `else.` | annotation `change: else` | t=12.00 |
| 13.16 | `variation` | final node `re-run` types in + `…` after it (the loop continues) | t=13.50 loop complete |
| 16.42 | `ledger` | annotation: `nobody keeps a ledger` | t=16.60 |
| 19.66 | `which` | `?` (mono, `--paper-dim`) after the `…` | t=19.80 |
| 21.96 | `Three` | loop fades to 40% + settles up; three identical run lines reveal (200ms, 150ms stagger) | t=22.30 |
| 23.94 | `survivor` | `survivor` tag on `run 2` (the middle line) | t=24.20 |
| 25.34 | `label` | annotation: `no label for which is real` | t=25.60 |
| 26.58 | (speech ends) | final hold — nothing moves | t=27.0 = final state |
| 27.86 | — | hard cut to scene-03 | t=27.85 stable |

Every cue keys to a word actually spoken in beat-02 — "nothing" itself is
never narrated; the `nothing` nodes key to `loses` / `something`. 15 state
changes over ~23.8s continuous speech (≥3 per 10s span, verified by check) ✓.
No pre-naming: every element lands on or within its naming word ✓. Survivor
tag on the middle line is a fixed authoring choice (not data).

## Continuity

- First frame: blank ink (matches scene-01's cold-open register; hard cut).
- Last frame: loop dimmed + three identical lines + survivor tag + annotation.
- Transition in: hard cut from scene-01.
- Transition out: hard cut to scene-03.
- Carryover frames: none.

## QA Checklist

- Final-frame proof: **t=27.0** — dim loop, three identical run lines,
  `survivor` on run 2, `no label for which is real` below.
- Boundary proofs: t=13.50 (loop complete with `…`), t=22.30 (final state
  settled), t=27.85 (hold stable to cut).
- Caption proof: run lines + annotations clear the bottom 132px band.
- Audio sync: first `nothing` in by end of "loses" (7.08); `re-run` + `…`
  in by end of "variation" (13.78); three lines settled by end of "runs,"
  (22.94).
- Known risk: bar glyphs (`▮`) — verify JetBrains Mono renders them; fallback
  is `█` (U+2588) or a CSS-drawn rect. Check in the probe render before full
  build. Also: chain width at 30px mono — verify 5 nodes + arrows fit within
  the 80px safe margins; if tight, drop node font to `--fs-anno` (22px).
- Acceptance: lint 0 errors; final-frame proof matches layout; no non-token
  color (`scan_theme_colors.py`).
