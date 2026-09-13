#!/usr/bin/env bash
# new_video.sh — create a new video by copying the pipeline skeleton.
# Usage: new_video.sh <slug>
# The slug becomes videos/<slug>/; spec.md must be committed BEFORE the first
# render (CONCEPT §4.1) — this script copies the spec template into place.
set -euo pipefail

SLUG=${1:-}
if [[ -z "$SLUG" ]]; then
  echo "usage: new_video.sh <slug>" >&2; exit 2
fi
if [[ ! "$SLUG" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
  echo "slug must be kebab-case: $SLUG" >&2; exit 2
fi

REPO_ROOT=$(git rev-parse --show-toplevel)
PIPELINE="$REPO_ROOT/videos/pipeline"
DEST="$REPO_ROOT/videos/$SLUG"

[[ -e "$DEST" ]] && { echo "refusing: $DEST already exists" >&2; exit 1; }

cp -r "$PIPELINE/skeleton" "$DEST"
rm -f "$DEST/.DS_Store"

# style/ + fonts/ snapshot (committed render inputs — see snapshot_style.sh)
bash "$PIPELINE/snapshot_style.sh" "$DEST"

# meta.json: set id/name to the slug
python3 - "$DEST/meta.json" "$SLUG" <<'PY'
import json, sys
p, slug = sys.argv[1], sys.argv[2]
m = json.load(open(p))
m["id"] = slug
m["name"] = slug
m.pop("note", None)
json.dump(m, open(p, "w"), indent=2)
open(p, "a").write("\n")
PY

# package.json: rename
python3 - "$DEST/package.json" "$SLUG" <<'PY'
import json, sys
p, slug = sys.argv[1], sys.argv[2]
m = json.load(open(p))
m["name"] = slug
json.dump(m, open(p, "w"), indent=2)
open(p, "a").write("\n")
PY

# Spec template (the gate — CONCEPT §4.1)
if [[ -f "$PIPELINE/templates/spec.md" ]]; then
  cp "$PIPELINE/templates/spec.md" "$DEST/spec.md"
  echo "spec template copied to $DEST/spec.md"
else
  echo "warning: $PIPELINE/templates/spec.md missing — author spec.md from CONCEPT §4.1" >&2
fi

mkdir -p "$DEST/audio" "$DEST/data"
touch "$DEST/audio/.gitkeep" "$DEST/data/.gitkeep"

echo "created videos/$SLUG from pipeline/skeleton"
echo "next: write spec.md, commit it (spec gates render), then build scenes."
