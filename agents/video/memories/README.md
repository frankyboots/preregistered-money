# Agent memory store (video)

This directory is the video agent's Hermes memory store, symlinked into the agent profile
(`~/.hermes/profiles/video/memories/ → agents/video/memories/`) so the agent's cross-session
state lives in the repo and is part of the audit trail.

## Contents

| File | What it is |
|---|---|
| `MEMORY.md` | The agent's task tracker (≤ 2,200 chars). Managed by the agent's `memory` tool; the tracker discipline (recent / in-flight stage / next session) is defined in `agents/video/SOUL.md`. |
| `USER.md` | Owner profile (≤ 1,375 chars). Created when the agent first saves owner preferences; may not exist yet. |

## How it works

- Hermes loads `MEMORY.md` as a frozen snapshot into the system prompt at **session start**; writes during a session persist to disk immediately but only appear in the prompt of the *next* session.
- The agent updates the tracker while working and at session end per the SOUL contract.

## Editing rules

- **Between sessions:** humans may edit `MEMORY.md` directly (e.g. to correct a stale entry or set the next task); the change is picked up at the next session start.
- **While a session runs:** don't hand-edit — the in-session agent has a frozen snapshot and its own writes will clobber yours. Direct the agent instead.
- **Keep it small.** This is a pointer, not a log: state plus a few next actions, with SHAs/paths instead of detail. What happened lives in git; procedures live in skills.
- This file (README) is documentation only — Hermes ignores it.
