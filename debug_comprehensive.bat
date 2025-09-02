@echo off
chcp 437 >nul 2>&1
title Comprehensive Debug Tool

echo ===============================================
echo     COMPREHENSIVE DEBUG TOOL
echo ===============================================
echo.

REM Create comprehensive debug log
set DEBUG_LOG=debug_comprehensive.log
echo [%date% %time%] Starting comprehensive debug... > %DEBUG_LOG%
echo. >> %DEBUG_LOG%

echo [1/8] SYSTEM INFORMATION
echo ===============================================
echo.
echo [%date% %time%] System Information: >> %DEBUG_LOG%
echo OS: %OS% >> %DEBUG_LOG%
echo Processor: %PROCESSOR_ARCHITECTURE% >> %DEBUG_LOG%
echo User: %USERNAME% >> %DEBUG_LOG%
echo Current Dir: %CD% >> %DEBUG_LOG%
echo. >> %DEBUG_LOG%

echo [2/8] PYTHON CHECK
echo ===============================================
echo.
echo [%date% %time%] Python Check: >> %DEBUG_LOG%
python --version >> %DEBUG_LOG% 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found! >> %DEBUG_LOG%
    echo CRITICAL ERROR: Python tidak ditemukan!
    echo Pastikan Python sudah terinstall dengan benar
    pause
    exit /b 1
)
echo Python: OK >> %DEBUG_LOG%
echo.

echo [3/8] PIP DEPENDENCIES CHECK  
echo ===============================================
echo.
echo [%date% %time%] Dependencies Check: >> %DEBUG_LOG%
echo Checking selenium... >> %DEBUG_LOG%
python -c "import selenium; print('selenium:', selenium.__version__)" >> %DEBUG_LOG% 2>&1
if %errorlevel% neq 0 (
    echo ERROR: selenium not found! >> %DEBUG_LOG%
    echo Installing selenium...
    pip install selenium >> %DEBUG_LOG% 2>&1
)

echo Checking webdriver_manager... >> %DEBUG_LOG%
python -c "import webdriver_manager; print('webdriver_manager: OK')" >> %DEBUG_LOG% 2>&1
if %errorlevel% neq 0 (
    echo ERROR: webdriver_manager not found! >> %DEBUG_LOG%
    echo Installing webdriver_manager...
    pip install webdriver-manager >> %DEBUG_LOG% 2>&1
)
echo.

echo [4/8] FILE STRUCTURE CHECK
echo ===============================================
echo.
echo [%date% %time%] File Structure Check: >> %DEBUG_LOG%
if exist "scripts\detect_profiles.py" (
    echo detect_profiles.py: FOUND >> %DEBUG_LOG%
) else (
    echo ERROR: detect_profiles.py NOT FOUND! >> %DEBUG_LOG%
    echo CRITICAL ERROR: scripts\detect_profiles.py tidak ditemukan!
    pause
    exit /b 1
)

if exist "scripts\shopee_bot.py" (
    echo shopee_bot.py: FOUND >> %DEBUG_LOG%
) else (
    echo ERROR: shopee_bot.py NOT FOUND! >> %DEBUG_LOG%
    echo CRITICAL ERROR: scripts\shopee_bot.py tidak ditemukan!
    pause
    exit /b 1
)
echo.

echo [5/8] CHROME PROFILES DETECTION
echo ===============================================
echo.
echo [%date% %time%] Chrome Profiles Detection: >> %DEBUG_LOG%
echo Running profile detection... >> %DEBUG_LOG%
python scripts\detect_profiles.py > temp_profiles.json 2>>%DEBUG_LOG%
if %errorlevel% neq 0 (
    echo ERROR: Profile detection failed! >> %DEBUG_LOG%
    echo CRITICAL ERROR: Gagal detect Chrome profiles!
    echo Check debug_comprehensive.log untuk detail error
    pause
    exit /b 1
)

if exist "temp_profiles.json" (
    echo Profile detection: SUCCESS >> %DEBUG_LOG%
    echo Profile file created: temp_profiles.json >> %DEBUG_LOG%
    type temp_profiles.json >> %DEBUG_LOG%
) else (
    echo ERROR: Profile file not created! >> %DEBUG_LOG%
    echo CRITICAL ERROR: File temp_profiles.json tidak terbuat!
    pause
    exit /b 1
)
echo.

echo [6/8] SHOPEE BOT SYNTAX CHECK
echo ===============================================
echo.
echo [%date% %time%] Bot Syntax Check: >> %DEBUG_LOG%
python -c "import sys; sys.path.append('scripts'); import shopee_bot; print('Bot syntax: OK')" >> %DEBUG_LOG% 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Bot syntax error! >> %DEBUG_LOG%
    echo CRITICAL ERROR: Ada syntax error di shopee_bot.py!
    echo Check debug_comprehensive.log untuk detail error
    pause
    exit /b 1
)
echo Bot syntax: OK >> %DEBUG_LOG%
echo.

echo [7/8] PARAMETER TEST
echo ===============================================
echo.
echo [%date% %time%] Parameter Test: >> %DEBUG_LOG%
echo Testing bot with test parameters... >> %DEBUG_LOG%
python scripts\shopee_bot.py test_session 1 5 >> %DEBUG_LOG% 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Parameter test failed! >> %DEBUG_LOG%
    echo WARNING: Parameter test gagal!
    echo Check debug_comprehensive.log untuk detail
) else (
    echo Parameter test: SUCCESS >> %DEBUG_LOG%
)
echo.

echo [8/8] CHROME INSTANCE TEST
echo ===============================================
echo.
echo [%date% %time%] Chrome Instance Test: >> %DEBUG_LOG%
echo Testing Chrome instance creation...
python -c "
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import sys

try:
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get('https://www.google.com')
    print('Chrome test: SUCCESS')
    driver.quit()
    sys.exit(0)
except Exception as e:
    print(f'Chrome test: ERROR - {e}')
    sys.exit(1)
" >> %DEBUG_LOG% 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Chrome instance test failed! >> %DEBUG_LOG%
    echo WARNING: Chrome instance test gagal!
    echo Check debug_comprehensive.log untuk detail
) else (
    echo Chrome instance test: SUCCESS >> %DEBUG_LOG%
)
echo.

echo ===============================================
echo     DEBUG SUMMARY
echo ===============================================
echo [%date% %time%] Debug Summary: >> %DEBUG_LOG%
echo.
echo All checks completed!
echo Results saved to: debug_comprehensive.log
echo.
echo Next steps:
echo 1. Check debug_comprehensive.log for any errors
echo 2. If all OK, try running main bot with: run.bat
echo 3. If still having issues, share debug_comprehensive.log
echo.
echo [%date% %time%] Comprehensive debug completed. >> %DEBUG_LOG%

pause
