# Narration — meta-preregistration-rules

Voice: Helen (default, professional en-brit). No beat overrides.
Written to the spec's beat sheet order; the beat map from the committed wav
is the timing source of truth (spec durations are planning targets).
Trim pass 2026-09-12: ~527 words, targeting the 3:30-4:00 runtime.

## beat-01

The name is the method.

## beat-02

The failure mode. You backtest a strategy and it loses. Change the window, add a filter, run it again. Change something else. Each variation is defensible on its own, but nobody keeps a ledger of every variation. No one can say which one produced the numbers. Three identical runs, one survivor, no label for which is real.

## beat-03

The fix comes from clinical trials: preregistration. Before the run, you write down three things. The hypothesis, in one falsifiable sentence. The data. And the bar, a number to clear after costs. The document goes to git; the commit is the seal, and git is the notary. After that the document is append-only: anyone can diff it against the run config to check nothing moved. The commitment is the point.

## beat-04

Four states. The prereg: hypothesis, data, and bar, written down before anything runs. The seal: the commit that locks the document. The verdict: the result, judged by the pre-registered criteria, not by how it looks. Confirmed, falsified, or inconclusive. Then the scoreboard: every prereg in one public table. And an arrow back to the prereg: the post-mortem becomes the next prereg. Every video on this channel lives inside this diagram.

## beat-05

What does sealed mean in practice? After the commit, the document is append-only, and the git history is the audit trail. The same rule holds for runs: a result counts only if it matches the sealed config. The seal is one command, on screen now. The commit produces a SHA, recorded in the document and on the scoreboard. The SHA on screen is the commit that first committed this spec: the channel's first sealed artifact. If the scoreboard shows a different one, that is a bug.

## beat-06

The bar: a number to reach, after costs. The chart draws the cost-adjusted series, then the bar, an amber line, last. The value in the tag is an example, labeled on screen: no results document exists yet. The bar is drawn the same way whether the strategy passes or fails: same chart, same bar. The only difference is where the curve ends relative to the line, and that is the story.

## beat-07

The scoreboard is the product. One table: each row a prereg, with its ID, hypothesis, seal date, verdict, out-of-sample number, and link to results. The rows on screen are examples, labeled as such. Above the table, the aggregate rows: total preregs, the confirmed, falsified, and inconclusive counts, and the confirmation rate against a null baseline: the fraction random strategies pass by chance. Below the table, the composite: the strategies the owner decides to trade. Until the first pin it is dormant, and the label says so.

## beat-08

The same four lines on every video. Educational content, not investment advice. Backtest results are estimates under stated assumptions; live performance will differ, possibly badly. Preregistration controls data snooping; it does not control overfitting in pre-seal choices, data quality, or market regime change. Past performance, including preregistered, costed, out-of-sample past performance, is the weakest predictor in finance.

## beat-09

Same inputs, same pixels. The video pipeline is held to the same reproducibility bar as the research. If you cannot reproduce a number from this repository, it is a bug.
