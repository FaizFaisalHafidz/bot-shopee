@echo off
chcp 65001
cls

:menu
echo ===============================================================================
echo                    SHOPEE LIVE BOT - ULTIMATE LAUNCHER
echo                         Choose your preferred method
echo ===============================================================================
echo.
echo Available Bot Options:
echo.
echo [1] RDP OPTIMIZED BOT (RECOMMENDED) - Fixed permissions + GPU disabled
echo [2] MONITORED BOT (CLIENT GRADE)   - Real-time monitoring + 100 viewers
echo [3] API Bot (EXPERIMENTAL)         - Direct API calls, most reliable  
echo [4] Ultra RDP Bot                  - Browser automation for RDP
echo [5] Device Fingerprint Bot         - Advanced device spoofing
echo [6] Auth Bypass Bot                - Authentication bypass method
echo [7] Quick Launch (Auto-detect)     - Smart launcher selection
echo.
echo [0] Exit
echo.
echo ===============================================================================
echo Recommendations:
echo • For RDP DEPLOYMENT: Use RDP OPTIMIZED BOT (#1) - Fixed all RDP issues
echo • For CLIENT REQUESTS (50-100 viewers): Use MONITORED BOT (#2)
echo • For EXPERIMENTAL API: Use API Bot (#3) 
echo ===============================================================================
echo.

set /p choice="Select option (1-7, 0 to exit): "

if "%choice%"=="1" goto rdp_optimized
if "%choice%"=="2" goto monitored_bot
if "%choice%"=="3" goto api_bot
if "%choice%"=="4" goto ultra_rdp
if "%choice%"=="5" goto device_fingerprint
if "%choice%"=="6" goto auth_bypass
if "%choice%"=="7" goto quick_launch
if "%choice%"=="0" goto exit

echo Invalid choice. Please try again.
pause
goto menu

:rdp_optimized
echo.
echo ===============================================================================
echo    LAUNCHING: SHOPEE RDP OPTIMIZED BOT (RECOMMENDED FOR RDP)
echo    - Fixed ChromeDriver permissions for RDP
echo    - Complete GPU disabling (no WebGL/3D errors)
echo    - Network error resilience
echo    - Simplified monitoring with manual verification
echo ===============================================================================
echo.
call rdp_optimized_launcher.bat
goto menu

:monitored_bot
echo.
echo ===============================================================================
echo    LAUNCHING: SHOPEE MONITORED BOT (CLIENT GRADE SOLUTION)
echo    - Real-time viewer count monitoring via API
echo    - Progressive scaling up to 100 viewers  
echo    - Verified results with success validation
echo    - Perfect for high-volume client requests
echo ===============================================================================
echo.
call monitored_launcher.bat
goto menu

:api_bot
echo.
echo ===============================================================================
echo    LAUNCHING: SHOPEE API BOT (Direct API Approach)
echo    - Uses official Shopee Live API endpoints
echo    - No browser required - pure API calls
echo    - Maximum reliability for RDP/VPS
echo    - Real viewer count increase
echo ===============================================================================
echo.
call api_launcher.bat
goto menu

:ultra_rdp

REM Verify dependencies
echo [CHECK] Verifying dependencies...
python -c "import selenium, webdriver_manager; print('Dependencies OK')" 2>nul
if errorlevel 1 (
    echo [INSTALL] Installing missing dependencies...
    pip install selenium webdriver-manager requests
)

REM Create necessary directories
if not exist "sessions\real_url_viewers" mkdir sessions\real_url_viewers
if not exist "logs" mkdir logs

echo.
echo Available launch options:
echo 1. Ultra RDP Bot [MAXIMUM OPTIMIZATION] - Ultra-aggressive bypass
echo 2. Device Fingerprint Bot - Advanced device spoofing  
echo 3. Auth Bypass Bot - Authentication bypass only
echo 4. Quick Launch - Ultra RDP optimized
echo.

set /p choice="Select option (1-4): "

if "%choice%"=="1" goto real_url_bot
if "%choice%"=="2" goto device_bot
if "%choice%"=="3" goto auth_bot
if "%choice%"=="4" goto quick_launch
goto real_url_bot

:real_url_bot
echo [LAUNCH] Ultra RDP Bot - Maximum Optimization
echo.
set /p session_id="Enter Shopee Live Session ID: "
if "%session_id%"=="" (
    echo ERROR: Session ID required!
    pause
    exit /b 1
)

set /p viewer_count="Enter viewer count (default 3): "
if "%viewer_count%"=="" set viewer_count=3

echo.
echo Starting Ultra RDP Bot with maximum optimization...
echo Session ID: %session_id%
echo Viewer Count: %viewer_count%
echo Mode: Ultra RDP Headless (GPU Disabled)
echo Bypass: Ultra-aggressive + Emergency methods
echo Expected Mega Boost: %viewer_count% x 500 = %viewer_count%500
echo.

python real_url_bot_ultra.py %session_id% %viewer_count%
goto end

:device_bot
echo [LAUNCH] Device Fingerprint Bot - Advanced device spoofing
echo.
set /p session_id="Enter Shopee Live Session ID: "
if "%session_id%"=="" (
    echo ERROR: Session ID required!
    pause
    exit /b 1
)

set /p device_count="Enter device count (default 3): "
if "%device_count%"=="" set device_count=3

echo.
echo Starting Device Fingerprint Bot...
echo Session ID: %session_id%
echo Device Count: %device_count%
echo.

python device_fingerprint_bot.py %session_id% %device_count%
goto end

:auth_bot
echo [LAUNCH] Auth Bypass Bot - Authentication bypass only
echo.
set /p session_id="Enter Shopee Live Session ID: "
if "%session_id%"=="" (
    echo ERROR: Session ID required!
    pause
    exit /b 1
)

set /p viewer_count="Enter viewer count (default 3): "
if "%viewer_count%"=="" set viewer_count=3

echo.
echo Starting Auth Bypass Bot...
echo Session ID: %session_id%
echo Viewer Count: %viewer_count%
echo.

python auth_bypass_bot.py %session_id% %viewer_count%
goto end

:quick_launch
echo [QUICK] Ultra RDP Quick Launch
echo.
set /p session_id="Enter Shopee Live Session ID: "
if "%session_id%"=="" (
    echo ERROR: Session ID required!
    pause
    exit /b 1
)

echo.
echo Quick launching Ultra RDP Bot with 3 viewers...
echo Session ID: %session_id%
echo Mode: Ultra-aggressive bypass + Mega booster
echo.

python real_url_bot_ultra.py %session_id% 3
goto end

:end
echo.
echo ===============================================================================
echo Bot execution completed.
echo Check logs\ directory for detailed execution logs.
echo.
echo Press any key to exit or run again...
pause >nul

REM Ask if user wants to run again
echo.
set /p again="Run bot again? (y/n): "
if /i "%again%"=="y" goto main
if /i "%again%"=="yes" goto main

exit
