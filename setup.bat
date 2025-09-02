@echo off
title SHOPEE BOT - ENVIRONMENT SETUP
color 0a

echo.
echo ===============================================================================
echo    SHOPEE BOT - ENVIRONMENT SETUP FOR WINDOWS
echo    Recreating virtual environment and installing dependencies
echo ===============================================================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python 3.7+ first:
    echo Download from: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo Python found.
python --version

REM Create virtual environment
echo.
echo [SETUP] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)
echo Virtual environment created.

REM Activate virtual environment
echo.
echo [SETUP] Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo.
echo [SETUP] Upgrading pip...
python -m pip install --upgrade pip

REM Install Python dependencies
echo.
echo [SETUP] Installing Python dependencies...
pip install selenium webdriver-manager requests
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo Python dependencies installed.

REM Install Node.js dependencies (optional)
if exist package.json (
    echo.
    echo [SETUP] Installing Node.js dependencies...
    where npm >nul 2>&1
    if not errorlevel 1 (
        npm install
        echo Node.js dependencies installed.
    ) else (
        echo npm not found, skipping Node.js dependencies
        echo Install Node.js if you need Chrome extension features
    )
)

REM Create necessary directories
echo.
echo [SETUP] Creating necessary directories...
if not exist "sessions\real_url_viewers" mkdir sessions\real_url_viewers
if not exist "sessions\device_profiles" mkdir sessions\device_profiles  
if not exist "sessions\chrome_profiles" mkdir sessions\chrome_profiles
if not exist "logs" mkdir logs
if not exist "accounts" mkdir accounts
echo Directories created.

REM Verify installation
echo.
echo [VERIFY] Verifying installation...
python -c "import selenium, webdriver_manager, requests; print('All Python dependencies OK')" 2>nul
if errorlevel 1 (
    echo ERROR: Dependency verification failed
    pause
    exit /b 1
)

echo.
echo ===============================================================================
echo    SETUP COMPLETED SUCCESSFULLY
echo ===============================================================================
echo Environment ready for Shopee bot deployment!
echo.
echo Available launchers:
echo   ultimate_launcher.bat - Complete launcher with all options
echo   python real_url_bot.py ^<session_id^> ^<viewer_count^> - Direct execution
echo.
echo Example usage:
echo   ultimate_launcher.bat
echo   python real_url_bot.py 157658364 3
echo.
echo ===============================================================================
echo.
echo Press any key to continue...
pause >nul
