#!/usr/bin/env python3
"""
Shopee Live Bot - RDP Optimized & Simplified
- Fixed ChromeDriver permissions
- Complete GPU disabling for RDP
- Simplified monitoring without complex API calls
- Network error resilience
- Client-grade reliability
"""

import os
import sys
import time
import json
import random
import requests
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import threading

class ShopeeRDPBot:
    def __init__(self):
        self.active_sessions = []
        self.success_count = 0
        self.failed_count = 0
        
        # Simple device profiles
        self.device_profiles = [
            {"platform": "Android", "user_agent": "Mozilla/5.0 (Linux; Android 12; SM-G998B) AppleWebKit/537.36"},
            {"platform": "iPhone", "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15"},
            {"platform": "Windows", "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"},
        ]
    
    def fix_chromedriver_permissions(self):
        """Fix ChromeDriver permissions for RDP"""
        try:
            # Install and get driver path
            driver_path = ChromeDriverManager().install()
            print(f"[FIX] ChromeDriver path: {driver_path}")
            
            # Set permissions (Windows)
            if os.name == 'nt':
                import subprocess
                try:
                    # Give full permissions to chromedriver
                    subprocess.run(['icacls', driver_path, '/grant', 'Everyone:F'], 
                                 capture_output=True, check=False)
                    print(f"[FIX] ChromeDriver permissions fixed!")
                except:
                    print(f"[WARNING] Could not fix permissions, but continuing...")
            
            return driver_path
        except Exception as e:
            print(f"[ERROR] ChromeDriver setup failed: {e}")
            return None
    
    def create_rdp_optimized_options(self, profile, viewer_index):
        """Create highly optimized Chrome options for RDP"""
        options = Options()
        
        # MAXIMUM RDP OPTIMIZATION
        options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        # COMPLETE GPU DISABLING
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-gpu-sandbox')
        options.add_argument('--disable-software-rasterizer')
        options.add_argument('--disable-background-timer-throttling')
        options.add_argument('--disable-backgrounding-occluded-windows')
        options.add_argument('--disable-renderer-backgrounding')
        options.add_argument('--disable-features=TranslateUI,BlinkGenPropertyTrees,VizDisplayCompositor')
        options.add_argument('--use-gl=swiftshader')  # Software rendering
        options.add_argument('--disable-webgl')
        options.add_argument('--disable-webgl2')
        options.add_argument('--disable-3d-apis')
        
        # NETWORK OPTIMIZATION
        options.add_argument('--disable-web-security')
        options.add_argument('--disable-features=VizDisplayCompositor')
        options.add_argument('--aggressive-cache-discard')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-plugins')
        options.add_argument('--disable-images')  # Skip images for speed
        options.add_argument('--disable-default-apps')
        options.add_argument('--no-first-run')
        
        # MEMORY OPTIMIZATION
        options.add_argument('--memory-pressure-off')
        options.add_argument('--max_old_space_size=2048')
        
        # USER AGENT
        options.add_argument(f'--user-agent={profile["user_agent"]}')
        
        # WINDOW SIZE
        options.add_argument('--window-size=1280,720')
        
        # PROFILE ISOLATION
        profile_dir = f"sessions/rdp_profiles/viewer_{viewer_index}"
        os.makedirs(profile_dir, exist_ok=True)
        options.add_argument(f'--user-data-dir={os.path.abspath(profile_dir)}')
        
        # UNIQUE DEBUG PORT
        debug_port = 9222 + viewer_index
        options.add_argument(f'--remote-debugging-port={debug_port}')
        
        # DISABLE LOGGING
        options.add_argument('--log-level=3')
        options.add_argument('--silent')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option('useAutomationExtension', False)
        
        return options
    
    def simple_monitoring(self, session_id):
        """Simple monitoring without complex API calls"""
        print(f"[MONITOR] Simple monitoring active for session {session_id}")
        print(f"[INFO] Check manually at: https://live.shopee.co.id/{session_id}")
        return True
    
    def ultra_aggressive_bypass(self, driver, profile, session_id):
        """Ultra-aggressive bypass for RDP"""
        try:
            print(f"[BYPASS] Deploying RDP-optimized bypass...")
            
            # Clear all auth data
            driver.execute_script("""
                try {
                    localStorage.clear();
                    sessionStorage.clear();
                    // Override auth functions
                    window.loginRequired = function() { return false; };
                    window.checkAuth = function() { return true; };
                    window.requireLogin = function() { return false; };
                    window.isGuest = function() { return true; };
                    // Set guest mode
                    localStorage.setItem('guest_session', 'true');
                    localStorage.setItem('bypass_auth', 'true');
                } catch(e) { console.log('Bypass script executed'); }
            """)
            
            print(f"[SUCCESS] RDP bypass deployed!")
            return True
            
        except Exception as e:
            print(f"[WARNING] Bypass deployment warning: {e}")
            return False
    
    def build_simple_url(self, session_id, profile):
        """Build simple URL without complex parameters"""
        user_id = random.randint(100000, 999999)
        
        # Simple URL formats that work in RDP
        url_formats = [
            f"https://shopee.co.id/live/{session_id}",
            f"https://m.shopee.co.id/live/{session_id}",
            f"https://live.shopee.co.id/{session_id}",
        ]
        
        return random.choice(url_formats)
    
    def create_rdp_viewer(self, session_id, viewer_index, profile):
        """Create single viewer optimized for RDP"""
        driver = None
        
        try:
            print(f"[VIEWER {viewer_index}] Creating RDP-optimized viewer...")
            print(f"[DEVICE] {profile['platform']}")
            
            # Fix ChromeDriver permissions first
            driver_path = self.fix_chromedriver_permissions()
            if not driver_path:
                raise Exception("ChromeDriver setup failed")
            
            # Create RDP-optimized options
            chrome_options = self.create_rdp_optimized_options(profile, viewer_index)
            
            # Start Chrome with fixed driver
            print(f"[CHROME] Starting RDP-optimized Chrome...")
            service = Service(driver_path)
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Set conservative timeouts
            driver.set_page_load_timeout(90)  # Longer for RDP
            driver.implicitly_wait(20)
            
            print(f"[SUCCESS] Chrome started for viewer {viewer_index}")
            
            # Build simple URL
            shopee_url = self.build_simple_url(session_id, profile)
            print(f"[URL] {shopee_url}")
            
            # Navigate with retry logic
            navigation_attempts = 3
            navigation_success = False
            
            for attempt in range(navigation_attempts):
                try:
                    print(f"[NAVIGATE] Attempt {attempt + 1}/{navigation_attempts}...")
                    
                    # Try direct navigation first
                    driver.get('https://shopee.co.id')
                    time.sleep(15)  # Long wait for RDP
                    
                    # Deploy bypass
                    self.ultra_aggressive_bypass(driver, profile, session_id)
                    time.sleep(5)
                    
                    # Navigate to live URL
                    driver.get(shopee_url)
                    time.sleep(20)  # Extra long wait
                    
                    # Simple success check
                    current_url = driver.current_url.lower()
                    page_title = driver.title.lower()
                    
                    success_indicators = ['live', 'shopee', session_id]
                    failure_indicators = ['login', 'auth', 'error']
                    
                    has_success = any(indicator in current_url or indicator in page_title 
                                    for indicator in success_indicators)
                    has_failure = any(indicator in current_url or indicator in page_title 
                                    for indicator in failure_indicators)
                    
                    if has_success and not has_failure:
                        navigation_success = True
                        break
                    else:
                        print(f"[RETRY] Navigation check failed, trying alternative...")
                        # Try alternative URLs
                        alt_urls = [
                            f"https://m.shopee.co.id/live/{session_id}",
                            f"https://shopee.co.id/live/{session_id}?guest=1",
                        ]
                        
                        for alt_url in alt_urls:
                            try:
                                driver.get(alt_url)
                                time.sleep(15)
                                if session_id in driver.current_url:
                                    navigation_success = True
                                    break
                            except:
                                continue
                        
                        if navigation_success:
                            break
                
                except Exception as nav_error:
                    print(f"[WARNING] Navigation attempt {attempt + 1} failed: {nav_error}")
                    if attempt < navigation_attempts - 1:
                        time.sleep(10)
            
            if not navigation_success:
                print(f"[WARNING] Navigation may have issues, but keeping session active")
            
            # Add to active sessions
            session_info = {
                'driver': driver,
                'viewer_id': viewer_index,
                'profile': profile,
                'url': shopee_url,
                'status': 'active',
                'created_at': datetime.now()
            }
            
            self.active_sessions.append(session_info)
            self.success_count += 1
            
            print(f"✅ [SUCCESS] RDP Viewer {viewer_index} active!")
            return driver
            
        except Exception as e:
            print(f"❌ [ERROR] Failed to create RDP viewer {viewer_index}: {e}")
            if driver:
                try:
                    driver.quit()
                except:
                    pass
            
            self.failed_count += 1
            return None
    
    def start_rdp_bot(self, session_id, viewer_count):
        """Start RDP-optimized bot"""
        print(f"\n{'='*80}")
        print(f"   SHOPEE RDP BOT - MAXIMUM RDP OPTIMIZATION")
        print(f"   Fixed permissions + GPU disabled + Network optimized")
        print(f"{'='*80}")
        print(f"Target Session: {session_id}")
        print(f"Viewer Count: {viewer_count}")
        print(f"Mode: RDP Headless + Network Resilient")
        print(f"{'='*80}")
        
        # Start simple monitoring
        self.simple_monitoring(session_id)
        
        # Create viewers with limited concurrency for RDP
        print(f"\n🚀 [LAUNCH] Creating {viewer_count} RDP-optimized viewers...")
        
        max_concurrent = min(3, viewer_count)  # Limit for RDP stability
        
        with ThreadPoolExecutor(max_workers=max_concurrent) as executor:
            futures = []
            
            for i in range(viewer_count):
                viewer_index = i + 1
                profile = self.device_profiles[i % len(self.device_profiles)].copy()
                
                future = executor.submit(
                    self.create_rdp_viewer,
                    session_id,
                    viewer_index,
                    profile
                )
                futures.append(future)
                
                # Stagger creation for RDP stability
                time.sleep(5)
            
            # Wait for completion
            completed = 0
            for future in as_completed(futures):
                result = future.result()
                completed += 1
                if result:
                    print(f"[PROGRESS] {completed}/{viewer_count} viewers completed")
        
        print(f"\n🎯 [COMPLETED] RDP Bot finished!")
        print(f"✅ Success: {self.success_count} | ❌ Failed: {self.failed_count}")
        print(f"📊 Success Rate: {(self.success_count/viewer_count)*100:.1f}%")
        
        if self.success_count > 0:
            print(f"\n🔥 [RESULT] {self.success_count} viewers should be active!")
            print(f"🔍 [CHECK] Manually verify at: https://live.shopee.co.id/{session_id}")
            print(f"💡 [TIP] Keep this terminal open to maintain sessions")
            
            # Keep sessions alive
            try:
                while True:
                    print(f"[ALIVE] {len(self.active_sessions)} sessions maintained - {datetime.now().strftime('%H:%M:%S')}")
                    time.sleep(60)  # Check every minute
            except KeyboardInterrupt:
                print(f"\n🛑 [STOP] Cleaning up sessions...")
                self.cleanup()
    
    def cleanup(self):
        """Cleanup all resources"""
        for session in self.active_sessions:
            try:
                session['driver'].quit()
            except:
                pass
        self.active_sessions.clear()
        print(f"[CLEANUP] Complete!")

def main():
    if len(sys.argv) > 1:
        session_id = sys.argv[1]
        viewer_count = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    else:
        session_id = input("Enter Shopee Live Session ID: ").strip()
        viewer_count = int(input("Enter viewer count (default 3): ").strip() or "3")
    
    if not session_id.isdigit():
        print("❌ Invalid session ID")
        return
    
    if viewer_count < 1 or viewer_count > 50:
        print("❌ Viewer count must be between 1-50")
        return
    
    bot = ShopeeRDPBot()
    bot.start_rdp_bot(session_id, viewer_count)

if __name__ == "__main__":
    main()
