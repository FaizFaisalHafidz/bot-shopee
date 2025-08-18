# Shopee Live Streaming Bot

Bot otomatis untuk meningkatkan engagement pada live streaming Shopee dengan fitur:
- ✅ Bot Like - Menambah like otomatis
- ✅ Bot Viewer - Menambah viewer otomatis  
- ✅ Bot ATC (Add to Cart) - Menambah produk ke keranjang otomatis

## 🚀 Fitur Utama

1. **Bot Like**: Memberikan like secara otomatis dengan interval random
2. **Bot Viewer**: Menambah viewer dengan join live stream
3. **Bot ATC**: Menambahkan produk live ke keranjang secara otomatis
4. **Multi-threading**: Performa optimal dengan multiple thread
5. **Real-time Monitoring**: Log aktivitas secara real-time

## 📋 Persyaratan

- Python 3.7 atau lebih baru
- File `input.csv` berisi cookie akun Shopee (sudah tersedia)
- Koneksi internet yang stabil

## 🛠️ Instalasi

### Untuk macOS (Recommended):

1. Clone atau download repository ini
2. Jalankan setup otomatis:
```bash
./setup_macos.sh
```

### Manual Installation:

1. Buat virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## 📝 Cara Penggunaan

### Metode 1: Script Otomatis (Recommended untuk macOS)

1. Pastikan file `input.csv` sudah berisi cookie akun Shopee
2. Jalankan bot standar:
```bash
./run.sh
```

3. Atau jalankan bot advanced:
```bash
./run_advanced.sh
```

### Metode 2: Manual

1. Aktifkan virtual environment:
```bash
source venv/bin/activate
```

2. Jalankan bot:
```bash
python main.py
# atau untuk advanced version
python advanced_bot.py
```

3. Pilih menu yang diinginkan:
   - Ketik `1` untuk Bot Like
   - Ketik `2` untuk Bot Viewer  
   - Ketik `3` untuk Bot ATC
   - Ketik `4` untuk Keluar

4. Masukkan Session Live ID dari Shopee live stream
5. Bot akan mulai bekerja secara otomatis

## 📊 Format Session Live ID

Session Live ID bisa didapat dari URL live streaming Shopee:
- URL: `https://live.shopee.co.id/12345678`
- Session ID: `12345678`

## 🔧 Konfigurasi

### File input.csv
File ini berisi cookie akun Shopee dalam format semicolon-separated:
```
cookie1; cookie2; cookie3
```

Setiap baris adalah satu akun dengan cookie lengkapnya.

### Interval dan Timing
- Bot Like: 2-8 detik interval
- Bot Viewer: 5-15 detik interval  
- Bot ATC: 3-10 detik interval

## ⚠️ Peringatan

- Gunakan bot ini dengan bijak dan sesuai Terms of Service Shopee
- Tidak disarankan untuk penggunaan komersial tanpa izin
- Author tidak bertanggung jawab atas penyalahgunaan bot ini

## 🐛 Troubleshooting

### Bot tidak bisa connect
- Pastikan session ID valid dan live stream masih aktif
- Cek koneksi internet
- Pastikan cookie akun masih valid

### Error parsing CSV
- Pastikan format CSV sesuai (semicolon separated)
- Cek encoding file (UTF-8)
- Pastikan tidak ada baris kosong

### Rate limiting
- Bot sudah dilengkapi dengan interval random
- Jika masih terkena rate limit, kurangi jumlah akun atau perbesar interval

## 📞 Support

Jika mengalami masalah atau memiliki pertanyaan, silakan buat issue di repository ini.

---
**Disclaimer**: Bot ini dibuat untuk tujuan edukasi. Penggunaan untuk aktivitas yang melanggar ToS platform adalah tanggung jawab pengguna.
