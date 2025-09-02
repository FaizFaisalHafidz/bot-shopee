@echo off
chcp 65001 > nul
echo ============================================
echo SHOPEE BOT ISOLATED MODE
echo ============================================
echo.

echo [INFO] This mode creates completely isolated Chrome profiles
echo [INFO] No conflicts with existing Chrome profiles
echo [INFO] Each viewer gets fresh isolated environment
echo.

echo [STEP 1] Detect original profiles for reference...
cd /d "%~dp0"
python scripts/detect_profiles_clean.py
if errorlevel 1 (
    echo [ERROR] Failed to detect profiles
    pause
    exit /b 1
)

echo.
echo [STEP 2] Kill existing Chrome processes...
echo [INFO] Clearing all Chrome processes for safe start...
taskkill /f /im chrome.exe /t 2>nul
timeout /t 3 /nobreak > nul
echo [SUCCESS] Chrome processes cleared

echo.
echo [STEP 3] Clean up old isolated profiles...
if exist "sessions\isolated_profiles" (
    echo [INFO] Removing old isolated profiles...
    rmdir /s /q "sessions\isolated_profiles"
    echo [SUCCESS] Cleanup completed
)

echo.
echo [STEP 4] Starting bot with isolated profiles...
echo [INFO] Configuration:
echo   Session ID: 157658364
echo   Viewers: 3 (isolated profiles)
echo   Delay: 5 seconds
echo   Mode: Isolated (no conflicts)
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
