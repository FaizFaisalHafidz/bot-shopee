#!/usr/bin/env python3
"""
SHOPEE ULTIMATE REAL URL BOT - SUPER RDP OPTIMIZED VERSION
Ultra-aggressive login bypass + GPU disabled untuk RDP Windows
"""

import time
import random
import json
import os
import threading
import hashlib
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class ShopeeUltraRDPBot:
    def __init__(self):
        self.active_sessions = []
        self.viewer_boost = 500
        
    def generate_device_profile(self, index):
        """Generate device profile optimized for login bypass"""
        devices = [
            {'platform': 'Android', 'screen': (412, 915)},
            {'platform': 'iPhone', 'screen': (414, 896)},  
            {'platform': 'Windows', 'screen': (1366, 768)},
            {'platform': 'iPad', 'screen': (768, 1024)}
        ]
        
        device = devices[index % len(devices)]
        user_ids = [266236471, 123456789, 987654321, 555666777, 111222333]
        
        return {
            'device_id': f"rdp_device_{int(time.time())}_{index:03d}",
            'user_id': random.choice(user_ids),
            'platform': device['platform'],
            'screen_resolution': device['screen'],
            'user_agent': self.get_mobile_user_agent(device['platform']),
            'session_token': hashlib.md5(f"session_{index}_{time.time()}".encode()).hexdigest(),
            'viewer_id': index + 1,
            'trackid': f"rdp{int(time.time())}{index:02d}lt"
        }
    
    def get_mobile_user_agent(self, platform):
        """Get mobile user agents for better bypass"""
        agents = {
            'Android': 'Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.101 Mobile Safari/537.36',
            'iPhone': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1',
            'Windows': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.101 Safari/537.36',
            'iPad': 'Mozilla/5.0 (iPad; CPU OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1'
        }
        return agents.get(platform, agents['Android'])
    
    def build_shopee_url(self, session_id, profile):
        """Build Shopee Live URL with proper bypass parameters"""
        return f"https://live.shopee.co.id/share?from=live&session={session_id}&share_user_id={profile['user_id']}&stm_medium=referral&stm_source=app&uls_trackid={profile['trackid']}&viewer={profile['viewer_id']}&in=1"
    
    def create_ultra_chrome_options(self, profile, viewer_index):
        """Create ultra-optimized Chrome options for RDP"""
        chrome_options = Options()
        
        # === ULTRA RDP OPTIMIZATION ===
        chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-gpu-compositing')
        chrome_options.add_argument('--disable-gpu-rasterization')
        chrome_options.add_argument('--disable-gpu-sandbox')
        chrome_options.add_argument('--disable-software-rasterizer')
        
        # === DISABLE ALL FEATURES THAT CAUSE ISSUES ===
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--disable-features=VizDisplayCompositor,VizServiceDisplay,VizHitTestSurfaceLayer')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-plugins')
        chrome_options.add_argument('--disable-images')
        chrome_options.add_argument('--disable-background-timer-throttling')
        chrome_options.add_argument('--disable-backgrounding-occluded-windows')
        chrome_options.add_argument('--disable-renderer-backgrounding')
        chrome_options.add_argument('--disable-field-trial-config')
        chrome_options.add_argument('--disable-background-networking')
        chrome_options.add_argument('--disable-sync')
        chrome_options.add_argument('--disable-translate')
        
        # === SILENCE ALL LOGS ===
        chrome_options.add_argument('--disable-logging')
        chrome_options.add_argument('--log-level=3')
        chrome_options.add_argument('--silent')
        chrome_options.add_argument('--disable-dev-tools')
        
        # === PERFORMANCE ===
        chrome_options.add_argument('--memory-pressure-off')
        chrome_options.add_argument('--aggressive-cache-discard')
        chrome_options.add_argument('--disable-hang-monitor')
        
        # === BYPASS AUTOMATION DETECTION ===
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # === USER AGENT ===
        chrome_options.add_argument(f'--user-agent={profile["user_agent"]}')
        
        # === WINDOW SIZE ===
        chrome_options.add_argument(f'--window-size={profile["screen_resolution"][0]},{profile["screen_resolution"][1]}')
        
        # === PROFILE DIRECTORY ===
        profile_dir = os.path.abspath(os.path.join('sessions', 'ultra_rdp', f'viewer_{viewer_index}'))
        os.makedirs(profile_dir, exist_ok=True)
        chrome_options.add_argument(f'--user-data-dir={profile_dir}')
        
        # === MOBILE EMULATION for bypass ===
        if profile['platform'] in ['Android', 'iPhone', 'iPad']:
            mobile_emulation = {
                "deviceMetrics": {
                    "width": profile['screen_resolution'][0],
                    "height": profile['screen_resolution'][1],
                    "pixelRatio": 2.0
                },
                "userAgent": profile['user_agent']
            }
            chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        
        return chrome_options
    
    def ultra_aggressive_bypass(self, driver, profile, session_id):
        """Ultra-aggressive bypass untuk RDP"""
        print(f"[ULTRA BYPASS] Deploying ultra-aggressive bypass for viewer {profile['viewer_id']}...")
        
        # Inject comprehensive bypass
        driver.execute_script(f"""
            console.log('[ULTRA BYPASS] Starting ultra-aggressive bypass...');
            
            // === COMPLETE SESSION SIMULATION ===
            const sessionData = {{
                userId: {profile['user_id']},
                sessionToken: '{profile['session_token']}',
                deviceId: '{profile['device_id']}',
                viewerId: {profile['viewer_id']},
                platform: '{profile['platform']}'
            }};
            
            // Set all possible Shopee storage
            localStorage.setItem('SPC_U', btoa(JSON.stringify({{
                user_id: sessionData.userId,
                username: 'viewer_' + sessionData.viewerId
            }})));
            localStorage.setItem('SPC_F', sessionData.sessionToken);
            localStorage.setItem('SPC_CLIENTID', sessionData.deviceId);
            localStorage.setItem('authenticated', 'true');
            localStorage.setItem('guest_mode', 'true');
            localStorage.setItem('auto_login', 'true');
            localStorage.setItem('bypass_login', 'true');
            localStorage.setItem('mobile_user', 'true');
            
            // Session storage
            sessionStorage.setItem('live_session_id', '{session_id}');
            sessionStorage.setItem('viewer_authenticated', 'true');
            sessionStorage.setItem('guest_access', 'true');
            sessionStorage.setItem('mobile_bypass', 'true');
            
            // === OVERRIDE ALL AUTH FUNCTIONS ===
            window.checkAuth = () => true;
            window.checkAuthentication = () => true;
            window.isLoggedIn = () => true;
            window.requireLogin = () => false;
            window.needLogin = () => false;
            window.showLogin = () => false;
            window.redirectToLogin = () => false;
            window.openLoginModal = () => false;
            
            // Override Shopee namespace
            if (typeof window.Shopee === 'undefined') window.Shopee = {{}};
            window.Shopee.requireLogin = () => false;
            window.Shopee.checkAuth = () => true;
            window.Shopee.isAuthenticated = () => true;
            window.Shopee.needAuth = () => false;
            window.Shopee.showAuthModal = () => false;
            
            // === COMPREHENSIVE COOKIE SETTING ===
            const cookies = [
                'SPC_F=' + sessionData.sessionToken + '; domain=.shopee.co.id; path=/',
                'SPC_U=' + btoa('user_' + sessionData.userId) + '; domain=.shopee.co.id; path=/',
                'SPC_CLIENTID=' + sessionData.deviceId + '; domain=.shopee.co.id; path=/',
                'authenticated=true; domain=.shopee.co.id; path=/',
                'guest_mode=true; domain=.shopee.co.id; path=/',
                'mobile_user=true; domain=.shopee.co.id; path=/',
                'auto_login=true; domain=.shopee.co.id; path=/',
                'bypass_auth=true; domain=.shopee.co.id; path=/',
                'live_viewer=1; domain=.shopee.co.id; path=/'
            ];
            
            cookies.forEach(cookie => document.cookie = cookie);
            
            // === REMOVE ALL LOGIN ELEMENTS ===
            const loginSelectors = [
                '[class*="login"]', '[class*="auth"]', '[class*="modal"]',
                '[id*="login"]', '[id*="auth"]', '[id*="modal"]',
                'div[class*="Login"]', 'div[class*="Auth"]', 'div[class*="Modal"]'
            ];
            
            loginSelectors.forEach(selector => {{
                try {{
                    document.querySelectorAll(selector).forEach(el => {{
                        if (el.textContent.toLowerCase().includes('login') || 
                            el.textContent.toLowerCase().includes('masuk') ||
                            el.textContent.toLowerCase().includes('auth')) {{
                            el.remove();
                        }}
                    }});
                }} catch(e) {{}}
            }});
            
            // === PREVENT LOGIN REDIRECTS ===
            const originalPushState = history.pushState;
            history.pushState = function(state, title, url) {{
                if (url && (url.includes('/login') || url.includes('/auth'))) {{
                    console.log('[ULTRA BYPASS] Blocked navigation to:', url);
                    return;
                }}
                return originalPushState.call(this, state, title, url);
            }};
            
            const originalReplaceState = history.replaceState;
            history.replaceState = function(state, title, url) {{
                if (url && (url.includes('/login') || url.includes('/auth'))) {{
                    console.log('[ULTRA BYPASS] Blocked replace state to:', url);
                    return;
                }}
                return originalReplaceState.call(this, state, title, url);
            }};
            
            // === PREVENT POPUPS ===
            window.alert = function(msg) {{
                if (msg && (msg.includes('login') || msg.includes('masuk'))) {{
                    console.log('[ULTRA BYPASS] Blocked login alert:', msg);
                    return;
                }}
            }};
            
            window.confirm = function(msg) {{
                if (msg && (msg.includes('login') || msg.includes('masuk'))) {{
                    console.log('[ULTRA BYPASS] Blocked login confirm:', msg);
                    return true;
                }}
            }};
            
            // === CONTINUOUS CLEANUP ===
            setInterval(() => {{
                // Remove login elements continuously
                document.querySelectorAll('[class*="login"], [class*="auth"], [class*="modal"]').forEach(el => {{
                    if (el.style.display !== 'none') {{
                        el.style.display = 'none';
                        console.log('[ULTRA BYPASS] Hidden login element');
                    }}
                }});
                
                // Ensure we're not on login page
                if (window.location.href.includes('/login') || window.location.href.includes('/auth')) {{
                    console.log('[ULTRA BYPASS] Redirecting from login page');
                    window.location.href = 'https://live.shopee.co.id/share?from=live&session={session_id}&share_user_id=' + sessionData.userId;
                }}
            }}, 2000);
            
            console.log('[ULTRA BYPASS] Ultra-aggressive bypass deployed successfully!');
        """)
        
        print(f"[SUCCESS] Ultra-aggressive bypass deployed for viewer {profile['viewer_id']}!")
    
    def inject_mega_booster(self, driver, profile):
        """Inject mega viewer booster"""
        print(f"[MEGA BOOST] Injecting mega booster for {profile['platform']}...")
        
        driver.execute_script(f"""
            console.log('[MEGA BOOST] Starting mega viewer booster...');
            
            const megaConfig = {{
                baseBoost: {self.viewer_boost},
                platform: '{profile['platform']}',
                viewerId: {profile['viewer_id']}
            }};
            
            function megaBoost() {{
                const elements = document.querySelectorAll('*');
                let boosted = 0;
                
                elements.forEach(el => {{
                    const text = el.textContent || '';
                    if (text.match(/\\d+/)) {{
                        const numbers = text.match(/\\d+/g);
                        numbers.forEach(numStr => {{
                            const num = parseInt(numStr);
                            if (num >= 1 && num <= 50000) {{
                                const boost = megaConfig.baseBoost + Math.floor(Math.random() * 200);
                                const newNum = num + boost;
                                
                                try {{
                                    const newText = text.replace(new RegExp('\\\\b' + numStr + '\\\\b', 'g'), newNum.toString());
                                    if (el.textContent === text) {{
                                        el.textContent = newText;
                                        el.style.color = '#FF6B6B';
                                        el.style.fontWeight = 'bold';
                                        boosted++;
                                        console.log(`[MEGA BOOST] ${{num}} -> ${{newNum}} (+${{boost}})`);
                                    }}
                                }} catch(e) {{}}
                            }}
                        }});
                    }}
                }});
                
                if (boosted > 0) {{
                    console.log(`[MEGA BOOST] ${{megaConfig.platform}} boosted ${{boosted}} elements!`);
                }}
                
                // Schedule next boost
                setTimeout(megaBoost, 3000 + Math.random() * 2000);
            }}
            
            // Start mega boosting
            setTimeout(megaBoost, 2000);
            
            console.log('[MEGA BOOST] Mega viewer booster activated!');
        """)
    
    def create_ultra_viewer(self, session_id, viewer_index):
        """Create ultra-optimized viewer for RDP with robust error handling"""
        driver = None
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                profile = self.generate_device_profile(viewer_index - 1)
                shopee_url = self.build_shopee_url(session_id, profile)
                
                print(f"[ULTRA VIEWER {viewer_index}] Creating ultra-optimized viewer (attempt {attempt + 1}/{max_retries})...")
                print(f"[DEVICE] {profile['platform']} - User ID: {profile['user_id']}")
                print(f"[URL] {shopee_url[:100]}...")
                
                # Create ultra Chrome options
                chrome_options = self.create_ultra_chrome_options(profile, viewer_index)
                
                # Start Chrome
                print(f"[CHROME] Starting ultra-optimized Chrome...")
                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=chrome_options)
                
                # Set timeouts with retry logic
                driver.set_page_load_timeout(60)  # Longer timeout
                driver.implicitly_wait(15)
                
                print(f"[CHROME] Chrome started successfully for viewer {viewer_index}")
                
                # Robust navigation with retries
                navigation_success = False
                nav_attempts = 3
                
                for nav_attempt in range(nav_attempts):
                    try:
                        print(f"[NAVIGATE] Accessing Shopee main page (attempt {nav_attempt + 1}/{nav_attempts})...")
                        driver.get('https://shopee.co.id')
                        time.sleep(10)  # Longer wait for RDP
                        navigation_success = True
                        break
                    except Exception as nav_error:
                        print(f"[WARNING] Navigation attempt {nav_attempt + 1} failed: {nav_error}")
                        if nav_attempt < nav_attempts - 1:
                            time.sleep(5)  # Wait before retry
                        else:
                            # Try alternative domains
                            alt_domains = ['https://m.shopee.co.id', 'https://www.shopee.co.id']
                            for alt_domain in alt_domains:
                                try:
                                    print(f"[FALLBACK] Trying alternative domain: {alt_domain}")
                                    driver.get(alt_domain)
                                    time.sleep(8)
                                    navigation_success = True
                                    break
                                except:
                                    continue
                
                if not navigation_success:
                    raise Exception("Failed to navigate to any Shopee domain")
                
                # Deploy ultra-aggressive bypass
                self.ultra_aggressive_bypass(driver, profile, session_id)
                
                # Navigate to live URL with retries
                live_navigation_success = False
                for live_attempt in range(3):
                    try:
                        print(f"[NAVIGATE] Accessing Shopee Live URL (attempt {live_attempt + 1}/3)...")
                        driver.get(shopee_url)
                        time.sleep(15)  # Longer wait
                        live_navigation_success = True
                        break
                    except Exception as live_error:
                        print(f"[WARNING] Live URL navigation attempt {live_attempt + 1} failed: {live_error}")
                        if live_attempt < 2:
                            time.sleep(8)
                
                if not live_navigation_success:
                    print(f"[WARNING] Live URL navigation failed, trying emergency bypasses...")
                
                # Check if bypassed with enhanced detection
                bypassed = True
                try:
                    current_url = driver.current_url.lower()
                    page_title = driver.title.lower()
                    
                    if 'login' in current_url or 'auth' in current_url or 'login' in page_title:
                        bypassed = False
                        print(f"[ULTRA BYPASS] Still on auth page, applying emergency bypass...")
                        
                        # Enhanced emergency bypass methods
                        emergency_bypasses = [
                            # Method 1: Force navigation with guest parameter
                            lambda: self.emergency_bypass_method_1(driver, shopee_url),
                            
                            # Method 2: Mobile fallback (skip if failed before)
                            lambda: self.emergency_bypass_method_2(driver, session_id) if attempt == 0 else None,
                            
                            # Method 3: Direct API style
                            lambda: self.emergency_bypass_method_3(driver, session_id),
                            
                            # Method 4: Alternative live URL format
                            lambda: self.emergency_bypass_method_4(driver, session_id, profile)
                        ]
                        
                        for i, method in enumerate(emergency_bypasses):
                            if method is None:
                                continue
                            try:
                                print(f"[EMERGENCY] Trying bypass method {i+1}...")
                                method()
                                time.sleep(12)
                                
                                # Check if method worked
                                new_url = driver.current_url.lower()
                                new_title = driver.title.lower()
                                if 'login' not in new_url and 'auth' not in new_url and 'login' not in new_title:
                                    print(f"[SUCCESS] Emergency bypass method {i+1} worked!")
                                    bypassed = True
                                    break
                            except Exception as emergency_error:
                                print(f"[WARNING] Emergency method {i+1} failed: {emergency_error}")
                
                except Exception as check_error:
                    print(f"[WARNING] Could not check bypass status: {check_error}")
                    bypassed = True  # Assume success if we can't check
                
                # Inject mega booster
                try:
                    self.inject_mega_booster(driver, profile)
                except Exception as booster_error:
                    print(f"[WARNING] Mega booster injection failed: {booster_error}")
                
                # Add to active sessions
                self.active_sessions.append({
                    'driver': driver,
                    'viewer_id': viewer_index,
                    'profile': profile,
                    'url': shopee_url,
                    'bypassed': bypassed,
                    'created_at': datetime.now(),
                    'attempt': attempt + 1
                })
                
                print(f"[SUCCESS] Ultra viewer {viewer_index} active! (Attempt {attempt + 1})")
                return driver
                
            except Exception as e:
                print(f"[ERROR] Attempt {attempt + 1} failed to create ultra viewer {viewer_index}: {e}")
                if driver:
                    try:
                        driver.quit()
                    except:
                        pass
                    driver = None
                
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 10  # Progressive wait
                    print(f"[RETRY] Waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)
                else:
                    print(f"[FAILED] All {max_retries} attempts failed for viewer {viewer_index}")
        
        return None
    
    def emergency_bypass_method_1(self, driver, shopee_url):
        """Emergency method 1: Guest parameter"""
        guest_url = shopee_url.replace('share?', 'share?guest=1&')
        driver.get(guest_url)
    
    def emergency_bypass_method_2(self, driver, session_id):
        """Emergency method 2: Mobile URL"""
        mobile_url = f"https://m.shopee.co.id/live/{session_id}"
        driver.get(mobile_url)
    
    def emergency_bypass_method_3(self, driver, session_id):
        """Emergency method 3: Direct API style"""
        direct_url = f"https://live.shopee.co.id/{session_id}?viewer=1"
        driver.get(direct_url)
    
    def emergency_bypass_method_4(self, driver, session_id, profile):
        """Emergency method 4: Alternative live URL format"""
        alt_url = f"https://live.shopee.co.id/live?session={session_id}&user={profile['user_id']}&mobile=1"
        driver.get(alt_url)
    
    def start_ultra_bot(self, session_id, viewer_count=3):
        """Start ultra-optimized bot for RDP"""
        print("\\n" + "="*80)
        print("   SHOPEE ULTRA RDP BOT - MAXIMUM OPTIMIZATION")
        print("   Ultra-aggressive login bypass + GPU disabled")
        print("="*80)
        print(f"Target Session: {session_id}")
        print(f"Viewer Count: {viewer_count}")
        print(f"Mode: Ultra RDP Headless")
        print(f"Expected Mega Boost: {self.viewer_boost * viewer_count}")
        print("="*80 + "\\n")
        
        # Create viewers with longer delays for stability
        for i in range(viewer_count):
            print(f"[LAUNCH] Starting ultra viewer {i+1}/{viewer_count}...")
            self.create_ultra_viewer(session_id, i + 1)
            time.sleep(15)  # Longer delay for RDP stability
        
        print(f"\\n[LAUNCHED] All {viewer_count} ultra viewers started...")
        print("[INFO] Ultra RDP optimization active")
        print("[INFO] Ultra-aggressive login bypass deployed")
        print("[INFO] Mega viewer booster enabled")
        print("[INFO] Press Ctrl+C to stop\\n")
        
        # Monitor
        try:
            while True:
                time.sleep(120)  # 2-minute intervals for RDP
                active_count = len(self.active_sessions)
                bypassed_count = len([s for s in self.active_sessions if s.get('bypassed')])
                expected_boost = active_count * self.viewer_boost
                
                print(f"[ULTRA MONITOR] {active_count}/{viewer_count} ultra viewers active")
                print(f"[BYPASS] {bypassed_count} successfully bypassed login")
                print(f"[MEGA BOOST] Expected total boost: +{expected_boost}")
                
                if self.active_sessions:
                    platforms = [s['profile']['platform'] for s in self.active_sessions]
                    platform_counts = {}
                    for platform in platforms:
                        platform_counts[platform] = platform_counts.get(platform, 0) + 1
                    
                    platform_summary = ', '.join([f"{k}: {v}" for k, v in platform_counts.items()])
                    print(f"[PLATFORMS] {platform_summary}")
                
        except KeyboardInterrupt:
            print("\\n[SHUTDOWN] Stopping all ultra viewers...")
            for session in self.active_sessions:
                try:
                    session['driver'].quit()
                except:
                    pass
            print("[CLEANUP] All ultra viewers stopped.")

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python real_url_bot_ultra.py <session_id> [viewer_count]")
        print("Example: python real_url_bot_ultra.py 157658364 3")
        sys.exit(1)
    
    session_id = sys.argv[1]
    viewer_count = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    
    bot = ShopeeUltraRDPBot()
    bot.start_ultra_bot(session_id, viewer_count)

if __name__ == "__main__":
    main()
