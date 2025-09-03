#!/usr/bin/env python3
"""
STEALTH SHOPEE BOT - Anti-Detection Version
Menggunakan teknik evasion untuk menghindari anti-bot detection
"""

import time
import random
import json
import os
import threading
import requests
import csv
import uuid
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class StealthShopeeBot:
    def __init__(self):
        self.session_cookies = []
        self.active_viewers = []
        self.session_id = None
        self.target_viewers = 10
        self.verified_cookies = []
        
        # Setup logging
        log_dir = os.path.join('bot-core', 'logs')
        os.makedirs(log_dir, exist_ok=True)
        self.log_file = os.path.join(log_dir, f'stealth_bot_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
        
        # Load verified cookies
        self.load_verified_cookies()
        
    def load_verified_cookies(self):
        """Load verified cookies from CSV file"""
        csv_path = os.path.join('bot-core', 'accounts', 'verified_cookies.csv')
        if not os.path.exists(csv_path):
            self.log("❌ verified_cookies.csv tidak ditemukan!")
            return
            
        try:
            with open(csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['status'] == 'active':
                        self.verified_cookies.append({
                            'account_id': row['account_id'],
                            'spc_f': row['spc_f'],
                            'spc_u': row['spc_u'], 
                            'spc_st': row['spc_st'],
                            'spc_ec': row['spc_ec'],
                            'device_id': row['device_id'],
                            'user_agent': row['user_agent']
                        })
            
            self.log(f"✅ Loaded {len(self.verified_cookies)} stealth cookies")
        except Exception as e:
            self.log(f"❌ Error loading cookies: {e}")
    
    def log(self, message):
        """Log message to console and file"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_msg = f"[{timestamp}] {message}"
        print(log_msg)
        
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_msg + "\\n")
        except:
            pass
    
    def create_stealth_chrome_options(self, profile_index, fingerprint):
        """Create ultra-stealth Chrome options - QUICK FIX VERSION"""
        chrome_options = Options()
        
        # Essential stealth arguments
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # QUICK FIX: Network stability
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--disable-features=VizDisplayCompositor')
        chrome_options.add_argument('--no-proxy-server')
        chrome_options.add_argument('--disable-background-networking')
        chrome_options.add_argument('--disable-default-apps')
        chrome_options.add_argument('--disable-sync')
        
        # QUICK FIX: Reduced resource usage
        chrome_options.add_argument('--disable-logging')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--log-level=3')
        chrome_options.add_argument('--silent')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-plugins')
        
        # Custom user agent per viewer
        chrome_options.add_argument(f'--user-agent={fingerprint["user_agent"]}')
        
        # QUICK FIX: Simpler profile directory
        profile_dir = os.path.abspath(os.path.join('bot-core', 'sessions', 'viewers', f'viewer_stealth_{profile_index}'))
        os.makedirs(profile_dir, exist_ok=True)
        chrome_options.add_argument(f'--user-data-dir={profile_dir}')
        
        return chrome_options
    
    def generate_stealth_fingerprint(self, viewer_index):
        """Generate comprehensive stealth fingerprint"""
        # Unique device ID untuk menghindari duplicate detection
        device_id = str(uuid.uuid4())
        
        # Pool user agents yang berbeda-beda
        user_agents = [
            f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(115, 121)}.0.{random.randint(1000, 9999)}.{random.randint(100, 999)} Safari/537.36",
            f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_{random.randint(15, 16)}_{random.randint(0, 7)}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(115, 121)}.0.{random.randint(1000, 9999)}.{random.randint(100, 999)} Safari/537.36",
            f"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(115, 121)}.0.{random.randint(1000, 9999)}.{random.randint(100, 999)} Safari/537.36"
        ]
        
        return {
            'device_id': device_id,
            'user_agent': user_agents[viewer_index % len(user_agents)],
            'screen_width': random.randint(1366, 1920),
            'screen_height': random.randint(768, 1080),
            'color_depth': random.choice([24, 32]),
            'timezone': random.choice(['Asia/Jakarta', 'Asia/Makassar']),
            'language': random.choice(['id-ID', 'id', 'en-US']),
            'platform': random.choice(['Win32', 'MacIntel', 'Linux x86_64'])
        }
    
    def apply_stealth_scripts(self, driver, fingerprint):
        """Apply comprehensive anti-detection scripts"""
        # Remove webdriver property
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        # Mock chrome runtime
        driver.execute_script("window.chrome = {runtime: {}}")
        
        # Mock plugins
        driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})")
        
        # Set languages
        driver.execute_script(f"Object.defineProperty(navigator, 'languages', {{get: () => ['{fingerprint['language']}', 'en']}})")
        
        # Set platform
        driver.execute_script(f"Object.defineProperty(navigator, 'platform', {{get: () => '{fingerprint['platform']}'}})")
        
        # Set screen properties
        driver.execute_script(f"""
            Object.defineProperty(screen, 'width', {{get: () => {fingerprint['screen_width']}}});
            Object.defineProperty(screen, 'height', {{get: () => {fingerprint['screen_height']}}});
            Object.defineProperty(screen, 'colorDepth', {{get: () => {fingerprint['color_depth']}}});
        """)
        
        # Mock device memory (anti-fingerprinting)
        driver.execute_script("Object.defineProperty(navigator, 'deviceMemory', {get: () => Math.floor(Math.random() * 8) + 4})")
        
        # Hide automation indicators
        driver.execute_script("window.navigator.chrome = {runtime: {}}")
        driver.execute_script("Object.defineProperty(navigator, 'permissions', {get: () => undefined})")
    
    def human_like_delay(self, min_seconds=2, max_seconds=8):
        """Random human-like delay"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
        return delay
    
    def create_stealth_browser_viewer(self, cookie_data, viewer_index):
        """QUICK FIX: Simplified stealth browser creation"""
        driver = None
        try:
            self.log(f"[STEALTH {viewer_index}] 🥷 Starting stealth mode...")
            
            # Generate unique fingerprint
            fingerprint = self.generate_stealth_fingerprint(viewer_index)
            self.log(f"[STEALTH {viewer_index}] 🎭 Device: {fingerprint['device_id'][:8]}...")
            
            # Create stealth Chrome
            chrome_options = self.create_stealth_chrome_options(f"stealth_{viewer_index}", fingerprint)
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # QUICK FIX: Set timeouts
            driver.set_page_load_timeout(30)
            driver.implicitly_wait(10)
            
            # Apply stealth scripts
            self.apply_stealth_scripts(driver, fingerprint)
            
            # QUICK FIX: Direct to Shopee instead of Google first
            self.log(f"[STEALTH {viewer_index}] 🛒 Direct to Shopee...")
            driver.get("https://shopee.co.id")
            time.sleep(3)
            
            # Inject cookies
            driver.delete_all_cookies()
            
            essential_cookies = [
                {'name': 'SPC_F', 'value': cookie_data['cookies']['SPC_F']},
                {'name': 'SPC_U', 'value': cookie_data['cookies']['SPC_U']},
                {'name': 'SPC_ST', 'value': cookie_data['cookies']['SPC_ST']},
                {'name': 'SPC_EC', 'value': cookie_data['cookies']['SPC_EC']},
            ]
            
            for cookie in essential_cookies:
                try:
                    driver.add_cookie({
                        'name': cookie['name'],
                        'value': cookie['value'],
                        'domain': '.shopee.co.id',
                        'path': '/'
                    })
                    self.log(f"[STEALTH {viewer_index}] ✅ Cookie {cookie['name']} injected")
                except Exception as e:
                    self.log(f"[STEALTH {viewer_index}] ⚠️ Cookie {cookie['name']}: {e}")
            
            # QUICK FIX: Refresh with cookies
            self.log(f"[STEALTH {viewer_index}] 🔄 Refreshing with cookies...")
            driver.refresh()
            time.sleep(5)
            
            # QUICK FIX: Try direct API join first
            session_id = self.session_id
            join_url = f"https://live.shopee.co.id/api/v1/session/{session_id}/joinv2"
            
            self.log(f"[STEALTH {viewer_index}] 📡 Testing API join...")
            
            # Get cookies for API request
            cookies = {}
            for cookie in driver.get_cookies():
                cookies[cookie['name']] = cookie['value']
            
            try:
                response = requests.post(join_url, cookies=cookies, timeout=10)
                self.log(f"[STEALTH {viewer_index}] API Response: {response.status_code}")
                
                if response.status_code == 200:
                    self.log(f"[STEALTH {viewer_index}] 🎯 API JOIN SUCCESS!")
                    
                    # Now visit the live page
                    live_url = f"https://live.shopee.co.id/share?from=live&session={session_id}"
                    self.log(f"[STEALTH {viewer_index}] 📺 Opening live: {live_url}")
                    
                    driver.get(live_url)
                    time.sleep(5)
                    
                    # Check success
                    current_url = driver.current_url
                    if 'live.shopee.co.id' in current_url and 'login' not in current_url:
                        self.log(f"[STEALTH {viewer_index}] ✅ STEALTH SUCCESS!")
                        self.log(f"[STEALTH {viewer_index}] Final URL: {current_url}")
                        
                        # Add to active viewers
                        self.active_viewers.append({
                            'driver': driver,
                            'viewer_id': viewer_index,
                            'type': 'stealth_browser',
                            'status': 'active',
                            'account_id': cookie_data.get('account_id', f'stealth_{viewer_index}'),
                            'device_id': fingerprint['device_id'],
                            'created_at': datetime.now()
                        })
                        
                        return True
                    else:
                        self.log(f"[STEALTH {viewer_index}] ❌ LOGIN REDIRECT: {current_url}")
                        
                else:
                    self.log(f"[STEALTH {viewer_index}] ❌ API Failed: {response.status_code}")
                    
            except Exception as e:
                self.log(f"[STEALTH {viewer_index}] ❌ API Error: {e}")
            
            # If API failed, try browser method
            live_url = f"https://live.shopee.co.id/share?from=live&session={session_id}"
            self.log(f"[STEALTH {viewer_index}] � Fallback browser: {live_url}")
            
            driver.get(live_url)
            time.sleep(7)
            
            current_url = driver.current_url
            if 'live.shopee.co.id' in current_url and 'login' not in current_url:
                self.log(f"[STEALTH {viewer_index}] ✅ BROWSER SUCCESS!")
                self.log(f"[STEALTH {viewer_index}] Final URL: {current_url}")
                
                self.active_viewers.append({
                    'driver': driver,
                    'viewer_id': viewer_index,
                    'type': 'stealth_browser',
                    'status': 'active',
                    'account_id': cookie_data.get('account_id', f'stealth_{viewer_index}'),
                    'device_id': fingerprint['device_id'],
                    'created_at': datetime.now()
                })
                
                return True
            else:
                self.log(f"[STEALTH {viewer_index}] ❌ FAILED: {current_url}")
                driver.quit()
                return False
                
        except Exception as e:
            self.log(f"[STEALTH {viewer_index}] 💥 CRITICAL ERROR: {str(e)[:100]}...")
            if driver:
                try:
                    driver.quit()
                except:
                    pass
            return False
    
    def start_stealth_bot(self, session_id, target_viewers=3):
        """Start stealth bot"""
        self.session_id = session_id
        
        self.log("=" * 60)
        self.log("🥷 STEALTH SHOPEE BOT")
        self.log("=" * 60)
        self.log(f"🎯 Session: {session_id}")
        self.log(f"🎭 Target: {target_viewers} stealth viewers")
        self.log("=" * 60)
        
        if not self.verified_cookies:
            self.log("❌ No cookies available!")
            return
        
        # Prepare session cookies
        cookies_available = min(target_viewers, len(self.verified_cookies))
        session_cookies = []
        
        for i in range(cookies_available):
            cookie_data = self.verified_cookies[i]
            session_cookie = {
                'cookies': {
                    'SPC_F': cookie_data['spc_f'],
                    'SPC_U': cookie_data['spc_u'],
                    'SPC_ST': cookie_data['spc_st'],
                    'SPC_EC': cookie_data['spc_ec']
                },
                'account_id': cookie_data['account_id']
            }
            session_cookies.append(session_cookie)
        
        self.log(f"\\n🥷 LAUNCHING {len(session_cookies)} STEALTH BROWSERS...")
        
        # Launch browsers sequentially (to avoid detection)
        successful_viewers = 0
        for i, cookie_data in enumerate(session_cookies):
            self.log(f"\\n--- STEALTH VIEWER {i+1}/{len(session_cookies)} ---")
            
            if self.create_stealth_browser_viewer(cookie_data, i + 1):
                successful_viewers += 1
            
            # Delay between launches
            if i < len(session_cookies) - 1:
                delay = random.uniform(10, 20)
                self.log(f"⏳ Delay {delay:.1f}s before next viewer...")
                time.sleep(delay)
        
        # Final status
        self.log("\\n" + "=" * 60)
        self.log("🥷 STEALTH BOT STATUS")
        self.log(f"✅ Successful: {successful_viewers}/{target_viewers}")
        self.log(f"🎭 Active Stealth Browsers: {len(self.active_viewers)}")
        self.log("=" * 60)
        
        if successful_viewers > 0:
            self.log("\\n💚 Stealth viewers active! Press Ctrl+C to stop...")
            try:
                while True:
                    time.sleep(30)
                    self.stealth_health_check()
            except KeyboardInterrupt:
                self.log("\\n🛑 Stopping stealth bot...")
                self.cleanup_stealth()
        else:
            self.log("❌ No stealth viewers created!")
    
    def stealth_health_check(self):
        """Check stealth viewers health"""
        alive_count = 0
        for viewer in self.active_viewers[:]:
            try:
                viewer['driver'].current_url
                alive_count += 1
            except:
                self.active_viewers.remove(viewer)
                self.log(f"❌ Stealth viewer {viewer['viewer_id']} died")
        
        self.log(f"💚 Health: {alive_count} stealth browsers alive")
    
    def cleanup_stealth(self):
        """Cleanup stealth resources"""
        self.log("🧹 Cleaning up stealth browsers...")
        for viewer in self.active_viewers:
            if 'driver' in viewer:
                try:
                    viewer['driver'].quit()
                except:
                    pass

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) >= 3:
        # Run dengan arguments dari run.bat
        session_id = sys.argv[1]
        viewer_count = int(sys.argv[2])
        
        print("🥷" + "=" * 60)
        print("           STEALTH SHOPEE BOT - Windows Mode")
        print("🥷" + "=" * 60)
        
        bot = StealthShopeeBot()
        bot.start_stealth_bot(session_id, viewer_count)
    else:
        # Interactive mode
        session_id = input("Session ID: ").strip()
        viewer_count = int(input("Jumlah viewers: ").strip())
        
        bot = StealthShopeeBot()
        bot.start_stealth_bot(session_id, viewer_count)
