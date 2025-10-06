@echo off
echo ========================================
echo Switch to Scheduled Task Approach
echo ========================================
echo.

REM Remove the problematic service
echo Removing existing service that failed to start...
sc stop NetworkPingMonitor >nul 2>&1
sc delete NetworkPingMonitor >nul 2>&1

echo ✅ Service removed.
echo.
echo Recommended Solution: Use Scheduled Task Instead
echo ===============================================
echo.
echo The scheduled task approach is more reliable for console applications.
echo.
echo To install as scheduled task:
echo.
echo 1. Right-click PowerShell and "Run as Administrator"
echo 2. Navigate to this folder: cd C:\STLNetworkMonitor
echo 3. Run: .\install_scheduled_task.ps1
echo.
echo This will:
echo ✅ Run automatically at startup
echo ✅ Work reliably with console applications  
echo ✅ Be manageable through Task Scheduler
echo ✅ Show up in Task Manager
echo.
echo Or manually run in background:
echo   start_background.bat
echo.
pause