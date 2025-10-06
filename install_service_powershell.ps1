# Install Network Ping Monitor as Windows Service
# Using PowerShell New-Service cmdlet (Windows 10/Server 2016+)
# Run as Administrator

$serviceName = "NetworkPingMonitor"
$displayName = "Network Ping Monitor"
$description = "Monitors network devices and sends email alerts"
$exePath = "$PSScriptRoot\dist\NetworkPingMonitor.exe"

Write-Host "========================================" -ForegroundColor Green
Write-Host "Install Network Ping Monitor as Service" -ForegroundColor Green
Write-Host "Using PowerShell New-Service" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Check if executable exists
if (-not (Test-Path $exePath)) {
    Write-Host "❌ NetworkPingMonitor.exe not found at: $exePath" -ForegroundColor Red
    Write-Host "Please ensure the executable is built and available." -ForegroundColor Red
    pause
    exit 1
}

try {
    # Remove existing service if it exists
    $existingService = Get-Service -Name $serviceName -ErrorAction SilentlyContinue
    if ($existingService) {
        Write-Host "Removing existing service..." -ForegroundColor Yellow
        Stop-Service -Name $serviceName -Force -ErrorAction SilentlyContinue
        Remove-Service -Name $serviceName -Force
        Start-Sleep -Seconds 2
    }

    # Create the service
    Write-Host "Creating Windows service..." -ForegroundColor Cyan
    New-Service -Name $serviceName -BinaryPathName $exePath -DisplayName $displayName -Description $description -StartupType Automatic

    Write-Host "✅ Service created successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Service Details:" -ForegroundColor Cyan
    Write-Host "  Name: $serviceName" -ForegroundColor Gray
    Write-Host "  Display Name: $displayName" -ForegroundColor Gray
    Write-Host "  Executable: $exePath" -ForegroundColor Gray
    Write-Host "  Startup: Automatic" -ForegroundColor Gray
    Write-Host ""
    
    # Start the service
    $startNow = Read-Host "Start the service now? (y/n)"
    if ($startNow -eq 'y' -or $startNow -eq 'Y') {
        Write-Host "Starting service..." -ForegroundColor Cyan
        Start-Service -Name $serviceName
        Write-Host "✅ Service started!" -ForegroundColor Green
        
        # Show service status
        Get-Service -Name $serviceName | Format-Table -AutoSize
    }
    
    Write-Host ""
    Write-Host "🎉 You can now see the service in Windows Services console:" -ForegroundColor Yellow
    Write-Host "   1. Press Win+R" -ForegroundColor Gray
    Write-Host "   2. Type 'services.msc'" -ForegroundColor Gray
    Write-Host "   3. Press Enter" -ForegroundColor Gray
    Write-Host "   4. Look for 'Network Ping Monitor'" -ForegroundColor Gray
    Write-Host ""
    Write-Host "PowerShell Commands:" -ForegroundColor Yellow
    Write-Host "  Start:  Start-Service -Name '$serviceName'" -ForegroundColor Gray
    Write-Host "  Stop:   Stop-Service -Name '$serviceName'" -ForegroundColor Gray
    Write-Host "  Status: Get-Service -Name '$serviceName'" -ForegroundColor Gray
    Write-Host "  Remove: Remove-Service -Name '$serviceName'" -ForegroundColor Gray

} catch {
    Write-Host "❌ Failed to create service: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Make sure you're running PowerShell as Administrator." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")