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
            profile_path = profile_data.get('path')
            email = profile_data.get('email', 'Unknown')
            name = profile_data.get('name', 'Unknown')
            print(f"   [DEBUG] Using profile: {email} ({name})")
        else:
            # Backward compatibility
            profile_path = profile_data
            email = 'Unknown'
            
        print(f"   [DEBUG] Profile path: {profile_path}")
        
        options = Options()
        
        # For Windows Chrome User Data structure
        # Path: C:\Users\...\Chrome\User Data\Default or Profile 1
        if "User Data" in profile_path:
            user_data_dir = profile_path.split("User Data")[0] + "User Data"
            profile_name = profile_path.split("User Data")[-1].strip("\\/")
            
            print(f"   [DEBUG] User Data Dir: {user_data_dir}")
            print(f"   [DEBUG] Profile Directory: {profile_name}")
            
            options.add_argument(f'--user-data-dir="{user_data_dir}"')
            if profile_name and profile_name != "Default":
                options.add_argument(f'--profile-directory="{profile_name}"')
        else:
            # For other profile structures
            options.add_argument(f'--user-data-dir="{profile_path}"')
        
        # Unique debugging port for each instance
        debug_port = 9222 + viewer_num
        options.add_argument(f'--remote-debugging-port={debug_port}')
        
        # Chrome options to preserve login state
        options.add_argument('--no-first-run')
        options.add_argument('--no-default-browser-check')
        options.add_argument('--disable-default-apps')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-web-security')
        options.add_argument('--allow-running-insecure-content')
        
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
            print(f"   [SUCCESS] Chrome launched for {email}")
        except Exception as e:
            print(f"   [DEBUG] System chromedriver failed, trying ChromeDriverManager...")
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            print(f"   [SUCCESS] Chrome launched for {email} (via ChromeDriverManager)")
        
        # Remove automation indicators
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
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
