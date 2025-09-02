import os
import sys
import json
from pathlib import Path

def analyze_chrome_preferences():
    """Analyze Chrome preferences to understand the structure"""
    
    # Define search paths for Windows
    if os.name == 'nt':  # Windows
        search_paths = [
            Path(os.environ.get('LOCALAPPDATA', '')) / 'Google' / 'Chrome' / 'User Data',
            Path(os.environ.get('APPDATA', '')) / 'Google' / 'Chrome' / 'User Data',
        ]
    else:  # macOS/Linux
        search_paths = [
            Path.home() / 'Library' / 'Application Support' / 'Google' / 'Chrome',
            Path.home() / '.config' / 'google-chrome',
        ]
    
    profiles_analyzed = 0
    
    for base_path in search_paths:
        try:
            if not base_path.exists():
                print(f"❌ Path not found: {base_path}")
                continue
                
            print(f"🔍 Analyzing: {base_path}")
                
            # Look for profile directories
            for item in base_path.iterdir():
                if item.is_dir() and ('Profile' in item.name or 'Default' in item.name):
                    pref_file = item / 'Preferences'
                    if pref_file.exists():
                        profiles_analyzed += 1
                        print(f"\n📁 Profile: {item.name}")
                        print(f"📄 Preferences file: {pref_file}")
                        
                        try:
                            with open(pref_file, 'r', encoding='utf-8') as f:
                                prefs = json.load(f)
                            
                            print("🔍 Looking for email/account information...")
                            
                            # Check profile section
                            if 'profile' in prefs:
                                profile_data = prefs['profile']
                                print("📋 Profile section found:")
                                for key in ['name', 'user_name', 'gaia_name', 'gaia_given_name', 'given_name']:
                                    if key in profile_data:
                                        print(f"  {key}: {profile_data[key]}")
                            
                            # Check account_info section
                            if 'account_info' in prefs:
                                print("👤 Account info section found:")
                                account_info = prefs['account_info']
                                if isinstance(account_info, list):
                                    for i, account in enumerate(account_info):
                                        print(f"  Account {i+1}: {account}")
                                else:
                                    print(f"  Account info: {account_info}")
                            
                            # Check signin section
                            if 'signin' in prefs:
                                signin_data = prefs['signin']
                                print("🔐 Signin section found:")
                                for key in ['allowed_username', 'username']:
                                    if key in signin_data:
                                        print(f"  {key}: {signin_data[key]}")
                            
                            # Check google services
                            if 'google' in prefs:
                                google_data = prefs['google']
                                print("🌐 Google section found:")
                                print(f"  Keys: {list(google_data.keys())}")
                            
                            # Search for any field containing '@'
                            def find_emails(data, path=""):
                                emails = []
                                if isinstance(data, dict):
                                    for key, value in data.items():
                                        current_path = f"{path}.{key}" if path else key
                                        if isinstance(value, str) and '@' in value and '.' in value:
                                            emails.append(f"{current_path}: {value}")
                                        elif isinstance(value, (dict, list)):
                                            emails.extend(find_emails(value, current_path))
                                elif isinstance(data, list):
                                    for i, item in enumerate(data):
                                        current_path = f"{path}[{i}]"
                                        if isinstance(item, str) and '@' in item and '.' in item:
                                            emails.append(f"{current_path}: {item}")
                                        elif isinstance(item, (dict, list)):
                                            emails.extend(find_emails(item, current_path))
                                return emails
                            
                            all_emails = find_emails(prefs)
                            if all_emails:
                                print("📧 Email addresses found:")
                                for email_info in all_emails:
                                    print(f"  {email_info}")
                            else:
                                print("❌ No email addresses found in this profile")
                            
                            print("-" * 50)
                            
                        except Exception as e:
                            print(f"❌ Error reading preferences: {e}")
                            
        except Exception as e:
            print(f"❌ Error analyzing {base_path}: {e}")
    
    print(f"\n📊 Total profiles analyzed: {profiles_analyzed}")

if __name__ == "__main__":
    analyze_chrome_preferences()
