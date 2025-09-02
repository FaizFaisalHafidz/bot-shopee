@echo off
chcp 65001 > nul
echo [INFO] Checking Chrome processes...

echo.
echo === ACTIVE CHROME PROCESSES ===
tasklist | findstr /i "chrome.exe" || echo No Chrome processes found

echo.
echo === KILL ALL CHROME? ===
echo WARNING: This will close all Chrome windows including your current browsing
set /p choice="Do you want to kill all Chrome processes? (y/N): "

if /i "%choice%"=="y" (
    echo [INFO] Killing all Chrome processes...
    taskkill /f /im chrome.exe /t 2>nul
    timeout /t 2 /nobreak > nul
    echo [SUCCESS] Chrome processes terminated
) else (
    echo [INFO] Keeping Chrome processes active
    echo [WARNING] Bot may fail if Chrome profiles are in use
)

echo.
echo Press any key to continue...
pause > nul
