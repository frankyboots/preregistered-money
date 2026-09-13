# Scene spec 03 — preregistration fields (the fix)

Status: SPEC (Phase B). Template: `meta:prereg-fields`.

## Scene Identity

- Scene ID: `scene-03`
- Working title: prereg-fields
- Window: **27.86–61.43s** (beat-03, `audio/timing/beat-map.json`; speech 27.94–60.14, hold 60.14–61.43)
- Output format: 1920×1080, 24fps, draft quality (Phase C)
- Source composition: `composition/scene-03.html`
- Render output: `renders/scene-03.mp4`

## User Intent

- Objective: preregistration as the fix — before the run, three things are
  written down and sealed: the hypothesis, the data, the bar.
- Tone: procedural, calm. The commitment is the point.
- Must communicate: order — sealed *before* anything runs — and append-only
  after the commit.
- Must not feel like: a form wizard, a tutorial UI, SaaS onboarding.

## Inputs

- Narration: beat-03, `narration.md` (71 words).
- Cue source: `audio/timing/words.json` (master sha256 `4cfb0cb0…`).
- Data inputs:
  - Seal date `2026-09-12` — commit date of the SHA in `data/spec-sha.txt`
    (`git log -1 --format=%cs 86140f9…`); the only number in the scene, in
    mono, inside the `SEALED:` tags.
- No result values. No run line is drawn — nothing has run yet.
- Corner bug: standard, fades in at scene open (200ms).

## Visual Direction

- Background: `--ink`.
- Three stacked field rows, center-left (max width ~1100px, top-aligned below
  the title zone): each row = label (mono `--fs-body`, `--paper`, typed in) +
  value (mono `--fs-body`, `--paper`) + a small `SEALED: 2026-09-12` tag
  (mono `--fs-anno`, `--paper-dim`) on the row's right.
  - `hypothesis:` — value `one falsifiable sentence` (value types in with the
    narration)
  - `data:` — value blank: a dim `·` placeholder (the dataset is named, never
    its contents — nothing to show)
  - `the bar:` — value `a number to clear, after costs`
- Title zone (top-left under the bug): `preregistration` (Inter 600,
  `--fs-title`, `--paper`); above it a small annotation `the fix — borrowed
  from clinical trials` (mono `--fs-anno`, `--paper-dim`).
- Case follows the narration: `Git` (proper noun) vs `git` (the tool/command
  line in scene-05).
- Bottom band (above the caption zone): two lines reveal as the narration says
  them: `→ git` / `the commit is the seal · git is the notary`
  (mono `--fs-anno`, `--paper-dim`), then the tagline
  `the commitment is the point` (Inter 400, `--fs-body`, `--paper`).
- The `SEALED:` tags use a 200ms fade + 12px slide (reveal verb), not the
  stamp verb — the stamp verb is reserved for the seal scene (scene-05).
- Empty field frames: before their words, the three rows exist as faint
  outlines (stroke `--paper-dim`, 40% opacity) — "three things" is visible
  structure, not yet data. Rows fill on their words.
- Colors: `--paper` + `--paper-dim` only. No amber, no verdict colors.
- Motion: reveal (250ms) for rows/annotations/tagline; typing (mono, ~90ms/char)
  for labels/values; fade (200ms) for the SEALED tags. Nothing after the last word.

## Beat Timeline

Times are word starts from `words.json`.

| Time | Word | Visual action | Required proof |
|---|---|---|---|
| 27.86 | — | open: ink, corner bug fades in; three empty field frames visible (faint outlines) | first frame |
| 28.78 | `from` | annotation `the fix — borrowed from clinical trials` reveals | t=28.90 |
| 30.52 | `preregistration.` | title `preregistration` reveals | t=30.70 |
| 34.58 | `three` | the three empty frames brighten (outline 40% → 70%) — "three things" named | t=34.80 |
| 36.12 | `hypothesis` | row 1 label `hypothesis:` types in | t=36.60 |
| 37.68 | `falsifiable` | row 1 value `one falsifiable sentence` types in (lands ~38.4) | t=38.30 |
| 38.38 | (row 1 complete) | row 1 `SEALED: 2026-09-12` tag fades in | t=38.60 |
| 39.68 | `data,` | row 2 label `data:` types in; value: dim `·` placeholder | t=39.90 |
| 40.84 | (row 2 complete) | row 2 `SEALED: 2026-09-12` tag fades in | t=40.90 |
| 41.14 | `bar,` | row 3 label `the bar:` types in | t=41.40 |
| 41.90 | `number` | row 3 value `a number to clear, after costs` types in (lands ~43.2) | t=42.80 |
| 43.20 | (row 3 complete) | row 3 `SEALED: 2026-09-12` tag fades in | t=43.50 |
| 44.68 | `document` | bottom line 1: `→ Git` reveals | t=44.90 |
| 46.72 | `commit` | bottom line 2: `the commit is the seal · Git is the notary` reveals | t=47.00 |
| 52.46 | `append` | tag `append-only` (mono, `--paper-dim`, boxed) reveals under the rows | t=52.70 |
| 54.55 | `diff` | annotation `anyone can diff it against the run config` reveals | t=54.80 |
| 58.52 | `commitment` | tagline `the commitment is the point` reveals (body, `--paper`) | t=58.80 |
| 60.14 | (speech ends) | final hold — nothing moves | t=60.80 = final state |
| 61.43 | — | hard cut to scene-04 | t=61.42 stable |

Change floor: ~32.2s continuous speech, 16 state changes (≥3 per 10s
span, verified by check) ✓. No pre-naming ✓ (empty frames are structure, not
data). No run line anywhere in the scene — the "before anything runs" order
is carried by the SEALED tags + the hold.

## Continuity

- First frame: ink + bug + three faint field frames (cold structure; the
  outlines are frame, not data — allowed to pre-exist per §5.1 rule 2).
- Last frame: all three rows sealed + git/notary lines + append-only + tagline.
- Transition in: hard cut from scene-02 (final-state jump: loop → fields).
- Transition out: hard cut to scene-04 (the lifecycle diagram is the same
  three things, generalized).
- Carryover frames: none.

## QA Checklist

- Final-frame proof: **t=60.80** — three sealed rows, bottom lines, tagline.
- Boundary proofs: t=38.60 (row 1 sealed), t=43.50 (row 3 sealed), t=47.00
  (notary line), t=61.42 (hold stable to cut).
- Caption proof: `append-only` tag + tagline + bottom lines clear the bottom
  132px band (tagline sits ≥140px above frame bottom).
- Audio sync: `hypothesis:` visible by end of "hypothesis" (37.14); row 3
  value settled by end of "costs." (43.69).
- Known risk: typing cadence vs word duration — value "a number to clear,
  after costs" must land by 43.20 (19 chars + label; keep ≤90ms/char, verify
  in probe). `SEALED:` tag width at 22px mono — check it doesn't collide with
  the value column on row 3 (longest value).
- Acceptance: lint 0 errors; final-frame proof matches layout; date matches
  `data/spec-sha.txt` commit date; no non-token color (`scan_theme_colors.py`).
