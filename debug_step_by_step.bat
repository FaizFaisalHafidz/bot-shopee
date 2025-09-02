@echo off
title Debug Bot - Step by Step
color 0E
cls

echo ================================================
echo           DEBUG BOT - STEP BY STEP
echo ================================================
echo.

REM Test 1: Basic Python
echo [STEP 1] Testing Python...
python --version
if errorlevel 1 (
    echo [FAIL] Python not working
    pause
    exit /b 1
)
echo [PASS] Python OK
echo.

REM Test 2: Profile Detection
echo [STEP 2] Testing Profile Detection...
python scripts\detect_profiles.py > debug_profiles.txt 2>&1
if errorlevel 1 (
    echo [FAIL] Profile detection failed
    echo Error:
    type debug_profiles.txt
    pause
    exit /b 1
)
echo [PASS] Profile detection OK
echo Output:
type debug_profiles.txt
echo.

REM Test 3: Dependencies
echo [STEP 3] Testing Dependencies...
python -c "import selenium; print('Selenium OK')" 2>&1
if errorlevel 1 (
    echo [INFO] Installing selenium...
    pip install selenium
)

python -c "import webdriver_manager; print('WebDriver Manager OK')" 2>&1  
if errorlevel 1 (
    echo [INFO] Installing webdriver-manager...
    pip install webdriver-manager
)
echo [PASS] Dependencies checked
echo.

REM Test 4: Bot Script Test
echo [STEP 4] Testing Bot Script (dry run)...
python scripts\shopee_bot.py test_session 1 1 > debug_bot.txt 2>&1
echo Bot test exit code: %ERRORLEVEL%
echo Bot output:
type debug_bot.txt
echo.

REM Get user input for real test
echo [STEP 5] Ready for real test
set /p session="Enter session ID (or 'skip' to exit): "
if "%session%"=="skip" (
    echo Test skipped
    pause
    exit /b 0
)

set /p viewers="Enter number of viewers (1-3): "
if "%viewers%"=="" set viewers=1

echo.
echo Starting bot with session=%session% viewers=%viewers%
echo.

python scripts\shopee_bot.py %session% %viewers% 3 > final_bot_output.txt 2>&1
echo Final bot exit code: %ERRORLEVEL%
echo Final output:
type final_bot_output.txt

echo.
echo ================================================
echo           DEBUG TEST COMPLETE
echo ================================================
echo.
echo Generated files:
echo - debug_profiles.txt
echo - debug_bot.txt  
echo - final_bot_output.txt
echo.
pause
