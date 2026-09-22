#!/usr/bin/env bash
# check-stage.sh — the gate every tutorial stage branch must pass.
#
# Runs, from the project root:
#   1. dogsbay-xml validate-project   every topic and map validates against its DOCTYPE
#   2. dogsbay-xml project-health     links, keys, element ids, conref pushes, index,
#                                     metadata policy and house rules are clean
#   2b. dogsbay-xml validate-conditions (once a subject scheme is referenced) every
#                                     platform/audience value is a controlled value
#   3. dita --project=project.json    every deliverable actually publishes
#
# Exit code is non-zero when any gate fails. Usage:
#   scripts/check-stage.sh [project-root]           (default: the repo root)
#   STRICT=0 scripts/check-stage.sh                 (project-health at severity=error only)
#   SKIP_BUILD=1 scripts/check-stage.sh             (skip the DITA-OT build)
#
# Tooling is found from, in order: $DOGSBAY_XML / $DITA_HOME, the PATH, then the
# developer defaults below.
set -u

ROOT="$(cd "${1:-$(dirname "$0")/..}" && pwd)"
DOGSBAY_XML="${DOGSBAY_XML:-$(command -v dogsbay-xml || echo "$HOME/github/dogsbay-xml/bin/dogsbay-xml")}"
DITA_HOME="${DITA_HOME:-$HOME/Downloads/dita-ot-4.3.5}"
DITA="${DITA:-$(command -v dita || echo "$DITA_HOME/bin/dita")}"
STRICT="${STRICT:-1}"
SKIP_BUILD="${SKIP_BUILD:-0}"
OUT="${OUT:-${TMPDIR:-/tmp}/check-stage-$$}"

status=0
say() { printf '\n== %s ==\n' "$*"; }
fail() { status=1; printf 'FAIL: %s\n' "$*"; }

[ -x "$DOGSBAY_XML" ] || { echo "dogsbay-xml CLI not found (set DOGSBAY_XML)"; exit 2; }

say "validate-project  $ROOT"
"$DOGSBAY_XML" validate-project "$ROOT" || fail "validation errors"

say "project-health  $ROOT"
if [ "$STRICT" = "1" ]; then
  "$DOGSBAY_XML" project-health "$ROOT" || fail "project-health found issues"
else
  "$DOGSBAY_XML" project-health --severity=error "$ROOT" || fail "project-health found errors"
fi

scheme=$(grep -l '<subjectScheme' "$ROOT"/*.ditamap 2>/dev/null | head -1 || true)
if [ -n "$scheme" ]; then
  # Without -S (or -m) the command discovers no scheme and passes vacuously.
  say "validate-conditions  $ROOT  (scheme: ${scheme#$ROOT/})"
  "$DOGSBAY_XML" validate-conditions -S "$scheme" "$ROOT" || fail "profiling values outside the subject scheme"
fi

if [ "$SKIP_BUILD" = "1" ]; then
  say "build  skipped (SKIP_BUILD=1)"
elif [ -f "$ROOT/project.json" ]; then
  [ -x "$DITA" ] || { echo "dita command not found (set DITA_HOME or DITA)"; exit 2; }
  say "build  project.json -> $OUT"
  log="$OUT.log"; mkdir -p "$OUT"
  # DITA-OT does not always exit non-zero on content errors, so also grep the log.
  if ! (cd "$ROOT" && "$DITA" --project=project.json --output="$OUT" >"$log" 2>&1) \
     || grep -qE '^Error:|\[(DOT[A-Z]+[0-9]+[EF])\]' "$log"; then
    grep -E '^Error:|\[(DOT[A-Z]+[0-9]+[EF])\]' "$log" | sort -u | head -40
    fail "DITA-OT build reported errors (full log: $log)"
  else
    echo "all deliverables built"
  fi
else
  say "build  skipped (no project.json yet)"
fi

echo
[ "$status" = 0 ] && echo "STAGE OK" || echo "STAGE FAILED"
exit "$status"
