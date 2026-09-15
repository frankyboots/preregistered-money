---
name: delivery-handoff
description: "Use when handing off a finished research deliverable."
version: 1.0.0
author: Preregistered Money
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [process, handoff, video, wiki, interface]
    editorial_name: Delivery Handoff
    editorial_description: "Phase 5 of spec-driven delivery: the research side's guarantees for the video side — citable results, parseable frontmatter, regenerable scoreboard.json — plus wiki ingest."
---

# Delivery Handoff (Phase 5)

Phase 5 of `spec-driven-delivery`: turn a reviewed deliverable into what
the rest of the project (and the public) can consume. This is the
**interface between the two agents**: the video agent has declared it
blocked on the research side producing its inputs — this skill is the
checklist that makes the handoff a gate, not a vibes check. It defines what
the **research side must guarantee**; it never directs the video side
(its own loop lives in `agents/video/skills/` — outside this agent's
commit boundary, don't touch it).

## Two deliverable types, two handoff shapes

### A. Hypothesis deliverable (a prereg + its results)

The video side's three legitimate inputs (`videos/VIDEO_CONCEPT.md` §3) —
results doc, prereg doc + scoreboard, derived data extracts — must all
exist and be citable. The checklist, in order:

1. **Results doc** at `docs/results/<PR>-results.md`, committed
   (`docs(results): …`), with machine-readable frontmatter exactly per
   METHODOLOGY §6.3: `pr_id, seal_sha, config_hash, run_id, methodology,
   verdict, date` — plus who assigned the verdict.
2. **Every number is citable.** Every figure the video may show traces to
   a line in the results doc (or prereg/scoreboard for recaps). Audit: the
   results doc contains the headline metrics, the criteria table
   (threshold / observed / pass-fail, hard+soft), the per-decade tables
   (§4.1), both eras (index + investable), and capacity notes. If the
   video needs a number not in the doc, that's a new prereg or a
   follow-up run — not an email with a number.
3. **Seal integrity:** the prereg doc is sealed, `seal(prereg):` commit
   exists, and the results doc's `seal_sha` matches it. `config_hash` in
   the results doc matches the run log line (`research/strategies/<slug>/
   runs.jsonl`) and the run is type `verdict`, status `ok`.
4. **Scoreboard regenerated** — `scoreboard/build.py` run, `chore(scoreboard)`
   commit. Until `build.py` exists, the scoreboard row is recorded in the
   handoff note as "pending build.py" and the video side is told the
   scoreboard segment is not yet available.
5. **Handoff note** — a short message (or a committed
   `research/handoffs/<PR>.md` if the notes pile up): PR id, verdict,
   results-doc path, seal SHA, config hash, which series fits (Portfolio /
   Seal / Verdict per CONCEPT §8), and any caveat the video must carry
   (e.g. "OOS window spans the rf boundary; results doc flags it").

### B. Engineering deliverable (engine, build script, tooling)

1. **Review passed** — `research/specs/<slug>/review.md` shows owner
   sign-off; no open `fail`/`gap` rows.
2. **README in the code dir** — what it is, how to run it, what it emits,
   determinism guarantees, and a link back to `research/specs/<slug>/`.
   The video side may cite the tooling in Build-log series; the README is
   what makes that citation checkable.
3. **Consumers wired** — if the deliverable feeds the video (e.g.
   `scoreboard/build.py`), its output contract is met: `scoreboard.json`
   **and** `SCOREBOARD.md` emitted together, regenerable, with the JSON
   carrying every figure the scoreboard segment renders (the video's CI
   checks its numbers against `scoreboard.json`).
4. **Wiki ingest** (below), then the handoff note as in A.5.

## Wiki ingest (both types)

Per `research-wiki` (load `llm-wiki` for mechanics):

- **Ingest design lessons, not process log.** A comparison page for a
  benchmark study, a concept page if thresholds are met, entity pages for
  new asset classes/datasets (linking to `research/data/datasets/` — never
  duplicating manifests). The per-decade tables and run details stay in the
  results doc; the wiki gets the *read* (what the regimes show), cited.
- **Comparisons/queries populate during spec-analysis sessions** — a
  finished study is exactly such a session; don't leave the comparison
  page for "later."
- **Confidence:** single-source claims carry `confidence:` per the schema.
- **Citable state:** note `git rev-list -1 HEAD -- research/wiki` in the
  handoff note — the next prereg pins that SHA as its design-time wiki
  state.

## Commit discipline for the handoff itself

- Each checklist item that lands a commit follows `research-commit`
  (atomic; scopes: `results`, `scoreboard`, `wiki`, `repo`).
- The handoff note commit (if a file) is `docs(repo)` or `docs(strategy)`
  as fits; it is the last commit of the delivery and names the review
  SHA it closes.
- Boundary check still applies: handoff artifacts never stage
  `videos/**` or `agents/video/**` — the note *addresses* the video side;
  it never writes to it.
