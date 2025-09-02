@echo off
chcp 437 >nul 2>&1
title Shopee Bot Launcher - Simplified

REM Setup logging
set LOGFILE=bot_debug.log
echo [%date% %time%] Bot started > %LOGFILE%

echo ================================================
echo        SHOPEE LIVE VIEWER BOT
echo ================================================
echo.

REM Check Python
echo [INFO] Checking Python installation...
echo [%date% %time%] Checking Python installation >> %LOGFILE%
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python tidak ditemukan!
    echo Install Python terlebih dahulu
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set python_version=%%i
echo [OK] %python_version%
echo [%date% %time%] Python version: %python_version% >> %LOGFILE%

REM Get session ID
echo.
echo Session ID bisa ditemukan di URL Shopee Live:
echo https://live.shopee.co.id/share?from=live^&session=XXXXXX^&in=1
echo.
set /p session_id="Masukkan Session ID Shopee Live: "
echo [%date% %time%] User input session ID: %session_id% >> %LOGFILE%

if "%session_id%"=="" (
    echo [ERROR] Session ID tidak boleh kosong!
    pause
    exit /b 1
)

REM Profile detection
echo.
echo [INFO] Mencari profile Chrome yang tersedia...
echo [%date% %time%] Starting profile detection >> %LOGFILE%
echo.

python scripts\detect_profiles_clean.py > temp_profiles.json 2>>%LOGFILE%
if %errorlevel% neq 0 (
    echo [ERROR] Gagal mendeteksi profile Chrome!
    echo [%date% %time%] ERROR: Profile detection failed >> %LOGFILE%
    echo Check %LOGFILE% for details
    pause
    exit /b 1
)

echo [OK] Profile detection berhasil
echo [%date% %time%] Profile detection successful >> %LOGFILE%

REM Show profiles
echo.
echo Profile yang ditemukan:
type temp_profiles.json
echo.

REM Get viewers count
set /p max_viewers="Jumlah viewers yang ingin disimulasikan (1-10): "
echo [%date% %time%] User input viewers: %max_viewers% >> %LOGFILE%

REM Validate viewers input
echo %max_viewers%| findstr /r "^[1-9][0-9]*$" >nul
if %errorlevel% neq 0 (
    echo [ERROR] Masukkan angka yang valid!
    pause
    exit /b 1
)

REM Get delay
set /p delay_seconds="Delay antar viewer dalam detik (1-10): "
echo [%date% %time%] User input delay: %delay_seconds% >> %LOGFILE%

REM Validate delay input  
echo %delay_seconds%| findstr /r "^[1-9][0-9]*$" >nul
if %errorlevel% neq 0 (
    echo [ERROR] Masukkan angka yang valid!
    pause
    exit /b 1
)

REM Final confirmation
echo.
echo ================================================
echo                KONFIRMASI
echo ================================================
echo Session ID: %session_id%
echo Jumlah Viewers: %max_viewers%
echo Delay: %delay_seconds% detik
echo Target URL: https://live.shopee.co.id/share?from=live^&session=%session_id%^&in=1
echo.
set /p confirm="Mulai bot? (y/n): "
echo [%date% %time%] User confirmation: %confirm% >> %LOGFILE%

if /i not "%confirm%"=="y" (
    echo [INFO] Dibatalkan oleh user
    pause
    exit /b 0
)

REM Dependencies check
echo.
echo [INFO] Checking dependencies...
echo [%date% %time%] Checking dependencies >> %LOGFILE%

python -c "import selenium, webdriver_manager" >nul 2>>%LOGFILE%
if %errorlevel% neq 0 (
    echo [WARNING] Installing dependencies...
    pip install selenium webdriver-manager >>%LOGFILE% 2>&1
)
echo [%date% %time%] Dependencies ready >> %LOGFILE%

REM Start bot
echo.
echo ================================================
echo              MEMULAI BOT...
echo ================================================
echo [%date% %time%] Starting bot with params: %session_id% %max_viewers% %delay_seconds% >> %LOGFILE%

python scripts\shopee_bot.py "%session_id%" %max_viewers% %delay_seconds% 2>>%LOGFILE%
set BOT_EXIT=%errorlevel%

echo.
echo ================================================
echo              BOT SELESAI
echo ================================================
echo [%date% %time%] Bot finished with exit code: %BOT_EXIT% >> %LOGFILE%

if %BOT_EXIT% equ 0 (
    echo [SUCCESS] Bot berhasil dijalankan!
) else (
    echo [ERROR] Bot mengalami error (Exit code: %BOT_EXIT%)
    echo Check %LOGFILE% for details
)

echo.
echo Log file: %LOGFILE%
echo Press any key to exit...
pause >nul
