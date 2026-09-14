---
name: render-qa-and-surgical-changes
description: "Use for final render QA or a tiny approved-video edit."
version: 1.0.0
author: Preregistered Money
license: Apache-2.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [video, qa, render, proof-frames, surgical-edit, regression]
    editorial_name: Render QA And Surgical Changes
    editorial_description: "Verifies final renders (probe, proof frames, contact sheet, stale-theme scan) and makes the smallest safe edits to approved videos without breaking sync."
---

# Render QA And Surgical Changes

Use this skill when the video is nearly done or already approved and changes must be controlled.

## Surgical Edit Rules

- Patch source artifacts, not the final MP4, when source scenes and assembly scripts exist.
- Re-render only affected scene(s).
- Rebuild the final assembly from the current approved timeline.
- Do not redesign, retime, or re-sync unrelated sections.
- Search for duplicated/carryover frames before declaring done.
- Extract proof frames at exact timestamps requested by the user.
- If the change alters shown content, the spec needs an amendment entry (append-only, with justification) and the build log a note — same commit (VIDEO_CONCEPT §4.1).

Use `videos/pipeline/templates/change-request.md` before implementing a final tiny change. `references/surgical-final-edit.md` is the step-by-step workflow; `references/failure-modes.md` lists the regressions to check.

## Owner-Nit Fixes

Owner review of a committed scene render flags a visual nit. Two classes by *where the element lives*:

- **Scene-local element** → patch the scene composition only; one video-scoped commit; no style-spec change (precedent: scene-03/04/05 fixes).
- **Pinned set piece** (style spec §4.6 — `.disclaimer-card`, corner bug, brand mark, any §4.6-named element) → the fix MUST go into the pin. A scene-local CSS override of a pinned pixel is forbidden by the scene spec: this video's card would no longer be pixel-identical to future videos. Any pixel change to a set piece is a **major version bump + owner decision** (style spec §4/§10); the owner's fix request IS the decision — name it in the changelog and build-log entry.

Pinned-set-piece fix flow (2 commits, in order):

1. **Probe first, when the fix is font- or geometry-dependent.** Throwaway `_probe-` composition (never committed, deleted before either commit) carrying the candidate value(s) plus a wrong control (e.g. 2ch vs 3ch), rendered draft; measure the settled frame with PIL (same recipes as `scene-build-and-commit` Step 5). Confirm: the fix lands exactly where intended, and line-1 geometry is byte-identical — the probe is the reflow proof. Prefer a font-anchored value (`2ch`) over a measured px: it self-documents (the marker is 2 chars) and is verified pixel-identical to the px in this engine.
2. **Commit 1 — the pin** (`fix`/`style` scope on the pipeline side): edit `videos/pipeline/style/setpieces.css` (source of truth), bump its version header AND the `style-spec.md` version + changelog entry + the §4.6 layout line, in ONE commit.
3. **Commit 2 — the video**: refresh the snapshot — `rm -rf <video>/style <video>/fonts && bash videos/pipeline/snapshot_style.sh <video>` (run via `bash`; the script lacks the executable bit; refresh is one-shot delete+re-copy — never hand-edit the snapshot). The snapshot diff is the change (plus the copy-from line when the pipeline SHA moved; verify other snapshot files stayed byte-identical). Amend the scene spec's pinned-element row (append-only, measured values), re-render the affected scene, re-extract the spec-named proof frames, lint + check + theme scan, and save a before/after crop under `snapshots/scene-NN-fix-check/` (snapshots are gitignored — the build-log entry names the crop as evidence). Build-log: a `##### scene-NN fix —` section after the scene's DRAFT section, mirroring the scene-05 format (owner nit, root cause + measurement, fix + sha256 lines, re-proof, before/after crop, no-design-change line).
4. **Verify the reflow invariant on the real render, not just the probe**: the changed property must leave the spec-pinned lines byte-identical (1px yuv420p rounding is acceptable; record the comparison) and change exactly the lines the fix targets — measure the left/right edge set across all affected lines and name both the old and the new set in the build log.

## Proposing a Fix Without Implementing

Owner flags a visual issue on a committed render and asks how it would be solved but does not request the change. Deliver a concrete, visual proposal — not a geometry argument from the spec:

1. **Measure in the rendered frame, not the spec.** The owner decides on pixels, and spec clearance math has been wrong before (a ring chord, a 3px line kiss) — the render is the record of what the owner sees. Extract the settled proof frame from the standalone scene render: identical pixels to the master at the boundary, cheaper to pull.
2. **Confirm the collision AND the clearance with PIL.** Per-zone ink extents (min/max x per line band; thresholds ~140 for `--paper`, ~85 for `--paper-dim` on the current palette) plus column scans at candidate re-route positions — a candidate leg/column with zero ink across the text band is a real gutter. Quote only measured extents in the proposal.
3. **Mock the fix on the proof frame.** Erase the old element with the background color sampled from the frame, draw the proposed geometry in the token color, and vision-verify the mock before presenting it. The owner approves a mock, not prose — a before/after frame is what makes "how would you solve it" answerable.
4. **State the implementation cost explicitly** — which file changes, which re-render scope, which re-proofs the change would force (a re-routed dash-draw path needs its pre-cue frame re-proven against the dasharray leak trap) — and do not implement until the owner approves. The proposal itself commits nothing.

## QA Sequence

1. Probe the final render (`videos/pipeline/tools/probe_media.py`).
   - Duration.
   - Resolution.
   - Frame rate.
   - Audio stream.
   - Sample rate and channels.

2. Extract proof frames (`videos/pipeline/tools/extract_proof_frames.py`).
   - Scene boundaries.
   - Changed timestamps.
   - Caption style frames.
   - Final frame.

3. Build a contact sheet (`videos/pipeline/tools/make_contact_sheet.py`).
   - Include all risky timestamps.
   - Include before/after frames for surgical changes.

4. Check audio.
   - Narration present and not clipped.
   - Final silence or fade timing correct.

5. Check theme and text.
   - Scan for stale colors (`videos/pipeline/tools/scan_theme_colors.py` against the style-spec palette).
   - Search duplicated labels in carryover scenes.
   - Verify user-provided imagery was not recolored accidentally.

6. Determinism check.
   - The committed video dir must re-render to matching pixels; record encoder settings and versions in the build log (VIDEO_CONCEPT §9).

## Acceptance

Report:

- Final video path.
- Probe summary.
- Proof frame/contact sheet paths.
- Files changed.
- Exact checks performed.
- Any unverified subjective item.

## Exact Timestamp Checks

When the user names a timestamp:

- Extract a frame at that exact time.
- Extract one frame slightly before if appearance timing matters.
- Extract one frame slightly after if disappearance timing matters.
- Inspect the rendered final, not only the source scene.
- If the same visual appears in the next scene, extract the boundary frame too.

## Source Search Checklist

Before patching:

- Search all source scene files for the text or color.
- Search assembly scripts for audio paths and durations.
- Search caption files for old wording.
- Ignore generated renders unless doing visual QA.

## Safe Audio Replacement

For replacing the voiceover (a deliberate, logged act):

- Probe old and new durations.
- If same duration, replace the committed wav and rebuild.
- If slightly different, decide whether to tempo-fit or retime visuals.
- Confirm no downstream scene start moves unless requested.
- Regenerate captions from the new wav.
- Record the new wav's checksum, voice/model/settings, and script hash in the build log.

## Safe Text Replacement

For replacing visible text:

- Patch source scene.
- Search next scene for carryover copy.
- Search old captions if spoken wording changed.
- Re-render affected scene.
- Rebuild final.
- Extract proof frames at visible times.

## Safe Theme Replacement

For color cleanup:

- Use the theme scanner.
- Patch editable source only.
- Do not recolor user-provided imagery.
- Check SVG values.
- Check next-scene carryovers.

## QA Output Bundle

Produce:

- Probe summary.
- Proof frames.
- Contact sheet.
- Preview clips for moving sync checks.
- Final render path.

Generated QA files do not need to be committed unless they are public examples.

## Stop Conditions

Stop and ask if:

- The requested change conflicts with locked scene approval.
- The source asset for the visible final frame cannot be found.
- A text/audio change implies a script change the user has not approved.
- The change would alter a number that is not in the cited results doc.

Otherwise make the smallest safe change and verify it.

## Provenance

Adapted from https://github.com/saranambiar/hyperframes-video-agent-skills (Apache-2.0, community project — not an official HyperFrames or HeyGen repository). Product-footage checks removed (faceless channel); determinism check added per VIDEO_CONCEPT §9. Edit this skill freely as the workflow evolves; keep this provenance section.
