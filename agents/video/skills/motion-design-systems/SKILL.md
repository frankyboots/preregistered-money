---
name: motion-design-systems
description: "Use when a video scene needs visual direction or style."
version: 1.0.0
author: Preregistered Money
license: Apache-2.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [video, design, motion, charts, theme, style]
    editorial_name: Motion Design Systems
    editorial_description: "The visual-taste layer: progressive chart reveal, small repeated motion vocabulary, tokenized colors, and the failure-recovery order when a scene 'feels off'."
---

# Motion Design Systems

Use this skill when the request depends on visual taste, design consistency, or reusable motion components.

## Brand First (this repo)

Palette, typography, and motion rules live in the versioned style spec (`videos/pipeline/style/style-spec.md`); the build log pins the version used. This channel is data-forward, faceless, and restrained: the visuals are the data (charts, tables, scoreboard, the sealed commit). If a motion effect explains nothing, it is cut. The defaults below apply only when no style-spec entry covers a decision.

## Start With The Visual System

Define these before animating:

- Background and lighting.
- Primary and neutral colors.
- Accent (one per series verdict color: confirmed / falsified / inconclusive).
- Typography and type scale.
- Component materials.
- Shadow style.
- Motion language.
- Forbidden looks.

Use `references/premium-motion.md` for motion language and `references/theme-tokens.md` for color discipline.

## Build Reusable Components

Create small components for repeated visual objects:

- Glass cards and panels.
- Logo rows.
- CTA lockups.
- Table frames.
- Chart axes, paths, labels, nodes, and gap fills.
- The pre-registered bar (always drawn on chart scenes).

Keep components parameterized with CSS custom properties or JS constants. Avoid hard-coded one-off colors if the user may request theme changes.

## Premium Motion Rules

- Prefer scale, blur, depth, path drawing, camera drift, and material changes over basic fade-only reveals.
- Use restraint. Premium motion should feel deliberate, not busy.
- Avoid bounce, rebound, neon, sci-fi HUDs, and generic SaaS explainer tropes unless explicitly requested.
- Use ease curves that settle naturally: `power2.out`, `power3.out`, `expo.out`, `sine.inOut`.
- Keep final-frame composition readable and still alive with subtle ambient motion.

## Chart And Data Storytelling

Use progressive reveal logic:

- Axes and labels establish the frame.
- Lines draw from left to right.
- Points appear only when the line reaches them.
- Labels sit near the object they describe, not in detached legends, unless the user asks for a legend.
- Gap fills appear after both curves make the gap meaningful.
- The pre-registered bar is drawn as a standing element, not a reveal for effect.
- A falsified result gets the same production values and the verdict color — no euphemism.

Read `references/chart-storytelling.md` for more.

### Anti-staleness: relevance ordering, not pixel activity

- Never ban scenes longer than N seconds. Long scenes are fine; cueless scenes are not. Boredom comes from preloaded frames sitting idle, not from duration.
- The frame state at any moment must equal the set of elements the narration has named so far — reveal each element on the word that names it, never more than ~2s before (axes/frame may pre-exist).
- Change floor: at least one state change per 10s of narration (new element, number roll, table row, line extension). A scene that can't hit the floor is overlong: split it or cut the script.
- Stillness is sanctioned only in the final hold — the settled, most-informative state, which is what proof frames check.
- A >3s narration silence is a script problem (tighten or add a cue), never something to fill with motion.

## Fonts (determinism)

- Scenes may only use the pipeline's vendored WOFF2 set (`videos/pipeline/fonts/`) via the pinned `@font-face` block in `tokens.css`; font checksums go in the build log. Never a runtime CDN font link — it breaks same-inputs-same-pixels and needs network at render time.
- Vendoring recipe (verified): `curl -sfL https://cdn.jsdelivr.net/fontsource/fonts/<family>@latest/<subset>-<weight>-normal.woff2 -o <Name>-<Weight>.woff2`, verify with `file` (must say "Web Open Font Format"), pin via `sha256sum`.

## Theme Consistency

When a theme changes:

- Search CSS, SVG, inline styles, gradients, canvas constants, and duplicated carryover frames (`videos/pipeline/tools/scan_theme_colors.py` against the style-spec palette).
- Do not recolor logos or user-provided reference imagery unless explicitly requested.
- Verify with proof frames from both source scene and next-scene carryover.

## Output

Provide:

- Component or composition changes.
- Token changes.
- Render/proof frame paths.
- Any remaining subjective items that need user approval.

## Visual Intake Checklist

Before designing:

- Identify audience and context.
- Identify brand colors and forbidden colors (style spec).
- Identify which series this is (Portfolio / Seal / Verdict / Build log / Meta) and its verdict color.
- Identify whether references are exact final frames or mood references.
- Identify whether the user wants premium restraint or high-energy editing (default here: restraint).

## Design System Defaults

When no brand system is supplied, default to:

- Warm off-white background.
- Black primary text.
- One accent color.
- Soft shadows.
- Conservative border radii.
- Plenty of negative space.
- Direct labels near objects.
- Few decorative elements.

Do not default to blue/purple gradients, neon lines, or dark sci-fi dashboards.

## Motion Palette

Use a small palette of repeated motion:

- Camera push.
- Camera swipe.
- Path draw.
- Material scale-in.
- Soft blur resolving to sharp.
- Highlight sweep.
- Gentle hold motion.

Repeating a small motion vocabulary makes multi-scene videos feel coherent.

## Component Size Discipline

For fixed-format video:

- Define dimensions explicitly.
- Keep title hierarchy separate from card hierarchy.
- Make cards smaller than instinct suggests.
- Leave room for captions.
- Test final frame with captions on.
- Avoid cards inside cards.
- Avoid chart labels that require a legend to understand.

## Brand Cleanup Checklist

When changing colors:

- Replace CSS variables.
- Replace raw hex values.
- Replace SVG fills and strokes.
- Replace shadows and glows.
- Replace gradients.
- Replace duplicated carryover frame styles.
- Leave real logos and user-provided imagery alone unless requested.

## Reference Matching Checklist

Compare:

- Object count.
- Relative positions.
- Scale.
- Typography weight.
- Line thickness.
- Border radius.
- Background warmth.
- Shadow softness.
- Label placement.
- Final hold readability.

## Questions To Ask

Ask if:

- The reference image conflicts with the style spec.
- A logo color conflicts with the requested theme.
- A crop or caption may hide important UI.
- The user asks for a subjective style change without enough preference.

Do not ask if the answer can be proven with a proof frame.

## Failure Recovery

If user says it feels off:

- Check scale first.
- Check spacing second.
- Check color consistency third.
- Check motion timing fourth.
- Check typography last.

Most "not premium" complaints come from oversized elements, too many colors, or uncontrolled motion.

## Provenance

Adapted from https://github.com/saranambiar/hyperframes-video-agent-skills (Apache-2.0, community project — not an official HyperFrames or HeyGen repository). Edit this skill freely as the workflow evolves; keep this provenance section.
