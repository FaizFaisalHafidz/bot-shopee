@echo off & title Shopee Bot & color 0A
cls
echo.
echo    ████████████████████████████████████████
echo       🤖 SHOPEE LIVE VIEWER BOT 🤖
echo    ████████████████████████████████████████
echo.

python --version >nul 2>&1 || (echo ❌ Install Python first! & pause & exit)

set /p s="🎥 Session ID (default 157658364): "
if "%s%"=="" set s=157658364

set /p v="👥 Viewers (default 5): "  
if "%v%"=="" set v=5

set /p d="⏱️ Delay (default 2s): "
if "%d%"=="" set d=2

echo.
echo 🚀 Starting %v% viewers for session %s%...
echo.

python -c "import os,sys,time,random,string;exec('from selenium import webdriver;from selenium.webdriver.chrome.service import Service;from selenium.webdriver.chrome.options import Options;from webdriver_manager.chrome import ChromeDriverManager') if True else os.system('pip install selenium webdriver-manager --quiet');session='%s%';viewers=int('%v%');delay=int('%d%');url=f'https://live.shopee.co.id/share?from=live&session={session}&in=1';drivers=[];[drivers.append({'d':webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=(lambda o:o.add_argument('--no-sandbox') or o.add_argument('--disable-dev-shm-usage') or o.add_experimental_option('excludeSwitches',['enable-automation']) or o)(Options())),'id':''.join(random.choices(string.ascii_uppercase+string.digits,k=32))}) and drivers[-1]['d'].set_window_position((i%%3)*400,(i//3)*300) and drivers[-1]['d'].set_window_size(400,300) and drivers[-1]['d'].get('https://shopee.co.id') and drivers[-1]['d'].execute_script(f\"localStorage.setItem('device_id','{drivers[-1]['id']}');console.log('Device:','{drivers[-1]['id'][:8]}...')\") and drivers[-1]['d'].get(url) and print(f'✅ Viewer #{i+1}: {drivers[-1]['id'][:8]}...') and (time.sleep(delay) if i<viewers-1 else None) for i in range(viewers)];print(f'\n🎉 {len(drivers)} viewers active!');print('🔥 Check live stream now!');[time.sleep(30) or print(f'⚡ Still running... {sum(1 for d in drivers if d[\"d\"].window_handles)} active') for _ in iter(int,1)]"

echo.
echo ✅ Bot finished!
pause
