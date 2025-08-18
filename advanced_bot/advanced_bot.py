#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced Shopee Live Bot - With Robust Authentication
Bypasses login detection and maintains persistent sessions
"""

import time
import random
import csv
import threading
import os
import sys
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    # Try different import paths
    try:
        from auth.shopee_auth import ShopeeAuth
        from utils.logger import BotLogger
    except ImportError:
        # Fallback to advanced_bot prefix
        from advanced_bot.auth.shopee_auth import ShopeeAuth
        from advanced_bot.utils.logger import BotLogger
except ImportError:
    print("❌ Missing dependencies! Installing required packages...")
    os.system("pip install undetected-chromedriver selenium requests")
    
    # Try imports again after installation
    try:
        from auth.shopee_auth import ShopeeAuth
        from utils.logger import BotLogger
    except ImportError:
        try:
            from advanced_bot.auth.shopee_auth import ShopeeAuth
            from advanced_bot.utils.logger import BotLogger
        except ImportError:
            print("❌ Could not import required modules!")
            print("💡 Make sure you're running from the advanced_bot directory")
            sys.exit(1)

class AdvancedShopeeBot:
    def __init__(self):
        self.accounts = []
        self.session_id = None
        self.running = False
        self.active_sessions = {}
        self.success_count = 0
        self.failure_count = 0
        
        # Initialize logger
        try:
            self.logger = BotLogger()
        except:
            self.logger = None
        
    def log(self, message, level="INFO"):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"
        print(formatted_message)
        
        if self.logger:
            if level == "ERROR":
                self.logger.error(message)
            elif level == "SUCCESS":
                self.logger.success(message)
            else:
                self.logger.info(message)
    
    def load_accounts(self, file_path="../input.csv"):
        """Load accounts from CSV file"""
        try:
            # Try different paths
            possible_paths = [
                file_path,
                "../input.csv",
                "../../input.csv",
                "input.csv"
            ]
            
            content = None
            used_path = None
            
            for path in possible_paths:
                try:
                    with open(path, 'r', encoding='utf-8') as file:
                        content = file.read().strip()
                        used_path = path
                        break
                except FileNotFoundError:
                    continue
            
            if not content:
                self.log("❌ File input.csv tidak ditemukan!", "ERROR")
                return False
            
            self.log(f"📁 Loading accounts from: {used_path}")
            
            lines = [line.strip() for line in content.split('\n') if line.strip()]
            
            for line_num, line in enumerate(lines, 1):
                if line.startswith('#'):
                    continue
                
                account = self.parse_cookie_line(line)
                if account:
                    self.accounts.append(account)
                    self.log(f"✅ Akun {len(self.accounts)}: {account['user_id'][:8]}... loaded")
                else:
                    self.log(f"⚠️  Baris {line_num}: Cookie tidak valid atau tidak lengkap")
            
            if len(self.accounts) == 0:
                self.log("❌ Tidak ada akun valid yang ditemukan!", "ERROR")
                return False
            
            self.log(f"✅ Berhasil memuat {len(self.accounts)} akun valid", "SUCCESS")
            return True
            
        except Exception as e:
            self.log(f"❌ Error loading accounts: {e}", "ERROR")
            return False
    
    def parse_cookie_line(self, cookie_string):
        """Parse cookie string into account object"""
        try:
            cookies = {}
            required_cookies = ['SPC_U', 'SPC_T_ID', 'csrftoken']
            
            # Parse cookies
            for cookie in cookie_string.split(';'):
                cookie = cookie.strip()
                if '=' in cookie:
                    name, value = cookie.split('=', 1)
                    cookies[name.strip()] = value.strip()
            
            # Check required cookies
            has_required = all(cookie in cookies for cookie in required_cookies)
            
            if not has_required:
                return None
            
            return {
                'cookies': cookies,
                'cookie_string': cookie_string,
                'user_id': cookies.get('SPC_U', ''),
                'token': cookies.get('SPC_T_ID', ''),
                'csrf': cookies.get('csrftoken', ''),
                'has_required_cookies': has_required
            }
            
        except Exception as e:
            self.log(f"❌ Error parsing cookie: {e}", "ERROR")
            return None
    
    def authenticate_and_join(self, account):
        """Authenticate account and join live stream"""
        auth = ShopeeAuth()
        success = False
        
        try:
            self.log(f"🔐 Authenticating {account['user_id'][:8]}...")
            
            # Authenticate account
            if auth.authenticate_account(account['cookie_string'], account['user_id']):
                self.log(f"✅ Authentication success for {account['user_id'][:8]}")
                
                # Navigate to live stream
                if auth.navigate_to_live_stream(self.session_id):
                    self.log(f"🎥 Successfully joined live stream: {account['user_id'][:8]}")
                    
                    # Keep session alive
                    keep_alive_time = random.randint(30, 180)  # 30s - 3 minutes
                    self.log(f"⏱️  Keeping session alive for {keep_alive_time}s...")
                    
                    time.sleep(keep_alive_time)
                    
                    self.success_count += 1
                    success = True
                else:
                    self.log(f"❌ Failed to join live stream: {account['user_id'][:8]}", "ERROR")
                    self.failure_count += 1
            else:
                self.log(f"❌ Authentication failed: {account['user_id'][:8]}", "ERROR")
                self.failure_count += 1
                
        except Exception as e:
            self.log(f"❌ Error with account {account['user_id'][:8]}: {e}", "ERROR")
            self.failure_count += 1
        finally:
            auth.cleanup()
        
        return success
    
    def worker_thread(self, account_batch):
        """Worker thread for processing account batch"""
        for account in account_batch:
            if not self.running:
                break
            
            self.authenticate_and_join(account)
            
            # Interval between accounts
            if self.running:
                time.sleep(random.uniform(5, 15))
    
    def run_advanced_bot(self, session_id, max_accounts=None):
        """Run the advanced bot with authentication"""
        self.session_id = session_id
        self.running = True
        self.success_count = 0
        self.failure_count = 0
        
        # Limit accounts if specified
        accounts_to_use = self.accounts[:max_accounts] if max_accounts else self.accounts
        
        self.log("🚀 STARTING ADVANCED SHOPEE BOT", "SUCCESS")
        self.log(f"🎯 Session ID: {session_id}")
        self.log(f"👥 Accounts to use: {len(accounts_to_use)}")
        self.log(f"🔐 Authentication: ENABLED")
        self.log(f"🛡️  Anti-detection: ENABLED")
        print("\n" + "="*60)
        
        # Divide accounts into batches for concurrent processing
        max_concurrent = min(3, len(accounts_to_use))  # Max 3 concurrent sessions
        batch_size = max(1, len(accounts_to_use) // max_concurrent)
        
        threads = []
        
        for i in range(0, len(accounts_to_use), batch_size):
            if not self.running:
                break
                
            batch = accounts_to_use[i:i + batch_size]
            if batch:
                thread = threading.Thread(target=self.worker_thread, args=(batch,))
                threads.append(thread)
                thread.start()
                
                # Stagger thread starts
                time.sleep(3)
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        self.running = False
        
        # Final report
        print("\n" + "="*60)
        self.log("🎉 ADVANCED BOT COMPLETED", "SUCCESS")
        self.log(f"✅ Successful logins: {self.success_count}")
        self.log(f"❌ Failed logins: {self.failure_count}")
        self.log(f"📊 Success rate: {(self.success_count/(self.success_count+self.failure_count)*100):.1f}%" if (self.success_count+self.failure_count) > 0 else "N/A")

def main():
    print("""
    ╔═══════════════════════════════════════════════════════╗
    ║           ADVANCED SHOPEE LIVE BOT v2.0              ║
    ║              WITH ROBUST AUTHENTICATION               ║
    ╚═══════════════════════════════════════════════════════╝
    
    🛡️  Features:
    ✅ Advanced authentication bypass
    ✅ Undetected Chrome driver  
    ✅ Anti-detection mechanisms
    ✅ Persistent session management
    ✅ Real viewer count increase
    ✅ Organized folder structure
    """)
    
    bot = AdvancedShopeeBot()
    
    # Load accounts
    if not bot.load_accounts():
        input("Press Enter to exit...")
        return
    
    print(f"\n📊 Total akun tersedia: {len(bot.accounts)}")
    
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
    
    # Ask for number of accounts
    while True:
        try:
            max_accounts_input = input(f"\n🔢 Berapa akun yang ingin digunakan? (max {len(bot.accounts)}, Enter untuk semua): ").strip()
            
            if not max_accounts_input:
                max_accounts = None
                break
            
            max_accounts = int(max_accounts_input)
            if 1 <= max_accounts <= len(bot.accounts):
                break
            else:
                print(f"❌ Jumlah harus antara 1-{len(bot.accounts)}")
        except ValueError:
            print("❌ Input harus berupa angka!")
    
    # Warning and confirmation
    account_count = max_accounts or len(bot.accounts)
    print(f"\n⚠️  ADVANCED BOT WARNING:")
    print(f"🔐 Bot akan melakukan authentication untuk {account_count} akun")
    print(f"🌐 Menggunakan undetected Chrome driver")
    print(f"🛡️  Anti-detection mechanisms aktif")
    print(f"⏱️  Proses mungkin memakan waktu 5-10 menit")
    print(f"📈 Viewer count akan naik secara real-time!")
    
    confirm = input(f"\n🚀 Lanjutkan dengan Advanced Bot? (y/n): ").lower()
    if confirm != 'y':
        print("👋 Bot dibatalkan!")
        return
    
    # Run bot
    try:
        bot.run_advanced_bot(session_id, max_accounts)
    except KeyboardInterrupt:
        print("\n⚠️ Bot dihentikan oleh user!")
        bot.running = False
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
