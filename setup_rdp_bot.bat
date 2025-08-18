@echo off
REM Setup Bot Shopee di RDP Windows Server
REM Jalankan script ini di Command Prompt sebagai Administrator

echo 🚀 Setting up Shopee Bot di RDP Windows Server...
echo.

REM Check current directory
echo 📍 Current directory: %CD%
echo.

REM Check if Python installed
echo 📋 Checking Python installation...
python --version
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Python not found!
    echo 📥 Please install Python 3.11+ from https://python.org
    echo ✅ Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo ✅ Python found!
echo.

REM Check if requirements.txt exists
if not exist requirements.txt (
    echo ❌ requirements.txt not found!
    echo 📁 Make sure you're in the correct bot directory
    echo 📋 Directory should contain: main.py, requirements.txt, input.csv
    pause
    exit /b 1
)

echo 📦 Installing Python packages...
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Failed to install some packages
    echo 🔧 Trying with --upgrade flag...
    pip install -r requirements.txt --upgrade
)

echo.
echo ✅ Bot setup complete!
echo.
echo 📋 Next steps:
echo 1. Install Google Chrome for cookie harvesting
echo 2. Login to Shopee accounts and extract cookies  
echo 3. Edit input.csv with your cookies
echo 4. Test bot: python main.py
echo.

REM Check if input.csv exists and show sample
if exist input.csv (
    echo 📄 Current input.csv content:
    echo ----------------------------------------
    type input.csv
    echo ----------------------------------------
    echo.
)

echo 🎯 Ready to run bot!
echo 💡 Command: python main.py
echo.
pause
