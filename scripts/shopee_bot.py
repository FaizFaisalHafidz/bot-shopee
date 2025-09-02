import sys
import os
import time
import random
import string
import json
from pathlib import Path

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
    print(f"❌ Import error: {e}")
    input("Tekan Enter untuk keluar...")
    sys.exit(1)

def generate_device_id():
    """Generate unique 32-character device ID"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=32))

def get_available_profiles():
    """Ambil daftar profile Chrome yang sudah dideteksi"""
    try:
        with open('temp_profiles.json', 'r', encoding='utf-8') as f:
            profiles = json.load(f)
        return profiles
    except:
        return []

def create_chrome_with_profile(profile_path, device_id, position):
    """Buat instance Chrome dengan profile Google yang ada"""
    options = Options()
    
    # Gunakan profile yang sudah ada
    options.add_argument(f"--user-data-dir={profile_path}")
    
    # Anti-detection settings
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # Disable notifications
    prefs = {
        "profile.default_content_setting_values.notifications": 2,
        "profile.default_content_settings.popups": 0
    }
    options.add_experimental_option("prefs", prefs)
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        # Set window position dan size
        x_pos = (position % 4) * 350
        y_pos = (position // 4) * 300
        driver.set_window_position(x_pos, y_pos)
        driver.set_window_size(400, 300)
        
        return driver
        
    except Exception as e:
        print(f"❌ Gagal membuat Chrome instance: {e}")
        return None

def inject_device_fingerprint(driver, device_id):
    """Inject device fingerprint ke browser"""
    fingerprint_script = f"""
    // Set device ID di localStorage
    localStorage.setItem('device_id', '{device_id}');
    localStorage.setItem('shopee_device_id', '{device_id}');
    localStorage.setItem('SPC_device_id', '{device_id}');
    
    // Override navigator properties
    Object.defineProperty(navigator, 'deviceMemory', {{
        get: () => {random.choice([4, 8, 16])}
    }});
    
    Object.defineProperty(navigator, 'hardwareConcurrency', {{
        get: () => {random.choice([4, 6, 8, 12])}
    }});
    
    // Override screen properties
    Object.defineProperty(screen, 'width', {{
        get: () => {random.choice([1920, 1366, 1440, 1680])}
    }});
    
    Object.defineProperty(screen, 'height', {{
        get: () => {random.choice([1080, 768, 900, 1050])}
    }});
    
    console.log('🔧 Device fingerprint injected:', '{device_id}');
    """
    
    try:
        driver.execute_script(fingerprint_script)
        return True
    except Exception as e:
        print(f"⚠️  Warning: Gagal inject fingerprint - {e}")
        return False

def main():
    try:
        print("[DEBUG] Starting shopee_bot.py...")
        
        # Ambil parameter dari command line
        if len(sys.argv) < 4:
            print("❌ Parameter tidak lengkap!")
            print("Usage: python shopee_bot.py <session_id> <viewers> <delay>")
            print(f"[DEBUG] Received {len(sys.argv)} arguments: {sys.argv}")
            input("Tekan Enter untuk keluar...")
            return
        
        session_id = sys.argv[1]
        max_viewers = int(sys.argv[2])
        delay_seconds = int(sys.argv[3])
        
        print(f"[DEBUG] Parameters: session={session_id}, viewers={max_viewers}, delay={delay_seconds}")
        
        print(f"🎯 Target: {max_viewers} viewers untuk session {session_id}")
        print(f"📺 URL: https://live.shopee.co.id/share?from=live&session={session_id}&in=1")
        print()
        
        # Ambil profile yang tersedia
        print("[DEBUG] Loading profiles from temp_profiles.json...")
        available_profiles = get_available_profiles()
        
        if not available_profiles:
            print("❌ Tidak ada profile Google Chrome yang ditemukan!")
            print("[DEBUG] temp_profiles.json is empty or missing")
            input("Tekan Enter untuk keluar...")
            return
        
        print(f"📋 Ditemukan {len(available_profiles)} profile Chrome:")
        for i, profile in enumerate(available_profiles):
            print(f"   {i+1}. {profile['email']}")
        print()
        
        viewers = []
        live_url = f"https://live.shopee.co.id/share?from=live&session={session_id}&in=1"
        
        try:
            for i in range(min(max_viewers, len(available_profiles))):
                profile = available_profiles[i]
                device_id = generate_device_id()
                
                print(f"🚀 Memulai viewer #{i+1}: {profile['email']}")
                print(f"   📱 Device ID: {device_id[:8]}...{device_id[-4:]}")
                print(f"   📁 Profile: {profile['name']}")
                
                # Buat Chrome instance dengan profile
                print(f"   [DEBUG] Creating Chrome instance with profile: {profile['path']}")
                driver = create_chrome_with_profile(profile['path'], device_id, i)
                
                if driver is None:
                    print(f"❌ Gagal membuat viewer #{i+1}")
                    continue
                
                try:
                    # Buka Shopee untuk set device fingerprint
                    print(f"   🔧 Setting device fingerprint...")
                    driver.get("https://shopee.co.id")
                    time.sleep(2)
                    
                    # Inject device fingerprint
                    if inject_device_fingerprint(driver, device_id):
                        print(f"   ✅ Device fingerprint berhasil di-inject")
                    else:
                        print(f"   ⚠️  Warning: Device fingerprint gagal di-inject")
                    
                    # Buka live stream
                    print(f"   🎥 Membuka live stream...")
                    driver.get(live_url)
                    time.sleep(3)
                    
                    viewers.append({
                        'driver': driver,
                        'email': profile['email'],
                        'device_id': device_id,
                        'number': i+1
                    })
                    
                    print(f"   ✅ Viewer #{i+1} berhasil terhubung!")
                    print()
                    
                    # Delay sebelum viewer berikutnya
                    if i < min(max_viewers, len(available_profiles)) - 1:
                        print(f"⏱️  Menunggu {delay_seconds} detik sebelum viewer berikutnya...")
                        time.sleep(delay_seconds)
                    
                except Exception as e:
                    print(f"❌ Error pada viewer #{i+1}: {e}")
                    print(f"[DEBUG] Full error: {str(e)}")
                    try:
                        driver.quit()
                    except:
                        pass
            
            if not viewers:
                print("❌ Tidak ada viewers yang berhasil dibuat!")
                input("Tekan Enter untuk keluar...")
                return
            
            print("="*60)
            print(f"🎉 SEMUA {len(viewers)} VIEWERS BERHASIL DIMULAI!")
            print("="*60)
            print()
            
            print("📋 DETAIL VIEWERS:")
            for viewer in viewers:
                print(f"   👤 Viewer #{viewer['number']}: {viewer['email']}")
                print(f"      📱 Device ID: {viewer['device_id']}")
            print()
            
            print("🎯 Bot sedang berjalan! Cek live stream Anda - jumlah viewer seharusnya bertambah!")
            print("💡 Jangan tutup jendela Chrome yang terbuka.")
            print("🛑 Tekan Ctrl+C untuk menghentikan bot...")
            print()
            
            # Monitor viewers
            while True:
                time.sleep(30)  # Cek setiap 30 detik
                
                active_count = 0
                for viewer in viewers:
                    try:
                        # Cek apakah browser masih aktif
                        if viewer['driver'].window_handles:
                            active_count += 1
                    except:
                        pass
                
                print(f"📊 Status: {active_count}/{len(viewers)} viewers masih aktif - {time.strftime('%H:%M:%S')}")
                
                if active_count == 0:
                    print("⚠️  Semua viewers sudah tidak aktif.")
                    break
            
        except KeyboardInterrupt:
            print("\n🛑 Bot dihentikan oleh user...")
        except Exception as e:
            print(f"\n❌ Error during bot execution: {e}")
            import traceback
            traceback.print_exc()
        finally:
            # Cleanup
            print("🧹 Membersihkan viewers...")
            for viewer in viewers:
                try:
                    viewer['driver'].quit()
                    print(f"   ✅ Viewer {viewer['email']} ditutup")
                except Exception as e:
                    print(f"   ⚠️  Error closing viewer: {e}")
            print("✅ Semua viewers berhasil ditutup. Bot selesai.")
            print()
            input("Tekan Enter untuk keluar...")
    
    except Exception as e:
        print(f"[ERROR] Fatal error in main(): {e}")
        import traceback
        traceback.print_exc()
        input("Tekan Enter untuk keluar...")

if __name__ == "__main__":
    main()
