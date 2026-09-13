# Video spec — meta-preregistration-rules

> Committed **before the first render** (VIDEO_CONCEPT §4.1). A video whose
> spec is not committed is not rendered. Pre-first-render: edit freely.
> Post-final: a spec change that alters shown content requires re-render +
> build-log note + append-only amendment entry below.

## Meta

| Field | Value |
|---|---|
| Slug | `meta-preregistration-rules` |
| Series | Meta (Phase 0 — the channel's first video, VIDEO_CONCEPT §10) |
| Working title | "How this channel works: preregistration, the seal, the verdict, the scoreboard" |
| Target runtime | 3:30–4:00 |
| Pipeline version | git SHA at authoring (recorded in build log at first render) |
| Style-spec version | 1.1.0 (`videos/pipeline/style/style-spec.md`) |
| Hyperframes version | 0.8.35 (`HF_VERSION` in `pipeline/render.sh`) |
| Template family | Meta v1 (first build of the family — blocks listed in beat sheet) |

Slug note: follows the series-prefix proposal in VIDEO_CONCEPT §11.2
(`meta-preregistration-rules`). Convention formally settles at video #2.

## Beat sheet

Series treatment (style spec §7): Meta runs on the neutral palette only —
no series accent. The pinned set pieces (seal scene, disclaimer card) keep
their pinned pixels regardless of series, per style spec §4.

Reveal discipline (style spec §5.1): every element appears on the narration
word that names it; ≥1 cue row per 10s of speech; stillness only after the
last word.

| # | On-screen content | Narration intent | Duration | Template block |
|---|---|---|---|---|
| 1 | Title card: wordmark `PREREGISTERED MONEY` + the brand mark (seal stamp, style spec §4.2), one line: "The name is the method." | Cold open. Establish what the channel is in one sentence. | 3s | `meta:title-card` |
| 2 | The failure mode: a monospace loop diagram — `run → nothing → re-run → nothing → re-run…` — drawing one cycle at a time; final state: three identical runs, one survivor, no label which is real. | Quant backtesting's failure mode: quietly re-running until something "works" (CONCEPT §1). Name it plainly. | 25s | `meta:loop-diagram` |
| 3 | Preregistration as the fix: three stacked fields type in — `hypothesis`, `data`, `the bar` — each stamped with `SEALED: <date>` before any run line appears. | Borrowed from clinical trials: commit the hypothesis, the data, and the bar *before* running (CONCEPT §1, §3). The commitment is the point. | 30s | `meta:prereg-fields` |
| 4 | Lifecycle diagram: four connected nodes draw left→right on cue — PREREG → SEAL → VERDICT → SCOREBOARD; a thin arrow returns from SCOREBOARD to PREREG (the next chapter). | The loop, stated once, calmly (CONCEPT §3, §5). Every video the channel makes lives inside this diagram. | 35s | `meta:life-cycle` |
| 5 | The seal, mechanically: append-only rule + "the git history is the audit trail" (CONCEPT §2) — then the **pinned seal scene**: `git commit` types in (the actual command that seals), seal stamp slams down, SHA held 3s. | What "sealed" means in practice: no more edits except logged amendments, and the SHA is shown on camera — this one. The SHA shown is this video's own spec commit (see Inputs). | 45s (incl. pinned seal scene ~7s) | prose beats + pinned `seal-scene` |
| 6 | The bar: a cost-adjusted series draws on a plain chart, then the amber bar line draws last with its mono tag `bar: ≥ <X> OOS CAGR` (example value, labeled `example`); a second small chart: same shape, series ends below the bar — no other difference. | Bars are pre-registered and always drawn (style spec §4.4/§6). Falsified results get identical production values — the curve's position relative to the bar is the story. | 30s | `meta:bar-chart` |
| 7 | The scoreboard ledger (pinned layout) with example rows: PR ID · hypothesis · date sealed · verdict · OOS · link — verdict cells in their colors; above it, three aggregate rows: total preregs, confirmed/falsified/inconclusive counts, **confirmation rate vs. null baseline**; below it, a dormant composite row labeled `dormant — no pins yet`. | The scoreboard is the product (CONCEPT §5): one table, aggregate stats, confirmation rate against a random-strategy baseline, and the composite of pinned strategies — dormant until the first pin. | 40s | pinned `ledger` + `meta:aggregate-rows` |
| 8 | The disclaimer card (pinned, verbatim CONCEPT §10) — full segment, not an end-card: the four bullets reveal on their narration words. | What preregistration does *not* fix (CONCEPT §10, VIDEO_CONCEPT §10). The rules segment of this video. | 30s | pinned `disclaimer-card` |
| 9 | Outro: "Same inputs → same pixels." wordmark + corner bug; pipeline determinism line (VIDEO_CONCEPT §1/§7). | The brand's promise about itself: the video pipeline is held to the same reproducibility bar as the research. Channel outro. | 12s | `meta:outro` |

**Citation of example values (beats 6–7).** The bar tag and ledger rows use
placeholder values — `PR-0000-000`-style IDs (never a real PR number, to
avoid colliding with the real ID sequence), example metrics, all labeled
`example` on screen in annotation type. No results doc exists yet, and the
no-uncited-number rule (VIDEO_CONCEPT §4.1) is satisfied by on-screen
`example` labels. No real PR number appears anywhere in this video.

## Number citations

Every figure the video will show, with its citation. **No uncited number.**

| Figure (as shown) | Value | Citation |
|---|---|---|
| Spec commit SHA (seal scene, beat 5) | `data/spec-sha.txt` — SHA of the commit that first commits this spec.md | source: `git rev-parse` of the first spec commit; file checksummed in build log |
| METHODOLOGY version (any on-screen reference) | v1.1, 2026-09-12 | `docs/METHODOLOGY.md` header |
| Bar tag example (beat 6) | labeled `example` on screen | rule text only: `docs/CONCEPT.md` §3–4 (the bar is pre-registered); no results doc exists |
| Ledger example rows (beat 7) | labeled `example` on screen | layout per `docs/CONCEPT.md` §5 (columns, aggregate stats, composite); no results/scoreboard data exists yet |
| Disclaimer bullets (beat 8) | verbatim, 4 bullets | `docs/CONCEPT.md` §10 (pinned card, style spec §4.6) |

No other figures appear. Nothing is computed in the composition.

## Inputs

| File | Checksum (sha256) | Source |
|---|---|---|
| `data/spec-sha.txt` | recorded at pin (commit after spec, before first render) | SHA of the commit that first commits this spec.md (`git rev-parse`) — the seal scene's SHA |

Rule-text sources (read-only, cited by path, not checksummed as data):
`docs/CONCEPT.md` (SHA at authoring — recorded in build log),
`docs/METHODOLOGY.md` (SHA at authoring — recorded in build log).

No other data files. No raw data, no datasets.

## Standing items

- [x] Disclaimer card (pinned, verbatim CONCEPT §10) — beat 8, full segment
- [ ] Scoreboard segment — **n/a for this video**: the scoreboard is empty;
      beat 7 shows the *layout* with example rows only. First real scoreboard
      segment lands with the first verdict video.
- [x] Channel outro — beat 9 (`meta:outro`)

## Production notes (for the build)

1. **Fonts + tokens wiring**: fonts vendored (Inter 400/600/700, JetBrains
   Mono 400/500 in `pipeline/fonts/`, checksums recorded below at commit);
   remaining task: `@import` tokens.css + setpieces.css into the
   skeleton/composition. Build log records font checksums.
2. **Meta template family v1** is born in this video:
   `meta:title-card`, `meta:loop-diagram`, `meta:prereg-fields`,
   `meta:life-cycle`, `meta:bar-chart`, `meta:aggregate-rows`, `meta:outro` —
   plus first exercise of the pinned `seal-scene`, `ledger`,
   `disclaimer-card` blocks.
3. **Captions**: committed SRT from the committed wav (standing proposal,
   VIDEO_CONCEPT §11.3), bottom 132px caption-safe band per style spec §3.
4. **Seal scene determinism**: the composition reads the SHA from
   `data/spec-sha.txt` (pinned, checksummed) — the SHA is a data input, not a
   computed value, keeping re-renders pixel-identical.
5. **TTS**: ElevenLabs v3 (creds pending — the audio glue is a pipeline task
   before first render; the wav commits to `audio/voiceover.wav` once
   generated).

## Amendments

(Append-only. Justification + affected beats + re-render SHA.)
