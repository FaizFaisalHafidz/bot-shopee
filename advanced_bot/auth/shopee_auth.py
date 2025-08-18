#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced Shopee Authentication Handler
Handles login bypass, cookie validation, and session management
"""

import time
import random
import json
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
# Browser automation imports
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    
    # Try to import undetected_chromedriver
    try:
        import undetected_chromedriver as uc
        UNDETECTED_AVAILABLE = True
    except ImportError:
        print("⚠️  undetected-chromedriver not available, using standard Chrome driver")
        UNDETECTED_AVAILABLE = False
        
except ImportError as e:
    print(f"❌ Selenium import error: {e}")
    print("💡 Install with: pip install selenium undetected-chromedriver")
    raise

class ShopeeAuth:
    def __init__(self):
        self.session = requests.Session()
        self.driver = None
        self.authenticated_sessions = {}
        
    def create_stealth_driver(self):
        """Create undetected Chrome driver for bypassing detection"""
        try:
            # Try undetected Chrome first
            if UNDETECTED_AVAILABLE:
                try:
                    options = uc.ChromeOptions()
                    
                    # Stealth settings
                    options.add_argument('--no-first-run')
                    options.add_argument('--no-default-browser-check')
                    options.add_argument('--disable-blink-features=AutomationControlled')
                    options.add_argument('--disable-extensions')
                    options.add_argument('--disable-plugins-discovery')
                    options.add_argument('--disable-dev-shm-usage')
                    options.add_argument('--no-sandbox')
                    
                    # Random window size
                    window_sizes = [
                        '--window-size=1366,768',
                        '--window-size=1920,1080', 
                        '--window-size=1440,900',
                        '--window-size=1280,720'
                    ]
                    options.add_argument(random.choice(window_sizes))
                    
                    # Create undetected Chrome driver
                    self.driver = uc.Chrome(options=options, version_main=None)
                    print("✅ Using undetected Chrome driver")
                    
                except Exception as e:
                    print(f"⚠️  Undetected Chrome failed: {e}")
                    print("🔄 Falling back to standard Chrome driver...")
                    UNDETECTED_AVAILABLE = False
            
            # Use standard Chrome if undetected not available
            if not UNDETECTED_AVAILABLE or not self.driver:
                options = Options()
                
                # Stealth settings for standard Chrome
                options.add_argument('--no-first-run')
                options.add_argument('--no-default-browser-check')
                options.add_argument('--disable-blink-features=AutomationControlled')
                options.add_argument('--disable-extensions')
                options.add_argument('--disable-plugins-discovery')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('--no-sandbox')
                options.add_experimental_option("excludeSwitches", ["enable-automation"])
                options.add_experimental_option('useAutomationExtension', False)
                
                # Random window size
                window_sizes = [
                    '--window-size=1366,768',
                    '--window-size=1920,1080', 
                    '--window-size=1440,900',
                    '--window-size=1280,720'
                ]
                options.add_argument(random.choice(window_sizes))
                
                # Random user agent
                user_agents = [
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
                ]
                options.add_argument(f'--user-agent={random.choice(user_agents)}')
                
                # Create standard Chrome driver
                self.driver = webdriver.Chrome(options=options)
                print("✅ Using standard Chrome driver with stealth settings")
            
            # Additional anti-detection (works for both)
            if self.driver:
                self.driver.execute_script("""
                    Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                    Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
                    Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en', 'id']});
                    window.chrome = {runtime: {}};
                """)
            
            return True
            
        except Exception as e:
            print(f"❌ Error creating stealth driver: {e}")
            return False
    
    def validate_cookie_string(self, cookie_string):
        """Validate and parse cookie string"""
        try:
            cookies = {}
            required_cookies = ['SPC_U', 'SPC_T_ID', 'csrftoken']
            
            for cookie in cookie_string.split(';'):
                cookie = cookie.strip()
                if '=' in cookie:
                    name, value = cookie.split('=', 1)
                    cookies[name.strip()] = value.strip()
            
            # Check required cookies
            missing_cookies = []
            for req_cookie in required_cookies:
                if req_cookie not in cookies:
                    missing_cookies.append(req_cookie)
            
            if missing_cookies:
                print(f"❌ Missing required cookies: {missing_cookies}")
                return None
            
            return cookies
            
        except Exception as e:
            print(f"❌ Error parsing cookies: {e}")
            return None
    
    def inject_cookies_advanced(self, cookies):
        """Advanced cookie injection with validation"""
        try:
            # Navigate to Shopee first
            print("🌐 Navigating to Shopee...")
            self.driver.get("https://shopee.co.id")
            time.sleep(3)
            
            # Clear existing cookies
            self.driver.delete_all_cookies()
            
            # Inject cookies in specific order
            cookie_order = ['SPC_U', 'SPC_T_ID', 'csrftoken', 'SPC_ST', 'SPC_EC', 'shopee_token']
            
            injected_count = 0
            for cookie_name in cookie_order:
                if cookie_name in cookies:
                    try:
                        self.driver.add_cookie({
                            'name': cookie_name,
                            'value': cookies[cookie_name],
                            'domain': '.shopee.co.id',
                            'path': '/'
                        })
                        injected_count += 1
                    except Exception as e:
                        print(f"⚠️  Could not inject {cookie_name}: {e}")
            
            # Inject remaining cookies
            for name, value in cookies.items():
                if name not in cookie_order:
                    try:
                        self.driver.add_cookie({
                            'name': name,
                            'value': value,
                            'domain': '.shopee.co.id',
                            'path': '/'
                        })
                        injected_count += 1
                    except:
                        pass
            
            print(f"✅ Injected {injected_count} cookies")
            
            # Refresh to apply cookies
            self.driver.refresh()
            time.sleep(2)
            
            return True
            
        except Exception as e:
            print(f"❌ Error injecting cookies: {e}")
            return False
    
    def check_authentication_status(self):
        """Check if user is authenticated"""
        try:
            # Look for authentication indicators
            auth_indicators = [
                "//div[contains(@class, 'navbar__username')]",  # Username in navbar
                "//div[contains(@class, 'user-info')]",         # User info section
                "//span[contains(@class, 'shopee-avatar')]",    # User avatar
                "//div[@data-sqe='nav_user']"                   # User nav element
            ]
            
            for indicator in auth_indicators:
                try:
                    element = self.driver.find_element(By.XPATH, indicator)
                    if element:
                        print("✅ Authentication confirmed - User is logged in")
                        return True
                except:
                    continue
            
            # Check if redirected to login page
            current_url = self.driver.current_url
            if 'login' in current_url.lower() or 'signin' in current_url.lower():
                print("❌ Redirected to login page - Authentication failed")
                return False
            
            # Look for login button (indicates not logged in)
            login_selectors = [
                "//div[contains(text(), 'Masuk')]",
                "//div[contains(text(), 'Login')]", 
                "//a[contains(@href, 'login')]"
            ]
            
            for selector in login_selectors:
                try:
                    element = self.driver.find_element(By.XPATH, selector)
                    if element and element.is_displayed():
                        print("❌ Login button found - User not authenticated")
                        return False
                except:
                    continue
            
            print("🤔 Authentication status unclear - assuming logged in")
            return True
            
        except Exception as e:
            print(f"⚠️  Error checking auth status: {e}")
            return False
    
    def bypass_login_detection(self):
        """Bypass various login detection mechanisms"""
        try:
            # Handle popup modals
            popup_selectors = [
                "//div[contains(@class, 'modal')]//button[contains(@class, 'close')]",
                "//div[contains(@class, 'popup')]//div[contains(@class, 'close')]",
                "//button[contains(text(), 'Tutup')]",
                "//button[contains(text(), 'Close')]"
            ]
            
            for selector in popup_selectors:
                try:
                    popup = self.driver.find_element(By.XPATH, selector)
                    if popup and popup.is_displayed():
                        popup.click()
                        print("✅ Closed popup/modal")
                        time.sleep(1)
                except:
                    continue
            
            # Handle CAPTCHA if present
            captcha_selectors = [
                "//div[contains(@class, 'captcha')]",
                "//div[contains(text(), 'captcha')]",
                "//div[contains(text(), 'Verify')]"
            ]
            
            for selector in captcha_selectors:
                try:
                    captcha = self.driver.find_element(By.XPATH, selector)
                    if captcha and captcha.is_displayed():
                        print("⚠️  CAPTCHA detected - manual intervention needed")
                        input("Please solve CAPTCHA manually and press Enter to continue...")
                        break
                except:
                    continue
            
            return True
            
        except Exception as e:
            print(f"⚠️  Error in bypass: {e}")
            return False
    
    def authenticate_account(self, cookie_string, user_id):
        """Main authentication method"""
        try:
            print(f"\n🔐 Authenticating User: {user_id[:8]}...")
            
            # Validate cookies first
            cookies = self.validate_cookie_string(cookie_string)
            if not cookies:
                return False
            
            # Create stealth driver if needed
            if not self.driver:
                if not self.create_stealth_driver():
                    return False
            
            # Inject cookies
            if not self.inject_cookies_advanced(cookies):
                return False
            
            # Wait for page load
            time.sleep(3)
            
            # Bypass any detection mechanisms
            self.bypass_login_detection()
            
            # Check authentication status
            if self.check_authentication_status():
                self.authenticated_sessions[user_id] = {
                    'cookies': cookies,
                    'timestamp': time.time(),
                    'status': 'authenticated'
                }
                print(f"✅ Authentication SUCCESS for {user_id[:8]}")
                return True
            else:
                print(f"❌ Authentication FAILED for {user_id[:8]}")
                return False
                
        except Exception as e:
            print(f"❌ Authentication error for {user_id[:8]}: {e}")
            return False
    
    def navigate_to_live_stream(self, session_id):
        """Navigate to live stream with authenticated session"""
        try:
            # Use share URL format for better compatibility
            live_url = f"https://live.shopee.co.id/share?from=live&session={session_id}"
            
            print(f"🎥 Navigating to live stream: {session_id}")
            self.driver.get(live_url)
            
            # Wait for page to load
            time.sleep(5)
            
            # Check if successfully on live stream page
            page_indicators = [
                "//div[contains(@class, 'live-stream')]",
                "//div[contains(@class, 'video-player')]",
                "//video",
                "//div[contains(text(), 'Live')]"
            ]
            
            for indicator in page_indicators:
                try:
                    element = self.driver.find_element(By.XPATH, indicator)
                    if element:
                        print("✅ Successfully on live stream page")
                        return True
                except:
                    continue
            
            # Check if redirected back to login
            current_url = self.driver.current_url
            if 'login' in current_url or 'signin' in current_url:
                print("❌ Redirected to login - session expired")
                return False
            
            print("🤔 On live stream page (status unclear)")
            return True
            
        except Exception as e:
            print(f"❌ Error navigating to live stream: {e}")
            return False
    
    def cleanup(self):
        """Clean up resources"""
        try:
            if self.driver:
                self.driver.quit()
                self.driver = None
            print("🧹 Cleanup completed")
        except Exception as e:
            print(f"⚠️  Cleanup error: {e}")

# Test function
def test_authentication():
    """Test authentication with sample cookie"""
    auth = ShopeeAuth()
    
    # Sample cookie for testing (replace with real cookie)
    test_cookie = "SPC_U=12345678; SPC_T_ID=sample_token; csrftoken=sample_csrf"
    
    try:
        success = auth.authenticate_account(test_cookie, "12345678")
        if success:
            print("🎉 Authentication test passed!")
            # Test live stream navigation
            auth.navigate_to_live_stream("154229259")
            time.sleep(10)  # Keep alive for testing
        else:
            print("❌ Authentication test failed!")
    finally:
        auth.cleanup()

if __name__ == "__main__":
    test_authentication()
