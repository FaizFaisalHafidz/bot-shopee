@echo off
title Test Bot Components
color 0E
cls

echo ================================================
echo           TEST BOT COMPONENTS
echo ================================================
echo.

echo [TEST 1] Checking Python...
python --version
if errorlevel 1 (
    echo [FAIL] Python not found
    pause
    exit /b 1
) else (
    echo [PASS] Python OK
)
echo.

echo [TEST 2] Testing detect_profiles.py...
echo ----------------------------------------
python scripts\detect_profiles.py > test_profiles.txt 2>&1
if errorlevel 1 (
    echo [FAIL] detect_profiles.py failed
    echo Error output:
    type test_profiles.txt
) else (
    echo [PASS] detect_profiles.py OK
    echo Output:
    type test_profiles.txt
)
echo.

echo [TEST 3] Checking temp_profiles.json...
if exist temp_profiles.json (
    echo [PASS] temp_profiles.json created
    echo Content preview:
    head -10 temp_profiles.json 2>nul || type temp_profiles.json | findstr /N "." | findstr "^[1-9]:"
) else (
    echo [FAIL] temp_profiles.json not created
)
echo.

echo [TEST 4] Testing shopee_bot.py with test params...
echo ----------------------------------------
python scripts\shopee_bot.py test_session 1 2 > test_bot.txt 2>&1
echo Bot test output:
type test_bot.txt
echo.

echo ================================================
echo              TEST COMPLETE
echo ================================================
echo.
echo Check these files for details:
echo - test_profiles.txt
echo - test_bot.txt  
echo - temp_profiles.json
echo.
pause
