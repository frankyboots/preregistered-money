# Scene spec 05 — the seal, mechanically

Status: SPEC (Phase B). Template: prose beats + pinned `seal-scene` (style spec §4.3).

## Scene Identity

- Scene ID: `scene-05`
- Working title: seal
- Window: **95.24–128.57s** (beat-05, `audio/timing/beat-map.json`; speech 95.31–127.26, hold 127.26–128.57)
- Output format: 1920×1080, 24fps, draft quality (Phase C)
- Source composition: `composition/scene-05.html`
- Render output: `renders/scene-05.mp4`

## User Intent

- Objective: what "sealed" means in practice — append-only after the commit,
  the git history as the audit trail, the same rule for runs — then the
  **pinned seal scene**: the sealing command types in, the brand mark stamps
  down, the SHA holds. The signature moment of the channel.
- Tone: mechanical, declarative. A certification, not a celebration.
- Must communicate: the rule (no edits except logged amendments; the history
  is the audit trail), and that the SHA on screen is *this video's own* spec
  commit — the channel's first sealed artifact.
- Must not feel like: a SaaS logo sting, a magic moment, a loading screen.

## Inputs

- Narration: beat-05, `narration.md` (87 words).
- Cue source: `audio/timing/words.json` (master sha256 `4cfb0cb0…`).
- Data inputs:
  - Spec commit SHA `86140f927343296bb2efc390288ac56b2c9865e2` —
    `data/spec-sha.txt` (file sha256 `225809172e884309cab78e4fb11be46bece0dc67856d7a3cdf9dc003acf4f29d`),
    committed snapshot; citation in `spec.md` Number citations row 1. The only
    number in the scene; read from the file at build time, never computed and
    never typed into markup (composition reads `../data/spec-sha.txt`, per
    `composition/README.md`).
- Brand mark: `style/brand-mark.svg` (committed snapshot, sha256
  `eccdc43f…0eb986b`).
- Corner bug: standard, fades in at scene open (200ms).

## Visual Direction

- Background: `--ink`.
- Layout (1920×1080):
  1. **Title zone** (top-left under the bug, y≈88–148): `the seal,
     mechanically` (Inter 600, `--fs-title`, `--paper`).
  2. **Command line** (centered on x=960, y≈190):
     `git commit  86140f927343296bb2efc390288ac56b2c9865e2` — JetBrains Mono
     `--fs-body` (30px), `--paper`. 52 chars ≈ 936px wide.
  3. **Prose column** (left, x=80, y≈240–400; five mono lines,
     `--fs-anno`, 34px leading):
     - L1 `--paper`: `after the commit: append-only`
     - L2 `--paper-dim`: `the git history is the audit trail`
     - L3a `--paper`: `a result counts only if`
     - L3b `--paper`: `it matches the sealed config`
     - L5 `--paper-dim`: `recorded in the document and on the scoreboard`
     All ≤607px wide; the seal ring's left edge at these y-values is ≥x=714 —
     no collision.
  4. **Seal zone** (the pinned set piece, style spec §4.3): brand mark
     (`style/brand-mark.svg`) centered at (960, 600), **640px** diameter
     (spans x 640–1280, y 280–920). Full SHA in JetBrains Mono, 18px,
     `--seal-amber`, centered x=960, y≈700 — 40 chars ≈ 439px, inside
     the inner ring below the mark (inner-ring chord at dy=111 ≈ 501px
     → ≈31px clearance per side). Held until the cut (≈14.4s — the
     pinned ≥3s stillness before cut is satisfied).
     - Amended (Phase C build, no design change): the SHA line renders at
       top y=699 (center ≈711) — the committed mark's ascending-line round
       cap (endpoint (814,692), cap bottom ≈700) measured intruding ~5px
       into the glyph tops at the original top 689. The +10px shift clears
       the cap (≥4px verified in proof); the SHA remains inside the outer
       ring.
     - Amended (owner nit, 2026-09-14 — the hash must sit INSIDE the
       stamp): the SHA size is **18px, a local override of the 22px
       `--fs-anno` token** (the spec previously pinned `--fs-anno`). At
       22px the rendered hash ink measured 532px (x694–1225) while the
       inner ring's chord at the line's depth (dy=111) is only ≈501px —
       the last ~13px of ink on each side crossed the inner ring, so the
       hash read as not fitting the stamp. 40 × 10.98 ≈ 439px at 18px
       leaves ≈31px per side inside the inner ring (verified on the
       re-render; see the scene-05 fix build-log entry). Top 699 and the
       whole-line reveal are unchanged — the smaller ascenders only
       improve the cap clearance; the t=114.44 proof cell still holds.
- Colors: `--paper` + `--paper-dim` for title/command/prose; the only scene
  amber is the SHA (the seal, §4.3 step 3) plus the mark's own pinned bar
  stroke (part of the committed mark, not scene coloring). No verdict colors
  — nothing is judged here.
- Motion: reveal (250ms) for title, prose lines; type for the command (the
  pinned §4.3 cadence: full 52-char line in ~1.2s ≈ 23ms/char — the 100ms/char
  cadence of scenes 02–03 applied to short node labels does not fit the
  pinned ~1.2s); stamp (150ms, 1.15→1.0) for the ring — the only stamp in the
  system. No roll (the SHA is a string, not a hero number). Nothing after the
  last word.
- Open state: at window start the frame is ink + corner bug only — nothing
  here is "frame" (every element is named by the narration), so nothing
  pre-exists.
- Case follows the narration: `git` (the tool/command line) vs `Git`
  (proper noun, scene-03 convention).

## Beat Timeline

Times are word starts from `words.json`; visual completes within ≤250ms
unless noted.

| Time | Word | Visual action | Required proof |
|---|---|---|---|
| 95.24 | — | open: ink, corner bug fades in; no scene elements | first frame |
| 95.78 | `sealed` | title `the seal, mechanically` reveals | t=96.00 |
| 100.02 | `append` | prose L1 `after the commit: append-only` reveals | t=100.30 |
| 102.30 | `audit` | prose L2 `the git history is the audit trail` reveals | t=102.60 |
| 106.10 | `result` | prose L3a/L3b (`a result counts only if / it matches the sealed config`) reveal as a unit | t=106.40 |
| 110.50 | `command` | command line types in left→right (~1.2s, 52 chars, pinned cadence; lands ~111.7, noted) | t=111.90 fully typed |
| 111.80 | `now.` | seal ring (brand mark) stamps in (150ms, pinned) — the seal, "on screen now" | t=111.95 ring settled (before end of "now." 112.06) |
| 114.16 | `SHA` | full SHA inside the inner ring below the mark reveals (`--seal-amber`, mono 18px) | t=114.44 |
| 116.50 | `scoreboard.` | prose L5 `recorded in the document and on the scoreboard` reveals | t=116.80 |
| 127.26 | (speech ends) | final hold — SHA held, nothing moves (pinned ≥3s hold, §4.3; stillness covers 125.57–128.57) | t=128.00 = final state |
| 128.57 | — | hard cut to scene-06 | t=128.56 stable |

Cue-keying notes: title keys to `sealed` (the word that names the object the
scene explains — "What does sealed mean in practice?" is the opening move).
The command line keys to `command` ("one command"); the stamp keys to `now.`
("on screen **now**" — the seal appears as "now" lands, 40ms after the line
finishes typing, keeping the pinned type-then-stamp order); the SHA keys to
`SHA`. Prose lines key to the words that name each clause (`append`, `audit`,
`result`, `scoreboard.`).

Change floor: 31.95s continuous speech (95.31–127.26, no gap >3s), 8 state
changes — per 10s span: 3 (95.3–105.3), 4 (105.3–115.3), 1 (115.3–125.3) ✓.
The last span's stillness is the pinned set piece's SHA hold — sanctioned
stillness (§4.3, §5.1 rule 5). No pre-naming ✓ (empty open; every element on
its word).

## Continuity

- First frame: ink + corner bug only (hard cut from scene-04's final frame:
  full lifecycle diagram → empty seal frame).
- Last frame: title, prose column, typed command, stamped ring with the amber
  SHA inside — the settled seal, held.
- Transition in: hard cut from scene-04 (the lifecycle's SEAL node, made
  mechanical — the cut carries it).
- Transition out: hard cut to scene-06 (the bar; its spec opens from ink).
- Carryover frames: none.

## QA Checklist

- Final-frame proof: **t=128.00** — title, prose column, command, stamped
  ring with amber SHA, settled.
- Boundary proofs: t=100.30 (append-only line in), t=106.40 (L3 unit in),
  t=111.90 (command fully typed), t=111.95 (ring settled), t=114.44 (SHA in
  amber), t=116.80 (L5 in), t=128.56 (hold stable to cut).
- Caption proof: lowest element is the ring's bottom edge (y=920); the
  bottom 132px band (from y=948) is empty.
- Audio sync: L1 by end of "append" (100.38); L2 by end of "trail." (102.88);
  L3 unit by end of "result" (106.50); command fully typed by t=111.90 (the
  line is *being named* from "command", 110.50); ring settled by end of
  "now." (112.06); SHA visible by end of "SHA" (114.88); L5 by end of
  "scoreboard." (117.00).
- Known risks: (1) SHA width — CLOSED by the owner-nit amendment
  (2026-09-14): at 22px the hash ink (532px) crossed the inner ring's
  chord (≈501px at dy=111); rebuilt at 18px (≈439px) with ≈31px
  clearance per side inside the inner ring, verified on the re-render.
  (2) Command line width at 30px mono ≈ 936px — fits the 1760px safe
  area; verify it clears the ring's top edge (27px at rest, 27px at the
  1.15× stamp scale — re-check in probe). (3) Typing cadence (23ms/char)
  vs the 100ms/char of scenes 02–03 — different verb instance (pinned
  ~1.2s full line, §4.3); verify the line reads as "typing", not a
  flash, at draft quality. (4) Prose column L5 (607px) vs the ring's
  left edge at y≈396 (x≈714) — 27px gap, verify in probe. (5) Mark's
  ascending-line cap vs the SHA glyph tops — realized: cap bottom ≈700
  intruded ~5px at SHA top 689; amended SHA to top 699 (see Seal zone
  note), clearance ≥4px in proof (improved by the 18px amendment).
- Acceptance: lint 0 errors; final-frame proof matches layout; SHA on screen
  byte-identical to `data/spec-sha.txt`; the only amber pixels are the SHA
  and the mark's pinned bar (`scan_theme_colors.py` clean); no other number
  in the scene.
