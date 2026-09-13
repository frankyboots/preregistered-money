# Wiki Log

> Chronological record of all wiki actions. Append-only.
> Format: `## [YYYY-MM-DD] action | subject`
> Actions: ingest, update, query, lint, create, archive, delete
> Rotate to log-YYYY.md when this file exceeds 500 entries.

## [2026-09-13] create | Wiki initialized
- Domain: preregistered-money research knowledge base (asset classes, datasets,
  concepts, design evidence for preregs)
- Structure created: SCHEMA.md, index.md, log.md, raw/{articles,papers,transcripts,assets}/
- Key domain decisions (owner-approved): concepts are dynamic (no pre-declared
  inventory); comparisons/queries populate during spec-analysis sessions;
  wiki lives in-repo at research/wiki/ (citable via git SHA), not at the
  llm-wiki skill's external default.
