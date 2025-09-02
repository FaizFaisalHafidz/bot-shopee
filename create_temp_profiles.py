"""
Create temporary Chrome profile copies for bot usage
This avoids conflicts with existing Chrome instances
"""

import json
import os
import shutil
import sys
from pathlib import Path

def load_profiles():
    """Load detected profiles"""
    try:
        with open('temp_profiles.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("[ERROR] temp_profiles.json not found. Run profile detection first.")
        return []
    except Exception as e:
        print(f"[ERROR] Failed to load profiles: {e}")
        return []

def create_temp_profile_copy(source_profile_path, temp_dir, profile_name):
    """Create temporary copy of Chrome profile"""
    try:
        temp_profile_path = os.path.join(temp_dir, f"temp_{profile_name}")
        
        # Remove existing temp profile
        if os.path.exists(temp_profile_path):
            shutil.rmtree(temp_profile_path)
        
        print(f"   [INFO] Copying profile from: {source_profile_path}")
        print(f"   [INFO] To temporary location: {temp_profile_path}")
        
        # Copy essential Chrome profile files
        os.makedirs(temp_profile_path, exist_ok=True)
        
        essential_files = [
            'Preferences',
            'Local State',
            'Cookies',
            'Login Data',
            'Web Data',
            'History',
            'Bookmarks',
            'Secure Preferences',
            'Network Action Predictor'
        ]
        
        essential_dirs = [
            'Default',
            'Extension Cookies',
            'Extension State',
            'Local Extension Settings',
            'Sync Extension Settings'
        ]
        
        # Copy files
        for file_name in essential_files:
            src_file = os.path.join(source_profile_path, file_name)
            dst_file = os.path.join(temp_profile_path, file_name)
            
            if os.path.exists(src_file):
                try:
                    shutil.copy2(src_file, dst_file)
                    print(f"     ✓ Copied: {file_name}")
                except Exception as e:
                    print(f"     ✗ Failed to copy {file_name}: {e}")
            else:
                print(f"     - Not found: {file_name}")
        
        # Copy directories
        for dir_name in essential_dirs:
            src_dir = os.path.join(source_profile_path, dir_name)
            dst_dir = os.path.join(temp_profile_path, dir_name)
            
            if os.path.exists(src_dir):
                try:
                    shutil.copytree(src_dir, dst_dir)
                    print(f"     ✓ Copied directory: {dir_name}")
                except Exception as e:
                    print(f"     ✗ Failed to copy directory {dir_name}: {e}")
            else:
                print(f"     - Directory not found: {dir_name}")
        
        return temp_profile_path
        
    except Exception as e:
        print(f"   [ERROR] Failed to create temp profile copy: {e}")
        return None

def main():
    print("=" * 60)
    print("CHROME PROFILE TEMP COPY CREATOR")
    print("=" * 60)
    
    # Load profiles
    profiles = load_profiles()
    if not profiles:
        return
    
    # Create temp directory
    temp_dir = "sessions/temp_bot_profiles"
    os.makedirs(temp_dir, exist_ok=True)
    
    print(f"\n[INFO] Creating temporary profile copies in: {temp_dir}")
    print("-" * 50)
    
    temp_profiles = []
    
    for i, profile in enumerate(profiles):
        profile_path = profile['path']
        email = profile.get('email', 'Unknown')
        display_name = profile.get('display_name', 'Unknown')
        
        print(f"\n[{i+1}] Processing profile: {email} ({display_name})")
        
        temp_path = create_temp_profile_copy(
            profile_path, 
            temp_dir, 
            f"profile_{i+1}_{email.replace('@', '_at_').replace('.', '_')}"
        )
        
        if temp_path:
            temp_profile = profile.copy()
            temp_profile['temp_path'] = temp_path
            temp_profile['original_path'] = profile_path
            temp_profiles.append(temp_profile)
            print(f"   [SUCCESS] Temporary profile created")
        else:
            print(f"   [ERROR] Failed to create temporary profile")
    
    # Save temp profiles info
    temp_profiles_file = "temp_bot_profiles.json"
    try:
        with open(temp_profiles_file, 'w', encoding='utf-8') as f:
            json.dump(temp_profiles, f, indent=2, ensure_ascii=False)
        
        print(f"\n[SUCCESS] Temporary profiles info saved to: {temp_profiles_file}")
        print(f"[INFO] Created {len(temp_profiles)} temporary profile copies")
        
    except Exception as e:
        print(f"\n[ERROR] Failed to save temp profiles info: {e}")

if __name__ == "__main__":
    main()
