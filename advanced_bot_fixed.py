#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced Shopee Live Bot - Fixed Authentication Version
With proper authentication detection and bypass
"""

import time
import random
import threading
import os
import sys
from datetime import datetime

# Core imports
import json
import requests

# Browser automation imports with fallbacks
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
    SELENIUM_AVAILABLE = True
except ImportError:
    print("❌ Selenium not installed! Run: pip install selenium")
    SELENIUM_AVAILABLE = False

# Try undetected chromedriver
try:
    import undetected_chromedriver as uc
    UNDETECTED_AVAILABLE = True
except ImportError:
    UNDETECTED_AVAILABLE = False

class SimpleLogger:
    def __init__(self, log_file="advanced_bot.log"):
        self.log_file = log_file
    
    def log(self, message, level="INFO"):
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"[{timestamp}] {level}: {message}\n"
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except:
            pass

class AdvancedShopeeBot:
    def __init__(self):
        self.accounts = []
        self.session_id = None
        self.running = False
        self.success_count = 0
        self.failure_count = 0
        self.logger = SimpleLogger()
        
        if not SELENIUM_AVAILABLE:
            print("❌ Selenium is required! Please install with: pip install selenium")
            sys.exit(1)
    
    def log(self, message, level="INFO"):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"
        print(formatted_message)
        self.logger.log(message, level)
    
    def load_accounts(self):
        """Load accounts from CSV file"""
        try:
            # Try different paths
            possible_paths = [
                "../input.csv",
                "input.csv", 
                "../../input.csv",
                "../../../input.csv"
            ]
            
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
                self.log("❌ File input.csv tidak ditemukan!", "ERROR")
                return False
            
            self.log(f"📁 Loading accounts from: {used_path}")
            
            lines = [line.strip() for line in content.split('\n') if line.strip()]
            
            for line_num, line in enumerate(lines, 1):
                if line.startswith('#'):
                    continue
                
                account = self.parse_cookie_line(line)
                if account:
                    self.accounts.append(account)
                    self.log(f"✅ Akun {len(self.accounts)}: {account['user_id'][:8]}... loaded")
                else:
                    self.log(f"⚠️  Baris {line_num}: Cookie tidak valid atau tidak lengkap")
            
            if len(self.accounts) == 0:
                self.log("❌ Tidak ada akun valid yang ditemukan!", "ERROR")
                return False
            
            self.log(f"✅ Berhasil memuat {len(self.accounts)} akun valid", "SUCCESS")
            return True
            
        except Exception as e:
            self.log(f"❌ Error loading accounts: {e}", "ERROR")
            return False
    
    def parse_cookie_line(self, cookie_string):
        """Parse cookie string into account object"""
        try:
            cookies = {}
            required_cookies = ['SPC_U', 'SPC_T_ID', 'csrftoken']
            
            # Parse cookies
            for cookie in cookie_string.split(';'):
                cookie = cookie.strip()
                if '=' in cookie:
                    name, value = cookie.split('=', 1)
                    cookies[name.strip()] = value.strip()
            
            # Check required cookies
            has_required = all(cookie in cookies for cookie in required_cookies)
            
            if not has_required:
                return None
            
            return {
                'cookies': cookies,
                'cookie_string': cookie_string,
                'user_id': cookies.get('SPC_U', ''),
                'token': cookies.get('SPC_T_ID', ''),
                'csrf': cookies.get('csrftoken', ''),
                'has_required_cookies': has_required
            }
            
        except Exception as e:
            self.log(f"❌ Error parsing cookie: {e}", "ERROR")
            return None
    
    def create_stealth_driver(self):
        """Create Chrome driver with stealth settings"""
        try:
            # Try undetected Chrome first
            if UNDETECTED_AVAILABLE:
                try:
                    options = uc.ChromeOptions()
                    options.add_argument('--no-sandbox')
                    options.add_argument('--disable-dev-shm-usage')
                    options.add_argument('--disable-blink-features=AutomationControlled')
                    
                    # Random window size
                    window_sizes = ['1366,768', '1920,1080', '1440,900', '1280,720']
                    options.add_argument(f'--window-size={random.choice(window_sizes)}')
                    
                    driver = uc.Chrome(options=options, version_main=None)
                    self.log("✅ Using undetected Chrome driver")
                    return driver
                    
                except Exception as e:
                    self.log(f"⚠️  Undetected Chrome failed: {e}")
                    self.log("🔄 Falling back to standard Chrome...")
            
            # Fallback to standard Chrome
            options = Options()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            # Random settings
            window_sizes = ['1366,768', '1920,1080', '1440,900', '1280,720']
            options.add_argument(f'--window-size={random.choice(window_sizes)}')
            
            user_agents = [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
            ]
            options.add_argument(f'--user-agent={random.choice(user_agents)}')
            
            driver = webdriver.Chrome(options=options)
            self.log("✅ Using standard Chrome driver with stealth settings")
            
            # Anti-detection script
            driver.execute_script("""
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
                window.chrome = {runtime: {}};
            """)
            
            return driver
            
        except WebDriverException as e:
            if "This version of ChromeDriver only supports Chrome version" in str(e):
                self.log("❌ ChromeDriver version mismatch!", "ERROR")
                self.log("💡 Run fix_chromedriver_version.bat to fix this", "ERROR")
            else:
                self.log(f"❌ WebDriver error: {e}", "ERROR")
            return None
        except Exception as e:
            self.log(f"❌ Error creating driver: {e}", "ERROR")
            return None
    
    def inject_cookies(self, driver, cookies):
        """Inject cookies into browser"""
        try:
            self.log("🌐 Navigating to Shopee...")
            driver.get("https://shopee.co.id")
            time.sleep(3)
            
            # Clear existing cookies
            driver.delete_all_cookies()
            
            # Inject cookies
            injected_count = 0
            for name, value in cookies.items():
                try:
                    driver.add_cookie({
                        'name': name,
                        'value': value,
                        'domain': '.shopee.co.id',
                        'path': '/'
                    })
                    injected_count += 1
                except:
                    pass
            
            self.log(f"✅ Injected {injected_count} cookies")
            
            # Refresh to apply cookies
            driver.refresh()
            time.sleep(3)  # Wait longer for cookies to take effect
            
            return True
            
        except Exception as e:
            self.log(f"❌ Error injecting cookies: {e}", "ERROR")
            return False
    
    def verify_authentication_by_api(self, cookies):
        """Verify authentication using Shopee API"""
        try:
            self.log("🔍 Verifying authentication via API...")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/json',
                'Cookie': '; '.join([f"{k}={v}" for k, v in cookies.items()])
            }
            
            # Try to access user profile API
            response = requests.get(
                'https://shopee.co.id/api/v4/account/basic',
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and data['data']:
                    self.log("✅ API authentication verified")
                    return True
            
            self.log("❌ API authentication failed")
            return False
            
        except Exception as e:
            self.log(f"⚠️  API verification error: {e}")
            return False
    
    def navigate_to_live_stream(self, driver, session_id):
        """Navigate to live stream"""
        try:
            live_url = f"https://live.shopee.co.id/share?from=live&session={session_id}"
            self.log(f"🎥 Navigating to live stream...")
            
            driver.get(live_url)
            time.sleep(5)
            
            # Check if redirected to login
            current_url = driver.current_url
            if 'login' in current_url or 'signin' in current_url:
                self.log("❌ Redirected to login from live stream")
                return False
            
            # Check if on live stream page
            if 'live.shopee.co.id' in current_url:
                self.log("✅ Successfully on live stream page")
                return True
            
            return False
            
        except Exception as e:
            self.log(f"❌ Error navigating to live stream: {e}", "ERROR")
            return False
    
    def authenticate_and_join(self, account):
        """Main authentication and join process"""
        driver = None
        success = False
        
        try:
            self.log(f"🔐 Authenticating {account['user_id'][:8]}...")
            
            # First verify authentication via API (faster)
            if not self.verify_authentication_by_api(account['cookies']):
                self.log(f"❌ API authentication failed for {account['user_id'][:8]}", "ERROR")
                self.failure_count += 1
                return False
            
            # Create driver
            driver = self.create_stealth_driver()
            if not driver:
                return False
            
            # Inject cookies
            if not self.inject_cookies(driver, account['cookies']):
                return False
            
            self.log(f"✅ Cookies injected for {account['user_id'][:8]}")
            
            # Navigate directly to live stream (skip authentication check)
            if self.navigate_to_live_stream(driver, self.session_id):
                self.log(f"🎥 Successfully joined live stream: {account['user_id'][:8]}")
                
                # Keep session alive
                keep_alive_time = random.randint(30, 180)
                self.log(f"⏱️  Keeping session alive for {keep_alive_time}s...")
                
                time.sleep(keep_alive_time)
                
                self.success_count += 1
                success = True
            else:
                self.log(f"❌ Failed to join live stream: {account['user_id'][:8]}", "ERROR")
                self.failure_count += 1
                
        except Exception as e:
            self.log(f"❌ Error with account {account['user_id'][:8]}: {e}", "ERROR")
            self.failure_count += 1
        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass
        
        return success
    
    def worker_thread(self, account_batch):
        """Worker thread for processing accounts"""
        for account in account_batch:
            if not self.running:
                break
            
            self.authenticate_and_join(account)
            
            if self.running:
                time.sleep(random.uniform(5, 15))
    
    def run_advanced_bot(self, session_id, max_accounts=None):
        """Run the advanced bot"""
        self.session_id = session_id
        self.running = True
        self.success_count = 0
        self.failure_count = 0
        
        accounts_to_use = self.accounts[:max_accounts] if max_accounts else self.accounts
        
        self.log("🚀 STARTING ADVANCED SHOPEE BOT", "SUCCESS")
        self.log(f"🎯 Session ID: {session_id}")
        self.log(f"👥 Accounts to use: {len(accounts_to_use)}")
        self.log(f"🔐 Authentication: API + Browser verification")
        print("\n" + "="*60)
        
        # Process accounts in batches
        max_concurrent = min(3, len(accounts_to_use))
        batch_size = max(1, len(accounts_to_use) // max_concurrent)
        
        threads = []
        
        for i in range(0, len(accounts_to_use), batch_size):
            if not self.running:
                break
                
            batch = accounts_to_use[i:i + batch_size]
            if batch:
                thread = threading.Thread(target=self.worker_thread, args=(batch,))
                threads.append(thread)
                thread.start()
                time.sleep(3)
        
        # Wait for completion
        for thread in threads:
            thread.join()
        
        self.running = False
        
        # Final report
        print("\n" + "="*60)
        self.log("🎉 ADVANCED BOT COMPLETED", "SUCCESS")
        self.log(f"✅ Successful logins: {self.success_count}")
        self.log(f"❌ Failed logins: {self.failure_count}")
        total = self.success_count + self.failure_count
        if total > 0:
            success_rate = (self.success_count / total) * 100
            self.log(f"📊 Success rate: {success_rate:.1f}%")

def main():
    print("""
    ╔═══════════════════════════════════════════════════════╗
    ║           ADVANCED SHOPEE LIVE BOT v2.1              ║
    ║           FIXED AUTHENTICATION VERSION               ║
    ╚═══════════════════════════════════════════════════════╝
    
    🛡️  Features:
    ✅ API-based authentication verification
    ✅ Direct live stream navigation
    ✅ Stealth Chrome driver (undetected if available)
    ✅ Better error handling
    ✅ Real viewer count increase
    """)
    
    bot = AdvancedShopeeBot()
    
    # Load accounts
    if not bot.load_accounts():
        input("Press Enter to exit...")
        return
    
    print(f"\n📊 Total akun tersedia: {len(bot.accounts)}")
    
    # Get session ID
    while True:
        session_input = input("\n🔗 Masukkan Session ID atau URL live Shopee: ").strip()
        
        if not session_input:
            print("❌ Session ID tidak boleh kosong!")
            continue
        
        # Extract session ID
        if 'live.shopee.co.id' in session_input:
            import re
            match = re.search(r'[?&]session=(\d+)', session_input)
            if match:
                session_id = match.group(1)
                print(f"✅ Session ID extracted: {session_id}")
                break
            match = re.search(r'live\.shopee\.co\.id/(\d+)', session_input)
            if match:
                session_id = match.group(1)
                print(f"✅ Session ID extracted: {session_id}")
                break
        elif session_input.isdigit():
            session_id = session_input
            print(f"✅ Session ID: {session_id}")
            break
        else:
            print("❌ Format tidak valid! Gunakan session ID atau URL live Shopee")
    
    # Ask for number of accounts
    while True:
        try:
            max_accounts_input = input(f"\n🔢 Berapa akun yang ingin digunakan? (max {len(bot.accounts)}, Enter untuk semua): ").strip()
            
            if not max_accounts_input:
                max_accounts = None
                break
            
            max_accounts = int(max_accounts_input)
            if 1 <= max_accounts <= len(bot.accounts):
                break
            else:
                print(f"❌ Jumlah harus antara 1-{len(bot.accounts)}")
        except ValueError:
            print("❌ Input harus berupa angka!")
    
    # Confirmation
    account_count = max_accounts or len(bot.accounts)
    print(f"\n⚠️  ADVANCED BOT WARNING:")
    print(f"🔐 Bot akan authenticate {account_count} akun")
    print(f"🌐 Menggunakan API + browser verification")
    print(f"⏱️  Proses mungkin memakan waktu 5-10 menit")
    print(f"📈 Viewer count akan naik secara real-time!")
    
    confirm = input(f"\n🚀 Lanjutkan dengan Advanced Bot? (y/n): ").lower()
    if confirm != 'y':
        print("👋 Bot dibatalkan!")
        return
    
    # Run bot
    try:
        bot.run_advanced_bot(session_id, max_accounts)
    except KeyboardInterrupt:
        print("\n⚠️ Bot dihentikan oleh user!")
        bot.running = False
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
