---
name: end-to-end-video-playbook
description: "Use when building a full video from prompt to render."
version: 1.0.0
author: Preregistered Money
license: Apache-2.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [video, hyperframes, workflow, production, assembly]
    editorial_name: End-To-End Video Playbook
    editorial_description: "The coordinator skill for full video production: routes each phase to the focused skills, enforces the spec-gates-render gate, and sets the verification bar before a video is called done."
---

# End-To-End Video Playbook

Use this skill to coordinate a complete video project from rough request to verified final render. It sequences the focused skills; it does not replace them.

## Grounding Rules (this repo)

- The video's `spec.md` (in `videos/<slug>/`) gates rendering: it is committed before the first render (VIDEO_CONCEPT §4.1). No committed spec, no render.
- Every figure shown on screen must already be cited in the spec's number-citation table (results doc, or prereg/scoreboard for recaps). Never compute numbers in a composition.
- The build log (`build.log`) is updated at every render and committed with the change it describes.
- Commits follow the `video-commit` skill (boundary, message format, integrity checklist).
- Style, palette, and motion come from the versioned style spec in `videos/pipeline/style/`; the build log pins the version used.
- A video directory is a HyperFrames project by copying the committed pipeline skeleton — never by running `npx hyperframes init` per video (scaffold once into the skeleton; see `hyperframes-scene-builder`, Project & CLI Mechanics). The framework version is pinned in the pipeline render script, not per video.

## Workflow

1. Ground in the current project.
   - Inspect available assets, renders, compositions, committed audio, and any existing spec.
   - Identify locked scenes and user boundaries such as "do not modify Scene 01."
   - **Phase A (new video, no render-ready dir yet): `video-bootstrap` owns the commit order** — spec gate first (fresh: `new_video.sh <slug>` → fill the spec → commit `spec.md` alone before anything else; audio-first pre-existing dir: spec already on top, manual skeleton merge), spec-SHA pin (first video only), audio lock + build-log creation, scaffold verify, style wiring. One commit per milestone; never `npx hyperframes init`; the spec is committed before the first render (CONCEPT §4.1).
   - Use `videos/pipeline/templates/storyboard.md` for multi-scene planning.

2. Convert intent into a spec.
   - Create `videos/<slug>/spec.md` per the layout in VIDEO_CONCEPT §4.1 (meta, beat sheet, number citations, inputs with checksums, standing items).
   - Use `videos/pipeline/templates/scene-spec.md` per scene where the beat sheet needs detail.
   - Separate user-specific content from reusable production patterns.
   - Record exact durations, final-frame requirements, narration, visual beats, transition dependencies, and proof timestamps.

3. Route to focused skills.
   - `video-intake-and-storyboard` for unclear prompts or new scenes.
   - `scene-build-and-commit` for the Phase C loop — one scene built from its spec, draft-rendered, proof-checked, committed, then the next (it owns the build-log + commit; it delegates composition craft to `hyperframes-scene-builder`).
   - `hyperframes-scene-builder` for HTML/GSAP composition work.
   - `audio-sync-assembly` for narration timing, segment retiming, and assembly.
   - `captions` for subtitle timing and wording.
   - `render-qa-and-surgical-changes` for proof frames, exact-timestamp checks, and safe final edits.
   - `channel-art` for the per-video thumbnail (house look + per-video hero).

4. Build in layers.
   - Draft scene renders first.
   - Assemble the narration-only master before anything else.
   - Add captions after the visual/audio timeline is stable.
   - Music: standing decision is none (VIDEO_CONCEPT §7). Do not add a music bed.
   - **Thumbnail last** (`channel-art`, "Thumbnails" section): render the per-video
     thumbnail from the committed house generator after the final MP4 is
     committed, before publish — the upload needs it. Never hand-make per-video
     art.

5. Verify before reporting completion.
   - Probe final outputs with `videos/pipeline/tools/probe_media.py`.
   - Extract proof frames at every risky timestamp and scene boundary with `videos/pipeline/tools/extract_proof_frames.py`.
   - Make a contact sheet for multi-scene QA with `videos/pipeline/tools/make_contact_sheet.py`.
   - State what was verified and what remains subjective.

6. Commit via `video-commit` — spec, composition, and build log as one coherent commit; refused boundary paths aborted.

## Production Rules

- Never patch an old final MP4 when source scenes and assembly scripts exist.
- Do not globally slow a scene if only a pause or one cue needs timing.
- Prefer hold frames for silence and deliberate pacing.
- Re-render only affected scenes during final surgical changes.
- Always check duplicated carryover frames when a previous final frame changes.
- A re-render of the committed directory must reproduce the published pixels; a mismatch is an incident (fix the pipeline, never hand-edit the output).

## Agent Routing Table

- New video (no spec or render-ready dir): start with `video-bootstrap` (Phase A), then `scene-spec-and-commit` per scene (Phase B).
- User gives a rough idea only: start with `video-intake-and-storyboard`.
- User gives a reference final frame: intake first, then `motion-design-systems`, then `hyperframes-scene-builder`.
- User says a scene must start from another scene: use `scene-continuity-and-transitions`.
- User says captions are late or wrong: use `captions`.
- User says narration changed: use `audio-sync-assembly`.
- User says "everything is perfect except": use `render-qa-and-surgical-changes`.
- User wants banner/logo/description or a video thumbnail (new look or per-video): `channel-art` — 3 distinct concepts → owner pick → committed generator.
- Owner ratifies or rejects a "Flagged for REVIEW" reading (style-spec / scene-spec): `scene-spec-and-commit` → "Resolving a flagged reading".

## Implementation Order

Phase map: A bootstrap (`video-bootstrap`) → B scene specs, one scene per commit (`scene-spec-and-commit`) → C scene builds, one scene per commit (`scene-build-and-commit`) → D assembly/final → thumbnail.

1. Lock approved scenes.
2. Phase B: one scene spec + commit at a time (`scene-spec-and-commit`) — never batch.
3. Build or revise scene sources.
4. Render scene drafts.
5. Extract proof frames.
6. Build narration-only assembly.
7. Align captions from the committed voiceover wav.
8. Export final MP4.
9. Generate proof sheet and preview clips.
10. Update build log; commit.
11. Render the per-video thumbnail from the committed generator (`channel-art`);
    verify it reads at list-view size (160 px); commit it with the build log
    before publish.

## Decision Checklist

Before building, decide and record:

- Whether this is a new video, scene addition, or final edit.
- Whether the user approved any existing scenes.
- Whether previous renders are source of truth or just previews.
- Whether the final output needs captions.
- Whether exact phrase timing matters.
- Whether a silent hook, pause, or final hold exists.
- Whether the final render should be 24, 30, 48, 60, or source FPS.
- Whether the user expects proof before full render.

## What To Ask The User

Ask only questions that change implementation:

- Which final frame should match the reference if multiple references exist.
- Whether caption delivery is soft (SRT upload) or burned in.
- Whether a requested edit may change approved timing.
- Whether the spec amendment alters shown content (requires re-render + amendment entry).

Do not ask questions discoverable from files:

- Clip durations, existing scene names, current frame rate, whether an audio stream exists.

## Quality Gate

Do not call a full video done until:

- Final duration is known.
- Final resolution and FPS are known.
- Audio stream exists.
- Captions are present if requested.
- Thumbnail is rendered from the committed generator, reads at 160 px, and is
  committed with the build log.
- Scene boundary proofs exist.
- Exact user-requested timestamp proofs exist.
- Any subjective preview requested by the user was shown or explicitly skipped.
- Build log updated in the same commit as the change it describes.

## Handoff Format

When finishing, report:

- Final render path.
- Important scene/render paths.
- Commands or scripts used.
- Proof frame or preview paths.
- Tests performed.
- Anything not verified.
- The commit made (message + scope) per `video-commit`.

## Provenance

Adapted from https://github.com/saranambiar/hyperframes-video-agent-skills (Apache-2.0, community project — not an official HyperFrames or HeyGen repository). Edit this skill freely as the workflow evolves; keep this provenance section.
