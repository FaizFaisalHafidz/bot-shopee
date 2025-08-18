#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shopee Live Streaming Bot - RDP Optimized Browser Automation
Khusus dioptimasi untuk Windows RDP dengan Chrome automation
"""

import time
import random
import csv
import threading
from datetime import datetime
import os
import sys
import subprocess

# Browser automation imports
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchDriverException
except ImportError:
    print("❌ Selenium not installed!")
    print("💡 Install with: pip install selenium")
    sys.exit(1)

class RDPOptimizedBot:
    def __init__(self):
        self.accounts = []
        self.session_id = None
        self.running = False
        self.successful_joins = 0
        self.failed_joins = 0
        self.active_drivers = []
        
    def check_chrome_installation(self):
        """Check apakah Chrome dan ChromeDriver tersedia"""
        try:
            # Check Chrome
            chrome_paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                "/usr/bin/google-chrome",
                "/usr/bin/chromium-browser"
            ]
            
            chrome_found = False
            for path in chrome_paths:
                if os.path.exists(path):
                    chrome_found = True
                    print(f"✅ Chrome found: {path}")
                    break
            
            if not chrome_found:
                print("❌ Google Chrome tidak ditemukan!")
                print("💡 Install Google Chrome terlebih dahulu")
                return False
            
            # Check ChromeDriver
            try:
                result = subprocess.run(['chromedriver', '--version'], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    print(f"✅ ChromeDriver found: {result.stdout.strip()}")
                    return True
            except Exception:
                pass
            
            print("❌ ChromeDriver tidak ditemukan di PATH!")
            print("💡 Download ChromeDriver dan tambahkan ke PATH atau folder bot")
            print("🔗 https://chromedriver.chromium.org/")
            return False
            
        except Exception as e:
            print(f"❌ Error checking Chrome installation: {e}")
            return False
    
    def load_accounts(self):
        """Memuat akun dari file input.csv"""
        try:
            with open('input.csv', 'r', encoding='utf-8') as file:
                content = file.read().strip()
                lines = [line.strip() for line in content.split('\n') if line.strip()]
                
                for line_num, line in enumerate(lines, 1):
                    if line.startswith('#'):
                        continue
                    
                    account = self.parse_cookies(line)
                    if account and account['has_important_cookies']:
                        self.accounts.append(account)
                        print(f"✅ Akun {len(self.accounts)}: User ID {account['user_id'][:8]}... loaded")
                    else:
                        print(f"⚠️ Baris {line_num}: Cookie tidak lengkap atau format salah")
                
                if len(self.accounts) == 0:
                    print("❌ Tidak ada akun valid yang berhasil dimuat!")
                    return False
                    
                print(f"\n✅ Berhasil memuat {len(self.accounts)} akun valid dari input.csv")
                return True
                
        except FileNotFoundError:
            print("❌ File input.csv tidak ditemukan!")
            return False
        except Exception as e:
            print(f"❌ Error membaca file: {e}")
            return False
    
    def parse_cookies(self, cookie_string):
        """Parse cookie string menjadi dictionary"""
        try:
            cookies = {}
            important_cookies = ['SPC_U', 'csrftoken', 'SPC_T_ID', 'SPC_ST', 'SPC_EC']
            
            for cookie in cookie_string.split(';'):
                cookie = cookie.strip()
                if '=' in cookie:
                    name, value = cookie.split('=', 1)
                    cookies[name.strip()] = value.strip()
            
            return {
                'cookies': cookies,
                'user_id': cookies.get('SPC_U', ''),
                'token': cookies.get('SPC_T_ID', ''),
                'csrf': cookies.get('csrftoken', ''),
                'session_token': cookies.get('SPC_ST', ''),
                'ec_token': cookies.get('SPC_EC', ''),
                'has_important_cookies': all(cookie in cookies for cookie in important_cookies)
            }
            
        except Exception as e:
            print(f"❌ Error parsing cookies: {e}")
            return None
    
    def create_rdp_chrome_driver(self, account, headless=False):
        """Buat Chrome driver yang dioptimasi khusus untuk RDP Windows"""
        try:
            chrome_options = Options()
            
            # RDP OPTIMIZATION SETTINGS
            if headless:
                chrome_options.add_argument('--headless')
            
            # Core RDP optimizations
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--disable-software-rasterizer')
            chrome_options.add_argument('--disable-background-timer-throttling')
            chrome_options.add_argument('--disable-backgrounding-occluded-windows')
            chrome_options.add_argument('--disable-renderer-backgrounding')
            
            # Memory and performance optimizations
            chrome_options.add_argument('--memory-pressure-off')
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument('--disable-plugins')
            chrome_options.add_argument('--disable-images')  # Save bandwidth
            chrome_options.add_argument('--disable-javascript')  # Save resources (video still works)
            chrome_options.add_argument('--disable-default-apps')
            chrome_options.add_argument('--disable-sync')
            chrome_options.add_argument('--disable-translate')
            chrome_options.add_argument('--disable-webgl')
            chrome_options.add_argument('--disable-webrtc')
            chrome_options.add_argument('--disable-features=VizDisplayCompositor')
            
            # Network optimizations for RDP
            chrome_options.add_argument('--aggressive-cache-discard')
            chrome_options.add_argument('--disable-background-networking')
            chrome_options.add_argument('--disable-client-side-phishing-detection')
            chrome_options.add_argument('--disable-component-extensions-with-background-pages')
            
            # Anti-detection (important for Shopee)
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Random user agent untuk avoid detection
            user_agents = [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
            ]
            chrome_options.add_argument(f'--user-agent={random.choice(user_agents)}')
            
            # Window optimization untuk RDP
            chrome_options.add_argument('--window-size=800,600')  # Smaller for RDP
            chrome_options.add_argument('--start-maximized')
            
            # Service configuration untuk Windows
            service = Service()
            if sys.platform.startswith('win'):
                service.creation_flags = 0x08000000  # CREATE_NO_WINDOW flag
            
            # Create driver dengan timeout pendek untuk cepat fail
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Set timeouts - lebih pendek untuk RDP
            driver.set_page_load_timeout(20)  # Reduced from 30
            driver.implicitly_wait(8)  # Reduced from 10
            
            # Anti-detection scripts
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})")
            driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en', 'id']})")
            
            # Add to active drivers untuk cleanup nanti
            self.active_drivers.append(driver)
            
            return driver
            
        except Exception as e:
            print(f"❌ Error creating Chrome driver: {str(e)[:100]}...")
            return None
    
    def set_cookies_fast(self, driver, account):
        """Set cookies dengan method yang cepat untuk RDP"""
        try:
            # Navigate to Shopee dengan timeout pendek
            driver.get("https://shopee.co.id")
            time.sleep(1)  # Reduced wait time
            
            # Add important cookies only untuk speed
            important_cookies = ['SPC_U', 'csrftoken', 'SPC_T_ID', 'SPC_ST']
            cookies_added = 0
            
            for name in important_cookies:
                if name in account['cookies']:
                    try:
                        driver.add_cookie({
                            'name': name,
                            'value': account['cookies'][name],
                            'domain': '.shopee.co.id'
                        })
                        cookies_added += 1
                    except Exception:
                        pass  # Skip failed cookies
            
            return cookies_added > 0
            
        except Exception as e:
            print(f"❌ Error setting cookies: {str(e)[:50]}...")
            return False
    
    def rdp_join_live(self, account, session_id):
        """RDP optimized join dengan fast processing"""
        driver = None
        max_retries = 1  # Reduced retries untuk RDP speed
        
        for attempt in range(max_retries):
            try:
                current_time = datetime.now().strftime("%H:%M:%S")
                print(f"[{current_time}] 🚀 RDP Chrome: {account['user_id'][:6]}... (Attempt {attempt + 1})")
                
                # Create optimized driver
                driver = self.create_rdp_chrome_driver(account, headless=False)
                if not driver:
                    continue
                
                # Set cookies dengan fast method
                if not self.set_cookies_fast(driver, account):
                    print(f"[{current_time}] ⚠️ Cookie warning untuk {account['user_id'][:6]}...")
                
                # Navigate ke live streaming dengan CORRECT share format
                live_url = f"https://live.shopee.co.id/share?from=live&session={session_id}"
                
                start_nav = time.time()
                driver.get(live_url)
                nav_time = time.time() - start_nav
                
                current_time = datetime.now().strftime("%H:%M:%S")
                print(f"[{current_time}] 🔗 Navigation time: {nav_time:.1f}s - {account['user_id'][:6]}...")
                
                # Quick page load check
                try:
                    WebDriverWait(driver, 10).until(
                        lambda d: d.execute_script("return document.readyState") == "complete"
                    )
                except TimeoutException:
                    print(f"[{current_time}] ⚠️ Quick timeout, continuing...")
                
                # Success
                current_time = datetime.now().strftime("%H:%M:%S")
                print(f"[{current_time}] ✅ RDP VIEWER SUCCESS: {account['user_id'][:6]}...")
                
                # Keep alive dengan duration pendek untuk RDP efficiency
                keep_alive_time = random.randint(15, 45)  # Reduced time
                print(f"[{current_time}] ⏱️ Keep-alive: {keep_alive_time}s...")
                
                time.sleep(keep_alive_time)
                
                self.successful_joins += 1
                return True
                
            except Exception as e:
                current_time = datetime.now().strftime("%H:%M:%S")
                error_msg = str(e)[:60]
                print(f"[{current_time}] ❌ RDP Error: {error_msg}...")
                
                if attempt < max_retries - 1:
                    time.sleep(2)  # Quick retry
                    
            finally:
                if driver:
                    try:
                        # Remove from active drivers
                        if driver in self.active_drivers:
                            self.active_drivers.remove(driver)
                        driver.quit()
                    except:
                        pass
                    driver = None
        
        # Failed
        self.failed_joins += 1
        current_time = datetime.now().strftime("%H:%M:%S")
        print(f"[{current_time}] ❌ RDP FAILED: {account['user_id'][:6]}...")
        return False
    
    def rdp_batch_worker(self, account_batch, session_id):
        """RDP optimized batch worker"""
        for account in account_batch:
            if not self.running:
                break
            
            # Process account
            self.rdp_join_live(account, session_id)
            
            # Quick interval untuk RDP
            time.sleep(random.uniform(2, 5))
    
    def cleanup_drivers(self):
        """Cleanup semua active drivers"""
        print("🧹 Cleaning up Chrome drivers...")
        for driver in self.active_drivers:
            try:
                driver.quit()
            except:
                pass
        self.active_drivers.clear()
    
    def run_rdp_bot(self, session_id, max_accounts=None, use_threading=True):
        """RDP optimized bot dengan threading control"""
        self.session_id = session_id
        self.running = True
        self.successful_joins = 0
        self.failed_joins = 0
        
        # Limit accounts
        accounts_to_use = self.accounts[:max_accounts] if max_accounts else self.accounts
        
        print(f"\n🚀 Starting RDP OPTIMIZED Bot dengan {len(accounts_to_use)} akun...")
        print(f"🎯 Target Session ID: {session_id}")
        print(f"🌐 Using CORRECT share URL format!")
        print(f"⚡ RDP Windows optimized dengan fast processing")
        print(f"🧵 Threading: {'Enabled' if use_threading else 'Sequential'}")
        print("\n" + "="*60)
        
        start_time = time.time()
        
        if use_threading and len(accounts_to_use) >= 4:
            # Multi-threading untuk accounts banyak
            batch_size = 3  # Smaller batches untuk RDP stability
            batches = [accounts_to_use[i:i + batch_size] for i in range(0, len(accounts_to_use), batch_size)]
            
            threads = []
            for batch in batches:
                thread = threading.Thread(target=self.rdp_batch_worker, args=(batch, session_id))
                threads.append(thread)
                thread.start()
                time.sleep(1)  # Stagger thread starts
            
            # Wait for all threads
            for thread in threads:
                thread.join()
        else:
            # Sequential processing untuk stability
            for i, account in enumerate(accounts_to_use):
                if not self.running:
                    break
                    
                current_time = datetime.now().strftime("%H:%M:%S")
                print(f"\n[{current_time}] 📊 Processing {i+1}/{len(accounts_to_use)}")
                
                self.rdp_join_live(account, session_id)
                
                # Quick delay
                if i < len(accounts_to_use) - 1:
                    delay = random.uniform(3, 6)
                    print(f"[{current_time}] ⏸️ Next account in {delay:.1f}s...")
                    time.sleep(delay)
        
        self.running = False
        end_time = time.time()
        
        # Cleanup
        self.cleanup_drivers()
        
        print("\n" + "="*60)
        print("🎉 RDP Optimized Bot Complete!")
        print(f"📊 Results:")
        print(f"   ✅ Successful joins: {self.successful_joins}")
        print(f"   ❌ Failed joins: {self.failed_joins}")
        print(f"   📈 Success rate: {(self.successful_joins/(self.successful_joins+self.failed_joins)*100):.1f}%")
        print(f"   ⏱️ Total time: {(end_time-start_time)/60:.1f} minutes")
        print(f"   🎯 Expected viewer increase: +{self.successful_joins}")

def main():
    print("""
    ╔═══════════════════════════════════════════════╗
    ║       SHOPEE RDP OPTIMIZED BOT                ║
    ║         WINDOWS RDP SPECIALIZED               ║
    ║               BY FLASHCODE                    ║
    ╚═══════════════════════════════════════════════╝
    
    🖥️ Windows RDP Optimized Browser Bot 
    ⚡ Fast processing dengan minimal resource usage
    🛡️ Error handling khusus untuk RDP environment
    📊 Real-time monitoring & statistics
    ✨ Uses CORRECT share URL format
    """)
    
    bot = RDPOptimizedBot()
    
    # Check prerequisites
    print("🔍 Checking system requirements...")
    if not bot.check_chrome_installation():
        input("\nPress Enter to exit...")
        return
    
    # Load accounts
    print("\n📁 Loading accounts...")
    if not bot.load_accounts():
        input("\nPress Enter to exit...")
        return
    
    print(f"\n📊 Total accounts loaded: {len(bot.accounts)}")
    
    # Get session ID
    while True:
        session_input = input("\n🔗 Session ID atau URL live Shopee: ").strip()
        
        if not session_input:
            print("❌ Session ID tidak boleh kosong!")
            continue
        
        # Extract session ID
        if 'live.shopee.co.id' in session_input:
            import re
            match = re.search(r'[?&]session=(\d+)', session_input)
            if match:
                session_id = match.group(1)
                break
            match = re.search(r'live\.shopee\.co\.id/(\d+)', session_input)
            if match:
                session_id = match.group(1)
                break
        elif session_input.isdigit():
            session_id = session_input
            break
        else:
            print("❌ Format tidak valid!")
    
    print(f"✅ Session ID: {session_id}")
    print(f"🔗 Target URL: https://live.shopee.co.id/share?from=live&session={session_id}")
    
    # Account selection
    while True:
        try:
            max_input = input(f"\n🔢 Berapa accounts? (max {len(bot.accounts)}, Enter=semua): ").strip()
            
            if not max_input:
                max_accounts = None
                break
            
            max_accounts = int(max_input)
            if 1 <= max_accounts <= len(bot.accounts):
                break
            else:
                print(f"❌ Range: 1-{len(bot.accounts)}")
        except ValueError:
            print("❌ Input angka!")
    
    # Threading option
    use_threading = True
    if max_accounts and max_accounts >= 6:
        threading_input = input(f"\n🧵 Use threading untuk speed? (y/n, default=y): ").lower()
        use_threading = threading_input != 'n'
    
    # Configuration summary
    accounts_count = max_accounts or len(bot.accounts)
    print(f"\n⚡ RDP BOT CONFIGURATION:")
    print(f"🌐 URL Format: Share (CORRECT format)")
    print(f"🛡️ Optimization: RDP Windows specialized")
    print(f"📊 Processing: {'Multi-threading' if use_threading else 'Sequential'}")
    print(f"🎯 Target Accounts: {accounts_count}")
    print(f"⏱️ Estimated Time: {(accounts_count * 1.5):.0f}-{(accounts_count * 2):.0f} minutes")
    
    confirm = input(f"\n🚀 Start RDP Optimized Bot? (y/n): ").lower()
    if confirm != 'y':
        print("👋 Bot cancelled!")
        return
    
    # Run bot
    try:
        bot.run_rdp_bot(session_id, max_accounts, use_threading)
    except KeyboardInterrupt:
        print("\n⚠️ Bot stopped by user!")
        bot.running = False
        bot.cleanup_drivers()
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        bot.cleanup_drivers()

if __name__ == "__main__":
    main()
