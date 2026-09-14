# Full-frame vectorized sweep (onset, negatives, hold)

Use when the QA checklist asks for frame-exact proof — "first lit frame = cue frame", pre-naming negatives across many elements, or hold stability over hundreds of frames. Never loop over pixels in pure Python per frame; dump the whole MP4 once and work in numpy (a pure-Python per-pixel loop over hundreds of full-res frames OOMs the execution kernel mid-sweep). Interpreter: the analysis host's bare `python3` usually lacks numpy/PIL — run the sweep script with `uv run --with numpy --with pillow python3` (first use installs into the uv cache in seconds); the same pattern works for PIL-based geometry probes on proof PNGs.

## 1. Decode once

```bash
ffmpeg -y -loglevel error -i renders/scene-NN.mp4 -f rawvideo -pix_fmt rgb24 /tmp/sNN.rgb
ls -la /tmp/sNN.rgb   # expect N × 1080 × 1920 × 3 bytes
```

N = frame count (duration × fps; a 33.49s @24fps scene has 804 frames). The dump is multi-GB — delete it (and any sweep dirs) when done.

## 2. Load and zone

```python
import numpy as np, hashlib
N = 1042  # = filesize / (1080*1920*3)
raw = np.memmap("/tmp/sNN.rgb", dtype=np.uint8, mode="r", shape=(N, 1080, 1920, 3))

# zone: (x1, y1, x2, y2, cue_local) — slice per zone, never materialize the
# whole (N, 1080, 1920) luminance array: raw.max(axis=3) allocates ~2.2GB
# for a 1000-frame dump and OOMs the analysis kernel mid-sweep.
for x1, y1, x2, y2, cue in zones:
    z = raw[:, y1:y2, x1:x2].max(axis=3)      # (N, zy, zx) — small
    lit = (z > TH).sum(axis=(1, 2))           # lit px per frame in the zone
    nz = np.nonzero(lit >= 3)[0]
    first_frame = nz[0] + 1                   # 1-indexed; frame == floor(t × fps) + 1
    cue_frame = int(cue * fps) + 1
```

Rule per zone: nothing lit before the cue frame (hard bar); first lit at cue frame +0/+1, or within a few frames (the front-loaded `--ease-out` curve delays first visible frame slightly; the bar is never-visible-before-cue, not at-cue-visible). If a zone is contaminated by a pre-existing element (a gridline row, another series crossing the zone), split the zone or raise TH past that element's luminance — otherwise the zone "lights" at the wrong frame. **A reveal sweep of one element contaminates its neighbors' zones**: a left-to-right clip wipe of a table sweeps its dim cell rules through every row band it passes, so a per-row zone reads a first-lit frame at the wipe start, not the row's cue. Clear each zone's band of the full-width/dim rule rows (measure the rule rows on a settled frame first) and/or raise TH past the dim token — then re-check the zone's pixel count at cue−1 (must be 0) before trusting the onset.

When unsure which frames are real content, print the per-frame lit-pixel counts around the suspect window: a one-frame blip that decays is a passing sweep artifact; a step to a stable count is the real onset.

## 3. Thresholds are per-token, after yuv420p

Calibrate to the rendered token, not the CSS value — yuv420p 4:2:0 decode shifts levels, and a 1px line straddling two sample rows reads dimmer than the token's nominal value:

- bright paper/ink fills: peak ≈ 232–255 — any TH 100–150 works
- mid dim (≈40–50% opacity paper): ≈ 58–70 depending on row — TH 80 excludes it; TH 50 includes it
- full-opacity `--paper-dim` TEXT (e.g. a supporting line in `--paper-dim` on `--ink`): peak ≈ 141 (the ink field decodes at ≈11–16 — ~10× contrast) — TH 40 captures it with margin; do NOT apply the 1px-line threshold (below) to dim text — they are different elements at different levels. Measure the settled peak on a final frame and set the threshold from the measured level, never from the CSS value.
- 35%-dim cell rules (`.ledger` set piece): peak ≈ 49 — TH 60 separates them from the 255 cell text, so per-cell text zones can be swept cleanly without clearing the rule rows first
- 1px `--paper-dim` frame/axis lines: 60–70 max even when fully drawn — never assert them with a high threshold; verify at a settled frame instead, with tolerance for the row they land on

When unsure, trace a zone's pixel count per frame around the expected cue — the step from 0 to the settled count is the real onset, and its level is the element's rendered luminance.

## 4. Hold verification

```python
hs = [hashlib.sha256(raw[i].tobytes()).hexdigest() for i in range(first_hold_frame, N)]
set(hs)  # one hash = byte-identical plateau
```

If two plateau blocks differ, diff them element-wise (`(a != b).any(axis=2)`), take the bbox and max channel diff, and judge: a few hundred px, max diff ≲10/255, confined to a text AA edge → codec micro-block, record bbox + max diff in the build log, passes. Anything wider or brighter → real motion, fails, fix the timeline.
