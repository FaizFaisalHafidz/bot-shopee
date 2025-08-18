# 🤖 Shopee Live Streaming Bot - Ready to Use!

## ✅ Status Project

- **27 akun valid** dengan cookie kualitas sempurna (100% score) ✅
- **Virtual environment** sudah dikonfigurasi ✅  
- **Dependencies** sudah terinstall ✅
- **Bot standard & advanced** siap digunakan ✅

## 🚀 Quick Start

### 1. Validasi Cookie (Optional)
```bash
./validate.sh
```

### 2. Jalankan Bot Standard
```bash
./run.sh
```

### 3. Jalankan Bot Advanced (Recommended)
```bash
./run_advanced.sh
```

## 🎯 Fitur Bot

### Bot Standard (main.py):
- ✅ Bot Like otomatis
- ✅ Bot Viewer otomatis  
- ✅ Bot ATC (Add to Cart) otomatis
- ✅ Multi-threading (5 thread untuk like)
- ✅ Random interval (2-8 detik)

### Bot Advanced (advanced_bot.py):
- ✅ Semua fitur standard
- ✅ **Real-time statistics** 📊
- ✅ **Advanced logging** 📝
- ✅ **Configurable settings** ⚙️
- ✅ **Better error handling** 🛡️
- ✅ **Session monitoring** 👁️

## 📋 Cara Penggunaan

1. **Pilih tipe bot** (standard/advanced)
2. **Pilih mode**: 1=Like, 2=Viewer, 3=ATC
3. **Masukkan Session Live ID** dari URL Shopee live
4. **Bot mulai bekerja** secara otomatis

### Contoh Session Live ID:
- URL: `https://live.shopee.co.id/71875688`
- Session ID: `71875688`

## ⚙️ Konfigurasi (Advanced Bot)

Edit `config.json` untuk mengatur:
```json
{
    "bot_settings": {
        "like_interval": {"min": 2, "max": 8},
        "viewer_interval": {"min": 5, "max": 15},
        "atc_interval": {"min": 3, "max": 10}
    },
    "thread_config": {
        "like_threads": 5,
        "viewer_threads": 3,
        "atc_threads": 4
    }
}
```

## 📊 Statistik Real-time (Advanced Bot)

Bot advanced menampilkan:
- ✅ **Likes sent**: Jumlah like yang berhasil dikirim
- 👥 **Viewers added**: Jumlah viewer yang ditambahkan
- 🛒 **ATC success**: Jumlah produk yang berhasil ditambah ke cart
- ❌ **Errors**: Jumlah error yang terjadi
- ⏱️ **Runtime**: Waktu bot berjalan

## 🔧 File Structure

```
bot-live-shopee/
├── main.py              # Bot standard
├── advanced_bot.py      # Bot advanced (recommended)
├── input.csv            # 27 akun Shopee (ready)
├── config.json          # Konfigurasi bot
├── validate_cookies.py  # Cookie validator
├── cookie_helper.py     # Cookie helper tool
├── venv/               # Virtual environment
├── run.sh              # Launch bot standard
├── run_advanced.sh     # Launch bot advanced
├── validate.sh         # Validate cookies
└── setup_macos.sh      # Setup script
```

## 💡 Tips Penggunaan

### Untuk Hasil Optimal:
1. **Gunakan bot advanced** - fitur lebih lengkap
2. **Test dengan sedikit akun dulu** (5-10 akun)
3. **Monitor rate limiting** - kurangi thread jika error
4. **Pastikan live stream aktif** sebelum menjalankan bot

### Safety Tips:
- ✅ Mulai dengan interval yang konservatif
- ✅ Monitor log untuk error
- ✅ Jangan gunakan semua akun sekaligus di awal
- ✅ Backup cookie jika diperlukan

## 🐛 Troubleshooting

### Bot tidak bisa connect:
```bash
# Check session ID valid
./run_advanced.sh
# Masukkan session ID dan lihat validasi
```

### Cookie expired:
```bash
# Validate semua cookie
./validate.sh
```

### Permission error:
```bash
chmod +x *.sh
```

### Virtual environment error:
```bash
rm -rf venv
./setup_macos.sh
```

## 📞 Command Cheat Sheet

```bash
# Setup awal (first time only)
./setup_macos.sh

# Validate cookie quality
./validate.sh

# Run bot standard
./run.sh

# Run bot advanced (recommended)
./run_advanced.sh

# Manual venv activation
source venv/bin/activate

# Check logs
tail -f shopee_bot.log
```

## 🎉 Project Ready!

**Status: ✅ PRODUCTION READY**

- 27 akun dengan cookie berkualitas tinggi
- Multi-threading untuk performa optimal  
- Real-time monitoring dan statistik
- Error handling yang robust
- Konfigurasi yang fleksibel

**Happy Botting! 🤖🔥**
