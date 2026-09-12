#!/usr/bin/env python3
"""Channel-art concept mockups — source of the three banner/logo proposals.

Generates HTML (the renderable source) under videos/pipeline/brand/concepts/<idea>/.
Deterministic: same script + fonts -> same pixels. Render with headless chrome:
  google-chrome-stable --headless=new --no-sandbox --disable-gpu \
    --force-device-scale-factor=1 --virtual-time-budget=5000 \
    --window-size=<W>,<H> --screenshot=<out>.png file://<in>.html

Constraints honored (style-spec v1.0.0):
  - palette: only the 7 tokens (tokens.css)
  - fonts: Inter + JetBrains Mono (vendored WOFF2 in videos/pipeline/fonts/)
  - no gradients, no glow, no text outside the palette
  - banner 2560x1440, all-device safe zone 1546x423 centered (x 507..2053, y 509..931)
  - profile logo 800x800, content kept inside the circular crop
No numbers are shown anywhere on the art (nothing to fabricate); the one
ledger row shown is the declared first prereg per docs/CONCEPT.md section 3.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_REL = "../../../fonts"  # concepts/<idea>/ -> pipeline/fonts/

FACES = """
@font-face{{font-family:"Inter";src:url("{f}/Inter-Regular.woff2") format("woff2");font-weight:400;}}
@font-face{{font-family:"Inter";src:url("{f}/Inter-SemiBold.woff2") format("woff2");font-weight:600;}}
@font-face{{font-family:"Inter";src:url("{f}/Inter-Bold.woff2") format("woff2");font-weight:700;}}
@font-face{{font-family:"JetBrains Mono";src:url("{f}/JetBrainsMono-Regular.woff2") format("woff2");font-weight:400;}}
@font-face{{font-family:"JetBrains Mono";src:url("{f}/JetBrainsMono-Medium.woff2") format("woff2");font-weight:500;}}
"""

BASE_CSS = """
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:{w}px;height:{h}px;background:#0B0E11;overflow:hidden;font-family:"Inter",-apple-system,sans-serif;}}
.mono{{font-family:"JetBrains Mono",ui-monospace,monospace;}}
"""

INK, PAPER, DIM, AMBER, CONF, FALS, INCON = (
    "#0B0E11", "#E8E6E1", "#6B7078", "#C89B3C", "#3FA46A", "#C4453C", "#8A9099")

NAME = "PREREGISTERED MONEY"

# ---- shared marks -----------------------------------------------------------

def seal_mark(scale=1.0):
    """Double-ring certification stamp with the ascending line crossing the bar."""
    s = scale
    return f'''
<svg width="{int(800*s)}" height="{int(800*s)}" viewBox="-400 -400 800 800"
     style="display:block;">
  <circle r="330" fill="none" stroke="{PAPER}" stroke-width="18"/>
  <circle r="282" fill="none" stroke="{PAPER}" stroke-width="4"/>
  <line x1="-170" y1="20" x2="170" y2="20" stroke="{AMBER}" stroke-width="7"/>
  <polyline points="-150,95 -15,10 150,-105" fill="none" stroke="{PAPER}"
            stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/>
</svg>'''

def ledger_mark(scale=1.0):
    """Stamp ring containing three ledger rows; third row pending (dim) with amber tick."""
    s = scale
    return f'''
<svg width="{int(800*s)}" height="{int(800*s)}" viewBox="-400 -400 800 800"
     style="display:block;">
  <circle r="330" fill="none" stroke="{PAPER}" stroke-width="18"/>
  <circle r="282" fill="none" stroke="{PAPER}" stroke-width="4"/>
  <line x1="-110" y1="-70" x2="110" y2="-70" stroke="{PAPER}" stroke-width="14" stroke-linecap="round"/>
  <line x1="-110" y1="0"   x2="110" y2="0"   stroke="{PAPER}" stroke-width="14" stroke-linecap="round"/>
  <line x1="-110" y1="70"  x2="-40" y2="70"  stroke="{DIM}"   stroke-width="14" stroke-linecap="round"/>
  <rect x="-146" y="54" width="10" height="32" fill="{AMBER}"/>
</svg>'''

def bar_mark(scale=1.0):
    """The bar: one amber horizontal, one ascending paper line crossing it."""
    s = scale
    return f'''
<svg width="{int(800*s)}" height="{int(800*s)}" viewBox="-400 -400 800 800"
     style="display:block;">
  <line x1="-320" y1="40" x2="320" y2="40" stroke="{AMBER}" stroke-width="12"/>
  <line x1="-240" y1="240" x2="240" y2="-220" stroke="{PAPER}" stroke-width="22"
        stroke-linecap="round"/>
</svg>'''

# ---- banners (2560x1440; safe zone x 507..2053, y 509..931) ------------------

def banner_seal():
    return f'''
<div style="position:absolute;left:507px;top:509px;width:1546px;height:423px;">
  <div style="position:absolute;left:0;top:20px;width:64px;height:4px;background:{DIM};"></div>
  <div style="position:absolute;left:0;top:64px;font-size:116px;font-weight:700;
       letter-spacing:2px;color:{PAPER};line-height:1.12;">PREREGISTERED<br>MONEY</div>
  <div class="mono" style="position:absolute;left:0;top:330px;font-size:27px;
       letter-spacing:1px;color:{DIM};">hypotheses sealed before the data is looked at</div>
  <div style="position:absolute;right:0;top:100px;width:320px;height:320px;">
    {seal_mark(scale=0.4)}
  </div>
</div>'''

def banner_ledger():
    return f'''
<div style="position:absolute;left:507px;top:509px;width:1546px;height:423px;">
  <div style="position:absolute;left:0;top:24px;font-size:64px;font-weight:700;
       letter-spacing:1px;color:{PAPER};white-space:nowrap;">PREREGISTERED MONEY</div>
  <div class="mono" style="position:absolute;left:0;top:100px;font-size:23px;color:{DIM};
       white-space:nowrap;letter-spacing:1px;">a public scoreboard of quant hypotheses</div>
  <!-- ledger -->
  <div style="position:absolute;left:0;top:160px;right:0;">
    <div class="mono" style="display:flex;font-size:21px;letter-spacing:2px;color:{DIM};">
      <div style="width:250px;">PR ID</div>
      <div style="width:560px;">HYPOTHESIS</div>
      <div style="width:240px;">BAR</div>
      <div>VERDICT</div>
    </div>
    <div style="height:1px;background:{DIM};margin-top:14px;"></div>
    <div class="mono" style="display:flex;align-items:baseline;font-size:26px;margin-top:34px;">
      <div style="width:250px;color:{PAPER};">PR-2026-001</div>
      <div style="width:560px;color:{PAPER};white-space:nowrap;">benchmark study — spx / tlt / gld</div>
      <div style="width:240px;font-size:22px;color:{DIM};">frozen at seal</div>
      <div style="font-size:22px;letter-spacing:2px;color:{AMBER};">AWAITING VERDICT</div>
    </div>
    <div style="height:1px;background:{DIM};opacity:.45;margin-top:30px;"></div>
    <div class="mono" style="display:flex;align-items:baseline;font-size:26px;margin-top:26px;">
      <div style="width:250px;"><span style="display:inline-block;width:16px;height:32px;
           background:{DIM};vertical-align:text-bottom;"></span></div>
      <div style="width:560px;color:{DIM};letter-spacing:4px;">· · ·</div>
      <div style="width:240px;color:{DIM};letter-spacing:4px;">· · ·</div>
      <div style="color:{DIM};letter-spacing:4px;">· · ·</div>
    </div>
  </div>
</div>'''

def banner_bar():
    # zone-local coordinates: 1546 x 423. curve + bar in the upper area, name below.
    curve_pts = [(0, 200), (300, 190), (600, 185), (900, 170),
                 (1150, 150), (1350, 110), (1500, 60), (1546, 45)]
    poly = " ".join(f"{x},{y}" for x, y in curve_pts)
    return f'''
<div style="position:absolute;left:507px;top:509px;width:1546px;height:423px;">
  <svg width="1546" height="260" viewBox="0 0 1546 260" style="position:absolute;left:0;top:0;">
    <line x1="0" y1="175" x2="1546" y2="175" stroke="{AMBER}" stroke-width="6"/>
    <polyline points="{poly}" fill="none" stroke="{PAPER}" stroke-width="7"
              stroke-linejoin="round" stroke-linecap="round"/>
  </svg>
  <div class="mono" style="position:absolute;right:0;top:228px;font-size:22px;color:{DIM};">
       bar: pre-registered</div>
  <div style="position:absolute;left:0;right:0;top:292px;text-align:center;font-size:92px;
       font-weight:700;letter-spacing:2px;color:{PAPER};">PREREGISTERED MONEY</div>
  <div class="mono" style="position:absolute;left:0;right:0;top:402px;text-align:center;
       font-size:24px;color:{DIM};">every result is judged against a bar set in advance</div>
</div>'''

# ---- logos (800x800) ---------------------------------------------------------

def logo_seal():
    return f'<div style="width:800px;height:800px;">{seal_mark(scale=1.0)}</div>'

def logo_ledger():
    return f'<div style="width:800px;height:800px;">{ledger_mark(scale=1.0)}</div>'

def logo_bar():
    return f'<div style="width:800px;height:800px;">{bar_mark(scale=1.0)}</div>'

# ---- page assembly -----------------------------------------------------------

IDEAS = {
    "seal":   {"label": "CONCEPT A — THE SEAL",   "banner": banner_seal,   "logo": logo_seal,   "mark": seal_mark},
    "ledger": {"label": "CONCEPT B — THE LEDGER", "banner": banner_ledger, "logo": logo_ledger, "mark": ledger_mark},
    "bar":    {"label": "CONCEPT C — THE BAR",    "banner": banner_bar,    "logo": logo_bar,    "mark": bar_mark},
}

# Owner decision 2026-09-12: channel name "Preregistered Money",
# handle @preregisteredmoney (already claimed). Final art = the bar banner
# (concept C) + the seal stamp with the bar inside (concept A). The seal
# stamp in the logo is the same mark pinned as style/brand-mark.svg
# (style-spec v1.1.0 §4.2).
FINAL = {"banner": banner_bar, "logo": logo_seal, "mark": seal_mark}

def page(w, h, body, label=None):
    css = BASE_CSS.format(w=w, h=h) + FACES.format(f=FONT_REL)
    lab = ""
    if label:
        lab = (f'<div class="mono" style="position:absolute;left:64px;top:48px;'
               f'font-size:24px;letter-spacing:2px;color:{DIM};">{label}</div>')
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head>
<body>{lab}{body}</body></html>'''

def safe_zone_guides():
    return f'''
<div style="position:absolute;left:507px;top:509px;width:1546px;height:423px;
     border:2px dashed {DIM};opacity:.6;pointer-events:none;">
  <span class="mono" style="position:absolute;left:10px;top:8px;font-size:20px;color:{DIM};">
    safe zone 1546×423 — visible on all devices</span>
</div>'''

def build_idea(idea, d):
    out = os.path.join(HERE, "concepts", idea)
    os.makedirs(out, exist_ok=True)
    # 1. clean banner asset
    open(f"{out}/banner.html", "w").write(page(2560, 1440, d["banner"]()))
    # 2. clean logo asset
    open(f"{out}/logo.html", "w").write(page(800, 800, d["logo"]()))
    # 3. review sheet: banner @0.5 with guides + logo at several sizes
    banner_small = (f'<div style="position:absolute;left:640px;top:120px;width:1280px;'
                    f'height:720px;overflow:hidden;border:1px solid {DIM};">'
                    f'<div style="transform:scale(0.5);transform-origin:top left;'
                    f'width:2560px;height:1440px;position:absolute;">'
                    f'{d["banner"]()}{safe_zone_guides()}</div></div>')
    sizes = ""
    bottom = 1170  # common baseline for the small-size marks
    for i, (s, x) in enumerate([(0.20, 1520), (0.1225, 1760), (0.095, 1940)]):
        w = int(800 * s)
        y = bottom - w
        sizes += (f'<div class="mono" style="position:absolute;left:{x}px;top:1184px;'
                  f'font-size:20px;color:{DIM};width:{w}px;text-align:center;">{w}px</div>')
        sizes += (f'<div style="position:absolute;left:{x}px;top:{y}px;">'
                  f'{d["mark"](scale=s)}</div>')
    sheet = banner_small + (
        f'<div class="mono" style="position:absolute;left:64px;top:950px;font-size:22px;'
        f'letter-spacing:2px;color:{DIM};">LOGO — 800×800 (circular crop shown at right)</div>'
        f'<div style="position:absolute;left:64px;top:990px;width:400px;height:400px;">'
        f'<div style="transform:scale(0.5);transform-origin:top left;width:800px;height:800px;">'
        f'{d["logo"]()}</div></div>'
        f'<div style="position:absolute;left:620px;top:990px;width:400px;height:400px;'
        f'border-radius:50%;overflow:hidden;border:1px solid {DIM};">'
        f'<div style="transform:scale(0.5);transform-origin:top left;width:800px;height:800px;">'
        f'{d["logo"]()}</div></div>'
        f'<div class="mono" style="position:absolute;left:1500px;top:950px;font-size:22px;'
        f'letter-spacing:2px;color:{DIM};">AT SMALL SIZES</div>'
        + sizes)
    open(f"{out}/sheet.html", "w").write(
        page(2560, 1440, sheet, label=d["label"] + " · channel art mockup"))
    print(f"wrote {out}/")

for idea, d in IDEAS.items():
    build_idea(idea, d)
# Final art: the chosen mix — bar banner + seal stamp logo.
build_idea("final", {"label": "FINAL — PREREGISTERED MONEY @preregisteredmoney",
                     **FINAL})
print("done")
