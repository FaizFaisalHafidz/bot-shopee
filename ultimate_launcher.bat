@echo off
title SHOPEE ULTIMATE REAL URL BOT - FINAL DEPLOYMENT
color 0a

echo.
echo ===============================================================================
echo    SHOPEE ULTIMATE REAL URL BOT - FINAL DEPLOYMENT FOR RDP
echo    Complete Authentication Bypass + Real URL Structure + Device Diversity
echo ===============================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found! Please install Python 3.7+ first.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo [SETUP] Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install selenium webdriver-manager requests
) else (
    echo [SETUP] Activating existing virtual environment...
    call venv\Scripts\activate.bat
)

REM Verify dependencies
echo [CHECK] Verifying dependencies...
python -c "import selenium, webdriver_manager; print('Dependencies OK')" 2>nul
if errorlevel 1 (
    echo [INSTALL] Installing missing dependencies...
    pip install selenium webdriver-manager requests
)

REM Create necessary directories
if not exist "sessions\real_url_viewers" mkdir sessions\real_url_viewers
if not exist "logs" mkdir logs

echo.
echo Available launch options:
echo 1. Real URL Bot [RECOMMENDED] - Exact Shopee Live URL structure
echo 2. Device Fingerprint Bot - Advanced device spoofing  
echo 3. Auth Bypass Bot - Authentication bypass only
echo 4. Quick Launch - Default settings
echo.

set /p choice="Select option (1-4): "

if "%choice%"=="1" goto real_url_bot
if "%choice%"=="2" goto device_bot
if "%choice%"=="3" goto auth_bot
if "%choice%"=="4" goto quick_launch
goto real_url_bot

:real_url_bot
echo [LAUNCH] Real URL Bot - Exact Shopee Live URL structure
echo.
set /p session_id="Enter Shopee Live Session ID: "
if "%session_id%"=="" (
    echo ERROR: Session ID required!
    pause
    exit /b 1
)

set /p viewer_count="Enter viewer count (default 3): "
if "%viewer_count%"=="" set viewer_count=3

echo.
echo Starting Real URL Bot with exact Shopee Live structure...
echo Session ID: %session_id%
echo Viewer Count: %viewer_count%
echo URL Structure: EXACT Shopee Live format
echo Expected Boost: %viewer_count% x 300 = %viewer_count%00
echo.

python real_url_bot.py %session_id% %viewer_count%
goto end

:device_bot
echo [LAUNCH] Device Fingerprint Bot - Advanced device spoofing
echo.
set /p session_id="Enter Shopee Live Session ID: "
if "%session_id%"=="" (
    echo ERROR: Session ID required!
    pause
    exit /b 1
)

set /p device_count="Enter device count (default 3): "
if "%device_count%"=="" set device_count=3

echo.
echo Starting Device Fingerprint Bot...
echo Session ID: %session_id%
echo Device Count: %device_count%
echo.

python device_fingerprint_bot.py %session_id% %device_count%
goto end

:auth_bot
echo [LAUNCH] Auth Bypass Bot - Authentication bypass only
echo.
set /p session_id="Enter Shopee Live Session ID: "
if "%session_id%"=="" (
    echo ERROR: Session ID required!
    pause
    exit /b 1
)

set /p viewer_count="Enter viewer count (default 3): "
if "%viewer_count%"=="" set viewer_count=3

echo.
echo Starting Auth Bypass Bot...
echo Session ID: %session_id%
echo Viewer Count: %viewer_count%
echo.

python auth_bypass_bot.py %session_id% %viewer_count%
goto end

:quick_launch
echo [QUICK] Quick Launch with default settings
echo.
set /p session_id="Enter Shopee Live Session ID: "
if "%session_id%"=="" (
    echo ERROR: Session ID required!
    pause
    exit /b 1
)

echo.
echo Quick launching Real URL Bot with 3 viewers...
echo Session ID: %session_id%
echo.

python real_url_bot.py %session_id% 3
goto end

:end
echo.
echo ===============================================================================
echo Bot execution completed.
echo Check logs\ directory for detailed execution logs.
echo.
echo Press any key to exit or run again...
pause >nul

REM Ask if user wants to run again
echo.
set /p again="Run bot again? (y/n): "
if /i "%again%"=="y" goto main
if /i "%again%"=="yes" goto main

exit
