#!/usr/bin/env bash
# check-tests.sh
#
# For each tests/testX.dc:
#   1) run:  dc -f tests/testX.dc
#   2) read expected output from: tests/testX.out
#   3) compare (pass if identical)
#
# Exit code: 0 if all pass, 1 otherwise.

set -u
shopt -s nullglob

PASS=0
FAIL=0
TOTAL=0

TEST_DIR="${TEST_DIR:-tests}"

# Sanity check
if ! command -v dc >/dev/null 2>&1; then
  echo "ERROR: dc not found on PATH." >&2
  exit 2
fi

tests=( "${TEST_DIR}"/test*.dc )
if (( ${#tests[@]} == 0 )); then
  echo "No tests found matching ${TEST_DIR}/test*.dc"
  exit 2
fi

for dc_file in "${tests[@]}"; do
  base="$(basename "$dc_file" .dc)"   # e.g., test0
  out_file="${TEST_DIR}/${base}.out"  # expected output

  ((TOTAL++))

  if [[ ! -f "$out_file" ]]; then
    echo "[FAIL] ${base}: missing expected file ${out_file}"
    ((FAIL++))
    continue
  fi

  # Run dc; normalize CRLF just in case
  actual="$(dc -f "$dc_file" 2>&1 | tr -d '\r')"
  expected="$(tr -d '\r' < "$out_file")"

  if [[ "$actual" == "$expected" ]]; then
    echo "[PASS] ${base}"
    ((PASS++))
  else
    echo "[FAIL] ${base}"
    echo "  --- actual (dc -f ${dc_file}) ---"
    printf '%s\n' "$actual"
    echo "  --- expected (${out_file}) ---"
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