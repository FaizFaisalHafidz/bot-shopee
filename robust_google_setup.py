#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Robust Google Profile Setup - Multi RDP Support
Handles 100+ accounts across 6 RDP sessions with proper button clicking
"""

import csv
import os
import time
import json
import random
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

class RobustGoogleSetup:
    def __init__(self, csv_file='accounts/google_accounts_100.csv'):
        self.csv_file = csv_file
        self.accounts = []
        self.setup_log = []
        self.chrome_options = self.get_stable_chrome_options()
        self.load_accounts()
        
    def get_stable_chrome_options(self):
        """Get stable Chrome options to prevent crashes"""
        options = Options()
        
        # Stability options
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--disable-background-timer-throttling")
        options.add_argument("--disable-renderer-backgrounding")
        options.add_argument("--disable-backgrounding-occluded-windows")
        
        # Memory management
        options.add_argument("--max_old_space_size=4096")
        options.add_argument("--memory-pressure-off")
        
        # Anti-detection
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # User agent
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        # Disable features that can cause crashes
        options.add_argument("--disable-features=VizDisplayCompositor")
        options.add_argument("--disable-ipc-flooding-protection")
        
        return options
        
    def load_accounts(self):
        """Load accounts from CSV"""
        try:
            if not os.path.exists(self.csv_file):
                print(f"❌ CSV file not found: {self.csv_file}")
                return
                
            with open(self.csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                # Filter only active accounts
                self.accounts = [row for row in reader if row['status'] == 'active' and row['email'].strip()]
                
            print(f"✅ Loaded {len(self.accounts)} active Google accounts")
            
        except Exception as e:
            print(f"❌ Error loading accounts: {e}")
    
    def create_stable_chrome(self, account, profile_id):
        """Create stable Chrome instance with error handling"""
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                profile_name = f"{account['profile_name']}_profile_{profile_id}"
                profile_path = os.path.abspath(f"sessions/google_profiles/{profile_name}")
                
                # Create profile directory
                os.makedirs(profile_path, exist_ok=True)
                
                # Clone base options and add profile
                options = Options()
                for arg in self.chrome_options.arguments:
                    options.add_argument(arg)
                for name, value in self.chrome_options.experimental_options.items():
                    options.add_experimental_option(name, value)
                
                # Profile settings
                options.add_argument(f"--user-data-dir={profile_path}")
                options.add_argument("--profile-directory=Default")
                
                # Window positioning for multiple RDP sessions
                rdp_session = profile_id % 6  # Distribute across 6 RDP
                x_base = (rdp_session % 3) * 400
                y_base = (rdp_session // 3) * 350
                x_offset = x_base + ((profile_id // 6) % 2) * 200
                y_offset = y_base + ((profile_id // 6) // 2) * 200
                
                options.add_argument(f"--window-position={x_offset},{y_offset}")
                options.add_argument("--window-size=800,700")
                
                # Create service with timeout
                service = Service(ChromeDriverManager().install())
                service.creation_timeout = 30
                
                # Create driver with timeout
                driver = webdriver.Chrome(service=service, options=options)
                driver.set_page_load_timeout(30)
                driver.implicitly_wait(10)
                
                # Anti-detection JavaScript
                driver.execute_script("""
                    Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                    Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
                    Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
                """)
                
                print(f"✅ Chrome created for profile #{profile_id} (RDP #{rdp_session + 1})")
                return driver, profile_path
                
            except Exception as e:
                print(f"⚠️  Chrome creation attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(5)
                    continue
                else:
                    print(f"❌ Failed to create Chrome after {max_retries} attempts")
                    return None, None
    
    def robust_google_login(self, driver, account, profile_id):
        """Robust Google login with proper button clicking"""
        try:
            print(f"🔐 Starting login for profile #{profile_id}: {account['email']}")
            
            # Step 1: Navigate to Google signin
            driver.get("https://accounts.google.com/signin/v2/identifier?hl=en")
            time.sleep(3)
            
            # Step 2: Handle "Use another account" if needed
            try:
                use_another_btns = driver.find_elements(By.XPATH, "//div[contains(text(), 'Use another account') or contains(text(), 'Add account')]")
                if use_another_btns:
                    print(f"   Clicking 'Use another account'...")
                    use_another_btns[0].click()
                    time.sleep(2)
            except:
                pass
            
            # Step 3: Email input with multiple selectors
            email_selectors = [
                "identifierId",
                "Email",
                "input[type='email']",
                "input[name='identifier']"
            ]
            
            email_input = None
            for selector in email_selectors:
                try:
                    if selector.startswith("input"):
                        email_input = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                        )
                    else:
                        email_input = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.ID, selector))
                        )
                    break
                except:
                    continue
            
            if not email_input:
                print(f"❌ Could not find email input for {account['email']}")
                return False
            
            # Clear and enter email
            email_input.clear()
            time.sleep(0.5)
            for char in account['email']:
                email_input.send_keys(char)
                time.sleep(0.05)  # Human-like typing
            
            print(f"   ✅ Email entered: {account['email']}")
            time.sleep(1)
            
            # Step 4: Click Next button (multiple selectors)
            next_selectors = [
                "identifierNext",
                "//span[text()='Next']",
                "//button[contains(@id, 'Next')]",
                "//div[@role='button'][contains(text(), 'Next')]",
                "button[type='submit']",
                "input[type='submit']"
            ]
            
            next_clicked = False
            for selector in next_selectors:
                try:
                    if selector.startswith("//"):
                        next_btn = driver.find_element(By.XPATH, selector)
                    elif selector.startswith("button") or selector.startswith("input"):
                        next_btn = driver.find_element(By.CSS_SELECTOR, selector)
                    else:
                        next_btn = driver.find_element(By.ID, selector)
                    
                    # Ensure button is clickable
                    WebDriverWait(driver, 5).until(EC.element_to_be_clickable(next_btn))
                    next_btn.click()
                    next_clicked = True
                    print(f"   ✅ 'Next' button clicked")
                    break
                except:
                    continue
            
            if not next_clicked:
                # Fallback: Press Enter
                email_input.send_keys(Keys.ENTER)
                print(f"   ⚠️  Used Enter key fallback")
            
            time.sleep(4)
            
            # Step 5: Password input with multiple selectors
            password_selectors = [
                "password",
                "Passwd",
                "input[type='password']",
                "input[name='password']"
            ]
            
            password_input = None
            for selector in password_selectors:
                try:
                    if selector.startswith("input"):
                        password_input = WebDriverWait(driver, 15).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                        )
                    else:
                        password_input = WebDriverWait(driver, 15).until(
                            EC.presence_of_element_located((By.ID, selector))
                        )
                    break
                except:
                    continue
            
            if not password_input:
                print(f"❌ Could not find password input for {account['email']}")
                return False
            
            # Clear and enter password
            password_input.clear()
            time.sleep(0.5)
            for char in account['password']:
                password_input.send_keys(char)
                time.sleep(0.05)  # Human-like typing
            
            print(f"   ✅ Password entered")
            time.sleep(1)
            
            # Step 6: Click Password Next button
            pwd_next_selectors = [
                "passwordNext",
                "//span[text()='Next']",
                "//button[contains(@id, 'passwordNext')]",
                "//div[@role='button'][contains(text(), 'Next')]"
            ]
            
            pwd_next_clicked = False
            for selector in pwd_next_selectors:
                try:
                    if selector.startswith("//"):
                        pwd_next_btn = driver.find_element(By.XPATH, selector)
                    else:
                        pwd_next_btn = driver.find_element(By.ID, selector)
                    
                    WebDriverWait(driver, 5).until(EC.element_to_be_clickable(pwd_next_btn))
                    pwd_next_btn.click()
                    pwd_next_clicked = True
                    print(f"   ✅ Password 'Next' button clicked")
                    break
                except:
                    continue
            
            if not pwd_next_clicked:
                # Fallback: Press Enter
                password_input.send_keys(Keys.ENTER)
                print(f"   ⚠️  Used Enter key fallback for password")
            
            time.sleep(5)
            
            # Step 7: Handle 2FA/Recovery if appears
            recovery_handled = self.handle_verification_challenges(driver, account)
            
            # Step 8: Wait for login completion with extended timeout
            print(f"   ⏳ Waiting for login completion...")
            
            success_indicators = [
                "myaccount.google.com",
                "accounts.google.com/ManageAccount",
                "accounts.google.com/b/0/ManageAccount"
            ]
            
            for i in range(60):  # 60 seconds timeout
                try:
                    current_url = driver.current_url.lower()
                    page_title = driver.title.lower()
                    
                    # Check for success indicators
                    if any(indicator in current_url for indicator in success_indicators):
                        print(f"   ✅ Login successful! URL: {current_url}")
                        return True
                    
                    # Check for additional challenges
                    elif "challenge" in current_url or "verify" in current_url:
                        print(f"   ⚠️  Additional verification required...")
                        if not recovery_handled:
                            self.handle_verification_challenges(driver, account)
                        time.sleep(5)
                        continue
                    
                    # Check page content for success
                    elif "google account" in page_title or "my account" in page_title:
                        print(f"   ✅ Login successful via page title!")
                        return True
                    
                    else:
                        time.sleep(1)
                        
                except Exception as e:
                    print(f"   Checking status... ({i+1}/60)")
                    time.sleep(1)
            
            # Final verification attempt
            try:
                current_url = driver.current_url
                if "accounts.google.com" in current_url and "signin" not in current_url:
                    print(f"   ✅ Login appears successful!")
                    return True
                else:
                    print(f"   ❌ Login timeout. Final URL: {current_url}")
                    return False
            except:
                print(f"   ❌ Could not verify final login status")
                return False
                
        except Exception as e:
            print(f"❌ Login error for {account['email']}: {e}")
            return False
    
    def handle_verification_challenges(self, driver, account):
        """Handle 2FA, recovery, captcha etc."""
        try:
            current_url = driver.current_url.lower()
            page_source = driver.page_source.lower()
            
            # Handle different verification types
            if "challenge" in current_url or "verify" in current_url:
                print(f"   🔐 Verification challenge detected")
                
                # Try to handle recovery questions
                try:
                    recovery_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='text'], input[type='tel']")
                    if recovery_inputs:
                        print(f"   ❓ Recovery question/phone detected - manual intervention needed")
                        return False
                except:
                    pass
                
                # Handle phone verification
                try:
                    phone_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'phone') or contains(text(), 'SMS')]")
                    if phone_elements:
                        print(f"   📱 Phone verification required - manual intervention needed")
                        return False
                except:
                    pass
                
                # Try clicking continue/skip buttons
                try:
                    continue_btns = driver.find_elements(By.XPATH, "//span[text()='Continue'] | //span[text()='Skip'] | //span[text()='Next']")
                    if continue_btns:
                        continue_btns[0].click()
                        print(f"   ✅ Clicked continue/skip button")
                        time.sleep(3)
                        return True
                except:
                    pass
            
            return False
            
        except Exception as e:
            print(f"   Error handling verification: {e}")
            return False
    
    def verify_login_success(self, driver, account):
        """Comprehensive login verification"""
        try:
            print(f"   🔍 Verifying login success...")
            
            # Navigate to account page
            driver.get("https://myaccount.google.com")
            time.sleep(5)
            
            # Multiple verification methods
            current_url = driver.current_url.lower()
            page_title = driver.title.lower()
            
            success_checks = [
                "myaccount.google.com" in current_url,
                "google account" in page_title,
                "my account" in page_title
            ]
            
            if any(success_checks):
                print(f"   ✅ Login verified successfully!")
                
                # Additional check - look for account info
                try:
                    profile_elements = driver.find_elements(By.XPATH, "//*[contains(@aria-label, 'Account') or contains(text(), 'Account')]")
                    if profile_elements:
                        print(f"   ✅ Account profile confirmed")
                except:
                    pass
                    
                return True
            else:
                print(f"   ❌ Login verification failed")
                print(f"      URL: {current_url}")
                print(f"      Title: {page_title}")
                return False
                
        except Exception as e:
            print(f"   ❌ Error during verification: {e}")
            return False
    
    def setup_accounts_batch(self, start_index=0, batch_size=10):
        """Setup accounts in batches for RDP stability"""
        if not self.accounts:
            print("❌ No accounts to setup")
            return
        
        total_accounts = len(self.accounts)
        end_index = min(start_index + batch_size, total_accounts)
        batch_accounts = self.accounts[start_index:end_index]
        
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║               ROBUST GOOGLE PROFILE SETUP                 ║
╚══════════════════════════════════════════════════════════════╝

🎯 Batch Setup: {start_index + 1} to {end_index} of {total_accounts}
📊 Batch Size: {len(batch_accounts)} accounts
🖥️  RDP Distribution: Across 6 RDP sessions
⏰ Estimated time: {len(batch_accounts) * 3} minutes

🔄 Starting batch setup...
""")
        
        successful_setups = 0
        failed_setups = 0
        
        for i, account in enumerate(batch_accounts):
            profile_id = start_index + i + 1
            
            print(f"\n{'='*70}")
            print(f"Account {profile_id}/{total_accounts}: {account['email']}")
            print(f"RDP Session: #{(profile_id % 6) + 1}")
            print(f"{'='*70}")
            
            # Create Chrome instance
            driver, profile_path = self.create_stable_chrome(account, profile_id)
            
            if not driver:
                failed_setups += 1
                self.log_setup_result(account, 'failed', 'Chrome creation failed')
                continue
            
            try:
                # Attempt Google login
                if self.robust_google_login(driver, account, profile_id):
                    # Extended session save time
                    print(f"   💾 Saving profile session...")
                    time.sleep(5)
                    
                    # Verify login
                    if self.verify_login_success(driver, account):
                        successful_setups += 1
                        self.log_setup_result(account, 'success', None, profile_path)
                        
                        # Update CSV
                        account['setup_date'] = datetime.now().isoformat()
                        account['status'] = 'setup_complete'
                        
                        print(f"   🎉 Profile #{profile_id} setup complete!")
                    else:
                        failed_setups += 1
                        self.log_setup_result(account, 'failed', 'Session verification failed')
                else:
                    failed_setups += 1
                    self.log_setup_result(account, 'failed', 'Google login failed')
                
            finally:
                # Cleanup browser
                try:
                    driver.quit()
                    print(f"   🧹 Browser cleanup complete")
                except:
                    pass
            
            # Pause between accounts for stability
            if profile_id < total_accounts:
                pause_time = random.randint(2, 5)
                print(f"   ⏸️  Stability pause: {pause_time}s...")
                time.sleep(pause_time)
        
        # Save results
        self.save_setup_results()
        
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║                   BATCH SETUP COMPLETE                    ║
╚══════════════════════════════════════════════════════════════╝

📊 Batch Results:
   ✅ Successful: {successful_setups}
   ❌ Failed: {failed_setups}
   📁 Profiles: sessions/google_profiles/
   
🎯 Progress: {end_index}/{total_accounts} accounts processed
""")
        
        # Ask for next batch
        if end_index < total_accounts:
            remaining = total_accounts - end_index
            print(f"💡 {remaining} accounts remaining")
            continue_batch = input(f"\nContinue with next batch? (y/N): ").strip().lower()
            if continue_batch == 'y':
                time.sleep(10)  # Longer pause between batches
                self.setup_accounts_batch(end_index, batch_size)
    
    def log_setup_result(self, account, status, error=None, profile_path=None):
        """Log setup result"""
        self.setup_log.append({
            'email': account['email'],
            'status': status,
            'error': error,
            'profile_path': profile_path,
            'timestamp': datetime.now().isoformat()
        })
    
    def save_setup_results(self):
        """Save results to files"""
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
            log_file = f"logs/robust_google_setup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            os.makedirs('logs', exist_ok=True)
            with open(log_file, 'w', encoding='utf-8') as file:
                json.dump(self.setup_log, file, indent=2, ensure_ascii=False)
            print(f"📝 Setup log saved: {log_file}")
        except Exception as e:
            print(f"❌ Error saving log: {e}")

def main():
    """Main function"""
    print("🚀 Robust Google Profile Setup - Multi RDP Support")
    
    setup = RobustGoogleSetup()
    
    if not setup.accounts:
        print("❌ No accounts found in CSV")
        return
    
    total_accounts = len(setup.accounts)
    print(f"📋 Found {total_accounts} accounts to setup")
    
    # Batch configuration
    print(f"""
🎛️  BATCH CONFIGURATION:
   └─ Total Accounts: {total_accounts}
   └─ RDP Sessions: 6 (accounts distributed automatically)
   └─ Recommended Batch Size: 10-20 accounts per batch
   └─ Chrome Stability: Enhanced anti-crash measures
""")
    
    batch_size = input(f"Batch size (1-{total_accounts}, default 10): ").strip()
    try:
        batch_size = int(batch_size) if batch_size else 10
        batch_size = max(1, min(batch_size, total_accounts))
    except:
        batch_size = 10
    
    start_index = input(f"Start from account # (1-{total_accounts}, default 1): ").strip()
    try:
        start_index = int(start_index) - 1 if start_index else 0
        start_index = max(0, min(start_index, total_accounts - 1))
    except:
        start_index = 0
    
    print(f"""
🎯 SETUP CONFIGURATION:
   └─ Starting from: Account #{start_index + 1}
   └─ Batch size: {batch_size}
   └─ RDP distribution: Automatic across 6 sessions
""")
    
    confirm = input("\n🤔 Start Google profile setup? (y/N): ").strip().lower()
    
    if confirm != 'y':
        print("❌ Setup cancelled")
        return
    
    print("\n⚠️  IMPORTANT FOR RDP:")
    print("   - Keep RDP connections stable")
    print("   - Complete 2FA manually when prompted")
    print("   - Chrome windows will open across RDP sessions")
    print("   - Process can be resumed if interrupted")
    
    input("\nPress Enter to start robust setup...")
    
    setup.setup_accounts_batch(start_index, batch_size)

if __name__ == "__main__":
    main()
