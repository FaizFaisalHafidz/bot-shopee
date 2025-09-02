@echo off
title SHOPEE ULTRA RDP BOT - MAXIMUM OPTIMIZATION
color 0a

echo.
echo ===============================================================================
echo    SHOPEE ULTRA RDP BOT - MAXIMUM OPTIMIZATION
echo    Ultra-aggressive login bypass + GPU disabled + Emergency bypasses
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
echo Starting ULTRA RDP Bot with maximum optimization...
echo Session ID: %SESSION_ID%
echo Viewer Count: %VIEWER_COUNT%
echo Mode: Ultra RDP Headless (GPU Disabled)
echo Bypass: Ultra-aggressive + Emergency methods
echo Expected Mega Boost: %VIEWER_COUNT% x 500 = %VIEWER_COUNT%500
echo.

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo [SETUP] Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo [WARNING] Virtual environment not found. Using system Python...
)

python real_url_bot_ultra.py %SESSION_ID% %VIEWER_COUNT%

echo.
echo Ultra bot stopped. Press any key to exit.
pause >nul
