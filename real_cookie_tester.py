#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Cookie Tester untuk Shopee
Test cookies secara real dengan browser untuk memastikan bisa login
"""

import time
import random
import os
import sys
from datetime import datetime

# Browser automation imports
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    SELENIUM_AVAILABLE = True
except ImportError:
    print("❌ Selenium not installed! Run: pip install selenium")
    SELENIUM_AVAILABLE = False

try:
    import undetected_chromedriver as uc
    UNDETECTED_AVAILABLE = True
except ImportError:
    UNDETECTED_AVAILABLE = False

class RealCookieTester:
    def __init__(self):
        self.working_cookies = []
        self.expired_cookies = []
        self.error_cookies = []
        
    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")
    
    def load_cookies_from_csv(self):
        """Load cookies dari input.csv"""
        try:
            possible_paths = ["input.csv", "../input.csv", "../../input.csv"]
            
            content = None
            used_path = None
            
            for path in possible_paths:
                try:
                    with open(path, 'r', encoding='utf-8') as file:
                        content = file.read().strip()
                        used_path = path
                        break
                except FileNotFoundError:
                    continue
            
            if not content:
                self.log("❌ File input.csv tidak ditemukan!")
                return []
            
            self.log(f"📁 Loading cookies from: {used_path}")
            
            lines = [line.strip() for line in content.split('\n') if line.strip() and not line.startswith('#')]
            
            cookies_list = []
            for line_num, line in enumerate(lines, 1):
                cookie_data = self.parse_cookie_line(line)
                if cookie_data:
                    cookie_data['line_number'] = line_num
                    cookie_data['raw_line'] = line
                    cookies_list.append(cookie_data)
                    
            self.log(f"✅ Loaded {len(cookies_list)} cookie sets from CSV")
            return cookies_list
            
        except Exception as e:
            self.log(f"❌ Error loading cookies: {e}")
            return []
    
    def parse_cookie_line(self, cookie_string):
        """Parse cookie string"""
        try:
            cookies = {}
            required_cookies = ['SPC_U', 'SPC_T_ID', 'csrftoken']
            
            # Handle both ; and ;space separators
            for separator in [';', '; ']:
                if separator in cookie_string:
                    parts = cookie_string.split(separator)
                    break
            else:
                parts = [cookie_string]
            
            for cookie in parts:
                cookie = cookie.strip()
                if '=' in cookie:
                    name, value = cookie.split('=', 1)
                    cookies[name.strip()] = value.strip()
            
            has_required = all(cookie in cookies for cookie in required_cookies)
            
            if not has_required:
                return None
            
            return {
                'cookies': cookies,
                'cookie_string': cookie_string,
                'user_id': cookies.get('SPC_U', ''),
                'token': cookies.get('SPC_T_ID', ''),
                'csrf': cookies.get('csrftoken', ''),
                'has_required': has_required
            }
            
        except Exception as e:
            return None
    
    def create_test_driver(self):
        """Create driver untuk testing"""
        try:
            # Try undetected Chrome first
            if UNDETECTED_AVAILABLE:
                try:
                    options = uc.ChromeOptions()
                    options.add_argument('--no-sandbox')
                    options.add_argument('--disable-dev-shm-usage')
                    # Don't use headless for visual debugging
                    
                    driver = uc.Chrome(options=options, version_main=None)
                    self.log("✅ Using undetected Chrome driver")
                    return driver
                    
                except Exception as e:
                    self.log(f"⚠️ Undetected Chrome failed: {e}")
            
            # Fallback to standard Chrome
            options = Options()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            # Don't use headless for visual debugging
            
            driver = webdriver.Chrome(options=options)
            self.log("✅ Using standard Chrome driver")
            return driver
            
        except Exception as e:
            self.log(f"❌ Error creating driver: {e}")
            return None
    
    def test_cookie_real_login(self, cookie_data):
        """Test apakah cookie bisa login secara real"""
        driver = None
        try:
            user_display = cookie_data['user_id'][:8] + "..."
            self.log(f"🧪 TESTING COOKIE: {user_display}")
            
            driver = self.create_test_driver()
            if not driver:
                return 'error', "Driver creation failed"
            
            # Step 1: Navigate to Shopee
            self.log("🌐 Step 1: Opening Shopee...")
            driver.get("https://shopee.co.id")
            time.sleep(4)
            
            # Step 2: Clear and inject cookies
            self.log("🍪 Step 2: Injecting cookies...")
            driver.delete_all_cookies()
            
            injected_count = 0
            for name, value in cookie_data['cookies'].items():
                try:
                    driver.add_cookie({
                        'name': name,
                        'value': value,
                        'domain': '.shopee.co.id',
                        'path': '/'
                    })
                    injected_count += 1
                except:
                    continue
            
            self.log(f"✅ Injected {injected_count} cookies")
            
            # Step 3: Test login by going to account page
            self.log("🔐 Step 3: Testing login access...")
            driver.get("https://shopee.co.id/user/account/profile")
            time.sleep(5)
            
            current_url = driver.current_url
            self.log(f"📍 Current URL: {current_url}")
            
            # Check URL for login redirect
            if any(keyword in current_url.lower() for keyword in ['login', 'signin', 'buyer/login']):
                self.log("❌ RESULT: EXPIRED - Redirected to login")
                return 'expired', "Redirected to login page"
            
            # Step 4: Look for profile content
            self.log("👤 Step 4: Checking profile content...")
            try:
                # Wait for page to load and look for profile indicators
                time.sleep(3)
                page_text = driver.page_source.lower()
                
                # Positive indicators (profile page elements)
                profile_indicators = ['profil saya', 'my profile', 'edit profil', 'nama pengguna', 'username', 'email', 'nomor telepon']
                found_profile = any(indicator in page_text for indicator in profile_indicators)
                
                # Negative indicators (login page elements)
                login_indicators = ['masuk dengan', 'login dengan', 'belum punya akun', 'daftar sekarang']
                found_login = any(indicator in page_text for indicator in login_indicators)
                
                if found_profile and not found_login:
                    self.log("✅ RESULT: WORKING - Profile page accessible!")
                    return 'working', "Profile page shows user data"
                elif found_login:
                    self.log("❌ RESULT: EXPIRED - Login page detected")
                    return 'expired', "Login elements found on page"
                
            except Exception as e:
                self.log(f"⚠️ Profile check error: {e}")
            
            # Step 5: Final test - try live page
            self.log("🎥 Step 5: Testing live page access...")
            driver.get("https://live.shopee.co.id")
            time.sleep(4)
            
            current_url = driver.current_url
            if any(keyword in current_url.lower() for keyword in ['login', 'signin']):
                self.log("❌ RESULT: EXPIRED - Live page requires login")
                return 'expired', "Live page redirected to login"
            
            # If we reach here, probably working
            self.log("✅ RESULT: WORKING - All tests passed!")
            return 'working', "All access tests successful"
            
        except Exception as e:
            self.log(f"❌ RESULT: ERROR - {e}")
            return 'error', f"Test error: {e}"
        finally:
            if driver:
                try:
                    # Keep browser open for a moment to see result
                    time.sleep(2)
                    driver.quit()
                except:
                    pass
    
    def test_all_cookies(self, max_test=None):
        """Test semua cookies"""
        cookies_list = self.load_cookies_from_csv()
        
        if not cookies_list:
            return
        
        if max_test:
            cookies_list = cookies_list[:max_test]
            self.log(f"🧪 Testing first {max_test} cookies only")
        
        print("\n" + "="*70)
        print("🧪 REAL COOKIE LOGIN TESTER")
        print("="*70)
        print("⚠️  Browser akan muncul untuk test setiap cookie")
        print("👀 Anda bisa lihat proses login secara visual")
        print("⏱️  Total waktu: ~2-3 menit per cookie")
        print("="*70)
        
        for i, cookie_data in enumerate(cookies_list, 1):
            user_display = cookie_data['user_id'][:8] + "..."
            
            print(f"\n🔍 [{i}/{len(cookies_list)}] Testing: {user_display}")
            print("-" * 50)
            
            result, reason = self.test_cookie_real_login(cookie_data)
            
            cookie_data['test_result'] = result
            cookie_data['test_reason'] = reason
            
            if result == 'working':
                print(f"✅ SUCCESS: Cookie {user_display} is WORKING!")
                self.working_cookies.append(cookie_data)
            elif result == 'expired':
                print(f"❌ EXPIRED: Cookie {user_display} needs refresh")
                print(f"   Reason: {reason}")
                self.expired_cookies.append(cookie_data)
            else:
                print(f"⚠️ ERROR: Cookie {user_display} test failed") 
                print(f"   Reason: {reason}")
                self.error_cookies.append(cookie_data)
            
            # Pause between tests
            if i < len(cookies_list):
                self.log("⏱️ Pausing 5 seconds before next test...")
                time.sleep(5)
        
        # Show final results
        self.show_final_results()
    
    def show_final_results(self):
        """Show final test results"""
        total = len(self.working_cookies) + len(self.expired_cookies) + len(self.error_cookies)
        
        print("\n" + "="*70)
        print("📊 FINAL COOKIE TEST RESULTS")  
        print("="*70)
        
        print(f"✅ WORKING COOKIES: {len(self.working_cookies)}/{total}")
        print(f"❌ EXPIRED COOKIES: {len(self.expired_cookies)}/{total}")
        print(f"⚠️ ERROR COOKIES: {len(self.error_cookies)}/{total}")
        
        if len(self.working_cookies) > 0:
            print(f"\n🎉 EXCELLENT! {len(self.working_cookies)} cookies are working!")
            print("🚀 Bot should work with these cookies!")
            
            # Show working cookies details
            print(f"\n✅ Working cookies:")
            for i, cookie_data in enumerate(self.working_cookies, 1):
                user_display = cookie_data['user_id'][:8] + "..."
                print(f"   {i}. {user_display} - {cookie_data['test_reason']}")
            
            # Save working cookies
            try:
                with open('working_cookies.csv', 'w', encoding='utf-8') as f:
                    f.write("# WORKING COOKIES - Real browser tested\n")
                    for cookie_data in self.working_cookies:
                        f.write(cookie_data['raw_line'] + '\n')
                print(f"\n💾 Saved {len(self.working_cookies)} working cookies to: working_cookies.csv")
                print("💡 You can use working_cookies.csv as input for the bot")
            except Exception as e:
                print(f"⚠️ Could not save working cookies: {e}")
        
        else:
            print(f"\n😞 NO WORKING COOKIES FOUND!")
            print("🔧 All cookies need to be refreshed")
        
        if len(self.expired_cookies) > 0:
            print(f"\n❌ Expired cookies (need refresh):")
            for i, cookie_data in enumerate(self.expired_cookies, 1):
                user_display = cookie_data['user_id'][:8] + "..."
                print(f"   {i}. {user_display} - {cookie_data['test_reason']}")
        
        # Show recommendations
        print("\n💡 RECOMMENDATIONS:")
        if len(self.working_cookies) >= 5:
            print("✅ You have enough working cookies for good bot performance")
        elif len(self.working_cookies) > 0:
            print("⚡ You have some working cookies - bot will work but more would be better")
        else:
            print("❌ You need to refresh cookies before running the bot")
        
        if len(self.expired_cookies) > 0:
            print("🔧 Refresh expired cookies using the guide below")
            self.show_refresh_guide()
    
    def show_refresh_guide(self):
        """Show refresh guide"""
        print("\n" + "="*70)
        print("🔧 COOKIE REFRESH GUIDE")
        print("="*70)
        print("""
📝 Steps to refresh expired cookies:

1️⃣ Open Chrome (normal mode, not incognito)
2️⃣ Go to https://shopee.co.id
3️⃣ Login with your account (username/password)
4️⃣ After successful login, press F12 (Developer Tools)
5️⃣ Click "Application" tab (or "Storage")
6️⃣ Click "Cookies" → "https://shopee.co.id"
7️⃣ Find and copy these cookie values:
   • SPC_U (your user ID)
   • SPC_T_ID (session token)
   • csrftoken (security token)
8️⃣ Format: SPC_U=value; SPC_T_ID=value; csrftoken=value;
9️⃣ Replace the old line in input.csv
🔟 Run this tester again to verify

⚠️ Important:
- One account = one line in input.csv
- Don't logout after copying cookies
- Fresh cookies usually work 1-7 days
- Always test cookies before running bot
        """)

def main():
    print("""
    ╔═══════════════════════════════════════════════════════╗
    ║            REAL COOKIE TESTER v1.0                    ║
    ║       Test login cookies dengan browser real           ║
    ╚═══════════════════════════════════════════════════════╝
    
    🧪 Features:
    ✅ Real browser testing (visual debugging)
    ✅ Detect working vs expired cookies
    ✅ Generate working_cookies.csv
    ✅ Comprehensive refresh guide
    """)
    
    if not SELENIUM_AVAILABLE:
        print("❌ Selenium required! Install: pip install selenium")
        return
    
    tester = RealCookieTester()
    
    print("\n🔍 Testing Options:")
    print("1. Test all cookies in input.csv")
    print("2. Test first 3 cookies (quick test)")
    print("3. Test first 5 cookies")
    print("4. Show refresh guide only")
    print("5. Exit")
    
    while True:
        choice = input("\n📍 Choose option (1-5): ").strip()
        
        if choice == '1':
            print("⚠️ This will test ALL cookies - may take a while!")
            confirm = input("🚀 Continue with full test? (y/n): ").lower()
            if confirm == 'y':
                tester.test_all_cookies()
            break
        elif choice == '2':
            print("🚀 Quick test: Testing first 3 cookies...")
            tester.test_all_cookies(max_test=3)
            break
        elif choice == '3':
            print("🚀 Testing first 5 cookies...")
            tester.test_all_cookies(max_test=5)
            break
        elif choice == '4':
            tester.show_refresh_guide()
            break
        elif choice == '5':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice!")

if __name__ == "__main__":
    main()
