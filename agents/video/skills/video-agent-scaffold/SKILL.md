---
name: video-agent-scaffold
description: "Use when editing video agent SOUL.md, memories, or config."
version: 1.0.0
author: Preregistered Money
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [scaffold, soul, memory, profile, dual-agent]
    editorial_name: Video Agent Scaffold
    editorial_description: "Maintenance rules for the video agent's own context layer: the dual SOUL.md copies, the symlinked memories/skills dirs, and the SOUL-vs-memory-vs-skills division of labor."
---

# Video Agent Scaffold

Maintaining the video agent's own files — identity, memory, config, skills — in the dual-agent `preregistered-money` setup. Video *content* work is out of scope here (see `video-commit`, `end-to-end-video-playbook`).

## File map (know this before editing anything)

| File | Live (runtime reads) | Repo (auditable record) |
|---|---|---|
| SOUL.md | `$HERMES_HOME/SOUL.md` = `/home/frank/.hermes/profiles/video/SOUL.md` | `/home/frank/preregistered-money/agents/video/SOUL.md` |
| memories/ | symlink → repo `agents/video/memories/` | same (single source of truth) |
| skills/ | symlink → repo `agents/video/skills/` | same (single source of truth) |
| config.yaml | machine-local (localhost LLM endpoint) — gitignored, never commit | — |

- **SOUL.md is TWO independent files, not a symlink** (verify with `stat %i` on both before relying on this). The runtime injects only the profile copy, verbatim, as system-prompt slot #1. The repo copy is the committed record for git review and re-provisioning.
- `$HERMES_HOME` for this agent is the profile dir, not `~/.hermes` — never hardcode the default home.

## Rules

1. **Every SOUL.md edit goes to both copies, byte-identical.** Edit repo copy → copy to profile copy → verify with `diff`. Pitfall: editing only the repo file changes nothing at runtime; editing only the profile file loses the change on re-provision and leaves the record stale.
2. **SOUL and memory only take effect next session** (frozen snapshot at session start). Tell the user the change lands on the next session — don't claim it's live.
3. **Division of labor, never cross it:** SOUL.md says *how* to work (identity, style, the task-tracker contract); MEMORY.md holds *state* (tracker entry: in-flight video slug + lifecycle stage SPEC → DRAFT → REVIEW → FINAL → PUBLISH, next 1–3 actions, blockers, open owner decisions); skills hold *procedure*. State bloats into SOUL/skills, or procedures parked in memory, and the context layer rots.
4. **Commit SOUL.md changes per `video-commit`**: `chore(agents):` scope. When a change seeds or redefines the tracker contract, commit the updated MEMORY.md in the same or a follow-up commit — both agents' owners treat committed memory as the auditable state.
5. **Dual-agent consistency:** the research agent (`agents/research/`) mirrors the same scaffold pattern. When changing a *shared convention* (e.g. the task-tracker contract), apply the equivalent edit to the research side's SOUL.md too — the owner expects the two agents to stay consistent. Machine-local and agent-specific content stays per-agent.
6. **The `memory` tool treats the whole MEMORY.md as ONE entry** (clobbered the tracker twice in one session before this rule existed): a `replace` swaps the ENTIRE file, so `content` must be the complete new tracker text — a partial snippet silently deletes the rest — and `usage`/`entry_count` in the response describe that single entry, not the file. For small or surgical tracker updates, skip the memory tool: use the `patch` tool directly on the repo file (the profile `memories/` is a symlink to the same file, so one edit lands in both), then verify `wc -c` stayed in the sane range — a sudden collapse is a clobber; `git show HEAD:agents/video/memories/MEMORY.md` restores it.

## Session-start behavior (from SOUL contract)

Open with the memory tracker, then verify against live state (`git log`/`git status` in the repo, in-flight video's build.log, `docs/results/` + scoreboard). Memory is a pointer; git is the record — on disagreement, the repo wins and memory gets fixed, not the other way around.
