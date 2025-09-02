@echo off
title Test Encoding Fix
color 0C
cls

echo ================================================
echo           TEST ENCODING FIX
echo ================================================
echo.

echo [TEST] Testing Windows encoding fix...
python test_encoding.py
if errorlevel 1 (
    echo [FAIL] Encoding test failed
) else (
    echo [PASS] Encoding test passed
)
echo.

echo [TEST] Testing detect_profiles.py with encoding fix...
python scripts\detect_profiles.py > test_detect_fixed.txt 2>&1
if errorlevel 1 (
    echo [FAIL] detect_profiles.py still has issues
    echo Error output:
    type test_detect_fixed.txt
) else (
    echo [PASS] detect_profiles.py works with encoding fix
    echo Output:
    type test_detect_fixed.txt
)
echo.

echo ================================================
echo         ENCODING TEST COMPLETE
echo ================================================
pause
