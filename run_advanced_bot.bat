@echo off
REM Run Advanced Shopee Bot
REM Quick launcher with error handling

title Advanced Shopee Bot - Launcher

echo 🚀 ADVANCED SHOPEE BOT LAUNCHER
echo ===============================
echo.

REM Check if advanced bot exists
if not exist "advanced_bot\advanced_bot.py" (
    echo ❌ Advanced bot not found!
    echo 💡 Run setup_advanced_bot.bat first
    pause
    exit /b 1
)

REM Check if input.csv exists
if not exist "input.csv" (
    echo ❌ input.csv not found!
    echo 💡 Add your account cookies to input.csv first
    pause
    exit /b 1
)

echo ✅ Files found, launching advanced bot...
echo.

REM Change to advanced_bot directory and run
cd advanced_bot
python advanced_bot.py

REM Return to original directory
cd ..

echo.
echo Bot execution completed.
pause
