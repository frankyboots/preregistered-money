---
name: spec-driven-delivery
description: "Use when building a research-side engineering deliverable."
version: 1.0.0
author: Preregistered Money
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [process, spec-driven, engineering, delivery, paper-trail]
    editorial_name: Spec-Driven Delivery
    editorial_description: "The research-side engineering loop: committed spec and validation design gate implementation, every phase leaves a paper trail in the repo, and handoff is a checklist, not vibes."
---

# Spec-Driven Delivery

The standard loop for **engineering deliverables on the research side**:
the backtest engine, the null-baseline generator, `scoreboard/build.py`,
tooling, and versioned specs that have no code of their own. The brand
already runs this loop for *hypotheses* (prereg → seal → run → verdict);
this skill gives the same shape to *engineering*, so the paper trail is
consistent across both tracks and build-in-public works at process level,
not just content level.

**Not for:** preregs and results docs — those follow `docs/CONCEPT.md` §3
and the `research-docs` / `research-commit` skills. Don't apply this loop's
doc layout to them.

## The five phases and their gates

```
1 SPEC + VALIDATION   →  committed spec.md + validation.md  (no code before this)
2 IMPLEMENTATION PLAN →  committed plan.md (phases, exit criteria, commits)
3 IMPLEMENT (phased)  →  each phase exits only when its exit criteria pass
4 REVIEW              →  review.md: requirement-by-requirement evidence table
5 HANDOFF + INGEST    →  commits clean, wiki updated, video side unblocked
```

- **Gates are commits, not intentions.** A phase that did not commit its
  artifact did not happen. The repo is the paper trail: no private process
  notes, no "it's in the conversation" evidence.
- **Phase 3 is gated per phase, not at the end.** Each phase in `plan.md`
  declares exit criteria (tests green, manual check, owner look). The next
  phase does not start until the previous one's criteria are verified and
  committed. This is what keeps a long build reviewable incrementally.
- **Owner review is a named step, not a hope.** Phases 1 and 4 end in
  owner review (the spec gate and the review gate). Present the artifact,
  get the sign-off, record who + date in the doc. Mechanical work between
  gates is the agent's to proceed with.

## Doc layout (per deliverable)

```
research/specs/<slug>/
├── spec.md         # requirement R1..Rn + design constraints   (phase 1)
├── validation.md   # per-R verification method + edge cases    (phase 1)
├── plan.md         # phases, exit criteria, commit decomposition (phase 2)
└── review.md       # R→evidence table, edge-case sweep, sign-off (phase 4)
```

Central location so the paper trail is one browsable place; each spec links
to its code (and the code's README links back). `<slug>` matches the code
dir slug (e.g. `research/specs/backtest-engine/` for `research/backtest/`).

## Degenerate case: sealed spec with no code

Some deliverables are *only* a spec (the composite recipe, the
null-baseline generator doc). The loop still applies: phases 1 + 2
(spec, validation of *decidability* — can a third party decide compliance
from the text alone?, and the design review), then a versioned seal per
the `research-docs` protocol. Phase 3 is empty; phases 4/5 still run
(review of the spec text, handoff to whichever consumer cites it).

## Versioning vs the seal ceremony

- `seal(prereg):` commits are **reserved for preregs** (`research-commit`
  skill). An engineering spec is never sealed with that type.
- Versioned spec docs (composite recipe, `NULL_BASELINE.md`) follow the
  `research-docs` versioned-doc protocol: version line + change-log row,
  changes are new versions, append-only, never retroactive. A spec adopted
  by a downstream deliverable is treated like a sealed prereg: changes to
  what was built are new versions, not edits.
- The deliverable's code may be freely iterated *before* its review passes;
after review passes, behavior changes follow the normal commit discipline
  and, where a requirement is fixed, trigger a review.md re-check row.

## Delegation map (reference, never restate)

| Concern | Skill |
|---|---|
| Phase 1 — writing spec + validation | `spec-and-validation` |
| Phase 4 — the review table, gap rules | `review-against-spec` |
| Phase 5 — handoff, wiki, video checklist | `delivery-handoff` |
| Any commit on the research side | `research-commit` |
| Changes to a governing/versioned doc | `research-docs` |
| Wiki ingest (phase 5) | `research-wiki` (mechanics: `llm-wiki`) |
| Data snapshot changes (phase 3, if any) | `data-snapshots` |
