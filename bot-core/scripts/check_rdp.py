#!/usr/bin/env python3
"""
RDP ENVIRONMENT CHECKER
Check if everything is ready for RDP bot
"""

import sys
import os
import subprocess

def check_python():
    print("1. Python Check:")
    print(f"   Version: {sys.version}")
    print(f"   Path: {sys.executable}")
    return True

def check_pip_packages():
    print("\n2. Required Packages Check:")
    packages = ['selenium', 'webdriver_manager', 'requests']
    
    for package in packages:
        try:
            __import__(package)
            print(f"   ✅ {package}: OK")
        except ImportError:
            print(f"   ❌ {package}: Missing")
            return False
    return True

def check_chrome():
    print("\n3. Chrome Check:")
    chrome_paths = [
        "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
        "/usr/bin/google-chrome",
        "/usr/bin/chromium-browser",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    ]
    
    for path in chrome_paths:
        if os.path.exists(path):
            print(f"   ✅ Chrome found: {path}")
            return True
    
    print("   ❌ Chrome not found in standard locations")
    return False

def check_webdriver():
    print("\n4. WebDriver Check:")
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        driver_path = ChromeDriverManager().install()
        print(f"   ✅ ChromeDriver: {driver_path}")
        return True
    except Exception as e:
        print(f"   ❌ ChromeDriver error: {e}")
        return False

def check_bot_files():
    print("\n5. Bot Files Check:")
    required_files = [
        'bot-core/bots/real_url_bot_rdp.py',
        'requirements.txt',
        'run.bat'
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"   ✅ {file}: OK")
        else:
            print(f"   ❌ {file}: Missing")
            return False
    return True

def test_basic_chrome():
    print("\n6. Chrome Test (Basic):")
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
        
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        driver.get('https://google.com')
        title = driver.title
        driver.quit()
        
        print(f"   ✅ Chrome test passed: {title}")
        return True
        
    except Exception as e:
        print(f"   ❌ Chrome test failed: {e}")
        return False

def main():
    print("="*60)
    print("        RDP ENVIRONMENT CHECKER")
    print("="*60)
    
    checks = [
        check_python,
        check_pip_packages,
        check_chrome,
        check_webdriver,
        check_bot_files,
        test_basic_chrome
    ]
    
    results = []
    for check in checks:
        results.append(check())
    
    print("\n" + "="*60)
    print("SUMMARY:")
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"✅ ALL CHECKS PASSED ({passed}/{total})")
        print("🎉 Ready to run RDP bot!")
        print("\nNext step: python quick_test.py <session_id>")
    else:
        print(f"❌ SOME CHECKS FAILED ({passed}/{total})")
        print("💡 Fix the issues above before running bot")
    
    print("="*60)

if __name__ == "__main__":
    main()
