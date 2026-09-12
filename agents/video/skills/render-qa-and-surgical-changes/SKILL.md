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

Adapted from https://github.com/saranambiar/hyperframes-video-agent-skills (Apache-2.0, community project — not an official HyperFrames or HeyGen repository). Product-footage checks removed (faceless channel); determinism check added per VIDEO_CONCEPT §9.
