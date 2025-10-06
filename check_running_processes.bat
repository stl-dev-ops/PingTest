@echo off
echo ========================================
echo Check NetworkPingMonitor Processes
echo ========================================
echo.

echo Checking for running NetworkPingMonitor processes...
echo.

tasklist /FI "IMAGENAME eq NetworkPingMonitor.exe" /FO TABLE

echo.
echo Process Details:
wmic process where "name='NetworkPingMonitor.exe'" get ProcessId,CommandLine,CreationDate /format:table

echo.
echo If you see multiple processes, you have duplicates running!
echo.
pause