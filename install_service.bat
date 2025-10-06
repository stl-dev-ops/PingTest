@echo off
echo ========================================
echo Install Network Ping Monitor as Service
echo ========================================
echo.
echo This script will install NetworkPingMonitor.exe as a Windows Service
echo using NSSM (Non-Sucking Service Manager)
echo.

REM Check if NSSM exists
if not exist "nssm.exe" (
    echo ❌ NSSM not found!
    echo.
    echo Please download NSSM from: https://nssm.cc/download
    echo 1. Download nssm-2.24.zip
    echo 2. Extract nssm.exe to this folder
    echo 3. Run this script again
    echo.
    pause
    exit /b 1
)

REM Get current directory
set "CURRENT_DIR=%cd%"
set "EXE_PATH=%CURRENT_DIR%\dist\NetworkPingMonitor.exe"

echo Installing service...
nssm install "NetworkPingMonitor" "%EXE_PATH%"

echo Configuring service...
nssm set "NetworkPingMonitor" Description "Network Ping Monitor - Monitors network devices and sends email alerts"
nssm set "NetworkPingMonitor" Start SERVICE_AUTO_START
nssm set "NetworkPingMonitor" AppDirectory "%CURRENT_DIR%"
nssm set "NetworkPingMonitor" AppStdout "%CURRENT_DIR%\logs\service_output.log"
nssm set "NetworkPingMonitor" AppStderr "%CURRENT_DIR%\logs\service_errors.log"
nssm set "NetworkPingMonitor" AppRotateFiles 1
nssm set "NetworkPingMonitor" AppRotateOnline 1
nssm set "NetworkPingMonitor" AppRotateBytes 1048576

echo Starting service...
nssm start "NetworkPingMonitor"

echo.
echo ✅ Service installed and started!
echo.
echo Service Name: NetworkPingMonitor
echo Status: Run "sc query NetworkPingMonitor" to check status
echo Logs: Check logs\service_output.log for output
echo.
echo To manage the service:
echo   Start:   nssm start NetworkPingMonitor
echo   Stop:    nssm stop NetworkPingMonitor
echo   Remove:  nssm remove NetworkPingMonitor confirm
echo.
pause