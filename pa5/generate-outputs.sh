#!/usr/bin/env bash
# generate-expected.sh
#
# For each outputs/testX.dc:
#   run dc -f outputs/testX.dc
#   write result to outputs/testX.out
#
# Exit code: 0 if all succeed, nonzero otherwise.

set -u
shopt -s nullglob

OUTPUT_DIR="${OUTPUT_DIR:-outputs}"

if ! command -v dc >/dev/null 2>&1; then
  echo "ERROR: dc not found on PATH." >&2
  exit 2
fi

files=( "${OUTPUT_DIR}"/test*.dc )

if (( ${#files[@]} == 0 )); then
  echo "No files found matching ${OUTPUT_DIR}/test*.dc"
  exit 2
fi

COUNT=0

for dc_file in "${files[@]}"; do
  base="$(basename "$dc_file" .dc)"        # testX
  out_file="${OUTPUT_DIR}/${base}.out"    # outputs/testX.out

  echo "Generating ${out_file} from ${dc_file}..."

  if dc -f "$dc_file" > "$out_file" 2>&1; then
    ((COUNT++))
  else
    echo "ERROR running ${dc_file}" >&2
  fi
done

echo
echo "Generated ${COUNT} .out file(s)."
exit 0