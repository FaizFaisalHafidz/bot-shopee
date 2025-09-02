@echo off
title Shopee Professional Bot v2.0
color 0E

cls
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                🤖 SHOPEE PROFESSIONAL BOT v2.0              ║
echo ║                   Device Fingerprint Bypass                 ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Environment check
echo [SYSTEM CHECK]
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found
    echo.
    echo Install options:
    echo 1. Microsoft Store: "Python 3.11"
    echo 2. Direct: https://python.org/downloads
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version') do set PYTHON_VER=%%i
echo ✅ Python %PYTHON_VER%

REM Check Chrome
set CHROME_FOUND=0
if exist "%PROGRAMFILES%\Google\Chrome\Application\chrome.exe" set CHROME_FOUND=1
if exist "%PROGRAMFILES(X86)%\Google\Chrome\Application\chrome.exe" set CHROME_FOUND=1
if exist "%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe" set CHROME_FOUND=1

if %CHROME_FOUND%==0 (
    echo ⚠️ Chrome not found - install from chrome.google.com
) else (
    echo ✅ Chrome detected
)

echo.

REM Configuration
echo [CONFIGURATION]
set /p SESSION_ID="Session ID (e.g. 157658364): "
if "%SESSION_ID%"=="" (
    echo ❌ Session ID required!
    pause
    exit /b 1
)

set /p MAX_VIEWERS="Max viewers (1-20): "
if "%MAX_VIEWERS%"=="" set MAX_VIEWERS=5

set /p DELAY_SEC="Delay between viewers (1-10s): "
if "%DELAY_SEC%"=="" set DELAY_SEC=3

set /p RUN_TIME="Run time in minutes (0=forever): "
if "%RUN_TIME%"=="" set RUN_TIME=30

echo.
echo ✅ Session: %SESSION_ID%
echo ✅ Viewers: %MAX_VIEWERS%  
echo ✅ Delay: %DELAY_SEC%s
echo ✅ Runtime: %RUN_TIME% minutes
echo.

REM Dependencies
echo [DEPENDENCIES]
python -c "import selenium,webdriver_manager,requests" >nul 2>&1
if errorlevel 1 (
    echo 📦 Installing packages...
    python -m pip install selenium webdriver-manager requests --quiet --disable-pip-version-check
    if errorlevel 1 (
        echo ❌ Package installation failed
        pause
        exit /b 1
    )
)
echo ✅ All packages ready

REM Create logs directory
if not exist "logs" mkdir logs

REM Generate timestamp
for /f "tokens=1-3 delims=/ " %%a in ('date /t') do set DATE=%%c-%%a-%%b
for /f "tokens=1-2 delims=: " %%a in ('time /t') do set TIME=%%a-%%b
set TIMESTAMP=%DATE%_%TIME::=-%
set LOG_FILE=logs\bot_%TIMESTAMP%.log

echo.
echo [STARTING BOT]
echo 🚀 Launching %MAX_VIEWERS% viewers...
echo 📝 Log file: %LOG_FILE%
echo.

REM Create and execute Python bot
(
echo import sys,os,time,random,string,json
echo from datetime import datetime
echo.
echo # Logging setup
echo log_file = "%LOG_FILE%"
echo def log^(msg^):
echo     timestamp = datetime.now^(^).strftime^("%%Y-%%m-%%d %%H:%%M:%%S"^)
echo     with open^(log_file, 'a', encoding='utf-8'^) as f:
echo         f.write^(f"[{timestamp}] {msg}\n"^)
echo     print^(f"[{timestamp}] {msg}"^)
echo.
echo try:
echo     from selenium import webdriver
echo     from selenium.webdriver.chrome.service import Service
echo     from selenium.webdriver.chrome.options import Options
echo     from webdriver_manager.chrome import ChromeDriverManager
echo     log^("✅ Selenium imported"^)
echo except ImportError as e:
echo     log^(f"❌ Import error: {e}"^)
echo     input^("Press Enter to exit..."^)
echo     sys.exit^(1^)
echo.
echo def generate_device_id^(^):
echo     return ''.join^(random.choices^(string.ascii_uppercase + string.digits, k=32^)^)
echo.
echo def create_chrome_options^(viewer_num^):
echo     options = Options^(^)
echo     
echo     # Security
echo     options.add_argument^("--no-sandbox"^)
echo     options.add_argument^("--disable-dev-shm-usage"^)
echo     options.add_argument^("--disable-blink-features=AutomationControlled"^)
echo     options.add_experimental_option^("excludeSwitches", ["enable-automation"]^)
echo     options.add_experimental_option^('useAutomationExtension', False^)
echo     
echo     # Random user agents
echo     user_agents = [
echo         "Mozilla/5.0 ^(Windows NT 10.0; Win64; x64^) AppleWebKit/537.36 ^(KHTML, like Gecko^) Chrome/120.0.0.0 Safari/537.36",
echo         "Mozilla/5.0 ^(Windows NT 10.0; Win64; x64^) AppleWebKit/537.36 ^(KHTML, like Gecko^) Chrome/119.0.0.0 Safari/537.36",
echo         "Mozilla/5.0 ^(Windows NT 10.0; Win64; x64^) AppleWebKit/537.36 ^(KHTML, like Gecko^) Chrome/118.0.0.0 Safari/537.36"
echo     ]
echo     options.add_argument^(f"--user-agent={random.choice^(user_agents^)}"^)
echo     
echo     # Window size variation
echo     sizes = [^(1366,768^), ^(1920,1080^), ^(1440,900^), ^(1536,864^)]
echo     width, height = random.choice^(sizes^)
echo     options.add_argument^(f"--window-size={width},{height}"^)
echo     
echo     return options
echo.
echo def inject_device_fingerprint^(driver, device_id^):
echo     script = f"""
echo     // Device ID override
echo     localStorage.setItem^('device_id', '{device_id}'^);
echo     
echo     // Navigator overrides
echo     Object.defineProperty^(navigator, 'deviceMemory', {{
echo         writable: false,
echo         value: {random.choice([2,4,8,16])}
echo     }}^);
echo     
echo     Object.defineProperty^(navigator, 'hardwareConcurrency', {{
echo         writable: false,
echo         value: {random.choice([2,4,6,8,12,16])}  
echo     }}^);
echo     
echo     // Screen overrides
echo     Object.defineProperty^(screen, 'width', {{
echo         writable: false,
echo         value: {random.choice([1920,1366,1440,1536])}
echo     }}^);
echo     
echo     Object.defineProperty^(screen, 'height', {{
echo         writable: false,
echo         value: {random.choice([1080,768,900,864])}
echo     }}^);
echo     
echo     console.log^('🔒 Device fingerprint set:', '{device_id}'^);
echo     """
echo     
echo     try:
echo         driver.execute_cdp_cmd^('Runtime.evaluate', {{'expression': script}}^)
echo         return True
echo     except:
echo         # Fallback to regular execute_script
echo         try:
echo             driver.execute_script^(script^)
echo             return True
echo         except:
echo             return False
echo.
echo # Main execution
echo session_id = "%SESSION_ID%"
echo max_viewers = %MAX_VIEWERS%
echo delay_sec = %DELAY_SEC%
echo run_minutes = %RUN_TIME%
echo.
echo live_url = f"https://live.shopee.co.id/share?from=live&session={session_id}&in=1"
echo.
echo log^(f"🎯 Target: {max_viewers} viewers for session {session_id}"^)
echo log^(f"📺 URL: {live_url}"^)
echo log^(f"⏱️ Runtime: {run_minutes} minutes"^)
echo.
echo viewers = []
echo start_time = time.time^(^)
echo.
echo try:
echo     for i in range^(max_viewers^):
echo         device_id = generate_device_id^(^)
echo         log^(f"🚀 Starting viewer #{i+1} with ID: {device_id[:8]}..."^)
echo         
echo         # Create driver
echo         options = create_chrome_options^(i^)
echo         service = Service^(ChromeDriverManager^(^).install^(^)^)
echo         driver = webdriver.Chrome^(service=service, options=options^)
echo         
echo         # Position windows in grid
echo         x_pos = ^(i %% 4^) * 350
echo         y_pos = ^(i // 4^) * 280
echo         driver.set_window_position^(x_pos, y_pos^)
echo         driver.set_window_size^(400, 300^)
echo         
echo         # Setup fingerprint
echo         driver.get^("https://shopee.co.id"^)
echo         
echo         if inject_device_fingerprint^(driver, device_id^):
echo             log^(f"✅ Fingerprint injected for viewer #{i+1}"^)
echo         else:
echo             log^(f"⚠️ Fingerprint injection failed for viewer #{i+1}"^)
echo         
echo         # Navigate to live
echo         driver.get^(live_url^)
echo         
echo         viewers.append^({
echo             'driver': driver,
echo             'device_id': device_id,
echo             'viewer_num': i + 1,
echo             'start_time': time.time^(^)
echo         }^)
echo         
echo         log^(f"✅ Viewer #{i+1} connected: {device_id}"^)
echo         
echo         # Delay between viewers
echo         if i ^< max_viewers - 1:
echo             time.sleep^(delay_sec^)
echo     
echo     log^(f"🎉 All {len^(viewers^)} viewers started successfully!"^)
echo     
echo     # Summary
echo     log^("📊 VIEWER SUMMARY:"^)
echo     for viewer in viewers:
echo         log^(f"  #{viewer['viewer_num']}: {viewer['device_id']}"^)
echo     
echo     # Keep alive loop
echo     log^("🔥 Bot running! Monitoring viewers..."^)
echo     
echo     end_time = start_time + ^(run_minutes * 60^) if run_minutes ^> 0 else float^('inf'^)
echo     
echo     while time.time^(^) ^< end_time:
echo         time.sleep^(30^)
echo         
echo         active_count = 0
echo         for viewer in viewers:
echo             try:
echo                 viewer['driver'].current_url
echo                 active_count += 1
echo             except:
echo                 pass
echo         
echo         elapsed = int^(^(time.time^(^) - start_time^) / 60^)
echo         log^(f"⚡ Status: {active_count}/{len^(viewers^)} active ^| {elapsed}min runtime"^)
echo     
echo     if run_minutes ^> 0:
echo         log^(f"⏰ Runtime limit reached ^({run_minutes} minutes^)"^)
echo.
echo except KeyboardInterrupt:
echo     log^("🛑 Bot stopped by user"^)
echo except Exception as e:
echo     log^(f"❌ Bot error: {e}"^)
echo     import traceback
echo     log^(f"Traceback: {traceback.format_exc^(^)}"^)
echo finally:
echo     # Cleanup
echo     log^("🧹 Cleaning up viewers..."^)
echo     for i, viewer in enumerate^(viewers^):
echo         try:
echo             viewer['driver'].quit^(^)
echo             log^(f"✅ Viewer #{viewer['viewer_num']} closed"^)
echo         except:
echo             log^(f"⚠️ Error closing viewer #{viewer['viewer_num']}"^)
echo     
echo     runtime = int^(^(time.time^(^) - start_time^) / 60^)
echo     log^(f"📈 Session complete: {len^(viewers^)} viewers, {runtime} minutes runtime"^)
echo     log^(f"📝 Full log saved to: {log_file}"^)
echo.
echo print^("✅ Bot session completed!"^)
echo input^("Press Enter to exit..."^)
) > temp_professional_bot.py

python temp_professional_bot.py

REM Cleanup
del temp_professional_bot.py >nul 2>&1

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                      SESSION COMPLETE                       ║
echo ╚════════════════════════════════════════════════════════════╝
pause
