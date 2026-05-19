# Start the Flask API on Windows (waitress). Run from Backend folder or any path.
$ErrorActionPreference = "Stop"
$Root = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
if (-not (Test-Path "$Root\app.py")) {
    $Root = Split-Path $PSScriptRoot -Parent
}
Set-Location $Root

function Get-PythonLauncher {
    if (Get-Command py -ErrorAction SilentlyContinue) {
        return { param($Args) & py @Args }
    }
    if (Get-Command python -ErrorAction SilentlyContinue) {
        return { param($Args) & python @Args }
    }
    if (Get-Command python3 -ErrorAction SilentlyContinue) {
        return { param($Args) & python3 @Args }
    }
    return $null
}

$launch = Get-PythonLauncher
if (-not $launch) {
    Write-Host ""
    Write-Host "Python is not installed or not on PATH."
    Write-Host "1. Download Python 3.12: https://www.python.org/downloads/windows/"
    Write-Host "2. Run the installer and CHECK: 'Add python.exe to PATH'"
    Write-Host "3. Close PowerShell, open a new window, then run this script again."
    Write-Host ""
    Write-Host "Or use Docker: docker build -t tma-be-api . ; docker run -p 5050:8080 --env-file .env tma-be-api"
    exit 1
}

if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Host "Creating virtual environment..."
    if (Get-Command py -ErrorAction SilentlyContinue) {
        & py -3 -m venv .venv
    } else {
        & $launch -m venv .venv
    }
}

& .\.venv\Scripts\pip install -q -r requirements.txt

$Port = if ($env:PORT) { $env:PORT } else { "5050" }
Write-Host "API listening on http://0.0.0.0:${Port}  (health: /api/health)"
& .\.venv\Scripts\waitress-serve --listen="0.0.0.0:${Port}" app:app
