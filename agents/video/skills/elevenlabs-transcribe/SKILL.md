---
name: elevenlabs-transcribe
description: "Use when narration needs word timings or SRT."
version: 1.0.0
author: Preregistered Money
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [video, stt, scribe, timestamps, captions, audio, sync]
    requires_environment_variables: [ELEVENLABS_API_KEY]
    editorial_name: ElevenLabs Transcript (Scribe)
    editorial_description: "Word-level transcript of the committed narration wav: the cue-timestamp backbone for visual beat sync plus the soft-SRT source."
---

# ElevenLabs Transcript (Scribe v2)

Use after the committed narration wav exists: to get word-level timestamps (the sync backbone) and the caption SRT.

## Source of Truth (this repo)

- Glue: `videos/pipeline/tts/transcribe.py` (same venv/pin as `elevenlabs-tts`). Run:
  ```bash
  python3 videos/pipeline/tts/transcribe.py --video-dir videos/<slug>
  ```
- Input is ALWAYS `audio/voiceover.wav` (the committed master). Never an obsolete pre-edit wav, a preview, or the final MP4 (captions skill rule: wording from the script, timing from the committed wav).

## Outputs (`audio/timing/`)

| File | Use |
|---|---|
| `words.json` | verbatim word-level transcript: `[{text, start, end}]` + wav sha256 + model + `transcription_id`. **The scene specs cite cue timestamps from here** — "element appears on the narration word that names it" (style spec §5.1) means: find that word in `words.json`, its `start` is the reveal cue. |
| `captions.srt` | soft captions: one line per phrase chunk (splits on punctuation, pauses ≥0.45s, or 8 words). Consumed by the `captions` skill at publish; committed in the video dir, uploaded soft — never burned in. |
| `transcribe-summary.json` | build-log record: transport version, model, keyterms, `transcription_id`, duration, word/caption counts, wav sha256. Note: the STT endpoint does not set a `request-id` header — `transcription_id` is the audit identifier (it appears in all three files). |

## Keyterms (the channel-vocabulary bias)

`voice_pin.json` `keyterms` biases Scribe toward channel terms (preregistration, scoreboard, OOS, Sharpe, CAGR, …). When the transcript shows a consistent mishearing of a spoken term: add the term to `keyterms` (≤100 terms, ≤5 words each), commit (`docs(pipeline)`), re-run. Do NOT hand-edit `words.json` timings; do NOT accept a wrong word in the SRT — fix the keyterm (or the script wording if the voice mangled it) and regenerate. Wording authority is always the committed `narration.md`; the transcript's `text` is for timing + a sanity check that the wav says what the script says.

## Sync Usage (feeds scene specs)

1. **Scene durations** come from `beat-map.json` (`voiceover.py`) — exact per-beat `start_s`/`end_s` on the master timeline. Each beat's scene renders to its beat duration; the 0.75s gaps are held on the previous scene's final frame (per `audio-sync-assembly` pause handling).
2. **Reveal cues** come from `words.json`: for each element, find the word that names it; cue `start` ±0.1s. Record cues as absolute master-timeline timestamps in the scene spec (style spec: no pre-naming >2s; ≥1 cue per 10s of speech).
3. **Beat boundary QA:** after assembly, `extract_proof_frames.py` at each beat-map `start_s` — the new beat's first frame must be on screen within ~2 frames of the audio boundary.
4. **Drift check:** `probe_media.py` on the assembled master vs `voiceover.wav` duration — mismatch beyond one frame = assembly bug, not a retiming opportunity.

## Rules

- Transcription runs once per committed wav. A new wav (regeneration) → new `words.json` + SRT → affected scene specs retimed → re-QA. Never mix timings across wavs.
- Scribe is not bit-reproducible across runs; the committed `words.json` (with its `transcription_id`) is the record for that wav. A re-run on the same wav can shift word boundaries by milliseconds — regenerate the SRT too and note it in the build log if it changed.
- If `words.json` word count is wildly off vs the script (e.g. Scribe dropped words): check the wav first (listen), then re-run; persistent drops → raise `keyterms` or flag for a re-synthesis with clearer wording.

## Provenance

Adapted from https://github.com/elevenlabs/skills (MIT, Copyright (c) 2024 ElevenLabs): `speech-to-text/SKILL.md` + `speech-to-text/references/transcription-options.md` (batch `scribe_v2`, word granularity, keyterms, srt export). Adapted: single-speaker batch only (diarization/multichannel/realtime skipped — no live audio in this channel), keyterms from the pin, SRT chunking per the `captions` skill rules, build-log summary. Edit this skill freely; keep this section.
