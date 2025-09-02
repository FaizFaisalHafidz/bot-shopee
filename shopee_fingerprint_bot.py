#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shopee Live Bot dengan Device Fingerprint Manipulation
Setiap Chrome profile menggunakan device fingerprint berbeda
"""

import os
import csv
import time
import json
import random
import string
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from concurrent.futures import ThreadPoolExecutor, as_completed

class DeviceFingerprintGenerator:
    """Generate unique device fingerprints untuk bypass Shopee detection"""
    
    def __init__(self):
        self.used_fingerprints = set()
    
    def generate_user_agent(self, profile_id):
        """Generate unique user agent"""
        chrome_versions = ["120.0.6099.109", "120.0.6099.129", "121.0.6167.85", "121.0.6167.139", "122.0.6261.69"]
        windows_versions = ["Windows NT 10.0; Win64; x64", "Windows NT 10.0; WOW64", "Windows NT 11.0; Win64; x64"]
        
        chrome_ver = random.choice(chrome_versions)
        win_ver = random.choice(windows_versions)
        
        # Add unique WebKit version based on profile
        webkit_base = 537 + (profile_id % 10)
        webkit_minor = 36 + (profile_id % 20)
        
        user_agent = f"Mozilla/5.0 ({win_ver}) AppleWebKit/{webkit_base}.{webkit_minor} (KHTML, like Gecko) Chrome/{chrome_ver} Safari/{webkit_base}.{webkit_minor}"
        return user_agent
    
    def generate_device_memory(self, profile_id):
        """Generate device memory"""
        memories = [2, 4, 8, 16, 32]
        return memories[profile_id % len(memories)]
    
    def generate_hardware_concurrency(self, profile_id):
        """Generate CPU cores"""
        cores = [2, 4, 6, 8, 12, 16]
        return cores[profile_id % len(cores)]
    
    def generate_screen_resolution(self, profile_id):
        """Generate unique screen resolution"""
        resolutions = [
            (1920, 1080), (1366, 768), (1536, 864), (1440, 900),
            (1280, 1024), (1600, 900), (1680, 1050), (1920, 1200),
            (2560, 1440), (3840, 2160)
        ]
        return resolutions[profile_id % len(resolutions)]
    
    def generate_timezone(self, profile_id):
        """Generate timezone"""
        timezones = [
            "Asia/Jakarta", "Asia/Makassar", "Asia/Jayapura",
            "Asia/Singapore", "Asia/Kuala_Lumpur", "Asia/Bangkok"
        ]
        return timezones[profile_id % len(timezones)]
    
    def generate_webgl_vendor(self, profile_id):
        """Generate WebGL vendor/renderer"""
        vendors = [
            ("Google Inc. (Intel)", "ANGLE (Intel, Intel(R) UHD Graphics 630 Direct3D11 vs_5_0 ps_5_0)"),
            ("Google Inc. (NVIDIA)", "ANGLE (NVIDIA, NVIDIA GeForce GTX 1060 Direct3D11 vs_5_0 ps_5_0)"),
            ("Google Inc. (AMD)", "ANGLE (AMD, AMD Radeon RX 580 Direct3D11 vs_5_0 ps_5_0)"),
            ("Google Inc. (Intel)", "ANGLE (Intel, Intel(R) HD Graphics 4000 Direct3D11 vs_5_0 ps_5_0)"),
        ]
        return vendors[profile_id % len(vendors)]
    
    def get_fingerprint_for_profile(self, profile_id):
        """Get complete fingerprint untuk specific profile"""
        width, height = self.generate_screen_resolution(profile_id)
        webgl_vendor, webgl_renderer = self.generate_webgl_vendor(profile_id)
        
        fingerprint = {
            'user_agent': self.generate_user_agent(profile_id),
            'device_memory': self.generate_device_memory(profile_id),
            'hardware_concurrency': self.generate_hardware_concurrency(profile_id),
            'screen_width': width,
            'screen_height': height,
            'timezone': self.generate_timezone(profile_id),
            'webgl_vendor': webgl_vendor,
            'webgl_renderer': webgl_renderer,
            'language': random.choice(['id-ID', 'en-US', 'id']),
            'platform': 'Win32',
            'do_not_track': random.choice(['1', None]),
            'cookie_enabled': True,
            'online': True
        }
        
        return fingerprint

class GoogleProfileManager:
    """Manage Google profiles yang sudah di-setup"""
    
    def __init__(self, csv_file='accounts/google_accounts_100.csv'):
        self.csv_file = csv_file
        self.accounts = []
        self.load_accounts()
    
    def load_accounts(self):
        """Load accounts from CSV"""
        try:
            if os.path.exists(self.csv_file):
                with open(self.csv_file, 'r', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    self.accounts = [row for row in reader if row['status'] == 'active']
        except Exception as e:
            print(f"❌ Error loading accounts: {e}")
    
    def get_available_profiles(self):
        """Get profiles yang sudah di-setup"""
        profiles = []
        base_path = "sessions/google_profiles"
        
        if os.path.exists(base_path):
            for profile_folder in os.listdir(base_path):
                profile_path = os.path.join(base_path, profile_folder)
                if os.path.isdir(profile_path):
                    # Extract account info dari folder name
                    account_info = None
                    for acc in self.accounts:
                        if acc['profile_name'] in profile_folder:
                            account_info = acc
                            break
                    
                    profiles.append({
                        'folder': profile_folder,
                        'path': os.path.abspath(profile_path),
                        'account': account_info
                    })
        
        print(f"✅ Found {len(profiles)} Google profiles ready")
        return profiles

class ShopeeViewer:
    """Single Shopee viewer dengan unique device fingerprint"""
    
    def __init__(self, viewer_id, session_id, profile_info, fingerprint):
        self.viewer_id = viewer_id
        self.session_id = session_id
        self.profile_info = profile_info
        self.fingerprint = fingerprint
        self.driver = None
        self.is_running = False
    
    def create_chrome_with_fingerprint(self):
        """Create Chrome dengan manipulated device fingerprint"""
        try:
            options = Options()
            
            # Use existing Google profile
            profile_path = self.profile_info['path']
            options.add_argument(f"--user-data-dir={profile_path}")
            options.add_argument("--profile-directory=Default")
            
            # Set unique user agent
            options.add_argument(f"--user-agent={self.fingerprint['user_agent']}")
            
            # Window positioning (berbeda per viewer)
            x_offset = (self.viewer_id - 1) * 400
            y_offset = (self.viewer_id - 1) % 3 * 300
            options.add_argument(f"--window-position={x_offset},{y_offset}")
            options.add_argument(f"--window-size={self.fingerprint['screen_width']},{self.fingerprint['screen_height']}")
            
            # Anti-detection
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            # Additional fingerprint options
            options.add_argument(f"--lang={self.fingerprint['language']}")
            
            # Performance & stability
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--remote-debugging-port=0")
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            
            # Inject device fingerprint manipulation
            self.inject_fingerprint_override()
            
            print(f"✅ Chrome #{self.viewer_id} created with unique fingerprint")
            return True
            
        except Exception as e:
            print(f"❌ Error creating Chrome #{self.viewer_id}: {e}")
            return False
    
    def inject_fingerprint_override(self):
        """Inject JavaScript untuk override device fingerprint"""
        fingerprint_script = f"""
        // Override navigator properties
        Object.defineProperty(navigator, 'deviceMemory', {{
            get: () => {self.fingerprint['device_memory']}
        }});
        
        Object.defineProperty(navigator, 'hardwareConcurrency', {{
            get: () => {self.fingerprint['hardware_concurrency']}
        }});
        
        Object.defineProperty(navigator, 'language', {{
            get: () => '{self.fingerprint['language']}'
        }});
        
        Object.defineProperty(navigator, 'platform', {{
            get: () => '{self.fingerprint['platform']}'
        }});
        
        Object.defineProperty(navigator, 'doNotTrack', {{
            get: () => '{self.fingerprint['do_not_track'] or ""}'
        }});
        
        Object.defineProperty(navigator, 'cookieEnabled', {{
            get: () => {str(self.fingerprint['cookie_enabled']).lower()}
        }});
        
        Object.defineProperty(navigator, 'onLine', {{
            get: () => {str(self.fingerprint['online']).lower()}
        }});
        
        // Override screen properties
        Object.defineProperty(screen, 'width', {{
            get: () => {self.fingerprint['screen_width']}
        }});
        
        Object.defineProperty(screen, 'height', {{
            get: () => {self.fingerprint['screen_height']}
        }});
        
        Object.defineProperty(screen, 'availWidth', {{
            get: () => {self.fingerprint['screen_width']}
        }});
        
        Object.defineProperty(screen, 'availHeight', {{
            get: () => {self.fingerprint['screen_height'] - 40}
        }});
        
        // Override WebGL fingerprint
        const getParameter = WebGLRenderingContext.prototype.getParameter;
        WebGLRenderingContext.prototype.getParameter = function(parameter) {{
            if (parameter === 37445) {{
                return '{self.fingerprint['webgl_vendor']}';
            }}
            if (parameter === 37446) {{
                return '{self.fingerprint['webgl_renderer']}';
            }}
            return getParameter(parameter);
        }};
        
        // Override timezone
        Date.prototype.getTimezoneOffset = function() {{
            return new Date().getTimezoneOffset();
        }};
        
        // Generate unique canvas fingerprint
        const toDataURL = HTMLCanvasElement.prototype.toDataURL;
        HTMLCanvasElement.prototype.toDataURL = function() {{
            const context = this.getContext('2d');
            context.fillStyle = 'rgb({random.randint(0,255)}, {random.randint(0,255)}, {random.randint(0,255)})';
            context.fillRect(0, 0, 1, 1);
            return toDataURL.apply(this, arguments);
        }};
        
        // Override webdriver detection
        Object.defineProperty(navigator, 'webdriver', {{
            get: () => undefined
        }});
        
        console.log('Device fingerprint overridden for viewer #{self.viewer_id}');
        """
        
        try:
            self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                'source': fingerprint_script
            })
        except:
            # Fallback to execute_script
            self.driver.execute_script(fingerprint_script)
    
    def join_shopee_live(self):
        """Join Shopee live session"""
        try:
            live_url = f"https://live.shopee.co.id/{self.session_id}"
            print(f"🎬 Viewer #{self.viewer_id} joining: {live_url}")
            
            self.driver.get(live_url)
            time.sleep(5)
            
            # Check if successfully joined
            current_url = self.driver.current_url
            if str(self.session_id) in current_url:
                print(f"✅ Viewer #{self.viewer_id} joined successfully")
                return True
            else:
                print(f"⚠️ Viewer #{self.viewer_id} join status uncertain")
                return True
                
        except Exception as e:
            print(f"❌ Viewer #{self.viewer_id} join error: {e}")
            return False
    
    def check_device_id(self):
        """Check current device_id yang digunakan Shopee"""
        try:
            # Get device_id from localStorage or cookies
            device_id_script = """
            return {
                localStorage_device_id: localStorage.getItem('device_id') || 'not_found',
                cookies: document.cookie,
                userAgent: navigator.userAgent,
                screen: screen.width + 'x' + screen.height,
                fingerprint: {
                    deviceMemory: navigator.deviceMemory || 'not_available',
                    hardwareConcurrency: navigator.hardwareConcurrency || 'not_available',
                    platform: navigator.platform,
                    language: navigator.language
                }
            };
            """
            
            result = self.driver.execute_script(device_id_script)
            
            print(f"🔍 Viewer #{self.viewer_id} Device Info:")
            print(f"   User Agent: {result['userAgent'][:50]}...")
            print(f"   Screen: {result['screen']}")
            print(f"   Device Memory: {result['fingerprint']['deviceMemory']}")
            print(f"   CPU Cores: {result['fingerprint']['hardwareConcurrency']}")
            print(f"   Platform: {result['fingerprint']['platform']}")
            
            return result
            
        except Exception as e:
            print(f"❌ Error checking device info for Viewer #{self.viewer_id}: {e}")
            return None
    
    def simulate_activity(self):
        """Simulate viewer activity"""
        try:
            self.is_running = True
            while self.is_running:
                # Random scroll
                scroll_amount = random.randint(-200, 200)
                self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                
                # Random wait
                wait_time = random.randint(15, 45)
                time.sleep(wait_time)
                
        except Exception as e:
            print(f"❌ Activity error for Viewer #{self.viewer_id}: {e}")
    
    def start(self):
        """Start viewer"""
        try:
            if not self.create_chrome_with_fingerprint():
                return False
            
            if not self.join_shopee_live():
                return False
            
            # Check device fingerprint
            device_info = self.check_device_id()
            
            # Start activity simulation
            import threading
            activity_thread = threading.Thread(target=self.simulate_activity)
            activity_thread.daemon = True
            activity_thread.start()
            
            return True
            
        except Exception as e:
            print(f"❌ Viewer #{self.viewer_id} start error: {e}")
            return False
    
    def stop(self):
        """Stop viewer"""
        self.is_running = False
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass

class ShopeeMultiViewerBot:
    """Main bot dengan device fingerprint manipulation"""
    
    def __init__(self):
        self.profile_manager = GoogleProfileManager()
        self.fingerprint_generator = DeviceFingerprintGenerator()
        self.viewers = []
    
    def start_multi_viewers(self, session_id, num_viewers):
        """Start multiple viewers dengan unique fingerprints"""
        profiles = self.profile_manager.get_available_profiles()
        
        if not profiles:
            print("❌ No Google profiles found! Setup profiles first.")
            return
        
        # Limit viewers to available profiles
        max_viewers = min(num_viewers, len(profiles))
        print(f"🎯 Starting {max_viewers} viewers for session {session_id}")
        
        success_count = 0
        
        for i in range(max_viewers):
            viewer_id = i + 1
            profile_info = profiles[i]
            
            # Generate unique fingerprint
            fingerprint = self.fingerprint_generator.get_fingerprint_for_profile(viewer_id)
            
            print(f"\n{'='*60}")
            print(f"Starting Viewer #{viewer_id}")
            print(f"Profile: {profile_info['folder']}")
            print(f"Fingerprint: {fingerprint['user_agent'][:50]}...")
            print(f"{'='*60}")
            
            # Create viewer
            viewer = ShopeeViewer(viewer_id, session_id, profile_info, fingerprint)
            
            if viewer.start():
                self.viewers.append(viewer)
                success_count += 1
                print(f"✅ Viewer #{viewer_id} started successfully")
            else:
                print(f"❌ Viewer #{viewer_id} failed to start")
            
            # Delay between viewers
            if i < max_viewers - 1:
                print("⏳ Delay before next viewer...")
                time.sleep(3)
        
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║                    MULTI VIEWER ACTIVE                     ║
╚══════════════════════════════════════════════════════════════╝

📊 Results:
   ✅ Active Viewers: {success_count}
   🎬 Session: {session_id}
   🔄 Each viewer has unique device fingerprint
   
🎉 Bot is running! Check Shopee for viewer count increase.
""")
        
        # Keep running
        try:
            while True:
                time.sleep(60)
                active_count = sum(1 for v in self.viewers if v.is_running)
                print(f"📊 Active viewers: {active_count}/{len(self.viewers)}")
                
        except KeyboardInterrupt:
            print("\n🛑 Stopping all viewers...")
            self.stop_all_viewers()
    
    def stop_all_viewers(self):
        """Stop all viewers"""
        for viewer in self.viewers:
            viewer.stop()
        print("✅ All viewers stopped")

def main():
    """Main function"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║        SHOPEE MULTI VIEWER BOT - FINGERPRINT BYPASS       ║
╚══════════════════════════════════════════════════════════════╝

🎯 Features:
   ├─ Unique device fingerprint per viewer
   ├─ Uses existing Google profiles  
   ├─ Bypass Shopee device detection
   └─ Increase real viewer count

🔧 Requirements:
   └─ Google profiles must be setup first
""")
    
    bot = ShopeeMultiViewerBot()
    
    # Check available profiles
    profiles = bot.profile_manager.get_available_profiles()
    if not profiles:
        print("❌ No Google profiles found!")
        print("Please setup Google profiles first using:")
        print("   python google_profile_setup_windows.py")
        return
    
    print(f"✅ Found {len(profiles)} Google profiles ready")
    for i, profile in enumerate(profiles, 1):
        account_name = profile['account']['profile_name'] if profile['account'] else "unknown"
        print(f"   {i}. {account_name}")
    
    # Get session ID
    session_id = input(f"\n🎬 Enter Shopee Live Session ID: ").strip()
    if not session_id:
        print("❌ Session ID required!")
        return
    
    # Get number of viewers
    max_viewers = len(profiles)
    viewer_input = input(f"👥 Number of viewers (max {max_viewers}, default {max_viewers}): ").strip()
    
    if not viewer_input:
        num_viewers = max_viewers
    else:
        try:
            num_viewers = int(viewer_input)
            num_viewers = min(num_viewers, max_viewers)
        except ValueError:
            num_viewers = max_viewers
    
    print(f"""
🚀 STARTING FINGERPRINT BYPASS BOT:
   ├─ Session ID: {session_id}
   ├─ Viewers: {num_viewers}
   ├─ Profiles: {len(profiles)} available
   └─ Each viewer = unique device fingerprint

⏳ Starting in 3 seconds...
""")
    
    time.sleep(3)
    
    # Start bot
    try:
        bot.start_multi_viewers(session_id, num_viewers)
    except KeyboardInterrupt:
        print("🛑 Bot stopped by user")
    except Exception as e:
        print(f"❌ Bot error: {e}")

if __name__ == "__main__":
    main()
