@echo off
title Shopee Live Viewer Bot - Existing Profiles + Device ID Bypass

echo ========================================
echo  SHOPEE LIVE VIEWER BOT - FINAL VERSION
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python first: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Activate virtual environment
if exist "venv" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo Installing required packages...
    pip install selenium webdriver-manager requests
)

REM Check if we can find Chrome profiles
echo Scanning for existing Chrome profiles...
python -c "
import os
profiles_found = False
chrome_paths = [
    os.path.expandvars(r'%LOCALAPPDATA%\Google\Chrome\User Data'),
    'sessions/google_profiles/'
]
for path in chrome_paths:
    if os.path.exists(path):
        items = [item for item in os.listdir(path) 
                if os.path.isdir(os.path.join(path, item)) 
                and ('Default' in item or 'Profile' in item or 'profile' in item.lower())]
        if items:
            print(f'Found {len(items)} Chrome profiles in {path}')
            profiles_found = True
if not profiles_found:
    print('No Chrome profiles found!')
    print('Please login to different Google accounts in Chrome first.')
"

echo.
echo Starting Shopee Live Viewer Bot...
echo.
echo Instructions:
echo 1. Make sure you have Google accounts logged in Chrome profiles
echo 2. Enter Shopee Live session ID when prompted
echo 3. Bot will use existing profiles with unique device fingerprints
echo 4. Check live stream - viewer count should increase!
echo.

REM Run the final bot
python final_shopee_bot.py

echo.
echo Bot finished! Press any key to exit.
pause >nul
