---
name: data-snapshots
description: "Use when adding, pinning, or verifying raw data snapshots."
version: 1.2.0
author: Preregistered Money
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [data, snapshots, manifests, checksums, reproducibility, research]
    editorial_name: Data Snapshots
    editorial_description: "How raw data enters the preregistered-money repo: the gitignored data/ drop zone, per-dataset manifests, checksum pinning, and the verify script that makes snapshots auditable."
---

# Data Snapshots

How raw data enters `preregistered-money`. The contract is two-sided:

- **`data/`** (repo root) — gitignored drop zone. Raw exports live here on disk so the owner can open them; nothing under it is committed except `data/README.md` (gitignore negation).
- **`research/data/`** (committed) — the reproducibility contract: `datasets/*.md` manifests, `checksums.txt` pins, `verify.py` checker.

`data/README.md` is the canonical repo doc for this — read it first if it and this skill disagree. Commits follow the `research-commit` skill (scope `data`, checklist item 4).

## Adding a snapshot (the procedure, in order)

1. **Drop the export into `data/`**, keeping the vendor's original filename (TradingView exports carry commas and spaces — always quote the path). Never rename a file after its manifest `raw:` field is pinned.
2. **Inspect the raw file before writing anything** — head/tail it, count data rows, find the real first and last dates. Manifest fields come from the file, not the vendor page.
3. **Hash it:** `sha256sum data/<file>`
4. **Write `research/data/datasets/<dataset-id>.md`** — copy the closest existing manifest as the model. YAML frontmatter: `id`, `raw` (path), `source`, `url`, `obtained` (date), `format`, `snapshot` (download date + last row), `sha256`, `first`, `last`, `frequency`, `license`; then a **Structure** section (columns, header layout, date encoding) and a **Caveats** section (what is NOT in the file, unusable regions, proxy gaps, string `'NA'` cells, estimated recent rows).
5. **Pin it:** append `<sha256>  data/<file>` (two spaces, `sha256sum` format) to `research/data/checksums.txt`.
6. **Verify:** `python3 research/data/verify.py` — must print OK for the new file and exit 0 with no `UNPINNED` lines.
7. **Commit** manifest + `checksums.txt` (+ loader changes) with scope `data`. Stage nothing under `data/` except `README.md`; sanity-check with `git check-ignore data/<file>` (should match) and `git status --short`.

## Refreshing a snapshot (re-download)

A re-download is a **new snapshot**, not an update:

- Never silently overwrite a file a sealed prereg's run pinned. If the old snapshot must stay reproducible, keep it and save the new export under a dated name (e.g. `ie_data-2026-12.xls`).
- New file → new manifest entry or manifest note, new `checksums.txt` line, `verify.py` re-run, a commit explaining which snapshot is now canonical.
- If the old file is truly disposable, replace in place but still bump the checksum and note the re-download in the manifest — the git history of `checksums.txt` is the audit trail.

## Verifying a dataset against a reference (before first sealed use)

When a manifest's convention is suspect, or an open data task demands empirical
verification before the dataset is first used in a sealed run, verify before
citing:

1. **Profile the file offline first** — day-of-month distribution of row dates
   (bar-start vs. value date?), open/close continuity across consecutive
   months, gap/missing-month scan. The convention comes from the file, not the
   vendor page.
2. **Get a free public reference** for the same quantity. Benchmark authorities
   are often licensed or bot-walled — check `references/verify-against-reference.md`
   for known-usable references before concluding a source is unavailable.
3. **Compare at anchor points** — at least the months the task names, spanning
   the eras it names; per-month deviations recorded in a table.
4. **Record it in the manifest, not a side doc** — a verification section: the
   reference URLs, the comparison table, numbered findings, bounded limitations
   (with the scope in which each is immaterial), and the rule that any
   re-download re-verifies — the section is valid only for the pinned sha256,
   and the checksum pin is the arbiter, not the section.
5. **Commit** with scope `data`; the commit body names the task satisfied.

Tolerances: ≤ ~0.5% across normal months confirms the convention; a large
deviation in an extreme-volatility month is a documented limitation, not an
automatic failure — judge materiality against the scope the data will be used
for.

## Pitfalls

- **Manifest from the file, not the marketing page.** Legacy formats hide their header: the Shiller `ie_data.xls` 'Data' sheet has an 8-row merged header block, data starting at row 9, fractional-year `YYYY.MM` dates, string `'NA'` in early CAPE/earnings cells, and an estimated-values footer note on the last row. Record all of it in Structure/Caveats so the loader — and any prereg's data section — is written against reality.
- **Unusable history is a manifest field.** When part of a file's history cannot be used, state it as `usable_from:` with the reason. GOLDUSD spot before 1970 is a flat 20.65 reconstruction (no liquid market, pre–Nixon-shock) — `usable_from: 1970-01-01` is in `datasets/gold.md`; loaders should refuse or warn on earlier rows, and every prereg must inherit the window.
- **Throwaway parsing on this box:** system `python3` has no pandas/xlrd — use `uv run --with xlrd python3 …` (or `--with pandas`) for ad-hoc inspection. `verify.py` itself must stay **stdlib-only** so CI can run it with no environment.
- **Vendor filenames with commas/spaces** break unquoted shell commands and some CSV readers; quote paths everywhere and keep the manifest `raw:` field byte-identical to the on-disk name.
- **A bar export's row date is not its value date.** TradingView monthly bars are dated the month's *first trading day* (day-of-month always 1–4); the value to use is the bar's `close` (month-end). Check the day-of-month distribution before treating any row date as the value date — loader slicing and every prereg's window are written against the value date, not the bar date.
- **The benchmark authority is often licensed or removed, not absent.** LBMA's historical tables are IBA-licensed, and FRED removed its IBA-administered benchmark series outright (the series IDs redirect to FRED's IBA-data-removal notice). Published per-year fix listings (sdbullion.com) are a free, regex-parseable reference for LBMA AM/PM fixes — see `references/verify-against-reference.md` before concluding a source is unavailable.
- **Verify before you commit, and test the verifier's failure modes** when you touch it: a stray unpinned file and a corrupted hash must both make `verify.py` exit 1 — a verifier that can't fail proves nothing.
