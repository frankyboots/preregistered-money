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
└── tts/        # TTS glue (ElevenLabs): voiceover.py (per-beat TTS), transcribe.py
                # (Scribe v2 word timings + SRT), voice_pin.json (the pin),
                # .venv (gitignored; elevenlabs SDK pinned by requirements.lock.txt)
```

## tts/ — narration glue (ElevenLabs)

The narration pipeline: `narration.md` (one `## beat-NN` per spec beat) → committed
`audio/voiceover.wav` (the timing source of truth) → `audio/timing/` (beat-map,
word-level transcript, SRT).

**Channel voices (duo — owner decision 2026-09-12):** the channel runs two
voices. `Helen` (`XB0fDUnXU5powFXDhCwa`, professional, en-british) is the
default narrator and narrates the pilot video; `Zane`
(`L6s7ahP9mHOb2S1Qynng`, "Cool & Energetic British Friend", professional) is the
second voice, reserved for future use (watch his energy against the channel's
flat/calm direction on his first beat). `voiceover.py` currently synthesizes a
whole script with the default `voice_id`; per-beat voice switching is a
documented extension, not yet built.

| Pinned (build log carries these) | Value / location |
|---|---|
| SDK | `elevenlabs` python — version in `tts/requirements.lock.txt` (venv: `tts/.venv`, gitignored) |
| TTS model | `voice_pin.json` `model_id` (`eleven_v3` per the first video's spec) |
| Voice + settings | `voice_pin.json` `voice_id` + `voice_settings` (owner decision; change = logged act) |
| STT model | `voice_pin.json` `stt.model_id` (`scribe_v2`, word granularity) |
| Output format | `voice_pin.json` `output_format` (`pcm_24000` on the Creator tier — raw 16-bit PCM, wrapped and normalized to 44.1 kHz by `voiceover.py`; `wav_44100` is Pro-only) |
| Inter-beat gap | `voice_pin.json` `gap_s` (0.75s; pinned — reshuffles the beat map if changed) |
| Keyterms | `voice_pin.json` `keyterms` (channel-vocabulary bias for the ASR) |

```bash
# generate narration (per-beat wavs + master + beat-map + build-log summary)
python3 videos/pipeline/tts/voiceover.py --script videos/<slug>/narration.md --video-dir videos/<slug>
# word timings + soft SRT (from the committed wav)
python3 videos/pipeline/tts/transcribe.py --video-dir videos/<slug>
```

Requires the key as `ELEVENLABS_API_KEY` in the environment, else
`~/.config/elevenlabs/api_key` (file, 0600 — the repo convention: `~/.bashrc`
early-returns for non-interactive shells, so tool invocations read the file).
The key never lands in the repo. TTS is never called inside a render —
the render consumes the committed wav, so re-renders stay deterministic
(VIDEO_CONCEPT §7). Regeneration is a deliberate, logged act (the summary JSON
records script sha256, voice/model/settings, per-beat request-ids, master sha256).

Vendored from [elevenlabs/skills](https://github.com/elevenlabs/skills) (MIT):
`text-to-speech` + `speech-to-text` (+ installation/voice-settings/
transcription-options references), adapted to the per-beat committed-wav model.
**Skipped upstream, by decision:** `music` (standing: no music, VIDEO_CONCEPT §7),
`sound-effects` (standing: no SFX, style spec §4.3), `speech-engine` / `agents` /
realtime-STT refs (live voice conversation — not this workflow), `voice-changer`,
`voice-isolator`, `dubbing` (not in the pipeline), `evals/` + MCP config
(we pin the Python SDK in a venv instead of the CLI). The setup-api-key flow is
folded into the `elevenlabs-tts` skill.

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
