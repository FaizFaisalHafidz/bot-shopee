@echo off
chcp 65001
cls

echo ===============================================================================
echo    SHOPEE HYBRID COOKIE + API BOT
echo    Cookie Harvesting → API Calls → Real Viewer Boost
echo ===============================================================================
echo.
echo Revolutionary Approach:
echo  🍪 Phase 1: Harvest real session cookies via browser automation
echo  🚀 Phase 2: Use harvested cookies for legitimate API calls  
echo  📈 Result: Real viewer count increase (not manipulation)
echo  🔄 Cookie rotation for up to 100 viewers
echo  ✅ Bypasses all authentication requirements
echo.
echo How it works:
echo  1. Create 10 browser sessions to harvest cookies
echo  2. Extract SPC_U, SPC_ST, SPC_T_ID and other session data
echo  3. Use cookies to make legitimate /joinv2 API calls
echo  4. Rotate cookies for multiple viewers
echo  5. Real viewer count increase!
echo.

set /p session_id="Enter Shopee Live Session ID (e.g., 157888904): "
set /p target_viewers="Enter target viewer count (1-100, default 10): "

if "%target_viewers%"=="" set target_viewers=10

echo.
echo Starting HYBRID COOKIE + API BOT...
echo Session ID: %session_id%
echo Target Viewers: %target_viewers%
echo Method: Cookie Harvesting → API Calls
echo Expected Result: REAL +%target_viewers% viewers via API
echo.

echo [SETUP] Activating virtual environment...
call venv\Scripts\activate

echo [SETUP] Creating cookie harvester directories...
if not exist "sessions\cookie_harvesters" mkdir sessions\cookie_harvesters

echo [SETUP] Installing additional dependencies...
pip install requests uuid

echo.
echo ===============================================================================
echo    SHOPEE HYBRID BOT - EXECUTING COOKIE HARVEST + API CALLS
echo ===============================================================================
echo Target Session: %session_id%
echo Target Viewers: %target_viewers%
echo Phase 1: Cookie Harvesting (up to 10 concurrent harvesters)
echo Phase 2: API Calls with cookie rotation
echo Expected: LEGITIMATE API joins with real session data
echo ===============================================================================
echo.

echo [LAUNCH] Starting hybrid cookie + API bot...
python hybrid_cookie_api_bot.py %session_id% %target_viewers%

echo.
echo ===============================================================================
echo    HYBRID COOKIE + API BOT - SESSION COMPLETED
echo ===============================================================================
echo.
echo Verification Steps:
echo 1. Check viewer count at: https://live.shopee.co.id/%session_id%
echo 2. Or mobile version: https://m.shopee.co.id/live/%session_id%
echo 3. Count should have increased by successful API joins
echo.
echo This method uses REAL session cookies for LEGITIMATE API calls!
echo No fake data - only harvested authentic session information.
echo.
echo Press any key to exit...
pause >nul
