#!/usr/bin/env bash
# check-all-stages.sh — run the stage gate on every tutorial/* branch.
#
# Each branch is checked out into a temporary git worktree and gated with the
# scripts/check-stage.sh *of that branch*. Exit code is non-zero when any stage
# fails. Usage:
#   scripts/check-all-stages.sh                 # every tutorial/NN-* branch, in order
#   scripts/check-all-stages.sh 03 05           # only these stage numbers
#   SKIP_BUILD=1 scripts/check-all-stages.sh    # passed through to the gate
set -u
cd "$(dirname "$0")/.."
WT="${TMPDIR:-/tmp}/stage-worktrees-$$"; mkdir -p "$WT"
trap 'for d in "$WT"/*; do [ -d "$d" ] && git worktree remove --force "$d" >/dev/null 2>&1; done; rmdir "$WT" 2>/dev/null' EXIT

branches=$(git for-each-ref --format='%(refname:short)' 'refs/heads/tutorial/[0-9]*' | sort)
if [ $# -gt 0 ]; then
  sel=""; for n in "$@"; do sel="$sel"$(printf '%s\n' "$branches" | grep "^tutorial/$n-")$'\n'; done; branches="$sel"
fi

failed=""; passed=0
for b in $branches; do
  d="$WT/${b#tutorial/}"
  git worktree add --detach -q "$d" "$b" || { failed="$failed $b(worktree)"; continue; }
  printf '\n######## %s ########\n' "$b"
  if OUT="$WT/out-${b#tutorial/}" "$d/scripts/check-stage.sh" "$d" | tail -3; then passed=$((passed+1)); else failed="$failed $b"; fi
  git worktree remove --force "$d" >/dev/null 2>&1
done

echo; echo "passed: $passed"
if [ -n "$failed" ]; then echo "failed:$failed"; exit 1; fi
echo "ALL STAGES OK"
