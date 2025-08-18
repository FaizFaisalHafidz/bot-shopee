@echo off
REM Safe Browser Automation Setup - Prevents CMD window closing
REM This version handles errors gracefully and keeps window open

title Shopee Bot - Browser Setup (Safe Mode)

echo 🛡️  SAFE BROWSER AUTOMATION SETUP
echo =================================
echo This version will NOT close the window on errors
echo.

REM Set error handling - continue on errors
setlocal EnableDelayedExpansion

echo 🔍 Step 1: Checking Python...
echo.

python --version 2>nul
if %errorlevel% neq 0 (
    echo ❌ Python not found!
    echo.
    echo 💡 SOLUTION:
    echo 1. Download Python from https://python.org
    echo 2. During install, check "Add Python to PATH" ✅
    echo 3. Restart this script after Python install
    echo.
    echo Press any key to exit and install Python...
    pause >nul
    goto :end
) else (
    echo ✅ Python found:
    python --version
)

echo.
echo 🔍 Step 2: Checking pip...
echo.

pip --version 2>nul
if %errorlevel% neq 0 (
    echo ⚠️  pip not found, trying to fix...
    python -m ensurepip --upgrade
    python -m pip install --upgrade pip
) else (
    echo ✅ pip found:
    pip --version
)

echo.
echo 📦 Step 3: Installing Python packages...
echo This may take 1-2 minutes...
echo.

REM Install packages one by one with error checking
echo Installing requests...
pip install requests
if %errorlevel% neq 0 (
    echo ⚠️  requests install had issues, but continuing...
) else (
    echo ✅ requests installed
)

echo.
echo Installing urllib3...
pip install urllib3
if %errorlevel% neq 0 (
    echo ⚠️  urllib3 install had issues, but continuing...
) else (
    echo ✅ urllib3 installed
)

echo.
echo Installing selenium (this is the big one)...
pip install selenium
if %errorlevel% neq 0 (
    echo ⚠️  selenium install had issues, trying alternative...
    echo Trying with --user flag...
    pip install --user selenium
    if %errorlevel% neq 0 (
        echo ❌ Selenium install failed!
        echo.
        echo 💡 MANUAL SOLUTION:
        echo 1. Open new CMD as Administrator
        echo 2. Run: pip install selenium requests urllib3
        echo 3. If still fails, try: python -m pip install selenium
        goto :show_status
    )
) else (
    echo ✅ selenium installed
)

echo.
echo 🌐 Step 4: Checking Chrome browser...
echo.

REM Check Chrome installation
reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Google\Chrome\BLBeacon" /v version >nul 2>&1
if %errorlevel%==0 (
    echo ✅ Google Chrome found
    for /f "tokens=3" %%i in ('reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Google\Chrome\BLBeacon" /v version 2^>nul') do echo Chrome version: %%i
) else (
    echo ⚠️  Google Chrome not found
    echo.
    echo 💡 SOLUTION:
    echo 1. Download Chrome from https://www.google.com/chrome/
    echo 2. Install Chrome normally
    echo 3. Run this script again
    echo.
    set /p continue="Continue without Chrome for now? (y/n): "
    if /i not "!continue!"=="y" goto :end
)

echo.
echo 🔧 Step 5: Setting up ChromeDriver...
echo.

REM Try to download ChromeDriver (but don't fail if it doesn't work)
echo Downloading ChromeDriver...
powershell -Command "try { [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_win32.zip' -OutFile 'chromedriver.zip'; Write-Host 'Download successful' } catch { Write-Host 'Download failed, will try manual method' }" 2>nul

if exist chromedriver.zip (
    echo ✅ ChromeDriver downloaded
    
    REM Extract ChromeDriver
    powershell -Command "try { Expand-Archive -Path 'chromedriver.zip' -DestinationPath '.' -Force; Write-Host 'Extract successful' } catch { Write-Host 'Extract failed' }" 2>nul
    
    if exist chromedriver.exe (
        echo Moving ChromeDriver to System32...
        copy chromedriver.exe C:\Windows\System32\ >nul 2>&1
        if %errorlevel%==0 (
            echo ✅ ChromeDriver installed to System32
        ) else (
            echo ⚠️  Could not copy to System32 (need admin rights)
            echo 💡 ChromeDriver is available in current folder
        )
    )
    
    REM Clean up
    if exist chromedriver.zip del chromedriver.zip >nul 2>&1
) else (
    echo ⚠️  ChromeDriver download failed
    echo 💡 MANUAL SOLUTION:
    echo 1. Download from: https://chromedriver.chromium.org/
    echo 2. Extract chromedriver.exe to C:\Windows\System32\
)

:show_status
echo.
echo 🧪 Step 6: Testing installation...
echo.

REM Test Python imports
echo Testing Python imports...
python -c "import requests; print('✅ requests OK')" 2>nul || echo "❌ requests failed"
python -c "import urllib3; print('✅ urllib3 OK')" 2>nul || echo "❌ urllib3 failed" 
python -c "from selenium import webdriver; print('✅ selenium OK')" 2>nul || echo "❌ selenium failed"

echo.
echo 🎉 SETUP COMPLETE!
echo ===================
echo.

REM Show final status
echo 📋 INSTALLATION SUMMARY:
echo.
python --version 2>nul && echo "✅ Python: Working" || echo "❌ Python: Failed"
pip --version 2>nul && echo "✅ pip: Working" || echo "❌ pip: Failed"
python -c "import requests" 2>nul && echo "✅ requests: Installed" || echo "❌ requests: Missing"
python -c "import urllib3" 2>nul && echo "✅ urllib3: Installed" || echo "❌ urllib3: Missing"
python -c "from selenium import webdriver" 2>nul && echo "✅ selenium: Installed" || echo "❌ selenium: Missing"

if exist chromedriver.exe echo "✅ ChromeDriver: Available in folder" || if exist C:\Windows\System32\chromedriver.exe echo "✅ ChromeDriver: Installed in System32" || echo "⚠️  ChromeDriver: Needs manual install"

echo.
echo 🚀 READY TO RUN:
echo.
echo For Browser Bot (RECOMMENDED):
echo    python browser_bot.py
echo.
echo For HTTP Bot (Alternative):  
echo    python main.py
echo.

:end
echo.
echo Press any key to close...
pause >nul
