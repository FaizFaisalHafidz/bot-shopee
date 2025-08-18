@echo off
REM Run Advanced Bot Simplified - Fixed version
REM Better import handling and error recovery

title Advanced Shopee Bot - Simplified Launcher

echo 🚀 ADVANCED BOT - SIMPLIFIED VERSION
echo ===================================
echo Fixed version dengan better import handling
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
    pip install selenium
    if %errorlevel% neq 0 (
        echo ❌ Gagal install Selenium!
        pause
        exit /b 1
    )
) else (
    echo ✅ Selenium sudah terinstall
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
echo 🚀 Launching Advanced Bot (Simplified)...
echo.

REM Run the simplified advanced bot
python advanced_bot_simple.py

echo.
echo Advanced Bot execution completed.
pause
