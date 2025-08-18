@echo off
REM Install webdriver-manager untuk auto ChromeDriver management
REM Solusi permanen untuk masalah ChromeDriver version mismatch

title Install webdriver-manager - Auto ChromeDriver Solution

echo 🔄 WEBDRIVER-MANAGER INSTALLER
echo ===============================
echo This will install webdriver-manager untuk automatic ChromeDriver management
echo No more manual ChromeDriver downloads needed!
echo.

echo ✅ Benefits:
echo    • Auto-download compatible ChromeDriver
echo    • No version mismatch issues
echo    • Always up-to-date ChromeDriver
echo    • Works with any Chrome version
echo.

pause

echo 📦 Installing webdriver-manager...
echo.

pip install webdriver-manager

if %errorlevel%==0 (
    echo ✅ webdriver-manager installed successfully!
    echo.
    
    echo 🧪 Testing webdriver-manager...
    python -c "from webdriver_manager.chrome import ChromeDriverManager; print('✅ webdriver-manager import OK')" 2>nul
    
    if %errorlevel%==0 (
        echo ✅ webdriver-manager is working!
        echo.
        
        echo 🎉 INSTALLATION COMPLETE!
        echo =========================
        echo.
        echo webdriver-manager will now:
        echo 1. Auto-detect your Chrome version
        echo 2. Download compatible ChromeDriver
        echo 3. Manage ChromeDriver automatically
        echo.
        echo 🚀 Ready to test browser bot:
        echo    python browser_bot.py
        echo.
        echo No more ChromeDriver version issues! 🎯
        
    ) else (
        echo ⚠️  webdriver-manager installed but import test failed
        echo This might still work when running the bot
    )
    
) else (
    echo ❌ webdriver-manager installation failed!
    echo.
    echo 💡 Alternative solutions:
    echo 1. Run: fix_chromedriver_version.bat
    echo 2. Or manually download ChromeDriver 127.x
    echo 3. Or try: python -m pip install webdriver-manager
)

echo.
echo Press any key to exit...
pause >nul
