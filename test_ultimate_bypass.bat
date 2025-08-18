@echo off
echo.
echo ========================================
echo      ULTIMATE BYPASS BOT LAUNCHER
echo ========================================
echo.

REM Check dependencies
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found!
    pause
    exit /b 1
)

echo [INFO] Installing/checking dependencies...

REM Install selenium
python -c "import selenium" >nul 2>&1
if errorlevel 1 (
    echo [INSTALL] Installing selenium...
    pip install selenium
)

REM Install undetected-chromedriver
echo [INSTALL] Installing undetected-chromedriver...
pip install undetected-chromedriver

echo [SUCCESS] Dependencies ready!
echo.

echo ========================================
echo        ULTIMATE BYPASS BOT v1.0
echo ========================================
echo.
echo Features:
echo - 5 Advanced bypass techniques per profile
echo - Ultimate stealth configuration
echo - Extended session maintenance
echo - Maximum anti-detection
echo.
echo Techniques:
echo 1. Iframe embedding
echo 2. JavaScript navigation
echo 3. Proxy referrer chain
echo 4. Meta refresh redirect
echo 5. Form POST redirect
echo.

python ultimate_bypass_bot.py

echo.
pause
