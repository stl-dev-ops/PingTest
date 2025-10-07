<#
Install Network Ping Monitor as Scheduled Task (robust)
Run this script as Administrator: right-click -> Run with PowerShell or run from an elevated PowerShell session.

This script is defensive about:
- $PSScriptRoot being empty when copy-pasting into a console
- Admin rights check
- Missing executable
- Existing scheduled task removal
- Clear error reporting
#>

param(
    [string]$TaskName = "NetworkPingMonitor",
    [string]$ExeRelativePath = "dist\NetworkPingMonitor.exe",
    [switch]$StartNow
)

function Write-Err([string]$m) { Write-Host $m -ForegroundColor Red }
function Write-Ok([string]$m)  { Write-Host $m -ForegroundColor Green }

# Determine script root: prefer PSScriptRoot when available, otherwise current directory
$scriptRoot = if ($PSScriptRoot) { $PSScriptRoot } else { (Get-Location).Path }
$exePath = Join-Path -Path $scriptRoot -ChildPath $ExeRelativePath
$workingDir = $scriptRoot

Write-Host "Installing Scheduled Task: $TaskName" -ForegroundColor Cyan
Write-Host "Resolved script root: $scriptRoot"
Write-Host "Looking for executable at: $exePath"

# Admin check
$principal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
if (-not $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Err "This script must be run as Administrator. Please open an elevated PowerShell and re-run."
    exit 1
}

# Check exe exists
if (-not (Test-Path -Path $exePath)) {
    Write-Err "NetworkPingMonitor.exe not found at: $exePath"
    Write-Host "Make sure you have built the exe and that you run this script from the install directory or provide -ExeRelativePath pointing to the exe." -ForegroundColor Yellow
    exit 1
}

# Remove existing task if it exists
try {
    $existing = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
    if ($existing) {
        Write-Host "Removing existing scheduled task $TaskName..." -ForegroundColor Yellow
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction Stop
    }
} catch {
    Write-Host "Warning: failed removing existing task (continuing): $($_.Exception.Message)" -ForegroundColor Yellow
}

# Build task objects
try {
    $action = New-ScheduledTaskAction -Execute "$exePath" -WorkingDirectory "$workingDir"
    $trigger = New-ScheduledTaskTrigger -AtStartup
    $principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest
    $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -RunOnlyIfNetworkAvailable -DontStopOnIdleEnd
} catch {
    Write-Err "Failed to create scheduled task objects: $($_.Exception.Message)"
    exit 1
}

# Register task
try {
    Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Principal $principal -Settings $settings -Description "Network Ping Monitor - Monitors devices and sends email alerts" -ErrorAction Stop
    Write-Ok "Scheduled Task '$TaskName' registered successfully."
    Write-Host "Executable: $exePath"
    Write-Host "Working dir: $workingDir"
    Write-Host "Trigger: At system startup"
    Write-Host "Run as: SYSTEM (ServiceAccount)"
} catch {
    Write-Err "Failed to register scheduled task: $($_.Exception.Message)"
    exit 1
}

if ($StartNow.IsPresent) {
    try {
        Start-ScheduledTask -TaskName $TaskName -ErrorAction Stop
        Write-Ok "Task started successfully."
    } catch {
        Write-Err "Failed to start the task: $($_.Exception.Message)"
    }
} else {
    $choice = Read-Host "Start the task now? (y/n)"
    if ($choice -match '^[yY]') {
        try {
            Start-ScheduledTask -TaskName $TaskName -ErrorAction Stop
            Write-Ok "Task started successfully."
        } catch {
            Write-Err "Failed to start the task: $($_.Exception.Message)"
        }
    } else {
        Write-Host "You can start the task later with: Start-ScheduledTask -TaskName $TaskName" -ForegroundColor Gray
    }
}

Write-Host "Done."
