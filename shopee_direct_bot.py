#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shopee Live Bot - Direct Chrome dengan Device ID Manipulation
Buka Chrome langsung dengan akun berbeda, manipulasi device_id, lalu akses live
"""

import os
import csv
import time
import json
import random
import string
import threading
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from concurrent.futures import ThreadPoolExecutor, as_completed

class DeviceIDGenerator:
    """Generate unique device IDs untuk bypass Shopee detection"""
    
    def __init__(self):
        self.used_device_ids = set()
    
    def generate_device_id(self, viewer_id):
        """Generate unique device ID format seperti Shopee"""
        # Format: 32 karakter hex uppercase
        while True:
            # Base pattern dengan variasi per viewer
            base_chars = ''.join(random.choices('ABCDEF0123456789', k=32))
            
            # Inject viewer-specific pattern
            viewer_hex = format(viewer_id, '02X')  # Convert ke hex
            timestamp_hex = format(int(time.time()) % 10000, '04X')
            
            # Replace beberapa karakter dengan viewer-specific data
            device_id_list = list(base_chars)
            device_id_list[0:2] = list(viewer_hex)  # 2 karakter pertama
            device_id_list[30:32] = list(timestamp_hex[:2])  # 2 karakter terakhir
            
            device_id = ''.join(device_id_list)
            
            if device_id not in self.used_device_ids:
                self.used_device_ids.add(device_id)
                return device_id
    
    def generate_fingerprint_data(self, viewer_id):
        """Generate complete fingerprint data"""
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ]
        
        screen_resolutions = [
            (1920, 1080), (1366, 768), (1536, 864), (1440, 900),
            (1280, 1024), (1600, 900), (1680, 1050), (1920, 1200)
        ]
        
        device_memories = [2, 4, 8, 16]
        cpu_cores = [2, 4, 6, 8, 12]
        
        # Select based on viewer_id untuk consistency
        width, height = screen_resolutions[viewer_id % len(screen_resolutions)]
        
        return {
            'device_id': self.generate_device_id(viewer_id),
            'user_agent': user_agents[viewer_id % len(user_agents)],
            'screen_width': width,
            'screen_height': height,
            'device_memory': device_memories[viewer_id % len(device_memories)],
            'hardware_concurrency': cpu_cores[viewer_id % len(cpu_cores)],
            'timezone_offset': random.choice([-420, -480, -360]),  # Different timezones
            'language': random.choice(['id-ID', 'en-US', 'id'])
        }

class GoogleAccountManager:
    """Manage Google accounts dari CSV"""
    
    def __init__(self, csv_file='accounts/google_accounts_100.csv'):
        self.csv_file = csv_file
        self.accounts = []
        self.load_accounts()
    
    def load_accounts(self):
        """Load Google accounts"""
        try:
            if os.path.exists(self.csv_file):
                with open(self.csv_file, 'r', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    self.accounts = [row for row in reader if row['status'] == 'active']
                    
                print(f"✅ Loaded {len(self.accounts)} Google accounts")
            else:
                print(f"❌ CSV file not found: {self.csv_file}")
        except Exception as e:
            print(f"❌ Error loading accounts: {e}")
    
    def get_account_for_viewer(self, viewer_id):
        """Get account untuk specific viewer"""
        if not self.accounts:
            return None
        
        account_index = (viewer_id - 1) % len(self.accounts)
        return self.accounts[account_index]

class ShopeeDirectViewer:
    """Direct Shopee viewer dengan device ID manipulation"""
    
    def __init__(self, viewer_id, session_id, google_account, fingerprint_data):
        self.viewer_id = viewer_id
        self.session_id = session_id
        self.google_account = google_account
        self.fingerprint = fingerprint_data
        self.driver = None
        self.is_running = False
    
    def create_chrome_instance(self):
        """Create Chrome instance dengan unique fingerprint"""
        try:
            # Create unique profile path
            profile_path = os.path.abspath(f"sessions/direct_profiles/viewer_{self.viewer_id}")
            os.makedirs(profile_path, exist_ok=True)
            
            options = Options()
            
            # Profile settings
            options.add_argument(f"--user-data-dir={profile_path}")
            options.add_argument("--profile-directory=Default")
            
            # Set unique user agent
            options.add_argument(f"--user-agent={self.fingerprint['user_agent']}")
            
            # Window positioning
            x_offset = (self.viewer_id - 1) * 350
            y_offset = (self.viewer_id - 1) % 3 * 250
            options.add_argument(f"--window-position={x_offset},{y_offset}")
            options.add_argument(f"--window-size={self.fingerprint['screen_width']},{self.fingerprint['screen_height']}")
            
            # Anti-detection
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            # Additional options
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--remote-debugging-port=0")
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            
            # Inject device fingerprint SEBELUM load halaman apapun
            self.inject_device_manipulation()
            
            print(f"✅ Chrome Viewer #{self.viewer_id} created with Device ID: {self.fingerprint['device_id'][:8]}...")
            return True
            
        except Exception as e:
            print(f"❌ Error creating Chrome Viewer #{self.viewer_id}: {e}")
            return False
    
    def inject_device_manipulation(self):
        """Inject JavaScript untuk manipulasi device ID dan fingerprint"""
        device_script = f"""
        // === DEVICE ID MANIPULATION ===
        // Override localStorage untuk device_id
        const originalSetItem = Storage.prototype.setItem;
        const originalGetItem = Storage.prototype.getItem;
        
        Storage.prototype.setItem = function(key, value) {{
            if (key === 'device_id' || key.includes('device')) {{
                console.log('Intercepted device_id set:', key, value);
                value = '{self.fingerprint["device_id"]}';
            }}
            return originalSetItem.call(this, key, value);
        }};
        
        Storage.prototype.getItem = function(key) {{
            if (key === 'device_id' || key.includes('device')) {{
                console.log('Intercepted device_id get:', key);
                return '{self.fingerprint["device_id"]}';
            }}
            return originalGetItem.call(this, key);
        }};
        
        // Pre-set device_id di localStorage
        localStorage.setItem('device_id', '{self.fingerprint["device_id"]}');
        
        // === FINGERPRINT MANIPULATION ===
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
            get: () => 'Win32'
        }});
        
        Object.defineProperty(navigator, 'webdriver', {{
            get: () => undefined
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
        
        // Override Date untuk timezone
        const originalGetTimezoneOffset = Date.prototype.getTimezoneOffset;
        Date.prototype.getTimezoneOffset = function() {{
            return {self.fingerprint['timezone_offset']};
        }};
        
        // Generate unique canvas fingerprint
        const toDataURL = HTMLCanvasElement.prototype.toDataURL;
        HTMLCanvasElement.prototype.toDataURL = function() {{
            const context = this.getContext('2d');
            context.fillStyle = 'rgb({random.randint(0,255)}, {random.randint(0,255)}, {random.randint(0,255)})';
            context.fillRect({self.viewer_id}, {self.viewer_id}, 1, 1);
            return toDataURL.apply(this, arguments);
        }};
        
        // Override WebGL fingerprint
        const getParameter = WebGLRenderingContext.prototype.getParameter;
        WebGLRenderingContext.prototype.getParameter = function(parameter) {{
            if (parameter === 37445) {{
                return 'Google Inc. (Viewer{self.viewer_id})';
            }}
            if (parameter === 37446) {{
                return 'ANGLE (Intel, Viewer{self.viewer_id} Graphics Direct3D11)';
            }}
            return getParameter.call(this, parameter);
        }};
        
        console.log('🔧 Device fingerprint manipulated for Viewer #{self.viewer_id}');
        console.log('📱 Device ID:', '{self.fingerprint["device_id"]}');
        console.log('💻 User Agent:', navigator.userAgent);
        console.log('📺 Screen:', screen.width + 'x' + screen.height);
        """
        
        try:
            # Inject via CDP (Chrome DevTools Protocol)
            self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                'source': device_script
            })
            print(f"✅ Device manipulation injected for Viewer #{self.viewer_id}")
        except Exception as e:
            print(f"⚠️ CDP injection failed, using fallback: {e}")
            # Fallback ke execute_script
            try:
                self.driver.execute_script(device_script)
            except Exception as fallback_error:
                print(f"❌ Script injection failed: {fallback_error}")
    
    def google_login(self):
        """Login ke Google dengan akun yang diberikan"""
        try:
            print(f"🔐 Logging in Google for Viewer #{self.viewer_id}: {self.google_account['email']}")
            
            # Go to Google login
            self.driver.get("https://accounts.google.com/signin")
            time.sleep(3)
            
            # Email input
            try:
                email_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "identifierId"))
                )
                email_input.clear()
                email_input.send_keys(self.google_account['email'])
                
                # Click Next
                next_button = self.driver.find_element(By.ID, "identifierNext")
                next_button.click()
                time.sleep(4)
            except Exception as e:
                print(f"❌ Email input error: {e}")
                return False
            
            # Password input
            try:
                password_input = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.NAME, "password"))
                )
                password_input.clear()
                password_input.send_keys(self.google_account['password'])
                
                # Click Next
                password_next = self.driver.find_element(By.ID, "passwordNext")
                password_next.click()
                time.sleep(6)
            except Exception as e:
                print(f"❌ Password input error: {e}")
                return False
            
            # Verify login success
            current_url = self.driver.current_url
            if "myaccount.google.com" in current_url or ("accounts.google.com" in current_url and "signin" not in current_url):
                print(f"✅ Google login successful for Viewer #{self.viewer_id}")
                return True
            else:
                print(f"⚠️ Google login uncertain for Viewer #{self.viewer_id}")
                return True  # Continue anyway
                
        except Exception as e:
            print(f"❌ Google login error for Viewer #{self.viewer_id}: {e}")
            return False
    
    def access_shopee_live(self):
        """Akses Shopee live dengan device ID yang sudah dimanipulasi"""
        try:
            live_url = f"https://live.shopee.co.id/share?from=live&session={self.session_id}&in=1"
            print(f"🎬 Viewer #{self.viewer_id} accessing: {live_url}")
            
            # Go to Shopee live
            self.driver.get(live_url)
            time.sleep(5)
            
            # Check device ID di console
            device_check_script = """
            return {
                device_id: localStorage.getItem('device_id'),
                current_url: window.location.href,
                user_agent: navigator.userAgent.substring(0, 50),
                screen: screen.width + 'x' + screen.height,
                device_memory: navigator.deviceMemory,
                hardware_concurrency: navigator.hardwareConcurrency
            };
            """
            
            device_info = self.driver.execute_script(device_check_script)
            
            print(f"🔍 Viewer #{self.viewer_id} Device Info:")
            print(f"   Device ID: {device_info.get('device_id', 'NOT_FOUND')}")
            print(f"   Screen: {device_info.get('screen', 'unknown')}")
            print(f"   Memory: {device_info.get('device_memory', 'unknown')} GB")
            print(f"   CPU: {device_info.get('hardware_concurrency', 'unknown')} cores")
            
            # Verify di live session
            current_url = self.driver.current_url
            if str(self.session_id) in current_url:
                print(f"✅ Viewer #{self.viewer_id} successfully joined live session")
                return True
            else:
                print(f"⚠️ Viewer #{self.viewer_id} join status uncertain")
                return True
                
        except Exception as e:
            print(f"❌ Shopee live access error for Viewer #{self.viewer_id}: {e}")
            return False
    
    def simulate_viewer_activity(self):
        """Simulate real viewer activity"""
        try:
            self.is_running = True
            while self.is_running:
                # Random scroll
                scroll_amount = random.randint(-300, 300)
                self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                
                # Random click di area aman (tidak ganggu UI)
                try:
                    safe_click_script = f"""
                    const x = Math.random() * (window.innerWidth - 100) + 50;
                    const y = Math.random() * (window.innerHeight - 100) + 50;
                    const event = new MouseEvent('click', {{
                        clientX: x,
                        clientY: y,
                        bubbles: false
                    }});
                    document.elementFromPoint(x, y)?.dispatchEvent(event);
                    """
                    if random.random() < 0.3:  # 30% chance untuk click
                        self.driver.execute_script(safe_click_script)
                except:
                    pass
                
                # Random wait
                wait_time = random.randint(20, 60)
                time.sleep(wait_time)
                
        except Exception as e:
            print(f"❌ Activity simulation error for Viewer #{self.viewer_id}: {e}")
    
    def start(self):
        """Start complete viewer process"""
        try:
            print(f"\n{'='*50}")
            print(f"🚀 Starting Viewer #{self.viewer_id}")
            print(f"📧 Google: {self.google_account['email']}")
            print(f"📱 Device ID: {self.fingerprint['device_id']}")
            print(f"{'='*50}")
            
            # Step 1: Create Chrome
            if not self.create_chrome_instance():
                return False
            
            # Step 2: Google login
            if not self.google_login():
                return False
            
            # Step 3: Access Shopee live
            if not self.access_shopee_live():
                return False
            
            # Step 4: Start activity simulation
            activity_thread = threading.Thread(target=self.simulate_viewer_activity)
            activity_thread.daemon = True
            activity_thread.start()
            
            print(f"🎉 Viewer #{self.viewer_id} is now watching live session!")
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
                print(f"🛑 Viewer #{self.viewer_id} stopped")
            except:
                pass

class ShopeeDirectBot:
    """Main bot untuk direct Chrome viewers"""
    
    def __init__(self):
        self.account_manager = GoogleAccountManager()
        self.device_generator = DeviceIDGenerator()
        self.viewers = []
    
    def start_direct_viewers(self, session_id, num_viewers):
        """Start viewers langsung dengan akun Google"""
        if not self.account_manager.accounts:
            print("❌ No Google accounts found in CSV!")
            return
        
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║              SHOPEE DIRECT VIEWER BOT STARTING             ║
╚══════════════════════════════════════════════════════════════╝

🎯 Session ID: {session_id}
👥 Viewers: {num_viewers}
📧 Google Accounts: {len(self.account_manager.accounts)}
🔧 Device ID Manipulation: ENABLED

⏳ Starting viewers with unique device fingerprints...
""")
        
        success_count = 0
        
        for i in range(num_viewers):
            viewer_id = i + 1
            
            # Get Google account
            google_account = self.account_manager.get_account_for_viewer(viewer_id)
            if not google_account:
                print(f"❌ No Google account for Viewer #{viewer_id}")
                continue
            
            # Generate unique fingerprint
            fingerprint_data = self.device_generator.generate_fingerprint_data(viewer_id)
            
            # Create viewer
            viewer = ShopeeDirectViewer(viewer_id, session_id, google_account, fingerprint_data)
            
            if viewer.start():
                self.viewers.append(viewer)
                success_count += 1
            
            # Delay antar viewers untuk stability
            if i < num_viewers - 1:
                delay = random.randint(3, 8)
                print(f"⏳ Delay {delay}s before next viewer...")
                time.sleep(delay)
        
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║                 DIRECT VIEWERS ACTIVE                       ║
╚══════════════════════════════════════════════════════════════╝

📊 Active Viewers: {success_count}/{num_viewers}
🎬 Session: {session_id}
📱 Unique Device IDs: {success_count}

🎉 Check Shopee live - viewer count should increase!
""")
        
        # Keep running dan monitoring
        try:
            while True:
                time.sleep(60)
                active_count = sum(1 for v in self.viewers if v.is_running)
                print(f"📊 [{datetime.now().strftime('%H:%M:%S')}] Active viewers: {active_count}/{len(self.viewers)}")
                
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
║         SHOPEE DIRECT VIEWER BOT - DEVICE ID BYPASS        ║
╚══════════════════════════════════════════════════════════════╝

🎯 Features:
   ├─ Direct Chrome login dengan Google accounts
   ├─ Device ID manipulation untuk setiap viewer
   ├─ Unique browser fingerprint per viewer
   └─ Real viewer count increase

🔧 Process:
   1. Buka Chrome dengan akun Google berbeda
   2. Manipulasi device_id sebelum akses Shopee
   3. Join live session dengan unique fingerprint
   4. Simulate real viewer activity
""")
    
    bot = ShopeeDirectBot()
    
    if not bot.account_manager.accounts:
        print("❌ No Google accounts found!")
        print("Please add accounts to: accounts/google_accounts_100.csv")
        return
    
    print(f"✅ Found {len(bot.account_manager.accounts)} Google accounts")
    
    # Get session ID
    session_id = input("\n🎬 Enter Shopee Live Session ID: ").strip()
    if not session_id:
        print("❌ Session ID required!")
        return
    
    # Get number of viewers
    max_viewers = len(bot.account_manager.accounts)
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
🚀 STARTING DIRECT VIEWER BOT:
   ├─ Session: {session_id}
   ├─ Viewers: {num_viewers}
   ├─ Google Accounts: {len(bot.account_manager.accounts)}
   └─ Each viewer = unique device_id

⚠️  IMPORTANT:
   - Each Chrome will login with different Google account
   - Device fingerprint manipulated before accessing Shopee
   - Viewer count should increase if working correctly

⏳ Starting in 3 seconds...
""")
    
    time.sleep(3)
    
    try:
        bot.start_direct_viewers(session_id, num_viewers)
    except KeyboardInterrupt:
        print("🛑 Bot stopped by user")
    except Exception as e:
        print(f"❌ Bot error: {e}")

if __name__ == "__main__":
    main()
