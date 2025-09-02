@echo off
chcp 65001 >nul
title Bot Shopee Live - Menggunakan Profile Google Chrome
color 0A
cls

echo.
echo ================================================
echo        BOT SHOPEE LIVE VIEWER v3.0
echo        Menggunakan Profile Chrome yang Ada
echo ================================================
echo.

REM Cek apakah Python terinstall
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ KESALAHAN: Python belum terinstall!
    echo.
    echo 💡 Cara install Python:
    echo    1. Buka Microsoft Store
    echo    2. Cari "Python 3.11"
    echo    3. Install dan restart komputer
    echo.
    echo    ATAU download dari: https://python.org/downloads
    echo    ⚠️  PASTIKAN centang "Add Python to PATH" saat install!
    echo.
    pause
    exit /b 1
)

echo ✅ Python ditemukan:
python --version
echo.

REM Input konfigurasi
echo ================================================
echo              KONFIGURASI BOT
echo ================================================
echo.

set /p session="🎯 Masukkan Session ID Shopee Live: "
if "%session%"=="" (
    echo ❌ Session ID wajib diisi!
    pause
    exit /b 1
)

echo.
echo � Mencari profile Chrome yang tersedia...
echo.

REM Buat script Python untuk deteksi profile otomatis
(
echo import os
echo import sys
echo from pathlib import Path
echo import json
echo.
echo def find_chrome_profiles^(^):
echo     """Cari semua profile Chrome di sistem"""
echo     profiles = []
echo     
echo     # Lokasi default Chrome profiles
echo     if os.name == 'nt':  # Windows
echo         base_paths = [
echo             Path.home^(^) / "AppData" / "Local" / "Google" / "Chrome" / "User Data",
echo             Path^("sessions"^) / "google_profiles",
echo             Path^("sessions"^) / "chrome_profiles", 
echo             Path^("sessions"^) / "multi_profiles"
echo         ]
echo     else:  # macOS/Linux
echo         base_paths = [
echo             Path.home^(^) / "Library" / "Application Support" / "Google" / "Chrome",
echo             Path^("sessions"^) / "google_profiles",
echo             Path^("sessions"^) / "chrome_profiles",
echo             Path^("sessions"^) / "multi_profiles"
echo         ]
echo     
echo     for base_path in base_paths:
echo         if base_path.exists^(^):
echo             try:
echo                 for item in base_path.iterdir^(^):
echo                     if item.is_dir^(^):
echo                         profile_name = item.name
echo                         
echo                         # Skip system folders dan folder yang tidak relevan
echo                         skip_folders = [
echo                             'system profile', 'guest profile', 'nativemessaginghosts',
echo                             'screen_ai', 'safe browsing', 'browsermetrics', 'local traces',
echo                             'grshaderCache', 'autofillstates', 'tpcdmetadata', 
echo                             'privacysandboxattestationspreloaded', 'opencookiedatabase',
echo                             'crashpad', 'certificaterevocation', 'ondeviceheadsuggestmodel',
echo                             'download_cache', 'firstpartysetspreloaded', 'sslerrorassistant',
echo                             'shadercache', 'cookiereadinesslist', 'zxcvbndata',
echo                             'deferredbrowsermetrics', 'safetytips', 'origintrials',
echo                             'webstore downloads', 'meipreload', 'filetypepolicies',
echo                             'graphitedawncache', 'segmentation_platform', 'component_crx_cache',
echo                             'extensions_crx_cache', 'recoveryimproved', 'amountextractionheuristicregexes',
echo                             'subresource filter', 'probabilisticrevealthokenregistry',
echo                             'widevinecdm', 'crowd deny', 'pkimetadata', 'optimizationhints',
echo                             'trusttokenkeycommitments', 'optimization_guide_model_store'
echo                         ]
echo                         
echo                         if profile_name.lower^(^) in skip_folders:
echo                             continue
echo                         
echo                         # Cek apakah folder ini adalah profile Chrome yang valid
echo                         preferences_file = item / "Preferences"
echo                         if not preferences_file.exists^(^):
echo                             continue
echo                             
echo                         try:
echo                             with open^(preferences_file, 'r', encoding='utf-8'^) as f:
echo                                 prefs = json.load^(f^)
echo                                 
echo                             # Extract email dari profile
echo                             email = f"Profile: {profile_name}"
echo                             
echo                             # Coba ambil email dari berbagai lokasi di preferences
echo                             if 'account_info' in prefs:
echo                                 for account in prefs['account_info']:
echo                                     if 'email' in account:
echo                                         email = account['email']
echo                                         break
echo                             elif 'profile' in prefs:
echo                                 if 'user_name' in prefs['profile']:
echo                                     email = prefs['profile']['user_name']
echo                                 elif 'name' in prefs['profile']:
echo                                     name = prefs['profile']['name']
echo                                     if '@' in name:
echo                                         email = name
echo                             
echo                             profiles.append^({
echo                                 'path': str^(item^),
echo                                 'name': profile_name,
echo                                 'email': email,
echo                                 'location': str^(base_path.name^)
echo                             }^)
echo                             
echo                         except Exception as e:
echo                             # Jika tidak bisa baca preferences, skip profile ini
echo                             continue
echo             except:
echo                 continue
echo     
echo     return profiles
echo.
echo # Main execution
echo profiles = find_chrome_profiles^(^)
echo.
echo if not profiles:
echo     print^("❌ Tidak ada profile Chrome yang ditemukan!"^)
echo     print^("💡 Pastikan Chrome sudah diinstall dan pernah digunakan."^)
echo     sys.exit^(1^)
echo.
echo print^(f"📋 Ditemukan {len^(profiles^)} profile Chrome:"^)
echo print^(^)
echo.
echo for i, profile in enumerate^(profiles^):
echo     print^(f"   {i+1}. {profile['email']}"^)
echo     print^(f"      � Path: {profile['path']}"^)
echo     print^(f"      🏠 Location: {profile['location']}"^)
echo     print^(^)
echo.
echo # Save profiles to temp file
echo with open^('temp_profiles.json', 'w'^) as f:
echo     json.dump^(profiles, f^)
echo.
echo print^(f"PROFILE_COUNT={len^(profiles^)}"^)
) > temp_detect_profiles.py

python temp_detect_profiles.py
if errorlevel 1 (
    echo ❌ Gagal mendeteksi profile Chrome!
    pause
    exit /b 1
)

REM Ambil jumlah profile dari output
for /f "tokens=2 delims==" %%i in ('python temp_detect_profiles.py ^| findstr "PROFILE_COUNT"') do set profile_count=%%i

if %profile_count%==0 (
    echo ❌ Tidak ada profile Chrome yang valid ditemukan!
    echo.
    echo 💡 Pastikan sudah pernah login ke Chrome dan buat profile
    echo.
    pause
    exit /b 1
)

echo.
set /p viewers="👥 Berapa viewer yang ingin dibuat (max %profile_count%): "
if "%viewers%"=="" set viewers=1

if %viewers% GTR %profile_count% (
    echo ⚠️  Jumlah viewer tidak boleh lebih dari %profile_count% profile!
    set viewers=%profile_count%
)

set /p delay="⏱️  Jeda antar viewer dalam detik (default 3): "
if "%delay%"=="" set delay=3

echo.
echo ================================================
echo            KONFIRMASI KONFIGURASI
echo ================================================
echo.
echo 🎯 Session ID    : %session%
echo 👥 Jumlah Viewer : %viewers%
echo ⏱️  Jeda         : %delay% detik
echo 📺 URL Live      : https://live.shopee.co.id/share?from=live^&session=%session%^&in=1
echo.

set /p confirm="✅ Mulai bot sekarang? (y/n): "
if /i not "%confirm%"=="y" (
    echo ❌ Bot dibatalkan.
    pause
    exit /b 0
)

echo.
echo ================================================
echo              MEMULAI BOT...
echo ================================================
echo.

REM Cek dan install dependencies
echo 🔍 Memeriksa dependencies...
python -c "import selenium,webdriver_manager" >nul 2>&1
if errorlevel 1 (
    echo 📦 Installing selenium dan webdriver-manager...
    python -m pip install selenium webdriver-manager --quiet
    if errorlevel 1 (
        echo ❌ Gagal install dependencies!
        pause
        exit /b 1
    )
)

echo ✅ Dependencies siap!
echo.

REM Buat script Python untuk bot
echo 🤖 Membuat script bot...
(
echo import sys
echo import os
echo import time
echo import random
echo import string
echo import json
echo from pathlib import Path
echo.
echo # Import Selenium
echo try:
echo     from selenium import webdriver
echo     from selenium.webdriver.chrome.service import Service
echo     from selenium.webdriver.chrome.options import Options
echo     from selenium.webdriver.common.by import By
echo     from selenium.webdriver.support.ui import WebDriverWait
echo     from selenium.webdriver.support import expected_conditions as EC
echo     from webdriver_manager.chrome import ChromeDriverManager
echo except ImportError as e:
echo     print^(f"❌ Import error: {e}"^)
echo     input^("Tekan Enter untuk keluar..."^)
echo     sys.exit^(1^)
echo.
echo def generate_device_id^(^):
echo     """Generate unique 32-character device ID"""
echo     return ''.join^(random.choices^(string.ascii_uppercase + string.digits, k=32^)^)
echo.
echo def get_available_profiles^(^):
echo     """Ambil daftar profile Chrome yang sudah dideteksi"""
echo     import json
echo     try:
echo         with open^('temp_profiles.json', 'r'^) as f:
echo             profiles = json.load^(f^)
echo         return profiles
echo     except:
echo         return []
echo.
echo def create_chrome_with_profile^(profile_path, device_id, position^):
echo     """Buat instance Chrome dengan profile Google yang ada"""
echo     options = Options^(^)
echo     
echo     # Gunakan profile yang sudah ada
echo     options.add_argument^(f"--user-data-dir={profile_path}"^)
echo     
echo     # Anti-detection settings
echo     options.add_argument^("--no-sandbox"^)
echo     options.add_argument^("--disable-dev-shm-usage"^)
echo     options.add_argument^("--disable-blink-features=AutomationControlled"^)
echo     options.add_experimental_option^("excludeSwitches", ["enable-automation"]^)
echo     options.add_experimental_option^('useAutomationExtension', False^)
echo     
echo     # Disable notifications
echo     prefs = {
echo         "profile.default_content_setting_values.notifications": 2,
echo         "profile.default_content_settings.popups": 0
echo     }
echo     options.add_experimental_option^("prefs", prefs^)
echo     
echo     try:
echo         service = Service^(ChromeDriverManager^(^).install^(^)^)
echo         driver = webdriver.Chrome^(service=service, options=options^)
echo         
echo         # Set window position dan size
echo         x_pos = ^(position %% 4^) * 350
echo         y_pos = ^(position // 4^) * 300
echo         driver.set_window_position^(x_pos, y_pos^)
echo         driver.set_window_size^(400, 300^)
echo         
echo         return driver
echo         
echo     except Exception as e:
echo         print^(f"❌ Gagal membuat Chrome instance: {e}"^)
echo         return None
echo.
echo def inject_device_fingerprint^(driver, device_id^):
echo     """Inject device fingerprint ke browser"""
echo     fingerprint_script = f"""
echo     // Set device ID di localStorage
echo     localStorage.setItem^('device_id', '{device_id}'^);
echo     localStorage.setItem^('shopee_device_id', '{device_id}'^);
echo     localStorage.setItem^('SPC_device_id', '{device_id}'^);
echo     
echo     // Override navigator properties
echo     Object.defineProperty^(navigator, 'deviceMemory', {{
echo         get: ^(^) =^> {random.choice^([4, 8, 16]^)}
echo     }}^);
echo     
echo     Object.defineProperty^(navigator, 'hardwareConcurrency', {{
echo         get: ^(^) =^> {random.choice^([4, 6, 8, 12]^)}
echo     }}^);
echo     
echo     // Override screen properties
echo     Object.defineProperty^(screen, 'width', {{
echo         get: ^(^) =^> {random.choice^([1920, 1366, 1440, 1680]^)}
echo     }}^);
echo     
echo     Object.defineProperty^(screen, 'height', {{
echo         get: ^(^) =^> {random.choice^([1080, 768, 900, 1050]^)}
echo     }}^);
echo     
echo     console.log^('🔧 Device fingerprint injected:', '{device_id}'^);
echo     """
echo     
echo     try:
echo         driver.execute_script^(fingerprint_script^)
echo         return True
echo     except Exception as e:
echo         print^(f"⚠️  Warning: Gagal inject fingerprint - {e}"^)
echo         return False
echo.
echo def main^(^):
echo     session_id = "%session%"
echo     max_viewers = %viewers%
echo     delay_seconds = %delay%
echo     
echo     print^(f"🎯 Target: {max_viewers} viewers untuk session {session_id}"^)
echo     print^(f"📺 URL: https://live.shopee.co.id/share?from=live&session={session_id}&in=1"^)
echo     print^(^)
echo     
echo     # Ambil profile yang tersedia
echo     available_profiles = get_available_profiles^(^)
echo     
echo     if not available_profiles:
echo         print^("❌ Tidak ada profile Google Chrome yang ditemukan!"^)
echo         input^("Tekan Enter untuk keluar..."^)
echo         return
echo     
echo     print^(f"📋 Ditemukan {len^(available_profiles^)} profile Google:"^)
echo     for i, profile in enumerate^(available_profiles^):
echo         print^(f"   {i+1}. {profile['email']}"^)
echo     print^(^)
echo     
echo     viewers = []
echo     live_url = f"https://live.shopee.co.id/share?from=live&session={session_id}&in=1"
echo     
echo     try:
echo         for i in range^(min^(max_viewers, len^(available_profiles^)^)^):
echo             profile = available_profiles[i]
echo             device_id = generate_device_id^(^)
echo             
echo             print^(f"🚀 Memulai viewer #{i+1}: {profile['email']}"^)
echo             print^(f"   📱 Device ID: {device_id[:8]}...{device_id[-4:]}"^)
echo             print^(f"   📁 Profile: {profile['name']}"^)
echo             
echo             # Buat Chrome instance dengan profile
echo             driver = create_chrome_with_profile^(profile['path'], device_id, i^)
echo             
echo             if driver is None:
echo                 print^(f"❌ Gagal membuat viewer #{i+1}"^)
echo                 continue
echo             
echo             try:
echo                 # Buka Shopee untuk set device fingerprint
echo                 print^(f"   🔧 Setting device fingerprint..."^)
echo                 driver.get^("https://shopee.co.id"^)
echo                 time.sleep^(2^)
echo                 
echo                 # Inject device fingerprint
echo                 if inject_device_fingerprint^(driver, device_id^):
echo                     print^(f"   ✅ Device fingerprint berhasil di-inject"^)
echo                 else:
echo                     print^(f"   ⚠️  Warning: Device fingerprint gagal di-inject"^)
echo                 
echo                 # Buka live stream
echo                 print^(f"   🎥 Membuka live stream..."^)
echo                 driver.get^(live_url^)
echo                 time.sleep^(3^)
echo                 
echo                 viewers.append^({
echo                     'driver': driver,
echo                     'email': profile['email'],
echo                     'device_id': device_id,
echo                     'number': i+1
echo                 }^)
echo                 
echo                 print^(f"   ✅ Viewer #{i+1} berhasil terhubung!"^)
echo                 print^(^)
echo                 
echo                 # Delay sebelum viewer berikutnya
echo                 if i ^< min^(max_viewers, len^(available_profiles^)^) - 1:
echo                     print^(f"⏱️  Menunggu {delay_seconds} detik sebelum viewer berikutnya..."^)
echo                     time.sleep^(delay_seconds^)
echo                 
echo             except Exception as e:
echo                 print^(f"❌ Error pada viewer #{i+1}: {e}"^)
echo                 try:
echo                     driver.quit^(^)
echo                 except:
echo                     pass
echo         
echo         print^("="*60^)
echo         print^(f"🎉 SEMUA {len^(viewers^)} VIEWERS BERHASIL DIMULAI!"^)
echo         print^("="*60^)
echo         print^(^)
echo         
echo         print^("📋 DETAIL VIEWERS:"^)
echo         for viewer in viewers:
echo             print^(f"   👤 Viewer #{viewer['number']}: {viewer['email']}"^)
echo             print^(f"      📱 Device ID: {viewer['device_id']}"^)
echo         print^(^)
echo         
echo         print^("🎯 Bot sedang berjalan! Cek live stream Anda - jumlah viewer seharusnya bertambah!"^)
echo         print^("💡 Jangan tutup jendela Chrome yang terbuka."^)
echo         print^("🛑 Tekan Ctrl+C untuk menghentikan bot..."^)
echo         print^(^)
echo         
echo         # Monitor viewers
echo         while True:
echo             time.sleep^(30^)  # Cek setiap 30 detik
echo             
echo             active_count = 0
echo             for viewer in viewers:
echo                 try:
echo                     # Cek apakah browser masih aktif
echo                     if viewer['driver'].window_handles:
echo                         active_count += 1
echo                 except:
echo                     pass
echo             
echo             print^(f"📊 Status: {active_count}/{len^(viewers^)} viewers masih aktif - {time.strftime^('%H:%M:%S'^)}"^)
echo             
echo             if active_count == 0:
echo                 print^("⚠️  Semua viewers sudah tidak aktif."^)
echo                 break
echo         
echo     except KeyboardInterrupt:
echo         print^("\\n🛑 Bot dihentikan oleh user..."^)
echo     except Exception as e:
echo         print^(f"\\n❌ Error: {e}"^)
echo     finally:
echo         # Cleanup
echo         print^("🧹 Membersihkan viewers..."^)
echo         for viewer in viewers:
echo             try:
echo                 viewer['driver'].quit^(^)
echo                 print^(f"   ✅ Viewer {viewer['email']} ditutup"^)
echo             except:
echo                 pass
echo         print^("✅ Semua viewers berhasil ditutup. Bot selesai."^)
echo         print^(^)
echo         input^("Tekan Enter untuk keluar..."^)
echo.
echo if __name__ == "__main__":
echo     main^(^)
) > scripts\shopee_bot.py

REM Jalankan bot
echo 🚀 Menjalankan bot...
echo.
python scripts\shopee_bot.py

REM Cleanup temporary files
del temp_detect_profiles.py >nul 2>&1
del temp_profiles.json >nul 2>&1

echo.
echo ================================================
echo              BOT SELESAI
echo ================================================
echo.
pause
