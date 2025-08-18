@echo off
REM Chrome Detection Test - Multiple Methods
REM This will test different ways to find Chrome on Windows

title Chrome Detection Test

echo 🔍 TESTING CHROME DETECTION
echo ===========================
echo Testing multiple methods to find Google Chrome...
echo.

echo Method 1: Registry - BLBeacon...
reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Google\Chrome\BLBeacon" /v version >nul 2>&1
if %errorlevel%==0 (
    echo ✅ Found via BLBeacon registry
    for /f "tokens=3" %%i in ('reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Google\Chrome\BLBeacon" /v version 2^>nul') do echo    Version: %%i
) else (
    echo ❌ Not found via BLBeacon registry
)

echo.
echo Method 2: Registry - Uninstall entry...
reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall" /s /f "Google Chrome" >nul 2>&1
if %errorlevel%==0 (
    echo ✅ Found in Uninstall registry
) else (
    echo ❌ Not found in Uninstall registry
)

echo.
echo Method 3: Registry - WOW6432Node (64-bit)...
reg query "HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Google\Chrome\BLBeacon" /v version >nul 2>&1
if %errorlevel%==0 (
    echo ✅ Found via WOW6432Node registry
    for /f "tokens=3" %%i in ('reg query "HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Google\Chrome\BLBeacon" /v version 2^>nul') do echo    Version: %%i
) else (
    echo ❌ Not found via WOW6432Node registry
)

echo.
echo Method 4: File system check - Program Files...
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    echo ✅ Found at: C:\Program Files\Google\Chrome\Application\chrome.exe
) else (
    echo ❌ Not found at: C:\Program Files\Google\Chrome\Application\
)

echo.
echo Method 5: File system check - Program Files (x86)...
if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" (
    echo ✅ Found at: C:\Program Files (x86)\Google\Chrome\Application\chrome.exe
) else (
    echo ❌ Not found at: C:\Program Files (x86)\Google\Chrome\Application\
)

echo.
echo Method 6: User AppData...
if exist "%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe" (
    echo ✅ Found at: %LOCALAPPDATA%\Google\Chrome\Application\chrome.exe
) else (
    echo ❌ Not found in user AppData
)

echo.
echo Method 7: WHERE command...
where chrome.exe >nul 2>&1
if %errorlevel%==0 (
    echo ✅ Chrome found in PATH:
    where chrome.exe
) else (
    echo ❌ Chrome not in system PATH
)

echo.
echo Method 8: Direct execution test...
"C:\Program Files\Google\Chrome\Application\chrome.exe" --version 2>nul
if %errorlevel%==0 (
    echo ✅ Chrome executable works (Program Files)
) else (
    "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --version 2>nul
    if %errorlevel%==0 (
        echo ✅ Chrome executable works (Program Files x86)
    ) else (
        echo ❌ Chrome executable test failed
    )
)

echo.
echo ================================
echo DETECTION SUMMARY
echo ================================
echo If any method above shows ✅, Chrome is installed!
echo If all show ❌, Chrome might need to be reinstalled.
echo.

pause
