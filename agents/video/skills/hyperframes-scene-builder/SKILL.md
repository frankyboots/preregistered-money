---
name: hyperframes-scene-builder
description: "Use when building or revising a HyperFrames scene."
version: 1.0.0
author: Preregistered Money
license: Apache-2.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [video, hyperframes, composition, gsap, render]
    editorial_name: HyperFrames Scene Builder
    editorial_description: "Composition craft for agent-built scenes: one HTML file per scene, paused seekable GSAP timelines, draft-then-final render loops, and the proof-frame checklist."
---

# HyperFrames Scene Builder

Use this skill when implementing or revising a HyperFrames scene. This skill assumes HyperFrames is the render engine and the scene source is HTML/CSS/JS.

## Project Conventions (this repo)

One video = one directory (VIDEO_CONCEPT §4):

```text
videos/<slug>/
├── spec.md            # gates rendering
├── composition/       # one HTML file per scene
├── data/              # small derived data inputs + sources + checksums
├── audio/voiceover.wav
├── thumbnail.png
└── build.log          # regenerated every render
```

Shared, versioned things (templates, render script, TTS glue, fonts, style spec) live in `videos/pipeline/`. A video never vendors a copy of a template — the build log names the template and style-spec versions used. The render script in `videos/pipeline/` is invoked with only the video dir as input.

Keep files small enough to inspect and diff.

## Composition Rules

- Define an explicit composition root with `data-composition-id`, `data-width`, `data-height`, and timing metadata where the project uses it.
- Register GSAP timelines under the matching composition ID.
- Scope selectors to the composition root when scenes are nested.
- Avoid global selectors that can mutate other sub-compositions.
- Prefer reusable HTML/CSS components for repeated cards, labels, charts, rings, logo rows, and panels.
- Keep media paths relative to the composition project.
- Draw charts from the video's committed data inputs (`videos/<slug>/data/`), never from numbers computed in the composition.

## GSAP Timeline Rules

- Use paused timelines for deterministic seekable animation.
- Place important moments at named labels or exact seconds.
- Use `set` for initial state.
- Use `fromTo` when CSS transforms already exist.
- Avoid accidental opacity-only transitions when the request asks for physical or material motion.
- Avoid bounce/rebound unless the user explicitly asks for it.
- Keep final frame stable enough for proof extraction.

## Render Loop

Typical commands (the repo's render script in `videos/pipeline/` wraps these):

```bash
npx hyperframes preview
npx hyperframes lint
npx hyperframes render --composition compositions/scene-name.html --output renders/scene-name.mp4 --fps 24 --quality draft --workers 2
```

Use higher FPS or quality only when the scene is approved or when testing frame-rate-specific motion. Every material render updates the build log.

## Visual QA

After rendering:

- Extract first-frame, key-beat, and final-frame PNGs (use `videos/pipeline/tools/extract_proof_frames.py`).
- Compare reference-image scenes against the final frame, not only the opening frame.
- Check text fit at desktop/video resolution.
- Check that hidden duplicated frames in following scenes are updated.
- Check theme colors in CSS, SVG fills/strokes, and inline styles (`videos/pipeline/tools/scan_theme_colors.py` against the style-spec palette).

## Common Fixes

- If a scene transition forgets a new label or visual, patch the next scene's carryover frame too.
- If timeline objects appear too early, verify initial `opacity`, path progress, and node visibility.
- If path points appear before the line reaches them, reveal points on line-progress milestones.
- If text gets clipped by a ring or card, reduce the full system scale instead of only shrinking the label.
- If a value on screen does not match the cited results doc, stop — the data input is wrong, not the composition.

## Output

Return changed composition files, render command used, render path, and proof frame paths.

## File Organization Guidance

Prefer:

- One HTML file per scene.
- Small sub-compositions for reusable sections.
- Shared design tokens near the top of the file.
- Component functions or repeated class patterns for repeated visuals.
- Asset paths that are easy to replace.

Avoid:

- One giant file for a full video.
- Inline magic numbers without comments for timeline-critical values.
- Duplicated colors that should be tokens.
- Hidden copies of final frames without comments.
- Global CSS that affects all mounted scenes.
- Numbers typed into markup instead of read from a data input.

## Timeline Authoring Checklist

For every timeline:

- Set all initial states at time `0`.
- Name or comment important cue times.
- Keep object reveal order aligned to narration.
- Use path progress for charts and line drawings.
- Reveal graph points when the path reaches them.
- Keep labels visible long enough to read.
- Add final ambient motion only after main layout lands.
- Avoid animations after the final hold unless ambient and subtle.

## Text And Layout QA

Before rendering final:

- Check long words fit their containers.
- Check captions will not cover key scene text.
- Check chart labels do not overlap paths.
- Check logo rows have spacing and no separator artifacts unless intended.
- Check cards and tables are not oversized.
- Check final frame matches reference scale.

## Render Strategy

Use draft renders while iterating:

- Lower worker count if GPU/Chrome becomes unstable.
- Use exact requested FPS for final.
- Render only changed scenes after a surgical edit.
- Keep old renders until the replacement is verified.
- Generate proof frames from the rendered MP4, not only browser screenshots.

## HyperFrames-Specific Risks

Watch for:

- Timeline ID mismatches.
- Unscoped selectors in nested compositions.
- GSAP overwriting existing CSS transforms.
- CDN or font loading differences between preview and render (fonts are pinned in the pipeline).
- Video/image assets not resolving in render workers.
- Large files becoming hard for agents to inspect.

## Component Patterns

Useful reusable scene components:

- `GlassPanel`
- `LogoRow`
- `ChartFrame`
- `PathCurve`
- `PointReveal`
- `CameraSwipe`
- `FinalFrameCarryover`
- `DisclaimerCard` (pinned, verbatim CONCEPT §10 — same pixels every video)
- `ScoreboardSegment` (renders from `scoreboard.json`)

These do not need to be formal JS classes. They can be CSS classes, HTML snippets, or helper functions as long as future agents can find and reuse them. Repeated components belong in the versioned pipeline templates, not copied per video.

## Proof Frame Checklist

Extract:

- First frame.
- First major reveal.
- Midpoint of main animation.
- User-requested timestamp.
- Final frame.
- Next-scene carryover start if relevant.

## Handoff Format

Report:

- Composition path.
- Render path.
- FPS and duration.
- Proof frame paths.
- Known lint warnings.
- Whether warnings are pre-existing or introduced.

## Provenance

Adapted from https://github.com/saranambiar/hyperframes-video-agent-skills (Apache-2.0, community project — not an official HyperFrames or HeyGen repository).
