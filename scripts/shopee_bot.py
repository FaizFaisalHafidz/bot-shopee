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
        print("[DEBUG] Trying to read temp_profiles.json...")
        if not os.path.exists('temp_profiles.json'):
            print("[ERROR] temp_profiles.json file not found!")
            print("[DEBUG] Current directory:", os.getcwd())
            print("[DEBUG] Files in current directory:", [f for f in os.listdir('.') if not f.startswith('.')])
            return []
            
        with open('temp_profiles.json', 'r', encoding='utf-8') as f:
            content = f.read()
            print(f"[DEBUG] File content length: {len(content)} characters")
            if not content.strip():
                print("[ERROR] temp_profiles.json is empty!")
                return []
                
        with open('temp_profiles.json', 'r', encoding='utf-8') as f:
            profiles = json.load(f)
            print(f"[DEBUG] Loaded {len(profiles)} profiles from JSON")
            return profiles
    except json.JSONDecodeError as e:
        print(f"[ERROR] JSON decode error: {e}")
        return []
    except Exception as e:
        print(f"[ERROR] Error reading profiles: {e}")
        return []

def create_chrome_with_profile(profile_path, device_id, viewer_num):
    """Buat Chrome instance dengan profile spesifik dan device ID"""
    try:
        print(f"   [DEBUG] Setting up Chrome for viewer #{viewer_num+1}")
        
        options = Options()
        options.add_argument(f'--user-data-dir={profile_path}')
        options.add_argument(f'--remote-debugging-port={9222 + viewer_num}')
        options.add_argument('--no-first-run')
        options.add_argument('--no-default-browser-check')
        options.add_argument('--disable-default-apps')
        options.add_argument('--disable-extensions-file-access-check')
        options.add_argument('--disable-extensions-http-throttling')
        options.add_argument('--disable-extensions-https-throttling')
        
        # Anti-detection options
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option("detach", True)
        
        # Create WebDriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        # Remove automation indicators
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print(f"   [SUCCESS] Chrome instance created for viewer #{viewer_num+1}")
        return driver
        
    except Exception as e:
        print(f"   [ERROR] Failed to create Chrome instance: {e}")
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
            result = subprocess.run([sys.executable, 'scripts/detect_profiles.py'], 
                                  capture_output=True, text=True, cwd='.')
            if result.returncode == 0:
                print("Profile generation successful!")
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
            print(f"   {i+1}. {profile.get('email', 'Unknown')} - {profile.get('name', 'Unknown')}")
        print()
        
        viewers = []
        live_url = f"https://live.shopee.co.id/share?from=live&session={session_id}&in=1"
        
        try:
            for i in range(min(max_viewers, len(available_profiles))):
                profile = available_profiles[i]
                device_id = generate_device_id()
                
                print(f"STARTING: Memulai viewer #{i+1}: {profile['email']}")
                print(f"   Device ID: {device_id[:8]}...{device_id[-4:]}")
                print(f"   Profile: {profile['name']}")
                
                # Buat Chrome instance dengan profile
                print(f"   [DEBUG] Creating Chrome instance with profile: {profile['path']}")
                driver = create_chrome_with_profile(profile['path'], device_id, i)
                
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
