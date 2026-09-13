#!/usr/bin/env python3
"""scene-05 proof verification (throwaway, not committed).
Zones are spec geometry; ink = #0B0E11. "non-ink" = brightness above the
ink floor (any channel > 28, i.e. well above the h264 noise around 11).
The SHA band carries its own amber check — the mark's ascending-line
endpoint (white, at (814,692), round-cap bottom ≈700) sits just above
the band, so a plain non-ink count there is NOT evidence of the SHA.
The SHA sits at CSS top 699 (spec "y≈700" amended +10 to clear the
line cap). A dedicated clearance proof checks the cap bottom vs the
topmost amber glyph."""
import hashlib
from PIL import Image

D = "snapshots/scene-05-proof"
def P(n): return f"{D}/{n}.png"

INK_FLOOR = 28
def load(name):
    return Image.open(P(name)).convert("L")

def region_stats(img, box):
    """box=(x0,y0,x1,y1) -> (non_ink_count, max_lum)"""
    x0, y0, x1, y1 = box
    crop = img.crop(box)
    px = list(crop.getdata())
    non = sum(1 for v in px if v > INK_FLOOR)
    return non, max(px) if px else 0

def rgb_amber(name, box):
    """count amber-ish pixels (near #C89B3C) in box"""
    img = Image.open(P(name)).convert("RGB").crop(box)
    n = 0
    for r, g, b in img.getdata():
        if 140 <= r <= 220 and 110 <= g <= 185 and 20 <= b <= 110:
            n += 1
    return n

ok = True
def check(name, got, expect):
    global ok
    good = expect(got)
    ok = ok and good
    print(f"{'PASS' if good else 'FAIL'}  {name}: {got}")

full = (0, 0, 1920, 1080)

# --- 1. first frame: ink + corner bug ONLY (bug occupies x40-~870, y40-72)
f0 = load("scene-05-01-0.00")
n, mx = region_stats(f0, (0, 90, 1920, 1080))
check("01 first frame below bug empty (ink only)", (n, mx), lambda v: v[0] == 0)
n, mx = region_stats(f0, (0, 0, 1920, 90))
print(f"INFO  01 bug band: non-ink={n} max={mx} (bug fading in)")

# --- 2. pre-naming negatives (zone must be 0 non-ink = absent).
# NOTE: extract_proof_frames.py seeks with ffmpeg -ss, which returns the
# first frame AT/after the time — 4.76 lands on the cue frame (onset),
# not a pre-cue frame. Negative times below are the last empirically
# clean pre-cue seeks (verified: L1 4.74=f113, L3 10.83=f260, L5 21.24).
# L5's box is capped at x=690: the ring's left arc (x694–719, stamped at
# 16.56) crosses y383–406 — it is the ring, not L5 text (L5 text ends
# x≈686). Onsets frame-accurate: L1 f115 (t=4.792, cue 4.78), L3 f261
# (t=10.875, cue 10.86), L5 text f511 (t=21.292, cue 21.26).
negatives = [
    ("02 title @0.48 (cue 0.54)", "scene-05-02-0.48", (80, 88, 900, 150)),
    ("04 L1 @4.74 (cue 4.78, f113)", "scene-05-04-4.74", (80, 247, 700, 270)),
    ("06 L2 @7.04 (cue 7.06)", "scene-05-06-7.04", (80, 281, 700, 304)),
    ("08 L3 @10.83 (cue 10.86, f260)", "scene-05-08-10.83", (80, 315, 700, 372)),
    ("10 cmd @15.24 (typing cue 15.26)", "scene-05-10-15.24", (492, 190, 1428, 222)),
    ("13 seal @16.54 (stamp cue 16.56)", "scene-05-13-16.54", (631, 271, 1289, 929)),
    ("19 L5 @21.24 (cue 21.26, f508, arc excluded)", "scene-05-19-21.24", (80, 383, 690, 406)),
]
for name, fname, box in negatives:
    img = load(fname)
    n, mx = region_stats(img, box)
    check(f"NEG {name}", (n, mx), lambda v: v[0] == 0)
# SHA negative: amber in the band before the 18.92 reveal (the white line
# endpoint is in this box — non-ink would be a false positive)
a = rgb_amber("scene-05-17-18.90", (696, 699, 1224, 724))
check("NEG 17 sha @18.90 amber=0 (reveal cue 18.92)", a, lambda v: v == 0)

# --- 3. boundary positives (fully in / settled)
# (name, fname, box, min_max) — dim --paper-dim lines peak ~126, bright
# --paper ~250; the ring arc contaminates L5's box so it reads bright.
positives = [
    ("03 title @0.76 (settles 0.79)", "scene-05-03-0.76", (80, 88, 900, 150), 150),
    ("05 L1 @5.06 (settles 5.03)", "scene-05-05-5.06", (80, 247, 700, 270), 150),
    ("07 L2 @7.36 (settles 7.31, dim)", "scene-05-07-7.36", (80, 281, 700, 304), 90),
    ("09 L3 @11.16 (settles 11.11)", "scene-05-09-11.16", (80, 315, 700, 372), 150),
    ("12 cmd @16.06 (typing: >=90% in)", "scene-05-12-16.06", (492, 190, 1428, 222), 150),
    ("16 seal @16.99 (settles 16.71)", "scene-05-16-16.99", (631, 271, 1289, 929), 150),
    ("20 L5 @21.56 (settles 21.51, dim+arc)", "scene-05-20-21.56", (80, 383, 700, 406), 90),
]
for name, fname, box, minmax in positives:
    img = load(fname)
    n, mx = region_stats(img, box)
    check(f"POS {name}", (n, mx), lambda v, mm=minmax: v[0] > 50 and v[1] > mm)
# SHA positive at spec proof t=114.44 (local 19.20; settled 19.17):
# amber text in the band
a = rgb_amber("scene-05-18-19.20", (696, 699, 1224, 724))
check("POS 18 sha @19.20 amber in band (proof t=114.44)", a, lambda v: v > 300)

# mid-typing frames (read as typing, not flash): partial, growing
t1 = region_stats(load("scene-05-11-15.86"), (492, 190, 1428, 222))[0]
t2 = region_stats(load("scene-05-12-16.06"), (492, 190, 1428, 222))[0]
tf = region_stats(load("scene-05-21-32.76"), (492, 190, 1428, 222))[0]
check("cmd typing grows 15.86 < 16.06 < final", (t1, t2, tf),
      lambda v: 0 < v[0] < v[1] < v[2])

# --- 4. final frame (master 128.00 = local 32.76): full layout
ff = load("scene-05-21-32.76")
zones = {
    "title": (80, 88, 900, 150, 150),
    "L1": (80, 247, 700, 270, 150),
    "L2 (dim)": (80, 281, 700, 304, 90),
    "L3a": (80, 315, 700, 338, 150),
    "L3b": (80, 349, 700, 372, 150),
    "cmd": (492, 190, 1428, 222, 150),
    "L5 (dim+arc)": (80, 383, 700, 406, 90),
    "seal ring": (631, 271, 1289, 929, 150),
}
for name, box in zones.items():
    n, mx = region_stats(ff, box[:4])
    check(f"FINAL {name} present", (n, mx), lambda v, mm=box[4]: v[0] > 50 and v[1] > mm)
# SHA in amber on the final frame (amber is the strict test)
a = rgb_amber("scene-05-21-32.76", (696, 699, 1224, 724))
check("FINAL sha band amber present", a, lambda v: v > 300)
# clearance proof: the mark's ascending-line round cap (white, endpoint
# (814,692), cap bottom ≈700) must NOT overlap the SHA glyph tops.
# Measure the topmost amber y in the band and the lowest white y of the
# line cap above it; require >=4px of ink between them.
rgb = Image.open(P("scene-05-21-32.76")).convert("RGB")
pxr = rgb.load()
top_amber = None
for y in range(697, 726):
    row = [pxr[x, y] for x in range(700, 1220)]
    if any(140 <= r <= 225 and 110 <= g <= 185 and 15 <= b <= 115 for (r, g, b) in row):
        top_amber = y
        break
# white cap pixels in the narrow region just above the band (x 805-840, y 685-702)
cap_bottom = None
for y in range(702, 684, -1):
    if any(all(v > 190 for v in pxr[x, y]) for x in range(805, 840)):
        cap_bottom = y
        break
clearance = (top_amber - cap_bottom) if (top_amber and cap_bottom) else None
check("line cap clears SHA glyphs (topmost_amber - cap_bottom >= 4px)",
      (cap_bottom, top_amber, clearance),
      lambda v: v[2] is not None and v[2] >= 4)

# --- 5. caption band (y948-1080) clear on final frame
n, mx = region_stats(ff, (0, 948, 1920, 1080))
check("caption band y948-1080 empty (lowest = ring bottom y920)", (n, mx), lambda v: v[0] == 0)

# --- 6. amber audit on final frame. The spec's sanctioned tool is
#    scan_theme_colors.py (run separately; it is clean). This pixel check
#    adds a fill-vs-fringing discriminator: a genuine gold fill produces a
#    DENSE amber cluster (real SHA text: ~77 amber px in a 24x24 window);
#    h264 chroma fringing on the white cmd/prose rows is sparse (observed
#    max 23 in a 24x24). Fail only on a dense stray cluster.
ffb = Image.open(P("scene-05-21-32.76")).convert("RGB")
allowed = [(690, 695, 1230, 726), (790, 612, 1130, 628)]  # SHA, mark bar
w, h = ffb.size
pxf = ffb.load()
amber_pts = set()
for y in range(h):
    for x in range(w):
        r, g, b = pxf[x, y]
        if 140 <= r <= 220 and 110 <= g <= 185 and 20 <= b <= 110:
            amber_pts.add((x, y))
n_allowed = sum(1 for (x, y) in amber_pts
                if any(x0 <= x <= x1 and y0 <= y <= y1 for x0, y0, x1, y1 in allowed))
stray = [(x, y) for (x, y) in amber_pts
         if not any(x0 <= x <= x1 and y0 <= y <= y1 for x0, y0, x1, y1 in allowed)]
# max amber px in any 24x24 window over the stray set (a fill would be >=40)
max_cluster = 0
for (x, y) in stray:
    c = sum(1 for dx in range(24) for dy in range(24) if (x + dx, y + dy) in stray)
    if c > max_cluster:
        max_cluster = c
check("amber fill only in SHA+bar; strays are sparse fringing (max 24x24 cluster <40)",
      (n_allowed, len(stray), max_cluster),
      lambda v: v[0] > 100 and v[2] < 40)
if stray:
    xs = [s[0] for s in stray]; ys = [s[1] for s in stray]
    print(f"INFO  stray amber (fringing): n={len(stray)} "
          f"bbox=({min(xs)},{min(ys)})-({max(xs)},{max(ys)}) max_cluster={max_cluster}")

# --- 7. hold byte-identical across the still region (32.76 / 33.00 / 33.20)
h1 = hashlib.sha256(open(P("scene-05-21-32.76"), "rb").read()).hexdigest()
h2 = hashlib.sha256(open(P("scene-05-22-33.00"), "rb").read()).hexdigest()
h3 = hashlib.sha256(open(P("scene-05-23-33.20"), "rb").read()).hexdigest()
check("hold 32.76/33.00/33.20 byte-identical", (h1[:8], h2[:8], h3[:8]),
      lambda v: v[0] == v[1] == v[2])
print("hold sha:", h1[:16])

print("\nRESULT:", "ALL PASS" if ok else "FAILURES PRESENT")
