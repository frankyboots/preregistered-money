# Scene spec 08 — the disclaimer

Status: SPEC (Phase B). Template: pinned `disclaimer-card` (style spec §4.6).

## Scene Identity

- Scene ID: `scene-08`
- Working title: disclaimer
- Window: **205.47–235.60s** (beat-08, `audio/timing/beat-map.json`; speech 205.56–234.34, hold 234.34–235.60)
- Output format: 1920×1080, 24fps, draft quality (Phase C)
- Source composition: `composition/scene-08.html`
- Render output: `renders/scene-08.mp4`

## User Intent

- Objective: what preregistration does *not* fix — the channel's standing
  disclaimer, the pinned card, delivered as a full segment, not an end-card.
- Tone: flat, procedural, no hedge, no apology. The rules segment of the
  video.
- Must communicate: the four bullets, verbatim, in order, each on its
  narration word; that this card is pinned — same pixels in every video
  (style spec §4.6: "rendered identically in every video").
- Must not feel like: legal fine print, an end-card, a confession, or a
  scene where anything moves for emphasis.

## Inputs

- Narration: beat-08, `narration.md` (57 words).
- Cue source: `audio/timing/words.json` (master sha256 `4cfb0cb0…`).
- Data inputs: **none — no number appears in this scene.** The four bullet
  strings are verbatim `docs/CONCEPT.md` §10 (the source of truth, style
  spec §4.6) and are identical to the four sentences of the committed
  narration — the card is rendered from the doc string, not retyped from
  memory (citation: `spec.md` Number citations row "Disclaimer bullets
  (beat 8)").
- Corner bug: standard, fades in at scene open (200ms).

## Visual Direction

- Background: `--ink`.
- Layout (1920×1080), the pinned card (style spec §4.6, `setpieces.css`
  `.disclaimer-card` — ink field, 1px `--paper-dim` border, 40px padding,
  left-aligned): card x=120–1800 (width 1680), y=180. Content area
  x 160–1760 (width 1600):
  1. **Title** `HONEST LIMITATIONS` (`.dc-title` — mono `--fs-anno`,
     `--paper-dim`, letterspaced `0.12em`; 16 chars ≈ 350px) — content
     x=160, baseline y≈232.
  2. **Four bullets** (`.disclaimer-card ul` — JetBrains Mono `--fs-body`,
     `--paper`, line-height 1.6 = 48px; `li::before` `·  ` marker in
     `--paper-dim`). Bullet line baselines: b1 y≈308; b2 y≈372/420 (wraps
     after `assumptions;`); b3 y≈468/516 (wraps after `choices,`);
     b4 y≈564/612 (wraps after `out-of-sample`). Card bottom y≈652.
     **2.0.0 amendment (2026-09-13):** the pinned card now carries a
     2ch hanging indent (style spec 2.0.0, owner decision — see the
     build-log `scene-08 fix` entry): wrapped lines (b2/b3/b4 line 2)
     start under the bullet's FIRST WORD (x≈240) instead of the ul
     content edge (x≈204). Line-1 word positions and all three wrap
     points are unchanged (probe-verified byte-identical wrap
     right-edges); no y-geometry, cue, or timing change — the spec's
     layout math above stands as-is for line 1 and card bottom.
  3. Card vertical center y≈416 ≈ frame center 540 minus margin — the card
     is top-anchored, not centered, so the bullet column reads downward
     from a comfortable top; nothing else in the scene.
- Colors: `--paper` (bullets) + `--paper-dim` (border, title, markers)
  only. No amber, no verdict colors, no accent — nothing is judged here.
  P&L rule untouched.
- Typography: all pinned — `.dc-title` mono `--fs-anno` letterspaced;
  bullets mono `--fs-body`; no scene-local overrides (pinned pixels).
- Motion: draw (600ms left→right) for the card border only (the frame
  element — frame-level, §5.1 rule 2); reveal (250ms opacity + 12px
  slide-up, `power2.out`) for the title and each bullet. No roll (no hero
  numbers), no stamp. Nothing after the last word.
- Open state: at window start the frame is ink + corner bug only — the card
  border draws on the first narration word ("The same"), so nothing
  pre-exists.

## Beat Timeline

Times are word starts from `words.json`; visual completes within ≤250ms
unless noted.

| Time | Word (narration, words.json) | Visual action | Required proof |
|---|---|---|---|
| 205.47 | — | open: ink, corner bug fades in; no scene elements | first frame |
| 205.56 | `The` | card border draws left→right (600ms; lands t=206.16, 230ms after word end, noted) | t=206.16 border complete |
| 206.20 | `four` | title `HONEST LIMITATIONS` reveals (250ms) | t=206.45 |
| 208.90 | `Educational` | bullet 1 `Educational content, not investment advice.` reveals (250ms, 1 line) | t=209.15 |
| 212.50 | `Backtest` | bullet 2 `Backtest results are estimates under stated assumptions; live performance will differ, possibly badly.` reveals (250ms, 2 lines) | t=212.75 |
| 219.09 | `Preregistration` | bullet 3 `Preregistration controls data snooping; it does not control overfitting in pre-seal choices, data quality, or market regime change.` reveals (250ms, 2 lines) | t=219.34 |
| 227.68 | `Past` | bullet 4 `Past performance (including preregistered, costed, out-of-sample past performance) is the weakest predictor in finance.` reveals (250ms, 2 lines) | t=227.93 |
| 234.34 | (speech ends) | final hold — card settled, nothing moves (earned hold, §5.1 rule 5) | t=234.90 = final state |
| 235.60 | — | hard cut to scene-09 | t=235.59 stable |

Cue-keying notes: the border keys to `The` (the scene's first word — the
naming clause "The same four lines" covers the whole card, so the frame
element goes in with it, frame-level per §5.1 rule 2). The title keys to
`four` ("the same **four** lines" — the title names what the four lines
are). Each bullet keys to its first word, which is the narration's own
verbatim opening of that bullet: `Educational`, `Backtest`,
`Preregistration`, `Past`. No other elements exist in the scene; the
remaining narration words ("on every video", clause tails) rename nothing
new, so they carry no cues. The narration text matches CONCEPT §10
verbatim — no beat-sheet contradiction found (no spec.md fix needed beyond
the §-number correction, noted in the commit body).

Change floor: 28.78s continuous speech (205.56–234.34, no gap >3s), 6 state
changes — per 10s span: 4 (205.5–215.5), 2 (215.5–225.5), 1
(225.5–234.34) ✓. No pre-naming ✓ (empty open; border is the frame element
drawn on the first word; title and every bullet on their naming word).

## Continuity

- First frame: ink + corner bug only (hard cut from scene-07's final frame:
  full ledger → empty disclaimer frame).
- Last frame: the full pinned card — border, `HONEST LIMITATIONS` title,
  all four bullets settled.
- Transition in: hard cut from scene-07 (the product shown → the rules it
  operates under; the cut carries the turn).
- Transition out: hard cut to scene-09 (the outro; its spec opens from ink).
- Carryover frames: none.

## QA Checklist

- Final-frame proof: **t=234.90** — full card settled (border + title +
  four bullets); nothing moves.
- Boundary proofs: t=206.16 (border complete), t=206.45 (title), t=209.15
  (bullet 1), t=212.75 (bullet 2), t=219.34 (bullet 3), t=227.93 (bullet
  4), t=235.59 (hold stable to cut).
- Caption proof: lowest element is bullet 4's second line (baseline y≈612,
  descender ≈621); the bottom 132px band (from y=948) is empty.
- Audio sync: title by end of "four" (206.36); bullet 1 by end of
  "Educational" (209.45); bullet 2 by end of "Backtest" (212.96); bullet 3
  by end of "Preregistration" (219.98); bullet 4 by end of "Past"
  (227.96). Border lands 206.16, 230ms after end of "The" (205.86) — noted.
- Known risks: (1) Bullet wrap points — the pinned card wraps by CSS, not
  by hand: probe must confirm b2 wraps after `assumptions;`, b3 after
  `choices,`, b4 after `out-of-sample`, matching the layout math above
  (JetBrains Mono 30px ≈ 9.3px/char, content width 1600px ≈ 172 chars/line;
  all three longest lines are ≤131 chars, so each wraps exactly as
  specified — verify in probe). (2) Card width 1680px — clears the 1760px
  safe area by 40px each side; verify against the corner bug (bug at x=40,
  card starts x=120 — no overlap). (3) The card must be the ONLY element
  with a `--paper-dim` border in the scene — `scan_theme_colors.py` must
  show no chromatic pixels at all (no amber, no verdict colors). (4)
  Verbatim text: the four bullets must be byte-identical to
  `docs/CONCEPT.md` §10 — diff against the doc at build (em-dash-free text;
  no glyph risk, but punctuation is part of the pin).
- Acceptance: lint 0 errors; final-frame proof matches layout; the pinned
  `.disclaimer-card` set-piece classes (border, 40px padding, `.dc-title`,
  `ul`/`li` styles) are used — no ad-hoc card CSS and no scene-local font
  or color overrides (pinned pixels, style spec §4.6); bullet text
  byte-identical to CONCEPT §10; no number in the scene;
  `scan_theme_colors.py` clean (paper + paper-dim only).
