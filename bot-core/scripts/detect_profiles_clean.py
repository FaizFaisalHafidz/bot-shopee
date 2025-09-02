import os
import sys
import json
from pathlib import Path

# Fix Windows encoding
if os.name == 'nt':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())

def find_chrome_profiles():
    """Find Chrome profiles from various locations"""
    profiles = []
    
    # Define search paths
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
    
    # Add custom session paths
    current_dir = Path.cwd()
    search_paths.extend([
        current_dir / 'sessions' / 'google_profiles',
        current_dir / 'sessions' / 'chrome_profiles',
        current_dir / 'sessions' / 'direct_profiles'
    ])
    
    for base_path in search_paths:
        try:
            if not base_path.exists():
                continue
                
            # Look for profile directories
            for item in base_path.iterdir():
                if item.is_dir() and ('Profile' in item.name or 'Default' in item.name or '_profile_' in item.name):
                    # Check if preferences file exists
                    pref_file = item / 'Preferences'
                    if pref_file.exists():
                        try:
                            with open(pref_file, 'r', encoding='utf-8') as f:
                                prefs = json.load(f)
                            
                            # Extract profile info
                            profile_name = item.name
                            email = "Unknown"
                            display_name = "Unknown"
                            
                            # Try multiple methods to get email from preferences
                            # Method 1: Check account_info for Google accounts
                            if 'account_info' in prefs:
                                for account_data in prefs['account_info']:
                                    if 'email' in account_data:
                                        email = account_data['email']
                                        if 'full_name' in account_data:
                                            display_name = account_data['full_name']
                                        break
                            
                            # Method 2: Check profile section
                            if email == "Unknown" and 'profile' in prefs:
                                profile_data = prefs['profile']
                                
                                # Check various email fields
                                email_fields = [
                                    'user_name',
                                    'gaia_name', 
                                    'gaia_given_name',
                                    'name'
                                ]
                                
                                for field in email_fields:
                                    if field in profile_data and profile_data[field]:
                                        candidate = profile_data[field]
                                        if '@' in str(candidate):
                                            email = candidate
                                            break
                                
                                # Check for display name
                                name_fields = ['gaia_name', 'name', 'given_name']
                                for field in name_fields:
                                    if field in profile_data and profile_data[field]:
                                        if '@' not in str(profile_data[field]):
                                            display_name = profile_data[field]
                                            break
                            
                            # Method 3: Check signin section
                            if email == "Unknown" and 'signin' in prefs:
                                signin_data = prefs['signin']
                                if 'allowed_username' in signin_data:
                                    email = signin_data['allowed_username']
                            
                            # Method 4: Check google services
                            if email == "Unknown" and 'google' in prefs:
                                google_data = prefs['google']
                                if 'services' in google_data:
                                    services = google_data['services']
                                    if 'signin' in services:
                                        signin = services['signin']
                                        if 'username' in signin:
                                            email = signin['username']
                            
                            # If still no email, try to find it in any nested structure
                            if email == "Unknown":
                                def find_email_recursive(data, depth=0):
                                    if depth > 3:  # Prevent infinite recursion
                                        return None
                                    if isinstance(data, dict):
                                        for key, value in data.items():
                                            if key in ['email', 'username', 'user_name', 'account_id']:
                                                if isinstance(value, str) and '@' in value:
                                                    return value
                                            elif isinstance(value, (dict, list)):
                                                result = find_email_recursive(value, depth + 1)
                                                if result:
                                                    return result
                                    elif isinstance(data, list):
                                        for item in data:
                                            result = find_email_recursive(item, depth + 1)
                                            if result:
                                                return result
                                    return None
                                
                                found_email = find_email_recursive(prefs)
                                if found_email:
                                    email = found_email
                            
                            profiles.append({
                                'path': str(item),
                                'name': profile_name,
                                'email': email,
                                'display_name': display_name,
                                'location': str(base_path.name)
                            })
                            
                        except Exception:
                            # Skip profiles that can't be read
                            continue
        except Exception:
            continue
    
    return profiles

def main():
    try:
        profiles = find_chrome_profiles()
        
        # Output only JSON
        print(json.dumps(profiles, ensure_ascii=False, indent=2))
        
    except Exception as e:
        # Output empty JSON on error
        print("[]")
        sys.exit(1)

if __name__ == "__main__":
    main()
