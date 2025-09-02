@echo off
title Shopee Bot - Windows RDP Fixer
echo ========================================
echo  SHOPEE BOT - WINDOWS RDP PYTHON FIX
echo ========================================
echo.

echo Diagnostic: Checking Python installation methods...
echo.

REM Method 1: Check standard python command
echo [TEST 1] python --version
python --version 2>nul
if %errorlevel% equ 0 (
    echo ✅ Python found via 'python'!
    set PYTHON_CMD=python
    goto :setup_bot
) else (
    echo ❌ 'python' command not found
)

echo.

REM Method 2: Check python3 command  
echo [TEST 2] python3 --version
python3 --version 2>nul
if %errorlevel% equ 0 (
    echo ✅ Python found via 'python3'!
    set PYTHON_CMD=python3
    goto :setup_bot
) else (
    echo ❌ 'python3' command not found
)

echo.

REM Method 3: Check py launcher
echo [TEST 3] py --version
py --version 2>nul
if %errorlevel% equ 0 (
    echo ✅ Python found via 'py'!
    set PYTHON_CMD=py
    goto :setup_bot
) else (
    echo ❌ 'py' command not found
)

echo.

REM Method 4: Check if Python installed but not in PATH
echo [TEST 4] Scanning for Python installation...
for /d %%i in ("C:\Python*") do (
    if exist "%%i\python.exe" (
        echo ✅ Found Python in %%i
        set PYTHON_CMD="%%i\python.exe"
        goto :setup_bot
    )
)

for /d %%i in ("%LOCALAPPDATA%\Programs\Python\Python*") do (
    if exist "%%i\python.exe" (
        echo ✅ Found Python in %%i
        set PYTHON_CMD="%%i\python.exe"
        goto :setup_bot
    )
)

for /d %%i in ("%PROGRAMFILES%\Python*") do (
    if exist "%%i\python.exe" (
        echo ✅ Found Python in %%i  
        set PYTHON_CMD="%%i\python.exe"
        goto :setup_bot
    )
)

echo ❌ No Python installation found anywhere!
echo.
goto :install_python

:install_python
echo ========================================
echo  INSTALLING PYTHON AUTOMATICALLY
echo ========================================
echo.

REM Try Microsoft Store Python (Windows 10/11)
echo [METHOD 1] Trying Microsoft Store Python...
start ms-windows-store://pdp/?ProductId=9NRWMJP3717K
timeout /t 5 >nul
echo Please install Python from Microsoft Store if it opened...
echo.

REM Method 1: Try winget (Windows Package Manager)
echo [METHOD 2] Trying Windows Package Manager...
winget --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Installing Python via winget...
    winget install Python.Python.3.11 --silent --accept-package-agreements --accept-source-agreements
    timeout /t 10 >nul
    
    REM Refresh PATH
    call :refresh_path
    
    REM Test again
    python --version >nul 2>&1
    if %errorlevel% equ 0 (
        set PYTHON_CMD=python
        goto :setup_bot
    )
) else (
    echo winget not available
)

echo.

REM Method 2: Try Chocolatey
echo [METHOD 3] Trying Chocolatey...
choco --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Installing Python via Chocolatey...
    choco install python -y
    timeout /t 10 >nul
    
    REM Refresh PATH
    call :refresh_path
    
    REM Test again  
    python --version >nul 2>&1
    if %errorlevel% equ 0 (
        set PYTHON_CMD=python
        goto :setup_bot
    )
) else (
    echo Chocolatey not available
)

echo.

REM Method 3: Direct download
echo [METHOD 4] Direct download from python.org...
echo Creating download directory...
if not exist "python_installer" mkdir python_installer
cd python_installer

echo Downloading Python 3.11.5...
powershell -NoProfile -ExecutionPolicy Bypass -Command "& {try { Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe' -OutFile 'python-3.11.5.exe'; Write-Host 'Download successful' } catch { Write-Host 'Download failed:' $_.Exception.Message }}"

if exist "python-3.11.5.exe" (
    echo ✅ Download complete!
    echo Installing Python (please wait)...
    
    REM Silent install with PATH addition
    "python-3.11.5.exe" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    
    echo Waiting for installation to complete...
    timeout /t 30 >nul
    
    REM Refresh PATH
    call :refresh_path
    
    REM Test installation
    python --version >nul 2>&1
    if %errorlevel% equ 0 (
        echo ✅ Python installed successfully!
        set PYTHON_CMD=python
        cd ..
        goto :setup_bot
    ) else (
        echo Installation may have failed, trying py launcher...
        py --version >nul 2>&1
        if %errorlevel% equ 0 (
            set PYTHON_CMD=py
            cd ..
            goto :setup_bot
        )
    )
) else (
    echo ❌ Download failed!
)

cd ..

REM If all methods failed
echo.
echo ========================================
echo  MANUAL INSTALLATION REQUIRED
echo ========================================
echo.
echo All automatic installation methods failed.
echo Please install Python manually:
echo.
echo 1. Go to: https://www.python.org/downloads/
echo 2. Download Python 3.11 or newer
echo 3. During installation:
echo    ✅ Check "Add Python to PATH"  
echo    ✅ Check "Install for all users"
echo 4. Restart this script after installation
echo.
echo Alternative: Install from Microsoft Store
echo 1. Open Microsoft Store
echo 2. Search for "Python 3.11"
echo 3. Install the official Python package
echo.
pause
exit /b 1

:setup_bot
echo.
echo ========================================
echo  SETTING UP SHOPEE BOT
echo ========================================
echo.
echo ✅ Using Python command: %PYTHON_CMD%
%PYTHON_CMD% --version

echo.
echo [1/4] Installing required packages...
%PYTHON_CMD% -m pip install --upgrade pip --quiet
%PYTHON_CMD% -m pip install selenium webdriver-manager requests colorama --quiet

if %errorlevel% neq 0 (
    echo ❌ Failed to install packages!
    pause
    exit /b 1
)

echo ✅ Packages installed successfully!

echo.
echo [2/4] Checking for Chrome installation...
if exist "%PROGRAMFILES%\Google\Chrome\Application\chrome.exe" (
    echo ✅ Chrome found in Program Files
) else if exist "%PROGRAMFILES(X86)%\Google\Chrome\Application\chrome.exe" (
    echo ✅ Chrome found in Program Files (x86)
) else if exist "%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe" (
    echo ✅ Chrome found in Local AppData
) else (
    echo ⚠️ Chrome not found! Please install Google Chrome first.
    echo Download from: https://www.google.com/chrome/
)

echo.
echo [3/4] Checking Chrome profiles...
set PROFILE_COUNT=0

if exist "%LOCALAPPDATA%\Google\Chrome\User Data\Default\Preferences" (
    echo ✅ Default profile found
    set /a PROFILE_COUNT+=1
)

for /d %%d in ("%LOCALAPPDATA%\Google\Chrome\User Data\Profile*") do (
    if exist "%%d\Preferences" (
        echo ✅ Profile found: %%~nd
        set /a PROFILE_COUNT+=1
    )
)

echo Total Chrome profiles: %PROFILE_COUNT%

if %PROFILE_COUNT% equ 0 (
    echo.
    echo ⚠️ WARNING: No Chrome profiles found!
    echo Please create Chrome profiles first:
    echo 1. Open Google Chrome
    echo 2. Click profile icon (top right)
    echo 3. Click "Add profile"
    echo 4. Login with different Google accounts
    echo 5. Repeat for multiple profiles
    echo.
    set /p continue="Continue anyway? (y/N): "
    if /i not "!continue!"=="y" (
        pause
        exit /b 0
    )
)

echo.
echo [4/4] Running Shopee Bot...
echo ========================================
echo.

if exist "final_shopee_bot.py" (
    echo Starting final_shopee_bot.py...
    %PYTHON_CMD% final_shopee_bot.py
) else (
    echo ❌ final_shopee_bot.py not found!
    echo Make sure you're in the correct directory.
    dir *.py
    pause
    exit /b 1
)

echo.
echo ========================================
echo  BOT EXECUTION COMPLETE
echo ========================================
pause
exit /b 0

:refresh_path
REM Refresh environment PATH variable
for /f "skip=2 tokens=3*" %%a in ('reg query HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment /v PATH') do set PATH=%%a %%b
for /f "skip=2 tokens=3*" %%a in ('reg query HKCU\Environment /v PATH') do set PATH=%PATH%;%%a %%b
exit /b
