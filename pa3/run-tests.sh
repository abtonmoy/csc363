#!/bin/bash

passed=0
failed=0
total=0

run_test () {
    base="$1"
    acfile="tests/${base}.ac"
    out_test="tests/${base}.dc"
    out_expected="outputs/${base}.dc"

    if [ ! -f "$acfile" ]; then
        echo "❌ Test input not found: $acfile"
        return
    fi

    if [ ! -f "$out_expected" ]; then
        echo "❌ Expected output not found: $out_expected"
        return
    fi

    echo "Running $base..."

    python3 acdc.py "$acfile" "$out_test"

    if diff -q "$out_test" "$out_expected" > /dev/null; then
        echo "  ✅ PASS"
        passed=$((passed + 1))
    else
        echo "  ❌ FAIL"
        echo "     Differences:"
        diff "$out_test" "$out_expected"
        failed=$((failed + 1))
    fi

    total=$((total + 1))
    echo
}

# If a test name is given, run only that test
if [ $# -eq 1 ]; then
    run_test "$1"
else
    # Otherwise, run all tests
    for acfile in tests/*.ac; do
        base=$(basename "$acfile" .ac)
        run_test "$base"
    done
fi

# Summary
echo "========================"
echo "Test Summary"
echo "------------------------"
echo "Total:  $total"
echo "Passed: $passed"
echo "Failed: $failed"

if [ $failed -eq 0 ]; then
    echo "🎉 All tests passed!"
else
    echo "⚠️  Some tests failed."
fi