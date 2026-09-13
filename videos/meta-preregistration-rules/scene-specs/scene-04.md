# Scene spec 04 — the lifecycle diagram

Status: SPEC (Phase B). Template: `meta:life-cycle`.

## Scene Identity

- Scene ID: `scene-04`
- Working title: life-cycle
- Window: **61.43–95.24s** (beat-04, `audio/timing/beat-map.json`; speech 61.50–93.94, hold 93.94–95.24)
- Output format: 1920×1080, 24fps, draft quality (Phase C)
- Source composition: `composition/scene-04.html`
- Render output: `renders/scene-04.mp4`

## User Intent

- Objective: the method as a loop — four states, PREREG → SEAL → VERDICT →
  SCOREBOARD, with a return arrow: the post-mortem becomes the next prereg.
- Tone: calm, structural. The loop stated once.
- Must communicate: order (prereg is always first), the three verdict
  outcomes named in their colors, and that the loop closes (SCOREBOARD feeds
  back into PREREG). Every video on the channel lives inside this diagram.
- Must not feel like: a flowchart template, a process-org-chart, a SaaS
  onboarding diagram.

## Inputs

- Narration: beat-04, `narration.md` (70 words).
- Cue source: `audio/timing/words.json` (master sha256 `4cfb0cb0…`).
- Data inputs: none. No number appears in this scene.
- Corner bug: standard, fades in at scene open (200ms).

## Visual Direction

- Background: `--ink`.
- Diagram register (style spec §7, Meta): method as connected nodes, the
  lifecycle as a literal timeline. Four node boxes on one horizontal
  baseline, left→right: `PREREG`, `SEAL`, `VERDICT`, `SCOREBOARD`.
  - Node box: 240×72px, 1px `--paper` stroke, no fill; label JetBrains Mono
    500, `--fs-body`, `--paper`, letterspaced, centered in the box.
  - Baseline: 1px `--paper-dim` rule at the box bottoms (the nodes sit
    on the timeline), pre-existing at scene open (frame, per §5.1 rule
    2). (Amended from "40% through the node centers" at build: a rule
    40% down the box height cuts through the vertically centered labels
    — a strikethrough, measured in the first render; the rule-at-bottoms
    reading is the spec's intent, same amendment class as the
    measured-curve cells.)
  - Inter-node connectors: 1px `--paper` rules along the baseline, drawn
    left→right (draw verb, 700ms).
- Node sub-lines (below each box, JetBrains Mono `--fs-anno`, `--paper-dim`):
  - PREREG: `hypothesis · data · bar` (the same three things as scene-03,
    generalized) + second line `written before anything runs`
  - SEAL: `the commit`
  - VERDICT: three stacked lines, one per word of the narration, each in
    its verdict token (the only colored elements in the scene):
    `confirmed` `--confirmed` / `falsified` `--falsified` /
    `inconclusive` `--inconclusive`
  - SCOREBOARD: `every prereg in one public table`
- Return arrow: 1px `--paper-dim` path from SCOREBOARD's bottom edge, down,
  left along a second rail below all sub-lines, up into PREREG's bottom
  edge; arrowhead at the PREREG end. Drawn left-arriving (draw verb, 900ms,
  right→left) on its word. Below it, centered: annotation
  `postmortem → next prereg` (mono `--fs-anno`, `--paper-dim`).
- Title zone (top-left under the bug): `the lifecycle` (Inter 600,
  `--fs-title`, `--paper`) — the diagram's identity, keyed to the word that
  names it, `states,`.
- Tagline (bottom, above the caption zone): `every video on this channel
  lives inside this diagram` (Inter 400, `--fs-body`, `--paper`), revealed
  on `Every`.
- Colors: `--paper` + `--paper-dim` everywhere except the three verdict
  words (verdict tokens, style spec §2). No amber — Meta runs neutral
  (style spec §7); the bar line (scene-06) is the first amber in this video.
- Motion: reveal (250ms) for title, labels, sub-lines, branches, annotation,
  tagline; draw (600–900ms, §5.2) for connectors and the return arrow only.
  Nothing after the last word.
- Only the baseline rule pre-exists at scene open (frame, not data, §5.1
  rule 2). The four node boxes appear on their words — no pre-naming.

## Beat Timeline

Times are word starts from `words.json`.

| Time | Word | Visual action | Required proof |
|---|---|---|---|
| 61.43 | — | open: ink, corner bug fades in; baseline rule (frame) visible, no nodes | first frame |
| 61.84 | `states,` | title `the lifecycle` reveals | t=62.10 |
| 63.04 | `prereg,` | node 1 `PREREG` box + label reveal | t=63.30 |
| 63.90 | `hypothesis,` | PREREG sub-line 1 `hypothesis · data · bar` reveals | t=64.20 |
| 66.28 | `written` | PREREG sub-line 2 `written before anything runs` reveals | t=66.60 |
| 68.98 | `seal,` | connector 1→2 draws (700ms, noted); node 2 `SEAL` box + label reveals on the word | t=69.40 (node fully visible ≤250ms after word start) |
| 70.04 | `commit` | SEAL sub-line `the commit` reveals | t=70.30 |
| 72.64 | `verdict,` | connector 2→3 draws (700ms, noted); node 3 `VERDICT` box + label reveals on the word | t=73.10 |
| 74.60 | `judged` | VERDICT sub-line `judged by the pre-registered criteria` reveals | t=75.00 |
| 78.84 | `Confirmed,` | branch `confirmed` (`--confirmed`) reveals | t=79.04 |
| 79.68 | `falsified,` | branch `falsified` (`--falsified`) reveals | t=79.88 |
| 80.78 | `inconclusive.` | branch `inconclusive` (`--inconclusive`) reveals | t=80.98 |
| 82.78 | `scoreboard,` | connector 3→4 draws (700ms, noted); node 4 `SCOREBOARD` box + label reveals on the word | t=83.20 |
| 83.90 | `every` | SCOREBOARD sub-line `every prereg in one public table` reveals | t=84.30 |
| 86.46 | `an` | return arrow draws (900ms, noted — draw verb §5.2), SCOREBOARD→PREREG along the lower rail | t=87.40 (draw completes 87.36) |
| 88.44 | `postmortem` | annotation `postmortem → next prereg` reveals under the arrow | t=88.70 |
| 91.14 | `Every` | tagline `every video on this channel lives inside this diagram` reveals | t=91.50 |
| 93.94 | (speech ends) | final hold — nothing moves | t=94.60 = final state |
| 95.24 | — | hard cut to scene-05 | t=95.23 stable |

Cue-keying notes: `an` (86.46) is the narration's naming word for the arrow
("and an arrow back to the prereg"); `postmortem` is as transcribed in
words.json (narration.md writes `post-mortem`). Title `the lifecycle` is an
on-screen identity label the narration never says, keyed to its nearest
naming word `states,`.

Change floor: 32.4s continuous speech (61.50–93.94, no gap >3s), 16 state
changes — per 10s span: 6 (61.5–71.5), 5 (71.5–81.5), 5 (81.5–91.5) ✓.
No pre-naming ✓ (boxes on their words; only the baseline frame pre-exists).

## Continuity

- First frame: ink + bug + baseline rule only (hard cut from scene-03's
  final frame: fields + tagline → empty timeline frame).
- Last frame: complete loop — four nodes with sub-lines, three colored
  branches under VERDICT, return arrow + postmortem annotation, tagline.
- Transition in: hard cut from scene-03 (the lifecycle diagram is the same
  three things, generalized — the cut carries that).
- Transition out: hard cut to scene-05 (seal; its spec opens from ink).
- Carryover frames: none.

## QA Checklist

- Final-frame proof: **t=94.60** — full diagram, arrow, tagline, settled.
- Boundary proofs: t=69.40 (SEAL node in by end of "seal,"), t=80.98 (all
  three branches in their colors), t=83.20 (SCOREBOARD node in by end of
  "scoreboard,"), t=87.40 (return arrow complete), t=95.23 (hold stable to
  cut).
- Caption proof: lowest elements (return-arrow rail, annotation, tagline)
  all clear the bottom 132px band — tagline baseline ≥140px above frame
  bottom.
- Audio sync: `PREREG` label visible by end of "prereg," (63.52); each
  branch word visible within its word (confirmed by 79.04, falsified by
  79.88, inconclusive by 80.98); tagline settled by end of "diagram."
  (93.94).
- Known risks: VERDICT branch stack height (3 × anno lines + `judged…`
  sub-line) vs the lower rail — keep rail ≥40px below the `inconclusive`
  line; `inconclusive` at 22px mono is the widest branch word — check node
  box width fit; connector-draw vs node-reveal overlap on `seal,`/
  `verdict,`/`scoreboard,` (both on the same word — verify in probe the
  node lands before the connector finishes).
- Acceptance: lint 0 errors; final-frame proof matches layout; the only
  non-neutral colors in the scene are the three verdict tokens
  (`scan_theme_colors.py` clean against §2 + verdict set); no number on
  screen.
