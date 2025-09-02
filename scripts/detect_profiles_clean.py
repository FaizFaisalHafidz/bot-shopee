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
                            
                            # Try to get email from preferences
                            if 'profile' in prefs:
                                if 'user_name' in prefs['profile']:
                                    email = prefs['profile']['user_name']
                                elif 'name' in prefs['profile']:
                                    name = prefs['profile']['name']
                                    if '@' in name:
                                        email = name
                            
                            profiles.append({
                                'path': str(item),
                                'name': profile_name,
                                'email': email,
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
