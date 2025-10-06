# Uninstall Network Ping Monitor Scheduled Task
# Run this PowerShell script as Administrator

$taskName = "NetworkPingMonitor"

Write-Host "========================================" -ForegroundColor Red
Write-Host "Uninstall Network Ping Monitor Scheduled Task" -ForegroundColor Red
Write-Host "========================================" -ForegroundColor Red
Write-Host ""

try {
    # Stop the task if running
    Write-Host "Stopping task..." -ForegroundColor Yellow
    Stop-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
    
    # Remove the task
    Write-Host "Removing task..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
    
    Write-Host "✅ Scheduled Task removed successfully!" -ForegroundColor Green
    
} catch {
    Write-Host "❌ Failed to remove scheduled task: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")