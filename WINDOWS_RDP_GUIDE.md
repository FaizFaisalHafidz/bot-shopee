# 🖥️ Windows RDP Connection Guide - Shopee Bot

## Step 1: Beli RDP dari Toko Online
**Info yang Anda dapatkan dari seller:**
- IP Address: xxx.xxx.xxx.xxx
- Username: Administrator (biasanya)
- Password: xxxxxxxxxx
- Port: 3389 (default, kadang custom)
- OS: Windows Server 2019/2022

## Step 2: Setup Remote Desktop Connection

### A. Buka Remote Desktop Connection
1. Tekan `Win + R`
2. Ketik: `mstsc`
3. Tekan Enter

### B. Input Connection Details
```
Computer: [IP dari seller]
User name: [Username dari seller]

Contoh:
Computer: 103.123.45.67
User name: Administrator
```

### C. Advanced Options (Recommended)
1. Klik "Show Options" ↓
2. **Tab General:**
   - ✅ Centang "Allow me to save credentials"
   - Klik "Save As" → simpan sebagai "Shopee-Bot-RDP.rdp"

3. **Tab Display:**
   - Color depth: "True Color (32 bit)"
   - Resolution: "Full Screen" atau custom

4. **Tab Local Resources:**
   - ✅ Clipboard
   - ✅ Drives (untuk transfer file bot)
   - Klik "More..." → pilih drive yang mau di-share

5. **Tab Experience:**
   - Connection speed: "LAN (10 Mbps or higher)"
   - ✅ Persistent bitmap caching
   - ✅ Reconnect if connection dropped

## Step 3: Connect & Test
1. Klik "Connect"
2. Jika muncul certificate warning → "Yes" atau "Connect anyway"
3. Login dengan password dari seller
4. Desktop Windows Server akan muncul

## Step 4: Setup Bot di RDP Server
1. **Install Python 3.11+**
   - Download dari python.org di browser RDP
   - Install dengan "Add to PATH" checked

2. **Transfer Bot Files**
   - Copy dari Local Drives (yang sudah di-share)
   - Paste ke C:\shopee-bot\ di server

3. **Install Browser**
   - Install Chrome untuk harvest cookies
   - Login 9-10 akun Shopee di browser
   - Export cookies ke input.csv

4. **Test Bot**
   - Buka Command Prompt di RDP
   - cd C:\shopee-bot
   - python main.py

## Troubleshooting

### Connection Failed?
- Cek IP address benar
- Cek port (default 3389)
- Test ping dulu: `ping IP_ADDRESS`
- Hubungi seller untuk konfirmasi

### Slow Performance?
- Reduce color depth ke 16 bit
- Disable visual effects
- Close unnecessary programs di RDP
- Check internet speed

### Can't Transfer Files?
- Enable "Drives" di Local Resources
- Check firewall settings
- Use cloud storage sebagai alternatif

## Pro Tips
1. **Save RDP file** untuk shortcut connection
2. **Multiple RDP**: Beli 2-3 server, setup terpisah
3. **Schedule Bot**: Buat batch file untuk auto-run
4. **Monitor Performance**: Cek log file secara berkala
5. **Backup Cookies**: Save cookies file di cloud

---
**Next Step**: Setelah berhasil connect, lanjut setup bot di Windows Server
