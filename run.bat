@echo off
title NEO - Ultimate Anti-Bot Arsenal
color 0A

cls
echo.
echo ==============================================================================
echo                     NEO - ULTIMATE ANTI-BOT ARSENAL
echo                    Advanced Captcha Bypass Technology
echo ==============================================================================
echo.
echo Pilih Anti-Bot Strategy:
echo [1] SUPER STEALTH BOT (Ultimate Bypass - RECOMMENDED)
echo [2] NETWORK INTERCEPTOR BOT (API Focused)
echo [3] STEALTH BOT (Advanced Anti-Detection)
echo [4] QUICK FIX BOT (Emergency Test)
echo [5] ULTIMATE BOT (Standard)
echo.
set /p bot_mode="Pilih strategy (1-5): "

echo.
set /p session_id="Session ID: "

if "%bot_mode%"=="1" (
    set /p viewer_count="Jumlah super stealth viewer (max 3): "
    if "%viewer_count%"=="" set viewer_count=3
    echo.
    echo 🦾 Menjalankan SUPER STEALTH BOT...
    echo Target: %viewer_count% ultimate bypass viewers
    echo Session: %session_id%
    echo ⚠️ WARNING: Using ultimate bypass techniques against anti-bot
    cd /d "%~dp0"
    call venv\Scripts\activate
    python bot-core\bots\super_stealth_bot.py %session_id% %viewer_count%
    
) else if "%bot_mode%"=="2" (
    set /p viewer_count="Jumlah network viewer (max 3): "
    if "%viewer_count%"=="" set viewer_count=3
    echo.
    echo 🌐 Menjalankan NETWORK INTERCEPTOR BOT...
    echo Target: %viewer_count% API-focused viewers
    echo Session: %session_id%
    echo 📡 INFO: Network manipulation and API bypass mode
    cd /d "%~dp0"
    call venv\Scripts\activate
    python bot-core\bots\network_interceptor_bot.py %session_id% %viewer_count%
    
) else if "%bot_mode%"=="3" (
    set /p viewer_count="Jumlah stealth viewer (max 3): "
    if "%viewer_count%"=="" set viewer_count=3
    echo.
    echo 🥷 Menjalankan STEALTH BOT...
    echo Target: %viewer_count% stealth viewers
    echo Session: %session_id%
    cd /d "%~dp0"
    call venv\Scripts\activate
    python bot-core\bots\stealth_shopee_bot.py %session_id% %viewer_count%
    
) else if "%bot_mode%"=="4" (
    set /p test_type="Test type [1=API, 2=Browser, 3=Both]: "
    echo.
    echo 🚀 Menjalankan QUICK FIX BOT...
    echo Target: Emergency test mode
    echo Session: %session_id%
    cd /d "%~dp0"
    call venv\Scripts\activate
    python bot-core\bots\quick_fix_bot.py %session_id% %test_type%
    
) else (
    set /p viewer_count="Jumlah viewer (max 3): "
    if "%viewer_count%"=="" set viewer_count=3
    echo.
    echo 🚀 Menjalankan ULTIMATE BOT...
    echo Target: %viewer_count% viewers  
    echo Session: %session_id%
    cd /d "%~dp0"
    call venv\Scripts\activate
    python bot-core\bots\ultimate_shopee_bot.py %session_id% %viewer_count%
)

echo.
echo Bot selesai. Press any key to exit...
pause
