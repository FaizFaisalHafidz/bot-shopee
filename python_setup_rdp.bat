@echo off
REM Auto Python Setup untuk RDP Windows
REM Script ini akan download dan install Python otomatis

echo 🐍 Python Auto-Setup untuk Shopee Bot RDP
echo ==========================================
echo.

REM Check if Python already installed
python --version >nul 2>&1
if %errorlevel%==0 (
    echo ✅ Python sudah terinstall!
    python --version
    goto install_packages
)

echo 📥 Python belum terinstall. Starting auto-download...
echo.

REM Download Python 3.11
set PYTHON_URL=https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe
set PYTHON_INSTALLER=python-installer.exe

echo 📥 Downloading Python 3.11.9...
powershell -Command "Invoke-WebRequest -Uri '%PYTHON_URL%' -OutFile '%PYTHON_INSTALLER%'"

if not exist %PYTHON_INSTALLER% (
    echo ❌ Download gagal! 
    echo 💡 Manual download dari: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Download complete!
echo.

echo 🔧 Installing Python...
echo ⚠️  PENTING: Installer akan berjalan dengan opsi:
echo    ✅ Add to PATH
echo    ✅ Install for all users  
echo    ✅ Include pip
echo.

REM Install Python with required options
%PYTHON_INSTALLER% /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1

echo ⏱️  Waiting for installation to complete...
timeout /t 30 /nobreak

REM Clean up installer
del %PYTHON_INSTALLER%

echo.
echo 🔍 Verifying Python installation...

REM Refresh PATH
call refreshenv 2>nul || echo Refreshing environment...

python --version
if %errorlevel%==0 (
    echo ✅ Python berhasil terinstall!
) else (
    echo ❌ Python installation gagal!
    echo 💡 Coba manual install dari python.org
    pause
    exit /b 1
)

:install_packages
echo.
echo 📦 Installing bot dependencies...

pip install requests urllib3

if %errorlevel%==0 (
    echo ✅ Dependencies berhasil terinstall!
) else (
    echo ❌ Package installation gagal!
    echo 💡 Coba manual: pip install requests urllib3
)

echo.
echo 🎯 Python setup complete!
echo.
echo 📋 Next steps:
echo 1. Copy bot files ke C:\shopee-bot\
echo 2. Edit input.csv dengan cookies Anda
echo 3. Run: python main.py
echo.

pause
