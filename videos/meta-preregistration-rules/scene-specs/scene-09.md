# Scene spec 09 — outro

Status: SPEC (Phase B). Template: `meta:outro` (last scene of the video;
window ends at `master_duration_s`).

## Scene Identity

- Scene ID: `scene-09`
- Working title: outro
- Window: **235.60–246.96s** (beat-09, `audio/timing/beat-map.json`;
  speech 235.72–246.86, hold 246.86–246.96 — the master tail)
- Output format: 1920×1080, 24fps, draft quality (Phase C)
- Source composition: `composition/scene-09.html`
- Render output: `renders/scene-09.mp4`

## User Intent

- Objective: close the loop from the cold open — the channel's promise
  about itself: the video pipeline is held to the same reproducibility bar
  as the research.
- Tone: declarative, calm, closing. The narration ends on "…it is a bug."
  — let it land flat, no emphasis.
- Must communicate: "same inputs, same pixels" as the brand's determinism
  claim, and that the pipeline answers to the same bar as the research
  (VIDEO_CONCEPT §1/§7).
- Must not feel like: an end-card, a credits roll, a call to action, or
  motion graphics. This is the cold open's mirror, not a logo sting.

## Inputs

- Narration: beat-09, `narration.md` (30 words).
- Cue source: `audio/timing/words.json` (master sha256 `4cfb0cb0…`,
  246.96s).
- Brand mark: `style/brand-mark.svg` (committed snapshot; inline-embed,
  never `<img>` for SVG — same rule as scene-01).
- Data inputs: **none. No number appears in this scene.** No digits at
  all — the closing sentence's "bug" is a word, not a figure.
- Corner bug: standard, fades in at scene open (200ms).

## Visual Direction

- Background: `--ink`, full frame.
- Layout: one centered vertical stack, dead-center on x=960, echoing the
  cold open (scene-01: mark + wordmark + line) — the outro mirrors it with
  two lines instead of one:
  1. **Brand mark** — 160px, y 200–360 (the pinned mark, §4.2: paper
     strokes + one `--seal-amber` bar).
  2. **Wordmark** `PREREGISTERED MONEY` — Inter 600 `--fs-title` (52px),
     `--paper`, baseline y≈430.
  3. **Headline** `Same inputs, same pixels.` — Inter 400 `--fs-body`
     (30px), `--paper`, y≈510.
  4. **Determinism line** `The video pipeline is held to the same
     reproducibility bar as the research.` — Inter 400 `--fs-body` (30px),
     `--paper-dim` (supporting text, one step down the hierarchy),
     y≈575.
  Stack bottom ≈ y 590 — nothing in the bottom 132px caption band
  (from y=948).
- Colors: `--paper` (mark strokes, wordmark, headline) + `--paper-dim`
  (determinism line) + the mark's pinned `--seal-amber` bar only. No
  verdict colors, no accent — nothing is judged in an outro. P&L rule
  untouched.
- Typography: Inter only (prose scene — no data, so no JetBrains Mono
  needed; the mono rule governs numbers, and there are none).
- Motion: reveal (250ms opacity + 12px slide-up, `power2.out`) for the
  identity unit, the headline, and the determinism line; the standard 200ms
  corner-bug fade at open. No draw, no roll, **no stamp** — the stamp verb
  is reserved for the seal scene (§5.2). No scale, no rotation, no ambient
  motion.
- Open state: at window start the frame is ink + corner bug only — the
  identity unit reveals on the first word ("Same"), so nothing
  pre-exists.

## Beat Timeline

Times are word starts from `words.json`; visual completes within ≤250ms
unless noted.

| Time | Word (narration, words.json) | Visual action | Required proof |
|---|---|---|---|
| 235.60 | — | open: ink, corner bug fades in (200ms); no scene elements | first frame |
| 235.72 | `Same` | brand mark + wordmark reveal as one unit (250ms; lands t=235.97, 7ms after word end, noted) | t=235.97 identity settled |
| 235.94 | `inputs,` | headline `Same inputs, same pixels.` reveals (250ms) | t=236.19 |
| 239.10 | `pipeline` | determinism line `The video pipeline is held to the same reproducibility bar as the research.` reveals (250ms) | t=239.35 |
| 246.86 | (speech ends) | final hold — stack settled, nothing moves (earned hold, §5.1 rule 5); the video ends 100ms later | t=246.90 = final state |
| 246.96 | — | end of video (`master_duration_s`); no scene 10 | t=246.95 stable |

Cue-keying notes: the identity unit (mark + wordmark) keys to `Same`, the
scene's first word — the channel is never named in this beat, so the
identity element goes in with the first word as the frame-level element
(§5.1 rule 2; same reading as scene-08's border). The headline keys to
`inputs,` — the headline's first content word: its naming clause is the
whole sentence ("Same inputs, same pixels.", 235.72–237.58) and the reveal
completes inside it; `pixels.` (237.08) completes the clause but renames
nothing new, so it carries no cue. The determinism line keys to `pipeline`,
the head noun of its subject ("The video pipeline…"); the line's remaining
words (`held`, `bar`, `research.`) rename nothing new. The closing
sentence ("If you cannot reproduce a number from this repository, it is a
bug.") is uncued narration over the settled stack — it names no on-screen
element, exactly as scene-08's clause tails carried no cues; the beat
sheet's on-screen content is the headline, the wordmark, the bug, and the
determinism line, and the spec adds nothing to it. Beat-sheet note: the
beat sheet writes the headline as "Same inputs → same pixels." — the arrow
is notation for the pair; on-screen text follows the narration verbatim
(comma, sentence case), per the narration-is-ground-truth rule. No spec.md
fix needed.

Change floor: 11.14s continuous speech (235.72–246.86, gaps 0.99s and
1.03s — none >3s), 3 state changes (235.72, 235.94, 239.10) — every 10s
span fully inside the speech holds ≥1 (the only such span is
235.72–245.72, which holds all 3) ✓. No pre-naming ✓ (empty open; identity
unit on the first word; headline and determinism line on their naming
words; nothing fully visible before its cue).

## Continuity

- First frame: ink + corner bug only (hard cut from scene-08's final
  frame: the full pinned disclaimer card → empty outro stack — the rules
  are stated; the channel signs off).
- Last frame: the settled outro stack — mark, wordmark, headline,
  determinism line. Natural thumbnail source (style spec §8: composition
  frame + pinned overlay); thumbnail composition is a separate task.
- Transition in: hard cut from scene-08.
- Transition out: none — end of video at `master_duration_s` (246.96).
- Carryover frames: none.

## QA Checklist

- Final-frame proof: **t=246.90** — full stack settled (mark + wordmark +
  headline + determinism line); nothing moves. (The master tail is only
  100ms — the proof frame must land at or before the video's end.)
- Boundary proofs: t=235.97 (identity settled), t=236.19 (headline),
  t=239.35 (determinism line), t=246.95 (stable to the end).
- Caption proof: lowest element is the determinism line (y≈575,
  descender ≈584); the bottom 132px band (from y=948) is empty.
- Audio sync: headline fully visible by end of "inputs," (236.38);
  determinism line by end of "pipeline" (239.58). Identity unit lands
  235.97, 7ms after end of "Same" (235.90) — noted, frame-level element.
- Known risks: (1) Wordmark width at 52px — verify "PREREGISTERED MONEY"
  fits the 80px safe margins (carried from scene-01; if tight, tighter
  tracking, not a smaller size). (2) Determinism line width — 73 chars at
  Inter 400 30px ≈ 1100px, fits the 1760px safe width; verify in probe
  render. (3) The brand mark carries one `--seal-amber` stroke (pinned
  mark pixels, §4.2) — `scan_theme_colors.py` must show tokens
  `--paper` + `--paper-dim` + `--seal-amber` only: no verdict colors, no
  other amber usage anywhere in the scene. (4) Verbatim text: headline and
  determinism line must be byte-identical to their sentences in
  `narration.md` beat-09 (diff at build; punctuation is part of the text).
- Acceptance: lint 0 errors; final-frame proof matches layout; only
  token colors in source (`scan_theme_colors.py` clean); no number in the
  scene; mark inline-embedded (no `<img>`); no motion verb outside
  reveal + the open/close fade (§5.2).
