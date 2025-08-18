@echo off
REM Shopee Live Bot - Configurable Viewers for Windows RDP
REM Script untuk mengatur jumlah viewers sesuai jumlah RDP

echo 🚀 Shopee Live Bot - Configurable Viewers
echo ==========================================
echo.

REM Function to count accounts in input.csv
set TOTAL_ACCOUNTS=0
if exist input.csv (
    for /f %%i in ('type input.csv ^| findstr /v /r "^#" ^| findstr /v /r "^[[:space:]]*$" ^| find /c /v ""') do set TOTAL_ACCOUNTS=%%i
)

echo 📊 Available accounts in input.csv: %TOTAL_ACCOUNTS%

if %TOTAL_ACCOUNTS%==0 (
    echo ❌ No valid accounts found in input.csv!
    echo 💡 Please add your Shopee cookies to input.csv
    pause
    exit /b 1
)

echo.
echo 🎯 RDP Configuration Options:
echo 1. Single RDP ^(1-9 viewers^) - Your current setup
echo 2. Dual RDP ^(10-18 viewers^) - 2 servers
echo 3. Triple RDP ^(19-27 viewers^) - 3 servers  
echo 4. Custom viewers - Manual input
echo.

set /p config_choice="🔢 Choose configuration [1-4]: "

if "%config_choice%"=="1" (
    set MAX_VIEWERS=9
    echo ✅ Single RDP mode: Maximum 9 viewers
) else if "%config_choice%"=="2" (
    set MAX_VIEWERS=18
    echo ✅ Dual RDP mode: Maximum 18 viewers
) else if "%config_choice%"=="3" (
    set MAX_VIEWERS=27
    echo ✅ Triple RDP mode: Maximum 27 viewers
) else if "%config_choice%"=="4" (
    set /p custom_viewers="🔢 Enter desired number of viewers (max %TOTAL_ACCOUNTS%): "
    set MAX_VIEWERS=%custom_viewers%
    echo ✅ Custom mode: %MAX_VIEWERS% viewers
) else (
    echo ❌ Invalid choice. Using Single RDP mode ^(9 viewers^)
    set MAX_VIEWERS=9
)

REM Limit viewers to available accounts
if %MAX_VIEWERS% GTR %TOTAL_ACCOUNTS% (
    echo ⚠️  Requested %MAX_VIEWERS% viewers, but only %TOTAL_ACCOUNTS% accounts available
    set MAX_VIEWERS=%TOTAL_ACCOUNTS%
)

echo.
echo 📋 Bot Configuration:
echo    • Available accounts: %TOTAL_ACCOUNTS%
echo    • Target viewers: %MAX_VIEWERS%
echo    • RDP Recommendation: %config_choice% server(s)
echo.

REM Create temporary input file with limited accounts
echo 🔧 Creating temporary input file with %MAX_VIEWERS% accounts...

REM Copy header comments first
type nul > input_temp.csv
for /f "delims=" %%i in ('findstr /r "^#" input.csv') do echo %%i >> input_temp.csv

REM Add the required number of accounts
set count=0
for /f "delims=" %%i in ('findstr /v /r "^#" input.csv ^| findstr /v /r "^[[:space:]]*$"') do (
    if !count! LSS %MAX_VIEWERS% (
        echo %%i >> input_temp.csv
        set /a count+=1
    )
)

echo ✅ Temporary input created with %MAX_VIEWERS% accounts

REM Check Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found! Please install Python 3.11+
    pause
    exit /b 1
)

REM Install requirements
echo 📦 Installing dependencies...
pip install -r requirements.txt >nul 2>&1

REM Backup and replace input file
echo 🔄 Preparing bot configuration...
if exist input_backup.csv del input_backup.csv
ren input.csv input_backup.csv
ren input_temp.csv input.csv

echo.
echo ✅ Setup complete!
echo 🎯 Launching Shopee Live Bot with %MAX_VIEWERS% viewers...
echo 💡 Bot will process %MAX_VIEWERS% accounts for optimal RDP usage
echo.

REM Run the bot
python main.py

REM Restore original input file
echo.
echo 🔄 Restoring original configuration...
if exist input_temp.csv del input_temp.csv
ren input.csv input_temp.csv
ren input_backup.csv input.csv
del input_temp.csv

echo.
echo ✅ Bot execution completed!
echo 📊 Processed %MAX_VIEWERS% out of %TOTAL_ACCOUNTS% available accounts
echo 💡 Perfect for your current RDP setup!
echo.
pause
