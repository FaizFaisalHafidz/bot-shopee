@echo off
chcp 65001
cls

echo ===============================================================================
echo    SHOPEE ULTRA RDP BOT - ROBUST LAUNCHER
echo    Auto-retry for connection errors + Enhanced stability
echo ===============================================================================
echo.

set /p session_id="Enter Shopee Live Session ID (e.g., 157658364): "
set /p viewer_count="Enter viewer count (default 3): "

if "%viewer_count%"=="" set viewer_count=3

echo.
echo Starting ROBUST RDP Bot with auto-retry...
echo Session ID: %session_id%
echo Viewer Count: %viewer_count%
echo Mode: Ultra RDP Headless (GPU Disabled + Robust)
echo Bypass: Ultra-aggressive + Emergency methods + Auto-retry
echo Expected Mega Boost: %viewer_count% x 500 = %viewer_count%500
echo.

echo [SETUP] Activating virtual environment...
call venv\Scripts\activate

:retry_loop
echo ================================================================================
echo    SHOPEE ULTRA RDP BOT - ROBUST EXECUTION
echo    Auto-retry enabled for connection errors
echo ================================================================================
echo Target Session: %session_id%
echo Viewer Count: %viewer_count%
echo Mode: Ultra RDP Headless + Robust
echo Expected Mega Boost: %viewer_count%500
echo ================================================================================
echo.

echo [LAUNCH] Starting robust ultra bot...
python real_url_bot_ultra.py %session_id% %viewer_count%

set exit_code=%ERRORLEVEL%

if %exit_code% NEQ 0 (
    echo.
    echo [ERROR] Bot encountered an error (Exit code: %exit_code%)
    echo.
    echo Common fixes for RDP environment:
    echo 1. Connection reset - usually temporary network issue
    echo 2. Chrome process conflict - will auto-cleanup
    echo 3. DevTools port busy - will auto-retry with new port
    echo.
    
    choice /C YN /M "Do you want to auto-retry in 10 seconds? (Y/N)"
    if errorlevel 2 goto end
    
    echo [CLEANUP] Cleaning up Chrome processes...
    taskkill /f /im chrome.exe >nul 2>&1
    taskkill /f /im chromedriver.exe >nul 2>&1
    
    echo [WAIT] Waiting 10 seconds for cleanup...
    timeout /t 10 /nobreak >nul
    
    echo [RETRY] Restarting bot...
    goto retry_loop
) else (
    echo.
    echo [SUCCESS] Bot completed successfully!
    echo All viewers should be active now.
    echo Check your Shopee Live stream for increased viewer count.
)

:end
echo.
echo [INFO] Bot session ended.
echo Press any key to exit...
pause >nul
