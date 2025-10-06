@echo off
echo ========================================
echo Fix Service Installation with NSSM
echo ========================================
echo.

REM First, remove the existing service that's not working
echo Removing existing service...
sc stop NetworkPingMonitor >nul 2>&1
sc delete NetworkPingMonitor >nul 2>&1

echo.
echo NSSM Installation Required
echo =========================
echo.
echo The service was created but failed to start because console
echo applications need a service wrapper like NSSM.
echo.
echo Please download NSSM to fix this:
echo.
echo 1. Go to: https://nssm.cc/download
echo 2. Download nssm-2.24.zip
echo 3. Extract nssm.exe to this folder: %cd%
echo 4. Run: install_with_nssm.bat
echo.
echo Alternative: Use the scheduled task approach instead
echo Run: install_scheduled_task.ps1 (in PowerShell as Administrator)
echo.
pause