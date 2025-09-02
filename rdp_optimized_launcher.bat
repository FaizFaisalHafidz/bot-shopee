@echo off
chcp 65001
cls

echo ===============================================================================
echo    SHOPEE RDP BOT - MAXIMUM RDP OPTIMIZATION
echo    Fixed ChromeDriver permissions + Complete GPU disabling
echo ===============================================================================
echo.
echo RDP Optimizations:
echo  🔧 ChromeDriver permission fixes
echo  🚫 Complete GPU disabling (no WebGL/3D)
echo  🌐 Network error resilience  
echo  💾 Memory optimization for RDP
echo  📱 Simple URL navigation
echo  ✅ Manual verification support
echo.

set /p session_id="Enter Shopee Live Session ID (e.g., 157878290): "
set /p viewer_count="Enter viewer count (1-20, default 3): "

if "%viewer_count%"=="" set viewer_count=3

echo.
echo Starting RDP-OPTIMIZED BOT...
echo Session ID: %session_id%
echo Viewer Count: %viewer_count%
echo Mode: RDP Headless + Network Resilient
echo GPU: COMPLETELY DISABLED
echo Expected Result: %viewer_count% active viewers
echo.

echo [SETUP] Activating virtual environment...
call venv\Scripts\activate

echo [SETUP] Creating RDP profile directories...
if not exist "sessions\rdp_profiles" mkdir sessions\rdp_profiles

echo.
echo ===============================================================================
echo    SHOPEE RDP BOT - EXECUTING WITH MAXIMUM OPTIMIZATION
echo ===============================================================================
echo Target Session: %session_id%
echo Viewer Count: %viewer_count%
echo ChromeDriver: Permission fixes applied
echo GPU: Completely disabled for RDP
echo Monitoring: Manual verification
echo ===============================================================================
echo.

echo [LAUNCH] Starting RDP-optimized bot...
python rdp_optimized_bot.py %session_id% %viewer_count%

echo.
echo ===============================================================================
echo    RDP BOT SESSION COMPLETED
echo ===============================================================================
echo.
echo Manual verification steps:
echo 1. Open: https://live.shopee.co.id/%session_id%
echo 2. Check if viewer count increased
echo 3. If successful, you should see +%viewer_count% viewers
echo.
echo Keep this window open to maintain active sessions!
echo Press Ctrl+C to stop and cleanup all viewers.
echo.
pause
