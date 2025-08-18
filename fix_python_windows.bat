@echo off
REM Fix "python was not found" error di Windows
REM Script untuk disable Python alias dan install Python proper

echo 🔧 Fixing "python was not found" Error
echo =====================================
echo.

echo 📋 Step 1: Disabling Windows Python Alias...

REM Disable Python alias yang mengarah ke Microsoft Store
echo Removing Python aliases...
reg delete HKCU\Software\Microsoft\Windows\CurrentVersion\App Paths\python.exe /f 2>nul
reg delete HKCU\Software\Microsoft\Windows\CurrentVersion\App Paths\python3.exe /f 2>nul

REM Disable via App Execution Aliases (Windows 10/11)
echo Checking App Execution Aliases...
powershell -Command "Get-AppxPackage *python* | Remove-AppxPackage" 2>nul

echo.
echo 📋 Step 2: Installing Python from python.org...

REM Check if we can access python.org
ping -n 1 python.org >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ No internet connection to download Python
    echo 💡 Manual solution:
    echo    1. Open Settings → Apps → App Execution Aliases
    echo    2. Turn OFF "Python" and "Python3" aliases
    echo    3. Download Python from https://python.org
    goto manual_instructions
)

REM Download Python installer
set PYTHON_URL=https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe
set PYTHON_INSTALLER=python-3.11.9-amd64.exe

echo 📥 Downloading Python 3.11.9 from python.org...
echo URL: %PYTHON_URL%

powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri '%PYTHON_URL%' -OutFile '%PYTHON_INSTALLER%'}"

if not exist "%PYTHON_INSTALLER%" (
    echo ❌ Download failed!
    goto manual_instructions
)

echo ✅ Download completed: %PYTHON_INSTALLER%
echo.

echo 🔧 Installing Python...
echo ⚠️  Installing with these options:
echo    ✅ Add Python to PATH
echo    ✅ Install for all users
echo    ✅ Include pip package manager

REM Install Python silently with all required options
"%PYTHON_INSTALLER%" /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1 AssociateFiles=1

echo.
echo ⏱️  Waiting for installation to complete (30 seconds)...
timeout /t 30 /nobreak >nul

REM Clean up installer
if exist "%PYTHON_INSTALLER%" del "%PYTHON_INSTALLER%"

echo.
echo 🔍 Testing Python installation...

REM Refresh environment variables
set PATH=%PATH%
for /f "tokens=2*" %%a in ('reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v PATH 2^>nul') do set "SysPath=%%b"
for /f "tokens=2*" %%a in ('reg query "HKCU\Environment" /v PATH 2^>nul') do set "UserPath=%%b"

REM Test Python
python --version 2>nul
if %errorlevel%==0 (
    echo ✅ Python installation successful!
    python --version
    
    echo.
    echo 🧪 Testing pip...
    pip --version
    
    if %errorlevel%==0 (
        echo ✅ pip is working!
        
        echo.
        echo 📦 Installing bot requirements...
        pip install requests urllib3
        
        echo.
        echo 🎉 Setup complete!
        echo 💡 You can now run: python main.py
    ) else (
        echo ⚠️  pip not working, trying to fix...
        python -m ensurepip --upgrade
        python -m pip install --upgrade pip
    )
    
) else (
    echo ❌ Python still not recognized!
    echo 💡 You may need to restart Command Prompt or reboot
    goto manual_instructions
)

goto end

:manual_instructions
echo.
echo 📋 MANUAL SOLUTION REQUIRED:
echo.
echo 1. Open Windows Settings
echo 2. Go to: Apps → App Execution Aliases
echo 3. Turn OFF these aliases:
echo    • App Installer (python.exe)
echo    • App Installer (python3.exe)
echo.
echo 4. Download Python manually:
echo    • Go to: https://www.python.org/downloads/
echo    • Download Python 3.11.x
echo    • IMPORTANT: Check "Add Python to PATH" during install
echo.
echo 5. Restart Command Prompt
echo 6. Test: python --version
echo.

:end
pause
