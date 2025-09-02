# SHOPEE LIVE BOT - ORGANIZED STRUCTURE

## Quick Start
Jalankan: **run.bat** (Windows) atau **run.sh** (Linux/Mac)

## Struktur Folder Terorganisir

```
📁 Root/
├── 📄 run.bat                    # SINGLE ENTRY POINT - Jalankan ini!
├── 📄 requirements.txt           # Dependencies Python
└── 📁 bot-core/                  # SEMUA FILE BOT TERSIMPAN DISINI
    ├── 📁 bots/                  # Bot utama
    │   ├── real_url_bot_rdp.py   # ✅ MAIN BOT - RDP Optimized dengan URL format BENAR
    │   ├── shopee_api_bot.py     # API-based bot
    │   ├── network_interceptor_bot.py
    │   ├── simple_network_bot.py
    │   └── real_url_bot.py
    ├── 📁 launchers/             # File launcher (.bat)
    ├── � configs/               # Konfigurasi
    ├── 📁 sessions/              # Browser sessions & profiles
    ├── 📁 logs/                  # Log files
    ├── 📁 scripts/               # Script tambahan
    ├── 📁 docs/                  # Dokumentasi
    └── 📁 chrome_extension/      # Chrome extension
```

## Main Bot: real_url_bot_rdp.py

**SUDAH DIPERBAIKI** dengan format URL yang BENAR sesuai yang Anda berikan:
```
https://live.shopee.co.id/share?from=live&session=157888904&share_user_id=266236471&stm_medium=referral&stm_source=rw&uls_trackid=53jp2kt800lt&viewer=5&in=1#copy_link
```

### Features:
- ✅ RDP Optimized (Windows Remote Desktop friendly)  
- ✅ Headless Chrome dengan pengaturan proper
- ✅ Auth bypass yang disempurnakan
- ✅ Viewer booster sistem
- ✅ Multiple device profiles (Android, iOS, Windows, macOS)
- ✅ Error handling yang robust
- ✅ Session management

### Cara Penggunaan:
```bash
# Via run.bat (Recommended)
run.bat

# Atau langsung:
python bot-core/bots/real_url_bot_rdp.py <session_id> [viewer_count]

# Contoh:
python bot-core/bots/real_url_bot_rdp.py 157888904 5
```

## Requirements
```
selenium
webdriver-manager
```

Install dengan:
```bash
pip install -r requirements.txt
```

## Catatan Penting

1. **Format URL**: Bot menggunakan format URL PERSIS seperti yang Anda berikan
2. **RDP Ready**: Dioptimalkan untuk Windows RDP environment  
3. **Single Entry Point**: Semua akses via `run.bat` - tidak perlu file scattered lagi
4. **Organized**: Semua file terorganisir dalam `bot-core/` - struktur bersih!

## Quick Test
```bash
# 1. Jalankan run.bat
# 2. Pilih option [1] Quick Start  
# 3. Masukkan Session ID (contoh: 157888904)
# 4. Masukkan jumlah viewer (contoh: 3)
# 5. Bot akan start dengan format URL yang BENAR!
```

**SEKARANG STRUKTURNYA BERSIH DAN TERORGANISIR! 🎉**
