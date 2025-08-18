@echo off
echo ================================================================
echo         SHOPEE BOT - RDP WINDOWS SETUP SCRIPT
echo                    BY FLASHCODE  
echo ================================================================
echo.

echo [1/6] Checking Python installation...
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python not found! 
    echo Please install Python 3.8+ first from python.org
    pause
    exit /b 1
)

python --version
echo Python OK!
echo.

echo [2/6] Upgrading pip...
python -m pip install --upgrade pip --quiet
echo Pip upgraded!
echo.

echo [3/6] Installing Selenium for browser automation...
python -m pip install selenium==4.15.0 --quiet
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to install Selenium!
    echo Trying alternative method...
    python -m pip install --user selenium==4.15.0 --quiet
)
echo Selenium installed!
echo.

echo [4/6] Installing other requirements...
python -m pip install requests urllib3 --quiet
echo Requirements installed!
echo.

echo [5/6] Checking Google Chrome installation...
set "CHROME_PATH="
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    set "CHROME_PATH=C:\Program Files\Google\Chrome\Application\chrome.exe"
)
if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" (
    set "CHROME_PATH=C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
)

if "%CHROME_PATH%"=="" (
    echo WARNING: Google Chrome not found!
    echo Please download and install Google Chrome manually:
    echo https://www.google.com/chrome/
    echo.
    echo Continue anyway? (y/n):
    set /p continue=
    if /i not "%continue%"=="y" (
        echo Setup cancelled.
        pause
        exit /b 1
    )
) else (
    echo Chrome found: %CHROME_PATH%
)
echo.

echo [6/6] Setting up ChromeDriver...

REM Get Chrome version for matching ChromeDriver
if not "%CHROME_PATH%"=="" (
    echo Getting Chrome version...
    for /f "tokens=*" %%i in ('"%CHROME_PATH%" --version 2^>nul') do set CHROME_VERSION=%%i
    echo Chrome version: %CHROME_VERSION%
)

REM Download ChromeDriver automatically
echo Downloading ChromeDriver...
echo NOTE: If download fails, manually download from:
echo https://chromedriver.chromium.org/downloads

REM Try to download ChromeDriver using PowerShell
powershell -Command "try { $response = Invoke-WebRequest -Uri 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE' -UseBasicParsing; $version = $response.Content.Trim(); Write-Host \"Latest ChromeDriver version: $version\"; $url = \"https://chromedriver.storage.googleapis.com/$version/chromedriver_win32.zip\"; Invoke-WebRequest -Uri $url -OutFile 'chromedriver.zip' -UseBasicParsing; Expand-Archive -Path 'chromedriver.zip' -DestinationPath '.' -Force; Remove-Item 'chromedriver.zip'; Write-Host 'ChromeDriver downloaded successfully!' } catch { Write-Host 'Download failed. Please download manually.' }" 2>nul

if exist "chromedriver.exe" (
    echo ChromeDriver setup complete!
) else (
    echo WARNING: ChromeDriver download failed!
    echo Please download ChromeDriver manually:
    echo 1. Go to https://chromedriver.chromium.org/downloads
    echo 2. Download version matching your Chrome
    echo 3. Extract chromedriver.exe to this folder
    echo.
)

echo.
echo ================================================================
echo                    SETUP COMPLETE!
echo ================================================================
echo.
echo RDP OPTIMIZED BOT is ready to use!
echo.
echo Available bots:
echo   1. rdp_optimized_bot.py  - RDP Windows specialized
echo   2. browser_bot.py        - Standard browser automation  
echo   3. main.py               - HTTP only (lightweight)
echo.
echo RECOMMENDED for RDP: rdp_optimized_bot.py
echo.
echo To run: python rdp_optimized_bot.py
echo.
echo ================================================================
echo                    TROUBLESHOOTING
echo ================================================================
echo.
echo If you get errors:
echo.
echo 1. SELENIUM IMPORT ERROR:
echo    pip install selenium==4.15.0
echo.
echo 2. CHROME/CHROMEDRIVER ERROR:
echo    - Install Google Chrome
echo    - Download matching ChromeDriver 
echo    - Place chromedriver.exe in bot folder
echo.
echo 3. PERMISSION ERROR:
echo    - Run as Administrator
echo    - Or use: pip install --user selenium
echo.
echo 4. PYTHON NOT FOUND:
echo    - Install Python 3.8+ from python.org
echo    - Add Python to PATH during installation
echo.
echo ================================================================

echo.
echo Setup complete! Press any key to exit...
pause >nul
