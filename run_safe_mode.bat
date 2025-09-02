@echo off
setlocal EnableDelayedExpansion
chcp 437 >nul 2>&1
title Shopee Bot - SAFE MODE

REM Enable error trapping
set "SAFE_MODE=1"
set "LOGFILE=bot_safe_mode.log"
set "TEMP_DIR=%TEMP%\shopee_bot"

echo ================================================
echo        SHOPEE BOT - SAFE MODE LAUNCHER
echo ================================================
echo.

REM Create temp directory and log file
if not exist "%TEMP_DIR%" mkdir "%TEMP_DIR%" >nul 2>&1
echo [%date% %time%] Safe mode started > "%LOGFILE%"
echo Safe mode log: %LOGFILE%
echo.

REM Test 1: Basic system check
echo [1/5] System Check...
echo [%date% %time%] System check started >> "%LOGFILE%"
python --version >nul 2>&1
if !errorlevel! neq 0 (
    echo ERROR: Python tidak ditemukan! >> "%LOGFILE%"
    echo CRITICAL: Python not installed or not in PATH
    goto safe_exit
)
echo OK - Python detected >> "%LOGFILE%"

REM Test 2: File structure check  
echo [2/5] File Structure Check...
echo [%date% %time%] File structure check started >> "%LOGFILE%"
if not exist "scripts\detect_profiles.py" (
    echo ERROR: detect_profiles.py not found >> "%LOGFILE%"
    echo CRITICAL: Missing detect_profiles.py
    goto safe_exit
)
if not exist "scripts\shopee_bot.py" (
    echo ERROR: shopee_bot.py not found >> "%LOGFILE%"
    echo CRITICAL: Missing shopee_bot.py  
    goto safe_exit
)
echo OK - All scripts found >> "%LOGFILE%"

REM Test 3: Dependencies check
echo [3/5] Dependencies Check...
echo [%date% %time%] Dependencies check started >> "%LOGFILE%"
python -c "import selenium, webdriver_manager; print('Dependencies OK')" >"%TEMP_DIR%\dep_test.txt" 2>&1
if !errorlevel! neq 0 (
    echo ERROR: Missing dependencies >> "%LOGFILE%"
    echo CRITICAL: Installing dependencies...
    pip install selenium webdriver-manager >> "%LOGFILE%" 2>&1
    if !errorlevel! neq 0 (
        echo Installation failed >> "%LOGFILE%"
        echo CRITICAL: Failed to install dependencies
        goto safe_exit
    )
)
echo OK - Dependencies available >> "%LOGFILE%"

REM Test 4: Profile detection in safe mode
echo [4/5] Profile Detection Test...
echo [%date% %time%] Profile detection test started >> "%LOGFILE%"
python scripts\detect_profiles.py >"%TEMP_DIR%\profile_test.txt" 2>&1
set PROFILE_ERROR=!errorlevel!
if !PROFILE_ERROR! neq 0 (
    echo ERROR: Profile detection failed with code !PROFILE_ERROR! >> "%LOGFILE%"
    echo CRITICAL: Profile detection failed
    type "%TEMP_DIR%\profile_test.txt"
    echo.
    echo Check log: %LOGFILE%
    goto safe_exit
)
echo OK - Profiles detected >> "%LOGFILE%"

REM Test 5: Bot syntax check
echo [5/5] Bot Syntax Check...
echo [%date% %time%] Bot syntax check started >> "%LOGFILE%"
python -c "import sys; sys.path.append('scripts'); import shopee_bot" >"%TEMP_DIR%\syntax_test.txt" 2>&1
if !errorlevel! neq 0 (
    echo ERROR: Bot syntax error >> "%LOGFILE%"
    echo CRITICAL: Bot syntax error detected
    type "%TEMP_DIR%\syntax_test.txt"
    echo.
    goto safe_exit
)
echo OK - Bot syntax valid >> "%LOGFILE%"

echo.
echo ================================================
echo           ALL CHECKS PASSED!
echo ================================================
echo.
echo System is ready for bot execution.
echo.

REM Safe user input section
:input_session
echo Please enter Shopee Live session ID:
echo (Example: abc123def456)
set /p session_id="Session ID: "

if "%session_id%"=="" (
    echo [ERROR] Session ID cannot be empty!
    echo [%date% %time%] Empty session ID provided >> "%LOGFILE%"
    goto input_session
)

echo [%date% %time%] Session ID provided: %session_id% >> "%LOGFILE%"
echo Session ID: %session_id%
echo.

:input_viewers
echo How many viewers to simulate? (1-10 recommended):
set /p max_viewers="Viewers: "

REM Validate numeric input
echo %max_viewers%| findstr /r "^[1-9][0-9]*$" >nul
if !errorlevel! neq 0 (
    echo [ERROR] Please enter a valid number!
    echo [%date% %time%] Invalid viewers input: %max_viewers% >> "%LOGFILE%"
    goto input_viewers
)

if %max_viewers% gtr 50 (
    echo [WARNING] %max_viewers% viewers is quite high!
    echo [%date% %time%] High viewer count requested: %max_viewers% >> "%LOGFILE%"
    echo Continue anyway? (y/N):
    set /p confirm="Confirm: "
    if /i not "!confirm!"=="y" goto input_viewers
)

echo [%date% %time%] Viewers requested: %max_viewers% >> "%LOGFILE%"
echo Viewers: %max_viewers%
echo.

REM Final confirmation
echo ================================================
echo                CONFIRMATION
echo ================================================
echo Session ID: %session_id%
echo Viewers: %max_viewers%
echo Target URL: https://live.shopee.co.id/share?from=live^&session=%session_id%^&in=1
echo.
echo [%date% %time%] Final confirmation requested >> "%LOGFILE%"
echo Start the bot? (Y/N):
set /p final_confirm="Start: "

if /i not "%final_confirm%"=="y" (
    echo [%date% %time%] User cancelled >> "%LOGFILE%"
    echo Operation cancelled by user.
    goto safe_exit
)

echo.
echo ================================================
echo              STARTING BOT...
echo ================================================
echo [%date% %time%] Bot execution started >> "%LOGFILE%"
echo Starting bot with session: %session_id% and %max_viewers% viewers...
echo.

REM Execute bot with error handling
python scripts\shopee_bot.py "%session_id%" %max_viewers% 30 >"%TEMP_DIR%\bot_execution.txt" 2>&1
set BOT_ERROR=!errorlevel!

echo.
echo ================================================
echo              BOT EXECUTION COMPLETE
echo ================================================

if !BOT_ERROR! equ 0 (
    echo [%date% %time%] Bot execution completed successfully >> "%LOGFILE%"
    echo SUCCESS: Bot completed successfully!
) else (
    echo [%date% %time%] Bot execution failed with code !BOT_ERROR! >> "%LOGFILE%"
    echo ERROR: Bot execution failed with error code !BOT_ERROR!
    echo.
    echo Bot output:
    type "%TEMP_DIR%\bot_execution.txt"
)

echo.
echo Bot output saved to: %TEMP_DIR%\bot_execution.txt
echo Full log saved to: %LOGFILE%

:safe_exit
echo.
echo ================================================
echo              SAFE EXIT
echo ================================================
echo [%date% %time%] Safe mode exiting >> "%LOGFILE%"
echo Press any key to exit...
pause >nul
echo [%date% %time%] Safe mode ended >> "%LOGFILE%"
exit /b 0
