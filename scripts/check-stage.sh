#!/usr/bin/env bash
# check-stage.sh — the gate every tutorial stage branch must pass.
#
# Runs, from the project root:
#   1. dogsbay-xml validate-project   every topic and map validates against its DOCTYPE
#      (learning/*.dita against the DITA-OT catalog: the editor's catalog has no L&T DTDs)
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
set -u -o pipefail

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
vp="$(mktemp)"
if ! "$DOGSBAY_XML" validate-project "$ROOT" | tee "$vp"; then
  # The editor's built-in catalog does not ship the Learning and Training DTDs.
  # Files under learning/ are validated against DITA-OT's catalog instead; any
  # other invalid file is a real failure.
  others=$(grep -E '^/.*\.dita(map)?:$' "$vp" | grep -v "^$ROOT/learning/" || true)
  if [ -n "$others" ]; then
    fail "validation errors"
  else
    say "validate learning/ against the DITA-OT catalog"
    for f in "$ROOT"/learning/*.dita; do
      "$DOGSBAY_XML" validate --catalog "$DITA_HOME/catalog-dita.xml" "$f" || fail "validation errors in $f"
    done
  fi
fi
rm -f "$vp"

say "project-health  $ROOT"
health=("$DOGSBAY_XML" project-health)
# validate-project above already covered grammar validation; project-health's own
# validation pass would trip over learning/ (no L&T DTDs in the editor catalog).
# Schematron is left out of the explicit list because --include requires rules;
# once .dogsbay/config.xml names a <default-schematron>, run it separately below.
[ -d "$ROOT/learning" ] && health+=(--include=reuse,elementIds,metadata,proposals,conrefPush,index,format,markers)
if [ "$STRICT" = "1" ]; then
  "${health[@]}" "$ROOT" || fail "project-health found issues"
else
  "${health[@]}" --severity=error "$ROOT" || fail "project-health found errors"
fi
if [ -d "$ROOT/learning" ] && grep -q '<default-schematron>' "$ROOT/.dogsbay/config.xml" 2>/dev/null; then
  say "house rules  $ROOT"
  "$DOGSBAY_XML" project-health --include=schematron "$ROOT" || fail "house-rule violations"
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
