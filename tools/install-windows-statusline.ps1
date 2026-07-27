<#
  Installs a Claude Code status line on Windows that is a faithful port of the
  macOS/Linux bash+jq+awk status line at ~/.claude/statusline.sh on this machine.

  What it does:
    1. Writes statusline.ps1 (embedded below) to $env:USERPROFILE\.claude\statusline.ps1
    2. Patches (or creates) $env:USERPROFILE\.claude\settings.json so its
       top-level "statusLine" key invokes that script, preserving every other
       existing key in settings.json untouched.

  Run on Windows with:
    powershell -NoProfile -ExecutionPolicy Bypass -File tools\install-windows-statusline.ps1
#>

$ErrorActionPreference = "Stop"

$claudeDir = Join-Path $env:USERPROFILE ".claude"
if (-not (Test-Path $claudeDir)) {
    New-Item -ItemType Directory -Path $claudeDir | Out-Null
}

$statuslinePath = Join-Path $claudeDir "statusline.ps1"

$statuslineScript = @'
# Claude Code status line:  <model>  ctx [bar] %  5h [bar] %  7d [bar] %
# Bars share one color scale: green <50%, yellow 50-80%, red >=80%.
# Port of the bash+jq+awk statusline.sh; reads the same JSON payload on stdin.

[Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)

$raw = [Console]::In.ReadToEnd()
$data = $raw | ConvertFrom-Json

$model       = $data.model.display_name
$ctx         = $data.context_window.used_percentage
$tok         = $data.context_window.total_input_tokens
$five        = $data.rate_limits.five_hour.used_percentage
$seven       = $data.rate_limits.seven_day.used_percentage
$fiveResetAt = $data.rate_limits.five_hour.resets_at
$sevenResetAt = $data.rate_limits.seven_day.resets_at

$esc = [char]27

function Get-Color([double]$p) {
    if ($p -lt 50) { return "32" }
    elseif ($p -lt 80) { return "33" }
    else { return "31" }
}

function Format-TokenCount($n) {
    if ($null -eq $n -or $n -eq "") { return "" }
    $n = [double]$n
    if ($n -ge 1000000) { return "{0:N1}M" -f ($n / 1000000) }
    elseif ($n -ge 1000) { return "{0:N0}k" -f ($n / 1000) }
    else { return "{0:N0}" -f $n }
}

function Format-Reset($resetsAt) {
    if ($null -eq $resetsAt -or $resetsAt -eq "") { return "" }
    $now = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
    $secs = [double]$resetsAt - $now
    if ($secs -le 0) { return "" }
    $h = [int][math]::Floor($secs / 3600)
    $m = [int][math]::Floor(($secs % 3600) / 60)
    if ($h -gt 0) { return "{0}h{1:D2}m" -f $h, $m }
    else { return "{0}m" -f $m }
}

function Get-Bar($label, $p, [string]$suffix) {
    if ($null -eq $p -or $p -eq "") { return "" }
    $p = [double]$p
    $w = 10
    $f = [math]::Floor($p * $w / 100 + 0.5)
    if ($f -gt $w) { $f = $w }
    if ($f -lt 0) { $f = 0 }
    $fullBlock = [char]0x2588
    $lightShade = [char]0x2591
    $middleDot = [char]0x00B7
    $col = "$esc[$(Get-Color $p)m"
    $filledStr = "$col$("$fullBlock" * $f)$esc[0m"
    $emptyStr = "$esc[2m$("$lightShade" * ($w - $f))$esc[0m"
    $bar = "$filledStr$emptyStr"
    $grey = "$esc[38;5;240m"
    $suffixStr = ""
    if ($suffix -ne "") { $suffixStr = " $grey$suffix$esc[0m" }
    $pctStr = "{0:0}" -f $p
    return "  $esc[2m$middleDot$esc[0m  $label $bar $col$pctStr%$esc[0m$suffixStr"
}

$out  = "$esc[36m$model$esc[0m"
$out += Get-Bar "ctx" $ctx (Format-TokenCount $tok)
$out += Get-Bar "5h"  $five (Format-Reset $fiveResetAt)
$out += Get-Bar "7d"  $seven (Format-Reset $sevenResetAt)

[Console]::Out.Write($out)
'@

[System.IO.File]::WriteAllText($statuslinePath, $statuslineScript, (New-Object System.Text.UTF8Encoding($false)))

$settingsPath = Join-Path $claudeDir "settings.json"
if ((Test-Path $settingsPath) -and (Get-Item $settingsPath).Length -gt 0) {
    $settings = Get-Content $settingsPath -Raw | ConvertFrom-Json
} else {
    $settings = [PSCustomObject]@{}
}

$statusLineValue = [PSCustomObject]@{
    type    = "command"
    command = "powershell -NoProfile -ExecutionPolicy Bypass -File `"$statuslinePath`""
}

if ($settings.PSObject.Properties.Name -contains "statusLine") {
    $settings.statusLine = $statusLineValue
} else {
    $settings | Add-Member -MemberType NoteProperty -Name "statusLine" -Value $statusLineValue
}

$settingsJson = $settings | ConvertTo-Json -Depth 20
[System.IO.File]::WriteAllText($settingsPath, $settingsJson, (New-Object System.Text.UTF8Encoding($false)))

Write-Host "Installed status line script at $statuslinePath"
Write-Host "Updated statusLine command in $settingsPath"
