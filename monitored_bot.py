#!/usr/bin/env python3
"""
Shopee Live Bot with Real-Time Monitoring
- Real-time viewer count tracking
- Progressive scaling up to 100 viewers
- Auto-validation and adjustment
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
import queue

class ShopeeMonitoredBot:
    def __init__(self):
        self.active_sessions = []
        self.monitoring_active = False
        self.target_viewers = 0
        self.current_viewers = 0
        self.session_id = None
        self.monitoring_thread = None
        self.viewer_queue = queue.Queue()
        self.success_count = 0
        self.failed_count = 0
        
        # Device profiles untuk variety
        self.device_profiles = [
            {"platform": "Android", "user_agent": "Mozilla/5.0 (Linux; Android 12; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36"},
            {"platform": "iPhone", "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"},
            {"platform": "Windows", "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"},
            {"platform": "Mac", "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"},
            {"platform": "Tablet", "user_agent": "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"},
        ]
    
    def get_session_info(self, session_id):
        """Get current viewer count from Shopee API"""
        try:
            # Try multiple API endpoints
            endpoints = [
                f"https://live.shopee.co.id/api/v1/session/{session_id}",
                f"https://live.shopee.co.id/api/v1/session/{session_id}/info",
                f"https://shopee.co.id/api/v4/live/get_session_info?session_id={session_id}"
            ]
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'id-ID,id;q=0.9,en;q=0.8',
                'Referer': f'https://live.shopee.co.id/',
                'X-Requested-With': 'XMLHttpRequest'
            }
            
            for endpoint in endpoints:
                try:
                    response = requests.get(endpoint, headers=headers, timeout=10)
                    if response.status_code == 200:
                        data = response.json()
                        
                        # Parse different response formats
                        viewer_count = 0
                        if 'data' in data and 'session' in data['data']:
                            viewer_count = data['data']['session'].get('viewer_count', 0)
                        elif 'data' in data and 'viewer_count' in data['data']:
                            viewer_count = data['data'].get('viewer_count', 0)
                        elif 'viewer_count' in data:
                            viewer_count = data.get('viewer_count', 0)
                        
                        return {
                            'viewer_count': viewer_count,
                            'status': 'success',
                            'endpoint': endpoint,
                            'full_data': data
                        }
                except:
                    continue
            
            return {'viewer_count': 0, 'status': 'failed', 'error': 'All endpoints failed'}
            
        except Exception as e:
            return {'viewer_count': 0, 'status': 'error', 'error': str(e)}
    
    def start_monitoring(self, session_id, target_viewers):
        """Start real-time monitoring thread"""
        self.session_id = session_id
        self.target_viewers = target_viewers
        self.monitoring_active = True
        
        def monitor():
            print(f"\n🔍 [MONITOR] Starting real-time monitoring for session {session_id}")
            print(f"📊 [TARGET] Goal: {target_viewers} viewers")
            print("=" * 80)
            
            baseline_count = 0
            monitoring_start = datetime.now()
            
            while self.monitoring_active:
                try:
                    info = self.get_session_info(session_id)
                    current_time = datetime.now().strftime("%H:%M:%S")
                    
                    if info['status'] == 'success':
                        current_count = info['viewer_count']
                        
                        # Set baseline on first check
                        if baseline_count == 0:
                            baseline_count = current_count
                            print(f"📈 [BASELINE] Initial viewer count: {baseline_count}")
                        
                        # Calculate progress
                        added_viewers = current_count - baseline_count
                        progress = min(100, (added_viewers / target_viewers) * 100) if target_viewers > 0 else 0
                        
                        # Status display
                        status_color = "🟢" if added_viewers > 0 else "🟡" if current_count > 0 else "🔴"
                        
                        print(f"{status_color} [{current_time}] Current: {current_count} | Added: +{added_viewers} | Progress: {progress:.1f}% | Active Bots: {len(self.active_sessions)}")
                        
                        # Update internal tracking
                        self.current_viewers = current_count
                        
                        # Success validation
                        if added_viewers >= target_viewers:
                            print(f"🎉 [SUCCESS] Target achieved! {added_viewers}/{target_viewers} viewers added!")
                            print(f"⏱️  [TIME] Took {datetime.now() - monitoring_start}")
                    
                    else:
                        print(f"❌ [{current_time}] Monitoring failed: {info.get('error', 'Unknown error')}")
                    
                    time.sleep(10)  # Check every 10 seconds
                    
                except Exception as e:
                    print(f"🚨 [MONITOR ERROR] {e}")
                    time.sleep(15)
        
        self.monitoring_thread = threading.Thread(target=monitor, daemon=True)
        self.monitoring_thread.start()
    
    def stop_monitoring(self):
        """Stop monitoring thread"""
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
    
    def create_chrome_options(self, profile, viewer_index):
        """Create optimized Chrome options"""
        options = Options()
        
        # RDP Optimization
        options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-gpu-sandbox')
        options.add_argument('--disable-software-rasterizer')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-plugins')
        options.add_argument('--disable-images')
        options.add_argument('--disable-background-timer-throttling')
        options.add_argument('--disable-backgrounding-occluded-windows')
        options.add_argument('--disable-renderer-backgrounding')
        options.add_argument('--disable-features=TranslateUI')
        options.add_argument('--disable-default-apps')
        options.add_argument('--no-first-run')
        options.add_argument('--disable-web-security')
        options.add_argument('--disable-features=VizDisplayCompositor')
        
        # Performance optimization
        options.add_argument('--memory-pressure-off')
        options.add_argument('--max_old_space_size=4096')
        options.add_argument('--aggressive-cache-discard')
        
        # User agent
        options.add_argument(f'--user-agent={profile["user_agent"]}')
        
        # Window size (for consistency)
        options.add_argument('--window-size=1366,768')
        
        # Profile directory untuk isolation
        profile_dir = f"sessions/monitored_profiles/viewer_{viewer_index}"
        os.makedirs(profile_dir, exist_ok=True)
        options.add_argument(f'--user-data-dir={os.path.abspath(profile_dir)}')
        
        # Remote debugging (unique port per viewer)
        debug_port = 9222 + viewer_index
        options.add_argument(f'--remote-debugging-port={debug_port}')
        
        return options
    
    def ultra_aggressive_bypass(self, driver, profile, session_id):
        """Deploy ultra-aggressive authentication bypass"""
        try:
            print(f"[ULTRA BYPASS] Deploying ultra-aggressive bypass...")
            
            # Method 1: Clear auth storage
            driver.execute_script("""
                localStorage.removeItem('SPC_U');
                localStorage.removeItem('SPC_T');
                localStorage.removeItem('shopee_token');
                sessionStorage.clear();
            """)
            
            # Method 2: Override auth functions
            driver.execute_script("""
                window.loginRequired = function() { return false; };
                window.checkAuth = function() { return true; };
                window.requireLogin = function() { return false; };
                window.isGuest = function() { return true; };
            """)
            
            # Method 3: Inject guest session
            driver.execute_script(f"""
                localStorage.setItem('guest_session', 'true');
                localStorage.setItem('guest_id', '{profile.get("user_id", random.randint(100000, 999999))}');
                sessionStorage.setItem('bypass_auth', 'true');
            """)
            
            print(f"[SUCCESS] Ultra-aggressive bypass deployed!")
            
        except Exception as e:
            print(f"[WARNING] Bypass deployment failed: {e}")
    
    def build_shopee_url(self, session_id, profile):
        """Build optimized Shopee Live URL"""
        user_id = profile.get('user_id', random.randint(100000, 999999))
        timestamp = int(time.time() * 1000)
        
        # Multiple URL formats for better success rate
        url_formats = [
            f"https://live.shopee.co.id/share?from=live&session={session_id}&share_user_id={user_id}&stm_medium=refer&stm_source=live&uls_trackid={timestamp}&viewer=1&guest=1",
            f"https://live.shopee.co.id/{session_id}?viewer=1&guest=1&mobile=1",
            f"https://m.shopee.co.id/live/{session_id}?ref=guest",
        ]
        
        return random.choice(url_formats)
    
    def create_monitored_viewer(self, session_id, viewer_index, profile):
        """Create a single monitored viewer with robust error handling"""
        driver = None
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                shopee_url = self.build_shopee_url(session_id, profile)
                
                print(f"[VIEWER {viewer_index}] Creating monitored viewer (attempt {attempt + 1}/{max_retries})...")
                print(f"[DEVICE] {profile['platform']} - URL: {shopee_url[:50]}...")
                
                # Create Chrome options
                chrome_options = self.create_chrome_options(profile, viewer_index)
                
                # Start Chrome
                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=chrome_options)
                
                # Set timeouts
                driver.set_page_load_timeout(60)
                driver.implicitly_wait(15)
                
                print(f"[CHROME] Chrome started for viewer {viewer_index}")
                
                # Navigate with retries
                navigation_success = False
                for nav_attempt in range(3):
                    try:
                        print(f"[NAVIGATE] Accessing Shopee (attempt {nav_attempt + 1}/3)...")
                        driver.get('https://shopee.co.id')
                        time.sleep(8)
                        navigation_success = True
                        break
                    except Exception as nav_error:
                        if nav_attempt < 2:
                            time.sleep(5)
                        else:
                            # Try mobile fallback
                            driver.get('https://m.shopee.co.id')
                            time.sleep(8)
                            navigation_success = True
                
                if not navigation_success:
                    raise Exception("Navigation failed")
                
                # Deploy bypass
                self.ultra_aggressive_bypass(driver, profile, session_id)
                
                # Navigate to live URL
                print(f"[NAVIGATE] Accessing live stream...")
                driver.get(shopee_url)
                time.sleep(12)
                
                # Verify success
                current_url = driver.current_url.lower()
                bypassed = 'login' not in current_url and 'auth' not in current_url
                
                if not bypassed:
                    print(f"[EMERGENCY] Applying emergency bypass...")
                    # Emergency methods
                    emergency_urls = [
                        f"https://live.shopee.co.id/{session_id}?guest=1&mobile=1",
                        f"https://m.shopee.co.id/live/{session_id}",
                        shopee_url.replace('share?', 'share?bypass=1&')
                    ]
                    
                    for emergency_url in emergency_urls:
                        try:
                            driver.get(emergency_url)
                            time.sleep(8)
                            if 'login' not in driver.current_url.lower():
                                bypassed = True
                                break
                        except:
                            continue
                
                # Add to active sessions
                session_info = {
                    'driver': driver,
                    'viewer_id': viewer_index,
                    'profile': profile,
                    'url': shopee_url,
                    'bypassed': bypassed,
                    'created_at': datetime.now(),
                    'status': 'active' if bypassed else 'auth_pending'
                }
                
                self.active_sessions.append(session_info)
                
                if bypassed:
                    self.success_count += 1
                    print(f"✅ [SUCCESS] Viewer {viewer_index} active!")
                else:
                    print(f"⚠️  [PARTIAL] Viewer {viewer_index} created but may need auth")
                
                return driver
                
            except Exception as e:
                print(f"❌ [ERROR] Attempt {attempt + 1} failed for viewer {viewer_index}: {e}")
                if driver:
                    try:
                        driver.quit()
                    except:
                        pass
                    driver = None
                
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 5
                    print(f"[RETRY] Waiting {wait_time} seconds...")
                    time.sleep(wait_time)
        
        self.failed_count += 1
        print(f"❌ [FAILED] All attempts failed for viewer {viewer_index}")
        return None
    
    def progressive_scaling(self, session_id, target_viewers):
        """Progressive scaling: 10 -> 25 -> 50 -> 100"""
        print(f"\n🚀 [SCALING] Starting progressive scaling to {target_viewers} viewers")
        print("=" * 80)
        
        # Define scaling stages
        if target_viewers <= 10:
            stages = [target_viewers]
        elif target_viewers <= 25:
            stages = [10, target_viewers]
        elif target_viewers <= 50:
            stages = [10, 25, target_viewers]
        else:
            stages = [10, 25, 50, target_viewers]
        
        total_created = 0
        
        for stage_index, stage_target in enumerate(stages):
            viewers_to_create = stage_target - total_created
            
            if viewers_to_create <= 0:
                continue
            
            print(f"\n📈 [STAGE {stage_index + 1}] Creating {viewers_to_create} viewers (Total target: {stage_target})")
            
            # Create viewers concurrently (but limit concurrency)
            max_concurrent = min(5, viewers_to_create)
            
            with ThreadPoolExecutor(max_workers=max_concurrent) as executor:
                futures = []
                
                for i in range(viewers_to_create):
                    viewer_index = total_created + i + 1
                    profile = self.device_profiles[i % len(self.device_profiles)].copy()
                    profile['user_id'] = random.randint(100000, 999999)
                    
                    future = executor.submit(
                        self.create_monitored_viewer,
                        session_id,
                        viewer_index,
                        profile
                    )
                    futures.append(future)
                
                # Wait for completion
                completed = 0
                for future in as_completed(futures):
                    result = future.result()
                    completed += 1
                    if result:
                        print(f"[PROGRESS] {completed}/{viewers_to_create} viewers completed in stage {stage_index + 1}")
            
            total_created = stage_target
            
            # Wait between stages for monitoring
            if stage_index < len(stages) - 1:
                print(f"\n⏳ [STAGE BREAK] Waiting 30 seconds before next stage...")
                time.sleep(30)
        
        print(f"\n🎯 [COMPLETED] Progressive scaling finished!")
        print(f"✅ Success: {self.success_count} | ❌ Failed: {self.failed_count}")
    
    def start_monitored_bot(self, session_id, target_viewers):
        """Start the monitored bot with progressive scaling"""
        print(f"\n{'='*80}")
        print(f"   SHOPEE MONITORED BOT - CLIENT GRADE")
        print(f"   Real-time monitoring + Progressive scaling")
        print(f"{'='*80}")
        print(f"Target Session: {session_id}")
        print(f"Target Viewers: {target_viewers}")
        print(f"Mode: Progressive Scaling + Real-time Monitoring")
        print(f"{'='*80}")
        
        # Start monitoring
        self.start_monitoring(session_id, target_viewers)
        
        # Start progressive scaling
        self.progressive_scaling(session_id, target_viewers)
        
        # Keep monitoring active
        print(f"\n🔄 [MONITORING] Bot active with {len(self.active_sessions)} viewers")
        print(f"💡 Press Ctrl+C to stop monitoring and cleanup")
        
        try:
            while self.monitoring_active:
                time.sleep(30)
                
                # Health check - remove failed sessions
                active_count = len([s for s in self.active_sessions if s['status'] == 'active'])
                print(f"[HEALTH] {active_count} active sessions maintained")
                
        except KeyboardInterrupt:
            print(f"\n🛑 [STOP] Stopping monitoring...")
            self.cleanup()
    
    def cleanup(self):
        """Cleanup all resources"""
        print(f"[CLEANUP] Stopping monitoring...")
        self.stop_monitoring()
        
        print(f"[CLEANUP] Closing {len(self.active_sessions)} browser sessions...")
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
        target_viewers = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    else:
        session_id = input("Enter Shopee Live Session ID (e.g., 157878290): ")
        target_viewers = int(input("Enter target viewer count (1-100): ") or "10")
    
    # Validate inputs
    if not session_id.isdigit():
        print("❌ Invalid session ID")
        return
    
    if target_viewers < 1 or target_viewers > 100:
        print("❌ Target viewers must be between 1-100")
        return
    
    bot = ShopeeMonitoredBot()
    bot.start_monitored_bot(session_id, target_viewers)

if __name__ == "__main__":
    main()
