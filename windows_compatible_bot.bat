@echo off
title Shopee Bot - Windows Compatible
color 0A
chcp 437 >nul

cls
echo.
echo ========================================
echo       SHOPEE LIVE VIEWER BOT
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found!
    echo.
    echo Install Python from:
    echo 1. Microsoft Store: Search "Python 3.11"
    echo 2. https://python.org/downloads
    echo.
    pause
    exit /b 1
)

echo [OK] Python found!
python --version
echo.

REM Get configuration
echo ========================================
echo         CONFIGURATION SETUP
echo ========================================
echo.

set /p SESSION="Shopee session ID (default: 157658364): "
if "%SESSION%"=="" set SESSION=157658364

set /p VIEWERS="Number of viewers (default: 3): "
if "%VIEWERS%"=="" set VIEWERS=3

set /p DELAY="Delay between viewers in seconds (default: 2): "
if "%DELAY%"=="" set DELAY=2

echo.
echo [CONFIG] Session: %SESSION%
echo [CONFIG] Viewers: %VIEWERS%
echo [CONFIG] Delay: %DELAY%s
echo [CONFIG] URL: https://live.shopee.co.id/share?from=live^&session=%SESSION%^&in=1
echo.

REM Install dependencies
echo ========================================
echo       INSTALLING DEPENDENCIES
echo ========================================
echo.

python -c "import selenium" >nul 2>&1 || (
    echo [INSTALL] Installing selenium...
    python -m pip install selenium --quiet
)

python -c "import webdriver_manager" >nul 2>&1 || (
    echo [INSTALL] Installing webdriver-manager...
    python -m pip install webdriver-manager --quiet
)

python -c "import requests" >nul 2>&1 || (
    echo [INSTALL] Installing requests...
    python -m pip install requests --quiet
)

echo [OK] All dependencies ready!
echo.

REM Create and run bot
echo ========================================
echo           STARTING BOT
echo ========================================
echo.

echo [INFO] Creating %VIEWERS% viewers...
echo [INFO] Each viewer will have unique device fingerprint
echo.

python -c "
import os, sys, time, random, string
from datetime import datetime

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager
except ImportError:
    print('[ERROR] Failed to import selenium')
    input('Press Enter to exit...')
    sys.exit(1)

def generate_device_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=32))

def create_chrome_options():
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    
    # Random user agent
    agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    ]
    options.add_argument(f'--user-agent={random.choice(agents)}')
    return options

def inject_fingerprint(driver, device_id):
    script = f\"\"\"
    localStorage.setItem('device_id', '{device_id}');
    Object.defineProperty(navigator, 'deviceMemory', {{value: {random.choice([4,8,16])}}});
    Object.defineProperty(navigator, 'hardwareConcurrency', {{value: {random.choice([4,8,12])}}});
    console.log('Device ID:', '{device_id}');
    \"\"\"
    try:
        driver.execute_script(script)
        print(f'[OK] Device fingerprint set: {device_id[:8]}...')
        return True
    except Exception as e:
        print(f'[ERROR] Fingerprint failed: {e}')
        return False

# Main execution
session_id = '%SESSION%'
max_viewers = int('%VIEWERS%')
delay = int('%DELAY%')

live_url = f'https://live.shopee.co.id/share?from=live&session={session_id}&in=1'
print(f'[TARGET] {max_viewers} viewers for session {session_id}')
print(f'[URL] {live_url}')
print()

viewers = []

try:
    for i in range(max_viewers):
        device_id = generate_device_id()
        print(f'[START] Viewer #{i+1}...')
        
        # Create Chrome driver
        options = create_chrome_options()
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        # Position window
        x = (i %% 3) * 400
        y = (i // 3) * 300
        driver.set_window_position(x, y)
        driver.set_window_size(400, 300)
        
        # Setup and navigate
        driver.get('https://shopee.co.id')
        time.sleep(1)
        
        if inject_fingerprint(driver, device_id):
            driver.get(live_url)
            viewers.append({
                'driver': driver, 
                'device_id': device_id, 
                'num': i+1
            })
            print(f'[SUCCESS] Viewer #{i+1} connected!')
        else:
            print(f'[WARNING] Viewer #{i+1} fingerprint setup failed')
            driver.quit()
        
        if i < max_viewers - 1:
            time.sleep(delay)
    
    print()
    print(f'[COMPLETE] {len(viewers)} viewers active!')
    print()
    print('DEVICE IDs:')
    for v in viewers:
        print(f'  Viewer #{v[\"num\"]}: {v[\"device_id\"]}')
    
    print()
    print('[RUNNING] Bot active! Press Ctrl+C to stop...')
    print('[INFO] Check live stream - viewer count should increase!')
    
    # Monitor loop
    while True:
        time.sleep(30)
        active = 0
        for v in viewers:
            try:
                v['driver'].current_url
                active += 1
            except:
                pass
        
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f'[{timestamp}] Status: {active}/{len(viewers)} viewers active')

except KeyboardInterrupt:
    print()
    print('[STOP] Stopping bot...')
except Exception as e:
    print(f'[ERROR] Bot failed: {e}')
finally:
    for v in viewers:
        try:
            v['driver'].quit()
        except:
            pass
    print('[CLEANUP] All viewers closed')
    print('[COMPLETE] Bot session finished')
"

echo.
echo ========================================
echo           SESSION COMPLETE
echo ========================================
echo.
pause
