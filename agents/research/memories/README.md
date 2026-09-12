# Agent memory store (research)

This directory is the research agent's Hermes memory store, symlinked into the agent profile
(`~/.hermes/profiles/research/memories/ → agents/research/memories/`) so the agent's cross-session
state lives in the repo and is part of the audit trail.

## Contents

| File | What it is |
|---|---|
| `MEMORY.md` | The agent's task tracker (char budget: config `memory.memory_char_limit`, currently 5,000): Recent / Queue / Next session. Managed by the agent's `memory` tool; the tracker discipline is defined in `agents/research/SOUL.md`. |
| `USER.md` | Owner profile (char budget: config `memory.user_char_limit`, currently 2,500). Created when the agent first saves owner preferences; may not exist yet. |

## How it works

- Hermes loads `MEMORY.md` as a frozen snapshot into the system prompt at **session start**; writes during a session persist to disk immediately but only appear in the prompt of the *next* session.
- The agent updates the scratchpad while working and at session end per the SOUL contract.

## Editing rules

- **Between sessions:** humans may edit `MEMORY.md` directly (e.g. to correct a stale entry or set the next task); the change is picked up at the next session start.
- **While a session runs:** don't hand-edit — the in-session agent has a frozen snapshot and its own writes will clobber yours. Direct the agent instead.
- **Keep it small.** This is a pointer, not a log: state plus a few next actions, with SHAs/paths instead of detail. What happened lives in git and the docs; procedures live in skills.
- **Integrity note:** memory is context, not the record — preregs, seals, results, and the scoreboard are authoritative regardless of what memory claims.
- This file (README) is documentation only — Hermes ignores it.
