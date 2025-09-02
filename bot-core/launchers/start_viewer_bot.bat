@echo off
echo ==========================================
echo    SHOPEE VIEWER BOT - SESSION COOKIES
echo ==========================================
echo.

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js not found! Please install Node.js first.
    echo Download from: https://nodejs.org/
    pause
    exit /b 1
)

REM Check if puppeteer is installed
if not exist "node_modules\puppeteer" (
    echo [INFO] Installing Puppeteer...
    npm install puppeteer
)

REM Get session ID and viewer count from user
set /p SESSION_ID="Enter Session ID (e.g., 157658364): "
set /p VIEWER_COUNT="Enter Viewer Count (1-28): "

if "%SESSION_ID%"=="" (
    echo [ERROR] Session ID cannot be empty!
    pause
    exit /b 1
)

if "%VIEWER_COUNT%"=="" set VIEWER_COUNT=5

echo.
echo [INFO] Starting bot with Session: %SESSION_ID%
echo [INFO] Viewer Count: %VIEWER_COUNT%
echo [INFO] Using cookies from input.csv
echo.

REM Run the Node.js bot
node generatex_4c.js %SESSION_ID% %VIEWER_COUNT%

pause
