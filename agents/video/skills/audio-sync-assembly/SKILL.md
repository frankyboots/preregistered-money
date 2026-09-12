---
name: audio-sync-assembly
description: "Use when scene renders must sync to committed narration."
version: 1.0.0
author: Preregistered Money
license: Apache-2.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [video, audio, sync, ffmpeg, assembly, timeline]
    editorial_name: Audio Sync Assembly
    editorial_description: "Assembles rendered scenes onto the narration timeline: probe-first, smallest-intervention retiming, hold frames for pauses, segment maps, and timeline manifests."
---

# Audio Sync Assembly

Use this skill when video timing must follow narration or when multiple rendered scenes need to become one final timeline.

## Source Of Truth (this repo)

- The committed TTS wav (`videos/<slug>/audio/voiceover.wav`) is the timing source — it is committed once, so re-renders stay deterministic (VIDEO_CONCEPT §7).
- Scene renders are the visual source.
- Use `videos/pipeline/templates/timeline-manifest.example.json` as the schema for target timing; keep the manifest in the video dir.
- Do not infer timings from old final MP4s if source renders and audio clips exist.

## Probe First

For every clip, use `videos/pipeline/tools/probe_media.py` (or `ffprobe`):

- Duration.
- Frame rate.
- Resolution.
- Audio stream presence.
- Sample rate and channels.

## Sync Strategy

Choose the smallest timing intervention:

- Simple scene: retime whole scene to narration length with `setpts`.
- Scene with cue points: split into segments and retime each segment.
- Narration pause: insert silence and hold a frame.
- Replacement audio slightly longer: use small audio-only `atempo` only if preserving downstream sync matters more than raw duration.
- A visual cue late/early: retime the segment before the cue.

Read `references/ffmpeg-retiming.md` for command patterns.

## Phrase Alignment

Map spoken phrase starts to global timestamps when visuals depend on narration:

- Question cards.
- Data points / chart reveals.
- Scene title reveals.
- Scoreboard / seal / CTA arrival.

Caption timing and visual timing should share the same narration timeline.

## Assembly Order

1. Build synced scene segments.
2. Concatenate synced segments into a narration-only master.
3. Generate captions from the narration-only master (SRT from the committed wav, per the standing decision).
4. Produce final MP4 and preview clips.

(Music bed: standing decision is none — no bed step, no ducking.)

## QA

- Probe final duration, frame rate, resolution, and audio (`videos/pipeline/tools/probe_media.py`).
- Watch boundary previews.
- Check exact cue timestamps with proof frames.
- Listen for clipped words after trims.
- Confirm no accidental blank final frame appears.

## Output

Return:

- Timeline manifest or script updates.
- Final path.
- Scene start map.
- Preview clips.
- Proof frames and probe results.

## Timeline Manifest Fields

Track:

- Scene ID.
- Source render path.
- Source duration.
- Target duration.
- Audio path.
- Audio trim start/end.
- Inserted silence.
- Hold frames.
- Segment retime ratios.
- Global scene start.
- Proof timestamps.

This prevents later caption work from guessing.

## Audio Replacement Rules

When narration changes (a deliberate, logged act — regenerate the committed wav and record voice/model/settings + script hash in the build log):

- Probe old and new durations.
- Decide whether visuals move or audio fits the existing slot.
- If preserving downstream sync, use small audio-only tempo correction when acceptable.
- If phrase timing changes materially, rebuild the segment map.
- Regenerate captions from the new narration master.

## Segment Mapping Heuristics

Split on:

- Scene transitions.
- Data-point reveals.
- Question reveals.
- Chart points.
- Title reveal.
- Final hold.
- Narration pauses.

Avoid splitting on arbitrary equal chunks.

## Pause Handling

For intentional silence:

- Insert silent audio.
- Hold or subtly animate visuals.
- Do not raise any bed during pauses (there is none).
- Preserve global downstream scene starts by accounting for pause duration.

## Preview Clip Strategy

Generate preview clips for:

- Updated narration insertion.
- Data-point timing.
- Question timing.
- Caption timing section.
- Final 10 seconds.
- Any scene boundary changed by the edit.

## Common Mistakes

- Retiming the full video when only one scene changed.
- Letting replacement audio shift all downstream scenes.
- Forgetting caption timings after narration changes.
- Copying stream segments with non-keyframe starts and causing preview oddities.

## Handoff Format

Report:

- Final scene start map.
- Audio files used (with committed-wav checksum).
- Any tempo changes.
- Any inserted pauses.
- Preview paths.
- Final duration.

## Provenance

Adapted from https://github.com/saranambiar/hyperframes-video-agent-skills (Apache-2.0, community project — not an official HyperFrames or HeyGen repository). Music-bed sections removed per the channel's standing "music: none" decision (VIDEO_CONCEPT §7).
