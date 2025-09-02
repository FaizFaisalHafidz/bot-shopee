@echo off
chcp 437 >nul
title Bot Shopee Live - Menggunakan Profile Chrome yang Ada
color 0A
cls

echo.
echo ================================================
echo        BOT SHOPEE LIVE VIEWER v3.0
echo        Menggunakan Profile Chrome yang Ada
echo ================================================
echo.

REM Cek apakah Python terinstall
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python belum terinstall!
    echo.
    echo Cara install Python:
    echo    1. Buka Microsoft Store
    echo    2. Cari "Python 3.11"  
    echo    3. Install dan restart komputer
    echo.
    echo    ATAU download dari: https://python.org/downloads
    echo    PASTIKAN centang "Add Python to PATH" saat install!
    echo.
    pause
    exit /b 1
)

echo [OK] Python ditemukan:
python --version
echo.

REM Input konfigurasi
echo ================================================
echo              KONFIGURASI BOT
echo ================================================
echo.

set /p session="Masukkan Session ID Shopee Live: "
if "%session%"=="" (
    echo [ERROR] Session ID wajib diisi!
    pause
    exit /b 1
)

echo.
echo [INFO] Mencari profile Chrome yang tersedia...
echo.

REM Jalankan script deteksi profile
python scripts\detect_profiles.py
if errorlevel 1 (
    echo [ERROR] Gagal mendeteksi profile Chrome!
    pause
    exit /b 1
)

REM Ambil jumlah profile dari output
for /f "tokens=2 delims==" %%i in ('python scripts\detect_profiles.py ^| findstr "PROFILE_COUNT"') do set profile_count=%%i

if %profile_count%==0 (
    echo [ERROR] Tidak ada profile Chrome yang valid ditemukan!
    echo.
    echo [INFO] Pastikan sudah pernah login ke Chrome dan buat profile
    echo.
    pause
    exit /b 1
)

echo.
set /p viewers="Berapa viewer yang ingin dibuat (max %profile_count%): "
if "%viewers%"=="" set viewers=1

if %viewers% GTR %profile_count% (
    echo [WARNING] Jumlah viewer tidak boleh lebih dari %profile_count% profile!
    set viewers=%profile_count%
)

set /p delay="Jeda antar viewer dalam detik (default 3): "
if "%delay%"=="" set delay=3

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
if /i not "%confirm%"=="y" (
    echo [INFO] Bot dibatalkan.
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
python -c "import selenium,webdriver_manager" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing selenium dan webdriver-manager...
    python -m pip install selenium webdriver-manager --quiet
    if errorlevel 1 (
        echo [ERROR] Gagal install dependencies!
        pause
        exit /b 1
    )
)

echo [OK] Dependencies siap!
echo.

REM Jalankan bot
echo [INFO] Menjalankan bot...
echo.
python scripts\shopee_bot.py %session% %viewers% %delay%

REM Cleanup temporary files
del temp_profiles.json >nul 2>&1

echo.
echo ================================================
echo              BOT SELESAI
echo ================================================
echo.
pause
