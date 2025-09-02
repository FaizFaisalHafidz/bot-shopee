@echo off
chcp 65001 > nul
echo ============================================
echo SHOPEE BOT FINAL TEST
echo ============================================
echo.

echo [INFO] Final test with isolated Chrome profiles
echo [INFO] This should avoid all profile conflicts
echo.

echo [STEP 1] Profile detection...
cd /d "%~dp0"
python scripts/detect_profiles_clean.py
if errorlevel 1 (
    echo [ERROR] Profile detection failed
    pause
    exit /b 1
)

echo.
echo [STEP 2] Chrome cleanup...
taskkill /f /im chrome.exe /t >nul 2>&1
timeout /t 3 /nobreak > nul
echo [SUCCESS] Chrome processes cleared

echo.
echo [STEP 3] Cleanup old bot sessions...
if exist "sessions\isolated_profiles" (
    rmdir /s /q "sessions\isolated_profiles" >nul 2>&1
)
echo [SUCCESS] Ready for fresh start

echo.
echo [STEP 4] Start bot (1 viewer test)...
echo [CONFIG] Session: 157658364, Viewers: 1, Delay: 5
echo.

cd scripts
python shopee_bot.py 157658364 1 5

echo.
echo [COMPLETED] Test finished
pause
