#!/usr/bin/env bash
# render.sh — the ONLY sanctioned entry point for hyperframes in this repo.
# Pins the framework version (single source of truth: HF_VERSION) and sets
# HYPERFRAMES_SKIP_SKILLS=1 so no vendor skill install/check ever runs.
# Usage: render.sh <video-dir> <hyperframes-subcommand> [args...]
#   e.g. render.sh videos/meta-explainer render --composition composition/scene-01.html --quality draft
#        render.sh videos/meta-explainer lint
#        render.sh videos/meta-explainer check
# Appends a one-line entry to <video-dir>/build.log on every invocation.
set -euo pipefail

HF_VERSION=0.8.35
export HYPERFRAMES_SKIP_SKILLS=1

if [[ $# -lt 2 || ! -d "$1" ]]; then
  echo "usage: render.sh <video-dir> <render|lint|check|preview> [args...]" >&2
  exit 2
fi

VIDEO_DIR=$1; shift
SUBCMD=$1; shift
CMD_STR="$SUBCMD $*"   # for build.log, captured before the arg loop consumes $@

# Refuse to run against the skeleton itself.
case "$(realpath "$VIDEO_DIR")" in
  "$(realpath "$(dirname "$0")/skeleton")")
    echo "refusing: skeleton is a template, not a video. Copy it first (pipeline/new_video.sh <slug>)." >&2
    exit 2 ;;
esac

[[ -f "$VIDEO_DIR/index.html" ]] || { echo "not a video dir (no index.html): $VIDEO_DIR" >&2; exit 2; }

# --output is CWD-relative in the CLI; make relative paths relative to the video
# dir so renders land in <video-dir>/renders/ (gitignored), per CONCEPT layout.
# An explicit --output is re-anchored in the loop below; when none is given,
# the default (renders/<name>.mp4) is set here, before the loop consumes $@.
ARGS=()
OUTPUT_DEFAULT=false
for a in "$@"; do
  case "$a" in --output|--output=*) OUTPUT_DEFAULT=true ;; esac
done
if [[ "$OUTPUT_DEFAULT" == false ]]; then
  case "$SUBCMD" in
    render) ARGS+=(--output "$VIDEO_DIR/renders/${VIDEO_DIR##*/}.mp4") ;;
  esac
fi
while [[ $# -gt 0 ]]; do
  case "$1" in
    --output)
      [[ -n "${2:-}" ]] || { echo "--output needs a value" >&2; exit 2; }
      case "$2" in /*) ;; *) V="$VIDEO_DIR/$2" ;; esac
      ARGS+=(--output "$V"); shift 2 ;;
    --output=*)
      V=${1#--output=}
      case "$V" in /*) ;; *) V="$VIDEO_DIR/$V" ;; esac
      ARGS+=(--output="$V"); shift ;;
    *) ARGS+=("$1"); shift ;;
  esac
done

# build.log entry (pre + outcome) — keep the log greppable: one line per invocation.
TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
GIT_REV=$(git -C "$(git -C "$VIDEO_DIR" rev-parse --show-toplevel 2>/dev/null || echo .)" rev-parse --short HEAD 2>/dev/null || echo none)
{
  echo "$TS pipeline=hyperframes@$HF_VERSION repo=$GIT_REV cmd=hyperframes $CMD_STR exit=?"
} >> "$VIDEO_DIR/build.log"

set +e
npx --yes "hyperframes@$HF_VERSION" "$SUBCMD" "$VIDEO_DIR" ${ARGS[@]+"${ARGS[@]}"}
RC=$?
set -e

# Rewrite the exit code on the line we just appended (last line of the log).
LAST=$(tail -n 1 "$VIDEO_DIR/build.log")
tail -n +1 "$VIDEO_DIR/build.log" | head -n -1 > "$VIDEO_DIR/build.log.tmp" && mv "$VIDEO_DIR/build.log.tmp" "$VIDEO_DIR/build.log"
echo "${LAST/exit=?/exit=$RC}" >> "$VIDEO_DIR/build.log"

exit "$RC"
