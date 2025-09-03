@echo off
title NEO - Bot Views Shopee
color 0A

cls
echo.
echo ==============================================================================
echo                           NEO - BOT VIEWS SHOPEE
echo ==============================================================================
echo.
set /p session_id="Session ID: "
set /p viewer_count="Jumlah viewer (default 10): "

if "%viewer_count%"=="" set viewer_count=10

echo.
echo Memulai bot...
cd /d "%~dp0"
echo Mengaktifkan Python environment...
call venv\Scripts\activate
echo Menjalankan: python bot-core\bots\ultimate_shopee_bot.py %session_id% %viewer_count%
python bot-core\bots\ultimate_shopee_bot.py %session_id% %viewer_count%
echo.
echo Bot selesai atau error terjadi.
pause
