# Rebuild and restart the full stack (wise-ai backend + frontend + S18Share + Ollama).
# Run from PowerShell: .\rebuild-full-stack.ps1
# Requires: S18Share at default sibling path, or set S18_PATH to your S18Share/S18Share folder.

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

Write-Host "Stopping stack..."
docker compose -f docker-compose.full.yml down

Write-Host "Building and starting (this may take several minutes)..."
docker compose -f docker-compose.full.yml up -d --build --force-recreate

Write-Host "Status:"
docker compose -f docker-compose.full.yml ps -a
