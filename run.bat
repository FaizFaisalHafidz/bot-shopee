@echo off
title Shopee Live Bot Launcher

echo.
echo ========================================
echo   SHOPEE LIVE BOT LAUNCHER
echo ========================================
echo.

echo 🚀 Starting Shopee Live Bot...
echo 📋 Checking requirements...

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python first.
    pause
    exit /b 1
)

REM Check if requirements.txt exists
if not exist "requirements.txt" (
    echo ❌ requirements.txt not found!
    pause
    exit /b 1
)

REM Check if input.csv exists
if not exist "input.csv" (
    echo ❌ input.csv not found! Please create input.csv with account cookies.
    pause
    exit /b 1
)

REM Install requirements
echo 📦 Installing dependencies...
pip install -r requirements.txt

REM Check if main.py exists
if not exist "main.py" (
    echo ❌ main.py not found!
    pause
    exit /b 1
)

echo ✅ All requirements satisfied!
echo 🎯 Launching Shopee Live Bot...
echo.

REM Run the bot
python main.py

echo.
echo 👋 Bot telah selesai. Press any key to exit...
pause >nul
