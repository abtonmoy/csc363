param(
    [string]$TestName = ""
)

$passed = 0
$failed = 0
$total  = 0

function Run-Test([string]$base) {
    $acfile = Join-Path "tests" ($base + ".ac")
    $outTest = Join-Path "tests" ($base + ".dc")
    $outExpected = Join-Path "outputs" ($base + ".dc")

    if (-not (Test-Path $acfile)) {
        Write-Host "FAIL: Test input not found: $acfile"
        return
    }
    if (-not (Test-Path $outExpected)) {
        Write-Host "FAIL: Expected output not found: $outExpected"
        return
    }

    Write-Host "Running $base..."

    # Run compiler
    python acdc.py $acfile $outTest

    # Compare outputs
    $diff = Compare-Object (Get-Content $outTest) (Get-Content $outExpected)
    if ($null -eq $diff) {
        Write-Host "  PASS"
        $script:passed++
    } else {
        Write-Host "  FAIL"
        Write-Host "  Differences:"
        # Show a readable diff-like display
        Compare-Object (Get-Content $outTest) (Get-Content $outExpected) | Format-Table -AutoSize
        $script:failed++
    }

    $script:total++
    Write-Host ""
}

if ($TestName -ne "") {
    Run-Test $TestName
} else {
    Get-ChildItem -Path "tests" -Filter "*.ac" | ForEach-Object {
        Run-Test $_.BaseName
    }
}

Write-Host "========================"
Write-Host "Test Summary"
Write-Host "------------------------"
Write-Host ("Total:  {0}" -f $total)
Write-Host ("Passed: {0}" -f $passed)
Write-Host ("Failed: {0}" -f $failed)

if ($failed -eq 0) {
    Write-Host "All tests passed!"
} else {
    Write-Host "Some tests failed."
    exit 1
}