@echo off
echo.
echo ========================================
echo    SIMPLE SHOPEE BOT - DIRECT APPROACH
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python tidak ditemukan!
    echo Silakan install Python terlebih dahulu.
    echo Download dari: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

REM Check if required packages are installed
echo [INFO] Checking dependencies...

python -c "import selenium" >nul 2>&1
if errorlevel 1 (
    echo [INSTALL] Installing selenium...
    pip install selenium
    if errorlevel 1 (
        echo [ERROR] Failed to install selenium!
        pause
        exit /b 1
    )
)

python -c "import undetected_chromedriver" >nul 2>&1
if errorlevel 1 (
    echo [INSTALL] Installing undetected-chromedriver...
    pip install undetected-chromedriver
    if errorlevel 1 (
        echo [WARNING] Failed to install undetected-chromedriver, using regular selenium
    )
)

echo [SUCCESS] All dependencies ready!
echo.

REM Check for input.csv
if not exist "input.csv" (
    echo [ERROR] File input.csv tidak ditemukan!
    echo Pastikan file input.csv berisi cookie akun Shopee ada di folder ini.
    echo Format: SPC_U=...; SPC_T_ID=...; csrftoken=...; (satu baris per akun)
    echo.
    pause
    exit /b 1
)

echo [SUCCESS] Found input.csv file
echo.

echo ========================================
echo        MENJALANKAN SIMPLE BOT
echo ========================================
echo.
echo Mode: NO API Verification (Direct)
echo Strategi: Cookie Injection + Direct Navigation
echo Target: Bypass Shopee detection dengan cara sederhana
echo.

REM Run the simple bot
python simple_direct_bot.py

if errorlevel 1 (
    echo.
    echo [ERROR] Bot mengalami error!
    echo Coba jalankan ulang atau cek log error di atas.
) else (
    echo.
    echo [SUCCESS] Simple Bot selesai!
)

echo.
pause
