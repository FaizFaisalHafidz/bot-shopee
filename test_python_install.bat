@echo off
REM Quick test setelah install Python via .exe

echo 🧪 Testing Python Installation
echo ==============================
echo.

echo 📋 Testing Python...
python --version
if %errorlevel%==0 (
    echo ✅ Python installed successfully!
) else (
    echo ❌ Python not found! 
    echo 💡 Solutions:
    echo    1. Restart Command Prompt
    echo    2. Make sure you checked "Add to PATH" during install
    echo    3. Reinstall Python with "Add to PATH" option
    pause
    exit /b 1
)

echo.
echo 📋 Testing pip...
pip --version
if %errorlevel%==0 (
    echo ✅ pip is working!
) else (
    echo ❌ pip not found!
    echo 💡 Try: python -m ensurepip --upgrade
    pause
    exit /b 1
)

echo.
echo 📦 Installing bot requirements...
pip install requests urllib3

if %errorlevel%==0 (
    echo ✅ Requirements installed successfully!
) else (
    echo ❌ Failed to install requirements
    echo 💡 Check internet connection or try manual install
)

echo.
echo 🎉 Python setup complete!
echo 💡 You can now run: python main.py
echo.
pause
