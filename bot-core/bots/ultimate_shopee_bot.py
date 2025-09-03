#!/usr/bin/env python3
"""
NEO - BOT VIEWS SHOPEE
Cookie Authentication + API Join Implementation
"""

import time
import random
import json
import os
import threading
import requests
import csv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class NeoShopeeBot:
    def __init__(self):
        self.session_cookies = []
        self.active_viewers = []
        self.session_id = None
        self.target_viewers = 10
        self.verified_cookies = []
        
        # Setup logging
        log_dir = os.path.join('bot-core', 'logs')
        os.makedirs(log_dir, exist_ok=True)
        self.log_file = os.path.join(log_dir, f'neo_bot_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
        
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
            
            self.log(f"✅ Loaded {len(self.verified_cookies)} verified cookies")
        except Exception as e:
            self.log(f"❌ Error loading cookies: {e}")
    
    def get_random_cookies(self):
        """Get random verified cookies"""
        if not self.verified_cookies:
            self.log("❌ No verified cookies available!")
            return None
            
        return random.choice(self.verified_cookies)
        
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
    
    def create_chrome_options(self, profile_index):
        """Create Chrome options untuk RDP"""
        chrome_options = Options()
        
        # RDP Optimized
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--disable-features=VizDisplayCompositor')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-plugins')
        
        # Performance
        chrome_options.add_argument('--disable-logging')
        chrome_options.add_argument('--log-level=3')
        chrome_options.add_argument('--silent')
        chrome_options.add_argument('--memory-pressure-off')
        
        # User agent
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
        ]
        chrome_options.add_argument(f'--user-agent={random.choice(user_agents)}')
        
        # Profile directory
        profile_dir = os.path.abspath(os.path.join('bot-core', 'sessions', 'viewers', f'viewer_{profile_index}'))
        os.makedirs(profile_dir, exist_ok=True)
        chrome_options.add_argument(f'--user-data-dir={profile_dir}')
        
        return chrome_options
    
    def create_session_cookies(self, count=3):
        """Create session cookies using verified cookies"""
        self.log(f"🔥 CREATE SESSION COOKIES - Target: {count}")
        
        if not self.verified_cookies:
            self.log("❌ No verified cookies available!")
            return False
        
        cookies_to_create = min(count, len(self.verified_cookies))
        
        for i in range(cookies_to_create):
            verified_cookie = self.verified_cookies[i]
            
            # Create session cookie from verified cookie
            session_cookie = {
                'cookies': {
                    'SPC_F': verified_cookie['spc_f'],
                    'SPC_U': verified_cookie['spc_u'],
                    'SPC_ST': verified_cookie['spc_st'],
                    'SPC_EC': verified_cookie['spc_ec']
                },
                'user_agent': verified_cookie['user_agent'],
                'device_id': verified_cookie['device_id'],
                'account_id': verified_cookie['account_id'],
                'created_at': datetime.now(),
                'is_valid': True
            }
            
            self.session_cookies.append(session_cookie)
            self.log(f"✅ Cookie {verified_cookie['account_id']} ready")
        
        self.log(f"✅ SESSION COOKIES READY - {len(self.session_cookies)}/{count}")
        return len(self.session_cookies) > 0
    
    def api_join(self, cookie_data, viewer_index):
        """Join via API dengan headers lengkap"""
        try:
            self.log(f"[API {viewer_index}] Join via API...")
            
            # Generate device fingerprint
            device_id = cookie_data.get('device_id', f"{random.randint(10000000, 99999999):08x}-{random.randint(1000, 9999):04x}-{random.randint(1000, 9999):04x}-{random.randint(1000, 9999):04x}-{random.randint(100000000000, 999999999999):012x}")
            
            headers = {
                'authority': 'live.shopee.co.id',
                'accept': 'application/json, text/plain, */*',
                'accept-encoding': 'gzip, deflate, br, zstd',
                'accept-language': 'en-US,en;q=0.9',
                'af-ac-enc-dat': f"{random.randint(100000000000000, 999999999999999):015x}",
                'af-ac-enc-sz-token': f"{random.choice(['4ajkrCY0SKLRm9EuH+1uRw==', 'uk4Hbgg71cRKXlHTWB4YbQ==', 'UuTCi16ItZXkHqEOMNTK8g=='])}|{random.choice(['3hbtI5BMdrA5g9vMmeo+sizjKGKL0aeLIM/C5/CSOM6KHT9WE8zR3SlBrTEo+OCQj3f8TdVVQWjYsdiM7xs=', '7lNAw8wYb8dgorY0uJwaecHjfHRyhAZrAiBiOi/7DjPUuzryCvTejlEN/7m0BG0FssEHR6pu3aRssuWKIv8=', 'mXSHUtsfEVEdanhXxWpfsN4LQADLt7BSXbjYmdBS926l6fefcC/UW2JW05IgL4C0G4KjOtlU2gJ/M1/ZsNI='])}|{random.choice(['AUt44MAmsawsEhs/', 'BSpU08C6165oARr2', 'c+xuAErhQ+2oZkoC'])}|08|3",
                'client-info': f'os=2;platform=9;scene_id=17;language=id;device_id={device_id}',
                'content-length': '55',
                'content-type': 'application/json',
                'origin': 'https://live.shopee.co.id',
                'priority': 'u=1, i',
                'referer': f'https://live.shopee.co.id/share?from=live&session={self.session_id}&share_user_id=266236471&stm_medium=referral&stm_source=rw&uls_trackid=53jtgs0g03oc&viewer={viewer_index}&in=1',
                'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': cookie_data['user_agent'],
                'x-livestreaming-auth': f"ls_web_v1_30001_{int(time.time())}_{''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=32))}|{random.choice(['c2pRbToV3Ry13OOOIqDwugcOQsYykzv5Pspf320HPj0=', '/HO6U/zDsLabxbzJGnhi3N28eDlllfhjqDT1Q/YwbdU=', 'pRD+tYLmzTxCfFE0a7j26kUl/Gnchvi/p0CDLE34kYE='])}",
                'x-livestreaming-source': 'shopee',
                'x-sap-ri': f"{random.randint(10**15, 9*10**15):016x}{random.randint(10**15, 9*10**15):016x}{random.randint(10**7, 9*10**7):08x}",
                'x-sz-sdk-version': '1.10.7'
            }
            
            payload = {"source": "web"}
            
            response = requests.post(
                f'https://live.shopee.co.id/api/v1/session/{self.session_id}/joinv2',
                headers=headers,
                cookies=cookie_data['cookies'],
                json=payload,
                timeout=20
            )
            
            if response.status_code == 200:
                self.log(f"[API {viewer_index}] ✅ Berhasil join!")
                return True
            else:
                self.log(f"[API {viewer_index}] ❌ Gagal: {response.status_code}")
                if response.text:
                    self.log(f"[API {viewer_index}] Response: {response.text[:200]}")
                return False
                
        except Exception as e:
            self.log(f"[API {viewer_index}] ❌ Error: {e}")
            return False
    
    def create_browser_viewer(self, cookie_data, viewer_index):
        """Buat browser viewer"""
        driver = None
        try:
            self.log(f"[BROWSER {viewer_index}] Membuat viewer...")
            
            chrome_options = self.create_chrome_options(f"viewer_{viewer_index}")
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Akses Shopee dulu
            driver.get("https://shopee.co.id")
            time.sleep(3)
            
            # Add cookies
            for name, value in cookie_data['cookies'].items():
                try:
                    driver.add_cookie({
                        'name': name,
                        'value': value,
                        'domain': '.shopee.co.id'
                    })
                except:
                    pass
            
            # Akses live URL
            live_url = f"https://live.shopee.co.id/share?from=live&session={self.session_id}&share_user_id=266236471&stm_medium=referral&stm_source=rw&uls_trackid=53jp7veh00m4&viewer={viewer_index}#copy_link"
            
            self.log(f"[BROWSER {viewer_index}] Akses live...")
            driver.get(live_url)
            time.sleep(8)
            
            # Check berhasil atau tidak
            current_url = driver.current_url.lower()
            if 'login' not in current_url:
                self.log(f"[BROWSER {viewer_index}] ✅ Berhasil!")
                
                self.active_viewers.append({
                    'driver': driver,
                    'viewer_id': viewer_index,
                    'type': 'browser',
                    'created_at': datetime.now()
                })
                
                return True
            else:
                self.log(f"[BROWSER {viewer_index}] ❌ Redirect login")
                driver.quit()
                return False
                
        except Exception as e:
            self.log(f"[BROWSER {viewer_index}] ❌ Error: {e}")
            if driver:
                try:
                    driver.quit()
                except:
                    pass
            return False
    
    def start_bot(self, session_id, target_viewers=10):
        """Start bot utama"""
        self.session_id = session_id
        self.target_viewers = target_viewers
        
        self.log("=" * 60)
        self.log("🚀 NEO - BOT VIEWS SHOPEE")
        self.log("=" * 60)
        self.log(f"🎯 Session ID: {session_id}")
        self.log(f"🎯 Target Viewers: {target_viewers}")
        self.log("=" * 60)
        
        # Fase 1: Harvest cookies
        self.log("\\n🔥 FASE 1: HARVEST COOKIES")
        if not self.create_session_cookies(min(5, target_viewers)):
            self.log("❌ Gagal harvest cookies!")
            return
        
        # Fase 2: API Join
        self.log("\\n⚡ FASE 2: API JOIN")
        api_success = 0
        
        for i in range(min(target_viewers, len(self.session_cookies))):
            cookie_data = self.session_cookies[i]
            if self.api_join(cookie_data, i + 1):
                api_success += 1
                self.active_viewers.append({
                    'viewer_id': i + 1,
                    'type': 'api',
                    'created_at': datetime.now()
                })
            time.sleep(2)
        
        # Fase 3: Browser viewers jika perlu
        browser_needed = target_viewers - api_success
        if browser_needed > 0:
            self.log(f"\\n🌐 FASE 3: BROWSER VIEWERS ({browser_needed})")
            
            for i in range(min(browser_needed, len(self.session_cookies))):
                if i < len(self.session_cookies):
                    self.create_browser_viewer(self.session_cookies[i], api_success + i + 1)
                    time.sleep(5)
        
        # Status final
        total_viewers = len(self.active_viewers)
        api_viewers = len([v for v in self.active_viewers if v['type'] == 'api'])
        browser_viewers = len([v for v in self.active_viewers if v['type'] == 'browser'])
        
        self.log("\\n" + "=" * 60)
        self.log("✅ BOT AKTIF!")
        self.log(f"📊 Total Viewers: {total_viewers}/{target_viewers}")
        self.log(f"⚡ API: {api_viewers}")
        self.log(f"🌐 Browser: {browser_viewers}")
        self.log("=" * 60)
        
        if total_viewers == 0:
            self.log("❌ TIDAK ADA VIEWERS AKTIF!")
            return
        
        # Keep bot running
        self.log("\\n💚 Bot berjalan... Tekan Ctrl+C untuk stop")
        try:
            while True:
                time.sleep(60)
                # Check browser viewers masih hidup
                active_browsers = 0
                for viewer in self.active_viewers[:]:
                    if viewer['type'] == 'browser':
                        try:
                            viewer['driver'].current_url
                            active_browsers += 1
                        except:
                            self.active_viewers.remove(viewer)
                
                current_total = len(self.active_viewers)
                self.log(f"💚 Status: {current_total} viewers aktif (API: {api_viewers}, Browser: {active_browsers})")
                
        except KeyboardInterrupt:
            self.log("\\n🛑 Bot dihentikan...")
            self.cleanup()
    
    def cleanup(self):
        """Cleanup resources"""
        self.log("🧹 Cleanup...")
        for viewer in self.active_viewers:
            if viewer['type'] == 'browser' and 'driver' in viewer:
                try:
                    viewer['driver'].quit()
                except:
                    pass
        self.log("✅ Cleanup selesai!")

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("\\nUsage: python ultimate_shopee_bot.py <session_id> [viewer_count]")
        print("Contoh: python ultimate_shopee_bot.py 157889844 10")
        sys.exit(1)
    
    session_id = sys.argv[1]
    viewer_count = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    
    bot = NeoShopeeBot()
    bot.start_bot(session_id, viewer_count)

if __name__ == "__main__":
    main()
