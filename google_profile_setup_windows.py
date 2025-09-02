#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google Profile Setup Tool - Windows Version
Setup 100 Google profiles menggunakan Chrome real (bukan Chromium)
"""

import csv
import os
import time
import json
import subprocess
import winreg
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class GoogleProfileSetupWindows:
    def __init__(self, csv_file='accounts/google_accounts_100.csv'):
        self.csv_file = csv_file
        self.accounts = []
        self.setup_log = []
        self.chrome_path = self.find_chrome_path()
        self.load_accounts()
        
    def find_chrome_path(self):
        """Find Chrome installation path di Windows"""
        possible_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            r"C:\Users\%USERNAME%\AppData\Local\Google\Chrome\Application\chrome.exe"
        ]
        
        for path in possible_paths:
            expanded_path = os.path.expandvars(path)
            if os.path.exists(expanded_path):
                print(f"✅ Found Chrome: {expanded_path}")
                return expanded_path
        
        # Try registry
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe")
            path = winreg.QueryValue(key, "")
            winreg.CloseKey(key)
            if os.path.exists(path):
                print(f"✅ Found Chrome in registry: {path}")
                return path
        except:
            pass
        
        print("❌ Chrome not found! Please install Chrome first.")
        return None
        
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
    
    def create_chrome_profile_windows(self, account, profile_id):
        """Create Chrome profile menggunakan Chrome real di Windows"""
        try:
            if not self.chrome_path:
                return None
                
            profile_name = f"{account['profile_name']}_profile_{profile_id}"
            profile_path = os.path.abspath(f"sessions\\google_profiles\\{profile_name}")
            
            # Create profile directory
            os.makedirs(profile_path, exist_ok=True)
            
            # Chrome options untuk Windows dengan real Chrome
            options = Options()
            options.binary_location = self.chrome_path
            options.add_argument(f"--user-data-dir={profile_path}")
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
            
            # Additional Windows-specific options
            options.add_argument("--no-first-run")
            options.add_argument("--no-default-browser-check")
            options.add_argument("--disable-default-apps")
            
            # Use ChromeDriver dengan real Chrome
            service = Service()  # Will use PATH or download
            driver = webdriver.Chrome(service=service, options=options)
            
            # Set additional properties
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            return driver, profile_path
            
        except Exception as e:
            print(f"❌ Error creating Chrome profile for {account['email']}: {e}")
            return None, None
    
    def setup_google_login_windows(self, driver, account, profile_id):
        """Setup Google login dengan handling Windows-specific issues"""
        try:
            print(f"🔐 Setting up Windows profile #{profile_id}: {account['email']}")
            
            # Go to Google login
            driver.get("https://accounts.google.com/signin")
            time.sleep(4)
            
            # Handle potential popups
            try:
                # Check for "Use another account" if needed
                use_another = driver.find_elements(By.XPATH, "//div[contains(text(), 'Use another account')]")
                if use_another:
                    use_another[0].click()
                    time.sleep(2)
            except:
                pass
            
            # Email input
            email_input = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "identifierId"))
            )
            email_input.clear()
            email_input.send_keys(account['email'])
            
            # Click Next button
            next_button = driver.find_element(By.ID, "identifierNext")
            next_button.click()
            
            time.sleep(5)
            
            # Password input
            password_input = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.NAME, "password"))
            )
            password_input.clear()
            password_input.send_keys(account['password'])
            
            # Click Next button
            password_next = driver.find_element(By.ID, "passwordNext")
            password_next.click()
            
            time.sleep(8)
            
            # Wait for manual intervention if needed
            print(f"⏳ Waiting for login completion for {account['email']}")
            print("   Please complete any 2FA/Captcha manually if appears...")
            
            # Extended wait for Windows (slower)
            for i in range(90):  # 90 seconds
                try:
                    current_url = driver.current_url
                    page_source = driver.page_source.lower()
                    
                    if ("myaccount.google.com" in current_url or 
                        "accounts.google.com" in current_url and "signin" not in current_url or
                        "google account" in page_source):
                        print(f"✅ Google login successful for {account['email']}")
                        return True
                    elif "challenge" in current_url or "verify" in current_url:
                        print(f"⚠️  Verification challenge for {account['email']} - please complete manually")
                        time.sleep(5)
                        continue
                    else:
                        time.sleep(2)
                        
                except Exception as check_error:
                    print(f"   Checking login status... ({i+1}/90)")
                    time.sleep(1)
            
            # Final check
            try:
                current_url = driver.current_url
                if "google.com" in current_url and "signin" not in current_url:
                    print(f"✅ Login appears successful for {account['email']}")
                    return True
                else:
                    print(f"❌ Login failed for {account['email']} - final URL: {current_url}")
                    return False
            except:
                print(f"❌ Could not verify login for {account['email']}")
                return False
                
        except Exception as e:
            print(f"❌ Error during Google login for {account['email']}: {e}")
            return False
    
    def verify_profile_session_windows(self, driver, account):
        """Verify Google session with Windows-specific checks"""
        try:
            print(f"🔍 Verifying session for {account['email']}")
            
            # Go to Google account page
            driver.get("https://myaccount.google.com")
            time.sleep(5)
            
            # Multiple verification methods
            current_url = driver.current_url
            page_title = driver.title.lower()
            
            if ("myaccount.google.com" in current_url or 
                "google account" in page_title or
                "my account" in page_title):
                print(f"✅ Session verified for {account['email']}")
                
                # Additional verification - check for profile info
                try:
                    profile_elements = driver.find_elements(By.XPATH, "//*[contains(@aria-label, 'Account') or contains(text(), 'Account')]")
                    if profile_elements:
                        print(f"✅ Profile data confirmed for {account['email']}")
                except:
                    pass
                    
                return True
            else:
                print(f"❌ Session verification failed for {account['email']}")
                print(f"   Current URL: {current_url}")
                print(f"   Page title: {page_title}")
                return False
                
        except Exception as e:
            print(f"❌ Error verifying session for {account['email']}: {e}")
            return False
    
    def setup_all_profiles_windows(self):
        """Setup all Google profiles for Windows"""
        if not self.chrome_path:
            print("❌ Chrome not found. Please install Chrome first.")
            return
            
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║           GOOGLE PROFILE SETUP - WINDOWS VERSION           ║
╚══════════════════════════════════════════════════════════════╝

🎯 Setting up {len(self.accounts)} Google profiles
🌐 Using Chrome: {self.chrome_path}
📁 Profile location: sessions/google_profiles/
⏰ Estimated time: {len(self.accounts) * 3} minutes

🔄 Starting Windows profile setup...
""")
        
        successful_setups = 0
        failed_setups = 0
        
        for i, account in enumerate(self.accounts, 1):
            print(f"\n{'='*70}")
            print(f"Windows Profile {i}/{len(self.accounts)}: {account['email']}")
            print(f"{'='*70}")
            
            # Create Chrome profile
            driver, profile_path = self.create_chrome_profile_windows(account, i)
            
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
                if self.setup_google_login_windows(driver, account, i):
                    # Extended wait for Windows session save
                    print(f"💾 Saving Windows session for {account['email']}...")
                    time.sleep(5)
                    
                    # Verify session
                    if self.verify_profile_session_windows(driver, account):
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
                
            finally:
                # Close browser with Windows-specific handling
                try:
                    driver.quit()
                    time.sleep(2)  # Extra wait for Windows
                except Exception as quit_error:
                    print(f"⚠️  Browser cleanup issue: {quit_error}")
            
            # Longer pause for Windows stability
            if i < len(self.accounts):
                print("⏸️  Windows pause before next profile...")
                time.sleep(3)
        
        # Save results
        self.save_setup_results()
        
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║                 WINDOWS SETUP COMPLETE                     ║
╚══════════════════════════════════════════════════════════════╝

📊 Results:
   ✅ Successful: {successful_setups}
   ❌ Failed: {failed_setups}
   📁 Profiles saved in: sessions/google_profiles/

🎉 Google profiles ready for Windows Shopee bot!
""")
    
    def save_setup_results(self):
        """Save setup results"""
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
            log_file = f"logs/google_setup_windows_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            os.makedirs('logs', exist_ok=True)
            with open(log_file, 'w', encoding='utf-8') as file:
                json.dump(self.setup_log, file, indent=2, ensure_ascii=False)
            print(f"📝 Setup log saved: {log_file}")
        except Exception as e:
            print(f"❌ Error saving log: {e}")

def main():
    """Main function for Windows"""
    print("🚀 Google Profile Setup Tool - Windows Version")
    
    setup = GoogleProfileSetupWindows()
    
    if not setup.accounts:
        print("❌ No accounts found in CSV")
        return
    
    if not setup.chrome_path:
        print("❌ Chrome not found. Please install Chrome first.")
        return
    
    print(f"📋 Found {len(setup.accounts)} accounts to setup")
    print(f"🌐 Using Chrome: {setup.chrome_path}")
    
    confirm = input("\n🤔 Ready to setup Google profiles on Windows? (y/N): ").strip().lower()
    
    if confirm != 'y':
        print("❌ Setup cancelled")
        return
    
    print("\n⚠️  WINDOWS SETUP NOTES:")
    print("   - Real Chrome will open (not Chromium)")
    print("   - Complete 2FA/Captcha manually when prompted")
    print("   - Each profile saves to separate folder")
    print("   - Process may take longer on Windows")
    print("   - Keep RDP connection stable during setup")
    
    input("\nPress Enter to start Windows setup...")
    
    setup.setup_all_profiles_windows()

if __name__ == "__main__":
    main()
