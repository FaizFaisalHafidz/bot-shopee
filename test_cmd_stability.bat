@echo off
chcp 437 >nul 2>&1
title Windows CMD Stability Test

echo ================================================
echo     WINDOWS COMMAND PROMPT STABILITY TEST
echo ================================================
echo.
echo Testing untuk menemukan penyebab window closing...
echo.

REM Test 1: Basic input
echo [TEST 1] Basic Input Test
echo Silakan ketik sesuatu dan tekan Enter:
set /p test_input=Input test: 
echo Anda mengetik: %test_input%
echo TEST 1: SUCCESS - Input berfungsi normal
echo.

REM Test 2: Python simple call
echo [TEST 2] Python Simple Call Test
echo Testing python call...
python -c "print('Python call test: SUCCESS')"
if %errorlevel% neq 0 (
    echo TEST 2: FAILED - Python call error
    echo Error code: %errorlevel%
    goto :error_exit
) else (
    echo TEST 2: SUCCESS - Python call OK
)
echo.

REM Test 3: Python with input simulation
echo [TEST 3] Python Input Simulation Test
echo Testing python script with parameters...
python -c "
import sys
print('Script started with args:', sys.argv)
print('Testing parameter parsing...')
try:
    if len(sys.argv) > 1:
        print('Parameter 1:', sys.argv[1])
    else:
        print('No parameters provided')
    print('Python input test: SUCCESS')
except Exception as e:
    print('Python input test: ERROR -', e)
    sys.exit(1)
" test_param
if %errorlevel% neq 0 (
    echo TEST 3: FAILED - Python input simulation error
    goto :error_exit
) else (
    echo TEST 3: SUCCESS - Python input simulation OK
)
echo.

REM Test 4: File existence check
echo [TEST 4] File Existence Check
echo Checking critical files...
if not exist "scripts\shopee_bot.py" (
    echo TEST 4: FAILED - shopee_bot.py not found
    goto :error_exit
)
if not exist "scripts\detect_profiles.py" (
    echo TEST 4: FAILED - detect_profiles.py not found  
    goto :error_exit
)
echo TEST 4: SUCCESS - All files found
echo.

REM Test 5: Multiple input simulation
echo [TEST 5] Multiple Input Simulation
echo Simulating multiple user inputs...
echo Input 1 - Session ID:
set /p session_test=Masukkan test session ID: 
echo Session ID: %session_test%
echo.
echo Input 2 - Confirmation:
set /p confirm_test=Ketik 'y' untuk konfirmasi: 
echo Confirmation: %confirm_test%
echo TEST 5: SUCCESS - Multiple inputs OK
echo.

REM Test 6: Error handling
echo [TEST 6] Error Handling Test
echo Testing error conditions...
python -c "
import sys
print('Testing error handling...')
try:
    # Test various error conditions
    result = 1 / 1  # This should work
    print('Math test: OK')
    
    # Test file access
    with open('test_temp_file.tmp', 'w') as f:
        f.write('test')
    with open('test_temp_file.tmp', 'r') as f:
        content = f.read()
    print('File test: OK')
    
    # Cleanup
    import os
    os.remove('test_temp_file.tmp')
    print('Cleanup test: OK')
    
except Exception as e:
    print('Error handling test: ERROR -', e)
    sys.exit(1)
"
if %errorlevel% neq 0 (
    echo TEST 6: FAILED - Error handling test failed
    goto :error_exit
) else (
    echo TEST 6: SUCCESS - Error handling OK
)
echo.

echo ================================================
echo           ALL TESTS COMPLETED
echo ================================================
echo.
echo All stability tests PASSED!
echo CMD window should remain open until you press a key.
echo.
echo If the window closed unexpectedly during any test,
echo that indicates where the problem occurs.
echo.
echo Press any key to exit normally...
pause >nul
exit /b 0

:error_exit
echo.
echo ================================================
echo              TEST FAILED
echo ================================================
echo.
echo A test failed! Check the output above for details.
echo This might explain why the main script window closes.
echo.
echo Press any key to exit...
pause >nul
exit /b 1
