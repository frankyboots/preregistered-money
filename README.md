# Preregistered Money

A YouTube channel and this repository, where trading strategies are researched
the way a clinical trial is run: every hypothesis is written down, sealed with
a git commit, and judged against criteria fixed *before* the decisive run.

**The name is the method.** Preregistration comes from clinical trials and
psychology, where it exists to stop researchers from quietly re-running
analyses until something "works". Quant backtesting has the same failure mode,
at industrial scale. We make the discipline the brand.

## How it works

1. **Preregistration.** Hypothesis, data spec, strategy spec, cost model, and
   pass criteria are written into a prereg doc.
2. **Seal.** The doc is committed to git; the commit SHA becomes the timestamp
   and the seal. Git is the notary.
3. **Verdict.** Results are published in a separate commit that references the
   seal and judged against the preregistered bar. Falsification is a success
   state — it gets the same production value as a confirmation.
4. **Scoreboard.** A multi-year public record of confirmed / falsified /
   inconclusive, plus the aggregate track record of the strategies the owner
   has decided to actually trade (pinned). A null baseline — random
   strategies through the identical pipeline — is the published reference for
   what passes by chance.

Anyone can diff a preregistration against the final run config and verify
nothing moved.

## What is in this repository

| Path | What it is |
|---|---|
| `docs/CONCEPT.md` | The method: integrity rules, protocol, scoreboard, pinning |
| `docs/METHODOLOGY.md` | Data, backtesting, and cost-model methodology |
| `docs/preregistrations/`, `docs/results/` | Sealed preregs and published results — land with the first verdict episode |
| `research/` | Data contracts (`data/` manifests + checksums + verify script) and the analysis wiki |
| `data/` | Raw-data drop zone (gitignored; the contract is `research/data/`) |
| `videos/` | One directory per video: composition + data inputs + build log — every published frame is regenerable from the repo |
| `videos/pipeline/` | Shared, versioned production tooling: style spec, render pipeline, TTS glue, channel art |
| `agents/` | The two agent profiles (research / video) — skills, prompts, and memory — the mechanical split that keeps the video side from ever touching run configs or producing numbers |
| `scoreboard/` | Upcoming: the generated scoreboard — the product |

## Reproducibility

- Every video directory is a self-contained HyperFrames project; a re-render
  from the committed directory must reproduce the published pixels.
- Every on-screen figure traces to a published results doc (or the
  prereg/scoreboard for recaps); the video side never computes numbers.
- Build logs pin the inputs — data snapshot, template version, TTS
  voice/model, encoder settings — for every render.

Educational content, not investment advice.

## License

[Apache-2.0](LICENSE). Vendored components carry their own licenses where
present (e.g. `videos/pipeline/LICENSE`).
