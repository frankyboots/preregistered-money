---
name: research-docs
description: "Use when designing or editing governing research docs."
version: 1.0.0
author: Preregistered Money
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [methodology, docs, design, governance, versioning]
    editorial_name: Research Docs
    editorial_description: "Design and versioning protocol for the project's governing research documents — approve the design first, then encode it with a version bump, change-log entry, and no retroactivity."
---

# Research Docs

Covers the project's governing research documents — the operational
contract between `docs/CONCEPT.md` (the *why*) and individual preregs
(instantiations): `docs/METHODOLOGY.md` today, and when they materialize
the composite recipe spec, `NULL_BASELINE.md`, and `PR_TEMPLATE.md`. This
skill is how to change them.

## Standing rules

1. **Design first, encode second.** Substantive design decisions go into
   chat before any edit: present them as a numbered list, each with a
   recommendation and one-line rationale, closed by an explicit question
   inviting disagreement. The user runs a design-review gate — draft only
   after sign-off. Small mechanical edits (typos, phrasing) may be applied
   directly.
2. **Scope check before writing.** Brand/product-level decisions belong in
   `CONCEPT.md` (open questions, §11, resolved as they settle);
   per-hypothesis decisions in the prereg. The methodology doc holds the
   defaults + mechanics every prereg inherits by silence — not the
   product, not the template, not the composite recipe (those are their
   own docs).
3. **Versioned-doc protocol** for every change to a governing doc:
   - bump the header version line (`vX.Y — date`);
   - append a change-log row describing exactly this change;
   - one commit per version, e.g. `docs(methodology): vX.Y — <summary>`
     (scope follows the doc per the research-commit skill's scope map).
4. **No retroactivity.** Before encoding a rule change, check whether any
   sealed preregs exist (grep `docs/preregistrations/` for `sealed: true`,
   if the dir exists). Sealed preregs stay judged under the
   `methodology: <sha>` they cite; the new version binds only preregs sealed
   after it. Say so in the commit body when sealed preregs exist; when none
   exist yet, no note is needed.
5. **Single source of truth — reference, never restate.** The data-file
   contract lives in `data/README.md` + `research/data/verify.py`; video
   production in `videos/VIDEO_CONCEPT.md`; high-level integrity rules in
   `CONCEPT.md`. Restated prose drifts and then two authorities disagree.
6. **Encode decisions mechanically.** A formula, a default table, and a
   normative ordering beat prose. Test: can a third party verify a sealed
   run from the published record without interpreting an adjective?

## Design principle: reporting ≠ judging

Every new reporting surface is added snooping surface — more published
numbers, finer resolution for "adjust until it works." So new statistical
reporting is **soft context by default**: required in the results doc,
engine-emitted, reproduced verbatim. Only preregistration at seal can
promote a reported quantity to a criterion. Partial or arbitrary slices
(a 78-month "decade", a custom window) can never be criteria — that is
overfitting to an arbitrary cut. The null baseline stays anchored to the
*default* criteria set; confirmations under extended bars are labeled as
such, not rate-comparable. Apply this principle to any future reporting
addition before it gets written down.

## Procedure

1. Read the current doc in full; check sealed state (`sealed: true` in
   `docs/preregistrations/`).
2. Present the design per rule 1; wait for the go-ahead on substantive
   decisions.
3. Apply the edits; bump the version line and append the change-log row in
   the same edit pass.
4. Commit per the `research-commit` skill (full checklist applies; atomic —
   the change-log row must describe exactly this commit and nothing else).
5. Report the commit SHA — prereg frontmatter citations
   (`methodology: <sha>`, via `git rev-list -1 HEAD -- <doc>`) depend on it
   being findable in history.
