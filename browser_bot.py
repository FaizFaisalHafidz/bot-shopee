#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shopee Live Streaming Bot - Browser Automation Version
Bot yang menggunakan browser Chrome untuk real viewer simulation
"""

import time
import random
import csv
import threading
from datetime import datetime
import os
import sys

# Browser automation imports
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException, WebDriverException
    
    # Try to import webdriver-manager for automatic ChromeDriver management
    try:
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
        WEBDRIVER_MANAGER_AVAILABLE = True
        print("✅ webdriver-manager available - Auto ChromeDriver management enabled")
    except ImportError:
        WEBDRIVER_MANAGER_AVAILABLE = False
        print("⚠️  webdriver-manager not available - Using system ChromeDriver")
        
except ImportError:
    print("❌ Selenium not installed!")
    print("💡 Install with: pip install selenium webdriver-manager")
    sys.exit(1)

class ShopeeBot:
    def __init__(self):
        self.accounts = []
        self.session_id = None
        self.running = False
        self.drivers = []  # Store all browser instances
        
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
    
    def create_chrome_driver(self, account):
        """Buat Chrome driver dengan cookies untuk akun"""
        try:
            chrome_options = Options()
            
            # Browser settings untuk real user simulation
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Random user agent
            user_agents = [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
            ]
            chrome_options.add_argument(f'--user-agent={random.choice(user_agents)}')
            
            # Create driver with automatic ChromeDriver management
            try:
                if WEBDRIVER_MANAGER_AVAILABLE:
                    # Use webdriver-manager for automatic ChromeDriver download
                    service = Service(ChromeDriverManager().install())
                    driver = webdriver.Chrome(service=service, options=chrome_options)
                else:
                    # Fallback to system ChromeDriver
                    driver = webdriver.Chrome(options=chrome_options)
            except Exception as e:
                print(f"⚠️  ChromeDriver version issue detected: {str(e)}")
                print("💡 Trying alternative ChromeDriver setup...")
                
                # Try with explicit executable path
                chrome_paths = [
                    './chromedriver.exe',
                    'C:\\Windows\\System32\\chromedriver.exe',
                    'chromedriver.exe'
                ]
                
                driver = None
                for chrome_path in chrome_paths:
                    try:
                        if os.path.exists(chrome_path):
                            driver = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)
                            break
                    except:
                        continue
                
                if not driver:
                    raise WebDriverException("No compatible ChromeDriver found")
            
            # Anti-detection script
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            # Navigate to Shopee first
            driver.get("https://shopee.co.id")
            time.sleep(2)
            
            # Add cookies
            for name, value in account['cookies'].items():
                try:
                    driver.add_cookie({
                        'name': name,
                        'value': value,
                        'domain': '.shopee.co.id'
                    })
                except:
                    pass  # Some cookies might fail, that's ok
            
            return driver
            
        except WebDriverException as e:
            print(f"❌ Error creating Chrome driver: {e}")
            if "This version of ChromeDriver only supports Chrome version" in str(e):
                print("💡 SOLUTION: Run fix_chromedriver_version.bat to download compatible ChromeDriver")
                print("💡 Or install webdriver-manager: pip install webdriver-manager")
            else:
                print("💡 Make sure ChromeDriver is installed and compatible with Chrome version")
            return None
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return None
    
    def browser_join_live(self, account, session_id):
        """Join live streaming menggunakan browser Chrome"""
        driver = None
        try:
            current_time = datetime.now().strftime("%H:%M:%S")
            print(f"[{current_time}] 🚀 Opening Chrome for User: {account['user_id'][:8]}...")
            
            # Create Chrome driver dengan cookies
            driver = self.create_chrome_driver(account)
            if not driver:
                return False
            
            # Navigate ke live streaming dengan format share
            live_url = f"https://live.shopee.co.id/share?from=live&session={session_id}"
            print(f"[{current_time}] 🔗 Navigating to SHARE URL: {live_url}")
            print(f"[{current_time}] 📋 Using correct share format with from=live parameter")
            
            driver.get(live_url)
            
            # Wait for page to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            current_time = datetime.now().strftime("%H:%M:%S")
            print(f"[{current_time}] ✅ BROWSER VIEWER = Success! User: {account['user_id'][:8]}...")
            
            # Keep browser open untuk simulate real viewer
            keep_alive_time = random.randint(30, 120)  # 30 detik - 2 menit
            print(f"[{current_time}] ⏱️ Keeping browser alive for {keep_alive_time}s...")
            
            time.sleep(keep_alive_time)
            
            return True
            
        except TimeoutException:
            current_time = datetime.now().strftime("%H:%M:%S")
            print(f"[{current_time}] ❌ BROWSER VIEWER = Timeout! User: {account['user_id'][:8]}...")
            return False
        except Exception as e:
            current_time = datetime.now().strftime("%H:%M:%S")
            print(f"[{current_time}] ❌ BROWSER VIEWER = Error! User: {account['user_id'][:8]}... Error: {str(e)}")
            return False
        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass
    
    def browser_viewer_worker(self, account_batch, session_id):
        """Worker untuk browser viewer"""
        for account in account_batch:
            if not self.running:
                break
            
            # Join menggunakan browser
            self.browser_join_live(account, session_id)
            
            # Interval antar akun
            time.sleep(random.uniform(3, 8))
    
    def run_browser_bot(self, session_id, max_accounts=None):
        """Menjalankan bot browser viewer"""
        self.session_id = session_id
        self.running = True
        
        # Limit akun jika diperlukan
        accounts_to_use = self.accounts[:max_accounts] if max_accounts else self.accounts
        
        print(f"\n🚀 Starting Browser Bot dengan {len(accounts_to_use)} akun...")
        print(f"🎯 Target Session ID: {session_id}")
        print(f"🌐 Each account akan membuka Chrome tab")
        print("\n" + "="*50)
        
        # Bagi akun ke beberapa thread (3-4 browser bersamaan max)
        max_concurrent = min(4, len(accounts_to_use))
        chunk_size = len(accounts_to_use) // max_concurrent
        
        if chunk_size == 0:
            chunk_size = 1
        
        threads = []
        
        for i in range(0, len(accounts_to_use), chunk_size):
            account_batch = accounts_to_use[i:i + chunk_size]
            if account_batch:  # Make sure batch is not empty
                thread = threading.Thread(
                    target=self.browser_viewer_worker,
                    args=(account_batch, session_id)
                )
                threads.append(thread)
                thread.start()
                
                # Delay antar thread untuk menghindari spike
                time.sleep(2)
        
        # Wait for all threads
        for thread in threads:
            thread.join()
        
        self.running = False
        print("\n" + "="*50)
        print("🎉 Browser Bot selesai!")
        print(f"📊 Total processed: {len(accounts_to_use)} akun")

def main():
    print("""
    ╔═══════════════════════════════════════════════╗
    ║       SHOPEE LIVE BROWSER AUTOMATION BOT      ║
    ║               BY FLASHCODE                    ║
    ╚═══════════════════════════════════════════════╝
    
    🌐 Real Browser Viewer Bot 
    🔥 Each account opens Chrome tab
    ✨ Simulate real user behavior
    """)
    
    bot = ShopeeBot()
    
    # Load akun
    if not bot.load_accounts():
        return
    
    print(f"\n📊 Total akun tersedia: {len(bot.accounts)}")
    
    # Get session ID
    while True:
        session_input = input("\n🔗 Masukkan Session ID atau URL live Shopee: ").strip()
        
        if not session_input:
            print("❌ Session ID tidak boleh kosong!")
            continue
        
        # Extract session ID jika berupa URL
        if 'live.shopee.co.id' in session_input:
            import re
            # Handle format: https://live.shopee.co.id/share?from=live&session=154212172
            match = re.search(r'[?&]session=(\d+)', session_input)
            if match:
                session_id = match.group(1)
                print(f"✅ Session ID extracted: {session_id}")
                break
            # Handle legacy format: https://live.shopee.co.id/154212172  
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
    
    # Ask for number of accounts to use
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
    
    # Warning about browser automation
    print(f"\n⚠️  BROWSER AUTOMATION WARNING:")
    print(f"📱 Bot akan membuka {max_accounts or len(bot.accounts)} tab Chrome")
    print(f"💻 Pastikan RDP/PC punya RAM cukup")
    print(f"🔄 Each tab akan aktif selama 30s - 2 menit")
    print(f"👀 Viewer count akan naik secara real-time!")
    
    confirm = input(f"\n🚀 Lanjutkan? (y/n): ").lower()
    if confirm != 'y':
        print("👋 Bot dibatalkan!")
        return
    
    # Run browser bot
    try:
        bot.run_browser_bot(session_id, max_accounts)
    except KeyboardInterrupt:
        print("\n⚠️ Bot dihentikan oleh user!")
        bot.running = False

if __name__ == "__main__":
    main()
