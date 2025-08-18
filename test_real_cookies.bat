@echo off
echo.
echo ========================================
echo        REAL COOKIE TESTER
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python tidak ditemukan!
    echo Silakan install Python terlebih dahulu.
    pause
    exit /b 1
)

REM Check and install selenium
echo [INFO] Checking selenium...
python -c "import selenium" >nul 2>&1
if errorlevel 1 (
    echo [INSTALL] Installing selenium...
    pip install selenium
)

REM Try to install undetected chromedriver
echo [INFO] Installing undetected-chromedriver...
pip install undetected-chromedriver

echo [SUCCESS] Dependencies ready!
echo.

REM Check for input.csv
if not exist "input.csv" (
    echo [ERROR] File input.csv tidak ditemukan!
    echo Buat file input.csv dengan format:
    echo SPC_U=...; SPC_T_ID=...; csrftoken=...;
    echo.
    pause
    exit /b 1
)

echo ========================================
echo     REAL BROWSER COOKIE TESTING
echo ========================================
echo.
echo Mode: Visual browser testing
echo Fungsi: Test apakah cookies bisa login
echo Output: working_cookies.csv (jika ada yang valid)
echo.

python real_cookie_tester.py

echo.
pause
