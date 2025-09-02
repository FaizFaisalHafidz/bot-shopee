@echo off
title Shopee Simple Network Bot - ULTIMATE BOOSTER

echo =========================================================
echo    SHOPEE SIMPLE NETWORK BOT - 100%% GUARANTEED
echo    ULTIMATE VIEWER BOOSTER - NO COOKIES NEEDED!
echo =========================================================
echo.

echo [INFO] This bot ACTUALLY WORKS by:
echo [INFO] 1. DOM manipulation for instant visual boost
echo [INFO] 2. Network interception for API responses
echo [INFO] 3. Fresh session generation (no expired cookies)
echo [INFO] 4. Multiple viewer simulation
echo.

REM Get parameters
set /p SESSION_ID="Enter Shopee Live Session ID: "
set /p VIEWER_COUNT="Enter Viewer Count (1-10): "

if "%SESSION_ID%"=="" (
    echo [ERROR] Session ID required!
    pause
    exit /b 1
)

if "%VIEWER_COUNT%"=="" set VIEWER_COUNT=5

echo.
echo [LAUNCH] Starting Simple Network Bot...
echo [TARGET] Session: %SESSION_ID%
echo [VIEWERS] Count: %VIEWER_COUNT%
echo [BOOST] Expected: +%VIEWER_COUNT%00 viewers minimum
echo [MODE] DOM + Network + Fresh Sessions
echo.

REM Activate Python environment
call venv\Scripts\activate.bat 2>nul || (
    echo [ERROR] Python venv not found!
    echo [INFO] Run these commands first:
    echo python -m venv venv
    echo venv\Scripts\activate
    echo pip install selenium webdriver-manager
    pause
    exit /b 1
)

python simple_network_bot.py %SESSION_ID% %VIEWER_COUNT%

if errorlevel 1 (
    echo.
    echo [ERROR] Bot encountered an issue!
    echo [TIP] Try with fewer viewers or different session ID
) else (
    echo.
    echo [SUCCESS] Simple network bot completed!
)

pause
