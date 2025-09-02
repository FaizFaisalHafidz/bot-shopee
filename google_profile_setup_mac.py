#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google Profile Setup Tool - Mac Version
Setup 100 Google profiles with persistent login sessions
"""

import csv
import os
import time
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class GoogleProfileSetup:
    def __init__(self, csv_file='accounts/google_accounts_100.csv'):
        self.csv_file = csv_file
        self.accounts = []
        self.setup_log = []
        self.load_accounts()
        
    def load_accounts(self):
        """Load accounts from CSV"""
        try:
            if not os.path.exists(self.csv_file):
                print(f"❌ CSV file not found: {self.csv_file}")
                return
                
            with open(self.csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                self.accounts = [row for row in reader]
                
            print(f"✅ Loaded {len(self.accounts)} Google accounts")
            
        except Exception as e:
            print(f"❌ Error loading accounts: {e}")
    
    def create_chrome_profile(self, account, profile_id):
        """Create Chrome profile for specific account"""
        try:
            profile_name = f"{account['profile_name']}_profile_{profile_id}"
            profile_path = f"sessions/google_profiles/{profile_name}"
            
            # Create profile directory
            os.makedirs(profile_path, exist_ok=True)
            
            # Chrome options untuk Mac
            options = Options()
            options.add_argument(f"--user-data-dir={os.path.abspath(profile_path)}")
            options.add_argument("--profile-directory=Default")
            
            # Disable automation detection
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            # Window positioning
            x_offset = (profile_id % 4) * 350
            y_offset = (profile_id // 4) * 300
            options.add_argument(f"--window-position={x_offset},{y_offset}")
            options.add_argument("--window-size=800,600")
            
            # Use ChromeDriver
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            
            return driver, profile_path
            
        except Exception as e:
            print(f"❌ Error creating Chrome profile for {account['email']}: {e}")
            return None, None
    
    def setup_google_login(self, driver, account, profile_id):
        """Setup Google login in Chrome profile"""
        try:
            print(f"🔐 Setting up profile #{profile_id}: {account['email']}")
            
            # Go to Google login
            driver.get("https://accounts.google.com/signin")
            time.sleep(3)
            
            # Email input
            email_input = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.ID, "identifierId"))
            )
            email_input.clear()
            email_input.send_keys(account['email'])
            email_input.send_keys(Keys.ENTER)
            
            time.sleep(4)
            
            # Password input
            password_input = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.NAME, "password"))
            )
            password_input.clear()
            password_input.send_keys(account['password'])
            password_input.send_keys(Keys.ENTER)
            
            time.sleep(6)
            
            # Wait for manual intervention if needed (2FA, captcha, etc.)
            print(f"⏳ Waiting for login completion for {account['email']}")
            print("   If 2FA/Captcha appears, please complete manually...")
            
            # Wait up to 60 seconds for successful login
            for i in range(60):
                current_url = driver.current_url
                if "myaccount.google.com" in current_url or "accounts.google.com/ManageAccount" in current_url:
                    print(f"✅ Google login successful for {account['email']}")
                    return True
                elif "challenge" in current_url or "signin/v2/challenge" in current_url:
                    print(f"⚠️  2FA challenge detected for {account['email']}")
                    # Wait longer for manual completion
                    time.sleep(10)
                    continue
                else:
                    time.sleep(1)
            
            # Check final status
            if "google.com" in driver.current_url and "signin" not in driver.current_url:
                print(f"✅ Login completed for {account['email']}")
                return True
            else:
                print(f"❌ Login failed for {account['email']}")
                return False
                
        except Exception as e:
            print(f"❌ Error during Google login for {account['email']}: {e}")
            return False
    
    def verify_profile_session(self, driver, account):
        """Verify that Google session is persistent"""
        try:
            # Go to Google account page to verify login
            driver.get("https://myaccount.google.com")
            time.sleep(3)
            
            # Check if logged in
            if "myaccount.google.com" in driver.current_url:
                print(f"✅ Session verified for {account['email']}")
                return True
            else:
                print(f"❌ Session verification failed for {account['email']}")
                return False
                
        except Exception as e:
            print(f"❌ Error verifying session for {account['email']}: {e}")
            return False
    
    def setup_all_profiles(self):
        """Setup Google profiles for all accounts"""
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║            GOOGLE PROFILE SETUP - MAC VERSION             ║
╚══════════════════════════════════════════════════════════════╝

🎯 Setting up {len(self.accounts)} Google profiles
📁 Profile location: sessions/google_profiles/
⏰ Estimated time: {len(self.accounts) * 2} minutes

🔄 Starting profile setup...
""")
        
        successful_setups = 0
        failed_setups = 0
        
        for i, account in enumerate(self.accounts, 1):
            print(f"\n{'='*60}")
            print(f"Profile {i}/{len(self.accounts)}: {account['email']}")
            print(f"{'='*60}")
            
            # Create Chrome profile
            driver, profile_path = self.create_chrome_profile(account, i)
            
            if not driver:
                failed_setups += 1
                self.setup_log.append({
                    'email': account['email'],
                    'status': 'failed',
                    'error': 'Chrome profile creation failed',
                    'timestamp': datetime.now().isoformat()
                })
                continue
            
            try:
                # Setup Google login
                if self.setup_google_login(driver, account, i):
                    # Verify session
                    if self.verify_profile_session(driver, account):
                        successful_setups += 1
                        self.setup_log.append({
                            'email': account['email'],
                            'status': 'success',
                            'profile_path': profile_path,
                            'timestamp': datetime.now().isoformat()
                        })
                        
                        # Update CSV
                        account['setup_date'] = datetime.now().isoformat()
                        account['status'] = 'setup_complete'
                    else:
                        failed_setups += 1
                        self.setup_log.append({
                            'email': account['email'],
                            'status': 'failed',
                            'error': 'Session verification failed',
                            'timestamp': datetime.now().isoformat()
                        })
                else:
                    failed_setups += 1
                    self.setup_log.append({
                        'email': account['email'],
                        'status': 'failed',
                        'error': 'Google login failed',
                        'timestamp': datetime.now().isoformat()
                    })
                
                # Keep browser open for a moment to save session
                print(f"💾 Saving session for {account['email']}...")
                time.sleep(3)
                
            finally:
                # Close browser
                try:
                    driver.quit()
                except:
                    pass
            
            # Brief pause between setups
            if i < len(self.accounts):
                print("⏸️  Brief pause before next profile...")
                time.sleep(2)
        
        # Save results
        self.save_setup_results()
        
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║                    SETUP COMPLETE                          ║
╚══════════════════════════════════════════════════════════════╝

📊 Results:
   ✅ Successful: {successful_setups}
   ❌ Failed: {failed_setups}
   📁 Profiles saved in: sessions/google_profiles/

🎉 Google profiles are ready for Shopee bot!
""")
    
    def save_setup_results(self):
        """Save setup results to files"""
        # Update CSV
        try:
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as file:
                if self.accounts:
                    writer = csv.DictWriter(file, fieldnames=self.accounts[0].keys())
                    writer.writeheader()
                    writer.writerows(self.accounts)
        except Exception as e:
            print(f"❌ Error saving CSV: {e}")
        
        # Save setup log
        try:
            log_file = f"logs/google_setup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            os.makedirs('logs', exist_ok=True)
            with open(log_file, 'w', encoding='utf-8') as file:
                json.dump(self.setup_log, file, indent=2, ensure_ascii=False)
            print(f"📝 Setup log saved: {log_file}")
        except Exception as e:
            print(f"❌ Error saving log: {e}")

def main():
    """Main function"""
    print("🚀 Google Profile Setup Tool - Mac Version")
    
    setup = GoogleProfileSetup()
    
    if not setup.accounts:
        print("❌ No accounts found in CSV")
        return
    
    print(f"📋 Found {len(setup.accounts)} accounts to setup")
    
    confirm = input("\n🤔 Ready to setup Google profiles? This will take time. (y/N): ").strip().lower()
    
    if confirm != 'y':
        print("❌ Setup cancelled")
        return
    
    print("\n⚠️  IMPORTANT:")
    print("   - Chrome windows will open automatically")
    print("   - Complete any 2FA/Captcha manually when prompted")
    print("   - Do not close Chrome windows during setup")
    print("   - Each profile will be saved automatically")
    
    input("\nPress Enter to start setup...")
    
    setup.setup_all_profiles()

if __name__ == "__main__":
    main()
