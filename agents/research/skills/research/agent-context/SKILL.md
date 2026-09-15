---
name: agent-context
description: "Use when editing this agent's SOUL.md or MEMORY.md."
version: 1.0.0
author: Preregistered Money
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [soul, memory, context, scratchpad, persistence]
    editorial_name: Agent Context
    editorial_description: "File mechanics for this profile's persistent context: the profile-to-repo wiring, the MEMORY.md entry format, round-trip verification, and the sync/commit procedure."
---

# Agent Context

How to edit or seed this profile's two persistent-context files: `SOUL.md`
(persona + the context-strategy policy) and `MEMORY.md` (the cross-session
scratchpad). The *policy* — what each file is for and the three-entry
scratchpad shape (Recent / Queue / Next session) — lives in `SOUL.md` itself
and is always loaded; **this skill carries the file mechanics only.** Don't
restate the policy here.

## The wiring (know this before touching anything)

The profile home is `~/.hermes/profiles/research/`. Its contents are a mix of
symlinks and real files into the repo (`~/preregistered-money`):

- `memories/` -> repo `agents/research/memories/` — **symlink, one live file**.
  The `memory` tool reads/writes `MEMORY.md` here; a repo edit and a tool edit
  are the same file. No sync step needed.
- `skills/` -> repo `agents/research/skills/` — symlink, already shared.
- `config.yaml` -> repo `agents/research/config.yaml` — symlink (but gitignored;
  machine-local, never committed).
- `SOUL.md` — **NOT a symlink. Two separate regular files:** the live one in the
  profile home, and the git-tracked record at repo `agents/research/SOUL.md`.
  These are independent files that must be kept in sync by hand.

## Edit SOUL.md

1. Edit the **live** copy: `~/.hermes/profiles/research/SOUL.md` (reloads every
   message, no restart).
2. `cp` it over the repo copy so the git record matches:
   `cp ~/.hermes/profiles/research/SOUL.md ~/preregistered-money/agents/research/SOUL.md`
3. Commit under the `agents` scope (see the Commit section below:
   `docs(agents)` for substantive content, `chore(agents)` for routine
   state).

## Seed or edit MEMORY.md

1. Write entries as short declarative facts, **one entry per scratchpad job**
   (Recent / Queue / Next session, per the SOUL.md policy).
2. Join entries with a single `\n§\n` (a `§` on its own line). A `§` mid-entry
   splits the entry — it is the record separator.
3. Stay under the per-store budget (config `memory.memory_char_limit`,
   `memory.user_char_limit` — currently 5000 / 2500 chars). Never cite the code
   defaults (2,200 / 1,375): the profile config overrides them, and docs that
   state the defaults are wrong for this profile. The `memory` tool
   enforces the budget at write time; a hand-written file is not, so keep it
   small and trim the oldest Recent items before adding.
4. Verify it round-trips through the store's own parser before committing:
   split the file on `\n§\n`, confirm each non-empty chunk is a complete
   entry, and check the joined length is within budget (a quick `python3`
   one-liner is fine). A file that doesn't parse loses or merges entries
   silently when the next session loads it.

## Commit

`SOUL.md`, `MEMORY.md`, and the `memories/` docs (e.g. `README.md`) all live
under `agents/research/` — inside the research-commit boundary, never a seal,
no raw data. Scope is `agents` (per the research-commit scope map: SOUL.md,
MEMORY.md, skills, memories/README.md all live there) with type per the change
(`chore(agents)` for routine scratchpad state, `docs(agents)` for substantive
content). Runtime lock files under `memories/` are
gitignored — never stage one. The scratchpad's evolution is part of the
public record, so commit the changes rather than leaving them untracked.
Re-check `git status --short` immediately before committing — the video agent
commits to the same working tree and its commits can land between your
check and yours (research-commit checklist item 8).

## Standing rules

- **Memory is the scratchpad, not the store of procedure.** If a lesson is a
  how-to, it belongs in a skill (`skill_manage`), not in MEMORY.md. Memory
  holds the current handoff: what landed, what's queued, what to pick up next
  session — and points at the repo, never duplicates it. When memory and the
  repo disagree, the repo wins.
- **SOUL.md has two copies — whichever you edit, verify the pair.** The
  documented procedure is live→repo, but a repo-side edit (one-line patch) is
  equally real, and it leaves the live file stale because the persona reloads
  from the *live* copy each message. After any SOUL.md edit from either side:
  `diff ~/.hermes/profiles/research/SOUL.md ~/preregistered-money/agents/research/SOUL.md`
  must be clean (propagating repo→live is fine — the live copy reloads without
  restart). A repo-only commit of a SOUL.md change is a known bad state.
- **One `§`-delimited entry per job.** Multi-paragraph blobs in one entry
  inflate the budget and blur the scratchpad into a log.
- **`memory` `replace` targets one entry, via `old_text`.** It is not a
  whole-file swap: `action=replace` takes `old_text` (a short unique substring
  identifying the target entry) plus `content` = the complete new text for that
  one entry. Two failure shapes: a missing/wrong `old_text` fails loudly (re-issue
  with `old_text` set); and `content` containing a `\n§\n` separator is split into
  multiple entries on write — passing whole-scratchpad content into a
  single-entry replace swaps one entry for three while the other old entries
  survive, leaving a five-entry file with duplicates. To rewrite the entire
  scratchpad, either replace each entry individually (three ops) or write the
  file directly and run the round-trip parse check above. After any op: confirm
  `entry_count` is exactly 3 — a sudden count change means entries were added or
  lost, and the fix is the direct file write, not more tool ops.
