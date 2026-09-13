---
name: research-wiki
description: "Use when working in the project research wiki."
version: 1.0.0
author: Preregistered Money
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [wiki, knowledge-base, research, markdown, provenance, preregistration]
    editorial_name: Research Wiki
    editorial_description: "How the in-repo LLM-wiki is built and maintained for preregistered-money: the authority boundary, dynamic concepts, citable SHA state, and the data≠wiki rule — mechanics deferred to the generic llm-wiki skill."
---

# Research Wiki

The preregistered-money research wiki lives **in-repo** at `research/wiki/`,
not at the `llm-wiki` skill's external default. Use it when building, ingesting
into, querying, or linting the wiki. This skill carries the project-specific
wiring; the generic `llm-wiki` skill carries the mechanics (ingest/query/lint
procedures, orientation protocol, templates, frontmatter, pitfalls). **Load
`llm-wiki` for the how; this skill tells you where it bends for this project.**

## Location

```bash
WIKI=/home/frank/preregistered-money/research/wiki
# or: WIKI="${WIKI_PATH:-$HOME/wiki}" — this profile's .env sets WIKI_PATH to the in-repo path.
```

`WIKI_PATH` is set in *this profile's* `.env`. Do not touch the default
profile's `.env` (it points at an unrelated `~/Projects/wiki`).

## Authority boundary (the load-bearing rules)

- **Wiki is evidence, not authority.** Normative decisions (windows, costs,
  target vol, criteria) are made by design review and encoded in
  `docs/METHODOLOGY.md` or a prereg. A wiki page may inform or flag; it may
  never override.
- **Sealed preregs are immutable.** The wiki never amends or contradicts a
  sealed prereg. New knowledge gets its own page; disagreement with a sealed
  prereg is marked `contested: true` and surfaced to the owner.
- **Reference, never restate.** The data contract lives in `data/README.md`
  + `research/data/`. Dataset pages *link* to the `research/data/datasets/`
  manifest; they never duplicate manifest content. Manifest wins on conflict.
- **Data ≠ wiki.** `raw/` holds documents only (articles, papers, transcripts,
  images). Raw data files never enter the wiki. Datasets are governed solely
  by the `data-snapshots` contract.

## Domain decisions (owner-approved)

- **Concepts are dynamic.** No pre-declared concept inventory. Concept pages
  are created on demand when they meet SCHEMA.md Page Thresholds. The tag
  taxonomy is the only constraint. Growth is wanted, not sprawl, so long as
  each page clears thresholds and carries provenance.
- **Comparisons and queries populate during spec-analysis sessions** — the
  sessions that study previous specs to prepare the next one. Don't pre-seed
  them.
- **`confidence:` is required when `sources:` has fewer than 2 entries.**
  Single-source or unsourced claims must not read as settled fact.
- **No stubs.** No empty or near-empty placeholder pages. A page needs sourced
  claims or analysis.

## Citable SHA state (how the wiki feeds a prereg)

A prereg may pin the wiki's design-time state by citing `wiki: <sha>` in its
frontmatter — the SHA of the last commit touching `research/wiki/` *before*
the prereg was written. This is the only way wiki content feeds a prereg
without breaking no-retroactivity. Compute it with:

```bash
git rev-list -1 HEAD -- research/wiki
```

Do not cite a SHA that includes the prereg's own commit; pin the state the
prereg was designed against, not the state after it landed.

## Committing wiki work

- Scope `wiki` (see `research-commit` skill's scope map). Path: `research/wiki/`.
- **Seal hygiene:** a wiki commit never bundles a seal commit. Seals are
  `seal(prereg):` commits containing exactly one prereg; wiki work has its own
  commits. Wiki commits also never bundle unrelated work (standard atomicity).

## First real use

PR-2026-001's benchmark study (SPX/10Y/gold passive benchmark selection).
Its design-evidence sources are the first ingests — expect them to spawn
entity pages (the three asset classes, linked to their `research/data/datasets/`
manifests) and the first comparison page (benchmark candidates).
