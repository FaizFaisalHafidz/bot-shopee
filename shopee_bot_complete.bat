@echo off
title Shopee Live Viewer Bot - BAT Version
color 0A

echo.
echo ████████████████████████████████████████████████
echo    🤖 SHOPEE LIVE VIEWER BOT - BAT VERSION 
echo ████████████████████████████████████████████████
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python first.
    echo.
    echo Quick install options:
    echo 1. Microsoft Store: Search "Python 3.11"
    echo 2. Direct: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo ✅ Python found!
python --version

REM Get session info
echo.
echo ═══════════════════════════════════════════════════
echo    📺 SHOPEE LIVE SESSION SETUP
echo ═══════════════════════════════════════════════════
echo.

set /p SESSION_ID="Enter Shopee Live session ID (e.g. 157658364): "
if "%SESSION_ID%"=="" set SESSION_ID=157658364

set /p MAX_VIEWERS="Number of viewers (1-20): "
if "%MAX_VIEWERS%"=="" set MAX_VIEWERS=5

set /p DELAY="Delay between viewers in seconds (1-10): "
if "%DELAY%"=="" set DELAY=3

echo.
echo ✅ Session ID: %SESSION_ID%
echo ✅ Max Viewers: %MAX_VIEWERS%
echo ✅ Delay: %DELAY% seconds
echo ✅ Live URL: https://live.shopee.co.id/share?from=live^&session=%SESSION_ID%^&in=1
echo.

REM Install packages if needed
echo ═══════════════════════════════════════════════════
echo    📦 CHECKING DEPENDENCIES
echo ═══════════════════════════════════════════════════
echo.

python -c "import selenium" >nul 2>&1
if errorlevel 1 (
    echo 📦 Installing selenium...
    python -m pip install selenium --quiet
)

python -c "import webdriver_manager" >nul 2>&1
if errorlevel 1 (
    echo 📦 Installing webdriver-manager...
    python -m pip install webdriver-manager --quiet
)

python -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo 📦 Installing requests...
    python -m pip install requests --quiet
)

echo ✅ All dependencies ready!

REM Create Python bot script on-the-fly
echo.
echo ═══════════════════════════════════════════════════
echo    🔧 GENERATING BOT SCRIPT
echo ═══════════════════════════════════════════════════

echo Creating temporary bot script...

(
echo import os
echo import sys
echo import time
echo import random
echo import string
echo import json
echo from datetime import datetime
echo.
echo try:
echo     from selenium import webdriver
echo     from selenium.webdriver.chrome.service import Service
echo     from selenium.webdriver.chrome.options import Options
echo     from webdriver_manager.chrome import ChromeDriverManager
echo     from selenium.webdriver.common.by import By
echo     from selenium.webdriver.support.ui import WebDriverWait
echo     from selenium.webdriver.support import expected_conditions as EC
echo except ImportError as e:
echo     print^(f"Import error: {e}"^)
echo     input^("Press Enter to exit..."^)
echo     sys.exit^(1^)
echo.
echo def generate_device_id^(^):
echo     """Generate unique 32-character device ID"""
echo     return ''.join^(random.choices^(string.ascii_uppercase + string.digits, k=32^)^)
echo.
echo def create_chrome_options^(profile_num=0^):
echo     """Create Chrome options with fingerprint protection"""
echo     options = Options^(^)
echo     
echo     # Basic options
echo     options.add_argument^("--no-sandbox"^)
echo     options.add_argument^("--disable-dev-shm-usage"^)
echo     options.add_argument^("--disable-blink-features=AutomationControlled"^)
echo     options.add_experimental_option^("excludeSwitches", ["enable-automation"]^)
echo     options.add_experimental_option^('useAutomationExtension', False^)
echo     
echo     # Random user agent
echo     user_agents = [
echo         "Mozilla/5.0 ^(Windows NT 10.0; Win64; x64^) AppleWebKit/537.36 ^(KHTML, like Gecko^) Chrome/120.0.0.0 Safari/537.36",
echo         "Mozilla/5.0 ^(Windows NT 10.0; Win64; x64^) AppleWebKit/537.36 ^(KHTML, like Gecko^) Chrome/119.0.0.0 Safari/537.36",
echo         "Mozilla/5.0 ^(Macintosh; Intel Mac OS X 10_15_7^) AppleWebKit/537.36 ^(KHTML, like Gecko^) Chrome/120.0.0.0 Safari/537.36"
echo     ]
echo     options.add_argument^(f"--user-agent={random.choice^(user_agents^)}"^)
echo     
echo     # Random window size
echo     widths = [1366, 1920, 1440, 1536]
echo     heights = [768, 1080, 900, 864]
echo     width = random.choice^(widths^)
echo     height = random.choice^(heights^)
echo     options.add_argument^(f"--window-size={width},{height}"^)
echo     
echo     return options
echo.
echo def inject_device_fingerprint^(driver, device_id^):
echo     """Inject device fingerprint manipulation script"""
echo     
echo     script = f"""
echo     // Override localStorage device_id
echo     const originalSetItem = localStorage.setItem;
echo     const originalGetItem = localStorage.getItem;
echo     
echo     localStorage.setItem = function^(key, value^) {{
echo         if ^(key === 'device_id' ^|^| key.includes^('device'^)^) {{
echo             console.log^('Setting device_id to: {device_id}'^);
echo             return originalSetItem.call^(this, key, '{device_id}'^);
echo         }}
echo         return originalSetItem.call^(this, key, value^);
echo     }};
echo     
echo     localStorage.getItem = function^(key^) {{
echo         if ^(key === 'device_id' ^|^| key.includes^('device'^)^) {{
echo             console.log^('Getting device_id: {device_id}'^);
echo             return '{device_id}';
echo         }}
echo         return originalGetItem.call^(this, key^);
echo     }};
echo     
echo     // Set device_id immediately
echo     localStorage.setItem^('device_id', '{device_id}'^);
echo     
echo     // Override navigator properties
echo     Object.defineProperty^(navigator, 'deviceMemory', {{
echo         writable: false,
echo         value: {random.choice([2, 4, 8, 16])}
echo     }}^);
echo     
echo     Object.defineProperty^(navigator, 'hardwareConcurrency', {{
echo         writable: false,
echo         value: {random.choice([2, 4, 6, 8, 12, 16])}
echo     }}^);
echo     
echo     // Override screen properties
echo     Object.defineProperty^(screen, 'width', {{
echo         writable: false,
echo         value: {random.choice([1920, 1366, 1440, 1536])}
echo     }}^);
echo     
echo     Object.defineProperty^(screen, 'height', {{
echo         writable: false,
echo         value: {random.choice([1080, 768, 900, 864])}
echo     }}^);
echo     
echo     console.log^('Device fingerprint injected for: {device_id}'^);
echo     """
echo     
echo     try:
echo         driver.execute_cdp_cmd^('Runtime.evaluate', {{
echo             'expression': script
echo         }}^)
echo         print^(f"✅ Device fingerprint injected: {device_id[:8]}..."^)
echo     except Exception as e:
echo         print^(f"⚠️ Fingerprint injection failed: {e}"^)
echo.
echo def main^(^):
echo     session_id = "%SESSION_ID%"
echo     max_viewers = %MAX_VIEWERS%
echo     delay = %DELAY%
echo     
echo     print^(f"🎯 Starting {max_viewers} viewers for session {session_id}"^)
echo     
echo     live_url = f"https://live.shopee.co.id/share?from=live&session={session_id}&in=1"
echo     print^(f"📺 Live URL: {live_url}"^)
echo     print^(^)
echo     
echo     drivers = []
echo     
echo     try:
echo         for i in range^(max_viewers^):
echo             device_id = generate_device_id^(^)
echo             
echo             print^(f"🚀 Starting viewer #{i+1} with device_id: {device_id[:8]}..."^)
echo             
echo             # Create Chrome options
echo             chrome_options = create_chrome_options^(i^)
echo             
echo             # Create driver
echo             service = Service^(ChromeDriverManager^(^).install^(^)^)
echo             driver = webdriver.Chrome^(service=service, options=chrome_options^)
echo             
echo             # Set window position ^(staggered^)
echo             x_pos = ^(i %% 4^) * 350
echo             y_pos = ^(i // 4^) * 300
echo             driver.set_window_position^(x_pos, y_pos^)
echo             driver.set_window_size^(400, 300^)
echo             
echo             # Navigate to Shopee first
echo             driver.get^("https://shopee.co.id"^)
echo             time.sleep^(1^)
echo             
echo             # Inject device fingerprint
echo             inject_device_fingerprint^(driver, device_id^)
echo             
echo             # Navigate to live stream
echo             driver.get^(live_url^)
echo             
echo             drivers.append^(^{
echo                 'driver': driver,
echo                 'device_id': device_id,
echo                 'viewer_num': i + 1
echo             }^)
echo             
echo             print^(f"✅ Viewer #{i+1} connected with device ID: {device_id}"^)
echo             
echo             # Delay between viewers
echo             if i ^< max_viewers - 1:
echo                 print^(f"⏱️ Waiting {delay} seconds before next viewer..."^)
echo                 time.sleep^(delay^)
echo         
echo         print^(f"🎉 All {len^(drivers^)} viewers started successfully!"^)
echo         print^(^)
echo         print^("📊 VIEWER SUMMARY:"^)
echo         print^("-" * 50^)
echo         
echo         for viewer_info in drivers:
echo             print^(f"Viewer #{viewer_info['viewer_num']}: {viewer_info['device_id']}"^)
echo         
echo         print^(^)
echo         print^("🔥 Bot is running! Press Ctrl+C to stop..."^)
echo         print^("💡 Check Shopee live stream - viewer count should increase!"^)
echo         
echo         # Keep alive
echo         while True:
echo             time.sleep^(30^)
echo             active_count = 0
echo             for viewer_info in drivers:
echo                 try:
echo                     viewer_info['driver'].current_url
echo                     active_count += 1
echo                 except:
echo                     pass
echo             
echo             timestamp = datetime.now^(^).strftime^("%H:%M:%S"^)
echo             print^(f"[{timestamp}] ⚡ {active_count}/{len^(drivers^)} viewers active"^)
echo             
echo     except KeyboardInterrupt:
echo         print^("\\n🛑 Stopping bot..."^)
echo         
echo         for i, viewer_info in enumerate^(drivers^):
echo             try:
echo                 viewer_info['driver'].quit^(^)
echo                 print^(f"✅ Viewer #{viewer_info['viewer_num']} closed"^)
echo             except:
echo                 pass
echo         
echo         print^("🧹 All viewers closed. Bot stopped."^)
echo         
echo     except Exception as e:
echo         print^(f"❌ Bot error: {e}"^)
echo         import traceback
echo         traceback.print_exc^(^)
echo         
echo         # Clean up on error
echo         for viewer_info in drivers:
echo             try:
echo                 viewer_info['driver'].quit^(^)
echo             except:
echo                 pass
echo     
echo     print^("Bot session completed."^)
echo     input^("Press Enter to exit..."^)
echo.
echo if __name__ == "__main__":
echo     main^(^)
) > temp_shopee_bot.py

REM Run the bot
echo.
echo ═══════════════════════════════════════════════════
echo    🚀 LAUNCHING SHOPEE BOT
echo ═══════════════════════════════════════════════════
echo.

python temp_shopee_bot.py

REM Cleanup
if exist temp_shopee_bot.py del temp_shopee_bot.py

echo.
echo ═══════════════════════════════════════════════════
echo    ✅ BOT SESSION COMPLETE
echo ═══════════════════════════════════════════════════
pause
