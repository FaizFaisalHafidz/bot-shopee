# 🤖 Bot Shopee Live Viewer

Bot untuk menambah viewer di live streaming Shopee menggunakan profile Chrome yang sudah ada.

## 📋 Persyaratan

1. **Python 3.7+** - Download dari [python.org](https://python.org/downloads) atau Microsoft Store
2. **Google Chrome** - Sudah login dengan akun Google
3. **Profile Chrome** - Otomatis terdeteksi dari sistem

## 🚀 Cara Penggunaan

### 1. Persiapan
- Pastikan Chrome sudah diinstall dan pernah login Google
- Bot akan otomatis mendeteksi semua profile Chrome di sistem

### 2. Menjalankan Bot
```cmd
# Double-click file ini:
run.bat

# Atau jalankan via Command Prompt:
cd "path/to/bot-live-shopee"
run.bat
```

### 3. Input yang Diperlukan
- **Session ID**: ID dari live stream Shopee (contoh: 157658364)
- **Jumlah Viewers**: Berapa viewer yang ingin dibuat (max sesuai profile tersedia)
- **Delay**: Jeda antar viewer dalam detik (default: 3 detik)

## 📁 Struktur File

```
bot-live-shopee/
├── run.bat                          # File utama untuk menjalankan bot
├── scripts/
│   ├── detect_profiles.py           # Script deteksi profile Chrome
│   ├── shopee_bot.py               # Script Python untuk bot
│   ├── config.json                 # Konfigurasi bot
│   └── README.md                   # Dokumentasi ini
├── sessions/                       # Profile Chrome custom (opsional)
├── accounts/                       # Data akun (CSV)
└── logs/                          # File log bot
```

## ⚙️ Fitur

✅ **Auto-Detect Profile Chrome** - Scan otomatis semua profile di sistem  
✅ **Cross-Platform** - Support Windows, macOS, Linux  
✅ **Device Fingerprint Manipulation** - Setiap viewer punya device ID unik  
✅ **Anti-Detection** - Bypass sistem deteksi otomasi Shopee  
✅ **Multi-Viewer** - Bisa buka multiple viewers sekaligus  
✅ **Window Management** - Atur posisi jendela otomatis  
✅ **Real-time Monitoring** - Pantau status viewers  
✅ **Bahasa Indonesia** - Interface dalam bahasa Indonesia  

## � Deteksi Profile Otomatis

Bot akan mencari profile Chrome di lokasi:

**Windows:**
- `%USERPROFILE%\AppData\Local\Google\Chrome\User Data\`
- `sessions\google_profiles\`
- `sessions\chrome_profiles\`
- `sessions\multi_profiles\`

**macOS:**
- `~/Library/Application Support/Google/Chrome/`
- `sessions/google_profiles/`
- `sessions/chrome_profiles/`
- `sessions/multi_profiles/`

**Linux:**
- `~/.config/google-chrome/`
- `sessions/google_profiles/`
- `sessions/chrome_profiles/`
- `sessions/multi_profiles/`

## �🛠️ Troubleshooting

### Profile Chrome Tidak Ditemukan
```
[ERROR] Tidak ada profile Chrome yang ditemukan!

💡 Solusi:
1. Buka Chrome
2. Login ke akun Google 
3. Pastikan Chrome pernah digunakan dan memiliki profile
```

### Error Python
```
[ERROR] Python belum terinstall!

💡 Solusi:
1. Download Python dari python.org
2. Centang "Add Python to PATH" saat install
3. Restart komputer
```

### Chrome Tidak Membuka
```
❌ Gagal membuat Chrome instance

💡 Solusi:
1. Update Chrome ke versi terbaru
2. Restart komputer
3. Jalankan sebagai Administrator
```

### Error Encoding di Windows
```
SyntaxError: invalid syntax

💡 Solusi:
1. Pastikan menggunakan run.bat (bukan yang lama)
2. File Python sudah terpisah dari BAT
3. Gunakan Command Prompt (bukan PowerShell)
```

## 📊 Output Contoh

```
================================================
       BOT SHOPEE LIVE VIEWER v3.0
       Menggunakan Profile Chrome yang Ada
================================================

[OK] Python ditemukan:
Python 3.10.0

================================================
             KONFIGURASI BOT
================================================

Masukkan Session ID Shopee Live: 157658364

[INFO] Mencari profile Chrome yang tersedia...

📋 Ditemukan 5 profile Chrome:

   1. flashcode.dev@gmail.com
      📁 Path: C:\Users\User\AppData\Local\Google\Chrome\User Data\Profile 1
      🏠 Location: Chrome

   2. mamanujang461@gmail.com  
      📁 Path: C:\Users\User\AppData\Local\Google\Chrome\User Data\Profile 2
      🏠 Location: Chrome

PROFILE_COUNT=5

Berapa viewer yang ingin dibuat (max 5): 3
Jeda antar viewer dalam detik (default 3): 2

Session ID    : 157658364
Jumlah Viewer : 3
Jeda         : 2 detik
URL Live      : https://live.shopee.co.id/share?from=live&session=157658364&in=1

Mulai bot sekarang? (y/n): y
```

## 🚫 Menghentikan Bot

- **Cara 1**: Tekan `Ctrl+C` di Command Prompt
- **Cara 2**: Tutup semua jendela Chrome yang dibuka bot
- **Cara 3**: Tutup Command Prompt

## 📝 Catatan Penting

⚠️ **Gunakan dengan bijak** - Jangan spam terlalu banyak viewers  
⚠️ **Jangan tutup Chrome** - Biarkan jendela Chrome terbuka selama bot berjalan  
⚠️ **Internet stabil** - Pastikan koneksi internet stabil  
⚠️ **Session ID valid** - Pastikan live stream masih aktif  
⚠️ **Kompatibilitas Windows** - File sudah dioptimasi untuk Windows RDP  

## 🆕 Update v3.0

- ✅ Auto-detect profile Chrome dari sistem
- ✅ Tidak perlu hardcode profile lagi
- ✅ File Python terpisah dari BAT untuk kompatibilitas Windows
- ✅ Support encoding Windows Command Prompt
- ✅ Simplified interface tanpa emoji untuk kompatibilitas
- ✅ Cross-platform support (Windows/macOS/Linux)

## 📞 Support

Jika ada masalah, cek:
1. File log di folder `logs/`
2. Konfigurasi di `scripts/config.json`
3. Output `python scripts/detect_profiles.py` untuk cek profile
