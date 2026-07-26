# ESPHome build/upload helper (Windows)
# Usage: .\esp-build.ps1 <file.yaml> [-Upload [-Device PORT]]

param(
    [Parameter(Mandatory = $false, Position = 0)]
    [string]$ConfigFile,

    [switch]$Upload,

    [string]$Device = ""
)

if (-not $ConfigFile) {
    Write-Error "Error: no config file given"
    Write-Host "Usage: esp-build.ps1 <file.yaml> [-Upload [-Device PORT]]"
    exit 1
}

if (-not (Test-Path $ConfigFile)) {
    Write-Error "Error: $ConfigFile not found"
    exit 1
}

# Extract current version and increment (skip if not defined in substitutions)
$VersionLine = Select-String -Path $ConfigFile -Pattern "device_version:" | Select-Object -First 1
if (-not $VersionLine) {
    Write-Host "No device_version found in $ConfigFile, skipping version increment"
} else {
    $CurrentVersion = [regex]::Match($VersionLine.Line, '"(.*)"').Groups[1].Value
    if (-not $CurrentVersion) {
        Write-Host "No device_version found in $ConfigFile, skipping version increment"
    } else {
        $Parts = $CurrentVersion.Split(".")
        $Major = $Parts[0]
        $Minor = [int]$Parts[1]
        $NewMinor = $Minor + 1
        $NewVersion = "$Major.$NewMinor"

        Write-Host "Incrementing version: $CurrentVersion -> $NewVersion"
        (Get-Content $ConfigFile) -replace [regex]::Escape("device_version: `"$CurrentVersion`""), "device_version: `"$NewVersion`"" | Set-Content $ConfigFile
    }
}

Write-Host "Compiling $ConfigFile..."
esphome compile $ConfigFile
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

if ($Upload) {
    if ($Device) {
        Write-Host "Uploading via USB ($Device)..."
        esphome upload $ConfigFile --device $Device
    } else {
        Write-Host "Uploading via WiFi/OTA..."
        esphome upload $ConfigFile
    }
}
