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

## Pipeline CSS + font wiring (verified v0.8.35, 2026-09-13)

- **Styles + fonts are per-video committed snapshots, not live references.** `pipeline/snapshot_style.sh <video-dir>` copies `pipeline/style/{tokens.css,setpieces.css,brand-mark.svg}` + `pipeline/fonts/*.woff2` into `videos/<slug>/{style,fonts}/`, rewrites `../fonts/`→`fonts/` in tokens.css, and stamps the pipeline SHA as a banner. `new_video.sh` runs it automatically. The video build log pins the pipeline SHA the snapshot came from (its version of record); a refresh = delete + re-snapshot + build-log note (the script refuses existing snapshots).
- **Why a snapshot:** (1) render workers resolve CSS `url()` relative to the css file, and lint errors on any asset path climbing above the project root (`invalid_parent_traversal_in_asset_path`) — a `../pipeline/style/` link cannot work from inside the project; (2) determinism: the render's inputs must live in the video dir so a committed re-render never depends on tree state outside it.
- **Asset paths in compositions: root-relative only** (base URL is the project root): `style/tokens.css`, `style/brand-mark.svg`, `assets/x.mp4`. Never `../`.
- **SVG box size ≠ drawn size.** Drawn geometry scales with the viewBox: drawn_extent = (extent_in_viewBox_units / viewBox) × box. When the spec pins a drawn dimension against a fixed layout (a ring with clearance math to text), read the asset's viewBox and the drawn element's radius, then set box = target_drawn × viewBox / drawn_extent_units. Eye-boxing the box to the target draws the wrong size and silently breaks the spec's clearance math (a 640px box on a viewBox-800 asset with r=330 draws a 528px ring).
- **SVG assets must be well-formed XML — no `--` inside XML comments.** CSS custom-property names (`--paper`, `--seal-amber`) in an SVG's comment make the file malformed: strict XML viewers reject it (`Comment must not contain '--'`) and the render's media preflight fails to load it (`media_load_failed` → broken-image frame). `<img src>` and inline SVG both work once the file is well-formed. (2026-09-13: `brand-mark.svg` shipped with `--paper`/`--seal-amber` in its comment; fixed at the pipeline source, snapshot re-synced, re-verified by render.)

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

## Sub-composition Authoring (verified v0.8.35)

A scene file is standalone HTML: its own `<div data-composition-id="scene-XX" data-start data-duration data-width data-height>` root, its own paused GSAP timeline registered under that ID, its own GSAP script tag. It renders alone via `--composition composition/scene-XX.html`. It mounts in `index.html` via `<div data-composition-id="scene-XX" data-composition-src="composition/scene-XX.html" data-start data-duration data-track-index>`.

**Carry the master's global resets into the standalone scene.** A sub-composition renders alone (probe + `--composition` renders) and is not mounted in the master, so any global reset the master CSS applies (notably `* { box-sizing: border-box }`) does not reach it. Pinned geometry derived from box-sizing then drifts silently — e.g. inline-block spans inside table rows pull the line-box strut into each row and a 56px row renders 77px, shifting every ruled line off its pinned y. If a probe render's geometry disagrees with the spec while the markup matches, suspect a missing global reset before suspecting the pin.

**Timing: cues are local, the offset lives only on the mount.** The composition root is always `data-start="0"` with `data-duration` = window length, and every GSAP cue is in the composition's local time (the spec's master word-start minus the window start). The global window offset lives only on the `index.html` mount div's `data-start` (= window start). If you set the root's `data-start` to the window start AND author cues in master time, the scene shifts by the offset and the render shows a blank lead-in of exactly that many seconds (the double-offset bug). Convert the cues to local once and keep the root at 0.

**Initial hidden state lives in CSS, not only a `tl.set` at t=0.** Elements hidden until a cue start hidden in CSS (e.g. `.hide-y { opacity:0; transform: translateY(12px) }`), so the render's first frame is correct even if the timeline hasn't applied its t=0 state. GSAP then animates them in. For a center-aligned element already using `translateX(-50%)`, bake the 12px slide into the same CSS transform (`translateX(-50%) translateY(12px)`) and reveal to `translateY(0)` — a reveal that only sets `y` won't compose with a `translateX(-50%)` the CSS didn't set up.
- **Reveal the hidden element itself, never only its children.** Opacity multiplies down the DOM: a reveal on child spans is invisible while a parent sits at `opacity:0`, so the settled frame reads as missing content with no lint, check, or motion signal. When the whole element enters on one cue, animate the element; per-child reveals only when the spec's verb is a sequence.

Lint is strict about mount elements: every `data-composition-src` host needs **both** `data-composition-id` and a stable `id` (the second is the Studio edit target) — a host with only `data-composition-src` is a lint error, not a warning.

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

## Project & CLI Mechanics (verified v0.8.35)

- A HyperFrames "project" is just a directory containing an index.html — no global install, no node_modules, no lockfile, no daemon. `render`, `lint`, `check`, and `preview` all take the project directory as an argument.
- Per-video vs. once: scaffolding happens once, when authoring the pipeline's committed skeleton; every new video is a **copy** of that skeleton. Never run `npx hyperframes init` inside this repo — it emits vendor router docs (AGENTS.md/CLAUDE.md) that claim authority over agent behavior and conflict with the repo's own skills. If the video dir pre-exists the scaffold (audio-first), `new_video.sh` refuses it — copy the skeleton's project files in manually, slug `meta.json`/`package.json`, leave committed files untouched, and verify boot with `lint` + `check` before committing.
- Framework version is pinned in exactly one place (the pipeline render script / skeleton package.json). All hyperframes commands run through npx with that pinned version; never leave them bare in committed scripts or notes.
- `npx hyperframes skills update` installs vendor skill docs into the home agent dirs (`~/.claude/skills`, `~/.agents/skills`) — this repo's agent stack reads only its own repo skills, so never run it here. The only opt-out env var is `HYPERFRAMES_SKIP_SKILLS=1`; set it in the render script as defense in case a future version makes the check mandatory. If vendor skill dirs or symlinks appear under `agents/video/skills/` in git status, they are vendor-install pollution (the repo skills dir is one of the vendor's install targets, so it symlinks into `~/.claude/skills`): remove the repo symlinks and the home-dir entries — they are never repo content and never get committed. If one specific framework detail is missing from the repo skills, pull that one reference file into the repo skill library with an Apache-2.0 provenance note — never bulk-install vendor skills.

## Master Assembly (index.html, verified v0.8.35, 2026-09-14)

- **Mount scene compositions as CHILDREN of the root composition div, not siblings.** As siblings, the compiler ignores the root's `data-duration` and resolves the render to the first mount's own duration — observed: a 9-scene master rendered 2.69s (65 frames = scene-01's window) with zero lint/check warnings. Confirmed by the vendor reference `hyperframes-launch-video` (mounts nested in the root div) and the HTML schema ("an explicit root data-duration is the render length").
- Root `data-duration` = the beat-map `master_duration_s` (scene windows sum exactly to it). Verify after render that the compiler log's `durationSeconds`/`totalFrames` match — a wrong duration is silent in lint/check.
- `--quality` takes `draft|standard|high` — `final` is rejected at render start. Use `high` for full renders.
- Assembly of the narration master = single master render of `index.html` (scenes authored at 1:1 beat-map windows) + `ffmpeg -c:v copy -c:a aac` mux of the committed wav. No per-scene retiming when windows match the beat map. Commit the `timeline-manifest.json` (beat-map windows, wav sha256, proof timestamps) with the assembly commit; the muxed MP4 is gitignored like all renders.
- Boundary QA: a scene's first frame in the master must frame-match its standalone render's first frame (~0.1–0.2% pixel diff = codec micro-block level) — catches mis-mounted or shifted scenes at every cut.

## Render Loop

Typical commands (the repo's render script in `videos/pipeline/` wraps these): the video directory is the positional argument to every command.

```bash
pipeline/render.sh <video-dir> preview
pipeline/render.sh <video-dir> lint
pipeline/render.sh <video-dir> check   # lint + runtime + layout + motion + contrast in one browser session
pipeline/render.sh <video-dir> render --composition composition/scene-name.html --output renders/scene-name.mp4 --fps 24 --quality draft --workers 2
```

`render.sh` is the sanctioned entry point: pins the framework version, sets `HYPERFRAMES_SKIP_SKILLS=1`, and appends a build.log line per invocation. Bare `npx hyperframes <cmd> <video-dir>` is for diagnostics only — see the `--output` pitfall below.

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
- If an SVG line-draw (stroke-dashoffset) reveals in the wrong direction or leaks a segment before its cue, the dash math is off. Two traps, both caught on a lifecycle-loop scene: (1) `stroke-dasharray` MUST equal the path's measured length — a dasharray shorter than the path leaves the tail un-hidden, so it renders pre-cue (the "gap" only covers part of the path); for a straight-line path, sum the segment lengths by hand — re-sum from the actual coordinates every time you change the path (a reroute re-derived from memory can be off by the segment you edited: 2152 vs true 2228 on the s04 side-elbow, a 76-unit leak of the final stub). (2) reveal direction = the path's point order: dashoffset `length→0` draws from the first point toward the last; to draw last→first, reverse the `d` point order rather than animating offset `0→length` (that direction is unreliable). (3) clearance math uses the cap extremum, not the path endpoint — a round line cap extends stroke_width/2 past the endpoint, so "the line ends above the text" from path geometry alone can still cross the glyphs; verify cap-to-text clearance in a settled proof frame. (4) prove the pre-cue frame with a region scan at the DIM threshold (~50 for --paper-dim on the dark background; the dim ink sits at ~50–116, so a bright-ink >90 threshold — and a downscaled vision pass — reads a real leak as zero): the draw zone must be 0 non-ink before the cue, and a few mid-draw frames must show the visible head advancing the intended way.
- If a table's ruled line (or any collapsed table border, `border-collapse`) renders through an ancestor row set to `opacity: 0`, that is the collapse mechanism, not a missing gate: the browser draws the collapsed border at the table grid, outside the row's element tree, so row opacity never hides it and the line can light up with the frame draw, long before its own cue. Fix: keep the structural border but make it color-transparent (a transparent border still wins the collapse, so row geometry is unchanged) and paint the visible line as an absolutely-positioned overlay div, revealed on the element's own cue.
- If a centered label in a fixed-size box renders flush against the box's left edge instead of centered, the cause is a shrink-to-fit flexbox no-op: an absolutely-positioned element with `display:flex; justify-content:center` but **no `width`** collapses to the width of its text, so `justify-content:center` has no spare space to distribute and the text hugs the left edge. Lint, check, and motion all pass — it is silent. Fix: give the label the same explicit `width` as the box so the flex container has the box's full width to center within.
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

## Scene-Spec Cue Rules (Phase B, this repo)

Spec-side rules (window derivation, cue-table verification against words.json, change floor) live in `scene-spec-and-commit` — the one-scene-spec-then-commit loop. Scene specs are that skill's output. The Phase C build loop — executing a committed spec, draft-rendering, proof-checking, committing one scene at a time — is `scene-build-and-commit`; it consumes scene specs as build contracts and delegates the composition craft here (GSAP/timeline/asset-path/proof-frame mechanics).

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
- Precompute monospace layout instead of eyeballing it: JetBrains Mono's advance is 0.6× the font size (30px → 18px/char). For a centered text chain, compute each node's center/left from char-count × advance plus the gaps, so the whole chain fits the safe margins before you render. Also use it to **detect collisions between two centered lines on the same row pinned to adjacent centers**: if each line's width (char-count × advance) approaches the center-to-center spacing, the two lines kiss or overlap (two ~40-char lines at 22px mono ≈ 480px each will collide in 400px of spacing). When one line is locked in place by content stacked below it, the fix is to split the movable line into two stacked centered lines — matching whatever stacked pattern a neighboring column already uses — rather than retiming or re-centering either.

## Render Strategy

Use draft renders while iterating:

- Lower worker count if GPU/Chrome becomes unstable.
- Use exact requested FPS for final.
- Render only changed scenes after a surgical edit.
- Keep old renders until the replacement is verified.
- Generate proof frames from the rendered MP4, not only browser screenshots.

## HyperFrames-Specific Risks

Watch for:

- **`--output` resolves relative to the shell CWD, not the project dir** — a bare CLI render silently dumps the MP4 at the repo root instead of the video dir. Always render through `pipeline/render.sh`, which re-anchors relative `--output` to the video dir (landed renders must sit under `videos/<slug>/renders/`, gitignored).
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

Ease curve gotcha: a `power2.out`-style ease is front-loaded — opacity is ~80% in at ~20–25% of the duration, so "mid-reveal" at an early proof timestamp is a misnomer; the frame reads nearly settled. Judge reveal proofs by measured opacity (max brightness in the element band, normalized against the ink/paper tokens), and keep the real bars: nothing visible before the cue, element fully in by the end of its naming word.

## Handoff Format

Report:

- Composition path.
- Render path.
- FPS and duration.
- Proof frame paths.
- Known lint warnings.
- Whether warnings are pre-existing or introduced.

## Provenance

Adapted from https://github.com/saranambiar/hyperframes-video-agent-skills (Apache-2.0, community project — not an official HyperFrames or HeyGen repository). Edit this skill freely as the workflow evolves; keep this provenance section.
