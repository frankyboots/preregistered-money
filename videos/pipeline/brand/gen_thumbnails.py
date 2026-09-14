#!/usr/bin/env python3
"""Pinned thumbnail generator — the two approved looks (owner decision 2026-09-14).

This is the source of truth for every video's thumbnail. Re-running it must
reproduce the published pixels. Concepts that were explored but not approved
live in gen_thumbnails.py (round 1: A/B/C) and gen_thumbnails2.py (round 2:
C2/D/E).

The two looks — both data-forward, no hype, palette-only:
  C2 "verdict chart" — full-bleed chart: thick paper curve vs the amber
     pre-registered bar, a huge verdict-colored number top-right, the brand
     mark stamped top-left. For VERDICT videos (the hero is the number).
  E  "the seal, stamped" — the brand mark stamped big on the left, the full
     spec-commit SHA in amber aligned to the ring's outer edges below it,
     and the tagline (meta) or verdict word + number (pre-verdict) in the
     open space to the right. For META / pre-verdict episodes (the hero is
     the seal — a meta video has no number, a chart would be a lie).
  Both share the chassis: 12px-inset dim border, series tag top-left,
  wordmark bottom-right.

Constraints (style spec v1.1.0):
  - palette: only the 7 tokens (CI: tools/scan_theme_colors.py, --allow all 7)
  - fonts: Inter + JetBrains Mono (vendored WOFF2 in videos/pipeline/fonts/)
  - 1280x720; type = the 1080p scale x 2/3
  - numbers: same trace rule as the video — every figure must exist in a
    published results doc (or the seal SHA from the video's own
    data/spec-sha.txt). Never computed here.

Render (headless chrome, pixel-exact):
  google-chrome-stable --headless=new --no-sandbox --disable-gpu \
    --hide-scrollbars --force-device-scale-factor=1 --virtual-time-budget=6000 \
    --window-size=1280,720 --screenshot=<out>.png file://<in>.html

Usage (emit one video's thumbnail):
  python3 gen_thumbnails.py <slug> <meta|pre-verdict> [series_tag] [hero] \
      [subline] [spec_sha]
  e.g. python3 gen_thumbnails.py meta-preregistration-rules meta
Writes <slug>/thumbnail.html and prints it; the render step (video-commit
procedure) writes <slug>/thumbnail.png into the video's renders dir.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_REL = "../../../fonts"  # brand/ -> pipeline/fonts/

FACES = """
@font-face{{font-family:"Inter";src:url("{f}/Inter-Regular.woff2") format("woff2");font-weight:400;}}
@font-face{{font-family:"Inter";src:url("{f}/Inter-SemiBold.woff2") format("woff2");font-weight:600;}}
@font-face{{font-family:"Inter";src:url("{f}/Inter-Bold.woff2") format("woff2");font-weight:700;}}
@font-face{{font-family:"JetBrains Mono";src:url("{f}/JetBrainsMono-Regular.woff2") format("woff2");font-weight:400;}}
@font-face{{font-family:"JetBrains Mono";src:url("{f}/JetBrainsMono-Medium.woff2") format("woff2");font-weight:500;}}
"""

INK, PAPER, DIM, AMBER, CONF, FALS, INCON = (
    "#0B0E11", "#E8E6E1", "#6B7078", "#C89B3C", "#3FA46A", "#C4453C", "#8A9099")

W, H = 1280, 720
BORDER = 12
TAG_FS = 18
WM_Y = 662
WM_FS = 18
NAME = "PREREGISTERED MONEY"

VERDICT_COLORS = {"confirmed": CONF, "falsified": FALS, "inconclusive": INCON}


def seal_mark_w(h):
    """Brand mark (style/brand-mark.svg, viewBox 0 0 800 800) at width h."""
    return f'''
<svg width="{h}" height="{h}" viewBox="0 0 800 800" style="display:block;">
  <circle cx="400" cy="400" r="330" fill="none" stroke="{PAPER}" stroke-width="18"/>
  <circle cx="400" cy="400" r="282" fill="none" stroke="{PAPER}" stroke-width="4"/>
  <line x1="230" y1="420" x2="570" y2="420" stroke="{AMBER}" stroke-width="7"/>
  <polyline points="250,495 385,410 550,295" fill="none" stroke="{PAPER}"
            stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/>
</svg>'''


def base_css():
    return f"""
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:{W}px;height:{H}px;background:{INK};overflow:hidden;
     font-family:"Inter",-apple-system,sans-serif;}}
.mono{{font-family:"JetBrains Mono",ui-monospace,monospace;
     font-variant-numeric:tabular-nums;}}
"""


def page(body):
    css = base_css() + FACES.format(f=FONT_REL)
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head>
<body>{body}</body></html>'''


def tag(text, x=40, y=32):
    return (f'<div class="mono" style="position:absolute;left:{x}px;top:{y}px;'
            f'font-size:{TAG_FS}px;letter-spacing:2px;color:{DIM};'
            f'white-space:nowrap;">{text}</div>')


def wordmark():
    return (f'<div class="mono" style="position:absolute;right:44px;top:{WM_Y}px;'
            f'font-size:{WM_FS}px;letter-spacing:2px;color:{DIM};'
            f'text-align:right;white-space:nowrap;">{NAME}</div>')


def border_box():
    return (f'<div style="position:absolute;left:{BORDER}px;top:{BORDER}px;'
            f'right:{BORDER}px;bottom:{BORDER}px;border:2px solid {DIM};"></div>')


# ---------------------------------------------------------------- C2 look -----
# Curve data is illustrative SHAPE ONLY (the verdict read is relative to the
# bar); the bar tag text and the number come from the video's prereg/results.
CURVE = {
    "confirmed": "60,430 190,398 330,344 470,236 590,150 720,96",
    "falsified": "60,430 190,404 330,372 470,344 590,352 720,392",
    "inconclusive": "60,430 190,404 330,372 470,344 590,352 720,392",
}


def look_c2(tag_text, kind, hero, subline, bar_tag):
    """Verdict chart: full-bleed chart + huge verdict-colored number + seal."""
    col = VERDICT_COLORS[kind]
    grid = "".join(
        f'<line x1="60" y1="{y}" x2="720" y2="{y}" stroke="{DIM}" stroke-width="1" opacity="0.35"/>'
        for y in (130, 240, 350))
    chart = f'''
<svg width="780" height="470" viewBox="0 0 780 470" style="position:absolute;left:44px;top:200px;display:block;">
  {grid}
  <line x1="60" y1="24"  x2="60"  y2="440" stroke="{DIM}" stroke-width="4"/>
  <line x1="60" y1="440" x2="740" y2="440" stroke="{DIM}" stroke-width="4"/>
  <line x1="60" y1="250" x2="740" y2="250" stroke="{AMBER}" stroke-width="8"/>
  <text x="736" y="238" text-anchor="end" font-family="JetBrains Mono"
        font-size="22" fill="{AMBER}">{bar_tag}</text>
  <polyline points="{CURVE[kind]}" fill="none" stroke="{PAPER}" stroke-width="12"
            stroke-linejoin="round" stroke-linecap="round"/>
</svg>'''
    seal = f'<div style="position:absolute;left:44px;top:44px;width:132px;height:132px;">{seal_mark_w(132)}</div>'
    num = (f'<div style="position:absolute;right:44px;top:52px;text-align:right;'
           f'font-size:150px;font-weight:700;color:{col};white-space:nowrap;">{hero}</div>')
    sub = (f'<div class="mono" style="position:absolute;right:44px;top:214px;'
           f'text-align:right;font-size:30px;color:{PAPER};white-space:nowrap;">{subline}</div>')
    return border_box() + tag(tag_text, x=204, y=92) + seal + chart + num + sub + wordmark()


# ---------------------------------------------------------------- E look ------
def look_e(tag_text, spec_sha, right_html):
    """The seal, stamped big. right_html fills the open space to the right:
    the tagline (meta) or the verdict word + number (pre-verdict)."""
    big = f'<div style="position:absolute;left:120px;top:120px;width:440px;height:440px;">{seal_mark_w(440)}</div>'
    # Full 40-char spec-commit SHA, 12px mono +0.1px tracking = ~367px ink;
    # set to the ring's outer width (154..526) so its edges align with the
    # stamp ring's edges. Verify by pixel scan on every render (amber line
    # x-extent vs ring outer x-extent, tolerance ~3px) — never trust font math.
    sha = (f'<div class="mono" style="position:absolute;left:154px;top:584px;'
           f'width:372px;text-align:center;font-size:12px;color:{AMBER};'
           f'letter-spacing:0.1px;white-space:nowrap;">'
           f'git commit {spec_sha}</div>')
    return border_box() + tag(tag_text) + big + sha + right_html + wordmark()


def right_meta(subline):
    """Meta: tagline centered in the right region, vertically centered on
    the seal (seal center y=340)."""
    return (f'<div class="mono" style="position:absolute;left:560px;right:44px;'
            f'top:325px;text-align:center;font-size:30px;color:{PAPER};'
            f'white-space:nowrap;">{subline}</div>')


def right_verdict(kind, hero):
    """Pre-verdict: big verdict word in the verdict color + the number below."""
    col = VERDICT_COLORS[kind]
    word = kind.upper()
    num = (f'<div class="mono" style="position:absolute;right:44px;top:400px;'
           f'text-align:right;font-size:34px;color:{PAPER};white-space:nowrap;">{hero}</div>' if hero else "")
    return (f'<div style="position:absolute;right:44px;top:280px;text-align:right;'
            f'font-size:96px;font-weight:700;color:{col};white-space:nowrap;">{word}</div>'
            + num)


# ---------------------------------------------------------------- emit --------
def emit(slug, mode, tag_text, hero, subline, spec_sha, bar_tag="bar: ≥ 6.0% OOS",
         kind="confirmed"):
    """Write <slug>/thumbnail.html into the video dir and return its path.

    mode: "meta" (E look, tagline right) | "pre-verdict" (E look, verdict
          word right) | "verdict:<kind>" (C2 look; kind in VERDICT_COLORS).
    """
    outdir = os.path.join(HERE, "..", "..", slug)
    os.makedirs(outdir, exist_ok=True)
    if mode == "meta":
        body = look_e(tag_text, spec_sha, right_meta(subline))
    elif mode == "pre-verdict":
        body = look_e(tag_text, spec_sha, right_verdict(kind, hero))
    elif mode.startswith("verdict:"):
        body = look_c2(tag_text, mode.split(":", 1)[1], hero, subline, bar_tag)
    else:
        raise SystemExit(f"unknown mode {mode!r}")
    path = os.path.normpath(os.path.join(outdir, "thumbnail.html"))
    with open(path, "w") as fh:
        fh.write(page(body))
    return path


if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise SystemExit(__doc__.split("Usage (emit one video's thumbnail):")[-1])
    slug, mode = sys.argv[1], sys.argv[2]
    tag_text = sys.argv[3] if len(sys.argv) > 3 else "META"
    hero = sys.argv[4] if len(sys.argv) > 4 else ""
    subline = sys.argv[5] if len(sys.argv) > 5 else ""
    spec_sha = sys.argv[6] if len(sys.argv) > 6 else ""
    print(emit(slug, mode, tag_text, hero, subline, spec_sha))
