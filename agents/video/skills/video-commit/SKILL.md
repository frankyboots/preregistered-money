---
name: video-commit
description: "Use when committing video work in preregistered-money."
version: 1.0.0
author: Preregistered Money
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [git, commits, video, hyperframes, build-log, integrity]
    editorial_name: Video Commit
    editorial_description: "Commit conventions for the video agent: conventional commits with project scopes, the one-video-dir-per-video rule with build logs, and the hard boundary that keeps preregistrations, results, and run configs out of video commits."
---

# Video Commit

Commit conventions for the **video** side of `preregistered-money`. This skill exists in the video agent's skills tree only — the research agent never loads it and never commits here.

The brand is reproducibility: every published frame is regenerable from the repo. Git is the record: a video's **build log is part of the audit trail** — it must name the inputs (data snapshot, results doc, composition files) so that same input → same pixels is checkable. Messages must be greppable and commits must be clean (exactly the change they claim).

**Commits are atomic.** One commit = one coherent change you could describe in a single conventional-commit line. Do not bundle unrelated edits (a composition fix plus a palette change, a build log plus a chore) — split them into separate commits. A single video's composition + its build log update for the same change is one coherent commit.

## Hard boundary (check before every commit)

Refused — unstage and abort, report to the user:

- `docs/preregistrations/**`
- `docs/results/**`
- `docs/METHODOLOGY.md`
- `docs/CONCEPT.md`
- `docs/templates/**`
- `research/**`
- `scoreboard/**`
- `agents/research/**`
- `.github/workflows/` — except the video-render job only

Allowed paths for video commits: `videos/**`, `agents/video/**`, the video-render workflow in `.github/workflows/`, and root files (README, LICENSE, .gitignore) *only when the change is about video tooling or the scaffold itself*.

`agents/video/memories/MEMORY.md` is committed — it is the agent's auditable task-tracker state, part of the scaffold. Its `*.lock` sibling is runtime noise and is gitignored; never stage a lock file.

The video agent **never edits run configs, sealed preregs, results docs, or scoreboard output.** Numbers for a video come *from* the published results doc (read-only); a video that needs a new number requests a new prereg — it never produces one. This is the mechanical research/video separation (CONCEPT §11).

Gate: before committing, run `git status --short` and inspect every path that would be staged. If any matches a refused pattern, stop. Do not "just leave it in the working tree if it's already staged" — unstage it explicitly.

**Concurrent writer:** the research agent commits to the same working tree while you work. Re-run `git status --short` immediately before each commit — a path that was untracked minutes ago may already be committed, and new commits can land between your check and yours. After committing, confirm with `git log --oneline` that your commit landed at the tip; if a foreign commit appeared around yours, `git show <sha> --stat` and confirm it stayed on the other side of the boundary before moving on.

## Message format

```
type(scope): summary
```

- Summary: imperative mood, ≤ 72 chars, no trailing period.
- Body (optional): wrapped at 72; for video commits it must carry the PR ID and results-doc path the video is built on (when applicable).
- No `Signed-off-by` or other trailers needed; footers allowed for `BREAKING CHANGE`.

### Types

Standard conventional set, plus one project type:

| Type | Use for |
|---|---|
| `feat` | new pipeline feature, new composition template, new video-series scaffolding |
| `fix` | corrections to compositions, pipeline scripts, render workflow |
| `docs` | build logs, video READMEs, methodology notes about production |
| `refactor` | restructuring compositions/pipeline with no output change |
| `chore` | dep pins, license, gitignore, scaffold plumbing |
| `ci` | video-render workflow changes |
| `build` | build/dependency tooling changes (FFmpeg, hyperframes deps) |
| `revert` | reverting a prior commit |
| `video` | **composition content** — one per video slug: new compositions, episode cuts, data-input updates, and their build-log updates |

### Scopes (mapped to paths)

| Scope | Path / concern |
|---|---|
| `video-<slug>` | `videos/<video-slug>/` — e.g. `video-benchmark-study` for the benchmark-study episode |
| `pipeline` | video pipeline tooling (render scripts, hyperframes config, TTS glue) outside a single video dir |
| `agents` | `agents/video/` (this skill, prompt, bundle pin) |
| `repo` | root files, repo plumbing |

Subject ≤ 72 chars; keep the whole `type(scope):` prefix short by preferring the narrowest scope that fits.

## Video integrity rules (the local equivalent of the seal ceremony)

1. **One video = one repo directory.** `videos/<video-slug>/` holds the composition (HTML/CSS/JS), its data inputs, and the build log (CONCEPT §7). No video content lives outside its directory; shared templates live in the pipeline, versioned, and the build log names the template version used.
2. **Numbers trace to the results doc.** Every figure shown on screen (headline OOS metric, Sharpe, max DD, confirmation rate, pin date) must appear in the cited results doc (`docs/results/PR-YYYY-NNN-results.md`). Cite the PR ID and results-doc path in the build log. Never compute new numbers inside a composition; a chart is drawn from a data input file that itself is copied/derived from the results doc or its data snapshot, and the build log records the derivation.
3. **Build log is regenerated, not narrated.** Each render or material composition change updates the build log: timestamp, composition + template versions (git SHAs where applicable), data input files with checksums, TTS voice/model version, encoder settings. The log is committed *in the same commit* as the change it describes.
4. **Deterministic builds.** Composition inputs are pinned (data files in the video dir, template version, font/asset list). If a re-render from the committed dir does not reproduce the published pixels, that is an incident — fix the pipeline, don't hand-edit the output.
5. **Verdict videos are self-sufficient (CONCEPT §8).** A verdict composition includes the prereg recap (hypothesis, pre-registered bar, seal date + SHA). The recap values come from the prereg doc and scoreboard — read-only, cited in the build log.
6. **No raw data dumps.** `videos/**` carries small derived data inputs (tables, series extracts) with their source cited; large datasets stay as manifests in `research/data/` (research's turf). A video input derived from a dataset records the snapshot/checksum it came from.

## Pre-commit integrity checklist

Run all six before every commit. On failure: fix or stop and tell the user — do not commit with a violation noted.

1. **Boundary clean** — no refused path staged (see Hard boundary).
2. **Build log in sync** — any composition or data-input change under `videos/<slug>/` ships with the updated build log in the same commit.
3. **Numbers cited** — every on-screen figure traces to a results doc (or prereg/scoreboard for recaps) named in the build log; no figure was computed ad hoc in the composition.
4. **No raw data** — data inputs in the video dir are small derived extracts with source + snapshot checksum recorded, not dataset dumps.
5. **No history rewriting** — never `rebase`, `reset --hard`, or `commit --amend` on a pushed commit. Fix forward with a new commit.
6. **Format valid** — type and scope both in the allowed sets above; subject ≤ 72 chars, imperative, no trailing period.

## Templates (the common cases)

```
video(video-benchmark-study): composition v2 — benchmark chart + verdict recap
(PR-2026-001, docs/results/PR-2026-001-results.md)
(body: build log updated — template 0.3.0, data inputs a1b2c3d…, TTS v3/voice X)

feat(pipeline): hyperframes render script with checksummed data inputs
docs(pipeline): TTS voice + model versions pinned in pipeline README
fix(video-verdict-pr2026002): correct max-DD label to results doc value
chore(repo): add video agent scaffold (skills, prompt, bundle pin)
ci: video-render workflow — render on merge for videos/ changes
build: pin FFmpeg 7.x for deterministic encodes
```
