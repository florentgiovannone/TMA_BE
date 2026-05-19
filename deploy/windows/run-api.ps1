# Start the Flask API on Windows (waitress). Run from Backend folder or any path.
$ErrorActionPreference = "Stop"
$Root = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
if (-not (Test-Path "$Root\app.py")) {
    $Root = Split-Path $PSScriptRoot -Parent
}
Set-Location $Root

if (-not (Test-Path ".venv\Scripts\python.exe")) {
    py -3.12 -m venv .venv
}

& .\.venv\Scripts\pip install -q -r requirements.txt

$Port = if ($env:PORT) { $env:PORT } else { "5050" }
Write-Host "API listening on http://0.0.0.0:${Port}  (health: /api/health)"
& .\.venv\Scripts\waitress-serve --listen="0.0.0.0:${Port}" app:app
