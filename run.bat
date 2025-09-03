@echo off
title NEO - Stealth Shopee Bot
color 0A

cls
echo.
echo ==============================================================================
echo                        NEO - STEALTH SHOPEE BOT
echo                       Anti-Detection Technology
echo ==============================================================================
echo.
echo Pilih Bot Mode:
echo [1] STEALTH BOT (Recommended - Anti Detection)
echo [2] ULTIMATE BOT (Standard)
echo [3] QUICK FIX BOT (Emergency Test)
echo.
set /p bot_mode="Pilih mode (1/2/3): "

echo.
set /p session_id="Session ID: "

if "%bot_mode%"=="3" (
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
    if "%bot_mode%"=="1" (
        echo 🥷 Menjalankan STEALTH BOT...
        echo Target: %viewer_count% stealth viewers
        echo Session: %session_id%
        cd /d "%~dp0"
        call venv\Scripts\activate
        python bot-core\bots\stealth_shopee_bot.py %session_id% %viewer_count%
    ) else (
        echo 🚀 Menjalankan ULTIMATE BOT...
        echo Target: %viewer_count% viewers  
        echo Session: %session_id%
        cd /d "%~dp0"
        call venv\Scripts\activate
        python bot-core\bots\ultimate_shopee_bot.py %session_id% %viewer_count%
    )
)

echo.
echo Bot selesai. Press any key to exit...
pause
