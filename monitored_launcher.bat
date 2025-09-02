@echo off
chcp 65001
cls

echo ===============================================================================
echo    SHOPEE MONITORED BOT - CLIENT GRADE SOLUTION
echo    Real-time monitoring + Progressive scaling up to 100 viewers
echo ===============================================================================
echo.
echo Features:
echo  🔍 Real-time viewer count monitoring via API
echo  📈 Progressive scaling: 10 → 25 → 50 → 100 viewers
echo  ✅ Success validation and reporting
echo  🔄 Auto health-check and maintenance
echo  📊 Detailed progress tracking
echo.

set /p session_id="Enter Shopee Live Session ID (e.g., 157878290): "
set /p target_viewers="Enter target viewer count (1-100, default 10): "

if "%target_viewers%"=="" set target_viewers=10

echo.
echo Starting MONITORED BOT for client-grade results...
echo Session ID: %session_id%
echo Target Viewers: %target_viewers%
echo Mode: Progressive Scaling + Real-time Monitoring
echo Expected Result: Verified %target_viewers% viewers added
echo.

echo [SETUP] Activating virtual environment...
call venv\Scripts\activate

echo.
echo ===============================================================================
echo    SHOPEE MONITORED BOT - STARTING PROGRESSIVE SCALING
echo ===============================================================================
echo Target Session: %session_id%
echo Target Viewers: %target_viewers%
echo Progressive Stages: 10 → 25 → 50 → %target_viewers%
echo Real-time Monitoring: ENABLED
echo ===============================================================================
echo.

echo [LAUNCH] Starting monitored bot with real-time tracking...
python monitored_bot.py %session_id% %target_viewers%

echo.
echo [INFO] Monitored bot session ended.
echo Check the monitoring logs above for detailed results.
echo.
echo Press any key to exit...
pause >nul
