---
name: review-against-spec
description: "Use when reviewing a deliverable against its spec."
version: 1.0.0
author: Preregistered Money
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [process, review, verification, quality, paper-trail]
    editorial_name: Review Against Spec
    editorial_description: "Phase 4 of spec-driven delivery: the requirement-by-requirement evidence table, the edge-case sweep, and the gap rules — fix, amend, or new spec."
---

# Review Against Spec (Phase 4)

Phase 4 of `spec-driven-delivery`: judge the implemented deliverable
against `spec.md` + `validation.md`, produce `review.md`, and either close
the loop or send gaps back. The review is a **table, not a narrative** —
the narrative is where gaps hide.

## review.md — the evidence table

One row per requirement, no exceptions (an R with no row is itself a
finding):

| R | Requirement (short) | Verification (method from validation.md) | Evidence | Status |
|---|---|---|---|---|
| R3 | Cost model per METHODOLOGY §3.1–3.4 | unit + known-answer | `tests/test_costs.py::test_fee_drag` + `fixtures/2month.example.md` | pass |

Rules:

- **Evidence is concrete and re-runnable:** test name + how to run it,
  command + output location, commit SHA, or owner-review record. "It works
  when I try it" is not evidence. A reviewer must be able to re-derive the
  status from the repo alone (the third-party test — CONCEPT §3, applied to
  engineering).
- **Status values:** `pass` | `fail` | `gap` (requirement exists, nothing
  implements it) | `waived` (owner explicitly waived, with date + reason
  recorded) | `deferred` (named follow-up per validation.md).
- **The edge-case sweep gets its own section:** every edge case from
  validation.md, same evidence discipline. A sweep that skips a row is
  incomplete — mark it, don't delete it.
- **Findings section:** everything observed that is *not* a requirement
  failure — missing edge cases the validation missed, spec ambiguities the
  implementation forced, better designs noticed late. Each finding is
  dispositioned: fixed now / amended into spec / follow-up (named).

## Gap rules (the accountability part)

- **fail or gap → fix and re-check the row** (new evidence, same R), or
  **amend the spec**, never silently drop the requirement.
- **Spec amendment:** a requirement that was wrong or missing is fixed in
  `spec.md` + `validation.md` with a dated, justified note ("R7 amended
  2026-09-XX: original wording assumed X; implementation revealed Y;
  owner approved"). The amendment is a commit of its own
  (`docs(specs): <slug> spec amendment — <reason>`). Amending after
  implementation started is fine *before* review passes; after the review
  passes and the deliverable is handed off, the spec is adopted — changes
  follow the versioning rules in `spec-driven-delivery` (new version,
  append-only, never retroactive), not inline edits.
- **A bar change is never a fix.** If the review reveals the *bar* was
  wrong (threshold, candidate set, definition), that is a new spec / new
  version with owner sign-off — mirroring METHODOLOGY §6.4 (a change that
  alters what was run or the bar is a new prereg, not an amendment). The
  same discipline applies to engineering: a shipped deliverable judged
  against an amended bar is a new delivery.
- **Owner sign-off closes the review.** Record `reviewed: <date>`,
  `by: owner` in review.md footer. The owner's job is the rows marked
  `waived`/`deferred` and any bar-adjacent finding — not re-running the
  tests.

## What this phase does NOT do

- No new features during review. A finding that needs new work goes to a
  follow-up (named, with a spec of its own if it's a new deliverable).
- No restating the spec — the table cites R-ids.
- No "close enough" statuses. The vocabulary is fixed (pass / fail / gap /
  waived / deferred); inventing a sixth status is how accountability leaks.
