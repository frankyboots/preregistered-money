---
name: project-skill-authoring
description: "Use when creating or editing project agent skills."
version: 1.0.0
author: Preregistered Money
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [skills, authoring, skill-authoring, process, curation]
    editorial_name: Project Skill Authoring
    editorial_description: "How to author, place, and land skills in this project's agent skill trees: the description budget, atomic batches, class-level naming, the bind-mounted placement, frontmatter shape, and commit+push."
---

# Project Skill Authoring

Creating or editing skills in this project's agent skill trees
(`agents/research/skills/` from this profile; the video side has its own tree
and is outside this profile's commit boundary — never touch it). Covers
authoring constraints, placement, frontmatter, and landing (commit + push).
Neighboring skills: `curator-skill-review` (reviewing curator edits that land
out-of-session), `agent-context` (SOUL.md / MEMORY.md — context files, not
skills), `research-commit` (the commit mechanics themselves).

## Authoring constraints

- **Description budget: ≤ 60 chars.** `skill_manage` create rejects longer
descriptions and the whole `operations` batch rolls back — every skill in the
batch fails, not just the offender. Shape: one sentence, trigger first ("Use
when <trigger>."), ends with a period; the skill index truncates at 57 chars,
so the routing signal must fit there. Depth goes in the body and
`editorial_description`, never the description.
- **Batches are atomic.** `create` must precede that skill's other ops. Verify
description lengths before batching multiple creates; when in doubt, one
create per call.
- **Class-level names, topical support files.** Name the class of task, not
the session artifact — no PR numbers, incident names, or `fix-X`. If the name
only makes sense for today's work, fold the lesson into an existing umbrella
(a rule in SKILL.md or a topic-named `references/` file) instead of creating.
`references/` files are named by topic (decision tables, recipes, domain
notes), never by date/incident. Extending an umbrella beats a growing flat
list of narrow skills.
- **Delegation, not restatement.** Link to sibling skills for shared
procedure (commit → `research-commit`, wiki → `research-wiki`, governing docs
→ `research-docs`, data → `data-snapshots`) — a delegation-map table, never
duplicated prose. Restated procedure drifts; the brand is single-source-of-
truth at the process level too.
- **SKILL.md = always-on rules; references/ = topical depth.** Standing gates
and user preferences live in SKILL.md whole; depth that only some instances
need goes in `references/<topic>.md`.

## Placement (bind-mounted — no sync step)

The profile's skills dir IS the repo tree (bind mount, identical inodes —
`stat -c '%i'` on a file in both paths if in doubt): `skill_manage` writes
land in `agents/research/skills/` directly and show up as untracked/modified
git files. They MUST be committed — the repo is the public record; an
uncommitted skill exists only on this machine. Research-domain skills live
under the `research/` category subdir; cross-cutting workflow skills
(`research-commit`, `curator-skill-review`, this one) sit top-level. Follow
the existing layout; do not reorganize opportunistically.

## Frontmatter shape

Copy the shape from any existing project skill (e.g. `research-commit`):
`name`, `description` (the ≤ 60-char one), `version` (semver — bump on
substantive change), `author: Preregistered Money`, `license: MIT`,
`platforms`, and `metadata.hermes` with `tags`, `editorial_name`,
`editorial_description` (the editorial description may be long — it is NOT the
60-char one; that budget applies to the top-level `description` field only).

## Landing (commit + push)

- Commit per `research-commit` (boundary gate, atomicity, push policy — push
  after each commit; the skills are public record): `docs(agents)` for new or
  corrected skill content, `chore(repo)` when accepting curator-authored edits
  (cite the curator session ID from `agents/research/skills/.curator_ledger.jsonl`
  in the body — the ledger is gitignored, so the commit body is the permanent
  audit record).
- Runtime state never enters git: `.usage.json`, `.usage.json.lock`,
  `.curator_ledger.jsonl`, `.hub/`, `.bundled_manifest` (gitignored). A new
  runtime-state pattern appearing untracked → add a `.gitignore` line, never
  commit it.
