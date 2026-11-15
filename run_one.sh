#!/bin/bash
# Run one problem in its own directory. Problems share nothing, so several of
# these can run at once.
#
#   problems/P-3.md  ->  runs/P-3/problem.md
#   ./run_one.sh P-3
#
# A second call on a problem that already has a run directory resumes it
# instead of starting over.
set -euo pipefail

PASS="${1:?usage: run_one.sh P-<n>}"
ROOT="$(cd "$(dirname "$0")" && pwd)"
SRC="$ROOT/problems/$PASS.md"
RUN="$ROOT/runs/$PASS"

if [ ! -f "$SRC" ]; then
  echo "no statement at $SRC" >&2
  exit 1
fi

mkdir -p "$RUN"/{computations/.briefs,derivations/.briefs,critiques,notes,references,data}
cp -a "$ROOT/prompts" "$ROOT/skills" "$ROOT/.grok" "$ROOT/AGENTS.md" "$ROOT/package.json" "$RUN/"
ln -sfn "$ROOT/.venv" "$RUN/.venv"
cp -a "$SRC" "$RUN/problem.md"

# Each pass gets its own prompt: the shared template names the pass and tells
# the runner to ignore every other pass's directory.
sed "s/__PASS__/$PASS/g" "$ROOT/prompts/run-template.md" > "$RUN/notes/autoresearch-prompt.md"

export PATH="$HOME/.grok/bin:$PATH"
GROK="${GROK_BIN:-grok}"
cd "$RUN"
echo "=== $PASS START $(date +%T) ===" >> autoresearch.log
"$GROK" --trust --always-approve --max-turns 150 \
  --cwd "$RUN" \
  --single "$(cat notes/autoresearch-prompt.md)" >> autoresearch.log 2>&1
echo "=== $PASS EXIT $? $(date +%T) ===" >> autoresearch.log
