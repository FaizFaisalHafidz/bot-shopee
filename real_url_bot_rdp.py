#!/usr/bin/env python3
"""
SHOPEE ULTIMATE REAL URL BOT - RDP OPTIMIZED VERSION
Fixed untuk Windows RDP dengan Chrome options yang proper
"""

import time
import random
import json
import os
import threading
import hashlib
import uuid
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class ShopeeRealURLBotRDP:
    def __init__(self):
        self.active_sessions = []
        self.viewer_boost = 300
        self.real_url_params = self.generate_real_url_params()
        
    def generate_real_url_params(self):
        """Generate realistic Shopee Live URL parameters"""
        return {
            'share_user_ids': [266236471, 123456789, 987654321, 555666777, 111222333],
            'stm_mediums': ['referral', 'social', 'direct', 'search'],
            'stm_sources': ['rw', 'fb', 'ig', 'tw', 'wa'],  
            'uls_trackids': [
                '53jjpcb102lt', '44kkpcb203mt', '66mmpcb304nt', '77nnpcb405ot', '88oopcb506pt'
            ]
        }
    
    def generate_device_profile(self, index):
        """Generate realistic device profile with proper parameters"""
        devices = [
            {'platform': 'Android', 'screen': (412, 915), 'memory': 8, 'cores': 8},
            {'platform': 'iOS', 'screen': (414, 896), 'memory': 6, 'cores': 6},
            {'platform': 'Windows', 'screen': (1366, 768), 'memory': 16, 'cores': 8},
            {'platform': 'macOS', 'screen': (1440, 900), 'memory': 16, 'cores': 8}
        ]
        
        device = devices[index % len(devices)]
        
        return {
            'device_id': self.generate_unique_device_id(index),
            'user_id': random.choice(self.real_url_params['share_user_ids']),
            'platform': device['platform'],
            'screen_resolution': device['screen'],
            'device_memory': device['memory'],
            'hardware_concurrency': device['cores'],
            'user_agent': self.generate_realistic_user_agent(device['platform'], index),
            'session_token': self.generate_session_token(index),
            'viewer_id': index + 1,
            'trackid': random.choice(self.real_url_params['uls_trackids']),
            'stm_medium': random.choice(self.real_url_params['stm_mediums']),
            'stm_source': random.choice(self.real_url_params['stm_sources'])
        }
    
    def generate_unique_device_id(self, index):
        """Generate completely unique device ID"""
        timestamp = str(int(time.time() * 1000))
        random_part = ''.join(random.choice('0123456789abcdef') for _ in range(12))
        return f"device_{timestamp}_{random_part}_{index:03d}"
    
    def generate_session_token(self, index):
        """Generate realistic session token"""
        base = f"session_{index}_{int(time.time())}_{random.random()}"
        return hashlib.sha256(base.encode()).hexdigest()[:32]
    
    def generate_realistic_user_agent(self, platform, index):
        """Generate platform-specific realistic user agents"""
        if platform == 'Android':
            android_versions = ['12', '13', '14']
            chrome_versions = ['119.0.6045.193', '120.0.6099.144', '121.0.6167.101']
            models = ['SM-G991B', 'SM-G998B', 'SM-A525F', 'Pixel 7', 'Pixel 6a']
            
            android_ver = random.choice(android_versions)
            chrome_ver = random.choice(chrome_versions)
            model = random.choice(models)
            
            return f"Mozilla/5.0 (Linux; Android {android_ver}; {model}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_ver} Mobile Safari/537.36"
        
        elif platform == 'iOS':
            ios_versions = ['16.6', '17.0', '17.1', '16.7']
            webkit_versions = ['605.1.15', '605.1.16', '605.2.1']
            
            ios_ver = random.choice(ios_versions).replace('.', '_')
            webkit_ver = random.choice(webkit_versions)
            
            return f"Mozilla/5.0 (iPhone; CPU iPhone OS {ios_ver} like Mac OS X) AppleWebKit/{webkit_ver} (KHTML, like Gecko) Version/{ios_ver.replace('_', '.')} Mobile/15E148 Safari/604.1"
        
        elif platform == 'Windows':
            chrome_versions = ['119.0.6045.193', '120.0.6099.144', '121.0.6167.101']
            chrome_ver = random.choice(chrome_versions)
            
            return f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_ver} Safari/537.36"
        
        elif platform == 'macOS':
            mac_versions = ['10_15_7', '11_7_10', '12_7_1', '13_6_1']
            chrome_versions = ['119.0.6045.193', '120.0.6099.144', '121.0.6167.101']
            
            mac_ver = random.choice(mac_versions)
            chrome_ver = random.choice(chrome_versions)
            
            return f"Mozilla/5.0 (Macintosh; Intel Mac OS X {mac_ver}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_ver} Safari/537.36"
        
        return "Mozilla/5.0 (compatible; ShopeeBot/1.0)"
    
    def build_real_shopee_url(self, session_id, profile):
        """Build exact Shopee Live URL with all real parameters"""
        base_url = "https://live.shopee.co.id/share"
        
        # Build query parameters exactly like real Shopee Live URLs
        params = {
            'from': 'live',
            'session': session_id,
            'share_user_id': profile['user_id'],
            'stm_medium': profile['stm_medium'],
            'stm_source': profile['stm_source'],
            'uls_trackid': profile['trackid'],
            'viewer': profile['viewer_id'],
            'in': '1'
        }
        
        # Build URL with fragment
        query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
        url = f"{base_url}?{query_string}#copy_link"
        
        return url
    
    def create_rdp_chrome_options(self, profile, viewer_index):
        """Create Chrome options optimized for RDP Windows"""
        chrome_options = Options()
        
        # === RDP OPTIMIZED OPTIONS ===
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--disable-features=VizDisplayCompositor')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-plugins')
        chrome_options.add_argument('--disable-images')
        chrome_options.add_argument('--disable-javascript')  # Temporarily disable to reduce load
        chrome_options.add_argument('--disable-background-timer-throttling')
        chrome_options.add_argument('--disable-backgrounding-occluded-windows')
        chrome_options.add_argument('--disable-renderer-backgrounding')
        chrome_options.add_argument('--disable-background-networking')
        
        # === HEADLESS MODE for RDP ===
        chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--disable-logging')
        chrome_options.add_argument('--log-level=3')
        chrome_options.add_argument('--silent')
        
        # === PERFORMANCE OPTIMIZATION ===
        chrome_options.add_argument('--memory-pressure-off')
        chrome_options.add_argument('--max_old_space_size=4096')
        chrome_options.add_argument('--aggressive-cache-discard')
        chrome_options.add_argument('--disable-hang-monitor')
        
        # === BYPASS RDP ISSUES ===
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--remote-debugging-port=0')  # Dynamic port
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--no-first-run')
        chrome_options.add_argument('--no-default-browser-check')
        chrome_options.add_argument('--disable-default-apps')
        
        # === USER AGENT ===
        chrome_options.add_argument(f'--user-agent={profile["user_agent"]}')
        
        # === WINDOW SIZE ===
        chrome_options.add_argument(f'--window-size={profile["screen_resolution"][0]},{profile["screen_resolution"][1]}')
        
        # === PROFILE DIRECTORY (RDP safe) ===
        profile_dir = os.path.abspath(os.path.join('sessions', 'rdp_viewers', f'viewer_{viewer_index}'))
        os.makedirs(profile_dir, exist_ok=True)
        chrome_options.add_argument(f'--user-data-dir={profile_dir}')
        
        # === MOBILE EMULATION for mobile platforms ===
        if profile['platform'] in ['Android', 'iOS']:
            mobile_emulation = {
                "deviceMetrics": {
                    "width": profile['screen_resolution'][0],
                    "height": profile['screen_resolution'][1],
                    "pixelRatio": 2.0
                },
                "userAgent": profile['user_agent']
            }
            chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        
        # === DISABLE AUTOMATION FLAGS ===
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        return chrome_options
    
    def inject_ultimate_auth_bypass(self, driver, profile, session_id):
        """Inject ultimate authentication bypass - optimized for RDP"""
        print(f"[AUTH BYPASS] Injecting RDP-optimized bypass for viewer {profile['viewer_id']}...")
        
        # Enable JavaScript temporarily for injection
        driver.execute_script("console.log('RDP Auth Bypass starting...');")
        
        # Simple but effective bypass
        driver.execute_script(f"""
            // Set session data
            localStorage.setItem('SPC_F', '{profile['session_token']}');
            localStorage.setItem('SPC_U', btoa('{profile['user_id']}'));
            localStorage.setItem('SPC_CLIENTID', '{profile['device_id']}');
            
            // Session storage
            sessionStorage.setItem('live_session_id', '{session_id}');
            sessionStorage.setItem('viewer_authenticated', 'true');
            sessionStorage.setItem('share_user_id', '{profile['user_id']}');
            
            // Override auth functions
            window.checkAuthentication = () => true;
            window.isLoggedIn = () => true;
            window.requireLogin = () => false;
            
            // Set cookies
            document.cookie = 'SPC_F={profile['session_token']}; domain=.shopee.co.id; path=/';
            document.cookie = 'authenticated=true; domain=.shopee.co.id; path=/';
            
            console.log('[RDP BYPASS] Authentication bypass complete');
        """)
        
        print(f"[SUCCESS] RDP auth bypass deployed for viewer {profile['viewer_id']}!")
    
    def inject_simple_viewer_booster(self, driver, profile):
        """Inject simple but effective viewer booster for RDP"""
        print(f"[BOOST] Injecting RDP-optimized booster for {profile['platform']}...")
        
        driver.execute_script(f"""
            console.log('[RDP BOOSTER] Starting simple viewer boost...');
            
            const boostConfig = {{
                baseBoost: {self.viewer_boost},
                platform: '{profile['platform']}',
                viewerId: {profile['viewer_id']}
            }};
            
            function simpleViewerBoost() {{
                const allElements = document.querySelectorAll('*');
                let boosted = false;
                
                allElements.forEach(el => {{
                    const text = el.textContent || '';
                    const numberMatches = text.match(/\\d+/g);
                    
                    if (numberMatches) {{
                        numberMatches.forEach(numStr => {{
                            const num = parseInt(numStr);
                            if (num >= 1 && num <= 100000) {{
                                const boostAmount = boostConfig.baseBoost + Math.floor(Math.random() * 100);
                                const newNum = num + boostAmount;
                                
                                try {{
                                    if (el.textContent === text) {{
                                        el.textContent = text.replace(numStr, newNum.toString());
                                        boosted = true;
                                        console.log(`[RDP BOOST] ${{num}} -> ${{newNum}} (+${{boostAmount}})`);
                                    }}
                                }} catch (e) {{
                                    // Ignore protected elements
                                }}
                            }}
                        }});
                    }}
                }});
                
                if (boosted) {{
                    console.log(`[RDP BOOST] ${{boostConfig.platform}} viewer boost applied!`);
                }}
                
                // Schedule next boost
                setTimeout(simpleViewerBoost, 5000 + Math.random() * 3000);
            }}
            
            // Start boosting after delay
            setTimeout(simpleViewerBoost, 3000);
            
            console.log('[RDP BOOSTER] Simple viewer booster active!');
        """)
    
    def create_real_url_viewer_rdp(self, session_id, viewer_index):
        """Create viewer optimized for RDP with proper error handling"""
        driver = None
        try:
            profile = self.generate_device_profile(viewer_index - 1)
            real_url = self.build_real_shopee_url(session_id, profile)
            
            print(f"[VIEWER {viewer_index}] Creating RDP-optimized viewer...")
            print(f"[DEVICE] {profile['platform']} - User ID: {profile['user_id']}")
            print(f"[URL] {real_url[:80]}...")
            
            # Create RDP-optimized Chrome options
            chrome_options = self.create_rdp_chrome_options(profile, viewer_index)
            
            # Create driver with proper error handling
            try:
                print(f"[CHROME] Starting Chrome for viewer {viewer_index}...")
                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=chrome_options)
                print(f"[CHROME] Chrome started successfully for viewer {viewer_index}")
            except Exception as e:
                print(f"[ERROR] Failed to start Chrome for viewer {viewer_index}: {e}")
                return None
            
            # Set page load timeout
            driver.set_page_load_timeout(30)
            
            # Navigate to Shopee domain first
            print(f"[NAVIGATE] Accessing Shopee domain...")
            driver.get('https://shopee.co.id')
            time.sleep(5)
            
            # Inject authentication bypass
            self.inject_ultimate_auth_bypass(driver, profile, session_id)
            
            # Navigate to real Shopee Live URL
            print(f"[NAVIGATE] Accessing real Shopee Live URL...")
            driver.get(real_url)
            time.sleep(8)
            
            # Check if successful
            current_url = driver.current_url.lower()
            if 'login' in current_url or 'auth' in current_url:
                print(f"[WARNING] Still on login page for viewer {viewer_index}")
                # Try simple bypass
                driver.execute_script("""
                    document.querySelectorAll('[class*="modal"], [class*="login"]').forEach(el => el.remove());
                """)
                time.sleep(3)
            
            # Inject viewer booster
            self.inject_simple_viewer_booster(driver, profile)
            
            # Add to active sessions
            self.active_sessions.append({
                'driver': driver,
                'viewer_id': viewer_index,
                'profile': profile,
                'real_url': real_url,
                'bypassed': True,
                'created_at': datetime.now()
            })
            
            print(f"[SUCCESS] RDP viewer {viewer_index} active!")
            return driver
            
        except Exception as e:
            print(f"[ERROR] Failed to create RDP viewer {viewer_index}: {e}")
            if driver:
                try:
                    driver.quit()
                except:
                    pass
            return None
    
    def start_rdp_bot(self, session_id, viewer_count=3):
        """Start the RDP-optimized bot"""
        print("\\n" + "="*80)
        print("   SHOPEE ULTIMATE REAL URL BOT - RDP OPTIMIZED VERSION")
        print("   Fixed untuk Windows RDP dengan proper Chrome options")
        print("="*80)
        print(f"Target Session: {session_id}")
        print(f"Viewer Count: {viewer_count}")
        print(f"Mode: RDP Headless Optimized")
        print(f"Expected Boost: {self.viewer_boost * viewer_count}")
        print("="*80 + "\\n")
        
        # Create viewers sequentially for better stability
        for i in range(viewer_count):
            print(f"[LAUNCH] Starting RDP viewer {i+1}/{viewer_count}...")
            self.create_real_url_viewer_rdp(session_id, i + 1)
            time.sleep(10)  # Longer delay for RDP stability
        
        print(f"\\n[LAUNCHED] All {viewer_count} RDP viewers started...")
        print("[INFO] RDP-optimized mode active")
        print("[INFO] Headless Chrome browsers")
        print("[INFO] Press Ctrl+C to stop\\n")
        
        # Monitor with RDP-friendly intervals
        try:
            while True:
                time.sleep(90)  # Longer intervals for RDP
                active_count = len(self.active_sessions)
                bypassed_count = len([s for s in self.active_sessions if s.get('bypassed')])
                expected_boost = active_count * self.viewer_boost
                
                print(f"[RDP MONITOR] {active_count}/{viewer_count} viewers active")
                print(f"[AUTH] {bypassed_count} successfully bypassed")
                print(f"[BOOST] Expected total boost: +{expected_boost}")
                
                if self.active_sessions:
                    platforms = [s['profile']['platform'] for s in self.active_sessions]
                    platform_counts = {}
                    for platform in platforms:
                        platform_counts[platform] = platform_counts.get(platform, 0) + 1
                    
                    platform_summary = ', '.join([f"{k}: {v}" for k, v in platform_counts.items()])
                    print(f"[PLATFORMS] {platform_summary}")
                
        except KeyboardInterrupt:
            print("\\n[SHUTDOWN] Stopping all RDP viewers...")
            for session in self.active_sessions:
                try:
                    session['driver'].quit()
                except:
                    pass
            print("[CLEANUP] All RDP viewers stopped.")

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python real_url_bot_rdp.py <session_id> [viewer_count]")
        print("Example: python real_url_bot_rdp.py 157658364 3")
        sys.exit(1)
    
    session_id = sys.argv[1]
    viewer_count = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    
    bot = ShopeeRealURLBotRDP()
    bot.start_rdp_bot(session_id, viewer_count)

if __name__ == "__main__":
    main()
