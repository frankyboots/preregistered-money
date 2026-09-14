#!/usr/bin/env python3
"""Thumbnail-look concepts, round 2 — richer, click-earning directions.

Round 1 (A centered / B ledger-row / C small chart) was read as "too minimal."
Round 2 makes a REAL set piece the dominant object filling the frame:
  C2 — full-bleed verdict chart + a certification seal stamp (data + proof)
  D  — the scoreboard ledger filling the frame (the channel's product)
  E  — the seal, stamped big (the signature moment)

Same constraints as round 1 (style spec v1.1.0):
  - palette: only the 7 tokens; fonts Inter + JetBrains Mono (vendored)
  - 1280x720; type = 1080p scale x 2/3
  - samples: the real one is video 1 (series META, the seal); numbers are
    labeled examples in the SHEET only (PR-0000-000 convention, no real PR),
    per the video-1 spec's placeholder rule.

Self-contained (copies the shared helpers) so it never touches round 1.
Deterministic: same script + fonts -> same pixels. Render with headless chrome
(--force-device-scale-factor=1), then scan_theme_colors.py with the 7 tokens
--allow'd.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_REL = "../../../fonts"

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


def seal_mark_w(h):
    """Brand mark (style/brand-mark.svg) scaled to width h; viewBox 0 0 800 800."""
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


# ---------------------------------------------------------------- C2: chart ----
# The full-bleed verdict chart (1:1 SVG, 780x470) — thick axes, dim gridlines,
# thick paper curve, thick amber pre-registered bar with its mono tag.
CURVE_BIG = {
    "confirmed": "60,430 190,398 330,344 470,236 590,150 720,96",
    "falsified": "60,430 190,404 330,372 470,344 590,352 720,392",
}


def chart_big(kind):
    grid = "".join(
        f'<line x1="60" y1="{y}" x2="720" y2="{y}" stroke="{DIM}" stroke-width="1" opacity="0.35"/>'
        for y in (130, 240, 350))
    return f'''
<svg width="780" height="470" viewBox="0 0 780 470" style="display:block;">
  {grid}
  <line x1="60" y1="24"  x2="60"  y2="440" stroke="{DIM}" stroke-width="4"/>
  <line x1="60" y1="440" x2="740" y2="440" stroke="{DIM}" stroke-width="4"/>
  <line x1="60" y1="250" x2="740" y2="250" stroke="{AMBER}" stroke-width="8"/>
  <text x="736" y="238" text-anchor="end" font-family="JetBrains Mono"
        font-size="22" fill="{AMBER}">bar: &ge; 6.0% OOS</text>
  <polyline points="{CURVE_BIG[kind]}" fill="none" stroke="{PAPER}" stroke-width="12"
            stroke-linejoin="round" stroke-linecap="round"/>
</svg>'''


def thumb_c2(s):
    if s["kind"] == "seal":
        # meta episode: the chart is replaced by the seal, but keep the frame
        hero = f'<div style="position:absolute;left:400px;top:150px;width:300px;height:300px;">{seal_mark_w(300)}</div>'
        return border_box() + tag(s["tag"]) + hero + \
            (f'<div class="mono" style="position:absolute;left:0;right:0;top:470px;'
             f'text-align:center;font-size:30px;color:{PAPER};white-space:nowrap;">'
             f'{s["sub"]}</div>') + wordmark()
    col = CONF if s["kind"] == "confirmed" else FALS
    chart = f'<div style="position:absolute;left:44px;top:200px;">{chart_big(s["kind"])}</div>'
    seal = f'<div style="position:absolute;left:44px;top:44px;width:132px;height:132px;">{seal_mark_w(132)}</div>'
    num = (f'<div style="position:absolute;right:44px;top:52px;text-align:right;'
           f'font-size:150px;color:{col};white-space:nowrap;">{s["hero"]}</div>')
    sub = (f'<div class="mono" style="position:absolute;right:44px;top:214px;'
           f'text-align:right;font-size:30px;color:{PAPER};white-space:nowrap;">'
           f'{s["sub"]}</div>')
    tg = tag(s["tag"], x=204, y=92)
    return border_box() + tg + seal + chart + num + sub + wordmark()


# ----------------------------------------------------------------- D: ledger ---
# The scoreboard (CONCEPT 5) fills the frame. Columns: PR ID | HYPOTHESIS |
# BAR | OOS | VERDICT. Verdict cells in semantic colors. Aggregate row below.
LEDGER_ROWS = [
    ("PR-0000-001", "momentum",       "\u2265 6.0%", "+8.4%", "CONFIRMED",    CONF),
    ("PR-0000-002", "value tilt",     "\u2265 6.0%", "\u22122.1%", "FALSIFIED",   FALS),
    ("PR-0000-003", "vol target",     "\u2265 4.5%", "+3.9%", "INCONCLUSIVE", INCON),
    ("PR-0000-004", "barbell",        "\u2265 6.0%", "\u2014",    "AWAITING",    AMBER),
]


def ledger_table():
    head = (f'<div class="mono" style="display:flex;font-size:19px;letter-spacing:2px;'
            f'color:{DIM};padding:0 24px 14px;">'
            f'<div style="width:170px;">PR ID</div>'
            f'<div style="width:220px;">HYPOTHESIS</div>'
            f'<div style="width:120px;">BAR</div>'
            f'<div style="width:120px;text-align:right;">OOS</div>'
            f'<div>VERDICT</div></div>')
    rows = ""
    for pr, hyp, bar, oos, verdict, vcol in LEDGER_ROWS:
        rows += (
            f'<div style="height:1px;background:{DIM};opacity:.5;margin:0 24px;"></div>'
            f'<div class="mono" style="display:flex;align-items:center;font-size:26px;'
            f'padding:15px 24px;">'
            f'<div style="width:170px;color:{PAPER};">{pr}</div>'
            f'<div style="width:220px;color:{PAPER};white-space:nowrap;">{hyp}</div>'
            f'<div style="width:120px;color:{DIM};font-size:23px;">{bar}</div>'
            f'<div style="width:120px;text-align:right;color:{PAPER};">{oos}</div>'
            f'<div style="letter-spacing:2px;color:{vcol};font-size:23px;">{verdict}</div>'
            f'</div>')
    agg = (
        f'<div style="height:2px;background:{PAPER};margin:6px 24px 0;"></div>'
        f'<div class="mono" style="display:flex;justify-content:space-between;'
        f'padding:14px 24px 0;font-size:22px;color:{DIM};">'
        f'<span>confirmation rate</span><span style="color:{PAPER};">60% &middot; baseline 25%</span>'
        f'</div>')
    return head + rows + agg


def thumb_d(s):
    table = f'<div style="position:absolute;left:44px;top:96px;right:44px;">{ledger_table()}</div>'
    return border_box() + tag(s["tag"]) + table + wordmark()


# ------------------------------------------------------------------- E: seal ---
# The seal, stamped big — the signature moment as the object.
def thumb_e(s):
    col = CONF if s["kind"] == "confirmed" else (FALS if s["kind"] == "falsified" else PAPER)
    big = f'<div style="position:absolute;left:120px;top:120px;width:440px;height:440px;">{seal_mark_w(440)}</div>'
    # full spec-commit SHA (video 1: data/spec-sha.txt), 51 mono chars.
    # The stamp ring (r=330 of 800 viewBox, sw=18) at 440px render spans
    # x ~154..526 (center 340) — the SHA line is set to that width so its
    # edges align with the ring's outer edges. Font/tracking chosen for
    # 51 chars ~ 372px; pixel-verified on the render.
    sha = (f'<div class="mono" style="position:absolute;left:154px;top:584px;'
           f'width:372px;text-align:center;font-size:12px;color:{AMBER};'
           f'letter-spacing:0.1px;white-space:nowrap;">'
           f'git commit 86140f927343296bb2efc390288ac56b2c9865e2</div>')
    verdict = ""
    if s["kind"] != "seal":
        word = "CONFIRMED" if s["kind"] == "confirmed" else "FALSIFIED"
        verdict = (f'<div style="position:absolute;right:44px;top:280px;text-align:right;'
                   f'font-size:96px;font-weight:700;color:{col};white-space:nowrap;">'
                   f'{word}</div>')
        num = (f'<div class="mono" style="position:absolute;right:44px;top:400px;'
               f'text-align:right;font-size:34px;color:{PAPER};white-space:nowrap;">'
               f'{s["hero"]}</div>')
    else:
        # tagline centered in the right region (stamp right edge 560 -> frame
        # right margin 44), vertically centered on the seal (seal center y=340)
        verdict = (f'<div class="mono" style="position:absolute;left:560px;right:44px;'
                   f'top:325px;text-align:center;font-size:30px;color:{PAPER};'
                   f'white-space:nowrap;">{s["sub"]}</div>')
        num = ""
    return border_box() + tag(s["tag"]) + big + sha + verdict + num + wordmark()


# ------------------------------------------------------------------- pages -----
def page(body, label=None):
    css = base_css() + FACES.format(f=FONT_REL)
    lab = ""
    if label:
        lab = (f'<div class="mono" style="position:absolute;left:64px;top:48px;'
               f'font-size:24px;letter-spacing:2px;color:{DIM};">{label}</div>')
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head>
<body>{lab}{body}</body></html>'''


def shelf_row(inner, x, y, label):
    """inner (a 1280x720 thumbnail) at 0.5, plus a small-size ladder at 0.25."""
    big = (f'<div class="mono" style="position:absolute;left:{x}px;top:{y}px;font-size:20px;'
           f'letter-spacing:2px;color:{DIM};">{label}</div>'
           f'<div style="position:absolute;left:{x}px;top:{y+34}px;width:640px;height:360px;'
           f'overflow:hidden;"><div style="transform:scale(0.5);transform-origin:top left;'
           f'width:{W}px;height:{H}px;position:absolute;">{inner}</div></div>')
    ladder = ""
    yy = y + 34 + 360 + 40
    for sc in (0.25, 0.1875, 0.125):
        w, h = int(W * sc), int(H * sc)
        ladder += (f'<div style="position:absolute;left:{x}px;top:{yy}px;width:{w}px;'
                   f'height:{h}px;overflow:hidden;"><div style="transform:scale({sc});'
                   f'transform-origin:top left;width:{W}px;height:{H}px;position:absolute;">'
                   f'{inner}</div></div>')
        ladder += (f'<div class="mono" style="position:absolute;left:{x + w + 16}px;top:{yy + h/2 - 10}px;'
                   f'font-size:16px;color:{DIM};">{w}px</div>')
        yy += h + 22
    return big + ladder


def build(idea, label, hero_samples):
    """hero_samples: list of (key, sample, thumb_fn, sheet_label)."""
    out = os.path.join(HERE, "concepts", idea)
    os.makedirs(out, exist_ok=True)
    for key, s, fn, _ in hero_samples:
        open(f"{out}/thumb-{key}.html", "w").write(page(fn(s)))
    sheet = ""
    for i, (key, s, fn, lab) in enumerate(hero_samples):
        sheet += shelf_row(fn(s), 96 + i * 800, 120, lab)
    open(f"{out}/sheet.html", "w").write(page(sheet, label=label))
    print(f"wrote {out}/")


# real = video 1 (META, seal); others labeled examples in the sheet only
SEAL_S = {"key": "seal", "tag": "META · EP 01", "kind": "seal",
          "hero": "", "sub": "the rules that run the channel"}
CONF_S = {"key": "confirmed", "tag": "STRATEGY 01", "kind": "confirmed",
          "hero": "+8.4%", "sub": "PR-0000-001 · bar: ≥ 6.0% OOS"}
FALS_S = {"key": "falsified", "tag": "STRATEGY 01", "kind": "falsified",
          "hero": "−2.1%", "sub": "PR-0000-001 · bar: ≥ 6.0% OOS"}

build("thumb-c2", "THUMBNAIL CONCEPT C2 — VERDICT CHART + SEAL",
      [("seal", SEAL_S, thumb_c2, "META · EP 01  (video 1)"),
       ("confirmed", CONF_S, thumb_c2, "STRATEGY 01  (example)"),
       ("falsified", FALS_S, thumb_c2, "STRATEGY 01  (example)")])
build("thumb-d", "THUMBNAIL CONCEPT D — THE SCOREBOARD",
      [("ledger", SEAL_S, thumb_d, "THE SCOREBOARD  (example rows)")])
build("thumb-e", "THUMBNAIL CONCEPT E — THE SEAL, STAMPED",
      [("seal", SEAL_S, thumb_e, "META · EP 01  (video 1)"),
       ("confirmed", CONF_S, thumb_e, "STRATEGY 01  (example)")])
print("done")
