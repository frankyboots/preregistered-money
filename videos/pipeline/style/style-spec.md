# Style Spec

**Version: 1.1.0**
Status: v1 — approved at the branding session (2026-09-12).

Changelog:
- 1.1.0 (2026-09-12): channel name settled — wordmark `PREREGISTERED MONEY`,
  handle `@preregisteredmoney`. New set piece §4.2 (brand mark: the seal
  stamp holding the bar); the seal ring and the corner bug now use it —
  those slots were declared placeholders pending exactly this decision
  (§11.1), and no output had been rendered against 1.0.0, so no shipped
  pixels change. Set pieces renumbered: bar §4.4, verdict card §4.5,
  disclaimer §4.6, ledger §4.7.
- 1.0.0 (2026-09-12): palette, type, set pieces, motion verbs (draft,
  owner review pending).

This file is the "what" of the channel's visual system (VIDEO_CONCEPT §6).
The concept document is the "why and how". Every build log pins this version.
Machine-readable tokens live in `tokens.css` (same directory); pinned set-piece
classes in `setpieces.css`. Scenes import both — scenes never hardcode palette
values or set-piece styles.

---

## 1. Design stance

The visual language looks like the method: a **ledger, a seal, an audit
trail**.

1. **Data-forward, faceless, minimal motion.** No on-camera presence, no
   presenter, no stock footage. The visuals are the data.
2. **Color is semantic only.** A color on screen must carry meaning (verdict,
   "untested", or emphasis). The base is nearly monochrome so the few colors
   that appear read as verdicts, not decoration.
3. **Change follows speech.** The frame builds itself as the narration names
   things (§5.1). Engagement comes from relevance-ordered reveals, not from
   pixel activity. No lights, no ambient motion.
4. **Determinism is the brand.** Same committed inputs → same pixels. Pinned
   versions, pinned fonts, pinned set pieces.

## 2. Palette (7 tokens, total)

| Token | Hex | Role |
|---|---|---|
| `--ink` | `#0B0E11` | Every background. Deep charcoal, never pure black. |
| `--paper` | `#E8E6E1` | All body text, chart series lines, rules. |
| `--paper-dim` | `#6B7078` | Axes, gridlines, captions, timestamps, the corner bug. |
| `--seal-amber` | `#C89B3C` | Anything pending/untested: Seal series accents, the pre-registered bar line, "awaiting verdict" states. |
| `--confirmed` | `#3FA46A` | Confirmed verdicts only. |
| `--falsified` | `#C4453C` | Falsified verdicts only. Same production values as confirmed — color is the only difference. |
| `--inconclusive` | `#8A9099` | Inconclusive verdicts only. |

Color-discipline rules:

- Chart series lines are **always** `--paper` (or `--paper-dim` for raw, §6.2).
  Verdict colors never appear on chart lines.
- No gradients, no glow, no neon. No blue/purple SaaS palette, no sci-fi HUD.
- Portfolio P&L figures do **not** use red/green — that would collide with
  verdict semantics. Deltas are `--paper-dim` with `+`/`−` glyphs. (Standing
  decision; a change is an owner decision, not drift.)
- The only amber in a Verdict video is the bar line.
- No hex in a scene file may exist outside this palette; CI drift check via
  `tools/scan_theme_colors.py`.

## 3. Typography

Fonts (pinned, SIL OFL, vendored WOFF2 in `videos/pipeline/fonts/`,
`@font-face` in `tokens.css`, checksums in the build log):

- **Inter** — display and body prose. Weights: 400, 600, 700.
- **JetBrains Mono** — all data. Weights: 400, 500.

**The mono rule: every number on screen is JetBrains Mono with tabular
figures.** SHAs, dates, bars, CAGRs, table cells, axis labels — no
exceptions. Prose is human, data is machine; the mono/sans contrast is the
brand.

Scale — three prose sizes, two data sizes. No other sizes:

| Level | Token | Size | Use |
|---|---|---|---|
| Hero | `--fs-hero` | 144px | Headline OOS number, verdict word |
| Title | `--fs-title` | 52px | Scene titles |
| Body | `--fs-body` | 30px | Narration-supporting on-screen text |
| Table | `--fs-table` | 24px | Tabular data cells only |
| Annotation | `--fs-anno` | 22px | Axis labels, tags, the corner bug, disclaimer title, captions |

Layout: 1920×1080. 80px outer safe margin. The bottom 132px is
**caption-safe**: no data element may sit in it.

Captions: Inter 400, `--fs-body`, `--paper`, single line, bottom band
(committed SRT from the committed wav, standing proposal).

## 4. Set pieces (the visual identity)

These are pinned elements defined in `setpieces.css`. Any pixel change to a
set piece is a **major** version bump and, for the disclaimer card, an owner
decision.

### 4.1 Corner bug

Upper-left, 40px margin, JetBrains Mono 20px `--paper-dim`:

```
PREREGISTERED MONEY · PR-YYYY-NNN · sealed YYYY-MM-DD · <short-sha-8>
```

Fades in with each scene (200ms). Every frame self-identifies — the
reproducibility promise, visually. Wordmark: `PREREGISTERED MONEY`
(channel name settled 2026-09-12, §11).

### 4.2 The brand mark (seal stamp with the bar)

The channel's profile logo and the mark inside the seal ring. Owner decision
2026-09-12: the certification stamp holds the bar — an ascending `--paper`
line crossing a `--seal-amber` horizontal. Source of truth:
`style/brand-mark.svg` (double ring, single-stroke weights, committed).
Channel art (banner, profile logo) renders from this mark per the
`channel-art` skill; the banner composition is the "bar" concept — curve,
bar, wordmark — all inside the 1546×423 all-device safe zone.

### 4.3 The seal scene

The channel's signature moment. Sequence (~6–8s total, fixed):

1. Ink background. A monospace line types in over ~1.2s:
   `git commit  <full-sha>` (left→right, 1 char/tick) — a plain commit: the
   seal never rewrites history (CONCEPT §2).
2. The seal stamp — the brand mark (`style/brand-mark.svg`, §4.2) —
   scales in with **stamp** motion (150ms, 1.15→1.0, no overshoot, no
   bounce). This is the only impact motion in the system.
3. The full SHA sits inside the ring below the mark, `--seal-amber`,
   JetBrains Mono, held 3s before scene cut.

Archetype: certification stamp / tamper-evident sticker, not a SaaS logo.
Sound: none (standing; a pinned CC0 thud would require an owner decision).

### 4.4 The bar

Pre-registered bars are **always drawn** on every chart that shows the
relevant metric: a solid `--seal-amber` 3px horizontal line across the plot
area, tagged above it at the right end in JetBrains Mono 22px
(`.bar-tag`): `bar: ≥ 6.0% OOS CAGR` — exact text from the prereg's bar
field, no paraphrase. Drawn **last**, after the series lines. The verdict is
read by eye: the curve ends above or below the line.

### 4.5 The verdict card

One layout for all three outcomes. Ink background, no border, no decoration:

- One word: `CONFIRMED` / `FALSIFIED` / `INCONCLUSIVE`, Inter 700,
  `--fs-hero`, centered, in the verdict color.
- Same position, same size, same 2s hold, in all three. No euphemism
  variants. Falsified gets identical production values; the post-mortem
  beat follows as a separate scene.

### 4.6 The disclaimer card

Verbatim CONCEPT §10, rendered identically in every video — same pixels
every time. An integrity anchor, not a decoration.

- Layout: ink field, 1px `--paper-dim` border, 40px padding, left-aligned.
- Title `HONEST LIMITATIONS` (annotation, `--paper-dim`, letterspaced).
- The four bullets, JetBrains Mono `--fs-body`, `--paper`, line-height 1.6:

> - Educational content, not investment advice.
> - Backtest results are estimates under stated assumptions; live performance will differ, possibly badly.
> - Preregistration controls data snooping; it does not control overfitting in pre-seal choices, data quality, or market regime change.
> - Past performance (including preregistered, costed, out-of-sample past performance) is the weakest predictor in finance.

Source of truth for the text is `docs/CONCEPT.md` §10. If CONCEPT §10
changes, the card changes in the same release with a major style-spec bump
and an owner decision recorded.

### 4.7 The scoreboard ledger

Full-bleed table, `--paper` on `--ink`, thin `--paper-dim` rules:

- Row height 56px, cells `--fs-table`. Header row: JetBrains Mono, uppercase,
  `--paper-dim`, letterspaced.
- Columns: PR ID · hypothesis (one line) · date sealed · verdict · headline
  OOS number · link (URL text).
- Verdict cell in the verdict color; everything else `--paper`.
- The composite row (pinned strategies) is distinguished by a 2px `--paper`
  rule above it, not by color.
- Rows reveal one at a time on their narration cue (200ms each), in
  scoreboard order. No full-table fade-in.

## 5. Motion system

### 5.1 The narration-anchored reveal rule (anti-staleness)

No scene may be a dead hold. The rule is **relevance ordering**, not pixel
activity:

1. **Reveal on naming.** Every data element (series, point, row, number,
   label, title) appears during the word of the narration that names it —
   not before, not after. Frame state at time *t* = the set of elements
   whose cues are ≤ *t*.
2. **No pre-naming.** A data element is never fully visible more than 2s
   before its cue. Axes and frame may pre-exist at scene open.
3. **Change floor.** Within any continuous 10s span of speech there is at
   least one state change: a new element, a number roll, a table row, or a
   line extension. Long scenes are allowed; cueless scenes are not. The beat
   sheet is checkable against this at REVIEW.
4. **Silence is a script problem.** If narration is silent mid-scene for more
   than 3s, the script is tightened or a cue is added — it is never filled
   with motion.
5. **Earn the stillness.** The final hold is the one sanctioned stillness:
   the settled, most-informative state of the scene. It is what the proof
   frames check.

Every scene's beat timeline therefore carries at least one cue row per 10s
of narration. A scene that can't satisfy the change floor is overlong: split
it or cut the script.

### 5.2 The five verbs

| Verb | Params | Where |
|---|---|---|
| **cut/fade** | hard cut default; 200ms fade for open/close only | scene changes |
| **reveal** | 250ms opacity + 12px slide-up, `power2.out`; table rows 200ms | every named element; scoreboard rows |
| **draw** | 600–900ms left→right, `power2.out`; the bar 400ms | chart series (raw first, cost-adjusted second, bar last) |
| **roll** | 600ms, one count-up, lands exactly at the narration word's end | hero numbers only |
| **stamp** | 150ms scale 1.15→1.0 + opacity, no overshoot | the seal only |

Easing vocabulary: `power2.out`, `power3.out`, `sine.inOut`. No bounce, no
rebound, no ease-back.

### 5.3 Forbidden

Parallax, camera moves, 3D, bounce/rebound, glow, gradient animations,
particle/ambient/idle motion, loops, stock-footage grain, light sweeps.
A motion pattern not in §5.2 requires a spec amendment with a justification,
same as any post-first-render spec change.

## 6. Chart conventions

1. **Axes**: `--paper-dim` 1px; gridlines `--paper-dim` at 40% opacity;
   tick labels JetBrains Mono 22px. No axis arrows, no chartjunk.
2. **Series**: cost-adjusted = `--paper` 3px solid; raw (only when shown for
   contrast) = `--paper-dim` 2px dashed. Draw order: raw, cost-adjusted,
   bar. Points appear only when the line reaches them (reveal).
3. **Labels near objects** — direct labels, no detached legend, unless a
   legend is explicitly justified in the video spec.
4. **Gap fills** appear only after both curves make the gap meaningful.
5. **The bar** is always drawn (§4.4), never omitted for space or drama.
6. **Falsified results**: identical chart treatment; the chart stays
   neutral. Verdict color appears only in the verdict card and the
   scoreboard cell. The curve's position relative to the bar is the story.
7. **Hero number placement**: upper third, right of the chart's last data
   point, with a 1px `--paper-dim` rule above it. Rolls (§5.2) to its final
   value.

## 7. Per-series treatment

| Series | Treatment |
|---|---|
| **Meta** | Plainest clothes: neutral palette only, **no series accent color at all**. Method diagrams as connected nodes; lifecycle as a literal timeline. The first video looks the most like the rules. |
| **Portfolio** | Table-forward ledger; rebalance diffs as `+`/`−` rows in `--paper-dim` (no P&L red/green, §2). |
| **Seal** | Amber-forward: `--seal-amber` allowed as the series accent; ends on the seal scene. |
| **Verdict** | Neutral for the first two-thirds; verdict color owns the final third (chart hero → verdict card → scoreboard row). Amber only on the bar. |
| **Build log** | Leans fully into the terminal aesthetic: monospace-dominant, framed as a console window with the commit SHA in the header. The one series where mono is the voice, not just the data. |

## 8. Thumbnails

Regenerable composition frame + pinned overlay; no hand-made art:

- Ink field, 12px `--paper-dim` border (same border as the disclaimer card —
  thumbnails visibly belong to the same system).
- Series tag top-left, JetBrains Mono `--fs-anno` `--paper-dim`, uppercase.
- One hero element centered: the number, the verdict word, or the seal.
- Wordmark bottom-right, annotation size.

## 9. Implementation notes

- **Tokens**: scenes import `tokens.css` and `setpieces.css` (relative
  import from the video dir). Scenes never define palette values locally.
- **Fonts**: vendored WOFF2 in `videos/pipeline/fonts/`; `@font-face` in
  `tokens.css`; font files + checksums go in the build log.
- **CI**: theme-color drift check via `tools/scan_theme_colors.py` against
  the §2 palette.

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

Resolved (2026-09-12): **channel name / handle** — `Preregistered Money`,
`@preregisteredmoney` (handle already claimed). Wordmark is `PREREGISTERED
MONEY` in the bug, seal scene, and channel art; the brand mark (§4.2) is
locked in `style/brand-mark.svg`.

Still open:

1. **P&L color in Portfolio tables** — spec says no red/green (§2); confirm.
2. **Seal SFX** — spec says none (§4.3); one pinned CC0 thud would need
   approval.
3. **Captions** — standing proposal: always, committed SRT from the committed
   wav; the bottom 132px caption-safe band assumes yes.
