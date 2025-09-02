@echo off
title SHOPEE ULTIMATE REAL URL BOT - EXACT URL STRUCTURE BYPASS
color 0a

echo.
echo ===============================================================================
echo    SHOPEE ULTIMATE REAL URL BOT - EXACT URL STRUCTURE BYPASS
echo    Complete Authentication Bypass + Ultimate Viewer Booster
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
echo Starting Ultimate Real URL Bot...
echo Session ID: %SESSION_ID%
echo Viewer Count: %VIEWER_COUNT%
echo URL Structure: EXACT Shopee Live format
echo.

python real_url_bot.py %SESSION_ID% %VIEWER_COUNT%

echo.
echo Bot stopped. Press any key to exit.
pause >nul
