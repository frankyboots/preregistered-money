# Video QA Failure Modes

## Visual

- Scene starts from an old carryover frame.
- A new chart label exists in one scene but disappears in the next.
- Theme changes miss inline SVG `fill` or `stroke` values.
- Final frame is blank because a render segment had dead time.
- Caption overlay (if ever burned) covers important chart labels.

## Audio

- Replacement narration shifts downstream sync.
- Audio is technically present but too quiet to hear.
- Final silence or fade timing is off.
- Words are clipped by aggressive trims.

## Captions

- Captions start several words late.
- Caption chunks invent punctuation not in the script.
- Captions wrap to two lines where one fits.
- Silent hooks or CTA screens get unwanted captions.

## Determinism (this repo)

- Re-render of the committed video dir does not match the published pixels.
- Build log missing a version pin (template, style spec, TTS voice/model, encoder) that the render actually used.
- A data input changed without a checksum update in the build log.
- A number on screen that is not in the cited results doc.

## Regression Checks

- Probe final file before and after (`videos/pipeline/tools/probe_media.py`).
- Extract exact timestamp proof frames.
- Compare boundary frames around changed scenes.
- Search all scene files for changed labels and stale colors.
- Keep generated proof outputs outside version control unless they are public examples.
