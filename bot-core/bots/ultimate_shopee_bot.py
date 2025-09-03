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
        
        # Setup logging
        log_dir = os.path.join('bot-core', 'logs')
        os.makedirs(log_dir, exist_ok=True)
        self.log_file = os.path.join(log_dir, f'neo_bot_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
        
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
    
    def harvest_cookies(self, count=3):
        """Harvest cookies dari Shopee"""
        self.log(f"🔥 HARVEST COOKIES - Target: {count}")
        
        for i in range(count):
            driver = None
            try:
                self.log(f"[HARVEST {i+1}] Membuat Chrome...")
                
                chrome_options = self.create_chrome_options(f"harvest_{i}")
                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=chrome_options)
                
                # Akses Shopee
                self.log(f"[HARVEST {i+1}] Akses Shopee...")
                driver.get("https://shopee.co.id")
                time.sleep(5)
                
                # Akses live URL
                live_url = f"https://live.shopee.co.id/share?from=live&session={self.session_id}&share_user_id=266236471&stm_medium=referral&stm_source=rw&uls_trackid=53jp7veh00m4&viewer={i+1}#copy_link"
                
                self.log(f"[HARVEST {i+1}] Akses Live...")
                driver.get(live_url)
                time.sleep(8)
                
                # Get cookies
                cookies = driver.get_cookies()
                cookie_dict = {}
                for cookie in cookies:
                    cookie_dict[cookie['name']] = cookie['value']
                
                user_agent = driver.execute_script("return navigator.userAgent;")
                
                if len(cookie_dict) > 3:
                    self.session_cookies.append({
                        'cookies': cookie_dict,
                        'user_agent': user_agent,
                        'harvested_at': datetime.now(),
                        'is_valid': True
                    })
                    self.log(f"[HARVEST {i+1}] ✅ Berhasil ({len(cookie_dict)} cookies)")
                else:
                    self.log(f"[HARVEST {i+1}] ❌ Gagal")
                
                driver.quit()
                time.sleep(3)
                
            except Exception as e:
                self.log(f"[HARVEST {i+1}] ❌ Error: {e}")
                if driver:
                    try:
                        driver.quit()
                    except:
                        pass
        
        valid_cookies = len([c for c in self.session_cookies if c['is_valid']])
        self.log(f"✅ HARVEST SELESAI - {valid_cookies}/{count}")
        return valid_cookies > 0
    
    def api_join(self, cookie_data, viewer_index):
        """Join via API"""
        try:
            self.log(f"[API {viewer_index}] Join via API...")
            
            headers = {
                'authority': 'live.shopee.co.id',
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'id,en-US;q=0.9,en;q=0.8',
                'content-type': 'application/json',
                'origin': 'https://live.shopee.co.id',
                'referer': f'https://live.shopee.co.id/share?from=live&session={self.session_id}&share_user_id=266236471&stm_medium=referral&stm_source=rw&uls_trackid=53jp7veh00m4&viewer={viewer_index}',
                'user-agent': cookie_data['user_agent']
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
        if not self.harvest_cookies(min(5, target_viewers)):
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
