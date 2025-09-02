@echo off
title Google Profile Setup - Windows RDP Multi-Session
color 0A

echo ========================================
echo  ROBUST GOOGLE PROFILE SETUP - WINDOWS
echo  Multi-RDP Support for 100+ Accounts
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python first: https://www.python.org/downloads/
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)

echo [OK] Python found
echo.

REM Check if Chrome is installed
set CHROME_FOUND=0
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    echo [OK] Chrome found: Program Files
    set CHROME_FOUND=1
) else if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" (
    echo [OK] Chrome found: Program Files x86
    set CHROME_FOUND=1
) else if exist "%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe" (
    echo [OK] Chrome found: Local AppData
    set CHROME_FOUND=1
)

if %CHROME_FOUND%==0 (
    echo [ERROR] Google Chrome not found!
    echo Please install Chrome first: https://www.google.com/chrome/
    echo.
    pause
    exit /b 1
)

REM Create virtual environment if not exists
if not exist "venv" (
    echo [SETUP] Creating Python virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
)

REM Activate virtual environment
echo [SETUP] Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip and install packages
echo [SETUP] Installing/upgrading packages...
python -m pip install --upgrade pip
pip install selenium webdriver-manager requests

REM Check if accounts CSV exists
if not exist "accounts\google_accounts_100.csv" (
    echo [ERROR] accounts\google_accounts_100.csv not found!
    echo.
    echo Creating sample CSV file...
    if not exist "accounts" mkdir accounts
    echo email,password,profile_name,status,setup_date > "accounts\google_accounts_100.csv"
    echo your_email1@gmail.com,your_password1,profile1,active, >> "accounts\google_accounts_100.csv"
    echo your_email2@gmail.com,your_password2,profile2,active, >> "accounts\google_accounts_100.csv"
    echo your_email3@gmail.com,your_password3,profile3,active, >> "accounts\google_accounts_100.csv"
    
    echo [CREATED] Sample CSV file created
    echo Please edit accounts\google_accounts_100.csv with your real Google accounts
    echo Then run this script again.
    echo.
    pause
    exit /b 0
)

REM Count accounts
for /f %%A in ('type "accounts\google_accounts_100.csv" ^| find /c /v ""') do set ACCOUNT_COUNT=%%A
set /a ACCOUNT_COUNT=%ACCOUNT_COUNT%-1
echo [INFO] Found %ACCOUNT_COUNT% Google accounts in CSV

echo.
echo ========================================
echo           SETUP CONFIGURATION
echo ========================================
echo  Total Accounts: %ACCOUNT_COUNT%
echo  RDP Sessions: 6 (automatic distribution)
echo  Chrome: Real Chrome (not Chromium)
echo  Profiles: sessions\google_profiles\
echo  Batch Mode: Yes (for stability)
echo ========================================
echo.

echo [WARNING] RDP REQUIREMENTS:
echo  - Keep RDP connection stable during setup
echo  - Complete 2FA/Captcha manually when prompted
echo  - Chrome windows will open automatically
echo  - Process can take 2-5 minutes per account
echo.

set /p CONFIRM="Continue with Google profile setup? (y/N): "
if /i not "%CONFIRM%"=="y" (
    echo [CANCELLED] Setup cancelled by user
    pause
    exit /b 0
)

echo.
echo [STARTING] Robust Google Profile Setup...
echo [INFO] Using enhanced stability measures
echo [INFO] Chrome crash prevention enabled
echo [INFO] Button clicking with multiple fallbacks
echo.

REM Run the robust setup
python robust_google_setup.py

echo.
echo ========================================
echo        GOOGLE PROFILE SETUP COMPLETE
echo ========================================
echo.
echo Check the logs folder for detailed results.
echo Profiles are saved in: sessions\google_profiles\
echo.
echo Press any key to exit...
pause >nul
