@echo off
title Shopee Bot - Simple BAT Version
color 0B

cls
echo.
echo     ========================================
echo            SHOPEE LIVE VIEWER BOT
echo     ========================================
echo.

REM Quick Python check
python --version >nul 2>&1 || (
    echo X Python not found! 
    echo.
    echo Install Python from:
    echo - Microsoft Store: Search "Python 3.11"
    echo - python.org/downloads
    echo.
    pause
    exit /b 1
)

echo [OK] Python ready!
echo.

REM Get user input
echo +---------------------------------------+
echo ^|           SETUP CONFIGURATION        ^|
echo +---------------------------------------+
echo.

set /p SESSION="[INPUT] Shopee session ID: "
if "%SESSION%"=="" set SESSION=157658364

set /p VIEWERS="[INPUT] Number of viewers (1-10): "
if "%VIEWERS%"=="" set VIEWERS=3

set /p WAIT="[INPUT] Delay between viewers (seconds): "
if "%WAIT%"=="" set WAIT=2

echo.
echo +---------------------------------------+
echo ^|            STARTING BOT...           ^|
echo +---------------------------------------+
echo.
echo [TARGET] %VIEWERS% viewers for session %SESSION%
echo [URL] https://live.shopee.co.id/share?from=live^&session=%SESSION%^&in=1
echo.

REM Install dependencies quietly
python -c "import selenium" >nul 2>&1 || python -m pip install selenium webdriver-manager requests --quiet

REM Create and run inline Python script
python -c "
import os, sys, time, random, string
from datetime import datetime

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service  
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager
except ImportError:
    print('Installing selenium...')
    os.system('python -m pip install selenium webdriver-manager --quiet')
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options  
    from webdriver_manager.chrome import ChromeDriverManager

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
    console.log('Device ID set:', '{device_id}');
    \"\"\"
    try:
        driver.execute_script(script)
        print(f'✅ Viewer setup: {device_id[:8]}...')
    except:
        print('⚠️ Fingerprint setup failed')

# Main bot logic  
session_id = '%SESSION%'
max_viewers = int('%VIEWERS%')
delay = int('%WAIT%')

live_url = f'https://live.shopee.co.id/share?from=live&session={session_id}&in=1'
drivers = []

try:
    for i in range(max_viewers):
        device_id = generate_device_id()
        print(f'🚀 Starting viewer #{i+1}...')
        
        # Create Chrome driver
        options = create_chrome_options()
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        # Position window
        x = (i %% 3) * 400
        y = (i // 3) * 300  
        driver.set_window_position(x, y)
        driver.set_window_size(400, 300)
        
        # Setup fingerprint and navigate
        driver.get('https://shopee.co.id')
        inject_fingerprint(driver, device_id)
        driver.get(live_url)
        
        drivers.append({'driver': driver, 'id': device_id, 'num': i+1})
        print(f'✅ Viewer #{i+1} connected!')
        
        if i < max_viewers - 1:
            time.sleep(delay)
    
    print(f'\\n🎉 {len(drivers)} viewers active!')
    print('📊 Device IDs:')
    for d in drivers:
        print(f'  #{d[\"num\"]}: {d[\"id\"]}')
    
    print('\\n🔥 Bot running! Press Ctrl+C to stop')
    print('💡 Check live stream - viewer count should increase!')
    
    while True:
        time.sleep(30)
        active = sum(1 for d in drivers if d['driver'].window_handles)
        print(f'[{datetime.now().strftime(\"%H:%M:%S\")}] ⚡ {active}/{len(drivers)} active')

except KeyboardInterrupt:
    print('\\n🛑 Stopping bot...')
except Exception as e:
    print(f'❌ Error: {e}')
finally:
    for d in drivers:
        try:
            d['driver'].quit()
        except:
            pass
    print('✅ All viewers closed')
"

echo.
echo ┌─────────────────────────────────────────┐
echo │              BOT FINISHED               │
echo └─────────────────────────────────────────┘
echo.
pause
