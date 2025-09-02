@echo off
title Shopee Live Viewer Bot
color 0A
cls

echo.
echo ==========================================
echo        SHOPEE LIVE VIEWER BOT v2.0
echo ==========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo.
    echo Please install Python:
    echo 1. Microsoft Store - Search "Python 3.11"
    echo 2. https://python.org/downloads
    echo    - Check "Add Python to PATH" during install
    echo.
    pause
    exit /b 1
)

echo SUCCESS: Python detected
python --version
echo.

REM Get inputs
echo ==========================================
echo              CONFIGURATION
echo ==========================================
echo.

set /p session="Enter Shopee Live session ID: "
if "%session%"=="" (
    echo ERROR: Session ID required!
    pause
    exit /b 1
)

set /p viewers="Number of viewers to create: "
if "%viewers%"=="" set viewers=5

set /p delay="Delay between viewers (seconds): "
if "%delay%"=="" set delay=2

echo.
echo CONFIGURATION:
echo - Session ID: %session%
echo - Viewers: %viewers%
echo - Delay: %delay% seconds
echo - URL: https://live.shopee.co.id/share?from=live^&session=%session%^&in=1
echo.

REM Confirm
set /p confirm="Start bot? (y/n): "
if /i not "%confirm%"=="y" (
    echo Cancelled.
    pause
    exit /b 0
)

echo.
echo ==========================================
echo              STARTING BOT
echo ==========================================
echo.

REM Check/install dependencies
python -c "import selenium,webdriver_manager" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    python -m pip install selenium webdriver-manager requests --quiet
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

echo Dependencies ready.
echo.

REM Create Python script and execute
(
echo import sys, time, random, string
echo try:
echo     from selenium import webdriver
echo     from selenium.webdriver.chrome.service import Service
echo     from selenium.webdriver.chrome.options import Options
echo     from webdriver_manager.chrome import ChromeDriverManager
echo except ImportError as e:
echo     print^(f"Import error: {e}"^)
echo     input^("Press Enter to exit..."^)
echo     sys.exit^(1^)
echo.
echo def generate_device_id^(^):
echo     return ''.join^(random.choices^(string.ascii_uppercase + string.digits, k=32^)^)
echo.
echo def setup_chrome^(^):
echo     options = Options^(^)
echo     options.add_argument^("--no-sandbox"^)
echo     options.add_argument^("--disable-dev-shm-usage"^)
echo     options.add_argument^("--disable-blink-features=AutomationControlled"^)
echo     options.add_experimental_option^("excludeSwitches", ["enable-automation"]^)
echo     options.add_experimental_option^('useAutomationExtension', False^)
echo     return options
echo.
echo def inject_device_id^(driver, device_id^):
echo     script = f"localStorage.setItem^('device_id', '{device_id}'^); console.log^('Device ID set:', '{device_id}'^);"
echo     try:
echo         driver.execute_script^(script^)
echo         return True
echo     except:
echo         return False
echo.
echo session_id = "%session%"
echo max_viewers = %viewers%
echo delay_sec = %delay%
echo.
echo live_url = f"https://live.shopee.co.id/share?from=live&session={session_id}&in=1"
echo print^(f"Target: {max_viewers} viewers for session {session_id}"^)
echo print^(f"URL: {live_url}"^)
echo print^(^)
echo.
echo viewers = []
echo.
echo try:
echo     for i in range^(max_viewers^):
echo         device_id = generate_device_id^(^)
echo         print^(f"Starting viewer #{i+1} with device ID: {device_id[:8]}..."^)
echo         
echo         options = setup_chrome^(^)
echo         service = Service^(ChromeDriverManager^(^).install^(^)^)
echo         driver = webdriver.Chrome^(service=service, options=options^)
echo         
echo         x_pos = ^(i %% 4^) * 300
echo         y_pos = ^(i // 4^) * 250
echo         driver.set_window_position^(x_pos, y_pos^)
echo         driver.set_window_size^(350, 250^)
echo         
echo         driver.get^("https://shopee.co.id"^)
echo         
echo         if inject_device_id^(driver, device_id^):
echo             print^(f"  Device fingerprint injected: {device_id}"^)
echo         else:
echo             print^(f"  Warning: Fingerprint injection failed"^)
echo         
echo         driver.get^(live_url^)
echo         viewers.append^({'driver': driver, 'device_id': device_id, 'num': i+1}^)
echo         
echo         print^(f"  Viewer #{i+1} connected successfully!"^)
echo         
echo         if i ^< max_viewers - 1:
echo             time.sleep^(delay_sec^)
echo     
echo     print^(f"\\nALL {len^(viewers^)} VIEWERS STARTED SUCCESSFULLY!"^)
echo     print^("\\nDEVICE IDs:"^)
echo     for viewer in viewers:
echo         print^(f"  Viewer #{viewer['num']}: {viewer['device_id']}"^)
echo     
echo     print^("\\nBot is running! Check your live stream - viewer count should increase!"^)
echo     print^("Press Ctrl+C to stop the bot..."^)
echo     
echo     while True:
echo         time.sleep^(60^)
echo         active_count = sum^(1 for v in viewers if v['driver'].window_handles^)
echo         print^(f"Status: {active_count}/{len^(viewers^)} viewers still active"^)
echo         
echo except KeyboardInterrupt:
echo     print^("\\nStopping bot..."^)
echo except Exception as e:
echo     print^(f"\\nError: {e}"^)
echo finally:
echo     for viewer in viewers:
echo         try:
echo             viewer['driver'].quit^(^)
echo         except:
echo             pass
echo     print^("All viewers closed. Bot stopped."^)
) > temp_bot.py

python temp_bot.py
del temp_bot.py >nul 2>&1

echo.
echo ==========================================
echo              BOT FINISHED
echo ==========================================
echo.
pause
