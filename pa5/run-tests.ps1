# run-tests.ps1
#
# For each tests/testX.ac:
#   1) compile:  python acdc.py tests/testX.ac tests/testX.dc
#   2) run:      dc -f tests/testX.dc
#   3) run gold: dc -f outputs/testX.dc
#   4) compare stdout (pass if identical)
#
# Exit code: 0 if all pass, 1 otherwise.

$PASS = 0
$FAIL = 0
$TOTAL = 0

$TEST_DIR = $env:TEST_DIR
if (-not $TEST_DIR) { $TEST_DIR = "tests" }

$GOLD_DIR = $env:GOLD_DIR
if (-not $GOLD_DIR) { $GOLD_DIR = "outputs" }

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "ERROR: python not found on PATH."
    exit 2
}

if (-not (Test-Path "acdc.py")) {
    Write-Error "ERROR: acdc.py not found in current directory."
    exit 2
}

if (-not (Get-Command dc -ErrorAction SilentlyContinue)) {
    Write-Error "ERROR: dc not found on PATH."
    exit 2
}

$tests = Get-ChildItem "$TEST_DIR/test*.ac" -ErrorAction SilentlyContinue

if (-not $tests) {
    Write-Host "No tests found matching $TEST_DIR/test*.ac"
    exit 2
}

foreach ($ac_file in $tests) {

    $base = [System.IO.Path]::GetFileNameWithoutExtension($ac_file.Name)
    $dc_out_file = Join-Path $TEST_DIR "$base.dc"
    $gold_dc_file = Join-Path $GOLD_DIR "$base.dc"

    $TOTAL++

    # Compile
    $compile = python acdc.py $ac_file.FullName $dc_out_file 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[FAIL] $base : acdc compilation failed"
        $FAIL++
        continue
    }

    if (-not (Test-Path $gold_dc_file)) {
        Write-Host "[FAIL] $base : missing expected file $gold_dc_file"
        $FAIL++
        continue
    }

    # Run both
    $actual = (dc -f $dc_out_file 2>&1) -join "`n"
    $expected = (dc -f $gold_dc_file 2>&1) -join "`n"

    if ($actual -eq $expected) {
        Write-Host "[PASS] $base"
        $PASS++
    }
    else {
        Write-Host "[FAIL] $base"
        Write-Host "  --- actual (dc -f $dc_out_file) ---"
        Write-Host $actual
        Write-Host "  --- expected (dc -f $gold_dc_file) ---"
        Write-Host $expected
        $FAIL++
    }
}

Write-Host ""
Write-Host "Summary: $PASS passed, $FAIL failed, $TOTAL total"

if ($FAIL -gt 0) {
    Write-Host "❌ Some tests failed. Keep debugging — you’ve got this."
    exit 1
}
else {
    Write-Host "🎉🎉 All tests passed! Outstanding work! 🎉🎉"
    Write-Host "🚀 Your compiler is behaving exactly as expected."
    exit 0
}