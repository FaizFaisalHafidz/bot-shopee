#!/usr/bin/env python3
"""
GHOST MODE BOT - Invisible Bypass
Menggunakan teknik ekstrem untuk bypass anti-bot Shopee
"""

import time
import random
import json
import os
import requests
import csv
import uuid
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class GhostModeBot:
    def __init__(self):
        self.active_viewers = []
        self.session_id = None
        self.verified_cookies = []
        
        # Setup logging
        log_dir = os.path.join('bot-core', 'logs')
        os.makedirs(log_dir, exist_ok=True)
        self.log_file = os.path.join(log_dir, f'ghost_mode_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
        
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
            
            self.log(f"✅ Loaded {len(self.verified_cookies)} ghost cookies")
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
    
    def test_pure_api_ghost_method(self, session_id):
        """Test pure API dengan advanced spoofing"""
        self.log("👻 === GHOST API INFILTRATION ===")
        
        success_count = 0
        
        for i, cookie_data in enumerate(self.verified_cookies):
            self.log(f"\n--- GHOST API {i+1}/{len(self.verified_cookies)} ---")
            self.log(f"👤 Account: {cookie_data['account_id']}")
            
            try:
                # Multiple endpoint attempts dengan berbagai methods
                endpoints_methods = [
                    (f"https://live.shopee.co.id/api/v1/session/{session_id}/joinv2", "POST"),
                    (f"https://live.shopee.co.id/api/v1/session/{session_id}/join", "POST"),
                    (f"https://shopee.co.id/api/v4/live/session/{session_id}/join", "POST"),
                    (f"https://live.shopee.co.id/api/v1/session/{session_id}/viewer/join", "POST"),
                    (f"https://live.shopee.co.id/api/v2/session/{session_id}/joinv2", "POST")
                ]
                
                for endpoint, method in endpoints_methods:
                    try:
                        # Advanced cookie setup
                        cookies = {
                            'SPC_F': cookie_data['spc_f'],
                            'SPC_U': cookie_data['spc_u'],
                            'SPC_ST': cookie_data['spc_st'],
                            'SPC_EC': cookie_data['spc_ec'],
                            'REC_T_ID': str(uuid.uuid4()),
                            'SPC_R_T_ID': f"REQ_{int(time.time())}_{random.randint(10000,99999)}",
                            'SPC_T_IV': str(random.randint(100000,999999))
                        }
                        
                        # Advanced headers untuk mimic real request
                        headers = {
                            'User-Agent': cookie_data['user_agent'],
                            'Accept': 'application/json, text/plain, */*',
                            'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
                            'Accept-Encoding': 'gzip, deflate, br',
                            'Content-Type': 'application/json',
                            'Origin': 'https://live.shopee.co.id',
                            'Referer': f'https://live.shopee.co.id/share?from=live&session={session_id}',
                            'X-Requested-With': 'XMLHttpRequest',
                            'X-Shopee-Language': 'id',
                            'X-API-SOURCE': 'pc',
                            'Sec-Fetch-Dest': 'empty',
                            'Sec-Fetch-Mode': 'cors',
                            'Sec-Fetch-Site': 'same-origin',
                            'Sec-CH-UA': '"Chromium";v="121", "Not A(Brand";v="99"',
                            'Sec-CH-UA-Mobile': '?0',
                            'Sec-CH-UA-Platform': '"Windows"',
                            'DNT': '1',
                            'Connection': 'keep-alive',
                            'Upgrade-Insecure-Requests': '1'
                        }
                        
                        # Request body for POST
                        payload = {
                            'session_id': session_id,
                            'device_id': cookie_data['device_id'],
                            'client_type': 'web',
                            'source': 'live_share'
                        }
                        
                        # Send request
                        if method == "POST":
                            response = requests.post(
                                endpoint, 
                                headers=headers,
                                cookies=cookies,
                                json=payload,
                                timeout=15,
                                allow_redirects=False
                            )
                        else:
                            response = requests.get(
                                endpoint, 
                                headers=headers,
                                cookies=cookies,
                                timeout=15,
                                allow_redirects=False
                            )
                        
                        self.log(f"  🎯 {method} {endpoint.split('/')[-1]}: {response.status_code}")
                        
                        # Check response
                        if response.status_code == 200:
                            try:
                                data = response.json()
                                self.log(f"  ✅ GHOST SUCCESS: {str(data)[:100]}...")
                                success_count += 1
                                break
                            except:
                                self.log(f"  ✅ GHOST SUCCESS: {response.text[:100]}...")
                                success_count += 1
                                break
                        elif response.status_code == 302 or response.status_code == 301:
                            redirect_url = response.headers.get('Location', 'No redirect')
                            self.log(f"  🔄 REDIRECT: {redirect_url}")
                        else:
                            self.log(f"  ❌ FAILED: {response.status_code}")
                            
                    except Exception as e:
                        self.log(f"  💥 ERROR: {str(e)[:50]}...")
                        continue
                
            except Exception as e:
                self.log(f"❌ Account {cookie_data['account_id']} error: {e}")
            
            # Random delay
            time.sleep(random.uniform(3, 8))
        
        self.log(f"\n👻 GHOST API RESULTS: {success_count}/{len(self.verified_cookies)} successful")
        return success_count
    
    def create_invisible_browser(self, cookie_data, viewer_index):
        """Create invisible browser dengan extreme stealth"""
        driver = None
        try:
            self.log(f"[GHOST {viewer_index}] 👻 Entering ghost mode...")
            
            # EXTREME stealth Chrome options
            chrome_options = Options()
            
            # === INVISIBILITY CLOAK ===
            chrome_options.add_argument('--headless=new')  # Invisible mode
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--disable-software-rasterizer')
            
            # === ANTI-DETECTION EXTREME ===
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # === NETWORK CLOAKING ===
            chrome_options.add_argument('--disable-web-security')
            chrome_options.add_argument('--disable-features=VizDisplayCompositor')
            chrome_options.add_argument('--no-proxy-server')
            chrome_options.add_argument('--ignore-certificate-errors')
            chrome_options.add_argument('--ignore-ssl-errors')
            chrome_options.add_argument('--allow-running-insecure-content')
            chrome_options.add_argument('--disable-background-networking')
            chrome_options.add_argument('--disable-default-apps')
            chrome_options.add_argument('--disable-sync')
            chrome_options.add_argument('--disable-translate')
            chrome_options.add_argument('--disable-ipc-flooding-protection')
            
            # === STEALTH HEADERS ===
            chrome_options.add_argument(f'--user-agent={cookie_data["user_agent"]}')
            chrome_options.add_argument('--disable-logging')
            chrome_options.add_argument('--log-level=3')
            chrome_options.add_argument('--silent')
            
            # === GHOST PROFILE ===
            profile_dir = os.path.abspath(os.path.join('bot-core', 'sessions', 'ghost', f'ghost_{viewer_index}_{int(time.time())}'))
            os.makedirs(profile_dir, exist_ok=True)
            chrome_options.add_argument(f'--user-data-dir={profile_dir}')
            
            # === ADVANCED PREFS ===
            chrome_options.add_experimental_option("prefs", {
                "profile.default_content_setting_values.notifications": 2,
                "profile.default_content_settings.popups": 0,
                "profile.managed_default_content_settings.images": 2,
                "profile.default_content_setting_values.media_stream": 2,
                "profile.default_content_setting_values.geolocation": 2,
                "profile.default_content_setting_values.camera": 2,
                "profile.default_content_setting_values.microphone": 2,
            })
            
            # Enable performance logging for network monitoring
            caps = DesiredCapabilities.CHROME
            caps['goog:loggingPrefs'] = {'performance': 'ALL', 'browser': 'ALL'}
            
            # Create invisible driver
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options, desired_capabilities=caps)
            driver.set_page_load_timeout(45)
            driver.implicitly_wait(20)
            
            # === PHASE 1: GHOST INITIALIZATION ===
            self.log(f"[GHOST {viewer_index}] 🌫️ Initializing ghost protocols...")
            
            # Enable network domain
            driver.execute_cdp_cmd('Network.enable', {})
            driver.execute_cdp_cmd('Runtime.enable', {})
            driver.execute_cdp_cmd('Page.enable', {})
            
            # Apply extreme stealth scripts
            driver.execute_script("""
                // Remove webdriver traces
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                
                // Mock chrome runtime
                window.chrome = {
                    runtime: {
                        onConnect: undefined,
                        onMessage: undefined,
                        connect: () => undefined
                    }
                };
                
                // Override function toString to hide automation
                const originalToString = Function.prototype.toString;
                Function.prototype.toString = function() {
                    if (this.name.includes('automation') || this.name.includes('webdriver')) {
                        return 'function() { [native code] }';
                    }
                    return originalToString.call(this);
                };
                
                // Mock plugins advanced
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [
                        {name: 'Chrome PDF Plugin', filename: 'internal-pdf-viewer', length: 1},
                        {name: 'Chrome PDF Viewer', filename: 'mhjfbmdgcfjbbpaeojofohoefgiehjai', length: 1},
                        {name: 'Native Client', filename: 'internal-nacl-plugin', length: 1}
                    ]
                });
                
                // Advanced navigator properties
                Object.defineProperty(navigator, 'languages', {get: () => ['id-ID', 'id', 'en-US', 'en']});
                Object.defineProperty(navigator, 'permissions', {get: () => undefined});
                Object.defineProperty(navigator, 'deviceMemory', {get: () => 8});
                Object.defineProperty(navigator, 'platform', {get: () => 'Win32'});
                Object.defineProperty(navigator, 'hardwareConcurrency', {get: () => 8});
                
                // Mock screen
                Object.defineProperty(screen, 'width', {get: () => 1920});
                Object.defineProperty(screen, 'height', {get: () => 1080});
                Object.defineProperty(screen, 'colorDepth', {get: () => 24});
                
                // Hide automation indicators
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_JSON;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Object;
            """)
            
            # === PHASE 2: STEALTH APPROACH ===
            self.log(f"[GHOST {viewer_index}] 🕳️ Approaching target with stealth...")
            
            # Visit blank page first
            driver.get("about:blank")
            time.sleep(3)
            
            # Visit Shopee with stealth
            try:
                driver.get("https://shopee.co.id")
                time.sleep(random.uniform(5, 10))
                
                # Re-apply stealth after page load
                self.apply_post_load_stealth(driver)
                
            except Exception as e:
                self.log(f"[GHOST {viewer_index}] ⚠️ Shopee access issue: {e}")
            
            # === PHASE 3: GHOST COOKIE INJECTION ===
            self.log(f"[GHOST {viewer_index}] 🍪 Injecting ghost cookies...")
            
            # Clear and inject cookies
            driver.delete_all_cookies()
            
            essential_cookies = [
                {'name': 'SPC_F', 'value': cookie_data['spc_f']},
                {'name': 'SPC_U', 'value': cookie_data['spc_u']},
                {'name': 'SPC_ST', 'value': cookie_data['spc_st']},
                {'name': 'SPC_EC', 'value': cookie_data['spc_ec']},
            ]
            
            # Add ghost tracking cookies
            ghost_cookies = [
                {'name': 'REC_T_ID', 'value': str(uuid.uuid4())},
                {'name': 'SPC_R_T_ID', 'value': f"GHOST_{int(time.time())}_{random.randint(10000,99999)}"},
                {'name': 'SPC_T_IV', 'value': str(random.randint(100000,999999))},
            ]
            
            all_cookies = essential_cookies + ghost_cookies
            
            for cookie in all_cookies:
                try:
                    driver.add_cookie({
                        'name': cookie['name'],
                        'value': cookie['value'],
                        'domain': '.shopee.co.id',
                        'path': '/',
                        'secure': False,
                        'httpOnly': False
                    })
                    self.log(f"[GHOST {viewer_index}] 👻 {cookie['name']} injected")
                except Exception as e:
                    self.log(f"[GHOST {viewer_index}] ⚠️ {cookie['name']} failed: {e}")
            
            # === PHASE 4: AUTHENTICATION REFRESH ===
            self.log(f"[GHOST {viewer_index}] 🔄 Refreshing ghost session...")
            
            driver.refresh()
            time.sleep(random.uniform(8, 15))
            
            # Re-apply stealth after refresh
            self.apply_post_load_stealth(driver)
            
            # === PHASE 5: GHOST API EXECUTION ===
            self.log(f"[GHOST {viewer_index}] 📡 Executing ghost API call...")
            
            api_result = driver.execute_script(f"""
                return fetch('https://live.shopee.co.id/api/v1/session/{self.session_id}/joinv2', {{
                    method: 'POST',
                    credentials: 'include',
                    headers: {{
                        'Content-Type': 'application/json',
                        'Accept': 'application/json, text/plain, */*',
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-Shopee-Language': 'id',
                        'X-API-SOURCE': 'pc'
                    }},
                    body: JSON.stringify({{
                        session_id: '{self.session_id}',
                        device_id: '{cookie_data["device_id"]}',
                        client_type: 'web',
                        source: 'live_share'
                    }})
                }}).then(response => {{
                    return {{
                        status: response.status,
                        ok: response.ok,
                        redirected: response.redirected,
                        url: response.url
                    }};
                }}).catch(error => {{
                    return {{
                        error: error.message
                    }};
                }});
            """)
            
            self.log(f"[GHOST {viewer_index}] 👻 API Result: {api_result}")
            
            # === PHASE 6: DIRECT INFILTRATION ===
            live_url = f"https://live.shopee.co.id/share?from=live&session={self.session_id}"
            self.log(f"[GHOST {viewer_index}] 🎯 Direct infiltration: {live_url}")
            
            try:
                driver.get(live_url)
                time.sleep(random.uniform(10, 20))
                
                # Final stealth application
                self.apply_post_load_stealth(driver)
                
            except Exception as e:
                self.log(f"[GHOST {viewer_index}] ⚠️ Infiltration error: {e}")
            
            # === PHASE 7: GHOST VERIFICATION ===
            time.sleep(5)
            
            try:
                current_url = driver.current_url
                page_title = driver.title
                
                self.log(f"[GHOST {viewer_index}] 🔍 Final URL: {current_url}")
                self.log(f"[GHOST {viewer_index}] 📄 Page Title: {page_title}")
                
                # Advanced blocking detection
                blocked_patterns = ['captcha', 'verify', 'anti_bot', 'robot', 'blocked', 'traffic', 'crawler']
                
                # Check URL and title
                url_blocked = any(pattern in current_url.lower() for pattern in blocked_patterns)
                title_blocked = any(pattern in page_title.lower() for pattern in blocked_patterns)
                
                # Check page source for anti-bot patterns
                try:
                    page_source = driver.page_source.lower()
                    source_blocked = any(pattern in page_source for pattern in blocked_patterns[:3])  # Only check main patterns
                except:
                    source_blocked = False
                
                if not url_blocked and not title_blocked and not source_blocked and 'live.shopee.co.id' in current_url:
                    self.log(f"[GHOST {viewer_index}] 👻 GHOST MODE SUCCESS!")
                    
                    # Add to active viewers
                    self.active_viewers.append({
                        'driver': driver,
                        'viewer_id': viewer_index,
                        'type': 'ghost_mode',
                        'status': 'active',
                        'account_id': cookie_data['account_id'],
                        'created_at': datetime.now(),
                        'final_url': current_url,
                        'page_title': page_title,
                        'api_result': api_result
                    })
                    
                    return True
                else:
                    self.log(f"[GHOST {viewer_index}] 🚫 GHOST DETECTION FAILED!")
                    if url_blocked:
                        self.log(f"[GHOST {viewer_index}] - URL blocked: {current_url}")
                    if title_blocked:
                        self.log(f"[GHOST {viewer_index}] - Title blocked: {page_title}")
                    if source_blocked:
                        self.log(f"[GHOST {viewer_index}] - Source blocked")
                    
                    driver.quit()
                    return False
                    
            except Exception as e:
                self.log(f"[GHOST {viewer_index}] ❌ Verification error: {e}")
                driver.quit()
                return False
                
        except Exception as e:
            self.log(f"[GHOST {viewer_index}] 💥 CRITICAL GHOST ERROR: {str(e)[:150]}...")
            if driver:
                try:
                    driver.quit()
                except:
                    pass
            return False
    
    def apply_post_load_stealth(self, driver):
        """Apply stealth scripts after page load"""
        try:
            driver.execute_script("""
                // Advanced post-load stealth
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                window.chrome = {runtime: {}};
                
                // Remove automation traces from window
                ['cdc_adoQpoasnfa76pfcZLmcfl_Array', 'cdc_adoQpoasnfa76pfcZLmcfl_Promise', 
                 'cdc_adoQpoasnfa76pfcZLmcfl_Symbol', '$cdc_asdjflasutopfhvcZLmcfl_'].forEach(prop => {
                    if (window.hasOwnProperty(prop)) {
                        delete window[prop];
                    }
                });
                
                // Mock permission API
                if (navigator.permissions) {
                    navigator.permissions.query = () => Promise.resolve({state: 'granted'});
                }
            """)
        except:
            pass
    
    def start_ghost_mode_bot(self, session_id, target_viewers=3):
        """Start ghost mode bot"""
        self.session_id = session_id
        
        self.log("=" * 60)
        self.log("👻 GHOST MODE SHOPEE BOT")
        self.log("Invisible Infiltration Technology")
        self.log("=" * 60)
        self.log(f"🎯 Session: {session_id}")
        self.log(f"👻 Target: {target_viewers} ghost viewers")
        self.log("=" * 60)
        
        if not self.verified_cookies:
            self.log("❌ No ghost cookies available!")
            return
        
        # Phase 1: Ghost API Test
        self.log("\n👻 PHASE 1: GHOST API INFILTRATION")
        api_success = self.test_pure_api_ghost_method(session_id)
        
        # Phase 2: Ghost Browser Infiltration
        self.log("\n👻 PHASE 2: INVISIBLE BROWSER INFILTRATION")
        
        browser_success = 0
        cookies_to_use = min(target_viewers, len(self.verified_cookies))
        
        for i in range(cookies_to_use):
            self.log(f"\n{'👻'*20} GHOST VIEWER {i+1}/{cookies_to_use} {'👻'*20}")
            
            if self.create_invisible_browser(self.verified_cookies[i], i + 1):
                browser_success += 1
                self.log(f"[GHOST {i+1}] ✅ SUCCESS - Total ghosts: {browser_success}")
            else:
                self.log(f"[GHOST {i+1}] ❌ DETECTED")
            
            # Extended ghost delay
            if i < cookies_to_use - 1:
                delay = random.uniform(20, 45)
                self.log(f"⏳ Ghost delay {delay:.1f}s before next infiltration...")
                time.sleep(delay)
        
        # Final ghost status
        self.log("\n" + "=" * 60)
        self.log("👻 GHOST MODE FINAL STATUS")
        self.log(f"📡 Ghost API Success: {api_success}/{len(self.verified_cookies)}")
        self.log(f"👻 Ghost Browser Success: {browser_success}/{target_viewers}")
        self.log(f"🎯 Active Ghost Viewers: {len(self.active_viewers)}")
        
        if len(self.active_viewers) > 0:
            self.log("\nActive Ghost Army:")
            for viewer in self.active_viewers:
                self.log(f"  👻 Ghost {viewer['viewer_id']}: {viewer['account_id']} - {viewer['status']}")
        
        self.log("=" * 60)
        
        if browser_success > 0:
            self.log("\n💚 Ghost viewers infiltrated successfully! Press Ctrl+C to stop...")
            try:
                while True:
                    time.sleep(60)  # Extended ghost health check
                    self.ghost_health_check()
            except KeyboardInterrupt:
                self.log("\n🛑 Recalling ghost army...")
                self.cleanup_ghosts()
        else:
            self.log("❌ All ghosts detected! Anti-bot system too strong.")
    
    def ghost_health_check(self):
        """Ghost health monitoring"""
        alive_count = 0
        for viewer in self.active_viewers[:]:
            try:
                current_url = viewer['driver'].current_url
                if 'live.shopee.co.id' in current_url and 'captcha' not in current_url:
                    alive_count += 1
                else:
                    self.log(f"👻 Ghost {viewer['viewer_id']} compromised: {current_url}")
                    self.active_viewers.remove(viewer)
                    viewer['driver'].quit()
            except:
                self.active_viewers.remove(viewer)
                self.log(f"👻 Ghost {viewer['viewer_id']} vanished")
        
        self.log(f"💚 Ghost Army Status: {alive_count} ghosts still infiltrated")
    
    def cleanup_ghosts(self):
        """Cleanup ghost resources"""
        self.log("🧹 Dissolving ghost army...")
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
        
        print("👻" + "=" * 60)
        print("           GHOST MODE BOT - Invisible Infiltration")
        print("👻" + "=" * 60)
        
        bot = GhostModeBot()
        bot.start_ghost_mode_bot(session_id, viewer_count)
    else:
        session_id = input("Session ID: ").strip()
        viewer_count = int(input("Jumlah ghost viewers: ").strip())
        
        bot = GhostModeBot()
        bot.start_ghost_mode_bot(session_id, viewer_count)
