---
name: channel-art
description: "Use when creating channel art: banner, logo, description, or a per-video thumbnail."
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

Channel art = banner (channel art), profile logo, channel description, and each
video's thumbnail. Like every published frame it is a **deterministic artifact of
the style system** — art is never hand-made pixels; it is HTML/SVG rendered from
committed source.

Living directory: `videos/pipeline/brand/` (generator + `concepts/<idea>/`).

## Standing rules

1. **Palette + fonts only from the style spec.** The 7 tokens and Inter / JetBrains
   Mono. Verify two ways after every render: hex-audit the generated HTML
   (`grep -rhoE '#[0-9A-Fa-f]{6}' ... | sort | uniq -c`) and run
   `videos/pipeline/tools/scan_theme_colors.py` over the concept dir — the brand
   claim is that the art is generated from the system, and one off-palette hex
   breaks it. The scanner takes ONE root and needs the full palette as
   `--allow` (quote the hexes — an unquoted `#` dies as a shell comment):
   `scan_theme_colors.py concepts --allow '#0B0E11' --allow '#E8E6E1'
   --allow '#6B7078' --allow '#C89B3C' --allow '#3FA46A' --allow '#C4453C'
   --allow '#8A9099'` — exit 0 is clean. Without `--allow` it flags every color
   as "review" and exits 1; that is unconfigured, not a violation.
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
   under `concepts/final/`. Banner v2 (2026-09-12) dropped the name from the
   banner per owner: chart + `bar: pre-registered` annotation + tagline only;
   the wordmark still appears in videos (beat 1), logo, and metadata.

## Sizes (YouTube)

- **Banner:** upload 2560×1440. All-device safe area is **1546×423 centered**
  → x 507..2053, y 509..931. All content lives inside the safe box; outer
  margins are plain ink shown only on TV. **No channel name on the banner**
  (owner decision 2026-09-12): YouTube already renders the name directly below
  the art on the channel page, so repeating it is redundant — the banner carries
  only the chart/wordless mark, annotations, and tagline (the tagline becomes
  the hero text).
- **Profile logo:** 800×800, all content inside the central circle — YouTube
  crops avatars to a circle.
- **Thumbnail:** 1280×720.
- Max file size 6 MB; these renders are ~50–150 KB.

## Thumbnails (per-video)

- **Design bar: a dominant object, not a poster.** A thumbnail earns the click
  with a visual object that fills the frame — the verdict chart (thick curve +
  amber pre-registered bar + huge number), the scoreboard, or the stamp. A small
  hero token on empty ink reads as a brand specimen, not a video: the owner
  rejected the minimal centered-poster and thin-ledger-row looks as "nobody
  will click on these." No hype (no stock, no glow, no exclamation) — richness
  comes from the set piece's density, not from ornament. A dense-text wall
  (full ledger) reads as substance at full size but smears at list size —
  density without a dominant object is not a click.
- **Two house looks (owner decision 2026-09-14).** C2 "verdict chart" for
  verdict episodes — full-bleed chart, amber bar, verdict-colored OOS number,
  a seal stamp certifying the corner; E "stamped" for meta / pre-verdict
  episodes — big brand-mark stamp, full spec-commit SHA line beneath it aligned
  to the stamp's edges, tagline (meta) or verdict word + number in the open
  space to the right. Shared chassis: 12px-inset dim border, series tag
  top-left mono uppercase, wordmark bottom-right, palette-only. Source of truth:
  style spec §8 + the thumbnail generator under `videos/pipeline/brand/`;
  per-video thumbnails render from the committed generator — never hand-made per
  video.
- **Per-video hero (owner decision 2026-09-14).** The hero varies by video — the
  OOS number (verdict color) on a C2 frame, the seal on an E frame. The seal is
  NOT a constant hero across the channel, and a meta episode has no number, so
  its frame must not fake one.
- **Emitter (pinned).**
  `python3 videos/pipeline/brand/gen_thumbnails.py <slug> <mode> [series_tag]
  [hero] [subline] [spec_sha]` — mode `meta` or `pre-verdict` renders the E
  look, `verdict:confirmed|verdict:falsified|verdict:inconclusive` the C2
  look. It emits `videos/<slug>/thumbnail.html`; headless chrome (window
  1280,720) renders it to `videos/<slug>/renders/thumbnail.png`. `spec_sha` is
  the video's own sealed spec commit from `data/spec-sha.txt`. The C2 curve
  shape is illustrative only — the verdict read is relative to the bar; the
  number and bar text must trace to the prereg/results doc.
- **Type scale.** 1080p token scale × 2/3 at 1280×720 — no new sizes.
- **List view is the acceptance bar.** The YouTube shelf shows thumbnails at
  ~160–320 px wide; the hero must read at 160 px. Every concept review sheet
  carries a "shelf" row with each sample at 320/240/160 px, and the vision QA
  pass judges the shelf row, not just the full-size frames.
- **Mockup numbers.** Concept sheets may show sample numbers under the
  `PR-0000-000` placeholder convention, labeled "(example)" in the SHEET label
  (never inside the asset). A committed thumbnail asset uses only values that
  trace to the results doc (rule 2).
- **Asset location + lifecycle.** The per-video thumbnail commits inside the
  video directory (one video = one dir, `video-commit` rule 1); the build log
  records generator version + inputs. The committed artifacts are
  `thumbnail.html` + the build-log section — `renders/` is gitignored
  (`videos/*/renders/`), so record the PNG's sha256 in the build log instead of
  staging it, and re-running the emitter + render must reproduce the pixels.
  Render it LAST in the video lifecycle — after the final MP4 is committed,
  before publish — the upload needs it.
- **Video description (per-video) — written at the thumbnail stage (owner
  decision 2026-09-14).** The description is part of the upload package: it is
  written during the thumbnail step (after the final MP4 is committed, before
  publish) and committed as `videos/<slug>/description.md` in the same commit
  as the build-log section that records it. Structure: one-line hook → what
  the episode does → the record (prereg ID, seal SHA, results-doc path, repo
  link) → the standing disclaimer ("Educational content, not investment
  advice."). Same number-trace rule as the frames: every figure traces to the
  cited results/prereg doc; a meta episode cites the seal SHA, not a number.
  No hype — the description is metadata for the record, not a pitch.
  **Caps:** the YouTube video-description field allows 5,000 chars but only the
  first ~150 are visible before "Show more" — the one-line hook must stand
  there. The channel "about" field is hard-capped at 1,000 chars — measure the
  pasted text (chars, not bytes) and trim, never silently overflow.

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
   "Educational content, not investment advice." Keep it ≤1,000 chars (YouTube's
   hard cap for the channel "about" field). Commit it as
   `videos/pipeline/brand/channel-description.md` (the channel-page text is a
   brand artifact, like the banner). Per-video descriptions are written at the
   thumbnail stage — see "Thumbnails → Video description".

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
  templates) — an unbalanced `@font-face` block raises KeyError — and a CSS unit
  inside the expression is a SyntaxError (`top:{y + 34px}`; the unit goes
  outside the braces). Lint the generator before the first run.
- **Design the banner in zone-local coordinates:** position the container at
  (507, 509) and lay out inside 1546×423 — it's easier to keep the safe zone
  than to audit global coordinates.
- **SVG width/height must match the viewBox aspect ratio:** a mismatched pair
  (e.g. 720×660 over a `0 0 720 540` viewBox) stretches the coordinate space
  non-uniformly and distorts stroke weights. Set width/height equal to the
  viewBox (1:1) for true pixel weights.
- **Right-aligning positioned divs:** a left-anchored div with
  `text-align:right` just left-aligns its content — anchor with `right:` (or give
  the div an explicit width) to actually right-align.
- **Text fitted to a shape is pixel-verified, not font-mathed.** Mono advance
  width × char count mispredicts the rendered width once letter-spacing and
  anti-aliasing enter. Render, then measure the 2D ink bbox of the text over its
  full row range (PIL scan for the token color) — a single scanline misses thin
  or low-contrast glyphs — and tune font-size/letter-spacing until the bbox
  edges line up with the target (e.g. the stamp ring's outer edge).
