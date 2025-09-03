#!/usr/bin/env python3
"""
SUPER STEALTH BOT - Ultimate Anti-Detection
Bypass semua captcha dan anti-bot dengan teknik advanced
"""

import time
import random
import json
import os
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

class SuperStealthBot:
    def __init__(self):
        self.active_viewers = []
        self.session_id = None
        self.verified_cookies = []
        
        # Setup logging
        log_dir = os.path.join('bot-core', 'logs')
        os.makedirs(log_dir, exist_ok=True)
        self.log_file = os.path.join(log_dir, f'super_stealth_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
        
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
            
            self.log(f"✅ Loaded {len(self.verified_cookies)} super cookies")
        except Exception as e:
            self.log(f"❌ Error loading cookies: {e}")
    
    def log(self, message):
        """Log message to console and file"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_msg = f"[{timestamp}] {message}"
        print(log_msg)
        
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_msg + "\n")
        except:
            pass
    
    def create_ultimate_stealth_options(self, viewer_index):
        """Create ultimate anti-detection Chrome options"""
        chrome_options = Options()
        
        # === ULTIMATE STEALTH BYPASS ===
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # === BYPASS DETECTION ===
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--disable-features=VizDisplayCompositor')
        chrome_options.add_argument('--disable-ipc-flooding-protection')
        chrome_options.add_argument('--no-proxy-server')
        chrome_options.add_argument('--ignore-certificate-errors-spki-list')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--ignore-ssl-errors')
        chrome_options.add_argument('--allow-running-insecure-content')
        chrome_options.add_argument('--disable-extensions-except')
        chrome_options.add_argument('--disable-plugins-discovery')
        
        # === RESOURCE BYPASS ===
        chrome_options.add_argument('--disable-logging')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--log-level=3')
        chrome_options.add_argument('--silent')
        chrome_options.add_argument('--disable-default-apps')
        chrome_options.add_argument('--disable-sync')
        chrome_options.add_argument('--disable-translate')
        
        # === FINGERPRINT BYPASS ===
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        ]
        chrome_options.add_argument(f'--user-agent={user_agents[viewer_index % len(user_agents)]}')
        
        # === PROFILE BYPASS ===
        profile_dir = os.path.abspath(os.path.join('bot-core', 'sessions', 'super', f'super_{viewer_index}_{random.randint(1000,9999)}'))
        os.makedirs(profile_dir, exist_ok=True)
        chrome_options.add_argument(f'--user-data-dir={profile_dir}')
        
        # === PREFS BYPASS ===
        chrome_options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_settings.popups": 0,
            "profile.managed_default_content_settings.images": 2,
            "profile.default_content_setting_values.media_stream": 2,
        })
        
        return chrome_options
    
    def apply_ultimate_stealth_scripts(self, driver):
        """Apply ultimate anti-detection JavaScript"""
        
        # === REMOVE WEBDRIVER TRACES ===
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        # === MOCK CHROME RUNTIME ===
        driver.execute_script("""
            window.chrome = {
                runtime: {
                    onConnect: undefined,
                    onMessage: undefined
                }
            };
        """)
        
        # === MOCK PLUGINS ===
        driver.execute_script("""
            Object.defineProperty(navigator, 'plugins', {
                get: () => [
                    {name: 'Chrome PDF Plugin', filename: 'internal-pdf-viewer'},
                    {name: 'Chrome PDF Viewer', filename: 'mhjfbmdgcfjbbpaeojofohoefgiehjai'},
                    {name: 'Native Client', filename: 'internal-nacl-plugin'}
                ]
            });
        """)
        
        # === MOCK LANGUAGES ===
        driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['id-ID', 'id', 'en-US', 'en']})")
        
        # === MOCK PERMISSIONS ===
        driver.execute_script("Object.defineProperty(navigator, 'permissions', {get: () => undefined})")
        
        # === MOCK DEVICE MEMORY ===
        driver.execute_script(f"Object.defineProperty(navigator, 'deviceMemory', {{get: () => {random.choice([4, 8, 16])}}})")
        
        # === MOCK CONNECTION ===
        driver.execute_script("""
            Object.defineProperty(navigator, 'connection', {
                get: () => ({
                    effectiveType: '4g',
                    downlink: 10,
                    rtt: 50
                })
            });
        """)
        
        # === OVERRIDE FUNCTION DETECTION ===
        driver.execute_script("""
            const originalQuery = window.document.querySelector;
            const originalQueryAll = window.document.querySelectorAll;
            const originalGetElementById = window.document.getElementById;
            
            window.document.querySelector = function(selector) {
                return originalQuery.call(document, selector);
            };
            
            window.document.querySelectorAll = function(selector) {
                return originalQueryAll.call(document, selector);
            };
            
            window.document.getElementById = function(id) {
                return originalGetElementById.call(document, id);
            };
        """)
        
        # === MOCK SCREEN PROPERTIES ===
        driver.execute_script(f"""
            Object.defineProperty(screen, 'width', {{get: () => {random.choice([1920, 1366, 1440])}}});
            Object.defineProperty(screen, 'height', {{get: () => {random.choice([1080, 768, 900])}}});
            Object.defineProperty(screen, 'colorDepth', {{get: () => {random.choice([24, 32])}}});
        """)
    
    def human_behavior_simulation(self, driver):
        """Simulate human behavior patterns"""
        
        # Random mouse movements
        try:
            driver.execute_script("""
                function simulateMouseMove() {
                    const event = new MouseEvent('mousemove', {
                        bubbles: true,
                        cancelable: true,
                        clientX: Math.random() * window.innerWidth,
                        clientY: Math.random() * window.innerHeight
                    });
                    document.dispatchEvent(event);
                }
                simulateMouseMove();
            """)
        except:
            pass
        
        # Random scroll
        try:
            scroll_amount = random.randint(100, 500)
            driver.execute_script(f"window.scrollBy(0, {scroll_amount})")
            time.sleep(random.uniform(0.5, 2))
            driver.execute_script("window.scrollTo(0, 0)")
        except:
            pass
    
    def create_super_stealth_viewer(self, cookie_data, viewer_index):
        """Create ultimate stealth viewer yang tidak terdeteksi"""
        driver = None
        try:
            self.log(f"[SUPER {viewer_index}] 🦾 Launching SUPER STEALTH mode...")
            
            # Create ultimate stealth Chrome
            chrome_options = self.create_ultimate_stealth_options(viewer_index)
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Set aggressive timeouts
            driver.set_page_load_timeout(45)
            driver.implicitly_wait(15)
            
            # Apply ultimate stealth scripts
            self.apply_ultimate_stealth_scripts(driver)
            
            # === PHASE 1: WARM UP BROWSER ===
            self.log(f"[SUPER {viewer_index}] 🔥 Warming up browser...")
            
            # Visit blank page first
            driver.get("about:blank")
            time.sleep(2)
            
            # Visit popular site untuk establish legitimacy
            try:
                driver.get("https://www.google.co.id")
                time.sleep(random.uniform(3, 6))
                self.human_behavior_simulation(driver)
            except:
                self.log(f"[SUPER {viewer_index}] ⚠️ Google visit failed, continuing...")
            
            # === PHASE 2: SHOPEE INFILTRATION ===
            self.log(f"[SUPER {viewer_index}] 🛒 Infiltrating Shopee...")
            
            try:
                driver.get("https://shopee.co.id")
                time.sleep(random.uniform(4, 8))
                
                # Apply stealth scripts again after page load
                self.apply_ultimate_stealth_scripts(driver)
                
                # Simulate human behavior
                self.human_behavior_simulation(driver)
                
            except Exception as e:
                self.log(f"[SUPER {viewer_index}] ⚠️ Shopee access issue: {e}")
            
            # === PHASE 3: COOKIE INJECTION ===
            self.log(f"[SUPER {viewer_index}] 🍪 Injecting verified cookies...")
            
            # Clear existing cookies
            driver.delete_all_cookies()
            
            # Inject essential cookies
            essential_cookies = [
                {'name': 'SPC_F', 'value': cookie_data['cookies']['SPC_F']},
                {'name': 'SPC_U', 'value': cookie_data['cookies']['SPC_U']},
                {'name': 'SPC_ST', 'value': cookie_data['cookies']['SPC_ST']},
                {'name': 'SPC_EC', 'value': cookie_data['cookies']['SPC_EC']},
            ]
            
            success_count = 0
            for cookie in essential_cookies:
                try:
                    driver.add_cookie({
                        'name': cookie['name'],
                        'value': cookie['value'],
                        'domain': '.shopee.co.id',
                        'path': '/',
                        'secure': False,
                        'httpOnly': False
                    })
                    success_count += 1
                    self.log(f"[SUPER {viewer_index}] ✅ {cookie['name']} injected")
                except Exception as e:
                    self.log(f"[SUPER {viewer_index}] ❌ {cookie['name']} failed: {e}")
            
            if success_count < 2:
                self.log(f"[SUPER {viewer_index}] ❌ Cookie injection failed!")
                driver.quit()
                return False
            
            # === PHASE 4: AUTHENTICATION VERIFICATION ===
            self.log(f"[SUPER {viewer_index}] 🔐 Verifying authentication...")
            
            driver.refresh()
            time.sleep(random.uniform(5, 10))
            
            # Apply stealth scripts after refresh
            self.apply_ultimate_stealth_scripts(driver)
            
            # === PHASE 5: LIVE STREAM INFILTRATION ===
            self.log(f"[SUPER {viewer_index}] 🎯 Targeting live stream...")
            
            # Test direct API join first
            try:
                join_url = f"https://live.shopee.co.id/api/v1/session/{self.session_id}/joinv2"
                
                # Get current cookies
                cookies = {}
                for cookie in driver.get_cookies():
                    cookies[cookie['name']] = cookie['value']
                
                headers = {
                    'User-Agent': driver.execute_script("return navigator.userAgent;"),
                    'Referer': f'https://live.shopee.co.id/share?from=live&session={self.session_id}',
                    'Content-Type': 'application/json',
                    'Accept': 'application/json, text/plain, */*',
                    'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
                    'X-Requested-With': 'XMLHttpRequest'
                }
                
                response = requests.post(join_url, cookies=cookies, headers=headers, timeout=15)
                
                self.log(f"[SUPER {viewer_index}] API Response: {response.status_code}")
                
                if response.status_code == 200:
                    self.log(f"[SUPER {viewer_index}] 🎯 API JOIN SUCCESS!")
                
            except Exception as e:
                self.log(f"[SUPER {viewer_index}] ⚠️ API join error: {e}")
            
            # === PHASE 6: BROWSER STREAM ACCESS ===
            live_url = f"https://live.shopee.co.id/share?from=live&session={self.session_id}"
            self.log(f"[SUPER {viewer_index}] 📺 Accessing: {live_url}")
            
            try:
                driver.get(live_url)
                time.sleep(random.uniform(8, 15))
                
                # Apply final stealth scripts
                self.apply_ultimate_stealth_scripts(driver)
                
                # Final human behavior simulation
                self.human_behavior_simulation(driver)
                
            except Exception as e:
                self.log(f"[SUPER {viewer_index}] ⚠️ Live access error: {e}")
            
            # === PHASE 7: SUCCESS VERIFICATION ===
            time.sleep(5)
            
            try:
                current_url = driver.current_url
                page_title = driver.title
                
                self.log(f"[SUPER {viewer_index}] Final URL: {current_url}")
                self.log(f"[SUPER {viewer_index}] Page Title: {page_title}")
                
                # Check for anti-bot patterns
                blocked_patterns = ['captcha', 'verify', 'anti_bot', 'robot', 'blocked', 'login']
                
                # URL check
                url_blocked = any(pattern in current_url.lower() for pattern in blocked_patterns)
                # Title check  
                title_blocked = any(pattern in page_title.lower() for pattern in blocked_patterns)
                
                if not url_blocked and not title_blocked and 'live.shopee.co.id' in current_url:
                    self.log(f"[SUPER {viewer_index}] 🏆 SUPER STEALTH SUCCESS!")
                    
                    # Add to active viewers
                    self.active_viewers.append({
                        'driver': driver,
                        'viewer_id': viewer_index,
                        'type': 'super_stealth',
                        'status': 'active',
                        'account_id': cookie_data.get('account_id', f'super_{viewer_index}'),
                        'created_at': datetime.now(),
                        'final_url': current_url,
                        'page_title': page_title
                    })
                    
                    return True
                else:
                    self.log(f"[SUPER {viewer_index}] 🚫 BLOCKED/REDIRECTED!")
                    self.log(f"[SUPER {viewer_index}] Blocked patterns detected")
                    driver.quit()
                    return False
                    
            except Exception as e:
                self.log(f"[SUPER {viewer_index}] ❌ Verification error: {e}")
                driver.quit()
                return False
                
        except Exception as e:
            self.log(f"[SUPER {viewer_index}] 💥 CRITICAL ERROR: {str(e)[:150]}...")
            if driver:
                try:
                    driver.quit()
                except:
                    pass
            return False
    
    def start_super_stealth_bot(self, session_id, target_viewers=3):
        """Start super stealth bot"""
        self.session_id = session_id
        
        self.log("=" * 60)
        self.log("🦾 SUPER STEALTH SHOPEE BOT")
        self.log("Ultimate Anti-Detection Technology")
        self.log("=" * 60)
        self.log(f"🎯 Session: {session_id}")
        self.log(f"🦾 Target: {target_viewers} super stealth viewers")
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
        
        self.log(f"\n🦾 LAUNCHING {len(session_cookies)} SUPER STEALTH BROWSERS...")
        
        # Launch browsers with extended delays
        successful_viewers = 0
        for i, cookie_data in enumerate(session_cookies):
            self.log(f"\n{'='*20} SUPER VIEWER {i+1}/{len(session_cookies)} {'='*20}")
            
            if self.create_super_stealth_viewer(cookie_data, i + 1):
                successful_viewers += 1
                self.log(f"[SUPER {i+1}] ✅ SUCCESS - Total: {successful_viewers}")
            else:
                self.log(f"[SUPER {i+1}] ❌ FAILED")
            
            # Extended delay between launches untuk avoid detection
            if i < len(session_cookies) - 1:
                delay = random.uniform(15, 30)
                self.log(f"⏳ Extended delay {delay:.1f}s before next super viewer...")
                time.sleep(delay)
        
        # Final status
        self.log("\n" + "=" * 60)
        self.log("🦾 SUPER STEALTH BOT FINAL STATUS")
        self.log(f"✅ Successful: {successful_viewers}/{target_viewers}")
        self.log(f"🦾 Active Super Browsers: {len(self.active_viewers)}")
        
        if len(self.active_viewers) > 0:
            self.log("\nActive Viewers:")
            for viewer in self.active_viewers:
                self.log(f"  🦾 Viewer {viewer['viewer_id']}: {viewer['account_id']} - {viewer['status']}")
        
        self.log("=" * 60)
        
        if successful_viewers > 0:
            self.log("\n💚 Super stealth viewers active! Press Ctrl+C to stop...")
            try:
                while True:
                    time.sleep(60)  # Extended health check interval
                    self.super_health_check()
            except KeyboardInterrupt:
                self.log("\n🛑 Stopping super stealth bot...")
                self.cleanup_super()
        else:
            self.log("❌ No super stealth viewers created!")
    
    def super_health_check(self):
        """Extended health check for super viewers"""
        alive_count = 0
        for viewer in self.active_viewers[:]:
            try:
                current_url = viewer['driver'].current_url
                if 'live.shopee.co.id' in current_url:
                    alive_count += 1
                else:
                    self.log(f"❌ Super viewer {viewer['viewer_id']} redirected: {current_url}")
                    self.active_viewers.remove(viewer)
                    viewer['driver'].quit()
            except:
                self.active_viewers.remove(viewer)
                self.log(f"❌ Super viewer {viewer['viewer_id']} died")
        
        self.log(f"💚 Super Health: {alive_count} browsers alive and streaming")
    
    def cleanup_super(self):
        """Cleanup super stealth resources"""
        self.log("🧹 Cleaning up super stealth browsers...")
        for viewer in self.active_viewers:
            if 'driver' in viewer:
                try:
                    viewer['driver'].quit()
                except:
                    pass

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) >= 3:
        session_id = sys.argv[1]
        viewer_count = int(sys.argv[2])
        
        print("🦾" + "=" * 60)
        print("       SUPER STEALTH SHOPEE BOT - Ultimate Mode")
        print("🦾" + "=" * 60)
        
        bot = SuperStealthBot()
        bot.start_super_stealth_bot(session_id, viewer_count)
    else:
        session_id = input("Session ID: ").strip()
        viewer_count = int(input("Jumlah super stealth viewers: ").strip())
        
        bot = SuperStealthBot()
        bot.start_super_stealth_bot(session_id, viewer_count)
