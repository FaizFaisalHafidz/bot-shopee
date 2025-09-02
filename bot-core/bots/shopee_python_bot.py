#!/usr/bin/env python3
"""
Shopee Live Viewer Bot - Python Version dengan Session Cookies
Tidak perlu Node.js, cukup Python + Selenium
"""

import csv
import time
import random
import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import threading

class ShopeeViewerBotPython:
    def __init__(self):
        self.session_cookies = []
        self.active_drivers = []
        self.viewer_boost = 25
        self.load_session_cookies()
        
    def load_session_cookies(self):
        """Load session cookies from input.csv"""
        try:
            csv_path = os.path.join(os.path.dirname(__file__), 'input.csv')
            
            with open(csv_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            print(f"[COOKIES] Loading {len(lines)} session cookies...")
            
            for i, line in enumerate(lines):
                line = line.strip()
                if line:
                    cookies = self.parse_cookie_string(line)
                    session_data = {
                        'id': i + 1,
                        'cookies': cookies,
                        'raw_cookies': line,
                        'device_id': self.generate_device_id(),
                        'user_agent': self.generate_user_agent()
                    }
                    self.session_cookies.append(session_data)
            
            print(f"[SUCCESS] Loaded {len(self.session_cookies)} authenticated sessions")
            
        except Exception as e:
            print(f"[ERROR] Failed to load cookies: {e}")
            exit(1)
    
    def parse_cookie_string(self, cookie_str):
        """Parse cookie string into Selenium cookie format"""
        cookies = []
        pairs = cookie_str.split('; ')
        
        for pair in pairs:
            if '=' in pair:
                name, value = pair.split('=', 1)
                cookie_dict = {
                    'name': name.strip(),
                    'value': value.strip(),
                    'domain': '.shopee.co.id',
                    'path': '/',
                    'secure': True,
                    'httpOnly': False
                }
                cookies.append(cookie_dict)
        
        return cookies
    
    def generate_device_id(self):
        """Generate random device ID"""
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        return ''.join(random.choice(chars) for _ in range(32))
    
    def generate_user_agent(self):
        """Generate random user agent"""
        versions = ['120.0.0.0', '119.0.0.0', '118.0.0.0', '117.0.0.0']
        version = random.choice(versions)
        return f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version} Safari/537.36'
    
    def create_viewer(self, session_data, session_id, viewer_index):
        """Create single viewer with session cookies"""
        try:
            print(f"[VIEWER {viewer_index}] Starting with session cookies...")
            
            # Chrome options
            chrome_options = Options()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-web-security')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument(f'--user-agent={session_data["user_agent"]}')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_argument('--no-first-run')
            chrome_options.add_argument('--mute-audio')
            
            # Profile directory
            profile_dir = os.path.join('sessions', 'viewer_sessions', f'viewer_{viewer_index}')
            os.makedirs(profile_dir, exist_ok=True)
            chrome_options.add_argument(f'--user-data-dir={profile_dir}')
            
            # Create driver
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Set window size
            driver.set_window_size(1366, 768)
            
            # Go to Shopee first to set domain for cookies
            driver.get('https://shopee.co.id')
            time.sleep(3)
            
            # Set cookies
            print(f"[VIEWER {viewer_index}] Setting {len(session_data['cookies'])} cookies...")
            for cookie in session_data['cookies']:
                try:
                    driver.add_cookie(cookie)
                except Exception as e:
                    # Skip invalid cookies
                    pass
            
            # Navigate to live stream
            shopee_url = f"https://live.shopee.co.id/share?from=live&session={session_id}&in=1"
            print(f"[VIEWER {viewer_index}] Navigating to: {shopee_url}")
            driver.get(shopee_url)
            
            # Wait for page load
            time.sleep(8)
            
            # Inject viewer manipulation script
            driver.execute_script(f"""
                // Device fingerprint override
                Object.defineProperty(navigator, 'deviceMemory', {{get: () => 8}});
                Object.defineProperty(navigator, 'hardwareConcurrency', {{get: () => 8}});
                Object.defineProperty(navigator, 'webdriver', {{get: () => undefined}});
                
                // Set device ID
                localStorage.setItem('device_id', '{session_data["device_id"]}');
                sessionStorage.setItem('session_device_id', '{session_data["device_id"]}');
                
                console.log('[INJECT] Device fingerprint set: {session_data["device_id"][:8]}...');
                
                // Viewer count manipulation
                setInterval(() => {{
                    const selectors = [
                        '[class*="viewer"]',
                        '[class*="count"]', 
                        '[data-testid*="viewer"]',
                        '[class*="audience"]',
                        '.live-viewer-count',
                        '.viewer-number'
                    ];
                    
                    selectors.forEach(selector => {{
                        const elements = document.querySelectorAll(selector);
                        elements.forEach(el => {{
                            const text = el.textContent || el.innerText;
                            if (text && /\\d+/.test(text)) {{
                                const match = text.match(/\\d+/);
                                if (match) {{
                                    const currentCount = parseInt(match[0]);
                                    if (currentCount > 0 && currentCount < 50000) {{
                                        const boost = {self.viewer_boost} + Math.floor(Math.random() * 10);
                                        const newCount = currentCount + boost;
                                        const newText = text.replace(/\\d+/, newCount.toString());
                                        el.textContent = newText;
                                        el.innerText = newText;
                                    }}
                                }}
                            }}
                        }});
                    }});
                    
                    console.log('[BOOST] Viewer count manipulation active (+{self.viewer_boost})');
                }}, 8000);
                
                // Keep page active
                setInterval(() => {{
                    document.dispatchEvent(new Event('mousemove'));
                }}, 30000);
            """)
            
            print(f"[SUCCESS] Viewer {viewer_index} active with session cookies!")
            print(f"[INFO] Device ID: {session_data['device_id'][:8]}...{session_data['device_id'][-4:]}")
            
            self.active_drivers.append({
                'driver': driver,
                'viewer_id': viewer_index,
                'session_data': session_data
            })
            
            return driver
            
        except Exception as e:
            print(f"[ERROR] Failed to create viewer {viewer_index}: {e}")
            if 'driver' in locals():
                driver.quit()
            return None
    
    def start_viewers(self, session_id, viewer_count):
        """Start multiple viewers with session cookies"""
        print("\n==========================================")
        print("   SHOPEE VIEWER BOT - PYTHON + COOKIES")
        print("==========================================")
        print(f"Target Session: {session_id}")
        print(f"Viewers: {viewer_count}")
        print(f"Available Sessions: {len(self.session_cookies)}")
        print("==========================================\n")
        
        if viewer_count > len(self.session_cookies):
            print(f"[WARNING] Requested {viewer_count} viewers but only {len(self.session_cookies)} sessions available")
            viewer_count = len(self.session_cookies)
        
        # Create viewers in threads for faster startup
        threads = []
        
        for i in range(viewer_count):
            session_data = self.session_cookies[i]
            
            def create_viewer_thread(session_data, session_id, viewer_index):
                self.create_viewer(session_data, session_id, viewer_index + 1)
                # Random delay between viewers
                delay = 3 + random.uniform(2, 5)
                print(f"[DELAY] Viewer {viewer_index + 1} waiting {delay:.1f}s...")
                time.sleep(delay)
            
            thread = threading.Thread(
                target=create_viewer_thread,
                args=(session_data, session_id, i)
            )
            threads.append(thread)
            thread.start()
            
            # Small delay between thread starts
            time.sleep(1)
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        print(f"\n[COMPLETED] {len(self.active_drivers)}/{viewer_count} viewers started successfully!")
        print("[INFO] Viewers will continue running with boost manipulation")
        print("[INFO] Press Ctrl+C to stop all viewers")
        
        # Keep alive and monitor
        try:
            while True:
                time.sleep(60)
                active_count = len([d for d in self.active_drivers if d['driver'].service.is_connectable()])
                print(f"[ALIVE] {active_count} viewers active")
        except KeyboardInterrupt:
            print("\n[CLEANUP] Stopping all viewers...")
            for driver_info in self.active_drivers:
                try:
                    driver_info['driver'].quit()
                except:
                    pass
            print("[CLEANUP] All viewers stopped.")

def main():
    """Main function"""
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python3 shopee_python_bot.py <session_id> <viewer_count>")
        print("Example: python3 shopee_python_bot.py 157658364 5")
        sys.exit(1)
    
    session_id = sys.argv[1]
    viewer_count = int(sys.argv[2])
    
    bot = ShopeeViewerBotPython()
    bot.start_viewers(session_id, viewer_count)

if __name__ == "__main__":
    main()
