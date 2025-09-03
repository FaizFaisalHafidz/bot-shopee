#!/usr/bin/env python3
"""
QUICK FIX BOT - Emergency Simple Version
Untuk testing cepat join Shopee Live
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

class QuickFixBot:
    def __init__(self):
        self.active_viewers = []
        self.session_id = None
        self.verified_cookies = []
        
        # Setup logging
        log_dir = os.path.join('bot-core', 'logs')
        os.makedirs(log_dir, exist_ok=True)
        self.log_file = os.path.join(log_dir, f'quick_fix_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
        
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
            
            self.log(f"✅ Loaded {len(self.verified_cookies)} cookies")
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
    
    def test_api_direct(self, session_id):
        """Test direct API join tanpa browser"""
        self.log("🧪 TESTING DIRECT API JOIN...")
        
        for i, cookie_data in enumerate(self.verified_cookies):
            self.log(f"\n--- API TEST {i+1}/{len(self.verified_cookies)} ---")
            self.log(f"Account: {cookie_data['account_id']}")
            
            try:
                join_url = f"https://live.shopee.co.id/api/v1/session/{session_id}/joinv2"
                
                cookies = {
                    'SPC_F': cookie_data['spc_f'],
                    'SPC_U': cookie_data['spc_u'],
                    'SPC_ST': cookie_data['spc_st'],
                    'SPC_EC': cookie_data['spc_ec']
                }
                
                headers = {
                    'User-Agent': cookie_data['user_agent'],
                    'Referer': f'https://live.shopee.co.id/share?from=live&session={session_id}',
                    'Content-Type': 'application/json'
                }
                
                response = requests.post(join_url, cookies=cookies, headers=headers, timeout=10)
                
                self.log(f"Status: {response.status_code}")
                self.log(f"Response: {response.text[:200]}...")
                
                if response.status_code == 200:
                    self.log("✅ API JOIN SUCCESS!")
                else:
                    self.log(f"❌ API FAILED: {response.status_code}")
                    
            except Exception as e:
                self.log(f"❌ API ERROR: {e}")
            
            time.sleep(2)
    
    def create_simple_browser(self, cookie_data, viewer_index):
        """Create simple browser viewer - minimal options"""
        driver = None
        try:
            self.log(f"[BROWSER {viewer_index}] 🚀 Starting simple browser...")
            
            # Minimal Chrome options
            chrome_options = Options()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--log-level=3')
            chrome_options.add_argument(f'--user-agent={cookie_data["user_agent"]}')
            
            # Simple profile
            profile_dir = os.path.abspath(os.path.join('bot-core', 'sessions', 'viewers', f'simple_{viewer_index}'))
            os.makedirs(profile_dir, exist_ok=True)
            chrome_options.add_argument(f'--user-data-dir={profile_dir}')
            
            # Create driver
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.set_page_load_timeout(20)
            
            # Go to Shopee
            self.log(f"[BROWSER {viewer_index}] 🛒 Going to Shopee...")
            driver.get("https://shopee.co.id")
            time.sleep(3)
            
            # Add cookies
            for name, value in [
                ('SPC_F', cookie_data['spc_f']),
                ('SPC_U', cookie_data['spc_u']),
                ('SPC_ST', cookie_data['spc_st']),
                ('SPC_EC', cookie_data['spc_ec'])
            ]:
                try:
                    driver.add_cookie({
                        'name': name,
                        'value': value,
                        'domain': '.shopee.co.id',
                        'path': '/'
                    })
                    self.log(f"[BROWSER {viewer_index}] ✅ Added {name}")
                except Exception as e:
                    self.log(f"[BROWSER {viewer_index}] ❌ Failed {name}: {e}")
            
            # Refresh
            driver.refresh()
            time.sleep(3)
            
            # Go to live
            live_url = f"https://live.shopee.co.id/share?from=live&session={self.session_id}"
            self.log(f"[BROWSER {viewer_index}] 📺 Going to live...")
            driver.get(live_url)
            time.sleep(5)
            
            # Check result
            current_url = driver.current_url
            self.log(f"[BROWSER {viewer_index}] Final URL: {current_url}")
            
            if 'live.shopee.co.id' in current_url and 'login' not in current_url:
                self.log(f"[BROWSER {viewer_index}] ✅ SUCCESS!")
                
                self.active_viewers.append({
                    'driver': driver,
                    'viewer_id': viewer_index,
                    'account_id': cookie_data['account_id'],
                    'status': 'active'
                })
                return True
            else:
                self.log(f"[BROWSER {viewer_index}] ❌ FAILED")
                driver.quit()
                return False
                
        except Exception as e:
            self.log(f"[BROWSER {viewer_index}] 💥 ERROR: {e}")
            if driver:
                try:
                    driver.quit()
                except:
                    pass
            return False
    
    def start_quick_test(self, session_id, test_type="both"):
        """Start quick test"""
        self.session_id = session_id
        
        self.log("=" * 60)
        self.log("🚀 QUICK FIX BOT - Emergency Mode")
        self.log("=" * 60)
        self.log(f"🎯 Session: {session_id}")
        self.log(f"🧪 Test Type: {test_type}")
        self.log("=" * 60)
        
        if not self.verified_cookies:
            self.log("❌ No cookies available!")
            return
        
        results = {"api_success": 0, "browser_success": 0}
        
        # Test 1: Direct API
        if test_type in ["api", "both"]:
            self.log("\n🧪 === API DIRECT TEST ===")
            self.test_api_direct(session_id)
        
        # Test 2: Browser method
        if test_type in ["browser", "both"]:
            self.log("\n🌐 === BROWSER TEST ===")
            
            for i, cookie_data in enumerate(self.verified_cookies[:3]):  # Max 3 browsers
                self.log(f"\n--- BROWSER {i+1}/3 ---")
                if self.create_simple_browser(cookie_data, i + 1):
                    results["browser_success"] += 1
                
                time.sleep(5)  # Delay between browsers
        
        # Final results
        self.log("\n" + "=" * 60)
        self.log("🎯 QUICK TEST RESULTS")
        self.log(f"🌐 Browser Success: {results['browser_success']}")
        self.log(f"📱 Active Browsers: {len(self.active_viewers)}")
        self.log("=" * 60)
        
        if len(self.active_viewers) > 0:
            self.log("\n💚 Some viewers active! Press Ctrl+C to stop...")
            try:
                while True:
                    time.sleep(30)
                    alive = 0
                    for viewer in self.active_viewers[:]:
                        try:
                            viewer['driver'].current_url
                            alive += 1
                        except:
                            self.active_viewers.remove(viewer)
                    self.log(f"💚 Health: {alive} browsers alive")
            except KeyboardInterrupt:
                self.log("\n🛑 Stopping...")
                for viewer in self.active_viewers:
                    try:
                        viewer['driver'].quit()
                    except:
                        pass
        else:
            self.log("❌ No active viewers!")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) >= 2:
        session_id = sys.argv[1]
        test_type = sys.argv[2] if len(sys.argv) >= 3 else "both"
        
        print("🚀" + "=" * 60)
        print("           QUICK FIX BOT - Emergency Mode")
        print("🚀" + "=" * 60)
        
        bot = QuickFixBot()
        bot.start_quick_test(session_id, test_type)
    else:
        session_id = input("Session ID: ").strip()
        print("Test type: [1] API only, [2] Browser only, [3] Both")
        choice = input("Choice (1-3): ").strip()
        
        test_types = {"1": "api", "2": "browser", "3": "both"}
        test_type = test_types.get(choice, "both")
        
        bot = QuickFixBot()
        bot.start_quick_test(session_id, test_type)
