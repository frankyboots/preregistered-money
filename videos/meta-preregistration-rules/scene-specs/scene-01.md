# Scene spec 01 — title card

Status: SPEC (Phase B). Template: `meta:title-card`.

## Scene Identity

- Scene ID: `scene-01`
- Working title: title-card
- Window: **0.00–2.69s** (beat-01, `audio/timing/beat-map.json`; speech 0.08–1.40, hold 1.40–2.69)
- Output format: 1920×1080, 24fps, draft quality (Phase C)
- Source composition: `composition/scene-01.html`
- Render output: `renders/scene-01.mp4`

## User Intent

- Objective: cold open — establish the channel in one sentence.
- Tone: declarative, calm. No hype, no logo-sting energy.
- Must communicate: the channel name and the method, in one line.
- Must not feel like: an intro sequence, a broadcast opener, motion graphics.

## Inputs

- Narration: beat-01, `narration.md` — "The name is the method."
- Cue source: `audio/timing/words.json` (master sha256 `4cfb0cb0…`, 246.96s).
- Brand mark: `style/brand-mark.svg` (committed snapshot; inline-embed, never `<img>` for SVG).
- Data inputs: **none. No number appears in this scene.**
- Corner bug: none — the title card *is* the wordmark (bug starts scene 02).

## Visual Direction

- Background: `--ink`, full frame, nothing else.
- Layout: brand mark centered (≈160px), wordmark below (Inter 600, `--fs-title`),
  one line below (Inter 400, `--fs-body`). Vertical stack, dead center.
- Colors: `--paper` only (wordmark, line, mark strokes). No `--paper-dim` needed.
- Motion: reveal verbs only (`--dur-fade`/`--dur-reveal`, `--ease-out`).
  **No stamp verb** — the stamp is reserved for the seal scene (style spec §5.2).
  No scale, no rotation, no ambient motion.
- Final frame: mark + wordmark + line, all settled, dead center.

## Beat Timeline

| Time | Word (words.json) | Visual action | Required proof |
|---|---|---|---|
| 0.00 | — | scene open: black, 200ms fade-in to `--ink` (sanctioned open); no elements visible | first frame |
| 0.24 | `name` | wordmark + brand mark reveal as one unit (250ms opacity + 12px slide-up) — the mark *is* the name | t=0.30 mid-reveal, not fully visible before 0.24 |
| 0.98 | `method.` | one line "The name is the method." reveals (250ms) | t=1.00 line ≥90% in |
| 1.40 | (speech ends) | final hold — nothing moves until cut | t=2.50 = final state |
| 2.69 | — | hard cut to scene-02 | t=2.68 stable |

Change floor: 1.32s of speech, 2 state changes on cue + the open fade ✓
(scene is 1.44s of speech; the floor is per 10s). No pre-naming: the mark
unit lands on "name", the line on "method." ✓ (narration names no other
element — nothing else is allowed on screen).

## Continuity

- First frame: blank ink (cold open; 200ms fade-in from black allowed — the
  only sanctioned fade open).
- Last frame: settled title card; not reused elsewhere.
- Transition in: none (cold open).
- Transition out: hard cut to scene-02.
- Carryover frames: none.

## QA Checklist

- Final-frame proof: **t=2.50** — mark + wordmark + line, settled, centered.
- Boundary proofs: t=0.30 (wordmark mid-reveal), t=1.00 (mark in, line not yet
  fully in), t=2.68 (hold stable to the cut).
- Caption proof: nothing in the bottom 132px band.
- Audio sync: wordmark fully visible by end of "name" (0.55); line fully
  visible by end of "method." (1.40).
- Known risk: wordmark width at 52px — check fit inside 80px safe margins
  ("PREREGISTERED MONEY" is long; if tight, drop to Inter 600 with tighter
  tracking, not a smaller size below the token).
- Acceptance: lint 0 errors; final-frame proof matches layout above; no
  non-token color in source (`scan_theme_colors.py`).
