@echo off
chcp 65001 > nul
echo ============================================
echo SHOPEE BOT WITH TEMP PROFILE SYSTEM
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
call check_chrome_process.bat

echo.
echo [STEP 4] Starting Shopee bot with temp profiles...
cd scripts
python shopee_bot.py
if errorlevel 1 (
    echo [ERROR] Bot execution failed
    pause
    exit /b 1
)

echo.
echo [SUCCESS] Bot execution completed
pause
