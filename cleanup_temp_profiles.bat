@echo off
chcp 65001 > nul
echo ============================================
echo CLEANUP TEMPORARY PROFILES
echo ============================================
echo.

echo [INFO] Removing temporary profile copies...

if exist "sessions\temp_bot_profiles" (
    echo [INFO] Found temp_bot_profiles directory
    rmdir /s /q "sessions\temp_bot_profiles"
    echo [SUCCESS] Temporary profiles deleted
) else (
    echo [INFO] No temporary profiles found
)

if exist "temp_bot_profiles.json" (
    echo [INFO] Removing temp profiles index file...
    del "temp_bot_profiles.json"
    echo [SUCCESS] Index file deleted
) else (
    echo [INFO] No temp profiles index file found
)

echo.
echo [SUCCESS] Cleanup completed
pause
