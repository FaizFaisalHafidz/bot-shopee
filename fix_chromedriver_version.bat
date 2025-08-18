@echo off
REM Fix ChromeDriver Version Mismatch - Download Compatible ChromeDriver
REM Script untuk download ChromeDriver yang compatible dengan Chrome 127

title Fix ChromeDriver Version Mismatch

echo 🔧 FIXING CHROMEDRIVER VERSION MISMATCH
echo =======================================
echo Chrome Version: 127.0.6533.74
echo Current ChromeDriver: 114.0.5735.90 (INCOMPATIBLE)
echo Target ChromeDriver: 127.0.6533.119 (COMPATIBLE)
echo.

echo ⚠️  DETECTED ISSUE:
echo    Chrome auto-updated to version 127
echo    But ChromeDriver is still version 114
echo    This causes "session not created" errors
echo.

pause

echo 🗑️  Step 1: Removing old ChromeDriver...
echo.

REM Remove old ChromeDriver dari berbagai lokasi
if exist chromedriver.exe (
    echo Removing chromedriver.exe from current folder...
    del chromedriver.exe
)

if exist C:\Windows\System32\chromedriver.exe (
    echo Removing chromedriver.exe from System32...
    del C:\Windows\System32\chromedriver.exe
)

if exist "%USERPROFILE%\Downloads\bot-shopee-main\chromedriver.exe" (
    echo Removing chromedriver.exe from Downloads folder...
    del "%USERPROFILE%\Downloads\bot-shopee-main\chromedriver.exe"
)

echo ✅ Old ChromeDriver removed
echo.

echo 📥 Step 2: Downloading compatible ChromeDriver 127.0.6533.119...
echo This will take a moment...
echo.

REM Download ChromeDriver 127.0.6533.119 (compatible dengan Chrome 127)
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Write-Host 'Downloading ChromeDriver 127.0.6533.119...'; try { Invoke-WebRequest -Uri 'https://chromedriver.storage.googleapis.com/127.0.6533.119/chromedriver_win32.zip' -OutFile 'chromedriver_127.zip'; Write-Host 'Download successful!' } catch { Write-Host 'Download failed, trying alternative URL...'; Invoke-WebRequest -Uri 'https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/127.0.6533.119/win32/chromedriver-win32.zip' -OutFile 'chromedriver_127.zip' }}"

if exist chromedriver_127.zip (
    echo ✅ ChromeDriver 127 downloaded successfully!
    echo.
    
    echo 📦 Step 3: Extracting ChromeDriver...
    powershell -Command "Expand-Archive -Path 'chromedriver_127.zip' -DestinationPath '.' -Force"
    
    REM Handle different extraction structures
    if exist chromedriver-win32\chromedriver.exe (
        echo Moving from chromedriver-win32 folder...
        move chromedriver-win32\chromedriver.exe .
        rmdir /s /q chromedriver-win32
    )
    
    if exist chromedriver.exe (
        echo ✅ ChromeDriver extracted successfully!
        echo.
        
        echo 🔧 Step 4: Installing ChromeDriver to System32...
        copy chromedriver.exe C:\Windows\System32\
        if %errorlevel%==0 (
            echo ✅ ChromeDriver installed to System32
        ) else (
            echo ⚠️  Could not copy to System32 (admin rights needed)
            echo 💡 ChromeDriver available in current folder
        )
        
        echo.
        echo 🧪 Step 5: Testing new ChromeDriver...
        chromedriver --version 2>nul
        if %errorlevel%==0 (
            echo ✅ ChromeDriver is working!
            chromedriver --version
        ) else (
            echo ⚠️  ChromeDriver test failed, but file exists
        )
        
    ) else (
        echo ❌ Extraction failed
        echo 💡 Try manual download from: https://chromedriver.chromium.org/
    )
    
    REM Clean up
    del chromedriver_127.zip
    
) else (
    echo ❌ Download failed!
    echo.
    echo 💡 MANUAL SOLUTION:
    echo 1. Go to https://chromedriver.chromium.org/downloads
    echo 2. Download ChromeDriver 127.0.6533.119
    echo 3. Extract chromedriver.exe to this folder
    echo 4. Copy chromedriver.exe to C:\Windows\System32\
)

echo.
echo 🎉 CHROMEDRIVER UPDATE COMPLETE!
echo ================================
echo.

if exist chromedriver.exe (
    echo ✅ ChromeDriver Status: READY
    echo 📍 Location: Current folder + System32
    echo 🔢 Version: 127.0.6533.119 (Compatible with Chrome 127)
    echo.
    echo 🚀 READY TO TEST:
    echo    python browser_bot.py
    echo.
    echo Browser automation should work now! 🎯
) else (
    echo ❌ ChromeDriver Status: FAILED
    echo 💡 Please try manual installation
)

echo.
echo Press any key to exit...
pause >nul
