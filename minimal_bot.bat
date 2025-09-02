@echo off
title Shopee Bot - Clean Version
color 0F
cls

echo Shopee Live Viewer Bot - Clean Edition
echo ======================================
echo.

REM Quick Python check
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not installed!
    echo Please install Python from Microsoft Store or python.org
    pause
    exit /b 1
)

echo Python: OK
echo.

REM Simple inputs
set /p session="Session ID (numbers only): "
set /p count="How many viewers (1-20): "
if "%count%"=="" set count=3

echo.
echo Configuration:
echo - Session: %session%
echo - Viewers: %count%
echo - URL: https://live.shopee.co.id/share?from=live^&session=%session%^&in=1
echo.
echo Press any key to start...
pause >nul

cls
echo Starting bot...
echo.

REM Install if needed
python -c "import selenium" >nul 2>&1
if errorlevel 1 (
    echo Installing selenium...
    pip install selenium webdriver-manager
)

REM Create minimal bot
echo import random, string, time > bot.py
echo from selenium import webdriver >> bot.py
echo from selenium.webdriver.chrome.service import Service >> bot.py
echo from selenium.webdriver.chrome.options import Options >> bot.py
echo from webdriver_manager.chrome import ChromeDriverManager >> bot.py
echo. >> bot.py
echo viewers = [] >> bot.py
echo session = "%session%" >> bot.py
echo count = %count% >> bot.py
echo url = f"https://live.shopee.co.id/share?from=live&session={session}&in=1" >> bot.py
echo. >> bot.py
echo for i in range(count): >> bot.py
echo     device_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=32)) >> bot.py
echo     print(f"Starting viewer {i+1} - Device: {device_id[:8]}...") >> bot.py
echo     options = Options() >> bot.py
echo     options.add_argument("--disable-blink-features=AutomationControlled") >> bot.py
echo     service = Service(ChromeDriverManager().install()) >> bot.py
echo     driver = webdriver.Chrome(service=service, options=options) >> bot.py
echo     driver.set_window_size(300, 200) >> bot.py
echo     driver.set_window_position(i*320, 0) >> bot.py
echo     driver.get("https://shopee.co.id") >> bot.py
echo     driver.execute_script(f"localStorage.setItem('device_id', '{device_id}')") >> bot.py
echo     driver.get(url) >> bot.py
echo     viewers.append(driver) >> bot.py
echo     time.sleep(2) >> bot.py
echo. >> bot.py
echo print(f"SUCCESS! {len(viewers)} viewers started for session {session}") >> bot.py
echo print("Check your live stream - viewer count should increase!") >> bot.py
echo input("Press Enter to stop bot...") >> bot.py
echo. >> bot.py
echo for driver in viewers: >> bot.py
echo     try: >> bot.py
echo         driver.quit() >> bot.py
echo     except: >> bot.py
echo         pass >> bot.py

python bot.py
del bot.py

echo.
echo Bot finished!
pause
