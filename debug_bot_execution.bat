@echo off
chcp 437 >nul 2>&1
title Debug Bot Execution

echo ===============================================
echo        DEBUG BOT EXECUTION
echo ===============================================
echo.

REM Create detailed execution log
set EXEC_LOG=bot_execution_debug.log
echo [%date% %time%] Debug bot execution started > %EXEC_LOG%

echo Testing bot execution step by step...
echo.

echo [STEP 1] Testing Python script import
echo [%date% %time%] Testing shopee_bot import >> %EXEC_LOG%
python -c "
import sys
sys.path.append('scripts')
print('[DEBUG] Python path:', sys.path)
try:
    import shopee_bot
    print('[SUCCESS] shopee_bot imported successfully')
except Exception as e:
    print('[ERROR] Failed to import shopee_bot:', e)
    import traceback
    traceback.print_exc()
" 2>>%EXEC_LOG%
echo.

echo [STEP 2] Testing bot with minimal parameters
echo [%date% %time%] Testing bot with test parameters >> %EXEC_LOG%
echo Running: python scripts\shopee_bot.py test_session 1 5
python scripts\shopee_bot.py test_session 1 5 2>>%EXEC_LOG%
set TEST_EXIT=%ERRORLEVEL%
echo [%date% %time%] Test execution exit code: %TEST_EXIT% >> %EXEC_LOG%
echo Test exit code: %TEST_EXIT%
echo.

echo [STEP 3] Testing bot with actual parameters (like in log)
echo [%date% %time%] Testing bot with real parameters >> %EXEC_LOG%
echo Running: python scripts\shopee_bot.py 157658364 2 3
echo This is the same command that caused window closing...
echo.

REM Capture output to file AND display
python scripts\shopee_bot.py 157658364 2 3 >bot_actual_output.txt 2>&1
set ACTUAL_EXIT=%ERRORLEVEL%

echo [%date% %time%] Actual execution exit code: %ACTUAL_EXIT% >> %EXEC_LOG%
echo Actual execution exit code: %ACTUAL_EXIT%
echo.

echo Bot output:
echo ----------------------------------------
type bot_actual_output.txt
echo ----------------------------------------
echo.

if %ACTUAL_EXIT% neq 0 (
    echo [ERROR] Bot failed with exit code: %ACTUAL_EXIT%
    echo [%date% %time%] Bot execution failed >> %EXEC_LOG%
) else (
    echo [SUCCESS] Bot completed successfully
    echo [%date% %time%] Bot execution successful >> %EXEC_LOG%
)

echo.
echo Full debug log saved to: %EXEC_LOG%
echo Bot output saved to: bot_actual_output.txt
echo.

echo ===============================================
echo           DEBUG ANALYSIS
echo ===============================================
echo.

echo Based on the original log, the issue occurs right after:
echo "Starting bot with params: 157658364 2 3"
echo.

echo If this debug script also closes the window suddenly,
echo then the issue is in the shopee_bot.py script itself.
echo.

echo Check the files above for detailed error information.
echo.
echo Press any key to exit...
pause >nul
