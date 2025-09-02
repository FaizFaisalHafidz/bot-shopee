@echo off
title Auto Python Installer for Shopee Bot

echo ========================================
echo  AUTO PYTHON INSTALLER - SHOPEE BOT
echo ========================================
echo.

REM Check if Python is already installed
python --version >nul 2>&1
if not errorlevel 1 (
    echo Python is already installed!
    python --version
    echo.
    goto :run_bot
)

echo Python not found. Installing Python automatically...
echo.

REM Check if we have winget (Windows Package Manager)
winget --version >nul 2>&1
if not errorlevel 1 (
    echo Using Windows Package Manager to install Python...
    winget install Python.Python.3.11
    goto :check_install
)

REM Check if we have chocolatey
choco --version >nul 2>&1
if not errorlevel 1 (
    echo Using Chocolatey to install Python...
    choco install python -y
    goto :check_install
)

REM Manual download and install
echo Downloading Python installer...
echo.

REM Create temp directory
if not exist "temp" mkdir temp
cd temp

REM Download Python 3.11 installer
echo Downloading Python 3.11.5 installer...
powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe' -OutFile 'python-installer.exe'"

if not exist "python-installer.exe" (
    echo Failed to download Python installer!
    echo Please install Python manually from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Installing Python...
echo This will take a few minutes...
python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

REM Wait for installation
timeout /t 30 /nobreak

REM Clean up
cd ..
rmdir /s /q temp

:check_install
echo.
echo Checking Python installation...
timeout /t 5 /nobreak

REM Refresh environment variables
call refreshenv 2>nul || echo Refreshing environment...

REM Check if Python is now available
python --version >nul 2>&1
if errorlevel 1 (
    echo Python installation failed or PATH not updated.
    echo Please:
    echo 1. Restart this command prompt
    echo 2. Or install Python manually from: https://www.python.org/downloads/
    echo 3. Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Python installed successfully!
python --version
echo.

:run_bot
echo Setting up Shopee Bot environment...
echo.

REM Create virtual environment
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install required packages
echo Installing required packages...
pip install --upgrade pip
pip install selenium webdriver-manager requests

echo.
echo ========================================
echo  SHOPEE BOT SETUP COMPLETE
echo ========================================
echo.
echo Python version:
python --version
echo.
echo Pip packages:
pip list | findstr -i "selenium webdriver requests"
echo.

REM Run the bot
echo Starting Shopee Live Viewer Bot...
echo.
python final_shopee_bot.py

echo.
echo Bot finished! Press any key to exit.
pause >nul
