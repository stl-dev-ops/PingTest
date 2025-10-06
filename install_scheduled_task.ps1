# Install Network Ping Monitor as Scheduled Task
# Run this PowerShell script as Administrator

$taskName = "NetworkPingMonitor"
$exePath = "$PSScriptRoot\dist\NetworkPingMonitor.exe"
$workingDir = $PSScriptRoot

Write-Host "========================================" -ForegroundColor Green
Write-Host "Install Network Ping Monitor as Scheduled Task" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Check if executable exists
if (-not (Test-Path $exePath)) {
    Write-Host "❌ NetworkPingMonitor.exe not found at: $exePath" -ForegroundColor Red
    Write-Host "Please ensure the executable is built and available." -ForegroundColor Red
    pause
    exit 1
}

# Remove existing task if it exists
try {
    $existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
    if ($existingTask) {
        Write-Host "Removing existing task..." -ForegroundColor Yellow
        Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
    }
} catch {
    # Task doesn't exist, continue
}

# Create the scheduled task action
$action = New-ScheduledTaskAction -Execute $exePath -WorkingDirectory $workingDir

# Create the trigger (at startup)
$trigger = New-ScheduledTaskTrigger -AtStartup

# Create the principal (run as SYSTEM)
$principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest

# Create the settings
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -RunOnlyIfNetworkAvailable -DontStopOnIdleEnd

# Register the scheduled task
try {
    Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Principal $principal -Settings $settings -Description "Network Ping Monitor - Monitors network devices and sends email alerts"
    
    Write-Host "✅ Scheduled Task created successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Task Name: $taskName" -ForegroundColor Cyan
    Write-Host "Executable: $exePath" -ForegroundColor Cyan
    Write-Host "Trigger: At system startup" -ForegroundColor Cyan
    Write-Host "User: SYSTEM" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "To manage the task:" -ForegroundColor Yellow
    Write-Host "  Start:  Start-ScheduledTask -TaskName '$taskName'" -ForegroundColor Gray
    Write-Host "  Stop:   Stop-ScheduledTask -TaskName '$taskName'" -ForegroundColor Gray
    Write-Host "  Status: Get-ScheduledTask -TaskName '$taskName'" -ForegroundColor Gray
    Write-Host "  Remove: Unregister-ScheduledTask -TaskName '$taskName'" -ForegroundColor Gray
    Write-Host ""
    
    # Start the task immediately
    $startNow = Read-Host "Start the task now? (y/n)"
    if ($startNow -eq 'y' -or $startNow -eq 'Y') {
        Start-ScheduledTask -TaskName $taskName
        Write-Host "✅ Task started!" -ForegroundColor Green
    }
    
} catch {
    Write-Host "❌ Failed to create scheduled task: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")