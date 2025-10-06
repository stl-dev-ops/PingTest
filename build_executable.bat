@echo off
echo ========================================
echo Building Standalone Ping Monitor
echo ========================================
echo.

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Installing PyInstaller...
pip install -r build_requirements.txt

echo.
echo Building standalone executable...
pyinstaller --onefile --name "NetworkPingMonitor" --icon=NONE --console ping_monitor_standalone.py

echo.
echo ========================================
echo Build Complete!
echo ========================================
echo.
echo Executable created at: dist\NetworkPingMonitor.exe
echo.
echo To deploy to server:
echo 1. Copy dist\NetworkPingMonitor.exe to your server
echo 2. Run: NetworkPingMonitor.exe
echo.
echo The executable is completely self-contained with:
echo - All Python dependencies embedded
echo - Configuration hardcoded for security
echo - Email credentials included (safe behind firewall)
echo - No external dependencies required
echo.
pause