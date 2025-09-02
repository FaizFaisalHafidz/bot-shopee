@echo off
title Shopee Live Bot - RDP Optimized
color 0A
mode con: cols=80 lines=30

echo.
echo ==============================================================================
echo                      SHOPEE LIVE BOT - RDP OPTIMIZED
echo                     Organized Structure - Single Entry Point
echo ==============================================================================
echo.
echo Bot organized in: bot-core\
echo Available options:
echo.
echo   [1] Quick Start - Real URL Bot (RDP Optimized)
echo   [2] Advanced Bot Options  
echo   [3] Setup Python Environment
echo   [4] View Logs
echo   [5] Clean Sessions
echo   [0] Exit
echo.
echo ==============================================================================
echo.

:MENU
set /p choice="Select option (0-5): "

if "%choice%"=="1" goto QUICK_START
if "%choice%"=="2" goto ADVANCED
if "%choice%"=="3" goto SETUP
if "%choice%"=="4" goto LOGS
if "%choice%"=="5" goto CLEAN
if "%choice%"=="0" goto EXIT
echo Invalid choice. Please try again.
goto MENU

:QUICK_START
cls
echo.
echo ==============================================================================
echo                           QUICK START - REAL URL BOT
echo ==============================================================================
echo.
set /p session_id="Enter Shopee Live Session ID: "
set /p viewer_count="Enter number of viewers (default 3): "

if "%viewer_count%"=="" set viewer_count=3

echo.
echo Starting Real URL Bot with:
echo - Session ID: %session_id%
echo - Viewers: %viewer_count%
echo - Mode: RDP Optimized
echo.
echo Press Enter to continue or Ctrl+C to cancel...
pause >nul

echo Starting bot...
cd /d "%~dp0"
python bot-core\bots\real_url_bot_rdp.py %session_id% %viewer_count%
pause
goto MENU

:ADVANCED
cls
echo.
echo ==============================================================================
echo                             ADVANCED OPTIONS
echo ==============================================================================
echo.
echo   [1] API Bot
echo   [2] Network Interceptor Bot
echo   [3] Simple Network Bot
echo   [4] View Available Bots
echo   [0] Back to Main Menu
echo.
set /p adv_choice="Select advanced option: "

if "%adv_choice%"=="1" goto API_BOT
if "%adv_choice%"=="2" goto NETWORK_BOT
if "%adv_choice%"=="3" goto SIMPLE_BOT
if "%adv_choice%"=="4" goto LIST_BOTS
if "%adv_choice%"=="0" goto MENU
echo Invalid choice.
goto ADVANCED

:API_BOT
set /p session_id="Enter Session ID: "
echo Starting API Bot...
cd /d "%~dp0"
python bot-core\bots\shopee_api_bot.py %session_id%
pause
goto ADVANCED

:NETWORK_BOT
set /p session_id="Enter Session ID: "
echo Starting Network Interceptor Bot...
cd /d "%~dp0"
python bot-core\bots\network_interceptor_bot.py %session_id%
pause
goto ADVANCED

:SIMPLE_BOT
set /p session_id="Enter Session ID: "
echo Starting Simple Network Bot...
cd /d "%~dp0"
python bot-core\bots\simple_network_bot.py %session_id%
pause
goto ADVANCED

:LIST_BOTS
cls
echo.
echo Available bots in bot-core\bots\:
echo.
dir /b bot-core\bots\*.py
echo.
pause
goto ADVANCED

:SETUP
cls
echo.
echo ==============================================================================
echo                           PYTHON SETUP
echo ==============================================================================
echo.
echo Setting up Python environment...
echo.
echo Checking Python installation...
python --version
echo.
echo Installing required packages...
pip install -r requirements.txt
echo.
echo Setup complete!
pause
goto MENU

:LOGS
cls
echo.
echo ==============================================================================
echo                              VIEW LOGS
echo ==============================================================================
echo.
echo Available logs:
dir /b bot-core\logs\*.log
echo.
set /p log_name="Enter log file name (or press Enter to view latest): "
if "%log_name%"=="" (
    echo Showing latest log entries...
    for %%i in (bot-core\logs\*.log) do (
        echo.
        echo === %%i ===
        tail -n 20 "%%i" 2>nul || echo Log file empty or not found
    )
) else (
    type "bot-core\logs\%log_name%" 2>nul || echo Log file not found
)
echo.
pause
goto MENU

:CLEAN
cls
echo.
echo ==============================================================================
echo                            CLEAN SESSIONS
echo ==============================================================================
echo.
echo This will remove all browser sessions and profiles.
echo.
set /p confirm="Are you sure? (y/N): "
if /i "%confirm%"=="y" (
    echo Cleaning sessions...
    rmdir /s /q "bot-core\sessions" 2>nul
    mkdir "bot-core\sessions"
    echo Sessions cleaned!
) else (
    echo Cancelled.
)
pause
goto MENU

:EXIT
cls
echo.
echo Thank you for using Shopee Live Bot!
echo.
timeout 2 >nul
exit
