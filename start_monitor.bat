@echo off
echo ========================================
echo Starting Network Ping Monitor
echo ========================================
echo.
echo Monitoring devices:
echo - 192.168.200.102 (200 Switch)
echo - 192.168.1.8 (Main Server)  
echo - 192.168.200.4 (Building 121)
echo - 192.168.200.5 (Building 200)
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Starting monitoring (Press Ctrl+C to stop)...
echo.
python ping_monitor.py
pause