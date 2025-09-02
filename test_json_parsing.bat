@echo off
chcp 437 >nul 2>&1
title Test JSON Profile Parsing

echo ===============================================
echo        TEST JSON PROFILE PARSING
echo ===============================================
echo.

echo [TEST 1] Generate profiles JSON
python scripts\detect_profiles_clean.py > test_profiles.json 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Failed to generate profiles
    type test_profiles.json
    pause
    exit /b 1
)

echo [TEST 2] Display JSON content
echo JSON Output:
echo ----------------------------------------
type test_profiles.json
echo ----------------------------------------
echo.

echo [TEST 3] Count profiles using Python
python -c "
import json
try:
    with open('test_profiles.json', 'r') as f:
        profiles = json.load(f)
    count = len(profiles)
    print(f'PROFILE_COUNT={count}')
    print(f'Found {count} profiles:')
    for i, profile in enumerate(profiles):
        email = profile.get('email', 'Unknown')
        name = profile.get('name', 'Unknown')
        path = profile.get('path', 'Unknown')
        print(f'  {i+1}. {email} ({name})')
        print(f'      Path: {path}')
except Exception as e:
    print(f'ERROR: {e}')
" > count_output.txt 2>&1

echo Count result:
type count_output.txt
echo.

echo [TEST 4] Extract count for BAT file
for /f "tokens=2 delims==" %%i in ('findstr "PROFILE_COUNT" count_output.txt') do set test_count=%%i
echo Extracted count: %test_count%

if "%test_count%"=="" (
    echo [ERROR] Could not extract count!
) else (
    echo [SUCCESS] Count extraction successful: %test_count% profiles
)

echo.
echo [TEST 5] Validate temp_profiles.json for bot
copy test_profiles.json temp_profiles.json >nul
python scripts\shopee_bot.py test_session 1 5 2>&1
if %errorlevel% equ 0 (
    echo [SUCCESS] Bot can read profiles correctly
) else (
    echo [ERROR] Bot cannot read profiles
)

echo.
echo Cleanup test files...
if exist "test_profiles.json" del test_profiles.json >nul
if exist "count_output.txt" del count_output.txt >nul

echo.
echo Test completed! If count extraction worked, 
echo the main run.bat should work too.
echo.
pause
