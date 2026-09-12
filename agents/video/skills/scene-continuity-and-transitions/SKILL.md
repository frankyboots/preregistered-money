---
name: scene-continuity-and-transitions
description: "Use when a scene must start from a prior final frame."
version: 1.0.0
author: Preregistered Money
license: Apache-2.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [video, continuity, transitions, carryover, boundaries]
    editorial_name: Scene Continuity And Transitions
    editorial_description: "Keeps multi-scene videos feeling like one journey: carryover-frame audits, boundary proof frames, camera-move patterns, and the surgical rule when a prior final frame changes."
---

# Scene Continuity And Transitions

Use this skill when scenes must feel like one continuous visual journey instead of separate slides.

## Continuity Contract

Before editing a scene, identify:

- Previous scene final frame.
- Current scene first frame.
- Transition direction.
- Camera movement duration.
- Any duplicated chart/table/card/logo/text in the next scene.
- Any approved scene that must not be modified.

Use `references/carryover-frames.md` for duplicated-frame checks.

## Camera Swipe Pattern

For a rightward camera movement:

- Move the current world left.
- Bring the next world in from the right or land on a clean blank field.
- Keep background color, lighting, and scale continuous.
- Use slight blur or parallax only if it improves realism.
- Avoid fading to a new slide unless the user asks for a cut or fade.

For a downward camera movement:

- Move from the hook/top field into the first current-video frame.
- Keep speed high enough to feel like a transition, not a scene pause.
- Match color and scale at the landing frame.

## First-Frame Matching

When a scene begins from the previous scene:

- Copy or recreate the previous final frame in the new composition.
- Include all latest text, labels, theme colors, plus symbols, highlights, and annotations.
- Re-render both affected scenes if the final frame is source-driven.
- Extract proof frame just before and after the boundary.

## Boundary QA

Always verify:

- No visual pop at the join.
- No stale text from an older render.
- No sudden color shift.
- No missing annotation that was added to the previous scene.
- No unwanted crop or scale change.
- Captions do not cover critical boundary text.

## Surgical Change Rule

If the previous final frame changes, assume the next scene may also need a source patch. Search before declaring done.

## Output

Provide:

- Changed scene files.
- Re-rendered scene list.
- Final assembly path.
- Boundary proof frames.
- Exact timestamps checked.

## Transition Types

Use the transition type that matches the story:

- Camera swipe: same world, different area.
- Camera push: moving deeper into the same object.
- Downward camera move: hook into main video.
- Dot-to-data transition: diagram becomes chart.
- Blank field reset: audience needs a breath before new idea.

Avoid hard cuts when the user says "seamlessly," "same object," "continue," or "camera movement."

## Timing Guidelines

- Fast scene-to-scene swipe: 0.4s to 1.0s.
- Clean reset hold: 0.5s to 1.5s.
- Final hold: fast movement, then still hold.
- Chart-to-question transition: leave clean negative space before cards appear.

These are defaults; narration timing wins when explicit.

## Carryover Audit

Whenever a final frame changes, search:

- Current scene source.
- Next scene source.
- Any old scene HTML with same title text.
- Inline SVG text.
- Axis labels.
- Table headers.
- CTA copy.
- Theme colors.
- Generated snapshots only for QA, not source.

## Boundary Proof Procedure

Extract frames (use `videos/pipeline/tools/extract_proof_frames.py`):

- 0.05s before boundary.
- 0.05s after boundary.
- Middle of transition.
- First settled frame.

If a label appears before the boundary and disappears after, the carryover source is stale.

## Common User Corrections

Map corrections to actions:

- "It jumps" means boundary proof and scale/position check.
- "It forgot the text" means carryover source search.
- "It feels like a slide" means replace fade/cut with camera motion.
- "Too fast" means extend transition or add hold after landing.
- "Too empty" may mean add ambient motion, not new panels.

## Handoff Format

Report:

- Transition type.
- Boundary timestamps.
- Changed carryover files.
- Proof frames.
- Whether source scene and next scene were both refreshed.

## Provenance

Adapted from https://github.com/saranambiar/hyperframes-video-agent-skills (Apache-2.0, community project — not an official HyperFrames or HeyGen repository). Edit this skill freely as the workflow evolves; keep this provenance section.
