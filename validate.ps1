# ESPHome YAML Validator — Claude Code safe version (Windows)
# Usage: .\validate.ps1 <config-name>

param(
    [Parameter(Mandatory = $true)]
    [string]$ConfigName
)

$ConfigFile = "$ConfigName.yaml"
if (-not (Test-Path $ConfigFile)) {
    $ConfigFile = "config/$ConfigName.yaml"
}

& ..\esphome-env\Scripts\Activate.ps1

if (-not (Test-Path $ConfigFile)) {
    Write-Host "ERROR: Config file not found: $ConfigName.yaml"
    exit 1
}

# Capture output, filter immediately — never let full config reach stdout
$Result = esphome config $ConfigFile 2>&1 | Out-String
$ExitCode = $LASTEXITCODE

if ($ExitCode -eq 0) {
    Write-Host "PASS: $ConfigName validated successfully"
} else {
    # Extract only actionable lines
    Write-Host "FAIL: $ConfigName"
    $Result -split "`n" | Select-String -Pattern "^(ERROR|WARNING|Invalid|Failed|in /)" | Select-Object -First 20
}

exit $ExitCode
