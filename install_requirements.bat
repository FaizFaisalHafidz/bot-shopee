@echo off
REM Install Requirements untuk Shopee Bot di RDP
REM Script otomatis install semua dependencies

echo 📦 Installing Shopee Bot Requirements
echo ====================================
echo.

REM Check if Python installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found!
    echo 💡 Please install Python first from https://python.org
    pause
    exit /b 1
)

echo ✅ Python found:
python --version
echo.

REM Check if pip available
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip not found!
    echo 🔧 Trying to install pip...
    python -m ensurepip --upgrade
    python -m pip install --upgrade pip
)

echo ✅ pip found:
pip --version
echo.

echo 📦 Installing required packages...
echo.

REM Install main packages
echo 🔄 Installing requests...
pip install requests
if %errorlevel%==0 (
    echo ✅ requests installed successfully
) else (
    echo ❌ Failed to install requests
)

echo.
echo 🔄 Installing urllib3...
pip install urllib3
if %errorlevel%==0 (
    echo ✅ urllib3 installed successfully
) else (
    echo ❌ Failed to install urllib3
)

echo.
echo 🔄 Installing additional packages (optional)...
pip install certifi charset-normalizer idna

echo.
echo 🧪 Testing imports...
python -c "import requests; print('✅ requests OK')" 2>nul || echo "❌ requests import failed"
python -c "import urllib3; print('✅ urllib3 OK')" 2>nul || echo "❌ urllib3 import failed"
python -c "import json; print('✅ json OK')" 2>nul || echo "❌ json import failed"
python -c "import csv; print('✅ csv OK')" 2>nul || echo "❌ csv import failed"
python -c "import threading; print('✅ threading OK')" 2>nul || echo "❌ threading import failed"

echo.
echo 🎉 Requirements installation complete!
echo.
echo 📋 Installed packages:
pip list | findstr -i "requests urllib3 certifi"

echo.
echo 💡 You can now run the bot:
echo    python main.py
echo.

pause
