import sys
import os
import time
import random
import string
import json
from pathlib import Path

# Fix Windows encoding
if os.name == 'nt':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())

# Import Selenium
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from webdriver_manager.chrome import ChromeDriverManager
except ImportError as e:
    print(f"ERROR: Import error: {e}")
    print("Please install required packages: pip install selenium webdriver-manager")
    input("Press any key to exit...")
    sys.exit(1)

def generate_device_id():
    """Generate unique 32-character device ID"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=32))

def inject_google_login(driver, profile_email):
    """Inject Google login session for Shopee"""
    try:
        print(f"   [INFO] Attempting to restore Google session for {profile_email}...")
        
        # First, go to Google to establish domain cookies
        driver.get("https://accounts.google.com")
        time.sleep(3)
        
        # Try to load saved cookies if available
        cookies_file = f"../sessions/cookies_{profile_email.replace('@', '_at_').replace('.', '_')}.json"
        
        if os.path.exists(cookies_file):
            print(f"   [INFO] Loading saved cookies from {cookies_file}")
            try:
                with open(cookies_file, 'r') as f:
                    cookies = json.load(f)
                    for cookie in cookies:
                        try:
                            driver.add_cookie(cookie)
                        except Exception as cookie_error:
                            print(f"   [DEBUG] Could not add cookie: {cookie_error}")
                            
                print(f"   [SUCCESS] Cookies loaded for {profile_email}")
                
                # Refresh to apply cookies
                driver.refresh()
                time.sleep(2)
                
            except Exception as e:
                print(f"   [WARNING] Could not load cookies: {e}")
        else:
            print(f"   [INFO] No saved cookies found for {profile_email}")
            
        # Check if already logged in
        try:
            # Look for signs of being logged in to Google
            current_url = driver.current_url
            if "myaccount.google.com" in current_url or "accounts.google.com/signin/continue" in current_url:
                print(f"   [SUCCESS] Google session restored for {profile_email}")
                return True
        except Exception as e:
            print(f"   [DEBUG] Could not verify Google login status: {e}")
            
        print(f"   [INFO] Starting with clean session for {profile_email}")
        return False
        
    except Exception as e:
        print(f"   [WARNING] Could not inject Google login: {e}")
        return False

def get_available_profiles():
    """Ambil daftar profile Chrome yang sudah dideteksi"""
    try:
        # Skip temp profiles untuk sementara, langsung pakai original profiles
        print("[INFO] Using original Chrome profiles (bypassing temp system)...")
        
        # Read temp_profiles.json directly
        profiles_file = '../temp_profiles.json' if os.path.exists('../temp_profiles.json') else 'temp_profiles.json'
        
        print(f"[DEBUG] Trying to read: {profiles_file}")
        if not os.path.exists(profiles_file):
            print("[ERROR] Profile file not found!")
            print("[DEBUG] Current directory:", os.getcwd())
            print("[DEBUG] Files in current directory:", [f for f in os.listdir('.') if not f.startswith('.')])
            return []
            
        with open(profiles_file, 'r', encoding='utf-8') as f:
            profiles = json.load(f)
            print(f"[DEBUG] Loaded {len(profiles)} profiles from JSON")
            
            # Filter out System Profile and Unknown emails
            valid_profiles = []
            for p in profiles:
                email = p.get('email', 'Unknown')
                name = p.get('name', '')
                if email != 'Unknown' and name != 'System Profile' and '@gmail.com' in email:
                    valid_profiles.append(p)
                    print(f"[VALID] {email} ({p.get('display_name', 'Unknown')})")
                else:
                    print(f"[SKIP] {email} - {name} (filtered out)")
            
            print(f"[INFO] Found {len(valid_profiles)} valid Gmail profiles")
            return valid_profiles
    except json.JSONDecodeError as e:
        print(f"[ERROR] JSON decode error: {e}")
        return []
    except Exception as e:
        print(f"[ERROR] Error reading profiles: {e}")
        return []

def create_chrome_with_profile(profile_data, device_id, viewer_num):
    """Buat Chrome instance dengan profile spesifik dan device ID"""
    try:
        print(f"   [DEBUG] Setting up Chrome for viewer #{viewer_num+1}")
        
        # Extract profile information
        if isinstance(profile_data, dict):
            original_profile_path = profile_data.get('path')
            email = profile_data.get('email', 'Unknown')
            name = profile_data.get('name', 'Unknown')
            print(f"   [DEBUG] Using profile: {email} ({name})")
        else:
            original_profile_path = profile_data
            email = 'Unknown'
            
        print(f"   [DEBUG] Original profile: {original_profile_path}")
        
        # Create isolated profile directory for this viewer
        base_dir = os.path.join(os.getcwd(), '..', 'sessions', 'isolated_profiles')
        os.makedirs(base_dir, exist_ok=True)
        
        isolated_profile = os.path.join(base_dir, f"viewer_{viewer_num+1}_{email.replace('@', '_at_').replace('.', '_')}")
        
        # Remove existing isolated profile
        if os.path.exists(isolated_profile):
            import shutil
            shutil.rmtree(isolated_profile)
        
        os.makedirs(isolated_profile, exist_ok=True)
        print(f"   [DEBUG] Isolated profile: {isolated_profile}")
        
        options = Options()
        
        # Use isolated profile directory
        options.add_argument(f'--user-data-dir={isolated_profile}')
        
        # Unique debugging port for each instance
        debug_port = 9222 + viewer_num
        options.add_argument(f'--remote-debugging-port={debug_port}')
        
        # Chrome options for clean start
        options.add_argument('--no-first-run')
        options.add_argument('--no-default-browser-check')
        options.add_argument('--disable-default-apps')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-web-security')
        options.add_argument('--allow-running-insecure-content')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-plugins')
        options.add_argument('--disable-images')  # Faster loading
        
        # Anti-detection options
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option("detach", True)
        
        # Find Chrome executable path
        chrome_executable = None
        
        if os.name == 'nt':  # Windows
            possible_paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe")
            ]
        else:  # macOS/Linux
            possible_paths = [
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                "/usr/bin/google-chrome",
                "/usr/bin/chromium-browser",
                "/snap/bin/chromium"
            ]
        
        for path in possible_paths:
            if os.path.exists(path):
                chrome_executable = path
                print(f"   [DEBUG] Found Chrome at: {path}")
                break
        
        if chrome_executable:
            options.binary_location = chrome_executable
            print(f"   [DEBUG] Using Chrome binary: {chrome_executable}")
        else:
            print(f"   [WARNING] Chrome executable not found, using system default")
        
        # Create WebDriver
        try:
            service = Service()
            driver = webdriver.Chrome(service=service, options=options)
            print(f"   [SUCCESS] Chrome launched for {email} (isolated profile)")
        except Exception as e:
            print(f"   [DEBUG] System chromedriver failed, trying ChromeDriverManager...")
            from webdriver_manager.chrome import ChromeDriverManager
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            print(f"   [SUCCESS] Chrome launched for {email} (via ChromeDriverManager)")
        
        # Remove automation indicators
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        # Copy cookies from original profile if available
        try:
            print(f"   [INFO] Attempting to copy session data from original profile...")
            import sqlite3
            import shutil
            
            # Try to copy essential files from original profile
            essential_files = ['Cookies', 'Login Data', 'Web Data']
            
            for file_name in essential_files:
                original_file = os.path.join(original_profile_path, file_name)
                isolated_file = os.path.join(isolated_profile, 'Default', file_name)
                
                os.makedirs(os.path.join(isolated_profile, 'Default'), exist_ok=True)
                
                if os.path.exists(original_file):
                    try:
                        shutil.copy2(original_file, isolated_file)
                        print(f"   [SUCCESS] Copied {file_name}")
                    except Exception as copy_error:
                        print(f"   [WARNING] Could not copy {file_name}: {copy_error}")
                else:
                    print(f"   [INFO] {file_name} not found in original profile")
        except Exception as session_error:
            print(f"   [WARNING] Could not copy session data: {session_error}")
            print(f"   [INFO] Chrome will start with clean session")
        
        return driver
        
    except Exception as e:
        print(f"   [ERROR] Failed to create Chrome for {email}: {e}")
        print(f"   [ERROR] Error details: {str(e)}")
        return None

def inject_device_fingerprint(driver, device_id):
    """Inject device fingerprint untuk bypass detection"""
    try:
        fingerprint_script = f"""
        // Override device properties
        Object.defineProperty(navigator, 'deviceMemory', {{get: () => 8}});
        Object.defineProperty(navigator, 'hardwareConcurrency', {{get: () => 8}});
        
        // Override WebGL fingerprint
        const getParameter = WebGLRenderingContext.prototype.getParameter;
        WebGLRenderingContext.prototype.getParameter = function(parameter) {{
            if (parameter === 37445) return 'Custom GPU {device_id[:8]}';
            if (parameter === 37446) return 'Custom Vendor {device_id[8:16]}';
            return getParameter(parameter);
        }};
        
        // Set device ID in localStorage
        localStorage.setItem('device_id', '{device_id}');
        localStorage.setItem('session_id', '{device_id[:16]}');
        
        console.log('[INJECTED] Device fingerprint set:', '{device_id[:8]}...{device_id[-4:]}');
        """
        
        driver.execute_script(fingerprint_script)
        print(f"   [SUCCESS] Device fingerprint injected: {device_id[:8]}...{device_id[-4:]}")
        return True
    except Exception as e:
        print(f"   [WARNING] Failed to inject fingerprint: {e}")
        return False

def main():
    try:
        print("[DEBUG] Starting shopee_bot.py...")
        print(f"[DEBUG] Command line args: {sys.argv}")
        print(f"[DEBUG] Number of args: {len(sys.argv)}")
        
        # Ambil parameter dari command line
        if len(sys.argv) < 4:
            print("ERROR: Parameter tidak lengkap!")
            print("Usage: python shopee_bot.py <session_id> <viewers> <delay>")
            print(f"[DEBUG] Received {len(sys.argv)} arguments: {sys.argv}")
            input("Press any key to exit...")
            sys.exit(1)
        
        try:
            session_id = str(sys.argv[1])
            max_viewers = int(sys.argv[2])  
            delay_seconds = int(sys.argv[3])
        except (ValueError, IndexError) as e:
            print(f"ERROR: Invalid parameters: {e}")
            print(f"[DEBUG] Args received: {sys.argv}")
            input("Press any key to exit...")
            sys.exit(1)
        
        print(f"[DEBUG] Parsed parameters: session={session_id}, viewers={max_viewers}, delay={delay_seconds}")
        
        if session_id == "test_session":
            print("[DEBUG] Test mode detected - exiting early")
            print("INFO: Bot script working - test mode completed")
            return 0
        
        print(f"TARGET: {max_viewers} viewers untuk session {session_id}")
        print(f"URL: https://live.shopee.co.id/share?from=live&session={session_id}&in=1")
        print()
        
        # Ambil profile yang tersedia
        print("[DEBUG] Loading profiles from temp_profiles.json...")
        print(f"[DEBUG] Current working directory: {os.getcwd()}")
        
        available_profiles = get_available_profiles()
        
        if not available_profiles:
            print("ERROR: Tidak ada profile Google Chrome yang ditemukan!")
            print("[DEBUG] temp_profiles.json is empty or missing")
            print("[DEBUG] Please run detect_profiles.py first to generate profiles")
            print("")
            print("Generating profiles now...")
            
            # Try to generate profiles
            import subprocess
            result = subprocess.run([sys.executable, 'scripts/detect_profiles_clean.py'], 
                                  capture_output=True, text=True, cwd='.')
            if result.returncode == 0:
                print("Profile generation successful!")
                with open('temp_profiles.json', 'w') as f:
                    f.write(result.stdout)
                # Try to read again
                available_profiles = get_available_profiles()
                if not available_profiles:
                    print("Still no profiles found after generation!")
                    input("Press any key to exit...")
                    sys.exit(1)
            else:
                print(f"Profile generation failed: {result.stderr}")
                input("Press any key to exit...")
                sys.exit(1)
        
        print(f"INFO: Ditemukan {len(available_profiles)} profile Chrome:")
        for i, profile in enumerate(available_profiles):
            email = profile.get('email', 'Unknown')
            display_name = profile.get('display_name', profile.get('name', 'Unknown'))
            profile_name = profile.get('name', 'Unknown')
            
            if email != 'Unknown' and '@' in email:
                print(f"   {i+1}. {email} ({display_name}) - {profile_name}")
            else:
                print(f"   {i+1}. {display_name} - {profile_name} [NO EMAIL]")
        print()
        
        viewers = []
        live_url = f"https://live.shopee.co.id/share?from=live&session={session_id}&in=1"
        
        try:
            for i in range(min(max_viewers, len(available_profiles))):
                profile = available_profiles[i]
                device_id = generate_device_id()
                
                email = profile.get('email', 'Unknown')
                display_name = profile.get('display_name', profile.get('name', 'Unknown'))
                profile_name = profile.get('name', 'Unknown')
                
                if email != 'Unknown' and '@' in email:
                    print(f"STARTING: Memulai viewer #{i+1}: {email} ({display_name})")
                else:
                    print(f"STARTING: Memulai viewer #{i+1}: {display_name}")
                    
                print(f"   Device ID: {device_id[:8]}...{device_id[-4:]}")
                print(f"   Profile: {profile_name}")
                
                # Buat Chrome instance dengan profile
                print(f"   [DEBUG] Creating Chrome instance with profile: {profile['path']}")
                driver = create_chrome_with_profile(profile, device_id, i)
                
                if driver is None:
                    print(f"ERROR: Gagal membuat viewer #{i+1}")
                    continue
                
                # Try to restore Google session
                print(f"   [INFO] Attempting to restore login session...")
                inject_google_login(driver, email)
                
                # Inject device fingerprint
                inject_device_fingerprint(driver, device_id)
                
                # Akses Shopee Live
                print(f"   [INFO] Accessing Shopee Live...")
                driver.get(live_url)
                
                # Tunggu halaman load
                time.sleep(3)
                
                print(f"SUCCESS: Viewer #{i+1} aktif dan menonton stream")
                viewers.append({
                    'driver': driver,
                    'profile': profile,
                    'device_id': device_id
                })
                
                # Delay antar viewer
                if i < max_viewers - 1:
                    print(f"   [INFO] Waiting {delay_seconds} seconds before next viewer...")
                    time.sleep(delay_seconds)
            
            print()
            print(f"SUCCESS: {len(viewers)} viewers berhasil dimulai!")
            print("Bot berjalan... Tekan Ctrl+C untuk stop")
            
            # Keep alive loop
            try:
                while True:
                    time.sleep(30)
                    print(f"[INFO] {len(viewers)} viewers masih aktif - {time.strftime('%H:%M:%S')}")
                    
            except KeyboardInterrupt:
                print("\n[INFO] Stopping bot...")
                
        except Exception as e:
            print(f"[ERROR] Bot execution error: {e}")
            import traceback
            traceback.print_exc()
            
        finally:
            # Cleanup
            print("[INFO] Cleaning up Chrome instances...")
            for viewer in viewers:
                try:
                    viewer['driver'].quit()
                except:
                    pass
            print("[INFO] Cleanup completed")
    
    except Exception as e:
        print(f"[CRITICAL ERROR] Main function error: {e}")
        import traceback
        traceback.print_exc()
        input("Press any key to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()
