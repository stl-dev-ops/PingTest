@echo off
echo ========================================
echo Install Network Ping Monitor as Service
echo Using Built-in Windows SC Command
echo ========================================
echo.

REM Get current directory and executable path
set "CURRENT_DIR=%cd%"
set "EXE_PATH=%CURRENT_DIR%\dist\NetworkPingMonitor.exe"

echo Installing service using Windows SC command...
sc create "NetworkPingMonitor" binPath= "\"%EXE_PATH%\"" DisplayName= "Network Ping Monitor" start= auto

echo Setting service description...
sc description "NetworkPingMonitor" "Monitors network devices and sends email alerts"

if %errorlevel% == 0 (
    echo ✅ Service installed successfully!
    echo.
    echo Starting service...
    sc start "NetworkPingMonitor"
    
    echo.
    echo Service installed and started!
    echo.
    echo You can now see it in Windows Services console:
    echo - Press Win+R, type "services.msc", press Enter
    echo - Look for "Network Ping Monitor"
    echo.
    echo To manage the service:
    echo   Start:  sc start NetworkPingMonitor
    echo   Stop:   sc stop NetworkPingMonitor
    echo   Delete: sc delete NetworkPingMonitor
    echo.
) else (
    echo ❌ Failed to install service!
    echo Make sure you're running as Administrator.
)

pause