#!/usr/bin/env python3
"""
Shopee Live Cookie Harvester + API Bot
- Harvest real session cookies via browser automation
- Use harvested cookies for API calls
- Scale up to 100 viewers with cookie rotation
"""

import os
import sys
import time
import json
import random
import requests
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import threading
import uuid

class ShopeeCookieHarvester:
    def __init__(self):
        self.harvested_cookies = []
        self.active_sessions = []
        self.success_count = 0
        self.failed_count = 0
        
        # Device profiles for cookie diversity
        self.device_profiles = [
            {"platform": "Android", "user_agent": "Mozilla/5.0 (Linux; Android 12; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36"},
            {"platform": "iPhone", "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"},
            {"platform": "Windows", "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"},
            {"platform": "Mac", "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"},
            {"platform": "iPad", "user_agent": "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"},
        ]
    
    def create_cookie_harvester_options(self, profile, harvester_index):
        """Create Chrome options optimized for cookie harvesting"""
        options = Options()
        
        # RDP Optimization
        options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-gpu-sandbox')
        options.add_argument('--disable-software-rasterizer')
        
        # Cookie optimization
        options.add_argument('--enable-features=NetworkService')
        options.add_argument('--disable-web-security')
        options.add_argument('--disable-features=VizDisplayCompositor')
        
        # User agent
        options.add_argument(f'--user-agent={profile["user_agent"]}')
        
        # Unique profile for each harvester
        profile_dir = f"sessions/cookie_harvesters/harvester_{harvester_index}"
        os.makedirs(profile_dir, exist_ok=True)
        options.add_argument(f'--user-data-dir={os.path.abspath(profile_dir)}')
        
        # Unique debug port
        debug_port = 9300 + harvester_index
        options.add_argument(f'--remote-debugging-port={debug_port}')
        
        return options
    
    def generate_device_fingerprint(self, profile):
        """Generate realistic device fingerprint"""
        device_ids = [
            f"{uuid.uuid4()}",
            f"f9c8fc8a-1ff5-422b-a403-{random.randint(100000000000, 999999999999)}",
            f"{random.randint(10000000, 99999999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(100000000000, 999999999999)}"
        ]
        
        return {
            'device_id': random.choice(device_ids),
            'client_id': f"{''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=16))}",
            'user_id': random.randint(100000000, 999999999),
            'platform': profile['platform']
        }
    
    def harvest_session_cookies(self, session_id, harvester_index, profile):
        """Harvest real session cookies from Shopee"""
        driver = None
        try:
            fingerprint = self.generate_device_fingerprint(profile)
            
            print(f"[HARVESTER {harvester_index}] Starting cookie harvesting...")
            print(f"[DEVICE] {profile['platform']} - User: {fingerprint['user_id']}")
            
            # Create Chrome options
            chrome_options = self.create_cookie_harvester_options(profile, harvester_index)
            
            # Start Chrome
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Set timeouts
            driver.set_page_load_timeout(90)
            driver.implicitly_wait(20)
            
            print(f"[CHROME] Cookie harvester started for harvester {harvester_index}")
            
            # Navigate to Shopee main page first
            print(f"[NAVIGATE] Accessing Shopee main page...")
            driver.get('https://shopee.co.id')
            time.sleep(15)
            
            # Inject device fingerprint
            driver.execute_script(f"""
                localStorage.setItem('device_id', '{fingerprint["device_id"]}');
                localStorage.setItem('client_id', '{fingerprint["client_id"]}');
                sessionStorage.setItem('user_fingerprint', JSON.stringify({json.dumps(fingerprint)}));
            """)
            
            # Navigate to live session
            live_url = f"https://live.shopee.co.id/share?from=live&session={session_id}&share_user_id={fingerprint['user_id']}&stm_medium=referral&stm_source=rw&uls_trackid={random.randint(1000000000000, 9999999999999)}&viewer={random.randint(1, 99)}"
            
            print(f"[NAVIGATE] Accessing live session...")
            driver.get(live_url)
            time.sleep(20)
            
            # Wait for cookies to be set
            print(f"[COOKIES] Waiting for session cookies to be generated...")
            time.sleep(30)  # Wait for all cookies to be set
            
            # Harvest cookies
            cookies = driver.get_cookies()
            cookie_dict = {}
            
            # Extract important cookies
            important_cookies = [
                'SPC_U', 'SPC_ST', 'SPC_T_ID', 'SPC_T_IV', 'SPC_EC', 
                'SPC_SI', 'SPC_R_T_ID', 'SPC_R_T_IV', 'SPC_CLIENTID',
                'SPC_F', 'shopee_webUnique_ccd', 'ds'
            ]
            
            for cookie in cookies:
                if cookie['name'] in important_cookies:
                    cookie_dict[cookie['name']] = cookie['value']
            
            # Get additional headers from network
            user_agent = driver.execute_script("return navigator.userAgent;")
            
            # Build complete session info
            session_info = {
                'cookies': cookie_dict,
                'headers': {
                    'User-Agent': user_agent,
                    'Accept': 'application/json, text/plain, */*',
                    'Accept-Language': 'id,en-US;q=0.9,en;q=0.8',
                    'Content-Type': 'application/json',
                    'Origin': 'https://live.shopee.co.id',
                    'Referer': live_url,
                    'X-Livestreaming-Source': 'shopee',
                    'Sec-CH-UA': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
                    'Sec-CH-UA-Mobile': '?0' if profile['platform'] in ['Windows', 'Mac'] else '?1',
                    'Sec-CH-UA-Platform': f'"{profile["platform"]}"',
                    'Sec-Fetch-Dest': 'empty',
                    'Sec-Fetch-Mode': 'cors',
                    'Sec-Fetch-Site': 'same-origin'
                },
                'device_info': fingerprint,
                'harvested_at': datetime.now(),
                'expires_at': datetime.now() + timedelta(hours=2),  # Assume 2 hour expiry
                'harvester_id': harvester_index,
                'session_id': session_id
            }
            
            # Validate cookies
            if len(cookie_dict) >= 3:  # At least 3 important cookies
                self.harvested_cookies.append(session_info)
                print(f"✅ [SUCCESS] Harvester {harvester_index} - {len(cookie_dict)} cookies harvested!")
                self.success_count += 1
                return session_info
            else:
                print(f"⚠️  [PARTIAL] Harvester {harvester_index} - Only {len(cookie_dict)} cookies harvested")
                return None
                
        except Exception as e:
            print(f"❌ [ERROR] Harvester {harvester_index} failed: {e}")
            self.failed_count += 1
            return None
            
        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass
    
    def api_join_with_cookies(self, session_id, cookie_session, viewer_index):
        """Use harvested cookies to make API join call"""
        try:
            api_url = f"https://live.shopee.co.id/api/v1/session/{session_id}/joinv2"
            
            # Prepare headers with harvested data
            headers = cookie_session['headers'].copy()
            
            # Add cookies to headers
            cookie_string = '; '.join([f"{k}={v}" for k, v in cookie_session['cookies'].items()])
            headers['Cookie'] = cookie_string
            
            # Generate realistic payload
            payload = {
                "uuid": str(uuid.uuid4()),
                "ver": 1,
                "device_id": cookie_session['device_info']['device_id'],
                "timestamp": int(time.time() * 1000)
            }
            
            print(f"[API {viewer_index}] Making join request with harvested cookies...")
            
            # Make API call
            response = requests.post(api_url, json=payload, headers=headers, timeout=30)
            
            print(f"[API {viewer_index}] Response Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if data.get('err_code') == 0:
                    print(f"✅ [SUCCESS] API join {viewer_index} successful!")
                    return True
                else:
                    print(f"⚠️  [WARNING] API join {viewer_index} returned error: {data.get('err_msg')}")
                    return False
            else:
                print(f"❌ [FAILED] API join {viewer_index} - HTTP {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ [ERROR] API join {viewer_index} failed: {e}")
            return False
    
    def start_hybrid_bot(self, session_id, target_viewers):
        """Start hybrid cookie harvesting + API bot"""
        print(f"\n{'='*80}")
        print(f"   SHOPEE HYBRID COOKIE + API BOT")
        print(f"   Cookie Harvesting → API Calls → Real viewer boost")
        print(f"{'='*80}")
        print(f"Target Session: {session_id}")
        print(f"Target Viewers: {target_viewers}")
        print(f"Method: Hybrid (Cookie Harvesting + API)")
        print(f"{'='*80}")
        
        # Phase 1: Cookie Harvesting
        print(f"\n🍪 [PHASE 1] Cookie Harvesting - Creating {min(10, target_viewers)} harvesters...")
        
        harvesters_needed = min(10, target_viewers)  # Max 10 concurrent harvesters
        
        with ThreadPoolExecutor(max_workers=5) as executor:  # Limit for stability
            harvest_futures = []
            
            for i in range(harvesters_needed):
                harvester_index = i + 1
                profile = self.device_profiles[i % len(self.device_profiles)].copy()
                
                future = executor.submit(
                    self.harvest_session_cookies,
                    session_id,
                    harvester_index,
                    profile
                )
                harvest_futures.append(future)
                
                # Stagger for stability
                time.sleep(3)
            
            # Collect results
            completed = 0
            for future in as_completed(harvest_futures):
                result = future.result()
                completed += 1
                print(f"[HARVEST] {completed}/{harvesters_needed} harvesters completed")
        
        print(f"\n📊 [HARVEST RESULTS] {len(self.harvested_cookies)} valid cookie sessions harvested")
        
        if len(self.harvested_cookies) == 0:
            print(f"❌ [FAILED] No cookies harvested - cannot proceed with API calls")
            return
        
        # Phase 2: API Calls with Cookie Rotation
        print(f"\n🚀 [PHASE 2] API Calls - Using harvested cookies for {target_viewers} joins...")
        
        api_success = 0
        api_failed = 0
        
        for viewer_index in range(1, target_viewers + 1):
            # Rotate cookies (reuse if needed)
            cookie_session = self.harvested_cookies[(viewer_index - 1) % len(self.harvested_cookies)]
            
            # Check if cookies are still valid (not expired)
            if datetime.now() > cookie_session['expires_at']:
                print(f"⚠️  [WARNING] Cookies for viewer {viewer_index} may be expired")
            
            success = self.api_join_with_cookies(session_id, cookie_session, viewer_index)
            
            if success:
                api_success += 1
            else:
                api_failed += 1
            
            # Rate limiting
            time.sleep(random.uniform(2, 5))
        
        # Results
        print(f"\n🎯 [COMPLETED] Hybrid Cookie + API Bot finished!")
        print(f"🍪 Cookie Harvest: {len(self.harvested_cookies)} sessions")
        print(f"🚀 API Success: {api_success}")
        print(f"❌ API Failed: {api_failed}")
        print(f"📊 Success Rate: {(api_success/target_viewers)*100:.1f}%")
        
        if api_success > 0:
            print(f"\n🔥 [RESULT] {api_success} viewers joined via API!")
            print(f"🔍 [VERIFY] Check viewer count at: https://live.shopee.co.id/{session_id}")
        
    def cleanup(self):
        """Cleanup resources"""
        self.harvested_cookies.clear()
        print(f"[CLEANUP] Complete!")

def main():
    if len(sys.argv) > 1:
        session_id = sys.argv[1]
        target_viewers = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    else:
        session_id = input("Enter Shopee Live Session ID: ").strip()
        target_viewers = int(input("Enter target viewer count (1-100): ").strip() or "10")
    
    if not session_id.isdigit():
        print("❌ Invalid session ID")
        return
    
    if target_viewers < 1 or target_viewers > 100:
        print("❌ Target viewers must be between 1-100")
        return
    
    bot = ShopeeCookieHarvester()
    bot.start_hybrid_bot(session_id, target_viewers)

if __name__ == "__main__":
    main()
