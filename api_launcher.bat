@echo off
chcp 65001
cls

echo ===============================================================================
echo    SHOPEE LIVE API BOT - DIRECT API APPROACH
echo    Ultra-reliable viewer boost using real API endpoints
echo ===============================================================================
echo.
echo This bot uses Shopee's official API endpoints to join live sessions
echo - No browser automation required
echo - Direct API calls for maximum reliability  
echo - Real viewer count increase (not manipulation)
echo - Works perfectly on RDP/VPS environments
echo.

set /p session_id="Enter Shopee Live Session ID (e.g., 157658364): "
set /p viewer_count="Enter viewer count (default 5): "

if "%viewer_count%"=="" set viewer_count=5

echo.
echo Starting API Bot with real viewer boost...
echo Session ID: %session_id%
echo Viewer Count: %viewer_count%
echo Mode: Direct API Calls
echo Method: POST to /api/v1/session/%session_id%/joinv2
echo Expected REAL Boost: +%viewer_count% genuine viewers
echo.

echo [SETUP] Activating virtual environment...
call venv\Scripts\activate

echo.
echo ================================================================================
echo    SHOPEE LIVE API BOT - EXECUTING
echo    Using official Shopee Live API endpoints
echo ================================================================================
echo Target Session: %session_id%
echo Viewer Count: %viewer_count%
echo API Endpoint: https://live.shopee.co.id/api/v1/session/%session_id%/joinv2
echo Expected Result: Real viewer count increase
echo ================================================================================
echo.

echo [LAUNCH] Starting API bot...
python shopee_api_bot.py %session_id% %viewer_count%

echo.
echo [INFO] API Bot session completed.
echo Check your live stream - the viewer count should have increased!
echo.
echo Press any key to exit...
pause >nul
