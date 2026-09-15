---
name: curator-skill-review
description: "Review curator's pending skill changes in git status."
version: 1.1.0
author: Preregistered Money
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [git, curator, skills, review, research]
    editorial_name: Curator Skill Review
    editorial_description: "Review pending skill changes the Hermes curator made outside user sessions: verify every claim against the repo, classify runtime state as ignored, and commit what's accepted."
---

# Curator Skill Review

The repo's `agents/research/skills/` is the **live research profile's skills directory** (bind-mounted — same inodes; check with `stat -c '%i'` on a file in both paths). The Hermes **curator** (self-improvement process) patches and creates skills outside user sessions, so its work lands in the working tree as pending git changes. **Pending skill changes in `git status` are curator-made until the user says otherwise** — review them, don't assume.

Commits follow the `research-commit` skill (boundary gate, message format, atomicity) — this skill only adds the review half.

## Procedure

1. **Inventory:** `git status --porcelain=v1` in the repo root. Separate the pending items into (a) skill content, (b) runtime state, (c) everything else (anything outside `agents/research/skills/` + `.gitignore` needs its own judgment — it is *not* a default curator artifact).
2. **Read the ledger:** `agents/research/skills/.curator_ledger.jsonl` (if present) is the curator's audit trail: one JSON line per action with `actor`, `action` (patch/create), `skill`, `evidence.session_id`, and before/after `sha256` per file. It tells you exactly what changed, when, and in which session. Note: the ledger is (or should be) gitignored — it does not enter the audit trail, so the commit message must cite the session ID instead.
3. **Review each pending skill file:** read the full `SKILL.md`, then **verify every factual claim against the repo** — paths it references, scripts (run them), frontmatter fields it asserts exist in real files, gitignore rules it cites, tool availability. The review is the verification pass: a skill that instructs future sessions to trust a script that fails, or a manifest field that doesn't exist, is worse than no skill. On failed claims: fix the skill (patch), fix the repo (separate commit), or reject.
4. **Classify untracked files — commit vs ignore.**
   - Commit: skill content (`<skill-name>/SKILL.md` and its `references/`/`scripts/`/`templates/`/`assets/` support files).
   - Ignore (add to `.gitignore`, mirroring the other agent's side): runtime state — `.usage.json`, `.usage.json.lock`, `.hub/`, `.curator_ledger.jsonl`, `.bundled_manifest`, vendored bundled dirs (`autonomous-ai-agents/`). If a new runtime-state pattern appears untracked, the fix is a `.gitignore` line, never a commit.
5. **Decide per file: accept / edit / reject.**
   - Rejecting: untracked → delete the file; modified → `git restore <path>`. Report the rejection and why to the user (do not append to the curator's ledger — that file is the curator's).
   - Accepting with edits: patch the working-tree file before staging.
6. **Commit atomically and push, one message per commit:** stage *per commit* and commit *per commit* — a `.gitignore` fix and the skill acceptance are two commits, not one. The message must describe exactly the files in that commit (see Pitfall 1). Cite the curator session ID in the skill-acceptance commit body (the permanent audit record, since the ledger is gitignored). Push after each commit per the `research-commit` Push policy.
7. **Verify:** `git status --porcelain=v1` → clean; then prove the committed content is exactly what the curator wrote: `git show HEAD:<path> | sha256sum` must equal the ledger's final `after` hash for that file (only when accepted as-is; edited files won't match, and that's expected).

## Pitfalls

- **Commit message must match commit contents.** Staging everything then committing with a message that describes only part of it produces a commit whose message lies — and the message is audit trail. Stage per commit, commit per commit. (Real incident: one commit intended for a `.gitignore` fix swallowed two skill files; fixed by `git reset --mixed HEAD~1` and re-committing split, while the commit was still local.)
- **`git reset --mixed HEAD~1` unstages everything.** After it, re-stage deliberately per commit; do not `git add -A` blindly.
- **Diagnostic `&&` chains die on expected non-zero exits.** A grep that finds nothing exits 1; a `git show` of a missing path exits 1 — either one silently kills an `&&` chain partway, and *the last command's output* is what you actually see. Use `;` separators (or `|| echo …`) for multi-check diagnostics.
- **Hash verification is the acceptance proof.** `git show HEAD:<path> | sha256sum` vs the ledger `after` hash proves the committed bytes equal the curator's. Do it per file, per commit.
- **No sync step exists.** The repo skills dir *is* the profile skills dir. `skill_manage` edits hit both; there is nothing to push or re-sync. (Verify the bind with `stat -c '%i'` if in doubt — identical inodes.)
- **Push immediately — the local-only window is gone.** The remote `origin`
  is public (added 2026-09-14) and the `research-commit` Push policy says a
  commit is not done until pushed, after *each* commit. So a botched commit
  is public almost as soon as it exists: `git reset --mixed HEAD~1` on a
  pushed commit is a rewrite of public history and is banned (it was a
  pre-remote escape hatch; it is no longer available in practice). Fix
  forward with a new commit, per research-commit checklist item 5.
- **A skill created during the review becomes a new pending change** (the skills dir is the repo). Commit it in the same pass (type `chore(repo)`, body noting it codifies the workflow) so the tree ends clean — don't leave the process's own artifact as untracked noise for the next cycle.

## Message templates

```
chore(repo): ignore research curator ledger in .gitignore

chore(repo): accept curator skill updates: data-snapshots, data checklist

Curator session 20260911_210329_44f920 created the data-snapshots skill and
expanded research-commit checklist item 4 with the verify.py / data drop-zone
procedure. Reviewed against the repo (verify.py exit 0, all 3 snapshots
pinned); accepted as-is.

chore(repo): codify curator skill review workflow

fix(repo): correct data-snapshots claim — verify.py flag is -s, not --strict
```
