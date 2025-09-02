@echo off
title Shopee Live Viewer Bot (Auto Mode)

echo ==========================================
echo    SHOPEE LIVE BOT - AUTO SESSION COOKIES  
echo ==========================================
echo.

REM Auto configuration (like the old bot)
set SESSION_ID=157658364
set VIEWER_COUNT=10
set AUTO_MODE=1

echo [AUTO] Session ID: %SESSION_ID%
echo [AUTO] Viewer Count: %VIEWER_COUNT%
echo [AUTO] Cookie Mode: ENABLED
echo [AUTO] Starting in 3 seconds...
echo.

timeout /t 3 /nobreak >nul

REM Install dependencies if needed
if not exist "node_modules\puppeteer" (
    echo [SETUP] Installing Puppeteer...
    npm install puppeteer >nul 2>&1
)

echo [LAUNCH] Starting viewers with session cookies...
node generatex_4c.js %SESSION_ID% %VIEWER_COUNT%

if errorlevel 1 (
    echo [ERROR] Bot encountered an error!
    pause
) else (
    echo [SUCCESS] Bot completed successfully!
)

pause
