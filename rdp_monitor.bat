@echo off
REM Multi-RDP Performance Monitor
REM Check status semua RDP bot secara real-time

:monitor_loop
cls
echo 📊 Multi-RDP Bot Performance Monitor
echo =====================================
echo Updated: %date% %time%
echo.

REM Configuration  
set RDP1_IP=MASUKKAN_IP_RDP_1
set RDP2_IP=MASUKKAN_IP_RDP_2
set RDP3_IP=MASUKKAN_IP_RDP_3

echo 🌍 RDP Server Status:
echo.

REM Test RDP-1
echo 📍 RDP-1 (Singapore): %RDP1_IP%
ping -n 1 %RDP1_IP% > nul 2>&1
if %errorlevel%==0 (
    echo    Status: ✅ Online
) else (
    echo    Status: ❌ Offline
)
echo    Target: Akun 1-9 ^| Expected: +9 viewers
echo.

REM Test RDP-2  
echo 📍 RDP-2 (Singapore): %RDP2_IP%
ping -n 1 %RDP2_IP% > nul 2>&1
if %errorlevel%==0 (
    echo    Status: ✅ Online
) else (
    echo    Status: ❌ Offline  
)
echo    Target: Akun 10-18 ^| Expected: +9 viewers
echo.

REM Test RDP-3
echo 📍 RDP-3 (Tokyo): %RDP3_IP%  
ping -n 1 %RDP3_IP% > nul 2>&1
if %errorlevel%==0 (
    echo    Status: ✅ Online
) else (
    echo    Status: ❌ Offline
)
echo    Target: Akun 19-27 ^| Expected: +9 viewers
echo.

echo 🎯 Expected Total Impact: +27 Real Viewers
echo 📊 From 3 Different IP Addresses
echo.

echo 💡 Instructions:
echo 1. Monitor each RDP via Remote Desktop
echo 2. Check bot logs for success/failure  
echo 3. Verify live stream viewer count
echo 4. Troubleshoot any offline RDP
echo.

echo ⚡ Quick Actions:
echo [R] Refresh monitor
echo [C] Connect to specific RDP
echo [Q] Quit monitor
echo.

set /p choice="Select action: "

if /i "%choice%"=="r" goto monitor_loop
if /i "%choice%"=="q" exit /b 0

if /i "%choice%"=="c" (
    echo.
    echo 🔗 RDP Connection Options:
    echo [1] Connect to RDP-1 (%RDP1_IP%)
    echo [2] Connect to RDP-2 (%RDP2_IP%)  
    echo [3] Connect to RDP-3 (%RDP3_IP%)
    echo.
    
    set /p rdp_choice="Select RDP: "
    
    if "%rdp_choice%"=="1" start mstsc /v:%RDP1_IP%
    if "%rdp_choice%"=="2" start mstsc /v:%RDP2_IP%  
    if "%rdp_choice%"=="3" start mstsc /v:%RDP3_IP%
    
    echo ✅ RDP connection initiated
    timeout /t 2 > nul
)

goto monitor_loop
