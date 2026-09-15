---
name: spec-and-validation
description: "Use when writing a spec with its validation design."
version: 1.0.0
author: Preregistered Money
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [process, spec, validation, test-design, engineering]
    editorial_name: Spec and Validation
    editorial_description: "Phase 1 of spec-driven delivery: how to write numbered, verifiable requirements and a validation strategy that answers 'how do we know it was delivered fully' before any implementation."
---

# Spec and Validation (Phase 1)

Phase 1 of `spec-driven-delivery`: produce `spec.md` + `validation.md` in
`research/specs/<slug>/` and get owner sign-off **before any code exists**.
The spec gate mirrors the video side's "spec gates render": no committed
spec, no implementation.

## spec.md — requirements, not prose

Structure:

1. **Goal** — one paragraph: what the deliverable is, who consumes it,
   what it must make possible.
2. **Requirements** — numbered `R1`, `R2`, … Each requirement:
   - **testable without vibes** — a third party could decide pass/fail
     from the requirement text plus the repo; no adjectives as bars
     ("robust", "clean", "fast" are not requirements);
   - **atomic** — one requirement, one verifiable claim. A compound
     requirement hides a gap in the review table;
   - **normative where the project has a bar** — cite the governing doc
     when a requirement inherits from it (e.g. "R3: cost model implements
     `docs/METHODOLOGY.md` §3.1–§3.4 exactly" — the citation IS the spec;
     reference, never restate the formula).
3. **Design constraints** — non-functional bars that aren't requirements
   (determinism: no network, no wall-clock in the research path, no
   randomness without a recorded seed — per METHODOLOGY §2.2; dependencies;
   toolchain; where the code lives).
4. **Out of scope** — explicit list (walk-forward, null generator, etc.).
   What's cut is part of the spec; "we'll add it later" without a named
   follow-up is a scope leak.
5. **Open questions** — anything undecided, each with a recommendation.
   Owner closes these at sign-off. A spec with unresolved open questions
   is not sealable.

## validation.md — how we know it was delivered fully

One section per requirement: **R → verification method + evidence form.**
Methods, strongest first:

1. **Automated unit test** — the default. Name the test (file::test) so
   the review table can cite it.
2. **Invariant / canary test** — for properties rather than values
   (look-ahead canary: mutating post-decision data must leave output
   byte-identical; idempotence; hash determinism).
3. **Known-answer check** — hand-computed fixture (e.g. a 2-month
   cost-model example computed on paper) that pins the formula's meaning.
4. **Owner review** — for judgment requirements (candidate menus, design
   taste). Record who + date + what was looked at.
5. **Deferred** — allowed only with the follow-up named and the reason
   (e.g. "needs real data" → deferred to phase 3 exit).

**Edge-case enumeration (mandatory section, no exceptions).** Before
sign-off, sweep the input space and list every boundary the spec must
survive. For this project the standing checklist is:

- data gaps / short series (window shorter than expected, missing months)
- window boundaries (usable-from/to honored; rows outside refused)
- pre-1954-07 (no FEDFUNDS → rf = 0, flagged)
- gold before 1970 (loader must refuse)
- snapshot refresh (a new checksum is a new snapshot; old pins still verify)
- config-hash sensitivity (every field that changes behavior changes the hash)
- empty/zero results (empty window, zero turnover, zero weights)
- concurrent writer (video agent commits interleaved — verify before commit)
- determinism across environments (same inputs, same platform → same bytes)

Each edge case gets: expected behavior (from which R), and its verification
method. An edge case with no requirement behind it is a spec hole — either
add the requirement or record it as out of scope.

## The sign-off gate

Present both docs to the owner with: (a) the numbered requirements,
(b) the open questions with recommendations, (c) any requirement the owner
is the arbiter of (criteria bars, candidate menus, design taste). Get
explicit sign-off; record it in `spec.md` footer (`status: approved`,
`approved: <date>`, `by: owner`). Then commit both docs (one commit,
`docs(specs): <slug> spec + validation design`) — **this commit is the
gate**; implementation may start after it and only after it.

## What this phase does NOT do

- No scaffolding, no "while I'm here" code. The temptation to start the
  obvious loader during spec writing is how specs rot to match the code.
- No restating governing docs (METHODOLOGY, CONCEPT, data contract) — cite
  sections. If the governing doc is ambiguous where the spec needs it,
  that's an open question or a `research-docs` change, not a restatement.
