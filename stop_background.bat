@echo off
echo ========================================
echo Stop Network Ping Monitor Background Process
echo ========================================
echo.

echo Checking for running NetworkPingMonitor processes...
tasklist | findstr NetworkPingMonitor

echo.
echo Stopping NetworkPingMonitor.exe...
taskkill /F /IM NetworkPingMonitor.exe

echo.
echo ✅ NetworkPingMonitor background process stopped!
echo.
pause