@echo off
chcp 65001 > nul
echo ============================================
echo SHOPEE BOT DIRECT PROFILE ACCESS
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
echo [STEP 2] Kill existing Chrome processes...
echo [INFO] Auto-killing Chrome processes for clean start...
taskkill /f /im chrome.exe /t 2>nul
timeout /t 3 /nobreak > nul
echo [SUCCESS] Chrome processes cleared

echo.
echo [STEP 3] Starting bot with original profiles...
echo [INFO] Using configuration:
echo   Session ID: 157658364
echo   Viewers: 3 (all Gmail accounts)
echo   Delay: 5 seconds
echo   Profile Mode: Direct access (no temp copies)
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
