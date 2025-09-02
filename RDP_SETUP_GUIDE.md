# SHOPEE MULTI VIEWER BOT - RDP SETUP GUIDE

## 🚨 PYTHON ERROR FIX (WINDOWS RDP)

**Error yang sering terjadi:**
```
Python tidak ditemukan; jalankan tanpa argumen untuk diinstal dari Microsoft Store, atau nonaktifkan pintasan ini dari Pengaturan > Aplikasi > Pengaturan aplikasi lanjutan > Alias eksekusi aplikasi.
```

### 🔧 QUICK FIX (Pilih salah satu):

**Option 1 - Auto Fix Script:**
```bash
# Jalankan auto-fixer
fix_python_rdp.bat
```

**Option 2 - PowerShell Fix:**
```powershell
# Run sebagai Administrator
powershell -ExecutionPolicy Bypass -File fix_python_rdp.ps1
```

**Option 3 - Microsoft Store (Paling Mudah):**
1. Buka Microsoft Store
2. Cari "Python 3.11"
3. Install dari Python Software Foundation
4. Restart Command Prompt
5. Test: `python --version`

**Option 4 - Manual Download:**
1. Go to: https://www.python.org/downloads/
2. Download Python 3.11.5
3. ✅ **CENTANG "Add Python to PATH"**
4. Install as Administrator
5. Restart Command Prompt

### ✅ Verifikasi Python Working:
```bash
# Test commands
python --version
# atau
py --version
# atau  
python3 --version
```

## 🎯 CARA PENGGUNAAN DI RDP WINDOWS

### Step 1: Setup Google Profiles (Manual)
1. Buka Chrome di RDP Windows
2. Login manual dengan akun Google yang berbeda-beda
3. Pastikan setiap akun tersimpan di profile Chrome terpisah
4. Folder profiles akan tersimpan di: `sessions/google_profiles/`

### Step 2: Jalankan Bot
```bash
# Cara 1: Double click
run_shopee_bot.bat

# Cara 2: Manual
python shopee_fingerprint_bot.py
```

### Step 3: Input Session ID
- Masukkan Session ID Shopee Live (contoh: 157658364)
- Pilih jumlah viewers (sesuai jumlah Google profiles)

## 🔧 FITUR DEVICE FINGERPRINT BYPASS

Bot akan otomatis:
✅ **User Agent berbeda** per viewer
✅ **Screen resolution berbeda** per viewer  
✅ **Device memory berbeda** per viewer
✅ **CPU cores berbeda** per viewer
✅ **WebGL fingerprint berbeda** per viewer
✅ **Canvas fingerprint berbeda** per viewer
✅ **Timezone manipulation**

## 📊 HASIL YANG DIHARAPKAN

Sebelum bot:
```
session_id → 157658364
device_id → A385108467C740AFBB21BAB8483F3273
viewer_count → 1
```

Setelah bot (3 viewers):
```
session_id → 157658364
device_id → B485208567D840BFCC32CAB9584G4384 (viewer 1)
device_id → C585308667E940CGDD43DBC0695H5495 (viewer 2)  
device_id → D685408767F040DHEE54ECD1706I6506 (viewer 3)
viewer_count → 4 (1 asli + 3 bot)
```

## ⚠️ PENTING UNTUK RDP:

1. **Stabilitas Koneksi**
   - Pastikan RDP connection stabil
   - Gunakan dedicated server untuk bot

2. **Resource Management** 
   - 1 RDP = maksimal 10-15 viewers
   - 6 RDP = maksimal 60-90 viewers total

3. **Profile Management**
   - Setiap RDP setup Google profiles terpisah
   - Jangan duplicate profiles antar RDP

4. **Detection Avoidance**
   - Jangan jalankan terlalu banyak viewers sekaligus
   - Start bertahap (5-10 viewers per 5 menit)
   - Gunakan delay antar viewers

## 🚀 SCALE TO 100 VIEWERS:

RDP 1: 15 viewers (profiles 1-15)
RDP 2: 15 viewers (profiles 16-30)
RDP 3: 15 viewers (profiles 31-45)
RDP 4: 15 viewers (profiles 46-60)
RDP 5: 15 viewers (profiles 61-75)
RDP 6: 25 viewers (profiles 76-100)

Total: 100 unique device fingerprints = 100 real viewers!

## 📝 TROUBLESHOOTING:

**Problem: viewer_count tidak naik**
- Solution: Check device fingerprint di console browser

**Problem: Chrome crash**
- Solution: Reduce concurrent viewers, increase delay

**Problem: Google login expired**  
- Solution: Re-login manual di Chrome profiles

**Problem: Shopee detect automation**
- Solution: Add more random delays, update fingerprints
