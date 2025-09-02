#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shopee Live Bot dengan Pre-setup Google Profiles
Menggunakan Google profiles yang sudah login
"""

import os
import time
import threading
import csv
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/shopee_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ProfileBasedViewer:
    """Shopee viewer menggunakan pre-setup Google profile"""
    
    def __init__(self, viewer_id, session_id, account):
        self.viewer_id = viewer_id
        self.session_id = session_id
        self.account = account
        self.driver = None
        self.is_running = False
        
        # Profile path
        self.profile_path = os.path.join(
            "sessions/google_profiles", 
            f"{account['profile_name']}_profile"
        )
        
    def check_profile_exists(self):
        """Check if Google profile exists"""
        exists = os.path.exists(self.profile_path)
        logger.info(f"👁️  Viewer #{self.viewer_id} - Profile exists: {exists}")
        return exists
    
    def create_chrome_with_profile(self):
        """Create Chrome menggunakan existing Google profile"""
        try:
            if not self.check_profile_exists():
                logger.error(f"❌ Profile not found for viewer #{self.viewer_id}: {self.profile_path}")
                return False
            
            options = Options()
            
            # Use existing profile
            options.add_argument(f"--user-data-dir={self.profile_path}")
            options.add_argument("--profile-directory=Default")
            
            # Anti-detection
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            # Window positioning
            x_offset = (self.viewer_id - 1) * 300
            y_offset = (self.viewer_id - 1) * 100
            options.add_argument(f"--window-position={x_offset},{y_offset}")
            options.add_argument("--window-size=800,600")
            
            # Performance
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            
            # Anti-detection script
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            logger.info(f"🌐 Chrome started for viewer #{self.viewer_id} with existing Google profile")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to create Chrome for viewer #{self.viewer_id}: {e}")
            return False
    
    def verify_google_login(self):
        """Verify Google masih login di profile"""
        try:
            logger.info(f"🔐 Verifying Google login for viewer #{self.viewer_id}")
            
            self.driver.get("https://myaccount.google.com/")
            time.sleep(5)
            
            current_url = self.driver.current_url
            page_title = self.driver.title.lower()
            
            # Check if logged in
            if "myaccount.google.com" in current_url or "google account" in page_title:
                logger.info(f"✅ Google login verified for viewer #{self.viewer_id}")
                return True
            else:
                logger.warning(f"⚠️ Google login uncertain for viewer #{self.viewer_id}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error verifying Google login for viewer #{self.viewer_id}: {e}")
            return False
    
    def shopee_oauth_login(self):
        """Login ke Shopee menggunakan Google OAuth"""
        try:
            logger.info(f"🛍️ Starting Shopee OAuth login for viewer #{self.viewer_id}")
            
            self.driver.get("https://shopee.co.id/buyer/login")
            time.sleep(3)
            
            # Find and click Google login button
            try:
                # Try different selectors for Google button
                google_selectors = [
                    "//button[contains(@class, 'google')]",
                    "//div[contains(@class, 'google')]//button",
                    "//button[contains(text(), 'Google')]",
                    "//div[contains(text(), 'Google')]",
                    "//*[contains(@class, 'social')]//button[1]"
                ]
                
                google_btn = None
                for selector in google_selectors:
                    try:
                        google_btn = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                        break
                    except TimeoutException:
                        continue
                
                if not google_btn:
                    logger.error(f"❌ Google login button not found for viewer #{self.viewer_id}")
                    return False
                
                google_btn.click()
                logger.info(f"🔘 Clicked Google login button for viewer #{self.viewer_id}")
                time.sleep(5)
                
            except Exception as e:
                logger.error(f"❌ Error clicking Google button for viewer #{self.viewer_id}: {e}")
                return False
            
            # Handle account selection if appears
            try:
                # Look for account selection page
                time.sleep(3)
                account_elements = self.driver.find_elements(By.XPATH, "//*[contains(@data-email, '@') or contains(text(), '@')]")
                
                if account_elements:
                    logger.info(f"🔍 Account selection found for viewer #{self.viewer_id}")
                    # Click first account or matching account
                    account_elements[0].click()
                    time.sleep(3)
                    
            except Exception as e:
                logger.info(f"ℹ️ No account selection needed for viewer #{self.viewer_id}")
            
            # Verify Shopee login success
            time.sleep(5)
            current_url = self.driver.current_url
            
            if "shopee.co.id" in current_url and "login" not in current_url:
                logger.info(f"✅ Shopee OAuth successful for viewer #{self.viewer_id}")
                return True
            elif "shopee.co.id" in current_url:
                logger.info(f"🔄 Shopee OAuth in progress for viewer #{self.viewer_id}")
                return True
            else:
                logger.warning(f"⚠️ Shopee OAuth result unclear for viewer #{self.viewer_id}")
                return True  # Continue anyway
                
        except Exception as e:
            logger.error(f"❌ Shopee OAuth error for viewer #{self.viewer_id}: {e}")
            return False
    
    def join_live_session(self):
        """Join Shopee live streaming session"""
        try:
            live_url = f"https://live.shopee.co.id/{self.session_id}"
            logger.info(f"📺 Joining live session for viewer #{self.viewer_id}")
            
            self.driver.get(live_url)
            time.sleep(10)
            
            # Check if successfully joined
            current_url = self.driver.current_url
            if str(self.session_id) in current_url:
                logger.info(f"✅ Successfully joined live session - viewer #{self.viewer_id}")
                return True
            else:
                logger.warning(f"⚠️ Live session join result unclear for viewer #{self.viewer_id}")
                return True
                
        except Exception as e:
            logger.error(f"❌ Live session error for viewer #{self.viewer_id}: {e}")
            return False
    
    def simulate_activity(self):
        """Simulate viewer activity"""
        try:
            activity_count = 0
            while self.is_running:
                # Random scroll
                scroll_amount = 100 + (self.viewer_id * 20)
                self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                
                activity_count += 1
                if activity_count % 10 == 0:
                    logger.info(f"📊 Viewer #{self.viewer_id} - Activity count: {activity_count}")
                
                # Staggered sleep
                sleep_time = 25 + (self.viewer_id * 5)
                time.sleep(sleep_time)
                
        except Exception as e:
            logger.error(f"❌ Activity simulation error for viewer #{self.viewer_id}: {e}")
    
    def start(self):
        """Start complete viewer process"""
        try:
            self.is_running = True
            
            # Step 1: Create Chrome with existing profile
            if not self.create_chrome_with_profile():
                return False
            
            # Step 2: Verify Google login
            if not self.verify_google_login():
                logger.warning(f"⚠️ Google verification failed for viewer #{self.viewer_id}, continuing...")
            
            # Step 3: Shopee OAuth
            if not self.shopee_oauth_login():
                return False
            
            # Step 4: Join live session
            if not self.join_live_session():
                return False
            
            # Step 5: Start activity
            activity_thread = threading.Thread(target=self.simulate_activity)
            activity_thread.daemon = True
            activity_thread.start()
            
            logger.info(f"🎉 Viewer #{self.viewer_id} fully active!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Viewer #{self.viewer_id} failed to start: {e}")
            return False
    
    def stop(self):
        """Stop viewer"""
        self.is_running = False
        if self.driver:
            try:
                self.driver.quit()
                logger.info(f"🛑 Viewer #{self.viewer_id} stopped")
            except:
                pass

class ShopeeProfileBot:
    """Main bot using pre-setup Google profiles"""
    
    def __init__(self):
        self.accounts_file = "accounts/google_accounts.csv"
        self.accounts = []
        self.viewers = []
        self.load_accounts()
    
    def load_accounts(self):
        """Load accounts from CSV"""
        try:
            with open(self.accounts_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                self.accounts = [row for row in reader if row['status'] == 'active']
            
            logger.info(f"✅ Loaded {len(self.accounts)} accounts")
            
        except Exception as e:
            logger.error(f"❌ Error loading accounts: {e}")
    
    def check_profiles_ready(self):
        """Check if Google profiles are setup"""
        missing_profiles = []
        
        for account in self.accounts:
            profile_path = os.path.join("sessions/google_profiles", f"{account['profile_name']}_profile")
            if not os.path.exists(profile_path):
                missing_profiles.append(account['profile_name'])
        
        if missing_profiles:
            print(f"""
❌ MISSING GOOGLE PROFILES:

The following profiles need to be setup first:
{chr(10).join([f"   - {profile}" for profile in missing_profiles])}

🔧 Run this command to setup profiles:
   python google_profile_setup.py

⚠️ Cannot start bot without Google profiles!
""")
            return False
        
        return True
    
    def start_bot(self, session_id, num_viewers):
        """Start bot with specified number of viewers"""
        
        if not self.check_profiles_ready():
            return
        
        available_accounts = len(self.accounts)
        if num_viewers > available_accounts:
            logger.warning(f"⚠️ Requested {num_viewers} viewers, but only {available_accounts} profiles available")
            num_viewers = available_accounts
        
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║              SHOPEE LIVE BOT STARTING                      ║
╚══════════════════════════════════════════════════════════════╝

🎯 Session ID: {session_id}
👥 Viewers: {num_viewers}
📁 Using Pre-setup Google Profiles

🚀 Starting viewers...
""")
        
        # Create viewers
        for i in range(num_viewers):
            account = self.accounts[i]
            viewer = ProfileBasedViewer(i + 1, session_id, account)
            self.viewers.append(viewer)
        
        # Start viewers concurrently
        max_workers = min(len(self.viewers), 3)  # Limit concurrent starts
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(viewer.start): viewer for viewer in self.viewers}
            
            success_count = 0
            for future in as_completed(futures):
                viewer = futures[future]
                try:
                    if future.result():
                        success_count += 1
                except Exception as e:
                    logger.error(f"❌ Viewer {viewer.viewer_id} failed: {e}")
            
            logger.info(f"✅ Successfully started {success_count}/{len(self.viewers)} viewers")
            
            # Keep running
            try:
                while True:
                    time.sleep(60)
                    active_count = sum(1 for v in self.viewers if v.is_running)
                    logger.info(f"📊 Active viewers: {active_count}/{len(self.viewers)}")
                    
            except KeyboardInterrupt:
                logger.info("🛑 Stopping all viewers...")
                self.stop_all()
    
    def stop_all(self):
        """Stop all viewers"""
        for viewer in self.viewers:
            viewer.stop()
        logger.info("✅ All viewers stopped")

def main():
    bot = ShopeeProfileBot()
    
    if not bot.accounts:
        print("❌ No accounts found! Please check accounts/google_accounts.csv")
        return
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║              SHOPEE LIVE BOT (Profile-Based)               ║
╚══════════════════════════════════════════════════════════════╝

📊 Available Accounts: {len(bot.accounts)}
🔐 Using Pre-setup Google Profiles
📁 Profile Location: sessions/google_profiles/
""")
    
    # Get session ID
    session_id = input("🎯 Enter Shopee Live Session ID: ").strip()
    if not session_id:
        print("❌ Session ID required!")
        return
    
    # Get number of viewers  
    max_viewers = len(bot.accounts)
    viewer_input = input(f"👥 Number of viewers (max {max_viewers}): ").strip()
    
    try:
        num_viewers = int(viewer_input) if viewer_input else max_viewers
        num_viewers = min(num_viewers, max_viewers)
    except ValueError:
        num_viewers = max_viewers
    
    print(f"""
🚀 STARTING BOT:
   Session: {session_id}
   Viewers: {num_viewers}
   Method: Pre-setup Google Profiles

⏳ Launching in 3 seconds...
""")
    
    time.sleep(3)
    
    try:
        bot.start_bot(session_id, num_viewers)
    except KeyboardInterrupt:
        print("🛑 Bot stopped by user")

if __name__ == "__main__":
    main()
