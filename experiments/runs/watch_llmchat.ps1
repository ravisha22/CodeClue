param(
    [string]$ChatPath = "LLMchat.md",
    [string]$LogPath = "experiments/runs/llmchat-watch.log"
)

$resolvedChat = (Resolve-Path $ChatPath).Path
$resolvedLog = Join-Path (Get-Location) $LogPath
$logDir = Split-Path $resolvedLog -Parent
New-Item -ItemType Directory -Path $logDir -Force | Out-Null

function Write-Log {
    param([string[]]$Lines)

    $timestamp = Get-Date -Format o
    Add-Content -Path $resolvedLog -Value "=== $timestamp ==="
    if ($Lines.Count -gt 0) {
        Add-Content -Path $resolvedLog -Value $Lines
    }
    Add-Content -Path $resolvedLog -Value ""
}

function Read-Lines {
    param([string]$Path)

    try {
        return @(Get-Content -Path $Path -ErrorAction Stop)
    }
    catch {
        return @()
    }
}

$watcher = New-Object System.IO.FileSystemWatcher
$watcher.Path = Split-Path $resolvedChat -Parent
$watcher.Filter = Split-Path $resolvedChat -Leaf
$watcher.NotifyFilter = [System.IO.NotifyFilters]::LastWrite -bor [System.IO.NotifyFilters]::Size -bor [System.IO.NotifyFilters]::FileName

$lastLines = Read-Lines -Path $resolvedChat
$lastJoined = $lastLines -join "`n"

Write-Log -Lines @("Watcher started for $resolvedChat")

while ($true) {
    $change = $watcher.WaitForChanged([System.IO.WatcherChangeTypes]::Changed, 5000)
    if ($change.TimedOut) {
        continue
    }

    $currentLines = Read-Lines -Path $resolvedChat
    $currentJoined = $currentLines -join "`n"

    if ($currentJoined -eq $lastJoined) {
        continue
    }

    if ($currentLines.Count -gt $lastLines.Count) {
        $newLines = $currentLines[$lastLines.Count..($currentLines.Count - 1)]
        Write-Log -Lines $newLines
    }
    else {
        Write-Log -Lines @("File changed but was not a clean append. Manual review required.")
    }

    $lastLines = $currentLines
    $lastJoined = $currentJoined
    Write-Output ("LLMchat changed at {0}" -f (Get-Date -Format o))
}