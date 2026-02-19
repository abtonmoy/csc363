#!/usr/bin/env bash
# run_tests.sh
#
# For each tests/testX.ac:
#   1) compile:  acdc tests/testX.ac tests/testX.dc
#   2) run:      dc -f tests/testX.dc
#   3) run gold: dc -f outputs/testX.dc
#   4) compare stdout (pass if identical)
#
# Exit code: 0 if all pass, 1 otherwise.

set -u
shopt -s nullglob

PASS=0
FAIL=0
TOTAL=0

# Optional: let caller override paths
TEST_DIR="${TEST_DIR:-tests}"
GOLD_DIR="${GOLD_DIR:-outputs}"

# Sanity checks
if ! command -v python >/dev/null 2>&1; then
  echo "ERROR: python not found on PATH." >&2
  exit 2
fi
if [[ ! -f acdc.py ]]; then
  echo "ERROR: acdc.py not found in current directory." >&2
  exit 2
fi
if ! command -v dc >/dev/null 2>&1; then
  echo "ERROR: dc not found on PATH." >&2
  exit 2
fi

tests=( "${TEST_DIR}"/test*.ac )
if (( ${#tests[@]} == 0 )); then
  echo "No tests found matching ${TEST_DIR}/test*.ac"
  exit 2
fi

for ac_file in "${tests[@]}"; do
  base="$(basename "$ac_file" .ac)"          # e.g., test0
  dc_out_file="${TEST_DIR}/${base}.dc"       # compiled output
  gold_dc_file="${GOLD_DIR}/${base}.dc"      # expected dc program

  ((TOTAL++))

  # Compile
  if ! python acdc.py "$ac_file" "$dc_out_file" >/dev/null 2>&1; then
    echo "[FAIL] ${base}: acdc compilation failed"
    ((FAIL++))
    continue
  fi

  # Check expected file exists
  if [[ ! -f "$gold_dc_file" ]]; then
    echo "[FAIL] ${base}: missing expected file ${gold_dc_file}"
    ((FAIL++))
    continue
  fi

  # Run both, normalize CRLF just in case
  actual="$(dc -f "$dc_out_file" 2>&1 | tr -d '\r')"
  expected="$(dc -f "$gold_dc_file" 2>&1 | tr -d '\r')"

  if [[ "$actual" == "$expected" ]]; then
    echo "[PASS] ${base}"
    ((PASS++))
  else
    echo "[FAIL] ${base}"
    echo "  --- actual (dc -f ${dc_out_file}) ---"
    printf '%s\n' "$actual"
    echo "  --- expected (dc -f ${gold_dc_file}) ---"
    printf '%s\n' "$expected"
    ((FAIL++))
  fi
done

echo
echo "Summary: ${PASS} passed, ${FAIL} failed, ${TOTAL} total"

if (( FAIL > 0 )); then
  exit 1
else
  exit 0
fi