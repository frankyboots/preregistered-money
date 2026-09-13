#!/usr/bin/env bash
# snapshot_style.sh — copy the pipeline style spec + vendored fonts into a
# video dir as committed render inputs.
#
# Why a snapshot (not a live ../pipeline/ reference):
#   1. Render workers resolve CSS url() relative to the css file, and any
#      asset path climbing above the project root (`../pipeline/…`) is a
#      lint error (invalid_parent_traversal_in_asset_path).
#   2. Determinism (VIDEO_CONCEPT §7): the render's inputs must live inside
#      the video dir, so a committed re-render never depends on tree state
#      outside it. The build log pins the pipeline SHA the snapshot came
#      from — that SHA is the snapshot's version of record.
#
# Usage: snapshot_style.sh <video-dir>
# Refuses to run if the video already has style/ or fonts/ (a snapshot is
# a one-shot committed act; refresh = delete + re-snapshot + build-log note).
set -euo pipefail

VIDEO_DIR=${1:-}
if [[ -z "$VIDEO_DIR" || ! -d "$VIDEO_DIR" ]]; then
  echo "usage: snapshot_style.sh <video-dir>" >&2; exit 2
fi
PIPELINE=$(cd "$(dirname "$0")" && pwd)
PIPELINE_SHA=$(git -C "$PIPELINE" rev-parse --short HEAD)

if [[ -e "$VIDEO_DIR/style" || -e "$VIDEO_DIR/fonts" ]]; then
  echo "refusing: $VIDEO_DIR already has style/ and/or fonts/ —" >&2
  echo "a snapshot is a one-shot committed act (delete + re-run + build-log note)." >&2
  exit 1
fi

mkdir -p "$VIDEO_DIR/style" "$VIDEO_DIR/fonts"
cp "$PIPELINE/style/tokens.css" "$PIPELINE/style/setpieces.css" "$PIPELINE/style/brand-mark.svg" "$VIDEO_DIR/style/"
cp "$PIPELINE/fonts/"*.woff2 "$VIDEO_DIR/fonts/"

# Render workers resolve url() relative to the css file — rewrite the
# pipeline-relative font paths to video-dir-relative.
sed -i 's|url("../fonts/|url("fonts/|g' "$VIDEO_DIR/style/tokens.css"

# Stamp the snapshot banner (idempotent guard).
if ! grep -q 'SNAPSHOT — copied from pipeline/style/' "$VIDEO_DIR/style/tokens.css"; then
  {
    echo "/* SNAPSHOT — copied from pipeline/style/ by snapshot_style.sh on $(date -u +%Y-%m-%d) from pipeline SHA $PIPELINE_SHA. */"
    echo "/* ../fonts/ paths rewritten to fonts/ (render workers resolve url() relative to the file;"
    echo "   ../ escapes the project root — lint: invalid_parent_traversal_in_asset_path)."
    echo "/* Version of record: the pipeline SHA in this video's build.log. */"
    cat "$VIDEO_DIR/style/tokens.css"
  } > "$VIDEO_DIR/style/tokens.css.tmp" && mv "$VIDEO_DIR/style/tokens.css.tmp" "$VIDEO_DIR/style/tokens.css"
fi

echo "snapshotted style/ + fonts/ into $VIDEO_DIR (pipeline $PIPELINE_SHA)"
echo "record the pipeline SHA + file checksums in the video build.log."
