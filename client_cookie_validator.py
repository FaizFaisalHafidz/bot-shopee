#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Client Cookie Validator - Business Solution
Validate cookies dari client dan berikan feedback yang clear
"""

import time
import random
import os
import sys
from datetime import datetime

# Browser automation imports
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

try:
    import undetected_chromedriver as uc
    UNDETECTED_AVAILABLE = True
except ImportError:
    UNDETECTED_AVAILABLE = False

class ClientCookieValidator:
    def __init__(self):
        self.working_cookies = []
        self.expired_cookies = []
        self.invalid_cookies = []
        
    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")
    
    def load_client_cookies(self):
        """Load cookies dari client (input.csv)"""
        try:
            with open('input.csv', 'r', encoding='utf-8') as file:
                content = file.read().strip()
            
            lines = [line.strip() for line in content.split('\n') if line.strip() and not line.startswith('#')]
            
            cookies_list = []
            for line_num, line in enumerate(lines, 1):
                cookie_data = self.parse_cookie_line(line, line_num)
                if cookie_data:
                    cookies_list.append(cookie_data)
                else:
                    self.invalid_cookies.append({
                        'line_number': line_num,
                        'raw_line': line,
                        'reason': 'Missing required cookies (SPC_U, SPC_T_ID, csrftoken)'
                    })
            
            self.log(f"✅ Loaded {len(cookies_list)} valid cookie formats from client")
            return cookies_list
            
        except FileNotFoundError:
            self.log("❌ File input.csv tidak ditemukan!")
            print("\n📧 FEEDBACK FOR CLIENT:")
            print("File input.csv not found. Please provide cookies in CSV format.")
            return []
        except Exception as e:
            self.log(f"❌ Error loading cookies: {e}")
            return []
    
    def parse_cookie_line(self, cookie_string, line_num):
        """Parse cookie string"""
        try:
            cookies = {}
            required_cookies = ['SPC_U', 'SPC_T_ID', 'csrftoken']
            
            # Handle different separators
            for separator in [';', '; ']:
                if separator in cookie_string:
                    parts = cookie_string.split(separator)
                    break
            else:
                parts = [cookie_string]
            
            for cookie in parts:
                cookie = cookie.strip()
                if '=' in cookie:
                    name, value = cookie.split('=', 1)
                    cookies[name.strip()] = value.strip()
            
            # Check required cookies
            missing = [cookie for cookie in required_cookies if cookie not in cookies]
            if missing:
                return None
            
            return {
                'line_number': line_num,
                'cookies': cookies,
                'cookie_string': cookie_string,
                'user_id': cookies.get('SPC_U', ''),
                'token': cookies.get('SPC_T_ID', ''),
                'csrf': cookies.get('csrftoken', ''),
                'raw_line': cookie_string
            }
            
        except Exception as e:
            return None
    
    def quick_validate_cookie(self, cookie_data):
        """Quick validation tanpa browser (format check only)"""
        try:
            # Basic format validation
            user_id = cookie_data['user_id']
            token = cookie_data['token'] 
            csrf = cookie_data['csrf']
            
            # Check if user_id is numeric (basic validation)
            if not user_id.isdigit():
                return False, "Invalid SPC_U format (should be numeric)"
            
            # Check if token and csrf have reasonable length
            if len(token) < 10:
                return False, "SPC_T_ID too short (likely invalid)"
            
            if len(csrf) < 10:
                return False, "csrftoken too short (likely invalid)"
            
            return True, "Format OK"
            
        except Exception as e:
            return False, f"Validation error: {e}"
    
    def validate_all_cookies_quick(self):
        """Quick validation untuk client feedback"""
        cookies_list = self.load_client_cookies()
        
        if not cookies_list:
            return
        
        print("\n" + "="*70)
        print("🔍 CLIENT COOKIE VALIDATION REPORT")
        print("="*70)
        
        print(f"📊 Total cookies received from client: {len(cookies_list)}")
        print(f"❌ Invalid format cookies: {len(self.invalid_cookies)}")
        print("\n" + "-"*70)
        
        format_valid = 0
        format_invalid = 0
        
        for i, cookie_data in enumerate(cookies_list, 1):
            user_display = cookie_data['user_id'][:8] + "..."
            line_num = cookie_data['line_number']
            
            is_valid, reason = self.quick_validate_cookie(cookie_data)
            
            if is_valid:
                format_valid += 1
                print(f"✅ Line {line_num:2d}: {user_display} - Format OK")
            else:
                format_invalid += 1
                print(f"❌ Line {line_num:2d}: {user_display} - {reason}")
                self.invalid_cookies.append({
                    'line_number': line_num,
                    'raw_line': cookie_data['raw_line'],
                    'reason': reason
                })
        
        # Summary
        total_processed = len(cookies_list) + len(self.invalid_cookies)
        
        print("\n" + "="*70)
        print("📊 VALIDATION SUMMARY")
        print("="*70)
        print(f"✅ Format Valid: {format_valid}/{total_processed} cookies")
        print(f"❌ Format Invalid: {len(self.invalid_cookies)}/{total_processed} cookies")
        
        if format_valid > 0:
            print(f"\n🎉 {format_valid} cookies have correct format!")
            print("💡 These cookies will be tested for login validity...")
        
        if len(self.invalid_cookies) > 0:
            print(f"\n⚠️ {len(self.invalid_cookies)} cookies have format issues:")
            for invalid in self.invalid_cookies:
                print(f"   Line {invalid['line_number']}: {invalid['reason']}")
        
        return format_valid > 0
    
    def generate_client_feedback(self):
        """Generate feedback untuk client"""
        total_received = len(self.working_cookies) + len(self.expired_cookies) + len(self.invalid_cookies)
        working_count = len(self.working_cookies)
        expired_count = len(self.expired_cookies)
        invalid_count = len(self.invalid_cookies)
        
        print("\n" + "="*70)
        print("📧 CLIENT FEEDBACK REPORT")
        print("="*70)
        
        # Success rate
        if total_received > 0:
            working_rate = (working_count / total_received) * 100
            print(f"📊 Cookie Status Summary:")
            print(f"   ✅ Working: {working_count}/{total_received} ({working_rate:.1f}%)")
            print(f"   ❌ Expired: {expired_count}/{total_received}")
            print(f"   ⚠️ Invalid: {invalid_count}/{total_received}")
        
        # Client recommendations
        print(f"\n💼 BUSINESS RECOMMENDATIONS:")
        
        if working_count >= total_received * 0.8:  # 80%+ working
            print("✅ EXCELLENT: Most cookies are working fine")
            print("🚀 Bot can proceed with high success rate")
            
        elif working_count >= total_received * 0.5:  # 50%+ working  
            print("⚡ GOOD: Majority of cookies are working")
            print("🚀 Bot can proceed with moderate success rate")
            if expired_count > 0:
                print(f"💡 Consider refreshing {expired_count} expired cookies for better results")
                
        elif working_count > 0:  # Some working
            print("⚠️ PARTIAL: Only some cookies are working")
            print("🔧 Bot will work but with limited accounts")
            print(f"💡 Recommend refreshing {expired_count} expired cookies")
            
        else:  # None working
            print("❌ CRITICAL: No cookies are currently working")
            print("🛑 Bot cannot proceed until cookies are refreshed")
            print("📧 Client must provide fresh cookies")
        
        # Instructions for client
        if expired_count > 0 or invalid_count > 0:
            print(f"\n📋 INSTRUCTIONS FOR CLIENT:")
            print("=" * 70)
            print("""
To refresh expired/invalid cookies:

1. Open Chrome browser (normal mode)
2. Clear all cookies: Settings → Privacy → Clear browsing data  
3. Login fresh to https://shopee.co.id
4. After successful login, press F12 (Developer Tools)
5. Go to Application → Cookies → https://shopee.co.id
6. Copy these cookie values:
   • SPC_U (User ID)
   • SPC_T_ID (Session Token)  
   • csrftoken (Security Token)
7. Format: SPC_U=value; SPC_T_ID=value; csrftoken=value;
8. Send back in same CSV format (one line per account)

⚠️ Important:
- Don't logout after copying cookies
- Fresh cookies valid for 3-7 days
- One account = one line in CSV
            """)
        
        # Files generated
        if working_count > 0:
            print(f"\n📁 FILES GENERATED:")
            try:
                with open('client_working_cookies.csv', 'w', encoding='utf-8') as f:
                    f.write("# WORKING COOKIES - Ready for bot\n")
                    for cookie_data in self.working_cookies:
                        f.write(cookie_data['raw_line'] + '\n')
                print(f"✅ client_working_cookies.csv - {working_count} working cookies")
            except:
                pass
        
        if expired_count > 0:
            print(f"📋 List of expired cookies provided for client reference")

def main():
    print("""
    ╔═══════════════════════════════════════════════════════╗
    ║         CLIENT COOKIE VALIDATOR v1.0                  ║
    ║       Business solution for client cookies             ║
    ╚═══════════════════════════════════════════════════════╝
    
    🎯 Purpose: Validate cookies dari client & provide feedback
    📁 Input: input.csv (cookies from client)
    📊 Output: Detailed validation report + client feedback
    """)
    
    validator = ClientCookieValidator()
    
    print("🔍 Menu:")
    print("1. Quick validation (format check only)")  
    print("2. Full validation (browser test) - Coming soon")
    print("3. Generate client feedback template")
    print("4. Exit")
    
    while True:
        choice = input("\n📍 Choose option (1-4): ").strip()
        
        if choice == '1':
            print("🚀 Running quick validation...")
            has_valid = validator.validate_all_cookies_quick()
            if has_valid:
                print("\n💡 Next: Run browser validation to check if cookies can actually login")
            validator.generate_client_feedback()
            break
            
        elif choice == '2':
            print("⚠️ Full browser validation coming soon...")
            print("💡 For now, use real_cookie_tester.py for browser validation")
            break
            
        elif choice == '3':
            validator.generate_client_feedback()
            break
            
        elif choice == '4':
            print("👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice!")

if __name__ == "__main__":
    main()
