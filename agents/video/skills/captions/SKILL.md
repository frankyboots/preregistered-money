---
name: captions
description: "Use when captions are requested, late, or need restyling."
version: 1.0.0
author: Preregistered Money
license: Apache-2.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [video, captions, srt, subtitles, timing]
    editorial_name: Captions
    editorial_description: "Caption timing and wording discipline for the channel: SRT generated from the committed voiceover wav, first-word timing, phrase chunking, and proof checks."
---

# Captions

Use this skill after the narration timeline is stable.

## Delivery Model (this repo)

Standing decision (VIDEO_CONCEPT §11): captions are **soft SRT**, auto-generated from the committed voiceover wav (`videos/<slug>/audio/voiceover.wav`), committed in the video dir, and uploaded with the video — not burned in. The generation step (whisper model/version or equivalent, pinned in the pipeline, settings recorded in the build log) lives in `videos/pipeline/`. If the standing decision changes to burn-in, use ASS via `ffmpeg -vf subtitles=` and keep the style conservative (see the timing rules below, which apply to both).

## Caption Source Rules

- Wording source: the narration script that produced the committed wav — keep it in the video dir with the wav.
- Timing source: the final narration-only master / committed wav. Never time captions from an obsolete pre-edit audio file.
- Preserve punctuation and capitalization.
- Show one caption line at a time.
- Start the caption when the first word is spoken.
- Avoid captions over silent hooks or silent CTA holds unless requested.

## Chunking Rules

Split captions by:

- Natural phrase boundaries.
- Breath points.
- Punctuation.
- Maximum line length.

Do not split in a way that changes meaning. Do not add punctuation that the script does not contain.

## Timing Sources

Preferred order:

1. Word-level alignment from the committed wav.
2. Phrase timestamps from user or transcript.
3. Scene-level known timings plus manual phrase estimates.

## Preview Before Upload

For any timing or wording doubt:

- Extract the relevant frame with `videos/pipeline/tools/extract_proof_frames.py`.
- Confirm the caption line is the one spoken at that timestamp (SRT preview in a player, or overlay a test render).
- Adjust chunk boundaries, then regenerate the SRT from the wav.

## QA

- Check captions begin on the first spoken word, not several words late.
- Check the final narrated line ends with the audio.
- Check no captions during silent sections (unless requested).
- Spot-check: first narration line, questions, scene title reveal, final narrated line.

## Failure Recovery

If captions are late:

- Check the alignment source (must be the committed wav / final master).
- Check whether silence or a hold shifted global times.
- Start chunks at the first word, not the middle of the phrase.
- Regenerate from the committed wav.

If a caption is wrong:

- If wording is wrong: the script or the TTS step drifted — fix the source, regenerate the wav (logged), regenerate the SRT.
- If timing is wrong: re-align from the wav, do not hand-shift timestamps.

## Output

Return:

- Caption source script.
- Caption timing source (wav checksum).
- SRT file path.
- Checks performed.

## Provenance

Adapted from the caption half of `captions-and-music-bed` in https://github.com/saranambiar/hyperframes-video-agent-skills (Apache-2.0, community project — not an official HyperFrames or HeyGen repository). Music-bed sections removed per the channel's standing "music: none" decision (VIDEO_CONCEPT §7); ASS burn-in template deferred until the delivery decision changes.
