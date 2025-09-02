import os
import sys
import json
from pathlib import Path

# Fix Windows encoding
if os.name == 'nt':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())

def find_chrome_profiles():
    """Cari semua profile Chrome di sistem"""
    profiles = []
    
    # Lokasi default Chrome profiles
    if os.name == 'nt':  # Windows
        base_paths = [
            Path.home() / "AppData" / "Local" / "Google" / "Chrome" / "User Data",
            Path("sessions") / "google_profiles",
            Path("sessions") / "chrome_profiles", 
            Path("sessions") / "multi_profiles"
        ]
    else:  # macOS/Linux
        base_paths = [
            Path.home() / "Library" / "Application Support" / "Google" / "Chrome",
            Path("sessions") / "google_profiles",
            Path("sessions") / "chrome_profiles",
            Path("sessions") / "multi_profiles"
        ]
    
    for base_path in base_paths:
        if base_path.exists():
            try:
                for item in base_path.iterdir():
                    if item.is_dir():
                        profile_name = item.name
                        
                        # Skip system folders dan folder yang tidak relevan
                        skip_folders = [
                            'system profile', 'guest profile', 'nativemessaginghosts',
                            'screen_ai', 'safe browsing', 'browsermetrics', 'local traces',
                            'grshaderCache', 'autofillstates', 'tpcdmetadata', 
                            'privacysandboxattestationspreloaded', 'opencookiedatabase',
                            'crashpad', 'certificaterevocation', 'ondeviceheadsuggestmodel',
                            'download_cache', 'firstpartysetspreloaded', 'sslerrorassistant',
                            'shadercache', 'cookiereadinesslist', 'zxcvbndata',
                            'deferredbrowsermetrics', 'safetytips', 'origintrials',
                            'webstore downloads', 'meipreload', 'filetypepolicies',
                            'graphitedawncache', 'segmentation_platform', 'component_crx_cache',
                            'extensions_crx_cache', 'recoveryimproved', 'amountextractionheuristicregexes',
                            'subresource filter', 'probabilisticrevealthokenregistry',
                            'widevinecdm', 'crowd deny', 'pkimetadata', 'optimizationhints',
                            'trusttokenkeycommitments', 'optimization_guide_model_store'
                        ]
                        
                        if profile_name.lower() in skip_folders:
                            continue
                        
                        # Cek apakah folder ini adalah profile Chrome yang valid
                        preferences_file = item / "Preferences"
                        if not preferences_file.exists():
                            continue
                            
                        try:
                            with open(preferences_file, 'r', encoding='utf-8') as f:
                                prefs = json.load(f)
                                
                            # Extract email dari profile
                            email = f"Profile: {profile_name}"
                            
                            # Coba ambil email dari berbagai lokasi di preferences
                            if 'account_info' in prefs:
                                for account in prefs['account_info']:
                                    if 'email' in account:
                                        email = account['email']
                                        break
                            elif 'profile' in prefs:
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
                            
                        except Exception as e:
                            # Jika tidak bisa baca preferences, skip profile ini
                            continue
            except:
                continue
    
    return profiles

# Main execution
if __name__ == "__main__":
    try:
        print("[DEBUG] Starting profile detection...")
        profiles = find_chrome_profiles()
        
        if not profiles:
            print("ERROR: Tidak ada profile Chrome yang ditemukan!")
            print("INFO: Pastikan Chrome sudah diinstall dan pernah digunakan.")
            print("[DEBUG] No profiles found in any search location")
            sys.exit(1)
        
        print(f"INFO: Ditemukan {len(profiles)} profile Chrome:")
        print()
        
        for i, profile in enumerate(profiles):
            print(f"   {i+1}. {profile['email']}")
            print(f"      Path: {profile['path']}")
            print(f"      Location: {profile['location']}")
            print()
        
        # Save profiles to temp file
        try:
            with open('temp_profiles.json', 'w', encoding='utf-8') as f:
                json.dump(profiles, f, ensure_ascii=False, indent=2)
            print("[DEBUG] Profiles saved to temp_profiles.json")
        except Exception as e:
            print(f"[ERROR] Failed to save profiles: {e}")
            sys.exit(1)
        
        print(f"PROFILE_COUNT={len(profiles)}")
        
    except Exception as e:
        print(f"[ERROR] Unexpected error in profile detection: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
