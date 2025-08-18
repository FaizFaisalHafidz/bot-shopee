#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script untuk memeriksa semua komponen bot
"""

import sys
import os
import subprocess
import time

def test_python():
    """Test Python installation"""
    print("🐍 Testing Python...")
    try:
        version = sys.version.split()[0]
        major, minor = version.split('.')[0:2]
        if int(major) >= 3 and int(minor) >= 8:
            print(f"   ✅ Python {version} - OK")
            return True
        else:
            print(f"   ❌ Python {version} - Need 3.8+")
            return False
    except:
        print("   ❌ Python version check failed")
        return False

def test_selenium():
    """Test Selenium installation"""
    print("🌐 Testing Selenium...")
    try:
        import selenium
        version = selenium.__version__
        print(f"   ✅ Selenium {version} - OK")
        
        # Test specific imports
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        print("   ✅ Selenium imports - OK")
        return True
    except ImportError as e:
        print(f"   ❌ Selenium not installed: {e}")
        print("   💡 Run: pip install selenium==4.15.0")
        return False

def test_chrome():
    """Test Chrome installation"""
    print("🌍 Testing Chrome...")
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/usr/bin/google-chrome"
    ]
    
    for path in chrome_paths:
        if os.path.exists(path):
            print(f"   ✅ Chrome found: {path}")
            return True
    
    print("   ❌ Chrome not found")
    print("   💡 Install Google Chrome from google.com/chrome")
    return False

def test_chromedriver():
    """Test ChromeDriver"""
    print("🚗 Testing ChromeDriver...")
    try:
        result = subprocess.run(['chromedriver', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"   ✅ ChromeDriver: {version}")
            return True
    except Exception:
        pass
    
    # Check in current directory
    if os.path.exists('chromedriver.exe') or os.path.exists('chromedriver'):
        print("   ✅ ChromeDriver found in current directory")
        return True
    
    print("   ❌ ChromeDriver not found")
    print("   💡 Download from chromedriver.chromium.org")
    return False

def test_input_file():
    """Test input.csv file"""
    print("📁 Testing input.csv...")
    try:
        with open('input.csv', 'r', encoding='utf-8') as f:
            content = f.read().strip()
            lines = [line.strip() for line in content.split('\n') if line.strip() and not line.startswith('#')]
            
            if len(lines) == 0:
                print("   ❌ input.csv is empty")
                return False
            
            # Test first line format
            first_line = lines[0]
            if 'SPC_U=' in first_line and 'csrftoken=' in first_line:
                print(f"   ✅ input.csv - {len(lines)} accounts detected")
                return True
            else:
                print("   ❌ input.csv format incorrect")
                return False
                
    except FileNotFoundError:
        print("   ❌ input.csv not found")
        return False
    except Exception as e:
        print(f"   ❌ input.csv error: {e}")
        return False

def test_bot_files():
    """Test bot files"""
    print("🤖 Testing bot files...")
    
    bots = {
        'main.py': 'HTTP Bot',
        'browser_bot.py': 'Browser Automation Bot',
        'rdp_optimized_bot.py': 'RDP Optimized Bot'
    }
    
    found_bots = 0
    for file, name in bots.items():
        if os.path.exists(file):
            print(f"   ✅ {name}: {file}")
            found_bots += 1
        else:
            print(f"   ⚠️ {name}: {file} - Not found")
    
    return found_bots > 0

def test_quick_selenium():
    """Quick Selenium functionality test"""
    print("⚡ Quick Selenium test...")
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        # Create headless browser for quick test
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.get('https://www.google.com')
        title = driver.title
        driver.quit()
        
        if 'Google' in title:
            print("   ✅ Selenium browser test - OK")
            return True
        else:
            print("   ❌ Selenium browser test - Failed")
            return False
            
    except Exception as e:
        print(f"   ❌ Selenium test failed: {str(e)[:100]}...")
        return False

def main():
    print("""
    ╔═══════════════════════════════════════════════╗
    ║            SHOPEE BOT TEST SUITE              ║
    ║              SYSTEM CHECK                     ║
    ╚═══════════════════════════════════════════════╝
    """)
    
    tests = [
        ("Python Installation", test_python),
        ("Selenium Library", test_selenium), 
        ("Google Chrome", test_chrome),
        ("ChromeDriver", test_chromedriver),
        ("Input File", test_input_file),
        ("Bot Files", test_bot_files),
        ("Selenium Functionality", test_quick_selenium)
    ]
    
    passed = 0
    failed = 0
    
    print("Running system checks...\n")
    
    for test_name, test_func in tests:
        print(f"{'='*50}")
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"   ❌ {test_name} - Exception: {e}")
            failed += 1
        print()
    
    print("="*50)
    print("📊 TEST RESULTS:")
    print(f"   ✅ Passed: {passed}")
    print(f"   ❌ Failed: {failed}")
    print(f"   📈 Success Rate: {(passed/(passed+failed)*100):.1f}%")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED!")
        print("✨ Your system is ready to run Shopee Bot!")
        print("\n🚀 Recommended next steps:")
        print("   1. Run: python rdp_optimized_bot.py (untuk RDP)")
        print("   2. Run: python browser_bot.py (untuk local)")
        print("   3. Run: python main.py (HTTP only)")
        
    else:
        print(f"\n⚠️ {failed} TESTS FAILED!")
        print("🔧 Please fix the issues above before running the bot.")
        
        if failed <= 2:
            print("\n💡 Quick fixes:")
            print("   • pip install selenium==4.15.0")
            print("   • Download ChromeDriver")
            print("   • Install Google Chrome")
    
    print(f"\n{'='*50}")

if __name__ == "__main__":
    main()
