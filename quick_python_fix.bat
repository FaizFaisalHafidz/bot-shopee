@echo off
REM Quick command line fix untuk Python Windows alias issue

echo 🚀 Quick Python Fix for Windows
echo ================================

echo Disabling Windows Python aliases...
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\App Paths\python.exe" /f 2>nul
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\App Paths\python3.exe" /f 2>nul

echo.
echo ✅ Aliases disabled!
echo.
echo 💡 Now you need to:
echo 1. Download Python from https://python.org
echo 2. Install with "Add to PATH" checked
echo 3. Restart Command Prompt
echo 4. Test: python --version
echo.

pause
