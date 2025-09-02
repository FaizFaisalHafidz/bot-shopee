@echo off
title Bot Live Shopee
color 0A

cls
echo.
echo BOT LIVE SHOPEE
echo.
set /p session_id="Session ID: "
set /p viewer_count="Jumlah viewer (default 10): "

if "%viewer_count%"=="" set viewer_count=10

echo.
echo Memulai bot...
cd /d "%~dp0"
python bot-core\bots\ultimate_shopee_bot.py %session_id% %viewer_count%
pause

:MENU
set /p choice="Select option (0-8): "

if "%choice%"=="1" goto ULTIMATE_BOT
if "%choice%"=="2" goto QUICK_START
if "%choice%"=="3" goto QUICK_TEST
if "%choice%"=="4" goto RDP_CHECK
if "%choice%"=="5" goto ADVANCED
if "%choice%"=="6" goto SETUP
if "%choice%"=="7" goto LOGS
if "%choice%"=="8" goto CLEAN
if "%choice%"=="0" goto EXIT
echo Invalid choice. Please try again.
goto MENU

:ULTIMATE_BOT
cls
echo.
echo ==============================================================================
echo                    ULTIMATE BOT - COOKIE HARVESTING + LIVE VIEWERS
echo ==============================================================================
echo.
echo This bot will:
echo - Harvest fresh cookies automatically
echo - Create multiple live viewers with valid cookies
echo - Auto-rotate cookies when they expire
echo - Monitor and maintain viewer count
echo.
set /p session_id="Enter Shopee Live Session ID: "
set /p viewer_count="Enter number of viewers (default 10): "
set /p harvest_first="Harvest fresh cookies first? (y/N): "

if "%viewer_count%"=="" set viewer_count=10
if /i "%harvest_first%"=="y" (
    set harvest_param=true
) else (
    set harvest_param=false
)

echo.
echo Starting Ultimate Bot with:
echo - Session ID: %session_id%
echo - Target Viewers: %viewer_count%
echo - Fresh Cookie Harvest: %harvest_param%
echo - Auto Cookie Rotation: Enabled
echo - Anti-Detection: Maximum
echo.
echo This may take 5-10 minutes for initial cookie harvesting...
echo Press Enter to continue or Ctrl+C to cancel...
pause >nul

echo Starting Ultimate Shopee Bot...
cd /d "%~dp0"
python bot-core\bots\ultimate_shopee_bot.py %session_id% %viewer_count% %harvest_param%
pause
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

:QUICK_TEST
cls
echo.
echo ==============================================================================
echo                         QUICK TEST - SINGLE VIEWER
echo ==============================================================================
echo.
set /p session_id="Enter Shopee Live Session ID: "
echo.
echo Starting Quick Test with:
echo - Session ID: %session_id%
echo - Viewers: 1 (test mode)
echo - Mode: RDP Ultra-Optimized
echo.
echo Press Enter to continue or Ctrl+C to cancel...
pause >nul

echo Starting quick test...
cd /d "%~dp0"
python bot-core\scripts\quick_test.py %session_id% 1
pause
goto MENU

:RDP_CHECK
cls
echo.
echo ==============================================================================
echo                         RDP ENVIRONMENT CHECK
echo ==============================================================================
echo.
echo Checking RDP environment and dependencies...
echo.
cd /d "%~dp0"
python bot-core\scripts\check_rdp.py
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
pip install -r bot-core\requirements.txt
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
