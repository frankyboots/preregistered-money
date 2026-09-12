# Video Pipeline

Shared, versioned production tooling for `videos/`. A video never vendors a copy of
anything in here — its build log names the pipeline version (git SHA) it used
(VIDEO_CONCEPT §4, §7).

```
pipeline/
├── skeleton/   # committed HyperFrames project skeleton — new videos are COPIES of this
├── tools/      # deterministic QA / assembly utilities (see below)
├── templates/  # spec + storyboard + change-request + timeline-manifest templates
├── style/      # style-spec.md v1.1.0 + tokens/setpieces css + brand-mark.svg (semver)
├── brand/      # channel art (banner, profile logo) — generator + committed renders
├── render.sh   # only hyperframes entry point: pins version, skips vendor skills, logs to build.log
├── new_video.sh# create videos/<slug>/ from skeleton/ + spec template
└── tts/        # TTS glue (ElevenLabs v3) + pinned voice/model/settings           [pending]
```

## Working with HyperFrames

- **A HyperFrames "project" is just a directory** (root = `index.html`). No node_modules,
  no lockfile, no daemon. Every command (`render`, `lint`, `check`, `preview`) takes the
  project dir as an argument.
- **Scaffold once, copy per video.** The skeleton in `skeleton/` was authored once
  (equivalent of `hyperframes init`); every new video is
  `pipeline/new_video.sh <slug>`. **Never run `npx hyperframes init` inside this repo**
  — it emits vendor router docs (AGENTS.md/CLAUDE.md) that claim authority over agent
  behavior, and it triggers a vendor-skill install. **Never run `npx hyperframes skills
  update`** either. All invocations go through `render.sh`, which pins the framework
  version (`HF_VERSION`) and sets `HYPERFRAMES_SKIP_SKILLS=1`.
- **Renders are not committed** (gitignored `<video>/renders/`); proof frames are the
  committed QA artifact. A CI re-render of the committed dir must reproduce the
  published pixels.

## tools/

All stdlib-only Python; require `ffmpeg`/`ffprobe` on PATH.

| Script | Use |
|---|---|
| `probe_media.py FILE` | Duration, codec, resolution, fps, audio streams. Run before and after every render/assembly. |
| `extract_proof_frames.py VIDEO --time label=0.5 --time label=27.0 -o snapshots/proof [--contact-sheet sheet.jpg]` | Exact-timestamp proof frames. The core QA primitive. |
| `make_contact_sheet.py IMG... -o sheet.jpg` | Multi-scene visual QA sheet. |
| `scan_theme_colors.py DIR --allow "#111111" --allow "#ef6f22"` | Palette-drift linter: finds color values outside the allow-list in CSS/HTML/SVG/JS sources. |
| `timeline_manifest_to_ffmpeg.py MANIFEST.json` | Turns a timeline manifest (see `templates/timeline-manifest.example.json`) into an FFmpeg assembly plan. |

## templates/

| Template | Use |
|---|---|
| `scene-spec.md` | Per-beat/per-scene spec; feeds the video's `spec.md` beat sheet. |
| `storyboard.md` | Multi-scene structure with lock/approval state. |
| `change-request.md` | Surgical final edits: what changes, what must not, proof timestamps. |
| `timeline-manifest.example.json` | Schema for scene assembly plans (retime, segment-map, hold frames, proofs). |

## Provenance

`tools/` and `templates/` are derived from
[hyperframes-video-agent-skills](https://github.com/saranambiar/hyperframes-video-agent-skills)
(Apache-2.0, community project — not an official HyperFrames or HeyGen repository).
The full Apache-2.0 license text is in `LICENSE`; each vendored file carries a
provenance header. **Change policy:** the curator and the agent are expected to
edit these files freely — that is the point of a working pipeline. The only
obligation is Apache-2.0 §4(b): when you modify a vendored file, note the change
in its header (one line, what and why). Git history carries the rest; do not
track upstream commits per file. The production *judgment* layer built on these
tools lives in the video agent's skills: `end-to-end-video-playbook`,
`hyperframes-scene-builder`, `audio-sync-assembly`, `captions`,
`render-qa-and-surgical-changes`, `motion-design-systems`,
`scene-continuity-and-transitions`, `video-intake-and-storyboard` — each carries
a Provenance section and may be edited freely the same way.

The music-bed caption tooling from the source repo was intentionally not vendored:
standing decision is no music (VIDEO_CONCEPT §7), and captions ship as soft SRT
generated from the committed voiceover wav (§11).
