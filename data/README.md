# data/ — raw snapshot drop zone

**This directory is gitignored.** Raw data files never enter git, never get
pushed, and never appear in any commit. The repo's data contract is:

- **Raw files** live here, on the machine, so you can open them.
- **Manifests** (`research/data/datasets/*.md`) live in the repo: source, URL,
  snapshot date, checksum, structure, known caveats.
- **`research/data/verify.py`** re-checks every file in this folder against
  `research/data/checksums.txt`.

## Adding a data file

1. Drop the export into `data/` (any filename, commas and spaces allowed).
2. Compute its checksum:
   `sha256sum data/<file>`
3. Create `research/data/datasets/<dataset>.md` (copy an existing manifest as
   the template) with source, URL, snapshot date, and the checksum.
4. Append `sha256  data/<file>` to `research/data/checksums.txt`.
5. `python3 research/data/verify.py` — must print `OK` for the new file.
6. Commit the manifest + checksums (+ any loader changes). **Never the raw
   file.**

## Re-downloading / refreshing a snapshot

A re-download produces a *new snapshot* — a different file, a different
checksum. That is fine and expected: the manifest notes it, `verify.py` is
updated, and preregs that pin the old snapshot keep working against it if the
old file is kept under a dated name. Never silently overwrite a file a sealed
prereg's run pinned.

## Current contents

| File | Dataset | Manifest |
|---|---|---|
| `ie_data.xls` | Shiller "Irrational Exuberance" monthly data, 1871–2026 | `datasets/shiller_ie_data.md` |
| `FRED_FEDFUNDS, 1M.csv` | TradingView export of FRED FEDFUNDS, monthly 1954–2026 | `datasets/fed_funds.md` |
| `TVC_GOLD, 1M.csv` | TradingView GOLDUSD spot, monthly 1833–2026 (usable from 1970) | `datasets/gold.md` |
