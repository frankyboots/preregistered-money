---
name: video-bootstrap
description: "Use when starting a new video (Phase A commit order)."
version: 1.0.0
author: Preregistered Money
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [video, bootstrap, phase-a, commit-order, build-log, audio-lock]
    editorial_name: Video Bootstrap
    editorial_description: "The Phase A loop: takes a video from approved concept to render-ready dir with one commit per milestone — spec gate, optional spec-SHA pin, audio lock (build log created here), scaffold, style wiring."
---

# Video Bootstrap

Phase A of the channel lifecycle: **A bootstrap** → B scene specs (`scene-spec-and-commit`) → C scene builds (`scene-build-and-commit`) → D assembly/final (`audio-sync-assembly`, `captions`, `render-qa-and-surgical-changes`). This skill owns the Phase A commit order. (Provenance: the channel's first video, `meta-preregistration-rules`, ran this loop in 2026-09; the commit order below is that run distilled.)

## Commit invariants

1. **Spec first.** `spec.md` is committed before anything else in the video dir renders (VIDEO_CONCEPT §4.1). Pre-first-render amendments are separate `video` commits; they are free.
2. **One milestone = one commit.** A pipeline bug found mid-step is fixed in a separate `fix`/`feat(pipeline)` commit *before* re-running the step — never bundled into a video-dir commit.
3. **Build log is created at the audio lock**, not at the spec commit: audio is the first artifact that needs an audit record.
4. **Audio before scene specs.** `words.json` + `beat-map.json` must exist before Phase B (scene specs cite the master sha256).
5. **Tracker updates ride with the milestone's commit** (MEMORY.md is committed per `video-commit`).
6. Concurrent-writer gate per `video-commit`: re-run `git status --short` immediately before each commit.

## Step 1 — Spec (the gate)

Per `video-intake-and-storyboard`. Fill the spec from `templates/spec.md` (meta, beat sheet, number citations, inputs with checksums, standing items); every on-screen number cited, or the placeholder rule in effect.

- **Fresh video:** `pipeline/new_video.sh <slug>` (copies the skeleton, auto-snapshots style/fonts, stages the spec template) → fill the spec → commit `spec.md` alone first: `video(video-<slug>): spec v1 — <one line>`. Never `npx hyperframes init`.
- **Pre-existing dir (audio-first):** the spec is already committed — keep it the top of the dir's commit order; `new_video.sh` refuses existing dirs, so step 4 is the manual merge.

## Step 2 — Spec-SHA pin (the channel's first video only)

`data/spec-sha.txt` = the SHA of the commit that **first** committed `spec.md`. Pin it in a follow-up commit **before** the first render; later spec amendments do not re-pin (the file holds the original commit). Checksum the file in the build log. The SHA is a data input for the seal scene — never computed in a composition.

## Step 3 — Narration lock (build log created here)

Draft narration (`humanizer`) → TTS per `elevenlabs-tts` (channel voice pin in the pipeline README — current: Helen narrator, Zane reserved) → word timings per `elevenlabs-transcribe` (scribe_v2, word granularity, keyterms per pin) → owner review loop.

On owner lock, one commit: `narration.md`, beat wavs, master `voiceover.wav`, `words.json`, `beat-map.json`, `captions.srt`, timing summaries, **and the build log created**: artifact checksum table, TTS audit record (voice, model, settings, per-beat request IDs, script hash), STT record (model, word count, transcription ID), iteration history. Message: `video(video-<slug>): locked narration + committed wav`. After this commit the narration is locked — no further trims without an owner act.

## Step 4 — Scaffold

- **Fresh video:** the skeleton + style/fonts snapshot already landed via `new_video.sh`. Verify boot: `pipeline/render.sh <dir> lint` + `check`. Commit the scaffold files: `chore(video-<slug>): merge pipeline skeleton into video dir; lint+check pass` — build log: scaffold file checksums, pipeline HEAD (version of record), HF version.
- **Audio-first dir:** copy `index.html`, `hyperframes.json`, `composition/README.md`, `data/README.md` from `pipeline/skeleton` verbatim; slug `meta.json` + `package.json` id/name; skip the skeleton's `README.md` (it documents the skeleton, not the video). Never overwrite committed files — `git status` must show only new untracked files. Verify boot the same way; same commit type. Build log: scaffold section + checksums + pipeline versions.

## Step 5 — Style + fonts (audio-first path only)

Fresh videos are already snapshotted by `new_video.sh`. Audio-first: `pipeline/snapshot_style.sh <dir>` (one-shot — refuses an existing snapshot; refresh = delete + re-run + build-log note), link `style/tokens.css` + `style/setpieces.css` in `index.html`, verify with a throwaway probe composition (corner bug, hero number, seal amber, SEALED stamp, brand mark) rendered via `render.sh`. Build log: snapshot checksums + pipeline SHA (the snapshot's version of record) + rule-text SHAs (CONCEPT/METHODOLOGY, read-only). Message: `video(video-<slug>): wire style spec <ver> + vendored fonts`.

## Done =

- spec committed, citations complete (or placeholder rule documented)
- audio locked; build log exists with full checksums
- lint + check pass
- style wired (fresh: automatic; audio-first: step 5)
- tracker: next = Phase B, one scene at a time

## Stop conditions

- A number the owner wants is not in a results doc → request a new prereg on the research side; the video never computes it.
- `new_video.sh` refuses or boot fails → fix the pipeline first, as its own commit, then re-run the step.
- Owner lock on narration not reached → no build log, no Phase B.
