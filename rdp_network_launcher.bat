@echo off
chcp 65001
cls

echo ===============================================================================
echo    SHOPEE RDP BOT V2 - NETWORK RESILIENT VERSION
echo    Enhanced network fallbacks + DNS resolution fixes
echo ===============================================================================
echo.
echo Network Enhancements:
echo  🌐 Multiple domain fallbacks (shopee.co.id, m.shopee.co.id, www.shopee.co.id)
echo  🔄 5 retry attempts with progressive wait times
echo  📡 Base domain testing before live URL access
echo  🛡️ DNS resolution error handling
echo  📱 Multiple URL format testing
echo  ✅ Partial success tolerance (keep working viewers)
echo.

echo [DIAGNOSTIC] Testing network connectivity...
ping -n 1 shopee.co.id >nul 2>&1
if %errorlevel%==0 (
    echo ✅ shopee.co.id - REACHABLE
) else (
    echo ❌ shopee.co.id - DNS ISSUE DETECTED
)

ping -n 1 m.shopee.co.id >nul 2>&1
if %errorlevel%==0 (
    echo ✅ m.shopee.co.id - REACHABLE
) else (
    echo ❌ m.shopee.co.id - DNS ISSUE DETECTED
)

ping -n 1 www.shopee.co.id >nul 2>&1
if %errorlevel%==0 (
    echo ✅ www.shopee.co.id - REACHABLE
) else (
    echo ❌ www.shopee.co.id - DNS ISSUE DETECTED
)

echo.

set /p session_id="Enter Shopee Live Session ID (e.g., 157878290): "
set /p viewer_count="Enter viewer count (1-10, default 3): "

if "%viewer_count%"=="" set viewer_count=3

echo.
echo Starting NETWORK RESILIENT RDP BOT...
echo Session ID: %session_id%
echo Viewer Count: %viewer_count%
echo Mode: Network Resilient + Multiple Fallbacks
echo DNS Handling: Enhanced with 3 domain fallbacks
echo Expected Result: Maximum possible viewers (target %viewer_count%)
echo.

echo [SETUP] Activating virtual environment...
call venv\Scripts\activate

echo [SETUP] Creating RDP profile directories...
if not exist "sessions\rdp_profiles" mkdir sessions\rdp_profiles

echo.
echo ===============================================================================
echo    SHOPEE RDP BOT V2 - EXECUTING WITH NETWORK RESILIENCE
echo ===============================================================================
echo Target Session: %session_id%
echo Viewer Count: %viewer_count%
echo Network Strategy: Multi-domain fallback with 5 retry attempts
echo Success Tolerance: Partial success accepted
echo ===============================================================================
echo.

echo [LAUNCH] Starting network resilient bot...
python rdp_optimized_bot.py %session_id% %viewer_count%

echo.
echo ===============================================================================
echo    NETWORK RESILIENT RDP BOT - SESSION COMPLETED
echo ===============================================================================
echo.
echo Results Summary:
echo - Check active viewers at: https://live.shopee.co.id/%session_id%
echo - Or try: https://m.shopee.co.id/live/%session_id%
echo - Or try: https://shopee.co.id/live/%session_id%
echo.
echo Even if some viewers failed due to network issues,
echo the successful ones should be boosting your viewer count!
echo.
echo Keep this window open to maintain active sessions!
echo Press Ctrl+C to stop and cleanup all viewers.
echo.
pause
