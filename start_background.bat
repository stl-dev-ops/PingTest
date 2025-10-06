@echo off
echo ========================================
echo Start Network Ping Monitor in Background
echo ========================================
echo.

echo Starting NetworkPingMonitor.exe in background...

REM Start the executable minimized and detached
start "Network Ping Monitor" /MIN /B dist\NetworkPingMonitor.exe

echo.
echo ✅ NetworkPingMonitor started in background!
echo.
echo The monitor is now running minimized in the background.
echo.
echo To check if it's running:
echo   tasklist | findstr NetworkPingMonitor
echo.
echo To stop it:
echo   taskkill /F /IM NetworkPingMonitor.exe
echo.
echo Logs will be created in the 'logs' folder.
echo.
pause