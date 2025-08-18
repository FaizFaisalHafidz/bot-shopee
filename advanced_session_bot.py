#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced Session Manager - Bypass Login dengan Teknik Advanced
Generate fresh sessions untuk bypass cookies expired
"""

import time
import random
import threading
import os
import sys
from datetime import datetime
import json

# Browser automation imports
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    SELENIUM_AVAILABLE = True
except ImportError:
    print("❌ Selenium not installed! Run: pip install selenium")
    SELENIUM_AVAILABLE = False

try:
    import undetected_chromedriver as uc
    UNDETECTED_AVAILABLE = True
except ImportError:
    UNDETECTED_AVAILABLE = False

class AdvancedSessionManager:
    def __init__(self):
        self.active_sessions = []
        self.session_pool = []
        self.success_count = 0
        self.failure_count = 0
        self.running = False
        
    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")
    
    def create_advanced_driver(self, profile_num):
        """Create driver dengan advanced evasion techniques"""
        try:
            if UNDETECTED_AVAILABLE:
                options = uc.ChromeOptions()
            else:
                options = Options()
            
            # Advanced evasion techniques
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            # Profile separation
            options.add_argument(f'--user-data-dir=/tmp/chrome_profile_{profile_num}')
            
            # Random settings
            window_sizes = ['1366,768', '1920,1080', '1440,900', '1280,720', '1536,864']
            options.add_argument(f'--window-size={random.choice(window_sizes)}')
            
            # Realistic user agents
            user_agents = [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            ]
            options.add_argument(f'--user-agent={random.choice(user_agents)}')
            
            # Additional evasion
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-plugins-discovery')
            options.add_argument('--disable-web-security')
            options.add_argument('--allow-running-insecure-content')
            
            if UNDETECTED_AVAILABLE:
                driver = uc.Chrome(options=options, version_main=None)
            else:
                driver = webdriver.Chrome(options=options)
            
            # Advanced anti-detection script
            driver.execute_script("""
                // Remove webdriver traces
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                
                // Fake plugins
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [
                        {name: 'Chrome PDF Plugin', description: 'Portable Document Format'},
                        {name: 'Chrome PDF Viewer', description: 'PDF Viewer'},
                        {name: 'Native Client', description: 'Native Client'},
                    ]
                });
                
                // Fake permissions
                Object.defineProperty(navigator, 'permissions', {
                    get: () => ({
                        query: () => Promise.resolve({state: 'granted'})
                    })
                });
                
                // Fake chrome object
                window.chrome = {
                    runtime: {
                        onConnect: null,
                        onMessage: null
                    }
                };
                
                // Override languages
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['en-US', 'en', 'id-ID', 'id']
                });
                
                // Random canvas fingerprint
                const getContext = HTMLCanvasElement.prototype.getContext;
                HTMLCanvasElement.prototype.getContext = function(type) {
                    if (type === '2d') {
                        const context = getContext.call(this, type);
                        const originalFillText = context.fillText;
                        context.fillText = function() {
                            const args = Array.from(arguments);
                            args[0] = args[0] + Math.random().toString(36).substring(7);
                            return originalFillText.apply(this, args);
                        };
                        return context;
                    }
                    return getContext.call(this, type);
                };
            """)
            
            return driver
            
        except Exception as e:
            self.log(f"❌ Error creating advanced driver: {e}")
            return None
    
    def generate_fresh_session(self, session_id, profile_num):
        """Generate fresh session untuk bypass login"""
        driver = None
        try:
            self.log(f"🔮 [{profile_num}] Generating fresh session...")
            
            driver = self.create_advanced_driver(profile_num)
            if not driver:
                return False
            
            # Step 1: Get base session dari shopee
            self.log(f"🌐 [{profile_num}] Establishing base session...")
            driver.get("https://shopee.co.id")
            time.sleep(random.uniform(3, 6))
            
            # Step 2: Interact dengan page untuk generate valid session
            try:
                # Scroll untuk trigger session activity
                for _ in range(3):
                    driver.execute_script(f"window.scrollBy(0, {random.randint(100, 500)});")
                    time.sleep(random.uniform(1, 3))
                
                # Click some elements untuk simulate user behavior
                try:
                    elements = driver.find_elements(By.TAG_NAME, "a")[:5]
                    for element in elements:
                        try:
                            if element.is_displayed():
                                driver.execute_script("arguments[0].click();", element)
                                time.sleep(random.uniform(0.5, 2))
                                break
                        except:
                            continue
                except:
                    pass
                
            except Exception as e:
                self.log(f"⚠️ [{profile_num}] Session interaction warning: {e}")
            
            # Step 3: Navigate to live stream
            live_url = f"https://live.shopee.co.id/share?from=live&session={session_id}"
            self.log(f"🎥 [{profile_num}] Accessing live stream with fresh session...")
            
            driver.get(live_url)
            time.sleep(random.uniform(5, 10))
            
            # Step 4: Check access success
            current_url = driver.current_url
            self.log(f"📍 [{profile_num}] Final URL: {current_url}")
            
            # Check for success
            if 'live.shopee.co.id' in current_url and 'login' not in current_url:
                # Additional verification
                try:
                    time.sleep(5)
                    page_title = driver.title.lower()
                    page_source = driver.page_source.lower()
                    
                    # Look for live indicators
                    live_keywords = ['live', 'streaming', 'viewer', 'watching', 'shopee live']
                    found_keywords = sum(1 for keyword in live_keywords if keyword in page_title or keyword in page_source)
                    
                    if found_keywords >= 2:
                        self.log(f"✅ [{profile_num}] SUCCESS! Fresh session active on live stream")
                        
                        # Keep session alive with realistic activity
                        session_duration = random.randint(120, 600)  # 2-10 minutes
                        self.log(f"⏱️ [{profile_num}] Maintaining session for {session_duration}s...")
                        
                        start_time = time.time()
                        while time.time() - start_time < session_duration and self.running:
                            try:
                                # Simulate viewing activity
                                activities = [
                                    lambda: driver.execute_script("window.scrollBy(0, Math.floor(Math.random() * 200 - 100));"),
                                    lambda: driver.execute_script("window.focus();"),
                                    lambda: driver.refresh() if random.random() < 0.1 else None,
                                ]
                                
                                random.choice(activities)()
                                time.sleep(random.uniform(30, 90))
                                
                            except Exception as e:
                                self.log(f"⚠️ [{profile_num}] Activity simulation error: {e}")
                                break
                        
                        self.success_count += 1
                        return True
                    else:
                        self.log(f"❌ [{profile_num}] Live indicators not found")
                
                except Exception as e:
                    self.log(f"⚠️ [{profile_num}] Verification error: {e}")
            else:
                self.log(f"❌ [{profile_num}] Not on live stream or redirected to login")
            
            self.failure_count += 1
            return False
            
        except Exception as e:
            self.log(f"❌ [{profile_num}] Session generation failed: {e}")
            self.failure_count += 1
            return False
        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass
    
    def run_advanced_session_bot(self, session_id, num_sessions=5):
        """Run advanced session bot"""
        self.running = True
        self.success_count = 0
        self.failure_count = 0
        
        print("\n" + "="*70)
        self.log("🔮 STARTING ADVANCED SESSION MANAGER")
        self.log(f"🎯 Target Session ID: {session_id}")
        self.log(f"🚀 Concurrent fresh sessions: {num_sessions}")
        self.log(f"🛡️ Mode: ADVANCED BYPASS - No login required")
        print("="*70)
        
        # Launch multiple fresh sessions
        threads = []
        
        for i in range(num_sessions):
            if not self.running:
                break
            
            profile_num = i + 1
            thread = threading.Thread(
                target=self.generate_fresh_session,
                args=(session_id, profile_num)
            )
            threads.append(thread)
            thread.start()
            
            # Stagger launches to avoid detection
            time.sleep(random.uniform(5, 12))
        
        # Wait for all sessions
        for thread in threads:
            thread.join()
        
        self.running = False
        
        # Final report
        print("\n" + "="*70)
        self.log("🎉 ADVANCED SESSION MANAGER COMPLETED")
        self.log(f"✅ Successful sessions: {self.success_count}")
        self.log(f"❌ Failed sessions: {self.failure_count}")
        total = self.success_count + self.failure_count
        if total > 0:
            success_rate = (self.success_count / total) * 100
            self.log(f"📊 Success rate: {success_rate:.1f}%")
            
            if success_rate >= 60:
                self.log("🔥 EXCELLENT: High success rate with fresh sessions!")
            elif success_rate >= 30:
                self.log("⚡ GOOD: Moderate success with bypass technique")
            else:
                self.log("⚠️ LOW: May need different approach")
        print("="*70)

def main():
    print("""
    ╔═══════════════════════════════════════════════════════╗
    ║        ADVANCED SESSION MANAGER v1.0                  ║
    ║         BYPASS LOGIN - FRESH SESSION GENERATION       ║
    ╚═══════════════════════════════════════════════════════╝
    
    🔮 Advanced Features:
    ✅ NO cookies required (generate fresh sessions)
    ✅ Advanced anti-detection evasion
    ✅ Multiple isolated browser profiles  
    ✅ Realistic user behavior simulation
    ✅ Session persistence management
    ✅ Bypass expired cookie problem
    
    💡 Technical Approach:
    - Generate fresh browser sessions
    - Advanced fingerprint evasion
    - Realistic user activity simulation
    - Multiple concurrent sessions
    - No dependency on client cookies
    """)
    
    if not SELENIUM_AVAILABLE:
        print("❌ Selenium required! Install: pip install selenium")
        return
    
    manager = AdvancedSessionManager()
    
    # Get session ID
    while True:
        session_input = input("\n🔗 Masukkan Session ID atau URL live Shopee: ").strip()
        
        if not session_input:
            print("❌ Session ID tidak boleh kosong!")
            continue
        
        # Extract session ID
        if 'live.shopee.co.id' in session_input:
            import re
            match = re.search(r'[?&]session=(\d+)', session_input)
            if match:
                session_id = match.group(1)
                print(f"✅ Session ID extracted: {session_id}")
                break
            match = re.search(r'live\.shopee\.co\.id/(\d+)', session_input)
            if match:
                session_id = match.group(1)
                print(f"✅ Session ID extracted: {session_id}")
                break
        elif session_input.isdigit():
            session_id = session_input
            print(f"✅ Session ID: {session_id}")
            break
        else:
            print("❌ Format tidak valid! Gunakan session ID atau URL live Shopee")
    
    # Ask for number of sessions
    while True:
        try:
            sessions_input = input(f"\n🔢 Berapa fresh sessions yang ingin di-generate? (1-8, default 3): ").strip()
            
            if not sessions_input:
                num_sessions = 3
                break
            
            num_sessions = int(sessions_input)
            if 1 <= num_sessions <= 8:
                break
            else:
                print("❌ Jumlah harus antara 1-8")
        except ValueError:
            print("❌ Input harus berupa angka!")
    
    # Confirmation
    print(f"\n⚠️ ADVANCED SESSION WARNING:")
    print(f"🔮 Bot akan generate {num_sessions} fresh sessions")
    print(f"🛡️ Advanced evasion techniques enabled") 
    print(f"⏱️ Setiap session aktif 2-10 menit")
    print(f"💻 Multiple browser profiles akan dibuat")
    print(f"📈 Bypass login problem dengan teknik advanced!")
    
    confirm = input(f"\n🚀 Lanjutkan dengan Advanced Session Manager? (y/n): ").lower()
    if confirm != 'y':
        print("👋 Proses dibatalkan!")
        return
    
    # Run advanced session manager
    try:
        manager.run_advanced_session_bot(session_id, num_sessions)
    except KeyboardInterrupt:
        print("\n⚠️ Bot dihentikan oleh user!")
        manager.running = False
    
    print("\n💡 Tips untuk meningkatkan success rate:")
    print("- Gunakan undetected-chromedriver: pip install undetected-chromedriver")
    print("- Run saat traffic rendah (malam hari)")
    print("- Gunakan VPN berbeda untuk setiap session")
    print("- Pastikan Chrome version up-to-date")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
