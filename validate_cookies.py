#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cookie Validator untuk Shopee Live Bot
Script untuk memvalidasi dan menganalisis cookie di input.csv
"""

import json
from datetime import datetime

class CookieValidator:
    def __init__(self):
        self.accounts = []
        self.valid_accounts = 0
        self.invalid_accounts = 0
        
    def parse_cookies(self, cookie_string):
        """Parse cookie string menjadi dict"""
        try:
            cookies = {}
            cookie_string = cookie_string.strip()
            
            for cookie in cookie_string.split('; '):
                if '=' in cookie:
                    key, value = cookie.split('=', 1)
                    cookies[key.strip()] = value.strip()
            
            return cookies
        except Exception as e:
            print(f"❌ Error parsing cookies: {e}")
            return None
    
    def validate_account(self, cookies):
        """Validasi cookie account"""
        if not cookies:
            return False, "Cookie parsing failed"
        
        # Check required cookies
        required_cookies = ['SPC_U', 'csrftoken']
        missing_required = [cookie for cookie in required_cookies if cookie not in cookies]
        if missing_required:
            return False, f"Missing required: {', '.join(missing_required)}"
        
        # Validate SPC_U
        if not cookies['SPC_U'].isdigit():
            return False, f"Invalid SPC_U: {cookies['SPC_U']}"
        
        return True, "Valid"
    
    def analyze_account(self, cookies):
        """Analisis detail account"""
        important_cookies = ['SPC_T_ID', 'SPC_ST', 'SPC_EC', 'SPC_R_T_ID']
        
        analysis = {
            'user_id': cookies.get('SPC_U', 'Unknown'),
            'csrf_token': cookies.get('csrftoken', 'Missing')[:20] + '...' if cookies.get('csrftoken') else 'Missing',
            'has_session_token': 'SPC_ST' in cookies,
            'has_auth_token': 'SPC_T_ID' in cookies,
            'has_ec_token': 'SPC_EC' in cookies,
            'has_refresh_token': 'SPC_R_T_ID' in cookies,
            'locale': cookies.get('__LOCALE__null', 'Unknown'),
            'total_cookies': len(cookies),
            'completeness_score': 0
        }
        
        # Calculate completeness score
        score = 0
        if analysis['has_session_token']:
            score += 25
        if analysis['has_auth_token']:
            score += 25
        if analysis['has_ec_token']:
            score += 25
        if analysis['has_refresh_token']:
            score += 25
        
        analysis['completeness_score'] = score
        
        return analysis
    
    def load_and_validate(self):
        """Load dan validate semua akun"""
        try:
            with open('input.csv', 'r', encoding='utf-8') as file:
                content = file.read().strip()
                lines = [line.strip() for line in content.split('\n') if line.strip()]
                
                print("🔍 Validating accounts from input.csv...")
                print("=" * 80)
                
                for line_num, line in enumerate(lines, 1):
                    if line.startswith('#') or not line:
                        continue
                    
                    cookies = self.parse_cookies(line)
                    is_valid, reason = self.validate_account(cookies)
                    
                    if is_valid:
                        self.valid_accounts += 1
                        analysis = self.analyze_account(cookies)
                        self.accounts.append(analysis)
                        
                        # Color coding berdasarkan score
                        if analysis['completeness_score'] >= 75:
                            status_icon = "🔥"  # Perfect
                        elif analysis['completeness_score'] >= 50:
                            status_icon = "⚡"  # Good
                        else:
                            status_icon = "⚠️"   # Basic
                        
                        print(f"{status_icon} Account {line_num:2d}: User ID {analysis['user_id'][:8]}... | Score: {analysis['completeness_score']}% | Cookies: {analysis['total_cookies']}")
                    else:
                        self.invalid_accounts += 1
                        print(f"❌ Account {line_num:2d}: {reason}")
                
                return True
                
        except FileNotFoundError:
            print("❌ File input.csv tidak ditemukan!")
            return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def generate_report(self):
        """Generate laporan detail"""
        print("\n" + "=" * 80)
        print("📊 COOKIE VALIDATION REPORT")
        print("=" * 80)
        
        print(f"📈 Total Accounts Processed: {self.valid_accounts + self.invalid_accounts}")
        print(f"✅ Valid Accounts: {self.valid_accounts}")
        print(f"❌ Invalid Accounts: {self.invalid_accounts}")
        
        if self.valid_accounts > 0:
            # Statistics
            scores = [acc['completeness_score'] for acc in self.accounts]
            avg_score = sum(scores) / len(scores)
            perfect_accounts = len([s for s in scores if s >= 75])
            good_accounts = len([s for s in scores if 50 <= s < 75])
            basic_accounts = len([s for s in scores if s < 50])
            
            print(f"\n📊 Score Distribution:")
            print(f"   🔥 Perfect (75-100%): {perfect_accounts} accounts")
            print(f"   ⚡ Good (50-74%):     {good_accounts} accounts") 
            print(f"   ⚠️  Basic (0-49%):     {basic_accounts} accounts")
            print(f"   📈 Average Score:     {avg_score:.1f}%")
            
            # Feature availability
            session_tokens = len([acc for acc in self.accounts if acc['has_session_token']])
            auth_tokens = len([acc for acc in self.accounts if acc['has_auth_token']])
            ec_tokens = len([acc for acc in self.accounts if acc['has_ec_token']])
            
            print(f"\n🔧 Feature Availability:")
            print(f"   🔑 Session Tokens:  {session_tokens}/{self.valid_accounts} ({session_tokens/self.valid_accounts*100:.1f}%)")
            print(f"   🎟️  Auth Tokens:     {auth_tokens}/{self.valid_accounts} ({auth_tokens/self.valid_accounts*100:.1f}%)")
            print(f"   💳 EC Tokens:       {ec_tokens}/{self.valid_accounts} ({ec_tokens/self.valid_accounts*100:.1f}%)")
            
            # Recommendations
            print(f"\n💡 Recommendations:")
            if perfect_accounts >= self.valid_accounts * 0.8:
                print("   ✅ Cookie quality is excellent! Ready for production use.")
            elif good_accounts + perfect_accounts >= self.valid_accounts * 0.6:
                print("   ⚡ Cookie quality is good. Consider refreshing basic accounts.")
            else:
                print("   ⚠️  Many accounts have basic cookies. Consider refreshing them.")
            
            if self.valid_accounts >= 20:
                print(f"   🎯 You have {self.valid_accounts} accounts - perfect for bot operations!")
            elif self.valid_accounts >= 10:
                print(f"   👍 You have {self.valid_accounts} accounts - good for testing.")
            else:
                print(f"   📝 You have {self.valid_accounts} accounts - consider adding more for better results.")
        
        print("\n" + "=" * 80)

def main():
    print("🍪 Shopee Cookie Validator")
    print("=" * 80)
    
    validator = CookieValidator()
    
    if validator.load_and_validate():
        validator.generate_report()
        
        if validator.valid_accounts > 0:
            print(f"\n🚀 Ready to run bot with {validator.valid_accounts} valid accounts!")
            print("💡 Use ./run.sh to start the standard bot")
            print("💡 Use ./run_advanced.sh to start the advanced bot")
        else:
            print("\n❌ No valid accounts found. Please check your input.csv file.")
    else:
        print("\n❌ Failed to validate cookies.")

if __name__ == "__main__":
    main()
