<#
Deploy helper for NetworkPingMonitor.exe
- Stops the scheduled task (if present)
- Kills any running NetworkPingMonitor.exe processes that are running from the scheduled task's path (safe kill)
- Backs up existing exe and logs
- Copies new exe into place
- Starts the scheduled task
- Verifies single instance and that log header is present

Usage:
  # Run as Administrator
  .\deploy_replace_exe.ps1 -TaskName 'NetworkPingMonitor' -ScheduledPath 'C:\STLNetworkMonitor\dist' -NewExePath 'C:\dev\PingTest\dist\NetworkPingMonitor.exe' -BackupDir 'C:\STLNetworkMonitor\backup'
#>
param(
    [string]$TaskName = 'NetworkPingMonitor',
    [string]$ScheduledPath = 'C:\STLNetworkMonitor\dist',
    [string]$NewExePath = 'C:\dev\PingTest\dist\NetworkPingMonitor.exe',
    [string]$BackupDir = 'C:\STLNetworkMonitor\backup',
    [switch]$Verbose
)

function Write-Log { param($s) Write-Host "[deploy] $s" }

if (-not (Test-Path $NewExePath)) {
    Write-Error "New exe not found at $NewExePath"
    exit 2
}

# Ensure running as Administrator
$identity = [System.Security.Principal.WindowsIdentity]::GetCurrent()
$principal = New-Object System.Security.Principal.WindowsPrincipal($identity)
if (-not $principal.IsInRole([System.Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Error "This script must be run as Administrator"
    exit 3
}

$exeName = [System.IO.Path]::GetFileName($NewExePath)
$destExe = Join-Path $ScheduledPath $exeName

# Stop scheduled task if it exists
try {
    $task = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
    if ($task) {
        Write-Log "Stopping scheduled task $TaskName"
        Stop-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
        Start-Sleep -Seconds 1
    } else {
        Write-Log "Scheduled task '$TaskName' not found. Continuing."
    }
} catch {
    Write-Log "Warning: could not query/stop scheduled task: $_"
}

# Find running processes for the exe and only kill those whose path matches the scheduled path
$procs = Get-CimInstance Win32_Process -Filter "Name = '$exeName'" | ForEach-Object {
    $p = $_
    $cmd = $p.CommandLine
    [PSCustomObject]@{ProcessId=$p.ProcessId; CommandLine=$cmd}
}

foreach ($p in $procs) {
    if ($p.CommandLine -and $p.CommandLine -like "*$ScheduledPath*") {
        Write-Log "Killing process $($p.ProcessId) running from scheduled path"
        Stop-Process -Id $p.ProcessId -Force -ErrorAction SilentlyContinue
    } else {
        Write-Log "Leaving process $($p.ProcessId) alone (different path)"
    }
}

# Backup existing exe and logs
if (-not (Test-Path $BackupDir)) { New-Item -ItemType Directory -Path $BackupDir -Force | Out-Null }
$timestamp = (Get-Date).ToString('yyyyMMdd_HHmmss')
$backupExe = Join-Path $BackupDir "${exeName}.${timestamp}.bak"
if (Test-Path $destExe) {
    Write-Log "Backing up current exe to $backupExe"
    Copy-Item -Path $destExe -Destination $backupExe -Force
}

# Backup logs directory if present
$logsDir = Join-Path $ScheduledPath 'logs'
if (Test-Path $logsDir) {
    $backupLogs = Join-Path $BackupDir "logs.${timestamp}.zip"
    Write-Log "Archiving logs to $backupLogs"
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    [System.IO.Compression.ZipFile]::CreateFromDirectory($logsDir, $backupLogs)
}

# Copy new exe
Write-Log "Copying new exe to $destExe"
Copy-Item -Path $NewExePath -Destination $destExe -Force

# Start scheduled task if present
try {
    if ($task) {
        Write-Log "Starting scheduled task $TaskName"
        Start-ScheduledTask -TaskName $TaskName
    } else {
        Write-Log "No scheduled task to start. You may want to start the exe manually or create a task."
    }
} catch {
    Write-Log "Warning: could not start scheduled task: $_"
}

Start-Sleep -Seconds 3

# Verify only one process is running from scheduled path
$running = Get-CimInstance Win32_Process -Filter "Name = '$exeName'" | Where-Object { $_.CommandLine -and $_.CommandLine -like "*$ScheduledPath*" }
$count = ($running | Measure-Object).Count
Write-Log "Found $count instance(s) running from $ScheduledPath"

if ($count -eq 0) {
    Write-Log "No running instances found. Check Task Scheduler or start manually."
} elseif ($count -gt 1) {
    Write-Log "Multiple instances detected - investigate scheduled task settings or previous manual starts."
} else {
    $pid = $running.ProcessId
    Write-Log "Single instance running (PID $pid). Checking log header presence..."
    # Wait for CSV to be created
    $logsDir = Join-Path $ScheduledPath 'logs'
    if (Test-Path $logsDir) {
        $latest = Get-ChildItem -Path $logsDir -Filter "ping_log_*.csv" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
        if ($latest) {
            $first = Get-Content $latest.FullName -TotalCount 1
            if ($first -match "Timestamp" -and $first -match "IP Address") {
                Write-Log "CSV header present in $($latest.Name)"
            } else {
                Write-Log "CSV header missing in $($latest.Name) - consider running tools/fix_logs_add_headers.py or inspect logs"
            }
        } else {
            Write-Log "No CSV log files found yet. The monitor may create logs soon."
        }
    } else {
        Write-Log "Logs directory not found at $logsDir"
    }
}

Write-Log "Deploy script finished."
