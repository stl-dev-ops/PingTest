@echo off
echo ========================================
echo Uninstall Network Ping Monitor Service
echo Using Built-in Windows SC Command
echo ========================================
echo.

echo Stopping service...
sc stop "NetworkPingMonitor"

echo Deleting service...
sc delete "NetworkPingMonitor"

if %errorlevel% == 0 (
    echo ✅ Service uninstalled successfully!
    echo The service has been removed from Windows Services.
) else (
    echo ⚠️  Service may not have existed or was already removed.
)

echo.
pause