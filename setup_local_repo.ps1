$ErrorActionPreference = "Stop"
$Target = "C:\work\isochron_phase_curvature"
$Source = (Resolve-Path $PSScriptRoot).Path
$TargetFull = [System.IO.Path]::GetFullPath($Target)

New-Item -ItemType Directory -Path $TargetFull -Force | Out-Null

if ($Source.TrimEnd('\\') -ine $TargetFull.TrimEnd('\\')) {
    Get-ChildItem -LiteralPath $Source -Force |
        Where-Object { $_.Name -ne ".git" } |
        ForEach-Object {
            Copy-Item -LiteralPath $_.FullName -Destination $TargetFull -Recurse -Force
        }
}

Set-Location $TargetFull

if (Get-Command git -ErrorAction SilentlyContinue) {
    if (-not (Test-Path ".git")) {
        git init -b main | Out-Null
    }
}

Write-Host "ISOCHRON working repository is ready at $TargetFull"
