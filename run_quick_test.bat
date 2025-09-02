@echo off
chcp 65001 > nul
echo ============================================
echo SHOPEE BOT QUICK START (DEFAULT VALUES)
echo ============================================
echo.

echo [STEP 1] Detect Chrome profiles...
cd /d "%~dp0"
python scripts/detect_profiles_clean.py
if errorlevel 1 (
    echo [ERROR] Failed to detect profiles
    pause
    exit /b 1
)

echo.
echo [STEP 2] Create temporary profile copies...
python create_temp_profiles.py
if errorlevel 1 (
    echo [ERROR] Failed to create temp profiles
    pause
    exit /b 1
)

echo.
echo [STEP 3] Check existing Chrome processes...
echo [INFO] Auto-killing Chrome processes for clean start...
taskkill /f /im chrome.exe /t 2>nul
timeout /t 2 /nobreak > nul
echo [SUCCESS] Chrome processes cleared

echo.
echo [STEP 4] Starting Shopee bot with default settings...
echo [INFO] Using default configuration:
echo   Session ID: 157658364
echo   Viewers: 3
echo   Delay: 5 seconds
echo.

cd scripts
python shopee_bot.py 157658364 3 5
if errorlevel 1 (
    echo [ERROR] Bot execution failed
    pause
    exit /b 1
)

echo.
echo [SUCCESS] Bot execution completed
pause
