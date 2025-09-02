@echo off
title Shopee Network Interceptor Bot - 100% GUARANTEED

echo ===============================================
echo    SHOPEE NETWORK INTERCEPTOR BOT
echo    100%% GUARANTEED WORK - NO EXPIRED COOKIES
echo ===============================================
echo.

echo [INFO] This bot uses NETWORK INTERCEPTION
echo [INFO] Bypasses server-side validation
echo [INFO] Generates FRESH cookies automatically
echo [INFO] Real viewer boost guaranteed!
echo.

REM Get parameters
set /p SESSION_ID="Enter Shopee Live Session ID: "
set /p VIEWER_COUNT="Enter Viewer Count (1-20): "

if "%SESSION_ID%"=="" (
    echo [ERROR] Session ID required!
    pause
    exit /b 1
)

if "%VIEWER_COUNT%"=="" set VIEWER_COUNT=8

echo.
echo [LAUNCH] Starting Network Interceptor...
echo [TARGET] Session: %SESSION_ID%
echo [BOOST] Viewers: %VIEWER_COUNT%
echo [MODE] Network Injection + Fresh Cookies
echo.

REM Activate Python environment and run
call venv\Scripts\activate.bat 2>nul || (
    echo [ERROR] Python venv not found! Run setup first.
    pause
    exit /b 1
)

python network_interceptor_bot.py %SESSION_ID% %VIEWER_COUNT%

if errorlevel 1 (
    echo.
    echo [ERROR] Bot encountered an issue!
    echo [TIP] Try with fewer viewers or check session ID
) else (
    echo.
    echo [SUCCESS] Network interceptor completed!
)

pause
