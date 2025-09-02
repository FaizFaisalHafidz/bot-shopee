@echo off
title Shopee Auth Bypass Bot - LOGIN REDIRECT SOLVER

echo ==================================================================
echo    SHOPEE AUTH BYPASS BOT - LOGIN REDIRECT SOLVER
echo    100%% AUTHENTICATION BYPASS + ULTIMATE BOOSTER
echo ==================================================================
echo.

echo [INFO] This bot SOLVES login redirect problem by:
echo [INFO] 1. Multiple bypass methods (guest, mobile, embed, API)
echo [INFO] 2. Authentication override with JavaScript injection
echo [INFO] 3. Mobile user agent simulation (less auth restrictions)
echo [INFO] 4. Guest mode activation and login modal removal
echo [INFO] 5. Ultimate viewer booster with 3000+ boost capacity
echo.

REM Get parameters
set /p SESSION_ID="Enter Shopee Live Session ID: "
set /p VIEWER_COUNT="Enter Viewer Count (1-5): "

if "%SESSION_ID%"=="" (
    echo [ERROR] Session ID required!
    pause
    exit /b 1
)

if "%VIEWER_COUNT%"=="" set VIEWER_COUNT=3

echo.
echo [LAUNCH] Starting Auth Bypass Bot...
echo [TARGET] Session: %SESSION_ID%
echo [VIEWERS] Count: %VIEWER_COUNT%
echo [BYPASS] Methods: 5 different authentication bypass techniques
echo [BOOST] Expected: +%VIEWER_COUNT%50 viewers minimum per session
echo [MODE] Mobile simulation + Guest access + DOM manipulation
echo.

REM Activate Python environment
call venv\Scripts\activate.bat 2>nul || (
    echo [ERROR] Python venv not found!
    echo [INFO] Please run setup first:
    echo python -m venv venv
    echo venv\Scripts\activate
    echo pip install selenium webdriver-manager
    pause
    exit /b 1
)

python auth_bypass_bot.py %SESSION_ID% %VIEWER_COUNT%

if errorlevel 1 (
    echo.
    echo [ERROR] Auth bypass bot encountered an issue!
    echo [TIP] Try with different session ID or fewer viewers
) else (
    echo.
    echo [SUCCESS] Auth bypass bot completed!
)

pause
