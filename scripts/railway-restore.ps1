# Restore WISE + S18 Railway production settings (run after: railway login)
# Usage:
#   cd wise-ai
#   .\scripts\railway-restore.ps1

$ErrorActionPreference = "Stop"

function Require-Railway {
    railway whoami | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw "Run 'railway login' first."
    }
}

Require-Railway

Write-Host "=== S18 (https://s18.up.railway.app) ===" -ForegroundColor Cyan
Push-Location (Join-Path $PSScriptRoot "..\..\S18Share\S18Share")
try {
    railway link 2>$null
    railway variables set `
        S18_MODEL_PROVIDER=gemini `
        S18_PROFILE=railway-gemini `
        --service s18 2>$null
    if ($LASTEXITCODE -ne 0) {
        railway variables set S18_MODEL_PROVIDER=gemini
        railway variables set S18_PROFILE=railway-gemini
    }
    Write-Host "Ensure GEMINI_API_KEY and SUPABASE_URL are set in Railway dashboard for S18." -ForegroundColor Yellow
    railway redeploy --yes 2>$null
    if ($LASTEXITCODE -ne 0) { railway up -d 2>$null }
}
finally {
    Pop-Location
}

Write-Host "=== WISE backend (tsai-eag-capstone-production) ===" -ForegroundColor Cyan
Push-Location (Join-Path $PSScriptRoot "..")
try {
    railway link 2>$null
    railway variables set `
        S18_BASE_URL=https://s18.up.railway.app `
        --service TSAI-EAG-Capstone 2>$null
    if ($LASTEXITCODE -ne 0) {
        railway variables set S18_BASE_URL=https://s18.up.railway.app
    }
    railway redeploy --yes 2>$null
    if ($LASTEXITCODE -ne 0) { railway up -d 2>$null }
}
finally {
    Pop-Location
}

Write-Host "Done. Verify:" -ForegroundColor Green
Write-Host "  curl https://tsai-eag-capstone-production.up.railway.app/health"
Write-Host "  curl https://s18.up.railway.app/health"
