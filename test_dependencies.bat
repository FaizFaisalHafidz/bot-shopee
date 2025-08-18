@echo off
REM Test Advanced Bot Dependencies
REM Verify semua requirements sebelum run bot

title Test Advanced Bot Dependencies

echo 🧪 TESTING ADVANCED BOT DEPENDENCIES
echo =====================================
echo.

echo Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python tidak ditemukan!
    echo 💡 Install Python dari https://python.org
    goto :end
) else (
    echo ✅ Python found:
    python --version
)

echo.
echo Running dependency test...
echo.

python test_advanced_bot.py

:end
echo.
pause
