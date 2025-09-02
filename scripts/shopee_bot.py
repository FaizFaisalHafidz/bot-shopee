import sys
import os
import time
import random
import string
import json
import platform
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

def convert_profile_path_for_os(original_path, profile_name):
    """
    Convert profile path based on current OS
    macOS: /Users/username/Library/Application Support/Google/Chrome/Profile X
    Windows: C:\\Users\\username\\AppData\\Local\\Google\\Chrome\\User Data\\Profile X
    """
    current_os = platform.system().lower()
    print(f"   [DEBUG] Current OS: {current_os}")
    print(f"   [DEBUG] Original profile path: {original_path}")
    print(f"   [DEBUG] Profile name: {profile_name}")
    
    if current_os == "windows":
        # Always use Windows format for Windows
        username = os.environ.get('USERNAME', 'Administrator')
        user_data_dir = rf"C:\Users\{username}\AppData\Local\Google\Chrome\User Data"
        
        if profile_name.lower() == 'default':
            print(f"   [DEBUG] Using Default profile on Windows: {user_data_dir}")
            return user_data_dir, None  # No profile directory needed for Default
        else:
            print(f"   [DEBUG] Using Windows profile: {user_data_dir} + {profile_name}")
            return user_data_dir, profile_name
            
    elif current_os == "darwin":  # macOS
        # Always use macOS format for macOS
        username = os.environ.get('USER', 'flashcode')
        user_data_dir = f"/Users/{username}/Library/Application Support/Google/Chrome"
        
        if profile_name.lower() == 'default':
            print(f"   [DEBUG] Using Default profile on macOS: {user_data_dir}")
            return user_data_dir, None
        else:
            print(f"   [DEBUG] Using macOS profile: {user_data_dir}/{profile_name}")
            return user_data_dir, profile_name
    
    # Fallback
    print(f"   [WARNING] Unknown OS, using original path")
    return original_path, profile_name

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

def check_chrome_installation():
    """Check Chrome installation and return status"""
    chrome_paths = []
    
    if os.name == 'nt':  # Windows
        possible_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe"),
            r"C:\Users\Administrator\AppData\Local\Google\Chrome\Application\chrome.exe"
        ]
    else:  # macOS/Linux
        possible_paths = [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/usr/bin/google-chrome",
            "/usr/bin/chrome"
        ]
    
    for path in possible_paths:
        if os.path.exists(path):
            chrome_paths.append(path)
    
    return chrome_paths

def create_chrome_with_profile(profile_data, device_id, viewer_num):
    """Buat Chrome instance dengan existing profile yang sudah login"""
    try:
        print(f"   [DEBUG] Setting up Chrome for viewer #{viewer_num+1}")
        
        # Extract profile information
        if isinstance(profile_data, dict):
            email = profile_data.get('email', 'Unknown')
            display_name = profile_data.get('display_name', 'Unknown')
            profile_path = profile_data.get('path', '')
            profile_name = profile_data.get('name', 'Default')
            print(f"   [INFO] Using EXISTING profile: {email} ({display_name})")
            print(f"   [DEBUG] Profile: {profile_name}")
        else:
            print("[ERROR] Invalid profile data")
            return None
        
        options = Options()
        
        # Use existing Chrome profile with login
        if os.name == 'nt':  # Windows
            user_data_dir = r"C:\Users\Administrator\AppData\Local\Google\Chrome\User Data"
            profile_directory = profile_name
        else:  # macOS/Linux
            user_data_dir = os.path.expanduser("~/Library/Application Support/Google/Chrome")
            profile_directory = profile_name
        
        print(f"   [DEBUG] User Data Dir: {user_data_dir}")
        print(f"   [DEBUG] Profile Directory: {profile_directory}")
        
        # Verify paths exist
        profile_full_path = os.path.join(user_data_dir, profile_directory)
        if os.path.exists(user_data_dir):
            print(f"   [DEBUG] ✅ User Data directory exists")
        else:
            print(f"   [WARNING] ❌ User Data directory NOT found")
            
        if os.path.exists(profile_full_path):
            print(f"   [DEBUG] ✅ Profile directory exists: {profile_full_path}")
        else:
            print(f"   [WARNING] ❌ Profile directory NOT found: {profile_full_path}")
            # List available profiles for debugging
            if os.path.exists(user_data_dir):
                available_profiles = [d for d in os.listdir(user_data_dir) if os.path.isdir(os.path.join(user_data_dir, d))]
                print(f"   [DEBUG] Available profiles: {available_profiles[:5]}...")  # Show first 5
        
        # Simplified Chrome options - minimize conflicts
        options.add_argument(f'--user-data-dir={user_data_dir}')
        options.add_argument(f'--profile-directory={profile_directory}')
        options.add_argument(f'--remote-debugging-port={9222 + viewer_num}')
        
        # Essential stability options
        options.add_argument('--no-first-run')
        options.add_argument('--no-default-browser-check')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-extensions')
        
        # Windows RDP compatibility
        if os.name == 'nt':
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-software-rasterizer')
        
        # Anti-detection
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option("detach", True)
        
        # Enhanced Chrome detection - MUST WORK!
        chrome_paths = check_chrome_installation()
        
        if not chrome_paths:
            print(f"   [CRITICAL ERROR] No Chrome installation found!")
            print(f"   [EMERGENCY] Searching system for any Chrome...")
            
            # Emergency Chrome search
            if os.name == 'nt':
                import glob
                emergency_paths = []
                # Search all drives and common locations
                search_patterns = [
                    r"C:\**\Google\Chrome\Application\chrome.exe",
                    r"D:\**\Google\Chrome\Application\chrome.exe", 
                    r"*:\Program Files*\Google\Chrome\Application\chrome.exe"
                ]
                
                for pattern in search_patterns:
                    try:
                        emergency_paths.extend(glob.glob(pattern, recursive=True))
                    except:
                        pass
                        
                if emergency_paths:
                    chrome_executable = emergency_paths[0]
                    print(f"   [EMERGENCY SUCCESS] Found Chrome: {chrome_executable}")
                else:
                    print(f"   [FATAL] No Chrome found anywhere - using default browser")
                    chrome_executable = None
            else:
                chrome_executable = None
        else:
            chrome_executable = chrome_paths[0]  # Use first found Chrome
            print(f"   [SUCCESS] Using Chrome: {chrome_executable}")
            
        # Set Chrome binary
        if chrome_executable:
            options.binary_location = chrome_executable
            print(f"   [CONFIRMED] Chrome binary set: {chrome_executable}")
            
            # Verify this is actual Chrome, not Chromium
            if "chromium" in chrome_executable.lower():
                print(f"   [WARNING] Detected Chromium path, will use auth bypass")
                use_auth_bypass = True
            else:
                print(f"   [SUCCESS] Confirmed Google Chrome installation")
                use_auth_bypass = False
        else:
            print(f"   [WARNING] No Chrome binary - using system default + auth bypass")
            use_auth_bypass = True
        
        # Create driver with most stable approach
        driver = None
        
        # Method 1: Try without webdriver-manager (direct system driver)
        try:
            print(f"   [DEBUG] Attempting system ChromeDriver...")
            driver = webdriver.Chrome(options=options)
            print(f"   [SUCCESS] System ChromeDriver worked!")
            
        except Exception as e:
            print(f"   [DEBUG] System driver failed: {str(e)[:100]}...")
            
            # Method 2: Try webdriver-manager as fallback
            try:
                print(f"   [DEBUG] Attempting ChromeDriverManager...")
                from webdriver_manager.chrome import ChromeDriverManager
                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=options)
                print(f"   [SUCCESS] ChromeDriverManager worked!")
                
            except Exception as e2:
                print(f"   [ERROR] All driver methods failed:")
                print(f"   System: {str(e)[:80]}")
                print(f"   Manager: {str(e2)[:80]}")
                
                # Method 3: Last resort - try minimal options
                try:
                    print(f"   [DEBUG] Trying minimal Chrome options...")
                    minimal_options = Options()
                    minimal_options.add_argument(f'--user-data-dir={user_data_dir}')
                    minimal_options.add_argument(f'--profile-directory={profile_directory}')
                    if chrome_executable:
                        minimal_options.binary_location = chrome_executable
                    
                    driver = webdriver.Chrome(options=minimal_options)
                    print(f"   [SUCCESS] Minimal options worked!")
                    
                except Exception as e3:
                    print(f"   [FINAL ERROR] All methods failed: {str(e3)[:80]}")
                    return None
        
        # Remove automation indicators and add auth bypass
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        # Smart auth bypass based on browser type
        if use_auth_bypass:
            print(f"   [BYPASS] Attempting authentication bypass for: {email}")
            try:
                # Method 1: Try existing profile first
                driver.get("https://accounts.google.com/")
                time.sleep(2)
                
                # Check if already logged in
                if "myaccount.google.com" in driver.current_url or "accounts.google.com/signin" not in driver.current_url:
                    print(f"   [BYPASS] Already logged in - profile worked!")
                else:
                    print(f"   [BYPASS] Not logged in - attempting auto-login")
                    
                    # Navigate to login page
                    driver.get("https://accounts.google.com/signin")
                    time.sleep(3)
                    
                    # Enhanced auth bypass script
                    bypass_script = """
                    // Enhanced login bypass
                    function attemptLogin(email) {
                        console.log('[BYPASS] Starting login attempt for:', email);
                        
                        // Find email input
                        const emailSelectors = [
                            'input[type="email"]',
                            'input[name="identifier"]',
                            '#identifierId',
                            'input[aria-label*="email"]'
                        ];
                        
                        let emailInput = null;
                        for (let selector of emailSelectors) {
                            emailInput = document.querySelector(selector);
                            if (emailInput) break;
                        }
                        
                        if (emailInput && email) {
                            emailInput.value = email;
                            emailInput.dispatchEvent(new Event('input', { bubbles: true }));
                            emailInput.dispatchEvent(new Event('change', { bubbles: true }));
                            
                            console.log('[BYPASS] Email filled:', email);
                            
                            // Find and click next button
                            setTimeout(() => {
                                const nextSelectors = [
                                    '#identifierNext',
                                    'button[type="submit"]',
                                    'input[type="submit"]',
                                    'button:contains("Next")',
                                    '[data-primary-action-label]'
                                ];
                                
                                let nextBtn = null;
                                for (let selector of nextSelectors) {
                                    nextBtn = document.querySelector(selector);
                                    if (nextBtn) break;
                                }
                                
                                if (nextBtn) {
                                    nextBtn.click();
                                    console.log('[BYPASS] Next button clicked');
                                } else {
                                    // Try finding by text
                                    const buttons = document.querySelectorAll('button');
                                    for (let btn of buttons) {
                                        if (btn.textContent.includes('Next') || btn.textContent.includes('Berikutnya')) {
                                            btn.click();
                                            console.log('[BYPASS] Next button found by text');
                                            break;
                                        }
                                    }
                                }
                            }, 1000);
                            
                            return true;
                        }
                        
                        console.log('[BYPASS] Could not find email input');
                        return false;
                    }
                    
                    return attemptLogin(arguments[0]);
                    """
                    
                    result = driver.execute_script(bypass_script, email)
                    print(f"   [BYPASS] Auto-login script executed: {result}")
                    
                    # Wait for potential auto-actions
                    time.sleep(5)
                    
                    # Check if we need to handle password
                    current_url = driver.current_url
                    if "password" in current_url.lower() or "signin/challenge" in current_url:
                        print(f"   [BYPASS] Password step detected - manual intervention needed")
                        print(f"   [INFO] Please complete login manually in the browser")
                        print(f"   [INFO] Bot will wait 30 seconds for manual login...")
                        time.sleep(30)
                
            except Exception as bypass_error:
                print(f"   [WARNING] Auth bypass failed: {bypass_error}")
                print(f"   [INFO] Continuing with manual login if needed")
        else:
            print(f"   [INFO] Using existing Chrome profile - should be pre-logged in")
        
        print(f"   [SUCCESS] Chrome opened with profile: {email}")
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
