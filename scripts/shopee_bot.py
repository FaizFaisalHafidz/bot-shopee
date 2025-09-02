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
        # Skip temp profiles - langsung pakai original profiles
        print("[INFO] Loading Gmail profiles only (filtering out System Profile)...")
        
        # Read temp_profiles.json directly
        profiles_file = '../temp_profiles.json' if os.path.exists('../temp_profiles.json') else 'temp_profiles.json'
        
        print(f"[DEBUG] Reading profiles from: {profiles_file}")
        if not os.path.exists(profiles_file):
            print("[ERROR] Profile file not found!")
            print("[DEBUG] Current directory:", os.getcwd())
            return []
            
        with open(profiles_file, 'r', encoding='utf-8') as f:
            all_profiles = json.load(f)
            print(f"[DEBUG] Total profiles loaded: {len(all_profiles)}")
            
            # STRICT filtering - hanya Gmail accounts yang valid
            gmail_profiles = []
            for i, profile in enumerate(all_profiles):
                email = profile.get('email', '')
                display_name = profile.get('display_name', '')
                name = profile.get('name', '')
                path = profile.get('path', '')
                
                print(f"[{i+1}] Checking profile:")
                print(f"    Name: {name}")
                print(f"    Email: {email}")
                print(f"    Display: {display_name}")
                
                # STRICT conditions untuk valid Gmail profile - FIXED cross platform
                is_gmail = email.endswith('@gmail.com')
                is_not_system = name != 'System Profile' and name != 'Guest Profile'
                is_not_unknown = email != 'Unknown' and email != ''
                has_valid_path = len(path.strip()) > 0  # Any valid path
                
                if is_gmail and is_not_system and is_not_unknown and has_valid_path:
                    gmail_profiles.append(profile)
                    print(f"    Status: ✅ ACCEPTED (Gmail account)")
                else:
                    print(f"    Status: ❌ REJECTED (Gmail:{is_gmail}, NotSystem:{is_not_system}, NotUnknown:{is_not_unknown}, ValidPath:{has_valid_path})")
                print()
            
            print(f"[FINAL] Valid Gmail profiles: {len(gmail_profiles)} out of {len(all_profiles)}")
            
            if len(gmail_profiles) == 0:
                print("[ERROR] No valid Gmail profiles found!")
                print("[INFO] Make sure you have Chrome profiles logged into Gmail accounts")
                return []
            
            return gmail_profiles
            
    except Exception as e:
        print(f"[ERROR] Failed to load profiles: {e}")
        import traceback
        print("[DEBUG] Full error traceback:")
        traceback.print_exc()
        return []
    except json.JSONDecodeError as e:
        print(f"[ERROR] JSON decode error: {e}")
        return []
    except Exception as e:
        print(f"[ERROR] Error reading profiles: {e}")
        return []

def kill_chrome_processes():
    """Kill all Chrome processes to avoid conflicts"""
    try:
        if os.name == 'nt':  # Windows
            print("[INFO] Killing Chrome processes on Windows...")
            import subprocess
            result = subprocess.run(['taskkill', '/f', '/im', 'chrome.exe', '/t'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("[SUCCESS] Chrome processes terminated")
            else:
                print("[INFO] No Chrome processes found or already terminated")
        else:  # macOS/Linux
            print("[INFO] Killing Chrome processes on Unix...")
            import subprocess
            subprocess.run(['pkill', '-f', 'Google Chrome'], capture_output=True)
            subprocess.run(['pkill', '-f', 'chrome'], capture_output=True)
            print("[SUCCESS] Chrome processes terminated")
        
        # Wait for processes to fully terminate
        time.sleep(3)
        
    except Exception as e:
        print(f"[WARNING] Could not kill Chrome processes: {e}")
        print("[INFO] Continuing anyway...")

def create_chrome_with_profile(profile_data, device_id, viewer_num):
    """Buat Chrome instance menggunakan profile yang sudah login"""
    try:
        print(f"   [DEBUG] Setting up Chrome for viewer #{viewer_num+1}")
        
        # Extract profile information
        if isinstance(profile_data, dict):
            original_profile_path = profile_data.get('path')
            email = profile_data.get('email', 'Unknown')
            display_name = profile_data.get('display_name', 'Unknown')
            name = profile_data.get('name', 'Unknown')
            print(f"   [INFO] Using existing profile: {email} ({display_name})")
            print(f"   [DEBUG] Profile path: {original_profile_path}")
        else:
            print("[ERROR] Invalid profile data")
            return None
        
        options = Options()
        
        # IMPORTANT: Use existing Chrome profile directly
        # This preserves login sessions
        if os.name == 'nt':  # Windows
            # Convert macOS path to Windows path if needed
            if original_profile_path.startswith('/Users/'):
                # This is a macOS path, need to convert to Windows
                print(f"   [DEBUG] Converting macOS path to Windows path")
                profile_name = name
                if profile_name.lower() == 'default':
                    user_data_dir = r"C:\Users\Administrator\AppData\Local\Google\Chrome\User Data"
                    options.add_argument(f'--user-data-dir="{user_data_dir}"')
                else:
                    user_data_dir = r"C:\Users\Administrator\AppData\Local\Google\Chrome\User Data"
                    options.add_argument(f'--user-data-dir="{user_data_dir}"')
                    options.add_argument(f'--profile-directory="{profile_name}"')
                
                print(f"   [DEBUG] Windows User Data: {user_data_dir}")
                print(f"   [DEBUG] Profile Directory: {profile_name}")
            elif "User Data" in original_profile_path:
                # Already Windows path
                user_data_dir = original_profile_path.split("User Data")[0] + "User Data"
                profile_name = original_profile_path.split("User Data")[-1].strip("\\/")
                
                print(f"   [DEBUG] Windows Chrome User Data: {user_data_dir}")
                print(f"   [DEBUG] Profile Directory: {profile_name}")
                
                options.add_argument(f'--user-data-dir="{user_data_dir}"')
                if profile_name and profile_name.lower() != "default":
                    options.add_argument(f'--profile-directory="{profile_name}"')
            else:
                print(f"   [WARNING] Unexpected Windows profile path: {original_profile_path}")
                # Fallback: construct Windows path from profile name
                profile_name = name
                user_data_dir = r"C:\Users\Administrator\AppData\Local\Google\Chrome\User Data"
                options.add_argument(f'--user-data-dir="{user_data_dir}"')
                if profile_name.lower() != "default":
                    options.add_argument(f'--profile-directory="{profile_name}"')
        else:  # macOS/Linux  
            # For macOS: /Users/.../Google/Chrome/Profile 1
            if "Chrome" in original_profile_path:
                # Extract User Data equivalent directory
                parts = original_profile_path.split("Chrome")
                if len(parts) >= 2:
                    user_data_dir = parts[0] + "Chrome"
                    profile_name = parts[1].strip("/")
                    
                    print(f"   [DEBUG] macOS Chrome Data: {user_data_dir}")
                    print(f"   [DEBUG] Profile Directory: {profile_name}")
                    
                    options.add_argument(f'--user-data-dir="{user_data_dir}"')
                    if profile_name and profile_name.lower() != "default":
                        options.add_argument(f'--profile-directory="{profile_name}"')
                else:
                    options.add_argument(f'--user-data-dir="{original_profile_path}"')
            else:
                options.add_argument(f'--user-data-dir="{original_profile_path}"')
        
        # Unique debugging port
        debug_port = 9222 + viewer_num
        options.add_argument(f'--remote-debugging-port={debug_port}')
        
        # Chrome options to preserve existing sessions
        options.add_argument('--no-first-run')
        options.add_argument('--no-default-browser-check')
        options.add_argument('--disable-default-apps')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        
        # CRITICAL: Don't disable web security - it breaks login sessions
        # options.add_argument('--disable-web-security')  # REMOVED
        
        # Anti-detection
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option("detach", True)
        
        # Find Chrome executable (NOT Chromium)
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
                "/usr/bin/chrome"
            ]
        
        for path in possible_paths:
            if os.path.exists(path):
                chrome_executable = path
                print(f"   [DEBUG] Found Chrome executable: {path}")
                break
        
        if chrome_executable:
            options.binary_location = chrome_executable
            print(f"   [SUCCESS] Using actual Chrome (not Chromium)")
        else:
            print(f"   [WARNING] Chrome executable not found, may use Chromium")
        
        # Create driver with existing profile
        try:
            service = Service()
            driver = webdriver.Chrome(service=service, options=options)
            print(f"   [SUCCESS] Chrome launched with existing profile for {email}")
        except Exception as e:
            print(f"   [DEBUG] System chromedriver failed: {e}")
            try:
                from webdriver_manager.chrome import ChromeDriverManager
                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=options)
                print(f"   [SUCCESS] Chrome launched via ChromeDriverManager for {email}")
            except Exception as e2:
                print(f"   [ERROR] Both chromedriver methods failed: {e2}")
                return None
        
        # Remove automation indicators
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print(f"   [INFO] Chrome should now show existing login for: {email}")
        return driver
        
    except Exception as e:
        print(f"   [ERROR] Failed to create Chrome: {e}")
        import traceback
        print("[DEBUG] Full error:")
        traceback.print_exc()
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
        
        # Kill any existing Chrome processes first
        print("[INFO] Preparing Chrome environment...")
        kill_chrome_processes()
        
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
                print(f"   [DEBUG] Creating Chrome instance for viewer #{i+1}")
                driver = create_chrome_with_profile(profile, device_id, i)
                
                if driver is None:
                    print(f"ERROR: Gagal membuat viewer #{i+1}")
                    continue
                
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
