# Run all .ac tests: python3 acdc.py tests/testX.ac tests/testX.dc

$ErrorActionPreference = "Stop"

Get-ChildItem -Path "tests" -Filter "*.ac" | ForEach-Object {
    $acfile = $_.FullName
    $base = $_.BaseName
    $dcfile = Join-Path "tests" ($base + ".dc")

    Write-Host "Running: $base"
    python acdc.py $acfile $dcfile
}