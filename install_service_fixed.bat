@echo off
echo ========================================
echo Install Network Ping Monitor as Service
echo Using Built-in Windows SC Command
echo ========================================
echo.

REM Check if running as Administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ❌ ERROR: This script must be run as Administrator!
    echo.
    echo Please:
    echo 1. Right-click Command Prompt
    echo 2. Select "Run as administrator"
    echo 3. Navigate to this folder
    echo 4. Run this script again
    echo.
    pause
    exit /b 1
)

REM Get current directory and executable path
set "CURRENT_DIR=%cd%"
set "EXE_PATH=%CURRENT_DIR%\dist\NetworkPingMonitor.exe"

REM Check if executable exists
if not exist "%EXE_PATH%" (
    echo ❌ ERROR: NetworkPingMonitor.exe not found!
    echo.
    echo Expected location: %EXE_PATH%
    echo.
    echo Please ensure the executable is built and available.
    echo.
    pause
    exit /b 1
)

echo Executable found: %EXE_PATH%
echo.

REM Stop and delete existing service if it exists
echo Checking for existing service...
sc query "NetworkPingMonitor" >nul 2>&1
if %errorlevel% == 0 (
    echo Stopping existing service...
    sc stop "NetworkPingMonitor" >nul 2>&1
    echo Deleting existing service...
    sc delete "NetworkPingMonitor" >nul 2>&1
    timeout /t 2 /nobreak >nul
)

echo Installing new service...
sc create "NetworkPingMonitor" binPath= "\"%EXE_PATH%\"" DisplayName= "Network Ping Monitor" start= auto

if %errorlevel% == 0 (
    echo Setting service description...
    sc description "NetworkPingMonitor" "Monitors network devices and sends email alerts"
    
    echo.
    echo ✅ Service installed successfully!
    echo.
    echo Starting service...
    sc start "NetworkPingMonitor"
    
    if %errorlevel% == 0 (
        echo ✅ Service started successfully!
    ) else (
        echo ⚠️  Service installed but failed to start.
        echo You can start it manually from Services console.
    )
    
    echo.
    echo ========================================
    echo SUCCESS - Service Installation Complete!
    echo ========================================
    echo.
    echo Service Details:
    echo   Name: NetworkPingMonitor
    echo   Display Name: Network Ping Monitor
    echo   Executable: %EXE_PATH%
    echo   Startup: Automatic
    echo.
    echo You can now manage the service:
    echo.
    echo From Services Console:
    echo   1. Press Win+R
    echo   2. Type: services.msc
    echo   3. Look for "Network Ping Monitor"
    echo   4. Right-click to Start/Stop/Restart
    echo.
    echo From Command Line:
    echo   Start:  sc start NetworkPingMonitor
    echo   Stop:   sc stop NetworkPingMonitor
    echo   Status: sc query NetworkPingMonitor
    echo.
) else (
    echo ❌ Failed to install service!
    echo.
    echo Possible issues:
    echo 1. Not running as Administrator
    echo 2. Service name already exists
    echo 3. Path contains invalid characters
    echo 4. Insufficient permissions
    echo.
    echo Current path: %EXE_PATH%
    echo.
)

echo.
pause