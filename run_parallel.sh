#!/bin/bash
# Launch one independent run per named problem, all at once.
#
#   ./run_parallel.sh P-3 P-4 P-5
#
# Each pass writes only under runs/P-<n>/. Nothing is shared except the
# read-only .venv symlink, so the passes cannot overwrite each other.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
if [ "$#" -lt 1 ]; then
  echo "usage: run_parallel.sh P-<n> [P-<n> ...]" >&2
  exit 1
fi

for PASS in "$@"; do
  if [ ! -f "$ROOT/problems/$PASS.md" ]; then
    echo "no statement at problems/$PASS.md" >&2
    exit 1
  fi
done

mkdir -p "$ROOT/logs"
for PASS in "$@"; do
  nohup "$ROOT/run_one.sh" "$PASS" > "$ROOT/logs/$PASS.nohup" 2>&1 &
  echo "$PASS  pid=$!  log=runs/$PASS/autoresearch.log"
done
