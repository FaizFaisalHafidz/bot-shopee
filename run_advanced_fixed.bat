@echo off
REM Run Advanced Bot Fixed - API Authentication Version
REM Fixed authentication detection with API verification

title Advanced Shopee Bot - Fixed Authentication

echo 🚀 ADVANCED BOT - FIXED AUTHENTICATION VERSION
echo ==============================================
echo Menggunakan API verification untuk authentication
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python tidak ditemukan!
    echo 💡 Install Python dari https://python.org
    pause
    exit /b 1
)

echo ✅ Python found:
python --version
echo.

REM Check if input.csv exists
if not exist "input.csv" (
    echo ❌ input.csv tidak ditemukan!
    echo 💡 Pastikan file input.csv ada dengan cookies akun Shopee
    pause
    exit /b 1
)

echo ✅ input.csv found
echo.

REM Check Selenium installation
python -c "import selenium" 2>nul
if %errorlevel% neq 0 (
    echo ⚠️  Selenium tidak terinstall, installing...
    pip install selenium requests
    if %errorlevel% neq 0 (
        echo ❌ Gagal install dependencies!
        pause
        exit /b 1
    )
) else (
    echo ✅ Selenium sudah terinstall
)

REM Check requests
python -c "import requests" 2>nul
if %errorlevel% neq 0 (
    echo ⚠️  Requests tidak terinstall, installing...
    pip install requests
) else (
    echo ✅ Requests available
)

REM Check undetected-chromedriver (optional)
python -c "import undetected_chromedriver" 2>nul
if %errorlevel%==0 (
    echo ✅ undetected-chromedriver available (stealth mode ON)
) else (
    echo ⚠️  undetected-chromedriver not available (using standard Chrome)
    echo 💡 For better stealth: pip install undetected-chromedriver
)

echo.
echo 🌐 Checking Chrome browser...
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    echo ✅ Chrome found
) else if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" (
    echo ✅ Chrome found (x86)
) else (
    echo ⚠️  Chrome not found - please install Chrome first
    echo 💡 Download: https://www.google.com/chrome/
)

echo.
echo 🎯 FEATURES ENABLED:
echo    ✅ API-based authentication verification
echo    ✅ Direct live stream navigation
echo    ✅ Better error handling
echo    ✅ Real viewer count increase
echo.

echo 🚀 Launching Advanced Bot (Fixed Authentication)...
echo.

REM Run the fixed advanced bot
python advanced_bot_fixed.py

echo.
echo Advanced Bot execution completed.
pause
