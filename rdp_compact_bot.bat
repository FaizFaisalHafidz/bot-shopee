@echo off
chcp 437 >nul
title Shopee Bot RDP
color 02
cls

echo SHOPEE LIVE VIEWER BOT - RDP EDITION
echo ====================================
echo.

python --version >nul 2>&1 || (echo ERROR: Install Python from Microsoft Store & pause & exit /b 1)

set /p s="Session ID: "
set /p n="Viewers (default 5): "
if "%n%"=="" set n=5

echo.
echo Starting %n% viewers for session %s%...
echo URL: https://live.shopee.co.id/share?from=live^&session=%s%^&in=1
echo.

python -c "import selenium" >nul 2>&1 || pip install selenium webdriver-manager

(
echo import random,string,time
echo from selenium import webdriver
echo from selenium.webdriver.chrome.service import Service  
echo from selenium.webdriver.chrome.options import Options
echo from webdriver_manager.chrome import ChromeDriverManager
echo viewers=[]
echo for i in range^(%n%^):
echo  device=''.join^(random.choices^(string.ascii_uppercase+string.digits,k=32^)^)
echo  print^(f'Viewer {i+1} starting - Device: {device[:8]}...'^ )
echo  opt=Options^(^);opt.add_argument^('--disable-blink-features=AutomationControlled'^)
echo  driver=webdriver.Chrome^(service=Service^(ChromeDriverManager^(^).install^(^)^),options=opt^)
echo  driver.set_window_size^(300,200^);driver.set_window_position^(i*320,0^)
echo  driver.get^('https://shopee.co.id'^);driver.execute_script^(f'localStorage.setItem^("device_id","{device}"^)'^)
echo  driver.get^('https://live.shopee.co.id/share?from=live^&session=%s%^&in=1'^);viewers.append^(driver^)
echo  time.sleep^(1.5^)
echo print^(f'SUCCESS! {len^(viewers^)} viewers active'^);input^('Press Enter to stop...'^)
echo for d in viewers:d.quit^(^)
) > t.py && python t.py && del t.py

pause
