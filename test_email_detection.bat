@echo off
chcp 437 >nul 2>&1
title Test Email Detection - Windows

echo ===============================================
echo        TEST EMAIL DETECTION - WINDOWS
echo ===============================================
echo.

echo [TEST 1] Generate profiles with email detection
echo Running detect_profiles_clean.py...
python scripts\detect_profiles_clean.py > profiles_with_emails.json 2>&1

if %errorlevel% neq 0 (
    echo [ERROR] Profile detection failed!
    type profiles_with_emails.json
    pause
    exit /b 1
)

echo [SUCCESS] Profile detection completed!
echo.

echo [TEST 2] Display detected profiles with emails
echo ================================================
type profiles_with_emails.json
echo ================================================
echo.

echo [TEST 3] Count profiles with real emails
python -c "
import json
try:
    with open('profiles_with_emails.json', 'r') as f:
        profiles = json.load(f)
    
    print(f'Total profiles found: {len(profiles)}')
    print()
    
    real_emails = []
    for i, profile in enumerate(profiles):
        email = profile.get('email', 'Unknown')
        display_name = profile.get('display_name', 'Unknown')
        name = profile.get('name', 'Unknown')
        path = profile.get('path', 'Unknown')
        
        print(f'{i+1}. Profile: {name}')
        print(f'   Email: {email}')
        print(f'   Display Name: {display_name}')
        print(f'   Path: {path}')
        
        if email != 'Unknown' and '@' in email:
            real_emails.append(email)
        print()
    
    print(f'Profiles with real emails: {len(real_emails)}')
    for email in real_emails:
        print(f'  - {email}')
    
    if 'ridwanfadilah245@gmail.com' in real_emails:
        print()
        print('[SUCCESS] ridwanfadilah245@gmail.com found!')
    else:
        print()
        print('[INFO] ridwanfadilah245@gmail.com not found (expected in Windows only)')
        
except Exception as e:
    print(f'Error: {e}')
"
echo.

echo [TEST 4] Test bot with detected profiles
copy profiles_with_emails.json temp_profiles.json >nul
python scripts\shopee_bot.py test_session 1 5

if %errorlevel% equ 0 (
    echo [SUCCESS] Bot can read profiles with emails correctly!
) else (
    echo [ERROR] Bot failed to read profiles
)

echo.
echo Test completed! 
echo In Windows environment, you should see:
echo - abdurahmad109@gmail.com
echo - mamanujang461@gmail.com (ujang maman)  
echo - ridwanfadilah245@gmail.com (ridwan fadilah)
echo.
echo Cleanup...
if exist "profiles_with_emails.json" del profiles_with_emails.json >nul

pause
