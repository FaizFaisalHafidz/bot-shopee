"""
Test Gmail profile detection
"""
import json
import os
import sys

def test_profile_detection():
    print("=" * 50)
    print("GMAIL PROFILE DETECTION TEST")
    print("=" * 50)
    
    # Read temp_profiles.json
    profiles_file = 'temp_profiles.json'
    if not os.path.exists(profiles_file):
        print(f"[ERROR] {profiles_file} not found!")
        print("[INFO] Run: python scripts/detect_profiles_clean.py")
        return
    
    with open(profiles_file, 'r', encoding='utf-8') as f:
        all_profiles = json.load(f)
    
    print(f"[INFO] Total profiles found: {len(all_profiles)}")
    print()
    
    # Filter Gmail profiles
    gmail_profiles = []
    for i, profile in enumerate(all_profiles):
        email = profile.get('email', '')
        display_name = profile.get('display_name', '')
        name = profile.get('name', '')
        path = profile.get('path', '')
        
        print(f"[{i+1}] Profile Check:")
        print(f"    Name: {name}")
        print(f"    Email: {email}")
        print(f"    Display: {display_name}")
        
        # Check conditions - FIXED untuk cross platform
        is_gmail = email.endswith('@gmail.com')
        is_not_system = name != 'System Profile' and name != 'Guest Profile'
        is_not_unknown = email != 'Unknown' and email != ''
        has_valid_path = len(path.strip()) > 0  # Any valid path
        
        if is_gmail and is_not_system and is_not_unknown and has_valid_path:
            gmail_profiles.append(profile)
            print(f"    Result: ✅ VALID Gmail profile")
        else:
            print(f"    Result: ❌ REJECTED")
            print(f"           Gmail: {is_gmail}, NotSystem: {is_not_system}")
            print(f"           NotUnknown: {is_not_unknown}, ValidPath: {has_valid_path}")
        print()
    
    print("=" * 50)
    print("FINAL RESULTS")
    print("=" * 50)
    print(f"Valid Gmail profiles: {len(gmail_profiles)} out of {len(all_profiles)}")
    print()
    
    if gmail_profiles:
        print("These accounts will be used by the bot:")
        for i, profile in enumerate(gmail_profiles):
            print(f"  {i+1}. {profile['email']} ({profile['display_name']})")
            print(f"     Path: {profile['path']}")
        print()
        print("✅ Bot will use these Gmail accounts")
    else:
        print("❌ No valid Gmail profiles found!")
        print("   Make sure you have Chrome profiles logged into Gmail")
    
    print()

if __name__ == "__main__":
    test_profile_detection()
