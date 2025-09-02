#!/usr/bin/env python3
"""
Emergency Python Installer for Windows RDP
This script helps when Python is not properly configured on Windows RDP
"""

import os
import sys
import subprocess
import urllib.request
import json
from pathlib import Path

def print_banner():
    print("=" * 60)
    print(" 🚨 EMERGENCY PYTHON INSTALLER - WINDOWS RDP")
    print("=" * 60)
    print()

def check_python_commands():
    """Test different Python commands"""
    commands = ['python', 'python3', 'py']
    
    for cmd in commands:
        try:
            result = subprocess.run([cmd, '--version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print(f"✅ Found Python: {cmd} -> {result.stdout.strip()}")
                return cmd
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
            print(f"❌ Command '{cmd}' not available")
    
    return None

def find_python_installations():
    """Search for Python installations in common locations"""
    print("🔍 Searching for Python installations...")
    
    search_paths = [
        Path("C:/Python*/python.exe"),
        Path(os.path.expandvars("%LOCALAPPDATA%/Programs/Python/Python*/python.exe")),
        Path(os.path.expandvars("%PROGRAMFILES%/Python*/python.exe")),
        Path(os.path.expandvars("%PROGRAMFILES(X86)%/Python*/python.exe")),
        Path(os.path.expandvars("%USERPROFILE%/AppData/Local/Microsoft/WindowsApps/python.exe"))
    ]
    
    found_installations = []
    
    for pattern in search_paths:
        try:
            parent = pattern.parent
            if parent.exists():
                for path in parent.rglob(pattern.name):
                    if path.exists():
                        try:
                            result = subprocess.run([str(path), '--version'],
                                                  capture_output=True, text=True, timeout=5)
                            if result.returncode == 0:
                                version = result.stdout.strip()
                                print(f"✅ Found: {path} -> {version}")
                                found_installations.append((str(path), version))
                        except:
                            pass
        except:
            pass
    
    return found_installations

def download_python():
    """Download Python installer"""
    print("📥 Downloading Python 3.11.5...")
    
    url = "https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe"
    installer_path = Path("python-3.11.5-installer.exe")
    
    try:
        print(f"   URL: {url}")
        print(f"   Saving to: {installer_path}")
        
        urllib.request.urlretrieve(url, installer_path)
        
        if installer_path.exists():
            size_mb = installer_path.stat().st_size / (1024 * 1024)
            print(f"✅ Download complete! Size: {size_mb:.1f} MB")
            return installer_path
        else:
            print("❌ Download failed - file not created")
            return None
            
    except Exception as e:
        print(f"❌ Download error: {e}")
        return None

def install_python(installer_path):
    """Install Python from downloaded installer"""
    print(f"🔧 Installing Python from {installer_path}...")
    
    # Silent installation with PATH addition
    install_args = [
        str(installer_path),
        "/quiet",
        "InstallAllUsers=1", 
        "PrependPath=1",
        "Include_test=0",
        "Include_doc=0"
    ]
    
    try:
        print("   Running installer (this may take a few minutes)...")
        result = subprocess.run(install_args, timeout=300)  # 5 minute timeout
        
        if result.returncode == 0:
            print("✅ Installation completed successfully!")
            return True
        else:
            print(f"❌ Installation failed with code: {result.returncode}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Installation timed out")
        return False
    except Exception as e:
        print(f"❌ Installation error: {e}")
        return False

def install_packages(python_cmd):
    """Install required packages"""
    packages = [
        "selenium",
        "webdriver-manager", 
        "requests",
        "colorama"
    ]
    
    print("📦 Installing required packages...")
    
    # Upgrade pip first
    try:
        subprocess.run([python_cmd, "-m", "pip", "install", "--upgrade", "pip"], 
                      check=True, timeout=60)
        print("✅ pip upgraded")
    except:
        print("⚠️ pip upgrade failed, continuing...")
    
    # Install packages
    for package in packages:
        try:
            print(f"   Installing {package}...")
            subprocess.run([python_cmd, "-m", "pip", "install", package], 
                          check=True, timeout=120)
            print(f"✅ {package} installed")
        except subprocess.SubprocessError:
            print(f"❌ Failed to install {package}")
            return False
        except subprocess.TimeoutExpired:
            print(f"❌ Timeout installing {package}")
            return False
    
    return True

def test_bot_requirements():
    """Test if bot requirements are met"""
    print("🧪 Testing bot requirements...")
    
    try:
        # Test selenium
        import selenium
        print("✅ selenium available")
    except ImportError:
        print("❌ selenium not available")
        return False
    
    try:
        # Test webdriver_manager
        import webdriver_manager
        print("✅ webdriver_manager available") 
    except ImportError:
        print("❌ webdriver_manager not available")
        return False
    
    try:
        # Test requests
        import requests
        print("✅ requests available")
    except ImportError:
        print("❌ requests not available")
        return False
    
    return True

def create_launcher():
    """Create a launcher script"""
    launcher_content = """@echo off
title Shopee Bot Launcher
echo Starting Shopee Bot...

REM Try different Python commands
python final_shopee_bot.py 2>nul
if %errorlevel% equ 0 goto :end

python3 final_shopee_bot.py 2>nul  
if %errorlevel% equ 0 goto :end

py final_shopee_bot.py 2>nul
if %errorlevel% equ 0 goto :end

echo Python not found! Please run the Python installer first.
pause

:end
echo Bot finished!
pause
"""
    
    launcher_path = Path("start_bot.bat")
    with open(launcher_path, 'w') as f:
        f.write(launcher_content)
    
    print(f"✅ Launcher created: {launcher_path}")

def main():
    print_banner()
    
    # Step 1: Check existing Python commands
    python_cmd = check_python_commands()
    
    if python_cmd:
        print(f"✅ Python already available: {python_cmd}")
    else:
        # Step 2: Search for installations
        installations = find_python_installations()
        
        if installations:
            print("📋 Found Python installations:")
            for i, (path, version) in enumerate(installations):
                print(f"   {i+1}. {path} -> {version}")
            
            # Use the first one found
            python_cmd = installations[0][0]
            print(f"✅ Using: {python_cmd}")
        else:
            print("❌ No Python installations found!")
            
            # Step 3: Download and install Python
            installer = download_python()
            if not installer:
                print("❌ Failed to download Python installer")
                print("\n📋 Manual installation required:")
                print("1. Go to: https://www.python.org/downloads/")
                print("2. Download Python 3.11+")
                print("3. During installation, check 'Add Python to PATH'")
                print("4. Restart this script")
                input("\nPress Enter to exit...")
                return
            
            if install_python(installer):
                # Clean up installer
                try:
                    installer.unlink()
                    print("🗑️ Installer cleaned up")
                except:
                    pass
                
                # Test installation
                python_cmd = check_python_commands()
                if not python_cmd:
                    print("❌ Python installation verification failed")
                    print("Please restart your command prompt and try again")
                    input("Press Enter to exit...")
                    return
            else:
                print("❌ Python installation failed")
                input("Press Enter to exit...")
                return
    
    # Step 4: Install required packages
    print("\n" + "=" * 60)
    print(" INSTALLING BOT DEPENDENCIES")
    print("=" * 60)
    
    if not install_packages(python_cmd):
        print("❌ Package installation failed")
        input("Press Enter to exit...")
        return
    
    # Step 5: Test requirements
    print("\n" + "=" * 60)
    print(" TESTING REQUIREMENTS")
    print("=" * 60)
    
    if not test_bot_requirements():
        print("❌ Requirements test failed")
        input("Press Enter to exit...")
        return
    
    # Step 6: Create launcher
    create_launcher()
    
    # Step 7: Success!
    print("\n" + "=" * 60)
    print(" ✅ SETUP COMPLETE!")
    print("=" * 60)
    print()
    print(f"🐍 Python command: {python_cmd}")
    print("📦 All packages installed")
    print("🚀 Bot ready to run")
    print()
    print("Next steps:")
    print("1. Double-click 'start_bot.bat' to run the bot")
    print("2. Or run: python final_shopee_bot.py")
    print()
    
    # Ask if user wants to run the bot now
    response = input("Run the bot now? (y/N): ").strip().lower()
    if response in ['y', 'yes']:
        print("\n🚀 Starting bot...")
        try:
            subprocess.run([python_cmd, "final_shopee_bot.py"])
        except KeyboardInterrupt:
            print("\n⚠️ Bot stopped by user")
        except Exception as e:
            print(f"\n❌ Bot error: {e}")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
