@echo off
title SHOPEE REAL URL BOT - RDP OPTIMIZED
color 0a

echo.
echo ===============================================================================
echo    SHOPEE REAL URL BOT - RDP OPTIMIZED VERSION
echo    Fixed untuk Windows RDP dengan proper Chrome options
echo ===============================================================================
echo.

set /p SESSION_ID="Enter Shopee Live Session ID (e.g., 157658364): "
if "%SESSION_ID%"=="" (
    echo ERROR: Session ID required!
    pause
    exit /b 1
)

set /p VIEWER_COUNT="Enter viewer count (default 3): "
if "%VIEWER_COUNT%"=="" set VIEWER_COUNT=3

echo.
echo Starting RDP-Optimized Real URL Bot...
echo Session ID: %SESSION_ID%
echo Viewer Count: %VIEWER_COUNT%
echo Mode: RDP Headless Optimized
echo Browser: Chrome Headless (RDP Safe)
echo.

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo [SETUP] Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo [WARNING] Virtual environment not found. Using system Python...
)

python real_url_bot_rdp.py %SESSION_ID% %VIEWER_COUNT%

echo.
echo Bot stopped. Press any key to exit.
pause >nul
