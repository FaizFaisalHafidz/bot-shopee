# Shopee Live Bot - Panduan macOS

## 🍎 Setup untuk macOS

Bot ini telah dikonfigurasi khusus untuk macOS dengan virtual environment untuk isolasi dependencies yang proper.

### ✅ Requirements

- macOS 10.14+ 
- Python 3.7+
- Terminal/Command Line access

### 🚀 Quick Start

1. **Setup Otomatis (First Time)**:
```bash
./setup_macos.sh
```

2. **Edit Cookie Accounts**:
   - Buka file `input.csv`
   - Masukkan cookie akun Shopee (satu per baris)
   - Format: cookie semicolon-separated

3. **Jalankan Bot**:
```bash
# Bot Standard
./run.sh

# Bot Advanced (dengan statistik real-time)
./run_advanced.sh
```

## 🔧 Virtual Environment

Bot menggunakan Python virtual environment untuk:
- ✅ Isolasi dependencies
- ✅ Menghindari konflik dengan system Python
- ✅ Easy cleanup dan reinstall

### Manual venv management:
```bash
# Aktivasi
source venv/bin/activate

# Deaktivasi
deactivate

# Reinstall dependencies
pip install -r requirements.txt
```

## 📂 File Structure

```
bot-live-shopee/
├── main.py              # Bot standard
├── advanced_bot.py      # Bot dengan fitur advanced
├── input.csv            # Cookie akun Shopee
├── config.json          # Konfigurasi bot
├── requirements.txt     # Python dependencies
├── setup_macos.sh       # Setup script untuk macOS
├── run.sh              # Launcher bot standard
├── run_advanced.sh     # Launcher bot advanced
├── venv/               # Virtual environment (auto-created)
└── README.md           # Dokumentasi
```

## ⚙️ Konfigurasi

Edit `config.json` untuk mengatur:
- Interval waktu antar request
- Jumlah thread per bot type
- Timeout settings
- API endpoints

## 🔍 Troubleshooting macOS

### Permission Denied
```bash
chmod +x setup_macos.sh
chmod +x run.sh
chmod +x run_advanced.sh
```

### Python Command Not Found
```bash
# Install via Homebrew
brew install python3

# Atau download dari python.org
```

### Virtual Environment Issues
```bash
# Remove dan recreate venv
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### SSL Certificate Errors
```bash
# Update certificates
pip install --upgrade certifi
```

## 🎯 Bot Features

### Standard Bot (`main.py`):
- ✅ Like automation
- ✅ Viewer automation  
- ✅ Add to Cart automation
- ✅ Multi-threading
- ✅ Random intervals

### Advanced Bot (`advanced_bot.py`):
- ✅ Semua fitur standard
- ✅ Real-time statistics
- ✅ Advanced logging
- ✅ Configurable settings
- ✅ Better error handling
- ✅ Session monitoring

## 📊 Usage Tips

1. **Test dengan sedikit akun dulu** - mulai dengan 5-10 akun
2. **Monitor rate limiting** - jika error, kurangi jumlah thread
3. **Gunakan cookie fresh** - cookie lama mungkin sudah expired
4. **Check live stream valid** - pastikan session ID benar

## 🛡️ Security

- Cookie disimpan di `input.csv` (sudah di .gitignore)
- Jangan commit file sensitive ke git
- Gunakan akun test untuk development

## 📞 Support

Jika ada masalah di macOS:
1. Check Python version: `python3 --version`
2. Check virtual env: `which python` (should point to venv)
3. Check dependencies: `pip list`
4. Check logs: `tail -f shopee_bot.log`

---

**Happy Botting! 🤖**
