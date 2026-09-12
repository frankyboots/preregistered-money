---
name: elevenlabs-tts
description: "Use when generating or regenerating narration wavs."
version: 1.0.0
author: Preregistered Money
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [video, tts, elevenlabs, narration, audio, voice]
    requires_environment_variables: [ELEVENLABS_API_KEY]
    editorial_name: ElevenLabs Narration (TTS)
    editorial_description: "Per-beat narration synthesis for the channel: pinned voice/model, deterministic master wav, beat map, and the build-log record — with the API-key setup flow."
---

# ElevenLabs Narration (TTS)

Use when a video needs its committed narration wav generated or regenerated, when auditioning voices, or when an ElevenLabs API error surfaces.

## Source of Truth (this repo)

- Glue lives in `videos/pipeline/tts/`: `voiceover.py` (per-beat synthesis), `voice_pin.json` (the pin), `.venv` (gitignored, `requests` pinned by `requirements.lock.txt`), this skill.
- The committed master wav (`videos/<slug>/audio/voiceover.wav`) is the timing source of truth (VIDEO_CONCEPT §7). Renders sync to it via `audio/timing/beat-map.json` and `audio/timing/words.json` (see `elevenlabs-transcribe`).
- `pipeline/README.md` TTS section lists every pinned version the build log must carry.

## API Key (never in chat, never in the repo)

1. Key resolution (the scripts do this; the flow for humans): `ELEVENLABS_API_KEY` in the environment, else `~/.config/elevenlabs/api_key` (file, 0600 — the repo convention, because `~/.bashrc` early-returns for non-interactive shells so its export is invisible to tool invocations). Validate without echoing the key (redact prefix/suffix):
   ```
   curl -s -H "xi-api-key: $(cat ~/.config/elevenlabs/api_key)" https://api.elevenlabs.io/v1/user
   ```
   HTTP 200 → key works; the JSON shows tier + remaining characters.
2. If missing/invalid: point the owner to https://elevenlabs.io/app/settings/api-keys (create key → copy once → write the key line into `~/.config/elevenlabs/api_key`, chmod 600, and keep the `~/.bashrc` export for interactive shells). Ask them to confirm when saved, then re-validate. Never paste keys into chat; never write keys into repo files.
3. **Budget check:** the `/v1/user` `character_count`/`character_limit` tell remaining monthly characters. Rough: ~1,600 chars ≈ 1 min of narration at speed 1.0. A 4-min video ≈ 6.5k chars; re-synthesis during beat iteration costs again. If the tier is low (free), warn before batch auditioning. The Creator tier also constrains output formats (no `wav_44100` — see the pin table).

## Voice Pin (`tts/voice_pin.json`)

| Field | Meaning |
|---|---|
| `voice_id` / `voice_name` | the one channel voice (owner decision). `null` = unpinned; `voiceover.py` refuses to run without it. |
| `model_id` | pinned model (`eleven_v3` per spec; v3 gives emotional range — for this channel we keep it flat, so `style: 0.0`). |
| `voice_settings` | `stability` (higher = steadier/less variance — favor 0.5–0.6 for flat, calm delivery), `similarity_boost`, `style` (0.0 for no exaggeration), `speed` (1.0 default; a deliberate speed change is a logged re-pin), `use_speaker_boost`. |
| `output_format` | `pcm_24000` on the Creator tier (raw 16-bit PCM — the API's lossless option below Pro; `voiceover.py` wraps it and normalizes to 44.1 kHz mono). `wav_44100` is Pro-only — a tier upgrade is an owner decision; any format change is a logged re-pin. |
| `gap_s` | inter-beat silence in the master (pinned; changing it reshuffles every beat-map → logged act). |
| `stt` / `keyterms` | consumed by `transcribe.py` (see `elevenlabs-transcribe`). Keyterms: channel vocabulary the ASR may mangle — add terms when a miss appears. |
| `audition_candidates` | voice IDs + labels for auditions. |

Changing the pin is a **deliberate, logged act**: edit `voice_pin.json`, commit as `docs(pipeline)`, and the next regeneration records the new pin in its summary. A changed pin means every previously committed wav in the channel will drift if regenerated — regenerate is never silent.

## Auditioning a Voice (first time, or re-choosing)

```bash
# one ~15s sample per candidate, from repo root
for v in $(python3 -c "import json;print(' '.join(json.load(open('videos/pipeline/tts/voice_pin.json'))['audition_candidates']))"); do
  python3 videos/pipeline/tts/voiceover.py --script /tmp/audition.md --video-dir /tmp/audition-$v --voice-id $v
  ffmpeg -i /tmp/audition-$v/audio/voiceover.wav -c:a libmp3lame -b:a 192k /tmp/audition-$v/audio/audition.mp3
  cp /tmp/audition-$v/audio/voiceover.wav /tmp/audition-$v/audio/$v.wav   # wav copy is the auditable artifact
done
```

- `/tmp/audition.md` = a single `## beat-01` with the actual opening narration lines (never audition on sample prose that isn't in the script).
- Deliver the wavs to the owner (TUI: state absolute paths). They pick; the pick goes into `voice_pin.json` + commit.
- Audition wavs/mp3s stay out of the repo (not part of the record; the pin + summary in the first real voiceover are). The one exception: first-time audition mp3s may live briefly in `videos/<slug>/audio/auditions/` (gitignored) for owner review.

## Generating the Narration

1. **Script first:** `videos/<slug>/narration.md` — one `## beat-NN` heading per spec beat, narration text under each heading, in spec order. The script is the caption wording source too (captions skill). Any number that appears spoken must be one cited in the spec (or an on-screen-and-spoken labeled example).
2. **Run:**
   ```bash
   python3 videos/pipeline/tts/voiceover.py --script videos/<slug>/narration.md --video-dir videos/<slug>
   ```
   (Transport: REST v1 via `requests` from `tts/.venv` — the script bootstraps the venv site-packages itself when the system site lacks `requests`. No SDK dependency; the raw headers are the audit data.)
3. **Output:** `audio/beats/beat-NN.wav` (44.1 kHz mono normalized from the pinned raw format), `audio/voiceover.wav` (concatenated, pinned `gap_s` between beats), `audio/timing/beat-map.json` (exact per-beat global start/end from ffprobe — scene durations for the sync pass), `audio/timing/voiceover-summary.json` (build-log record: transport version, voice, model, settings, per-beat chars + request-id + duration, script sha256, master sha256 + duration).
4. **Listen before syncing** (it's the only human QC the channel does on audio): delivery flat and calm, no artifacts, no mispronunciations. Fix = edit the script (wording), re-run (logged), or a pin change (logged). Re-running one beat requires regenerating the whole master — acceptable (cheap, logged); do NOT hand-splice the master wav.
5. **Then transcribe:** `transcribe.py` (see `elevenlabs-transcribe`) → `words.json` + `captions.srt`. Beat map + words = the locked timing the scene specs cite.
6. **Commit** (one coherent `video(video-<slug>)` commit: narration.md + audio/ + updated spec if durations moved + build log entry with the summary's fields).

## Determinism Rules

- The render consumes the committed wav — TTS is never called inside a render (VIDEO_CONCEPT §7). Same committed wav → same pixels.
- ElevenLabs TTS is **not** bit-reproducible across requests even with identical inputs; that is why the wav is committed once and re-synthesis is a logged act, not an accident. The summary's `script_sha256` + pin + request-ids are the audit record of what produced the committed wav.
- Regeneration policy: any narration wording change → full re-run → new beat-map → affected scene specs retimed (smallest intervention per `audio-sync-assembly`) → `transcribe.py` again → SRT again.

## Failure Handling

- **401** — key invalid/expired → re-validate flow above.
- **403 `subscription_required`** — tier lacks the requested output format (e.g. `wav_44100` on Creator) → use the tier-appropriate pinned format; a tier upgrade is an owner decision, not drift.
- **422** — bad voice/model id or settings → check the pin against `GET /v1/voices` and the model table in this skill's provenance refs.
- **429** — rate limit → back off and retry once; if it persists, check the tier's RPM in the dashboard.
- `requests` missing (fresh clone) → `uv venv videos/pipeline/tts/.venv && uv pip install --python videos/pipeline/tts/.venv/bin/python -r videos/pipeline/tts/requirements.lock.txt`.

## Provenance

Adapted from https://github.com/elevenlabs/skills (MIT, Copyright (c) 2024 ElevenLabs): `text-to-speech/SKILL.md`, `text-to-speech/references/{installation,voice-settings}.md`, `setup-api-key/SKILL.md`. Adapted to this repo: per-beat markdown-script synthesis, `voice_pin.json` pin, committed-wav timing model, beat-map emission, build-log summary, budget check, REST-v1 transport for header audit data. Real-time/streaming sections skipped (not in the pipeline); music/sound-effects/voice-changer/dubbing skills skipped per standing decisions. Edit this skill freely; keep this section.
