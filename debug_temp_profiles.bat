@echo off
chcp 65001 > nul
echo ============================================
echo TEMP PROFILE DEBUG TEST
echo ============================================
echo.

echo [DEBUG] Checking temp profile files...
echo.

if exist "temp_bot_profiles.json" (
    echo [✓] Found temp_bot_profiles.json
    echo [INFO] Profile contents:
    type temp_bot_profiles.json
) else (
    echo [✗] temp_bot_profiles.json not found
)

echo.
echo [DEBUG] Checking temp profile directories...

if exist "sessions\temp_bot_profiles" (
    echo [✓] Found temp_bot_profiles directory
    echo [INFO] Contents:
    dir /b "sessions\temp_bot_profiles"
    echo.
    
    echo [DEBUG] Checking first profile structure:
    for /d %%i in ("sessions\temp_bot_profiles\temp_*") do (
        echo [INFO] Profile: %%i
        if exist "%%i\Preferences" (
            echo   [✓] Has Preferences
        ) else (
            echo   [✗] Missing Preferences
        )
        
        if exist "%%i\Default" (
            echo   [✓] Has Default directory
            if exist "%%i\Default\Cookies" (
                echo     [✓] Has Default\Cookies
            ) else (
                echo     [✗] Missing Default\Cookies
            )
            if exist "%%i\Default\Login Data" (
                echo     [✓] Has Default\Login Data
            ) else (
                echo     [✗] Missing Default\Login Data
            )
        ) else (
            echo   [✗] Missing Default directory
        )
        echo.
        goto :break
    )
    :break
) else (
    echo [✗] sessions\temp_bot_profiles directory not found
)

echo.
echo [DEBUG] Test bot with temp profiles (dry run)...
cd scripts
python -c "
import os, json
os.chdir('..')
try:
    if os.path.exists('temp_bot_profiles.json'):
        with open('temp_bot_profiles.json', 'r', encoding='utf-8') as f:
            profiles = json.load(f)
        print(f'[✓] Loaded {len(profiles)} temp profiles')
        for i, p in enumerate(profiles[:2]):  # Show first 2
            print(f'[{i+1}] {p.get(\"email\", \"Unknown\")} -> {p.get(\"temp_path\", \"No temp path\")}')
    else:
        print('[✗] No temp_bot_profiles.json found')
except Exception as e:
    print(f'[ERROR] {e}')
"

echo.
echo Press any key to continue...
pause > nul
