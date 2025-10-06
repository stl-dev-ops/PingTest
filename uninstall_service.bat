@echo off
echo ========================================
echo Uninstall Network Ping Monitor Service
echo ========================================
echo.

echo Stopping service...
nssm stop "NetworkPingMonitor"

echo Removing service...
nssm remove "NetworkPingMonitor" confirm

echo.
echo ✅ Service removed successfully!
echo.
pause