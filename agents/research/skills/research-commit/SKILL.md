---
name: research-commit
description: "Use when committing on the research side of the preregistered-money repo. Conventional commits with scope, the seal ceremony, and the agents/video + videos boundary."
version: 1.0.0
author: Preregistered Money
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [git, commits, preregistration, seal, integrity, research]
    editorial_name: Research Commit
    editorial_description: "Commit conventions for the research agent: conventional commits with project scopes, the seal ceremony that makes a commit the notary, and the hard boundary that keeps video work out of research commits."
---

# Research Commit

Commit conventions for the **research** side of `preregistered-money`. This skill exists in the research agent's skills tree only — the video agent never loads it and never commits here.

The brand is an immutable, timestamped, public record. Git is the notary: **the commit message is part of the audit trail.** Messages must be greppable (CI and `scoreboard/build.py` recover the seal SHA from `git log`) and the commit must be clean (exactly the change it claims to be).

**Commits are atomic.** One commit = one coherent change you could describe in a single conventional-commit line. Do not bundle unrelated edits (a fix plus a refactor, a feature plus a chore, a doc tweak plus a code change) — split them into separate commits. This holds for *every* commit, not just seals; the seal ceremony's one-prereg-per-commit rule is the strictest instance of the same principle.

## Hard boundary (check before every commit)

Refused — unstage and abort, report to the user:

- `agents/video/**`
- `videos/**`

Allowed paths for research commits: `docs/`, `research/`, `scoreboard/`, `.github/workflows/` (research jobs only — never the video-render job), `agents/research/`, and root files (README, LICENSE, pyproject/requirements, .gitignore).

Gate: before committing, run `git status --short` and inspect every path that would be staged. If any matches `^agents/video/` or `^videos/`, stop. Do not "just leave it in the working tree if it's already staged" — unstage it explicitly.

## Message format

```
type(scope): summary
```

- Summary: imperative mood, ≤ 72 chars, no trailing period.
- Body (optional): wrapped at 72; for results commits it must carry the seal SHA and config hash.
- No `Signed-off-by` or other trailers needed; footers allowed for `BREAKING CHANGE`.

### Types

Standard conventional set, plus one project type:

| Type | Use for |
|---|---|
| `feat` | new engine feature, new data loader/manifest, strategy package, scoreboard feature |
| `fix` | corrections to engine, loaders, generator, CI |
| `docs` | methodology, concept, templates, and **amendments to sealed preregs** |
| `test` | tests for the backtest engine / data / generator |
| `refactor` | restructuring with no behavior change |
| `chore` | dep pins, license, gitignore, repo plumbing, scoreboard regeneration |
| `ci` | workflow changes (research jobs only) |
| `build` | build/dependency tooling changes |
| `revert` | reverting a prior commit |
| `seal` | **the seal ceremony** — one per prereg, never anything else |

### Scopes (mapped to paths)

| Scope | Path / concern |
|---|---|
| `prereg` | `docs/preregistrations/` (incl. amendments) |
| `results` | `docs/results/` |
| `backtest` | `research/backtest/` |
| `data` | `research/data/` (manifests, loaders, recipes — **no raw data**) |
| `wiki` | `research/wiki/` (LLM-wiki pages, raw/ sources, schema, index, log) |
| `strategy` | `research/strategies/` |
| `scoreboard` | `scoreboard/` |
| `methodology` | `docs/METHODOLOGY.md` |
| `concept` | `docs/CONCEPT.md` |
| `templates` | `docs/templates/` |
| `repo` | root files, repo plumbing |
| `agents` | `agents/research/` — the research agent profile: SOUL.md, MEMORY.md, skills, memories/README.md |

Subject ≤ 72 chars; keep the whole `type(scope):` prefix short by preferring the narrowest scope that fits.

## The seal ceremony

A sealed prereg's **commit SHA is the seal** (CONCEPT §2–§3). Therefore:

1. **One prereg per seal commit.** The commit contains exactly that prereg doc with frontmatter `sealed: true`. Never bundle two seals, and never bundle a seal with unrelated work — bundling makes the seal SHA ambiguous.
2. **Subject format** (greppable by CI/scoreboard — the PR ID is mandatory):
   ```
   seal(prereg): PR-2026-001 — SPX/10Y/gold passive benchmark study
   ```
   The em-dash clause is a one-line version of the hypothesis.
3. **Where the seal SHA lives.** The sealed doc cannot contain the SHA of its own seal commit, so the frontmatter field `seal_sha:` is left **empty** at seal time. The SHA is recorded in two later places, both of which stay byte-stable:
   - `scoreboard/build.py` greps `git log` for the `seal(prereg): PR-…` commit and records PR→SHA in generated `SCOREBOARD.md` (regenerated in a separate `chore(scoreboard)` commit).
   - The results doc (`docs(results): …`) references the seal SHA in its frontmatter/body.
   Do **not** hand-edit the prereg to backfill the SHA, and do **not** use a second "seal record" commit — that muddies "sealed = immutable."
4. **Sealed docs are append-only.** After sealing, any change to that doc is an amendment: edit **only** the `## Amendments` section, and commit separately:
   ```
   docs(prereg): PR-2026-001 amendment — <short reason>
   ```
   Body must carry the justification. The git history is the audit trail; the amendment is never folded into the seal commit.

## Pre-commit integrity checklist

Run all seven before every commit. On failure: fix or stop and tell the user — do not commit with a violation noted.

1. **Boundary clean** — no `agents/video/` or `videos/` path staged (see Hard boundary).
2. **Sealed doc touched?** — must be an append-only amendment (ceremony rule 4); if the intended change is not an amendment, stop and flag it for a new PR instead.
3. **Sealing?** — the commit contains exactly one prereg with `sealed: true`, and nothing else.
4. **No raw data** — `research/data/` commits carry manifests, loaders, and download recipes only (source/version/checksum/recipe), never data dumps. Raw snapshots live in the gitignored `data/` drop zone at the repo root: before committing any data change, run `python3 research/data/verify.py` (must exit 0 — all pinned hashes match, no unpinned files) and confirm nothing under `data/` is staged except `data/README.md`, the only tracked file there. Full procedure: the `data-snapshots` skill.
5. **No history rewriting** — never `rebase`, `reset --hard`, or `commit --amend` on a pushed commit or on any `seal` commit. Fix forward with a new commit.
6. **Scoreboard is generated** — `SCOREBOARD.md` changes come from `scoreboard/build.py`, never hand-edits (commit type `chore(scoreboard)`).
7. **Format valid** — type and scope both in the allowed sets above; subject ≤ 72 chars, imperative, no trailing period.
8. **Concurrent writer** — the video agent commits to the same working tree while you work. Re-run `git status --short` immediately before committing: a path that was pending minutes ago may already be committed (by the other agent), and new commits can land between your check and yours. After committing, confirm with `git log --oneline` that your commit is at the tip; if a foreign commit interleaved, `git show <sha> --stat` and confirm it stayed on the other side of the boundary.

## Templates (the common cases)

```
seal(prereg): PR-2026-001 — SPX/10Y/gold passive benchmark study

docs(prereg): PR-2026-001 amendment — extend data window to 1950

docs(results): PR-2026-001 results — 60/40 blend selected, CONFIRMED
Seal: <sha>  Config: <hash>
(body: headline OOS metrics, verdict against pre-registered criteria)

feat(backtest): walk-forward engine with explicit costs and config-hash logging
test(backtest): look-ahead and survivorship unit tests
feat(data): SPY/TLT/GLD manifests + loaders (source/version/checksum/recipe)
feat(strategy): scaffold config-driven package for PR-2026-002
feat(scoreboard): null-baseline column in aggregate stats
docs(methodology): cost model — commission, spread, slippage assumptions
docs(concept): resolve open question — data budget
docs(templates): PR_TEMPLATE.md first draft
chore(scoreboard): regenerate from prereg+result docs
chore(repo): pin deps, add LICENSE (MIT) and .gitignore
docs(agents): README for research memory store
ci: re-run latest sealed prereg on schedule, publish drift as incident
```
