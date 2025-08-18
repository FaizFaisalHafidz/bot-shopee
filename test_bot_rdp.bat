@echo off
REM Quick test script untuk bot Shopee di RDP
REM Test semua komponen sebelum production run

echo 🧪 Testing Shopee Bot Components...
echo.

REM Test Python
echo 📋 Testing Python...
python --version
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Python test failed
    exit /b 1
)

REM Test imports
echo 📦 Testing Python packages...
python -c "import requests, time, random, json, csv, threading; print('✅ All packages imported successfully')"
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Package import failed
    echo 🔧 Run: pip install -r requirements.txt
    exit /b 1
)

REM Test input.csv
echo 📄 Testing input.csv...
if not exist input.csv (
    echo ❌ input.csv not found!
    echo 📝 Please create input.csv with your Shopee cookies
    exit /b 1
)

REM Count accounts in input.csv
for /f %%i in ('type input.csv ^| find /c /v ""') do set /a lines=%%i
for /f %%i in ('type input.csv ^| findstr /r "^#" ^| find /c /v ""') do set /a comments=%%i
set /a accounts=%lines%-%comments%

echo ✅ Found %accounts% accounts in input.csv
echo.

REM Test main.py exists
if not exist main.py (
    echo ❌ main.py not found!
    exit /b 1
)

echo ✅ All tests passed!
echo.
echo 🚀 Ready to run bot:
echo    python main.py
echo.
echo 📋 Bot options:
echo    1 = Like Bot
echo    2 = Viewer Bot  
echo    3 = Add to Cart Bot
echo.
pause

REM Optional: Run bot directly
set /p choice="Run bot now? (y/n): "
if /i "%choice%"=="y" (
    echo.
    echo 🚀 Starting Shopee Bot...
    python main.py
)
