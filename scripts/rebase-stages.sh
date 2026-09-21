#!/usr/bin/env bash
# rebase-stages.sh — after amending one stage branch, carry every later stage
# along the chain and re-gate them.
#
#   scripts/rebase-stages.sh 14 <old-sha-of-14>
#
# <old-sha-of-14> is the commit tutorial/14-* pointed at BEFORE you amended it
# (take it from `git rev-parse` first, or from the reflog). Each later branch is
# rebased with --onto its (already rebased) predecessor. Conflicts stop the
# script; resolve them, `git rebase --continue`, then rerun for the next stage.
set -u -o pipefail
cd "$(dirname "$0")/.."
from="$1"; oldsha="$2"
branches=$(git for-each-ref --format='%(refname:short)' 'refs/heads/tutorial/[0-9]*' | sort)
prev=$(printf '%s\n' "$branches" | grep "^tutorial/$from-"); oldprev="$oldsha"
started=0; todo=""
for b in $branches; do
  [ "$b" = "$prev" ] && { started=1; continue; }
  [ $started = 1 ] || continue
  old=$(git rev-parse "$b")
  echo "== rebase $b onto $prev"
  git rebase --onto "$prev" "$oldprev" "$b" || exit 1
  prev="$b"; oldprev="$old"; todo="$todo ${b#tutorial/}"
done
git checkout -q main
[ -n "$todo" ] && scripts/check-all-stages.sh $(for t in $todo; do echo "${t%%-*}"; done)
