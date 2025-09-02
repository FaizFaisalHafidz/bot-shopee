# 🤖 Bot Shopee Live Viewer

Bot untuk menambah viewer di live streaming Shopee menggunakan profile Google Chrome yang sudah ada.

## 📋 Persyaratan

1. **Python 3.7+** - Download dari [python.org](https://python.org/downloads) atau Microsoft Store
2. **Google Chrome** - Sudah login dengan akun Google
3. **Profile Chrome** - Tersimpan di folder `sessions/google_profiles/`

## 🚀 Cara Penggunaan

### 1. Persiapan
```bash
# Pastikan sudah login Google di Chrome
# Profile akan otomatis tersimpan di:
# - sessions/google_profiles/sendipede093_profile_1/
# - sessions/google_profiles/neoflashtech_profile_2/ 
# - sessions/google_profiles/mamanujang461_profile_3/
```

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
├── run.bat                    # File utama untuk menjalankan bot
├── scripts/
│   ├── shopee_bot.py         # Script Python untuk bot
│   └── config.json           # Konfigurasi bot
├── sessions/
│   └── google_profiles/      # Profile Chrome yang sudah login Google
├── accounts/                 # Data akun (CSV)
└── logs/                     # File log bot
```

## ⚙️ Fitur

✅ **Menggunakan Profile Google yang Ada** - Tidak perlu login manual  
✅ **Device Fingerprint Manipulation** - Setiap viewer punya device ID unik  
✅ **Anti-Detection** - Bypass sistem deteksi otomasi Shopee  
✅ **Multi-Viewer** - Bisa buka multiple viewers sekaligus  
✅ **Window Management** - Atur posisi jendela otomatis  
✅ **Real-time Monitoring** - Pantau status viewers  
✅ **Bahasa Indonesia** - Interface dalam bahasa Indonesia  

## 🛠️ Troubleshooting

### Profile Chrome Tidak Ditemukan
```
❌ Tidak ada profile Google Chrome yang ditemukan!

💡 Solusi:
1. Buka Chrome
2. Login ke akun Google 
3. Pastikan profile tersimpan di sessions/google_profiles/
```

### Error Python
```
❌ Python belum terinstall!

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

## 📊 Monitoring

Bot akan menampilkan status real-time:
- Jumlah viewers aktif
- Device ID setiap viewer
- Email akun yang digunakan
- Timestamp aktivitas

## 🚫 Menghentikan Bot

- **Cara 1**: Tekan `Ctrl+C` di Command Prompt
- **Cara 2**: Tutup semua jendela Chrome yang dibuka bot
- **Cara 3**: Tutup Command Prompt

## 📝 Catatan Penting

⚠️ **Gunakan dengan bijak** - Jangan spam terlalu banyak viewers  
⚠️ **Jangan tutup Chrome** - Biarkan jendela Chrome terbuka selama bot berjalan  
⚠️ **Internet stabil** - Pastikan koneksi internet stabil  
⚠️ **Session ID valid** - Pastikan live stream masih aktif  

## 📞 Support

Jika ada masalah, cek:
1. File log di folder `logs/`
2. Konfigurasi di `scripts/config.json`
3. Status profile di `sessions/google_profiles/`
