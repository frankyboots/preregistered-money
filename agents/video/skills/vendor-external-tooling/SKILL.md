---
name: vendor-external-tooling
description: "Use when porting an external repo into this one."
version: 1.0.0
author: Preregistered Money
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [vendoring, pipeline, skills, attribution, external-repo, smoke-test]
    editorial_name: Vendor External Tooling
    editorial_description: "Port an external/community repo's skills, scripts, and templates into this repo: survey, license check, adopt/adapt/skip plan, attribution-aware copies, real smoke tests, atomic commits."
---

# Vendor External Tooling

Use when an external repo (community skill collections, script toolkits) has been dropped into the workspace and the job is to decide what to adopt and where it lives: agent skills, `videos/pipeline/`, or discarded. The user prefers procedural community tooling over official how-to skills and wants a review of every supporting file before anything moves.

## Procedure

1. **Survey the entire repo before planning.** Enumerate all files (excluding `.git`); read every SKILL.md, script, template, workflow, AGENTS.md, README, and LICENSE. Plan from content, not the tree.
2. **License check before adopting.** MIT/Apache-2.0 are adoptable with attribution; anything else, stop and ask the user.
3. **Gap-map against governance.** Read `videos/VIDEO_CONCEPT.md` and the existing skills. Produce a verdict per item — adopt / adopt-adapted / skip — with a one-line rationale. The channel's standing decisions (music: none, soft-SRT captions, faceless, determinism, number citations) are the main skip drivers; a skip for a standing decision is a decision, not an oversight.
4. **Present the plan and get approval** before moving anything.
5. **Port skills** via `skill_manage`. They land in `agents/video/skills/`, which is the video profile's live skills directory — they must be committed, and they are the canonical home (do not copy them into `videos/`). Per skill: adapt to the repo (one-video-dir layout, spec-gates-render, committed-wav timing, standing decisions), point at `videos/pipeline/tools/` paths, add a Provenance section with the source URL. **The frontmatter `description` has a 60-character budget — create is refused for longer.** Write a short trigger sentence; put the detail in the body and `metadata.hermes.editorial_description`.
6. **Port scripts and templates** into `videos/pipeline/tools/` and `videos/pipeline/templates/` with a per-file attribution header. The header syntax must match the file format:
   - `.py` / shell: after the shebang, `# Vendored from <url> (<license>)` plus a standing line `# If you modify this file, add a change note here per Apache-2.0 §4(b).` (word the change-note line to the license; MIT needs no change-note obligation).
   - `.md`: HTML comment on line 1, same two parts.
   - `.json`: **no comment syntax exists** — use an inline `"_provenance"` key containing both parts. Prepending a comment line silently breaks every JSON parser.
   - Headers must stay true after future edits: they say "derived from", never "unmodified", so the curator/agent can change the file freely and the attribution never goes stale.
   - After vendoring, parse-validate every machine-parsed file (e.g. `python3 -c "import json; json.load(open('...'))"`).
7. **Verify bulk text transforms.** After any scripted mass edit (header insertion, sed across files), diff each output against the source or compare line counts. A truncated Python file still executes and exits 0, so a clean exit is not evidence the content survived.
8. **Smoke-test every vendored script** before declaring the port done: generate a small fixture (e.g. `ffmpeg -f lavfi -i testsrc2=duration=6:size=1920x1080:rate=30 -f lavfi -i sine=frequency=440:duration=6 -c:v libx264 -pix_fmt yuv420p -c:a aac -shortest test.mp4`) and run each tool end-to-end, inspecting outputs. Palette-scan-style linters exit 1 when they find findings — that is correct behavior, not a failure; do not run them under naive `set -e`.
9. **Delete the dropped clone folder** when done. Never commit it: a clone inside `videos/` violates the one-video-per-dir rule and the commit boundary.
10. **Commit atomically** per the `video-commit` skill: one commit per concern — pipeline tooling (`pipeline` scope), skills (`agents` scope), gitignore/scaffold (`repo` scope).

## Standing Conventions

- Attribution lives per file (header or `_provenance` key) plus a Provenance section in `videos/pipeline/README.md`. The full license text lives once in `videos/pipeline/LICENSE` — the byte-identical canonical text from apache.org, not a copy of the upstream repo's LICENSE file (which may be boilerplate with no copyright holder). Headers point at `../LICENSE`. When a vendored file is modified, add a one-line change note in its header (Apache-2.0 §4(b)); git history carries the rest — do not track upstream commits per file.
- Generated outputs of vendored tools (proof frames, contact sheets, renders) stay gitignored — regenerable is not committed (`videos/*/renders/`, `videos/*/snapshots/`).
- Record skipped-but-relevant upstream items in the pipeline README (what was skipped and which standing decision drove it), so a future session can flip the decision without re-auditing the upstream repo.
