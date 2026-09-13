---
name: scene-build-and-commit
description: "Use when building one scene (Phase C loop)."
version: 1.0.0
author: Preregistered Money
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [video, scene-build, phase-c, composition, proof-frames, build-log, commit]
    editorial_name: Scene Build And Commit
    editorial_description: "The Phase C loop: one scene built from its committed spec, draft-rendered, proof-checked against the spec's QA checklist, and committed before the next scene starts."
---

# Scene Build And Commit

One scene of Phase C, then commit, then the next. The loop is build 01 → commit → build 02 → commit. Never batch multiple scene builds into one commit; never start scene N+1 while scene N is uncommitted. The committed scene spec (Phase B, `scene-spec-and-commit`) is the build contract — this skill does not re-derive the design, it *executes and verifies* the spec, then records it. (Provenance: the channel's first video, `meta-preregistration-rules`, 2026-09; the build contract reference is `scene-specs/scene-01.md`, the composition mechanics come from `hyperframes-scene-builder`, the commit from `video-commit`.)

## Prerequisites (all committed, this is the gate)

- `scene-specs/scene-NN.md` — the build contract (window, cue table, inputs, QA checklist). Status not yet "built".
- Phase A artifacts locked: `spec.md` (citation table), `audio/timing/{words.json,beat-map.json}`, `style/` snapshot, `data/` inputs.
- The previous scene's build committed (scene 01: none). Its final frame is scene N's continuity-in reference.
- `videos/pipeline/render.sh` (the only sanctioned hyperframes entry point), `videos/pipeline/tools/{extract_proof_frames.py,probe_media.py,scan_theme_colors.py,make_contact_sheet.py}`.

If a prerequisite is missing, stop — Phase C consumes committed state, it does not author it. A missing or contradictory spec is a Phase B defect; fix and commit the spec first (its own commit), then start this one.

## Step 1 — Read the contract

From `scene-specs/scene-NN.md`, take, verbatim:

- **Window** (Scene Identity) → the mount's `data-start` (window start) + `data-duration` (window length), the root's `data-duration`, and the render's expected length.
- **Source composition** + **Render output** paths (Scene Identity) — the file to author and the MP4 the render must land at.
- **Output format** (resolution, fps, quality) — draft fps/quality per the spec's Phase C line.
- **Data inputs** (Inputs) — files under `data/` to draw charts from; or "none. No number appears in this scene." If a shown number has no committed data input or no citation in `spec.md`'s table, stop (Step 6 rule).
- **Cue table** (Beat Timeline) → the GSAP timeline: each cue's word-start time, visual action, required proof.
- **QA Checklist** → the exact proof timestamps and acceptance bar this scene must meet before it is "done."

The spec is the whole design brief. Do not invent layout, motion, or content the spec does not pin. If you find yourself wanting to change the design, that is a spec amendment — stop and flag it; do not silently redesign.

## Step 2 — Author the composition

Build `composition/scene-NN.html` to the spec. Craft rules live in `hyperframes-scene-builder` (sub-composition authoring, GSAP timeline rules, root-relative asset paths, component patterns) — follow that skill; the rules below are the Phase C loop's non-negotiables:

- Standalone HTML: `data-composition-id="scene-NN"`, `data-width`, `data-height`, `data-start="0"` + `data-duration` = window length (cues are local to the root; the window offset goes only on the `index.html` mount — see Step 3). Paused, seekable GSAP timeline registered under that ID; initial hidden states in CSS (see `hyperframes-scene-builder`); cues placed at the spec's word-start times minus the window start (the visual completes within ≤250ms of its cue unless the spec notes otherwise).
- Import `style/tokens.css` + `style/setpieces.css` root-relative (base URL is the project root) — never `../`. Colors from tokens only; motion verbs from style spec §5.2 only. No P&L red/green where nothing is judged.
- Draw charts/tables from the `data/` input files — never type a number into markup.
- **Data-injected strings: build script + template, verified by re-parse.** When an Inputs line says "read from the file at build time, never computed and never typed into markup" (a SHA, an exact command line), commit a small generator (`scripts/_build_sceneNN.py`) + template that checksums the data input, injects its characters as spans, and re-parses the generated markup to assert byte-identity with the file. Parse by span class, not regex char class — a command like `git commit <sha>` contains the same alphabet as hex, so `[0-9a-f]` matches the wrong spans. The script + template are committed provenance (same input → byte-identical output); the generated composition is derived from them.
- SVG assets well-formed (no `--` inside XML comments).

## Step 3 — Mount + lint + check

Mount the scene in `index.html` via `data-composition-src="composition/scene-NN.html"`. The mount host needs **both** `data-composition-id` and a stable `id` (lint errors on a host with only `data-composition-src`). Mount `data-start` = window start, `data-duration` = window length, `data-track-index` = scene order. The composition root itself stays `data-start="0"` — setting the window start on *both* mount and root double-offsets the scene (blank lead-in of exactly the window-start seconds).

Then, through the sanctioned entry point (never bare `npx hyperframes` in committed work):

```bash
pipeline/render.sh <video-dir> lint
pipeline/render.sh <video-dir> check   # lint + runtime + layout + motion + contrast
```

`lint` must be 0 errors (per the spec's acceptance bar). `check` must pass. A pipeline bug found here is a `fix`/`feat(pipeline)` commit of its own — *before* re-running — never bundled into the scene commit.

## Step 4 — Draft render

```bash
pipeline/render.sh <video-dir> render --composition composition/scene-NN.html --output renders/scene-NN.mp4 --fps <spec fps> --quality draft --workers 2
```

`render.sh` re-anchors relative `--output` to the video dir (landed MP4 must sit under `videos/<slug>/renders/`, gitignored) and appends a build.log line per invocation automatically. Higher fps/quality only when the scene is approved or testing fps-specific motion. Draft first; final render is Phase D's job.

## Step 5 — Proof frames against the spec's QA checklist

Extract proof frames at **exactly the timestamps the spec's QA Checklist names** — first frame, each boundary proof, each audio-sync proof, the final-frame proof — then judge each against the spec's stated expectation:

**The MP4's clock is render-local.** `--time` is an offset into `renders/scene-NN.mp4`, which starts at 0 — for a single-scene render that is *not* the spec's master time. Master time (what the QA checklist names) = render-local + the window start; convert once, extract in local. Master times on a single-scene MP4 silently yield empty/blank frames for any time beyond the window length (ffmpeg -ss past EOF prints no frame) — the tool exits 0.

**Pre-naming negative proofs must verify their frame.** The extractor seeks with `ffmpeg -ss t`, which returns the first frame at pts ≥ t — a "pre-cue" time a few ms before the cue lands ON the cue frame, so a red "leak" can be a false positive on the first visible frame, and a green one proves nothing. Verify each negative landed pre-cue (frame index = floor(t × fps) < the cue frame), and prefer a frame-exact sweep across the cue: the first lit frame must equal the cue frame, which is direct proof that nothing is over-named by a frame. Run the sweep vectorized, not as a per-pixel Python loop over frames — a loop over hundreds of full-res frames OOMs the execution kernel; the recipe (one ffmpeg rawvideo dump, numpy memmap, per-token thresholds, hold hashing) is `references/full-frame-sweep.md`.

```bash
python3 pipeline/tools/extract_proof_frames.py <video-dir>/renders/scene-NN.mp4 --time <t1> --time <t2> --output-dir <video-dir>/snapshots/scene-NN-proof/ --prefix scene-NN
python3 pipeline/tools/probe_media.py <video-dir>/renders/scene-NN.mp4   # duration, fps, streams
python3 pipeline/tools/scan_theme_colors.py <composition or video-dir>  # token-only colors
```

`extract_proof_frames.py` takes the full MP4 path (not the video dir), one `--time` per frame (repeatable), and writes to `--output-dir` with `--prefix`-numbered filenames. The first frame must be blank ink + persistent set pieces (corner bug) — if it comes out white or shows content, suspect a double-offset (Step 3) or missing CSS initial hidden state before touching cues. For risky content (a font glyph you haven't rendered in this stack, a long text chain that must fit margins), draft a throwaway probe composition (an `_probe-` name, never committed, deleted before commit) and verify it in a render before authoring the full scene.

**Hold verification: hash the decoded frames, don't eyeball them.** Decode the hold window (same rawvideo dump) and hash every frame — the plateau must be byte-identical. If two plateau blocks differ, diff them element-wise, take the bbox and max channel diff, and judge: a few hundred px, max diff ≲10/255, confined to a text AA edge → codec micro-block, record bbox + max diff in the build log and it passes; anything wider or brighter → real motion, fails, fix the timeline. Extracted-frame holds (three spaced times, SHA-identical PNGs) are the quick check; the per-frame hash plateau is the strong one — use both when the spec's QA line names the hold.

Pass/fail per the spec's Acceptance line (lint 0 errors; final-frame proof matches the spec layout; `scan_theme_colors.py` clean). Check audio-sync: each key element fully visible by the end of its naming word. Check the bottom 132px caption band is clear of key text. If a proof fails, fix the composition and re-render — do not lower the bar to pass. `make_contact_sheet.py` for a quick multi-frame look.

**Pixel audits: calibrate to the token, separate codec fringing.** Draft h264 renders put warm chroma fringing on bright text edges — a "foreign color present" pixel check catches isolated fringe pixels (a few per local window) even when the scene uses only tokens. Separate a real filled region from fringing by density (a glyph row packs far more colored pixels per small window than fringing ever does), and keep `scan_theme_colors.py` clean as the acceptance criterion with pixel scans as diagnostics. Likewise, ink/brightness floors must be set per the actual rendered token — a dim text token peaks well below a bright paper token, and a floor calibrated to one token reads the other as absent or present.

**Proof expectations for fast reveals: measure, don't guess.** The pinned `--ease-out` (power2.out) is front-loaded — a 250ms reveal is already ~83% opaque at 24% of its duration. "Mid-reveal at cue+60ms"-style cells written from a linear mental model fail against the rendered pixels; "not visible before the cue" and "fully in by the end of the naming word" are the hard bars. When a proof cell contradicts the pinned duration+ease, that is a spec defect: amend the cell to the measured curve (a few extra frames + pixel brightness) and ship the measured-geometry amendment in the scene commit with a build-log note (no design change → rides with the build; a design change is a spec commit first, per Step 1) — never change the motion to pass a cell, and never hand-wave the mismatch in the build log. Likewise pick the motion verb by its settle time: it must land inside both the spec's proof timestamps and the end of the naming word; if the spec's own verb can't settle inside both (a type verb that finishes after the word ends), that is a spec defect on the verb — fix the spec, do not silently switch to the verb that passes.

## Step 6 — Build-log entry (same commit as the build)

The build log is regenerated, not narrated. For this scene, the log carries:

- The `render.sh` auto-line (one per render invocation, already appended).
- A composition entry in the Phase C section: `composition/scene-NN.html` + sha256, `renders/scene-NN.mp4` (duration + fps), the style-spec version + pipeline SHA the snapshot came from, data inputs used (with checksums) or the "no number appears" note, and the render command. Same input → same pixels must be checkable from this file.

If a shown number has no committed data input / `spec.md` citation → stop; the video never computes it (request a new prereg on the research side).

## Step 7 — Commit (one scene = one commit)

Per `video-commit` (boundary, concurrent-writer re-check, 6-point integrity checklist). Message:

```
video(video-<slug>): scene NN built (<name>)
```

Body: window + render command + proof evidence (which spec timestamps verified, lint 0 errors, check pass, `scan_theme_colors` clean) + build-log note (composition sha256, style-spec/pipeline versions, data inputs or no-number note). Composition + its build-log update are ONE coherent commit.

Tracker update rides with the commit (scene built, next scene number, next action). Reference the *previous* scene by SHA; reference *this* scene by name — never this commit's own SHA (self-reference breaks on amend; git log carries the SHA). `memory` tool: a `replace` swaps the WHOLE tracker entry, so `content` is always the complete new tracker text. When a `replace` fails "No entry matched", read the error's `current_entries` before retrying — the store may already be current (the commit's MEMORY.md wrote it); retry only if genuinely stale, with the full text.

## Handoff

Report: composition path, render path (duration + fps), proof frame paths + what each verified, lint/check/theme-scan results, data inputs used or the no-number note, the commit (message + scope) per `video-commit`, and the next scene in the loop.

## Stop conditions

- No committed scene spec, or the spec contradicts a locked Phase A artifact → Phase B defect; fix + commit the spec first (its own commit), then build.
- `lint`/`check` fail on a pipeline bug → separate `fix`/`feat(pipeline)` commit, then re-run; do not bundle into the scene commit.
- A shown number has no committed data input or `spec.md` citation → stop; request a new prereg, never compute it in the composition.
- A required proof frame does not match the spec's stated expectation → fix the composition and re-render; do not lower the acceptance bar.
- A re-render from the committed dir does not reproduce the pixels → incident: fix the pipeline (its own commit), never hand-edit the output.
