@echo off
REM Simple Requirements Installer - Won't close window on errors
REM Use this if main setup scripts keep closing

title Shopee Bot - Simple Package Install

echo 🔧 SIMPLE PACKAGE INSTALLER
echo ===========================
echo This script will install required packages step by step
echo Window will stay open even if there are errors
echo.

REM Keep window open on any error
setlocal EnableDelayedExpansion

echo Checking Python...
python --version
if %errorlevel% neq 0 (
    echo.
    echo ❌ Python not found!
    echo.
    echo SOLUTION:
    echo 1. Install Python from https://python.org
    echo 2. Make sure to check "Add Python to PATH" during install
    echo 3. Restart this script
    echo.
    goto :wait_exit
)

echo.
echo ✅ Python found! Installing packages...
echo.

echo [1/3] Installing requests...
pip install requests
echo Done with requests (error level: %errorlevel%)
echo.

echo [2/3] Installing urllib3...  
pip install urllib3
echo Done with urllib3 (error level: %errorlevel%)
echo.

echo [3/3] Installing selenium...
pip install selenium
echo Done with selenium (error level: %errorlevel%)
echo.

echo ================================
echo TESTING INSTALLATIONS:
echo ================================
echo.

python -c "import requests; print('✅ requests: OK')" 2>nul || echo "❌ requests: FAILED"
python -c "import urllib3; print('✅ urllib3: OK')" 2>nul || echo "❌ urllib3: FAILED"
python -c "from selenium import webdriver; print('✅ selenium: OK')" 2>nul || echo "❌ selenium: FAILED"

echo.
echo ================================
echo INSTALLATION COMPLETE
echo ================================
echo.

echo If any package shows FAILED above:
echo 1. Try running as Administrator
echo 2. Or try: python -m pip install [package_name]
echo 3. Or try: pip install --user [package_name]
echo.

echo Ready to test bot:
echo • python browser_bot.py (recommended)
echo • python main.py (alternative)
echo.

:wait_exit
echo Press any key to exit...
pause >nul
