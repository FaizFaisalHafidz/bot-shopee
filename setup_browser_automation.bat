@echo off
REM Setup Browser Automation Bot untuk RDP Windows
REM Install Chrome, ChromeDriver, dan Selenium

echo 🌐 Setting up Browser Automation Bot
echo ===================================
echo.

REM Check if Python installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found! Please install Python first
    pause
    exit /b 1
)

echo ✅ Python found:
python --version
echo.

echo 📦 Installing Selenium and dependencies...
pip install selenium requests urllib3

echo.
echo 🌐 Checking Chrome browser...

REM Check if Chrome is installed
reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Google\Chrome\BLBeacon" /v version >nul 2>&1
if %errorlevel%==0 (
    echo ✅ Google Chrome found
) else (
    echo ⚠️  Google Chrome not found
    echo 📥 Please install Chrome from: https://www.google.com/chrome/
    echo.
    set /p continue="Continue setup? Chrome will be needed later (y/n): "
    if /i not "%continue%"=="y" exit /b 1
)

echo.
echo 🔧 Installing ChromeDriver...

REM Download ChromeDriver
echo 📥 Downloading ChromeDriver...
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_win32.zip' -OutFile 'chromedriver.zip'}"

if exist chromedriver.zip (
    echo ✅ ChromeDriver downloaded
    
    REM Extract ChromeDriver
    powershell -Command "Expand-Archive -Path 'chromedriver.zip' -DestinationPath '.' -Force"
    
    REM Move to Windows directory
    if exist chromedriver.exe (
        move chromedriver.exe C:\Windows\System32\
        echo ✅ ChromeDriver installed to System32
    )
    
    REM Clean up
    del chromedriver.zip
) else (
    echo ⚠️  ChromeDriver download failed
    echo 💡 Manual download: https://chromedriver.chromium.org/
)

echo.
echo 🧪 Testing browser automation...
python -c "from selenium import webdriver; print('✅ Selenium import OK')" 2>nul || echo "❌ Selenium import failed"

echo.
echo 🎉 Browser automation setup complete!
echo.
echo 📋 Files ready:
echo    • browser_bot.py - Browser automation bot
echo    • main.py - HTTP-only bot (original)
echo.
echo 💡 Usage:
echo    python browser_bot.py  - Real browser tabs (recommended)
echo    python main.py         - HTTP requests only
echo.
echo 🚀 Browser bot will open Chrome tabs for each account!
echo 📊 This will show REAL viewer increase in live stream
echo.

pause
