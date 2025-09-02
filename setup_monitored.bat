@echo off
chcp 65001
cls

echo ===============================================================================
echo    SHOPEE BOT - QUICK SETUP FOR MONITORED BOT
echo    Installing required dependencies for client-grade solution
echo ===============================================================================

echo [SETUP] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.8+ first.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python found!

echo [SETUP] Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo ✅ Virtual environment created!
) else (
    echo ✅ Virtual environment exists!
)

echo [SETUP] Activating virtual environment...
call venv\Scripts\activate

echo [SETUP] Upgrading pip...
python -m pip install --upgrade pip

echo [SETUP] Installing required packages...
echo Installing: selenium webdriver-manager requests
pip install selenium webdriver-manager requests

echo [SETUP] Creating necessary directories...
if not exist "sessions\monitored_profiles" mkdir sessions\monitored_profiles
if not exist "logs" mkdir logs

echo [SETUP] Testing dependencies...
python -c "import selenium, webdriver_manager, requests; print('✅ All dependencies OK!')" 2>nul
if errorlevel 1 (
    echo ❌ Dependency test failed!
    echo Retrying installation...
    pip install --force-reinstall selenium webdriver-manager requests
)

echo.
echo ===============================================================================
echo    SETUP COMPLETE! 
echo ===============================================================================
echo.
echo ✅ Python environment ready
echo ✅ All dependencies installed  
echo ✅ Directories created
echo ✅ Ready for client-grade monitoring
echo.
echo You can now run:
echo   • monitored_launcher.bat (for real-time monitoring)
echo   • ultimate_launcher.bat (for all options)
echo.
echo Press any key to continue...
pause >nul
