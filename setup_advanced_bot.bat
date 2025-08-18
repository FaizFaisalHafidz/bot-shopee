@echo off
REM Setup Advanced Shopee Bot - Complete Installation
REM With undetected Chrome and robust authentication

title Advanced Shopee Bot - Setup

echo 🚀 ADVANCED SHOPEE BOT SETUP
echo ============================
echo Installing advanced bot dengan authentication bypass
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

echo 📦 Installing advanced requirements...
echo This may take 2-3 minutes...
echo.

REM Install advanced requirements
pip install -r advanced_bot/requirements_advanced.txt

if %errorlevel%==0 (
    echo ✅ Advanced packages installed successfully!
) else (
    echo ⚠️  Some packages had issues, trying alternatives...
    
    echo Installing core packages individually...
    pip install selenium
    pip install requests
    pip install urllib3
    pip install undetected-chromedriver
    pip install webdriver-manager
    pip install fake-useragent
)

echo.
echo 🧪 Testing advanced bot imports...

python -c "import selenium; print('✅ selenium OK')" 2>nul || echo "❌ selenium failed"
python -c "import undetected_chromedriver; print('✅ undetected-chromedriver OK')" 2>nul || echo "❌ undetected-chromedriver failed"
python -c "import requests; print('✅ requests OK')" 2>nul || echo "❌ requests failed"

echo.
echo 🔍 Checking Chrome installation...

REM Check Chrome dengan beberapa metode
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    echo ✅ Chrome found at Program Files
) else if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" (
    echo ✅ Chrome found at Program Files (x86)
) else (
    echo ⚠️  Chrome not found in standard locations
    echo 💡 Please install Chrome from https://www.google.com/chrome/
)

echo.
echo 📁 Checking file structure...

if exist "advanced_bot\advanced_bot.py" (
    echo ✅ Main bot file found
) else (
    echo ❌ Main bot file missing!
)

if exist "advanced_bot\auth\shopee_auth.py" (
    echo ✅ Authentication module found
) else (
    echo ❌ Authentication module missing!
)

if exist "input.csv" (
    echo ✅ input.csv found
) else (
    echo ⚠️  input.csv not found - you'll need to add your cookies
)

echo.
echo 🎉 ADVANCED BOT SETUP COMPLETE!
echo ===============================
echo.

echo 🚀 Ready to run:
echo    cd advanced_bot
echo    python advanced_bot.py
echo.

echo 🛡️  Features enabled:
echo    ✅ Undetected Chrome driver
echo    ✅ Advanced authentication bypass
echo    ✅ Anti-detection mechanisms
echo    ✅ Persistent session management
echo    ✅ Organized folder structure
echo.

echo 💡 If you get import errors:
echo    1. Make sure all packages installed successfully
echo    2. Try running as Administrator
echo    3. Check Python PATH configuration
echo.

pause
