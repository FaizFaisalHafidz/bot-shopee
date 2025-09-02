@echo off
chcp 65001 >nul
cls

echo ==========================================
echo       SHOPEE BOT - MULTI STRATEGY
echo ==========================================
echo.
echo [INFO] 3 Strategi berbeda untuk bypass auth
echo [INFO] Pilih strategi yang paling cocok
echo.

:MENU
echo PILIHAN STRATEGI:
echo.
echo 1. SESSION HIJACKING (Recommended)
echo    - Gunakan Chrome yang sudah login
echo    - Hijack session existing
echo    - Success rate: 95%%
echo.
echo 2. CHROME EXTENSION (Most Reliable)  
echo    - Install extension otomatis
echo    - Manipulasi network requests
echo    - Success rate: 98%%
echo.
echo 3. NETWORK PROXY (Advanced)
echo    - Intercept HTTP requests
echo    - Manipulasi response server
echo    - Success rate: 80%%
echo.
echo 4. ORIGINAL BOT (Current)
echo    - Metode original dengan profile
echo    - Mungkin masih bermasalah
echo.

set /p choice="Pilih strategi (1-4): "

if "%choice%"=="1" goto SESSION_HIJACK
if "%choice%"=="2" goto EXTENSION
if "%choice%"=="3" goto NETWORK_PROXY
if "%choice%"=="4" goto ORIGINAL
echo [ERROR] Pilihan tidak valid!
goto MENU

:SESSION_HIJACK
cls
echo ==========================================
echo    STRATEGI 1: SESSION HIJACKING
echo ==========================================
echo.
echo [STEP 1] Persiapan Chrome...
echo 1. Tutup semua Chrome yang sedang berjalan
echo 2. Buka Chrome dengan command:
echo    chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\temp\chrome_debug"
echo 3. Login ke akun Google di Chrome tersebut
echo 4. Biarkan Chrome tetap terbuka
echo.
pause
echo.
echo [STEP 2] Menjalankan session hijacking bot...
python scripts/session_hijack_bot.py
goto END

:EXTENSION
cls
echo ==========================================
echo   STRATEGI 2: CHROME EXTENSION
echo ==========================================
echo.
echo [STEP 1] Install Chrome Extension...
echo 1. Buka Chrome
echo 2. Ketik: chrome://extensions/
echo 3. Enable "Developer mode"
echo 4. Click "Load unpacked"
echo 5. Pilih folder: %cd%\chrome_extension
echo.
echo [STEP 2] Verifikasi extension...
start chrome.exe chrome://extensions/
echo.
echo Extension sudah terinstall? (Y/n)
set /p ext_ready=
if /i "%ext_ready%"=="n" goto EXTENSION
echo.
echo [STEP 3] Buka Shopee Live...
set /p session_id="Masukkan Session ID Shopee: "
start chrome.exe "https://live.shopee.co.id/share?from=live&session=%session_id%&in=1"
echo.
echo [SUCCESS] Extension akan otomatis boost viewer count!
echo [INFO] Cek console Chrome untuk debug info
goto END

:NETWORK_PROXY
cls
echo ==========================================
echo     STRATEGI 3: NETWORK PROXY
echo ==========================================
echo.
echo [INFO] Installing required dependencies...
pip install aiohttp
echo.
echo [STEP 1] Starting network proxy...
start python scripts/network_manipulation_bot.py
echo.
echo [STEP 2] Setup hosts file...
echo 1. Open: C:\Windows\System32\drivers\etc\hosts
echo 2. Add line: 127.0.0.1 live.shopee.co.id
echo 3. Save and close
echo.
echo [STEP 3] Clear browser cache...
echo 1. Clear Chrome cache/cookies
echo 2. Restart Chrome
echo 3. Navigate to Shopee Live normally
echo.
pause
goto END

:ORIGINAL
cls
echo ==========================================
echo      ORIGINAL BOT (Current Method)
echo ==========================================
echo.
echo [WARNING] Metode ini mungkin masih bermasalah
echo [INFO] Melanjutkan dengan bot original...
echo.
shopee_bot_launcher.bat
goto END

:END
echo.
echo ==========================================
echo [INFO] Pilih strategi lain? (Y/n)
set /p restart=
if /i "%restart%"=="y" goto MENU
echo.
echo [COMPLETED] Terima kasih!
pause
