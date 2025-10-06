@echo off
echo ========================================
echo Network Ping Monitor Setup
echo ========================================
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Virtual environment activated!
echo Python location: %VIRTUAL_ENV%
echo.
echo Available commands:
echo   python ping_monitor.py         - Start real monitoring
echo   python test_email.py           - Test email functionality  
echo   python ping_monitor_test.py    - Run test with fake IP
echo.
echo Current directory: %CD%
echo ========================================

cmd /k