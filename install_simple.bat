@echo off
echo Simple Service Installation
echo ==========================
echo.

set "EXE_PATH=%cd%\dist\NetworkPingMonitor.exe"

echo Creating service...
sc create NetworkPingMonitor binPath= "\"%EXE_PATH%\"" DisplayName= "Network Ping Monitor" start= auto

echo Setting description...
sc description NetworkPingMonitor "Monitors network devices and sends email alerts"

echo Starting service...
sc start NetworkPingMonitor

echo.
echo Done! Check Services console (services.msc) for "Network Ping Monitor"
pause