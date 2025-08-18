@echo off
REM Setup script untuk Windows laptop
REM Bot Shopee Live Streaming

echo 🚀 Setting up Shopee Bot di Windows laptop...
echo.

REM Check if Python installed
echo 📋 Checking Python installation...
python --version
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Python not found! Please install Python 3.11+ first
    echo Download from: https://python.org
    pause
    exit /b 1
)

echo ✅ Python found!
echo.

REM Check if pip available
echo 📋 Checking pip...
pip --version
if %ERRORLEVEL% NEQ 0 (
    echo ❌ pip not found! Something wrong with Python installation
    pause
    exit /b 1
)

echo ✅ pip found!
echo.

REM Create virtual environment
echo 🔧 Creating virtual environment...
python -m venv venv
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Failed to create virtual environment
    pause
    exit /b 1
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo 📦 Installing requirements...
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Failed to install requirements
    pause
    exit /b 1
)

echo.
echo ✅ Setup complete!
echo.
echo 📝 Next steps:
echo 1. Edit input.csv with your Shopee cookies
echo 2. Run: python main.py
echo 3. Choose bot mode (1=Like, 2=Viewer, 3=ATC)
echo 4. Enter Shopee live session ID
echo.

pause
