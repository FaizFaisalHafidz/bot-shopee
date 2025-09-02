#!/usr/bin/env python3
"""
Standalone Python Setup and Shopee Bot Runner
This script ensures all dependencies are installed and runs the bot.
"""

import os
import sys
import subprocess
import platform
import urllib.request
import json
from pathlib import Path

def print_banner():
    """Print setup banner"""
    print("=" * 60)
    print(" 🤖 SHOPEE LIVE VIEWER BOT - AUTO SETUP")
    print("=" * 60)
    print()

def run_command(command, shell=True, capture_output=True):
    """Run a command and return the result"""
    try:
        result = subprocess.run(
            command, 
            shell=shell, 
            capture_output=capture_output,
            text=True,
            timeout=300  # 5 minutes timeout
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except Exception as e:
        return False, "", str(e)

def check_python():
    """Check Python version"""
    version = sys.version_info
    print(f"🐍 Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ required!")
        return False
    
    print("✅ Python version OK")
    return True

def install_packages():
    """Install required packages"""
    packages = [
        "selenium",
        "webdriver-manager", 
        "requests",
        "colorama"
    ]
    
    print("📦 Installing required packages...")
    
    for package in packages:
        print(f"   Installing {package}...")
        success, stdout, stderr = run_command([
            sys.executable, "-m", "pip", "install", 
            "--upgrade", package, "--quiet"
        ], shell=False)
        
        if not success:
            print(f"❌ Failed to install {package}: {stderr}")
            return False
    
    print("✅ All packages installed successfully")
    return True

def check_chrome_profiles():
    """Check for existing Chrome profiles"""
    print("🔍 Checking for Chrome profiles...")
    
    # Common Chrome profile locations
    if platform.system() == "Windows":
        chrome_paths = [
            Path(os.path.expanduser("~")) / "AppData/Local/Google/Chrome/User Data",
            Path("sessions/google_profiles")
        ]
    elif platform.system() == "Darwin":  # macOS
        chrome_paths = [
            Path(os.path.expanduser("~")) / "Library/Application Support/Google/Chrome",
            Path("sessions/google_profiles")
        ]
    else:  # Linux
        chrome_paths = [
            Path(os.path.expanduser("~")) / ".config/google-chrome",
            Path("sessions/google_profiles")
        ]
    
    total_profiles = 0
    found_paths = []
    
    for chrome_path in chrome_paths:
        if chrome_path.exists():
            profiles = []
            for item in chrome_path.iterdir():
                if item.is_dir():
                    if (item.name == "Default" or 
                        item.name.startswith("Profile ") or
                        "profile" in item.name.lower()):
                        profiles.append(item)
            
            if profiles:
                print(f"   ✅ Found {len(profiles)} profiles in: {chrome_path}")
                total_profiles += len(profiles)
                found_paths.append(str(chrome_path))
    
    if total_profiles == 0:
        print("   ⚠️ No Chrome profiles found!")
        print()
        print("📋 To create Chrome profiles:")
        print("   1. Open Google Chrome")
        print("   2. Click profile icon (top right)")
        print("   3. Add new profile for each Google account")
        print("   4. Login to different Google accounts in each profile")
        print("   5. Close Chrome and restart this script")
        print()
        
        response = input("Continue anyway? (y/N): ").strip().lower()
        if response != 'y':
            return False
    else:
        print(f"   ✅ Total profiles available: {total_profiles}")
    
    return True

def create_config():
    """Create bot configuration"""
    config = {
        "max_viewers": 10,
        "delay_between_viewers": 2,
        "session_duration": 300,
        "device_fingerprint": {
            "randomize_user_agent": True,
            "randomize_screen_resolution": True,
            "randomize_device_memory": True,
            "randomize_cpu_cores": True
        },
        "chrome_options": {
            "headless": False,
            "disable_images": True,
            "disable_javascript": False,
            "window_size": "1366,768"
        }
    }
    
    config_path = Path("config/bot_config.json")
    config_path.parent.mkdir(exist_ok=True)
    
    if not config_path.exists():
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"✅ Configuration created: {config_path}")
    else:
        print(f"✅ Configuration exists: {config_path}")
    
    return True

def setup_logging():
    """Setup logging directory"""
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    print(f"✅ Logging directory ready: {logs_dir}")
    return True

def run_bot():
    """Run the Shopee bot"""
    bot_file = Path("final_shopee_bot.py")
    
    if not bot_file.exists():
        print(f"❌ Bot file not found: {bot_file}")
        return False
    
    print("🚀 Starting Shopee Live Viewer Bot...")
    print()
    
    try:
        # Run the bot
        result = subprocess.run([sys.executable, str(bot_file)], 
                              timeout=3600)  # 1 hour timeout
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("⚠️ Bot timed out after 1 hour")
        return True
    except KeyboardInterrupt:
        print("\n⚠️ Bot stopped by user")
        return True
    except Exception as e:
        print(f"❌ Error running bot: {e}")
        return False

def main():
    """Main setup and run function"""
    print_banner()
    
    # Step 1: Check Python
    if not check_python():
        input("Press Enter to exit...")
        sys.exit(1)
    
    # Step 2: Install packages
    if not install_packages():
        input("Press Enter to exit...")
        sys.exit(1)
    
    # Step 3: Check Chrome profiles  
    if not check_chrome_profiles():
        input("Press Enter to exit...")
        sys.exit(0)
    
    # Step 4: Create configuration
    if not create_config():
        input("Press Enter to exit...")
        sys.exit(1)
    
    # Step 5: Setup logging
    if not setup_logging():
        input("Press Enter to exit...")
        sys.exit(1)
    
    # Step 6: Show setup complete
    print()
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                    SETUP COMPLETE                           ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()
    print("✅ Python: Ready")
    print("✅ Packages: Installed")
    print("✅ Chrome Profiles: Available")
    print("✅ Configuration: Ready")
    print("✅ Logging: Ready")
    print()
    
    # Step 7: Run the bot
    success = run_bot()
    
    print()
    if success:
        print("✅ Bot completed successfully!")
    else:
        print("❌ Bot encountered an error")
    
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
