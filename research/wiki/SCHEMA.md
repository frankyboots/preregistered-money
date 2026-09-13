# Wiki Schema

> Domain schema for the `preregistered-money` research wiki.
> This schema is the third layer: it constrains how the agent builds and
> maintains the wiki below it.

## Domain

Domain knowledge for the preregistered-money project: asset classes, datasets
and data-quality facts, investment concepts, and the literature/evidence that
preregistrations are designed against. Covers: passive benchmarks (SPX, 10Y
treasuries, gold), data-vintage and reconstruction caveats, backtesting and
cost methodology, and the design evidence behind each prereg.

## Authority Boundary (read this before writing any page)

- The wiki is **evidence and design context**, not authority. Normative
  decisions (windows, cost assumptions, target vol, criteria) are made through
  design review and encoded in `docs/METHODOLOGY.md` or in a prereg doc.
  Wiki pages may *inform* those decisions and flag contradictions; they may
  never override them.
- **Sealed preregs are immutable.** The wiki never amends, contradicts, or
  overrides a sealed prereg. New knowledge gets its own page; disagreements
  with a sealed prereg are flagged in the page frontmatter
  (`contested: true`) and surfaced to the owner.
- **Reference, never restate.** The data-file contract lives in
  `data/README.md` + `research/data/` (manifests, checksums, `verify.py`).
  The wiki links to dataset pages, never duplicates manifest content. If the
  manifest and a wiki page disagree, the manifest wins; fix the wiki page.
- Wiki commits follow the `research-commit` skill (scope `wiki`).
- **Citable state:** a prereg may pin the wiki's state at design time by
  citing `wiki: <sha>` in its frontmatter (the SHA of the last commit
  touching `research/wiki/` before the prereg was written). This is the only
  way wiki content feeds a prereg without breaking no-retroactivity.

## Conventions

- File names: lowercase, hyphens, no spaces.
- Every wiki page starts with YAML frontmatter (below).
- Use `[[wikilinks]]` between pages — minimum 2 outbound links per page.
  Wikilinks may also point at **repo docs outside the wiki** by path, e.g.
  `[[../../research/data/datasets/gold.md]]`, for cross-references into the
  data contract.
- Bump `updated` on every edit.
- Every new page goes into `index.md` under the correct section.
- Every action is appended to `log.md`.
- **Provenance markers:** pages synthesizing 3+ sources append
  `^[raw/articles/source-file.md]` at the end of paragraphs whose claims come
  from a specific source.

## Frontmatter

```yaml
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | comparison | query | summary
tags: [from taxonomy below]
sources: [raw/articles/source-name.md]   # repo-doc refs allowed: research/data/datasets/gold.md
confidence: high | medium | low          # required when sources < 2
contested: true                           # set when the page has unresolved contradictions
contradictions: [other-page-slug]
---
```

`confidence` is **required whenever `sources:` has fewer than 2 entries** —
unsourced or single-source claims must never read as settled fact.

### raw/ Frontmatter

Raw sources get a small frontmatter block so re-ingests can detect drift:

```yaml
---
source_url: https://example.com/article   # original URL, if applicable
ingested: YYYY-MM-DD
sha256: <hex digest of the body below the frontmatter>
---
```

The hash is computed over the body only (everything after the closing `---`).
On re-ingest of the same URL: recompute, skip if identical, flag drift and
update if different.

## Tag Taxonomy

Every tag on a page must appear here. Add a new tag to this list **before**
using it.

- **Assets:** asset-class, index, bond, commodity, treasury
- **Data:** dataset, data-quality, vintage, license
- **Method:** backtest, walk-forward, cost-model, risk, allocation, benchmark
- **Domain:** valuation, macro, monetary-policy, market-structure
- **Meta:** comparison, controversy, prediction, open-question

## Page Thresholds

- **Create a page** when an entity/concept appears in 2+ sources OR is central
  to one source.
- **Add to existing page** when a source mentions something already covered.
- **DON'T create a page** for passing mentions, minor details, or things
  outside the domain.
- **Split a page** when it exceeds ~200 lines.
- **Archive a page** when fully superseded — move to `_archive/`, remove from
  index, convert inbound wikilinks to plain text + "(archived)".

## Entities

Pre-declared, grounded by the data contract — one page per asset class the
project trades or benchmarks against (SPX, 10Y treasuries, gold). Entity
pages link to the corresponding `research/data/datasets/` manifest. New
entities are created only when they meet the Page Thresholds (e.g. a new
instrument enters a prereg).

## Concepts

**Dynamic by design.** No pre-declared concept inventory exists or will be
maintained. Concept pages are created purely on-demand when a concept meets
the Page Thresholds, and the tag taxonomy above is the only constraint.
Concepts that arise during spec-analysis sessions (comparisons, queries) are
expected to spawn concept pages as the wiki compounds — that growth is
wanted, not sprawl, as long as each page clears the thresholds and carries
provenance.

## Comparison Pages

Side-by-side analyses (e.g. benchmark candidates for a prereg). Expected to
populate during **spec-analysis sessions** — the sessions that study previous
specs to prepare the next one. Structure: what is compared and why,
comparison dimensions (table preferred), verdict or synthesis, sources.

## Query Pages

Filed answers that would be painful to re-derive. Expected to populate during
spec-analysis sessions. Trivial lookups are not filed.

## Update Policy

When new information conflicts with existing content:

1. Check the dates — newer sources generally supersede older ones.
2. If genuinely contradictory, note both positions with dates and sources.
3. Mark the contradiction in frontmatter: `contradictions: [page-name]`,
   `contested: true`.
4. Flag for owner review in the next lint report.

Never silently overwrite.

## Standing rules for this wiki (project-specific, beyond the llm-wiki skill)

- **No stubs.** Do not create empty or near-empty placeholder pages. A page
  with no sourced claims and no analysis is not a page.
- **Data ≠ wiki.** Raw data files never enter the wiki. `raw/` holds
  documents only (articles, papers, transcripts, images). Datasets are
  governed exclusively by the `data-snapshots` contract.
- **Seal hygiene.** A wiki commit never bundles a seal commit. Seals are
  `seal(prereg):` commits containing exactly one prereg; wiki work has its own
  commits with scope `wiki`.
