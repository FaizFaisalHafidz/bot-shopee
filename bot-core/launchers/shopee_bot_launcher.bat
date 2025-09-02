@echo off
chcp 65001 > nul
cls
echo ==========================================
echo       SHOPEE LIVE VIEWER BOT v2.0
echo ==========================================
echo.

echo [INFO] Bot dengan sistem Gmail profile detection
echo [INFO] Fresh Chrome profiles untuk setiap viewer  
echo [INFO] Zero profile conflicts - Safe untuk deploy
echo.

cd /d "%~dp0"

echo [STEP 1] Deteksi Gmail profiles...
echo.
python scripts/detect_profiles_clean.py
if errorlevel 1 (
    echo.
    echo [ERROR] Gagal mendeteksi Chrome profiles
    echo [HELP] Solusi:
    echo   1. Pastikan Chrome sudah diinstall
    echo   2. Buka Chrome dan login ke akun Gmail
    echo   3. Tutup Chrome dan coba lagi
    pause
    exit /b 1
)

echo.
echo [STEP 2] Mempersiapkan environment...
echo [INFO] Chrome processes akan dihentikan otomatis oleh bot
echo [SUCCESS] Environment preparation ready

echo.
echo [STEP 3] Konfigurasi bot...
set /p session_id="Shopee Live Session ID: "
echo.
echo Pilihan jumlah viewers:
echo   1 = 1 viewer (testing)
echo   2 = 2 viewers (recommended) 
echo   3 = 3 viewers (maximum)
set /p num_viewers="Pilih jumlah viewers (1-3): "

if "%num_viewers%"=="" set num_viewers=1
if %num_viewers% GTR 3 set num_viewers=3
if %num_viewers% LSS 1 set num_viewers=1

set delay=5

echo.
echo ==========================================
echo KONFIGURASI FINAL
echo ==========================================
echo Session ID    : %session_id%
echo Viewers       : %num_viewers% Gmail accounts
echo Delay         : %delay% detik per aksi
echo Mode          : Fresh isolated profiles
echo Chrome        : Auto-detected system Chrome
echo ==========================================
echo.

set /p confirm="Mulai bot sekarang? (Y/n): "
if /i "%confirm%"=="n" (
    echo.
    echo [INFO] Dibatalkan oleh pengguna
    pause
    exit /b 0
)

echo.
echo [STEP 4] Menjalankan Shopee Live Bot...
echo ==========================================
cd scripts
python shopee_bot.py %session_id% %num_viewers% %delay%

echo.
echo ==========================================
echo [COMPLETED] Bot session selesai
echo.

echo [INFO] Summary:
echo   - Bot viewers: %num_viewers%
echo   - Session ID: %session_id%
echo   - Status: Completed
echo.

if exist "..\sessions\bot_viewers" (
    echo [CLEANUP] Temporary profiles akan dibersihkan otomatis pada run berikutnya
)

echo.
echo Tekan tombol apapun untuk keluar...
pause > nul
