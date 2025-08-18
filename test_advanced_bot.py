#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Script - Verify All Dependencies
Test semua imports dan dependencies sebelum run bot
"""

import sys
import os

def test_imports():
    """Test all required imports"""
    print("🧪 TESTING ALL IMPORTS")
    print("======================")
    print()
    
    # Test basic Python modules
    try:
        import time
        import random
        import threading
        import json
        import requests
        print("✅ Basic Python modules: OK")
    except ImportError as e:
        print(f"❌ Basic Python modules failed: {e}")
        return False
    
    # Test Selenium
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
        print("✅ Selenium: OK")
        SELENIUM_OK = True
    except ImportError as e:
        print(f"❌ Selenium failed: {e}")
        print("💡 Install with: pip install selenium")
        SELENIUM_OK = False
    
    # Test undetected-chromedriver (optional)
    try:
        import undetected_chromedriver as uc
        print("✅ undetected-chromedriver: OK (stealth mode available)")
        UNDETECTED_OK = True
    except ImportError as e:
        print("⚠️  undetected-chromedriver: Not available (will use standard Chrome)")
        print("💡 For better stealth: pip install undetected-chromedriver")
        UNDETECTED_OK = False
    
    # Test Chrome installation
    chrome_paths = [
        "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
    ]
    
    chrome_found = False
    for path in chrome_paths:
        if os.path.exists(path):
            print(f"✅ Chrome browser: Found at {path}")
            chrome_found = True
            break
    
    if not chrome_found:
        print("❌ Chrome browser: Not found")
        print("💡 Download from: https://www.google.com/chrome/")
    
    # Test input.csv
    input_paths = ["input.csv", "../input.csv", "../../input.csv"]
    input_found = False
    
    for path in input_paths:
        if os.path.exists(path):
            print(f"✅ input.csv: Found at {path}")
            input_found = True
            break
    
    if not input_found:
        print("❌ input.csv: Not found")
        print("💡 Make sure input.csv exists with Shopee account cookies")
    
    print()
    print("📊 SUMMARY:")
    print("===========")
    
    if SELENIUM_OK and chrome_found and input_found:
        print("🎉 ALL READY! Bot dapat dijalankan")
        if UNDETECTED_OK:
            print("🛡️  Stealth mode available (undetected Chrome)")
        else:
            print("⚠️  Standard Chrome mode (consider installing undetected-chromedriver)")
        return True
    else:
        print("❌ MISSING REQUIREMENTS:")
        if not SELENIUM_OK:
            print("   - Selenium (run: pip install selenium)")
        if not chrome_found:
            print("   - Chrome browser (download from google.com/chrome)")
        if not input_found:
            print("   - input.csv file with account cookies")
        return False

def test_chrome_driver():
    """Test Chrome driver creation"""
    try:
        print("\n🔧 TESTING CHROME DRIVER CREATION")
        print("==================================")
        
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        options = Options()
        options.add_argument('--headless')  # Run in background for testing
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        driver = webdriver.Chrome(options=options)
        driver.get("https://www.google.com")
        
        if "Google" in driver.title:
            print("✅ Chrome driver: Working perfectly!")
            driver.quit()
            return True
        else:
            print("❌ Chrome driver: Page load failed")
            driver.quit()
            return False
            
    except Exception as e:
        print(f"❌ Chrome driver error: {e}")
        
        if "This version of ChromeDriver only supports Chrome version" in str(e):
            print("💡 SOLUTION: ChromeDriver version mismatch!")
            print("   Run: fix_chromedriver_version.bat")
            print("   Or install: pip install webdriver-manager")
        elif "chromedriver" in str(e).lower():
            print("💡 SOLUTION: ChromeDriver not found!")
            print("   Download ChromeDriver and put in PATH")
            print("   Or run setup scripts provided")
        
        return False

if __name__ == "__main__":
    print("🧪 DEPENDENCY TEST FOR ADVANCED SHOPEE BOT")
    print("===========================================")
    print()
    
    # Test imports
    imports_ok = test_imports()
    
    if imports_ok:
        # Test Chrome driver if imports are OK
        driver_ok = test_chrome_driver()
        
        print("\n🏁 FINAL RESULT:")
        print("================")
        
        if driver_ok:
            print("🎉 ALL TESTS PASSED!")
            print("✅ Bot siap digunakan dengan advanced_bot_simple.py")
            print()
            print("🚀 Run command:")
            print("   python advanced_bot_simple.py")
        else:
            print("⚠️  Chrome driver issues detected")
            print("💡 Bot mungkin masih bisa berjalan, tapi fix ChromeDriver untuk hasil optimal")
    else:
        print("\n❌ DEPENDENCY ISSUES FOUND")
        print("Please fix the missing requirements above")
    
    input("\nPress Enter to exit...")
