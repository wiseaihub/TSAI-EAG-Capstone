param(
    [ValidateSet("ollama", "llama_cpp_host")]
    [string]$Mode = "ollama",
    [switch]$Build
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$Root = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$ComposeDir = Resolve-Path $PSScriptRoot

$envFile = if ($Mode -eq "llama_cpp_host") {
    Join-Path $ComposeDir ".env.full.llama-cpp-host"
}
else {
    Join-Path $ComposeDir ".env.full.ollama"
}

if (-not (Test-Path $envFile)) {
    throw "Missing env file: $envFile"
}

Push-Location $ComposeDir
try {
    $args = @("--env-file", $envFile, "-f", "docker-compose.full.yml", "up", "-d")
    if ($Build) {
        $args = @("--env-file", $envFile, "-f", "docker-compose.full.yml", "up", "-d", "--build")
    }
    & docker compose @args
}
finally {
    Pop-Location
}

Write-Host "Full stack started with mode '$Mode'."
Write-Host "Env file: $envFile"
if ($Mode -eq "llama_cpp_host") {
    Write-Host "Expect host llama-server at http://host.docker.internal:8080"
}
else {
    Write-Host "Using bundled s18share-ollama at http://s18share-ollama:11434"
}
