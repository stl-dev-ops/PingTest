@echo off
echo ========================================
echo Stop ALL NetworkPingMonitor Processes
echo ========================================
echo.

echo Stopping all NetworkPingMonitor.exe processes...
taskkill /F /IM NetworkPingMonitor.exe

echo.
echo Checking if any processes remain...
tasklist /FI "IMAGENAME eq NetworkPingMonitor.exe" /FO TABLE

echo.
echo All NetworkPingMonitor processes have been stopped.
echo.
echo To start again with only ONE instance:
echo   Option 1: Use scheduled task only (recommended)
echo   Option 2: Use background process only (manual restart after reboot)
echo.
echo Do NOT use both at the same time!
echo.
pause