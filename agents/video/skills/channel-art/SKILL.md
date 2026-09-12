---
name: channel-art
description: "Use when creating channel art: banner, logo, description."
version: 1.0.0
author: Preregistered Money
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [branding, channel-art, banner, logo, youtube]
    editorial_name: Channel Art
    editorial_description: How to design, render, QA, and commit the channel's banner, profile logo, and description from the committed style system.
---

# Channel Art

Channel art = banner (channel art), profile logo, channel description. Like every
published frame it is a **deterministic artifact of the style system** — art is
never hand-made pixels; it is HTML/SVG rendered from committed source.

Living directory: `videos/pipeline/brand/` (generator + `concepts/<idea>/`).

## Standing rules

1. **Palette + fonts only from the style spec.** The 7 tokens and Inter / JetBrains
   Mono. Verify two ways after every render: hex-audit the generated HTML
   (`grep -rhoE '#[0-9A-Fa-f]{6}' ... | sort | uniq -c`) and run
   `videos/pipeline/tools/scan_theme_colors.py` over the concept dir — the brand
   claim is that the art is generated from the system, and one off-palette hex
   breaks it.
2. **No numbers on the art.** The number-trace rule applies to art too: every
   figure must exist in a published doc, and brand art has no results doc to cite.
   Allowed text: the name/tagline and identifiers declared in `docs/CONCEPT.md`
   (e.g. `PR-2026-001` shown in its actual pending state). Never a fabricated
   metric, count, or date.
3. **Commit the source, not just the PNGs.** Generator script + emitted HTML +
   rendered PNGs all land under `videos/pipeline/brand/`. Re-running the
   generator must regenerate the pixels — same input → same pixels is the brand.
4. **Wordmark.** Channel name settled 2026-09-12: **Preregistered Money**,
   handle `@preregisteredmoney`. Wordmark is `PREREGISTERED MONEY`; the mark
   is pinned in `style/brand-mark.svg` (style-spec §4.2). Art renders from
   the generator — when anything brand-level changes, edit the one constant
   and re-render everything; never re-handcraft art. The final mix (owner
   decision 2026-09-12): bar banner + seal stamp holding the bar, committed
   under `concepts/final/`.

## Sizes (YouTube)

- **Banner:** upload 2560×1440. All-device safe area is **1546×423 centered**
  → x 507..2053, y 509..931. All required content (name, mark, tagline) lives
  inside the safe box; outer margins are plain ink shown only on TV.
- **Profile logo:** 800×800, all content inside the central circle — YouTube
  crops avatars to a circle.
- Max file size 6 MB; these renders are ~50–150 KB.

## Procedure

1. **Concepts first.** Present 3 distinct directions, each a mark + banner
   composition + rationale tied to the brand (the seal scene, the scoreboard,
   the bar). Don't render one idea and ask for approval.
2. **Generator.** One Python script emits `concepts/<idea>/{banner.html,logo.html,sheet.html}`.
   Pure HTML; SVG marks inline; fonts referenced relatively from the vendored
   WOFF2 in `videos/pipeline/fonts/`.
3. **Render** at 1:1 scale:
   ```
   google-chrome-stable --headless=new --no-sandbox --disable-gpu --hide-scrollbars \
     --force-device-scale-factor=1 --virtual-time-budget=6000 \
     --window-size=W,H --screenshot=out.png file://$PWD/abs/path.html
   ```
   `--force-device-scale-factor=1` for pixel-exact output; `--virtual-time-budget`
   gives the `@font-face` WOFF2s time to load before capture (skip it and the
   fonts silently fall back).
4. **Review sheet** per concept (one 2560×1440 sheet the owner can compare):
   banner at 0.5 scale with a dashed safe-zone guide + label, logo at full size
   and inside a circular crop, plus the mark at small sizes (160/98/76 px) to
   catch legibility collapse.
5. **Vision QA loop.** `vision_analyze` each sheet → surgical fix (a line in the
   generator) → re-render → re-verify the fixed region before moving on.
6. **Hex audit** + `scan_theme_colors.py` (rule 1).
7. **Commit.** One atomic commit, `feat(pipeline)` scope, paths confined to
   `videos/pipeline/brand/` (inside the `video-commit` boundary; never stage
   `docs/**` or `research/**`).
8. **Descriptions.** Deliver 1–2 short channel-description paragraphs with the
   art: method → what the archive is → honesty. End with the standing disclaimer:
   "Educational content, not investment advice."

## Pitfalls

- **Position SVGs inside a positioned container div; never `transform:translate`
  the SVG element itself.** An SVG with its own viewBox centers its content in
  its own coordinate space; a translate in the outer flow silently shifts the
  mark off-canvas instead of re-centering it.
- **Fixed-layout HTML art: `white-space:nowrap` on every text element and
  explicit widths on flex cells.** Absolutely-positioned text wraps silently at
  column edges, and the wrap looks like a defect in the mockup. Measure before
  you place; don't eyeball widths.
- **Text baselines graze:** a 23 px tagline needs ~10–16 px below a 64 px
  title's baseline or they touch. Re-verify with a vision pass after moving
  any text.
- **f-string templates double their CSS braces** (`{{ }}` in `.format()`
  templates) — an unbalanced `@font-face` block raises KeyError. Lint the
  generator before the first run.
- **Design the banner in zone-local coordinates:** position the container at
  (507, 509) and lay out inside 1546×423 — it's easier to keep the safe zone
  than to audit global coordinates.
