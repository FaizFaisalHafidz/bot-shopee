@echo off
REM Multi-RDP Execution Strategy
REM Shopee Bot - 27 Viewers from 3 Different IPs

echo 🚀 Multi-RDP Shopee Bot Strategy
echo ================================
echo.

REM Configuration - Edit sesuai RDP Anda
set RDP1_IP=MASUKKAN_IP_RDP_1
set RDP2_IP=MASUKKAN_IP_RDP_2  
set RDP3_IP=MASUKKAN_IP_RDP_3

set RDP_USER=Administrator
set RDP_PASS=MASUKKAN_PASSWORD

echo 📋 RDP Configuration:
echo RDP-1 (Singapore): %RDP1_IP% - Akun 1-9
echo RDP-2 (Singapore): %RDP2_IP% - Akun 10-18  
echo RDP-3 (Tokyo):     %RDP3_IP% - Akun 19-27
echo.

REM Get Session ID dari user
set /p SESSION_ID="🔗 Enter Shopee Live Session ID: "
if "%SESSION_ID%"=="" (
    echo ❌ Session ID tidak boleh kosong!
    pause
    exit /b 1
)

echo.
echo ✅ Session ID: %SESSION_ID%
echo 🎯 Target: +27 viewers dari 3 IP berbeda
echo.

echo 📊 Execution Plan:
echo 1. Connect RDP-1 → Run VIEWER bot (akun 1-9)
echo 2. Wait 30 seconds
echo 3. Connect RDP-2 → Run VIEWER bot (akun 10-18)
echo 4. Wait 30 seconds  
echo 5. Connect RDP-3 → Run VIEWER bot (akun 19-27)
echo.

set /p confirm="🚀 Start execution? (y/n): "
if /i not "%confirm%"=="y" exit /b 0

echo.
echo 🚀 Starting Multi-RDP Bot Execution...
echo.

REM Step 1: RDP-1
echo [%time%] 📍 Step 1: Connecting to RDP-1 (%RDP1_IP%)
echo 🎯 Target: Run VIEWER bot dengan akun 1-9
echo 💡 Instruction: Setelah connect, jalankan:
echo    cd C:\shopee-bot
echo    python main.py
echo    Pilih mode: 2 (VIEWER)  
echo    Session ID: %SESSION_ID%
echo.

REM Open RDP connection
start mstsc /v:%RDP1_IP%

echo ⏱️  Waiting 10 seconds untuk RDP-1 connection...
timeout /t 10 /nobreak > nul

echo 📢 RDP-1 should be connected now!
echo 🔧 Setup bot di RDP-1, kemudian press any key untuk lanjut...
pause > nul

echo.
echo ⏱️  Waiting 30 seconds before next RDP...
echo 💡 RDP-1 bot should be running in background
timeout /t 30 /nobreak

REM Step 2: RDP-2  
echo.
echo [%time%] 📍 Step 2: Connecting to RDP-2 (%RDP2_IP%)
echo 🎯 Target: Run VIEWER bot dengan akun 10-18
echo 💡 Instruction: Setelah connect, jalankan:
echo    cd C:\shopee-bot
echo    python main.py
echo    Pilih mode: 2 (VIEWER)
echo    Session ID: %SESSION_ID%
echo.

start mstsc /v:%RDP2_IP%

echo ⏱️  Waiting 10 seconds untuk RDP-2 connection...
timeout /t 10 /nobreak > nul

echo 📢 RDP-2 should be connected now!  
echo 🔧 Setup bot di RDP-2, kemudian press any key untuk lanjut...
pause > nul

echo.
echo ⏱️  Waiting 30 seconds before next RDP...
echo 💡 RDP-1 & RDP-2 bots should be running
timeout /t 30 /nobreak

REM Step 3: RDP-3
echo.
echo [%time%] 📍 Step 3: Connecting to RDP-3 (%RDP3_IP%)  
echo 🎯 Target: Run VIEWER bot dengan akun 19-27
echo 💡 Instruction: Setelah connect, jalankan:
echo    cd C:\shopee-bot  
echo    python main.py
echo    Pilih mode: 2 (VIEWER)
echo    Session ID: %SESSION_ID%
echo.

start mstsc /v:%RDP3_IP%

echo ⏱️  Waiting 10 seconds untuk RDP-3 connection...
timeout /t 10 /nobreak > nul

echo 📢 RDP-3 should be connected now!
echo 🔧 Setup bot di RDP-3, kemudian press any key...
pause > nul

echo.
echo 🎉 ALL RDP CONNECTIONS ESTABLISHED!
echo.
echo 📊 Current Status:
echo ✅ RDP-1: Running VIEWER bot (akun 1-9)
echo ✅ RDP-2: Running VIEWER bot (akun 10-18)  
echo ✅ RDP-3: Running VIEWER bot (akun 19-27)
echo.
echo 🎯 Expected Result: +27 real viewers
echo 🌍 From 3 different IP addresses
echo ⏱️  Bot execution time: ~2-5 minutes
echo.
echo 💡 Monitor each RDP untuk melihat progress
echo 📊 Check live stream counter untuk confirm viewers
echo.

pause
