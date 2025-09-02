@echo off
chcp 437 >nul
title Bot Shopee Live - Menggunakan Profile Chrome yang Ada
color 0A

REM Create log file untuk debugging
set LOGFILE=logs\bot_debug.log
if not exist logs mkdir logs
echo [%date% %time%] Bot started > %LOGFILE%

cls

echo.
echo ================================================
echo        BOT SHOPEE LIVE VIEWER v3.0
echo        Menggunakan Profile Chrome yang Ada  
echo ================================================
echo.

REM Cek apakah Python terinstall
echo [INFO] Checking Python installation... 
echo [%date% %time%] Checking Python installation >> %LOGFILE%

python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python belum terinstall!
    echo [%date% %time%] ERROR: Python not found >> %LOGFILE%
    echo.
    echo Cara install Python:
    echo    1. Buka Microsoft Store
    echo    2. Cari "Python 3.11"  
    echo    3. Install dan restart komputer
    echo.
    echo    ATAU download dari: https://python.org/downloads
    echo    PASTIKAN centang "Add Python to PATH" saat install!
    echo.
    echo Check log file: %LOGFILE%
    pause
    exit /b 1
)

echo [OK] Python ditemukan:
python --version
for /f "delims=" %%i in ('python --version') do echo [%date% %time%] Python version: %%i >> %LOGFILE%
echo.

REM Input konfigurasi
echo ================================================
echo              KONFIGURASI BOT
echo ================================================
echo.

set /p session="Masukkan Session ID Shopee Live: "
echo [%date% %time%] User input session ID: %session% >> %LOGFILE%

if "%session%"=="" (
    echo [ERROR] Session ID wajib diisi!
    echo [%date% %time%] ERROR: Empty session ID >> %LOGFILE%
    echo Check log file: %LOGFILE%
    pause
    exit /b 1
)

echo.
echo [INFO] Mencari profile Chrome yang tersedia...
echo [%date% %time%] Starting profile detection >> %LOGFILE%
echo.

REM Jalankan script deteksi profile
echo [INFO] Menjalankan detect_profiles.py...
echo [%date% %time%] Running detect_profiles.py >> %LOGFILE%

python scripts\detect_profiles.py > temp_profile_output.txt 2>&1
set DETECTION_ERROR=%ERRORLEVEL%

echo [%date% %time%] detect_profiles.py exit code: %DETECTION_ERROR% >> %LOGFILE%

if %DETECTION_ERROR% NEQ 0 (
    echo [ERROR] Gagal mendeteksi profile Chrome!
    echo [%date% %time%] ERROR: Profile detection failed >> %LOGFILE%
    echo.
    echo Output dari detect_profiles.py:
    type temp_profile_output.txt
    echo.
    echo Full error logged to: %LOGFILE%
    echo Output saved to: temp_profile_output.txt
    pause
    exit /b 1
) else (
    echo [OK] Profile detection berhasil
    echo [%date% %time%] Profile detection successful >> %LOGFILE%
    type temp_profile_output.txt
)

REM Ambil jumlah profile dari output
for /f "tokens=2 delims==" %%i in ('findstr "PROFILE_COUNT" temp_profile_output.txt') do set profile_count=%%i
echo [%date% %time%] Profile count detected: %profile_count% >> %LOGFILE%

if "%profile_count%"=="" (
    echo [ERROR] Tidak bisa mendapatkan jumlah profile!
    echo [%date% %time%] ERROR: Could not get profile count >> %LOGFILE%
    echo Check temp_profile_output.txt for details
    pause
    exit /b 1
)

if %profile_count%==0 (
    echo [ERROR] Tidak ada profile Chrome yang valid ditemukan!
    echo [%date% %time%] ERROR: No valid Chrome profiles found >> %LOGFILE%
    echo.
    echo [INFO] Pastikan sudah pernah login ke Chrome dan buat profile
    echo Check log file: %LOGFILE%
    echo.
    pause
    exit /b 1
)

echo.
set /p viewers="Berapa viewer yang ingin dibuat (max %profile_count%): "
if "%viewers%"=="" set viewers=1
echo [%date% %time%] User input viewers: %viewers% >> %LOGFILE%

if %viewers% GTR %profile_count% (
    echo [WARNING] Jumlah viewer tidak boleh lebih dari %profile_count% profile!
    echo [%date% %time%] WARNING: Viewers count adjusted to %profile_count% >> %LOGFILE%
    set viewers=%profile_count%
)

set /p delay="Jeda antar viewer dalam detik (default 3): "
if "%delay%"=="" set delay=3
echo [%date% %time%] User input delay: %delay% >> %LOGFILE%

echo.
echo ================================================
echo            KONFIRMASI KONFIGURASI
echo ================================================
echo.
echo Session ID    : %session%
echo Jumlah Viewer : %viewers%
echo Jeda         : %delay% detik
echo URL Live      : https://live.shopee.co.id/share?from=live^&session=%session%^&in=1
echo.

set /p confirm="Mulai bot sekarang? (y/n): "
echo [%date% %time%] User confirmation: %confirm% >> %LOGFILE%

if /i not "%confirm%"=="y" (
    echo [INFO] Bot dibatalkan.
    echo [%date% %time%] Bot cancelled by user >> %LOGFILE%
    pause
    exit /b 0
)

echo.
echo ================================================
echo              MEMULAI BOT...
echo ================================================
echo.

REM Cek dan install dependencies
echo [INFO] Memeriksa dependencies...
echo [%date% %time%] Checking dependencies >> %LOGFILE%

python -c "import selenium,webdriver_manager" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing selenium dan webdriver-manager...
    echo [%date% %time%] Installing dependencies >> %LOGFILE%
    python -m pip install selenium webdriver-manager --quiet
    if errorlevel 1 (
        echo [ERROR] Gagal install dependencies!
        echo [%date% %time%] ERROR: Failed to install dependencies >> %LOGFILE%
        echo Check log file: %LOGFILE%
        pause
        exit /b 1
    )
)

echo [OK] Dependencies siap!
echo [%date% %time%] Dependencies ready >> %LOGFILE%
echo.

REM Jalankan bot
echo [INFO] Menjalankan bot...
echo [%date% %time%] Starting bot with params: %session% %viewers% %delay% >> %LOGFILE%
echo.

python scripts\shopee_bot.py %session% %viewers% %delay% 2>&1 | tee bot_output.txt
set BOT_ERROR=%ERRORLEVEL%

echo [%date% %time%] Bot exit code: %BOT_ERROR% >> %LOGFILE%

if %BOT_ERROR% NEQ 0 (
    echo.
    echo [ERROR] Bot mengalami error!
    echo Check bot_output.txt untuk detail error
    echo Check %LOGFILE% untuk debug info
    pause
)

REM Cleanup temporary files  
del temp_profiles.json >nul 2>&1
del temp_profile_output.txt >nul 2>&1

echo.
echo ================================================
echo              BOT SELESAI
echo ================================================
echo.
echo Log tersimpan di: %LOGFILE%
echo Output tersimpan di: bot_output.txt
echo.
pause
