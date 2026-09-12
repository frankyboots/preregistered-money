# HyperFrames skeleton (pipeline)

The committed HyperFrames project scaffold. **New video = copy of this directory** —
`pipeline/new_video.sh <slug>` does it.

## Rules

- **Never run `npx hyperframes init` inside this repo.** It emits vendor router docs
  (`AGENTS.md`/`CLAUDE.md`) that claim authority over agent behavior and conflict with
  the repo's own skills, and it triggers a vendor-skill install check.
- **Never run `npx hyperframes skills update`** (installs vendor skills into home agent
  dirs). All hyperframes invocations go through `pipeline/render.sh`, which sets
  `HYPERFRAMES_SKIP_SKILLS=1` and pins the framework version.
- **One framework version pin**: `HF_VERSION` in `pipeline/render.sh` (mirrored in
  `package.json` here). Update both together; record the bump in the next video's build log.
- A video directory is a HyperFrames *project* (root = `index.html`). No node_modules,
  no lockfile, no daemon — everything runs via `npx --yes hyperframes@<pinned>`.

## Structure

```
<video-slug>/                # = this skeleton, copied by new_video.sh
├── spec.md                  # authored per video from pipeline/templates/ — committed BEFORE first render (CONCEPT §4.1)
├── index.html               # composition entry point (render default); master assembly of scene compositions
├── hyperframes.json         # project config (paths) — do not edit per video
├── meta.json                # project id — update to the slug when copying
├── package.json             # pinned hyperframes scripts (backup path; render.sh is primary)
├── composition/             # one HTML file per scene (CONCEPT §4)
├── data/                    # small derived data inputs + sources + checksums
├── audio/voiceover.wav      # committed TTS output (CONCEPT §7)
├── thumbnail.png
└── build.log                # appended by render.sh on every invocation; committed with the change
```

Renders land in `<video-slug>/renders/` (gitignored — regenerable). Proof frames are
the committed QA artifact (`pipeline/tools/extract_proof_frames.py`).

## Render

```bash
pipeline/render.sh videos/<slug> render --composition composition/scene-01.html --quality draft
pipeline/render.sh videos/<slug> lint
pipeline/render.sh videos/<slug> check
pipeline/render.sh videos/<slug> preview
```
