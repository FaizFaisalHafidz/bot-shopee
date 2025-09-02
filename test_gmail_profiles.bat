@echo off
chcp 65001 > nul
echo ============================================
echo GMAIL PROFILE TEST
echo ============================================
echo.

echo [DEBUG] Testing profile filtering...
cd /d "%~dp0"

echo [INFO] Running profile detection and filtering test:
python -c "
import json
import os
os.chdir('scripts')

# Read profiles
with open('../temp_profiles.json', 'r', encoding='utf-8') as f:
    profiles = json.load(f)

print(f'Total profiles found: {len(profiles)}')
print()

valid_profiles = []
for i, p in enumerate(profiles):
    email = p.get('email', 'Unknown')
    name = p.get('name', '')
    display_name = p.get('display_name', 'Unknown')
    
    print(f'[{i+1}] Profile: {name}')
    print(f'    Email: {email}')
    print(f'    Display: {display_name}')
    
    if email != 'Unknown' and name != 'System Profile' and '@gmail.com' in email:
        valid_profiles.append(p)
        print('    Status: ✓ VALID (will be used)')
    else:
        print('    Status: ✗ FILTERED OUT')
    print()

print(f'Valid Gmail profiles: {len(valid_profiles)}')
print('These will be used for bot viewers:')
for i, p in enumerate(valid_profiles):
    print(f'  {i+1}. {p.get(\"email\")} ({p.get(\"display_name\")})')
"

echo.
echo Press any key to continue with actual bot test...
pause > nul

echo.
echo [INFO] Starting bot with filtered profiles...
taskkill /f /im chrome.exe /t 2>nul
timeout /t 2 /nobreak > nul

cd scripts
python shopee_bot.py 157658364 3 5

pause
