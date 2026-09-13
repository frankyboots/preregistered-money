---
name: scene-spec-and-commit
description: "Use when writing one scene spec (Phase B loop)."
version: 1.0.0
author: Preregistered Money
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [video, scene-spec, phase-b, cue-table, words-json, commit]
    editorial_name: Scene Spec And Commit
    editorial_description: "The Phase B loop: one scene spec at a time — window from the beat map, cue rows verified against words.json, change floor checked, committed before the next scene starts."
---

# Scene Spec And Commit

One scene of Phase B, then commit, then the next. The loop is spec 04 → commit → spec 05 → commit. Never batch multiple scene specs into one commit; never start scene N+1's spec while scene N is uncommitted. Phase C consumes these specs as build contracts (one scene build per commit; skill pending). (Provenance: scenes 01–03 of `meta-preregistration-rules`, 2026-09; the format reference is `scene-specs/scene-02.md`.)

## Prerequisites (all committed)

- `spec.md` — beat sheet + number citations (the gate; `video-intake-and-storyboard`)
- `audio/timing/beat-map.json` + `words.json` (master sha256, recorded in the spec)
- `scene-specs/README.md` + the previous scene spec as the format reference
- `videos/pipeline/templates/scene-spec.md`

## Step 1 — Window

`beats[i].start_s` → `beats[i+1].start_s` from beat-map.json (last scene: `master_duration_s`). Record in Scene Identity: window, speech range, hold range. All scene windows must sum exactly to the master duration.

## Step 2 — Cue table (Beat Timeline)

Rows: `| Time | Word (narration, words.json) | Visual action | Required proof |`.

- Time = the word's *start* from words.json; the visual completes within ≤250ms unless noted.
- **Every cue keys to a word actually spoken in that beat** — verify each cited word against words.json. On-screen labels the narration never says key to the narration's nearest naming word (e.g. a `nothing` node → `loses` / `something`), never to the label text. A cited word that is not in words.json is a spec error, not a rendering hint.
- **Speech end = the last word's `end`, not its start.** The final hold begins there; stillness only after the last word (earned hold, style spec §5.1).
- **No pre-naming:** no element fully visible >2s before its cue.
- First row = window start: what is on screen at 0.0s (open state, corner bug fade).
- Last rows: hold proof + hard cut to the next scene.

## Step 3 — Change floor

Every 10s span fully inside continuous speech (gaps >3s split it) needs ≥1 cue; the floor binds within the scene's own speech (a scene window can be shorter than a span). Verify by computation and record the count in the spec ("N state changes over Xs continuous speech ✓").

## Step 4 — Sections

Fill the template:

- **Scene Identity** — ID, working title, window (step 1), template block from the beat sheet, source composition path, render output path.
- **User Intent** — objective, tone, must communicate, must not feel like.
- **Inputs** — narration beat + word count; cue source `words.json` + master sha256; data inputs with source + checksum — or explicitly "none. No number appears in this scene."; corner bug.
- **Visual Direction** — background token; states; colors from style-spec tokens only (no verdict colors where nothing is judged — P&L never red/green); typography; motion verbs from style spec §5.2 only.
- **Beat Timeline** — steps 2–3.
- **Continuity** — first frame vs. the previous scene's final frame (scene 01: cold-open register); last frame; transitions in/out; carryover frames to update.
- **QA Checklist** — final-frame proof timestamp; boundary proofs; caption clearance (bottom 132px band); audio-sync proofs (key element in by the end of its naming word); known risks (glyph/font fallbacks, width fits); acceptance (lint 0 errors, final-frame proof matches layout, `scan_theme_colors.py` clean).

Numbers: every on-screen number is already in `spec.md`'s citation table; the spec points to it and never invents a value. Placeholders per `video-intake-and-storyboard` (`PR-0000-000`-style IDs, `example` labels, documented exception).

## Step 5 — Commit (one scene = one commit)

```
video(video-<slug>): scene spec NN (<name>)
```

Body: window + verification evidence (cue rows verified against words.json, change floor verified, citations / no on-screen numbers). **No build-log entry** — no render yet; build-log updates start in Phase C.

Tracker update rides with the commit (scenes done, next scene number).

## Stop conditions

- A cited word is not in words.json → re-key it to a word actually spoken; do not render around it.
- Windows do not sum to the master duration → re-derive from beat-map.json; do not round.
- An on-screen number with no citation in `spec.md` → stop; it needs a results doc or the placeholder rule.
- The scene depends on a previous scene's final frame that is not yet spec'd → spec that dependency first.
