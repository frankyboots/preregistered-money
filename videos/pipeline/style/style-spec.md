# Style Spec

**Version: 1.0.0**
Status: draft v1 — proposed at the branding session, owner review pending.

This file is the "what" of the channel's visual system (VIDEO_CONCEPT §6). The
concept document is the "why and how". Every build log pins this version.
Tokens live in `tokens.css` (same directory); scenes consume tokens, never
hardcode values.

---

## 1. Design stance

The visual language looks like the method: a **ledger, a seal, an audit
trail**. Rules:

1. **Data-forward, faceless, minimal motion.** No on-camera presence, no
   presenter, no stock footage. The visuals are the data.
2. **Color is semantic only.** A color on screen must carry meaning (verdict,
   "untested", or emphasis). The base is nearly monochrome so the few colors
   read as verdicts, not decoration.
3. **Change follows speech.** The frame builds itself as the narration names
   things (§5.1). No lights, no ambient motion — engagement comes from
   relevance-ordered reveals, not from pixel activity.
4. **Determinism is the brand.** Same committed inputs → same pixels. Pinned
   versions, pinned fonts, pinned set pieces.

## 2. Palette (7 tokens, total)

| Token | Hex | Role |
|---|---|---|
| `--ink` | `#0B0E11` | Every background. Deep charcoal, never pure black. |
| `--paper` | `#E8E6E1` | All body text, chart series lines, rules. |
| `--paper-dim` | `#6B7078` | Axes, gridlines, captions, timestamps, the corner bug. |
| `--seal-amber` | `#C89B3C` | Anything pending/untested: Seal series accents, the pre-registered bar line, "awaiting verdict" states. |
| `--confirmed` | `#3FA46A` | Confirmed verdicts only (verdict card, scoreboard cell). |
| `--falsified` | `#C4453C` | Falsified verdicts only. Same production values as confirmed — color is the only difference. |
| `--inconclusive` | `#8A9099` | Inconclusive verdicts only. |

Color-discipline rules:

- Chart series lines are **always** `--paper` (or `--paper-dim` for raw,
  §6.2). Verdict colors never appear on chart lines.
- No gradients, no glow, no neon. No blue/purple SaaS palette, no sci-fi HUD.
- Portfolio P&L figures do **not** use red/green — that would collide with
  verdict semantics. Deltas are `--paper-dim` with `+`/`−` glyphs. (Standing
  decision; a change is an owner decision, not drift.)
- The only amber in a Verdict video is the bar line.

## 3. Typography

Fonts (pinned, SIL OFL, vendored as WOFF2 in `videos/pipeline/fonts/`,
checksummed in the build log):

- **Inter** — display and body prose. Weights: 400, 600, 700.
- **JetBrains Mono** — all data. Weights: 400, 500.

**The mono rule: every number on screen is JetBrains Mono with tabular
figures.** SHAs, dates, bars, CAGRs, table cells, axis labels — no
exceptions. Prose is human, data is machine; the mono/sans contrast is the
brand.

Scale — 4 levels only, no 5th size:

| Level | Size | Use |
|---|---|---|
| Hero | 120–160px | Headline OOS number, verdict word |
| Title | 48–56px | Scene titles |
| Body | 28–32px | Narration-supporting on-screen text |
| Annotation | 20–22px | Axis labels, tags, the corner bug, disclaimer title |

Layout: 1920×1080. 80px outer safe margin. The bottom 132px is
**caption-safe**: no data element may sit in it (SRT overlays there).

## 4. Set pieces (the visual identity)

These five are pinned elements. Any pixel change to a set piece is a
**major** version bump and, for the disclaimer card, an owner decision.

### 4.1 Corner bug

Upper-left, 40px margin, JetBrains Mono 20px `--paper-dim`:

```
WORDMARK · PR-YYYY-NNN · sealed YYYY-MM-DD · <short-sha-8>
```

Fades in with each scene (200ms). Every frame self-identifies — the
reproducibility promise, visually. The wordmark text waits on the channel-name
decision; placeholder ring/wordmark slot until then.

### 4.2 The seal scene

The channel's signature moment. Sequence (~6–8s total, fixed):

1. Ink background. A monospace line types in over 1.2s:
   `git commit --amend --no-edit  <full-sha>` (types left→right, 1 char/tick).
2. The seal stamp — a single-stroke ring, embossed look, wordmark inside —
   scales in with **stamp** motion (150ms, 1.15→1.0, no overshoot, no
   bounce). This is the only impact motion in the system.
3. The full SHA sits inside the ring, `--seal-amber`, JetBrains Mono, held
   3s before scene cut.

The seal is the certification-stamp / tamper-evident-sticker archetype, not a
SaaS logo: one stroke weight, `--paper` stroke on ink, amber only for the SHA.
Sound: none (standing; a pinned CC0 thud would require an owner decision).

### 4.3 The bar

Pre-registered bars are **always drawn** on every chart that shows the
relevant metric: a solid `--seal-amber` 3px horizontal line across the plot
area, tagged above it at the right end in JetBrains Mono 22px:
`bar: ≥ 6.0% OOS CAGR` — exact text from the prereg's bar field, no
paraphrase. The bar is drawn **last**, after the series lines. The verdict is
read by eye: the curve ends above or below the line.

### 4.4 The verdict card

One layout for all three outcomes. Ink background, no border, no decoration:

- One word: `CONFIRMED` / `FALSIFIED` / `INCONCLUSIVE`, Inter 700, 160px,
  centered, in the verdict color.
- Same position, same size, same 2s hold, in all three. No euphemism variants.
- Falsified gets identical production values; the post-mortem beat follows as
  a separate scene.

### 4.5 The disclaimer card

Verbatim CONCEPT §10, rendered identically in every video — same pixels every
time. An integrity anchor, not a decoration.

- Layout: ink field, 1px `--paper-dim` border, 40px padding, left-aligned.
- Title `HONEST LIMITATIONS` (annotation size, JetBrains Mono,
  `--paper-dim`, letterspaced).
- The four bullets, JetBrains Mono 26px `--paper`, line-height 1.6:

> - Educational content, not investment advice.
> - Backtest results are estimates under stated assumptions; live performance will differ, possibly badly.
> - Preregistration controls data snooping; it does not control overfitting in pre-seal choices, data quality, or market regime change.
> - Past performance (including preregistered, costed, out-of-sample past performance) is the weakest predictor in finance.

Source of truth for the text is `docs/CONCEPT.md` §10. If CONCEPT §10 changes,
the card changes in the same release with a major style-spec bump and an owner
decision recorded.

### 4.6 The scoreboard ledger

Full-bleed table, `--paper` on `--ink`, thin `--paper-dim` rules:

- Row height 56px. Header row: JetBrains Mono, uppercase, `--paper-dim`.
- Columns: PR ID · hypothesis (one line) · date sealed · verdict · headline OOS number · link (URL text).
- Verdict cell in the verdict color; everything else `--paper`.
- The composite row (pinned strategies) is distinguished by a 2px `--paper`
  rule above it, not by color.
- Rows reveal one at a time on their narration cue (reveal, 200ms), in
  scoreboard order. No full-table fade-in.

## 5. Motion system

### 5.1 The narration-anchored reveal rule (anti-staleness)

No scene may be a dead hold. The rule is **relevance ordering**, not pixel
activity:

1. **Reveal on naming.** Every element (line, point, row, number, label,
   title) appears during the word of the narration that names it — not
   before, not after.
2. **No pre-naming.** An element is never fully visible for more than 2s
   before the narration reaches it.
3. **Earn the still.** Stillness is allowed only after the scene's last word
   (or during an intentional pause). The final hold is the scene's most
   informative state — everything that was named is on screen.
4. **Change floor.** Within any continuous 10s span of speech there is at
   least one state change: a new element, a number roll, a table row, or a
   line extension.
5. **Silence is a script problem.** If narration is silent mid-scene for more
   than 3s, that is flagged at REVIEW (tighten the script or re-cut the
   scene). It is never filled with motion.

Every scene's beat timeline (scene-spec template) therefore carries at least
one cue row per 10s of narration. A scene that can't satisfy the change floor
is overlong: split it or cut the script.

### 5.2 The five verbs

| Verb | Params | Where |
|---|---|---|
| **cut/fade** | hard cut default; 200ms fade for open/close only | scene changes |
| **reveal** | 250ms opacity + 12px slide-up (`power2.out`); table rows 200ms | every named element; scoreboard rows |
| **draw** | 600–900ms left→right, `power2.out`; the bar 400ms | chart series (raw first, cost-adjusted second, bar last) |
| **roll** | 500–800ms, one count-up, lands exactly at the narration word's end | hero numbers only |
| **stamp** | 150ms scale 1.15→1.0 + opacity, no overshoot | the seal only |

Easing vocabulary: `power2.out`, `power3.out`, `sine.inOut`. No bounce, no
rebound, no ease-back.

### 5.3 Forbidden

Parallax, camera moves, 3D, bounce/rebound, glow, gradient animations,
particle/ambient/idle motion, loops, stock-footage grain, light sweeps.
A motion pattern not in §5.2 requires a spec amendment with a justification,
same as any post-first-render spec change.

## 6. Chart conventions

1. **Axes**: `--paper-dim` 1px; gridlines `--paper-dim` at 40% opacity; tick
   labels JetBrains Mono 22px. No axis arrows, no chartjunk.
2. **Series**: cost-adjusted = `--paper` 3px solid; raw (only when shown for
   contrast) = `--paper-dim` 2px dashed. Draw order: raw, cost-adjusted, bar.
   Points appear only when the line reaches them (reveal).
3. **Labels near objects** — direct labels, no detached legend, unless a
   legend is explicitly justified in the video spec.
4. **Gap fills** appear only after both curves make the gap meaningful.
5. **The bar** is always drawn (§4.3), never omitted for space or drama.
6. **Falsified results**: identical chart treatment, verdict color appears
   only in the verdict card and the scoreboard cell. The chart itself stays
   neutral; the position of the curve relative to the bar is the story.
7. Hero number placement: upper third, right of the chart's last data point,
   with a 1px `--paper-dim` rule above it. The number rolls (§5.2) to its
   final value.

## 7. Per-series treatment

| Series | Treatment |
|---|---|
| **Meta** | Plainest clothes: neutral palette only, **no accent color at all**. Method diagrams as connected nodes (prereg → seal → verdict); lifecycle as a literal timeline. The first video looks the most like the rules. |
| **Portfolio** | Table-forward ledger; rebalance diffs as `+`/`−` rows in `--paper-dim` (no P&L red/green, §2). |
| **Seal** | Amber-forward: `--seal-amber` allowed as the series accent; ends on the seal scene. |
| **Verdict** | Neutral for the first two-thirds; verdict color owns the final third (chart hero → verdict card → scoreboard row). Amber only on the bar. |
| **Build log** | Leans fully into the terminal aesthetic: monospace-dominant, framed as a console window with the commit SHA in the header. The one series where mono is the voice, not just the data. |

## 8. Thumbnails

Regenerable composition frame + pinned overlay; no hand-made art:

- Ink field, 12px `--paper-dim` border (same border as the disclaimer card —
  thumbnails visibly belong to the same system).
- Series tag top-left, JetBrains Mono 28px `--paper-dim`, uppercase.
- One hero element centered: the number, the verdict word, or the seal.
- Wordmark bottom-right, annotation size.

## 9. Implementation notes

- **Tokens**: `tokens.css` (this directory) holds the palette, type scale,
  spacing, and component classes for the pinned set pieces. Scenes import it
  via `@import "url(../../pipeline/style/tokens.css)"` (or a relative
  equivalent) — scenes never define palette values locally.
- **Fonts**: WOFF2 files vendored in `videos/pipeline/fonts/` with an
  `@font-face` block in `tokens.css`. The skeleton does not yet carry
  `@font-face`; wiring tokens.css + fonts into the skeleton is the first
  implementation step before the first render. Font files + checksums go in
  the build log.
- **CI**: theme-color drift check via `tools/scan_theme_colors.py` against
  this palette (any hex not in §2 fails the check unless in a documented
  exception list).

## 10. Change policy

Semver.

- **Major**: any pixel change to a pinned set piece (§4); removal or rename
  of a token; palette change. Disclaimer-card text changes additionally
  require an owner decision.
- **Minor**: new set piece, new motion verb (with justification), new
  per-series treatment.
- **Patch**: prose clarifications, no pixel change.

Every video's build log pins the style-spec version it rendered against.

## 11. Open items (owner decisions, not drift)

1. **Channel name / handle** — wordmark slot in the seal and bug waits on it
   (placeholder until settled).
2. **P&L color in Portfolio tables** — spec says no red/green (§2); confirm.
3. **Seal SFX** — spec says none (§4.2); one pinned CC0 thud would need
   approval.
4. **Captions** — standing proposal: always, committed SRT from the committed
   wav; bottom 132px caption-safe band assumes yes.
