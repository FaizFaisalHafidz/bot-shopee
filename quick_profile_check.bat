@echo off
chcp 437 >nul 2>&1
title Quick Profile Check

echo ===============================================
echo        QUICK PROFILE CHECK
echo ===============================================
echo.

echo [CHECK 1] temp_profiles.json file existence
if exist "temp_profiles.json" (
    echo [OK] temp_profiles.json exists
) else (
    echo [ERROR] temp_profiles.json NOT FOUND!
    echo This is likely the cause of window closing
    echo.
    echo Generating temp_profiles.json...
    python scripts\detect_profiles.py > temp_profiles.json 2>&1
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to generate profiles!
        echo Check detect_profiles.py
        pause
        exit /b 1
    )
    echo [OK] temp_profiles.json generated
)
echo.

echo [CHECK 2] temp_profiles.json content
echo Content preview:
echo ----------------------------------------
type temp_profiles.json
echo ----------------------------------------
echo.

echo [CHECK 3] JSON validation
python -c "
import json
try:
    with open('temp_profiles.json', 'r') as f:
        profiles = json.load(f)
    print(f'[OK] Valid JSON with {len(profiles)} profiles')
    for i, profile in enumerate(profiles):
        email = profile.get('email', 'Unknown')
        name = profile.get('name', 'Unknown')  
        print(f'   Profile {i+1}: {email} ({name})')
except json.JSONDecodeError as e:
    print(f'[ERROR] Invalid JSON: {e}')
except Exception as e:
    print(f'[ERROR] {e}')
"
echo.

echo [CHECK 4] Bot execution test
echo Testing bot with minimal parameters...
python scripts\shopee_bot.py test_session 1 5
if %errorlevel% neq 0 (
    echo [ERROR] Bot test failed!
    echo This confirms the issue
) else (
    echo [OK] Bot test passed
)
echo.

echo Profile check completed!
echo If temp_profiles.json was missing, that was the cause of window closing.
echo.
pause
