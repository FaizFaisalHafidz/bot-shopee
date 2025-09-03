# 🥷 NEO STEALTH SHOPEE BOT - WINDOWS GUIDE

## ✅ READY TO RUN!

Bot sudah siap dijalankan di Windows dengan 2 mode:

### 🚀 MODE 1: STEALTH BOT (RECOMMENDED)
- **Anti-Detection Technology**
- **Device Fingerprinting**  
- **Human Behavior Simulation**
- **URL Format**: `https://live.shopee.co.id/share?from=live&session=XXXXXX`
- **Max Viewers**: 3 (sesuai verified cookies)

### 🔧 MODE 2: ULTIMATE BOT (STANDARD)
- **Standard Browser + API**
- **Cookie Authentication**
- **Multi-threading**

## 📁 VERIFIED COOKIES READY
File: `bot-core/accounts/verified_cookies.csv`
```
account_001,1623919941 ✅
account_002,1623914432 ✅  
account_003,1623911809 ✅
```

## 🎯 CARA MENJALANKAN

### Method 1: Double-click `run.bat`
1. Double-click `run.bat`
2. Pilih mode (1=Stealth, 2=Ultimate)
3. Masukkan Session ID
4. Masukkan jumlah viewers (max 3)
5. Bot akan mulai berjalan!

### Method 2: Command Line
```batch
# Stealth Bot
python bot-core\bots\stealth_shopee_bot.py 157924233 3

# Ultimate Bot  
python bot-core\bots\ultimate_shopee_bot.py 157924233 3
```

## 🎭 STEALTH BOT FEATURES

### Anti-Detection:
- ✅ Unique Device ID per viewer
- ✅ Randomized User Agents
- ✅ Screen resolution spoofing
- ✅ JavaScript fingerprint masking
- ✅ Human-like delays
- ✅ Normal browsing simulation (Google → Shopee → Live)

### Cookie Strategy:
- ✅ Menggunakan verified cookies dari CSV
- ✅ Proper cookie injection
- ✅ Domain `.shopee.co.id`
- ✅ Essential cookies only (SPC_F, SPC_U, SPC_ST, SPC_EC)

### URL Strategy:
- ✅ Simple URL format: `https://live.shopee.co.id/share?from=live&session=XXXXX`
- ✅ No tracking parameters
- ✅ Clean navigation

## 🛡️ ANTI-BOT EVASION

Bot akan mendeteksi dan menghindari:
- ❌ Captcha pages
- ❌ Anti-bot verification
- ❌ Login redirects
- ❌ Blocked content

## 📊 EXPECTED RESULTS

**Stealth Mode:**
```
🥷 STEALTH SHOPEE BOT
Session: 157924233
Target: 3 stealth viewers
========================

[15:30:01] ✅ Loaded 3 stealth cookies
[15:30:02] 🥷 LAUNCHING 3 STEALTH BROWSERS...
[15:30:05] [STEALTH 1] 🥷 Starting stealth mode...
[15:30:08] [STEALTH 1] 🔍 Simulating normal browsing...
[15:30:12] [STEALTH 1] 🛒 Visiting Shopee...
[15:30:18] [STEALTH 1] 📺 Opening live...
[15:30:25] [STEALTH 1] ✅ STEALTH SUCCESS!
...
✅ Successful: 3/3
🎭 Active Stealth Browsers: 3
```

## 🔧 TROUBLESHOOTING

### Jika kena Captcha/Anti-bot:
1. Gunakan **Stealth Mode** (Mode 1)
2. Kurangi jumlah viewers (coba 1-2 dulu)
3. Tunggu delay lebih lama antar browser
4. Pastikan cookies masih valid

### Jika cookies expired:
1. Update `bot-core/accounts/verified_cookies.csv`
2. Gunakan cookies baru yang valid
3. Test dengan 1 viewer dulu

### Performance Tips:
- **Windows**: Tutup aplikasi lain untuk RAM
- **Chrome**: Bot akan buka multiple Chrome instances
- **Network**: Pastikan koneksi stabil
- **RDP**: Gunakan resolution 1920x1080

## 📝 LOG FILES
Bot akan create log files di:
```
bot-core/logs/stealth_bot_YYYYMMDD_HHMMSS.log
```

## 🎯 TESTING CHECKLIST

Sebelum run production:
- [ ] Test dengan 1 viewer dulu
- [ ] Pastikan tidak kena captcha
- [ ] Check viewer count bertambah di live
- [ ] Monitor CPU/RAM usage
- [ ] Pastikan Chrome instances stable

## 🚀 PRODUCTION READY!

Bot sudah ready untuk:
- ✅ Windows 10/11
- ✅ Multiple viewers (max 3)
- ✅ Long-running sessions
- ✅ Anti-detection
- ✅ Stable operation

**JALANKAN: Double-click `run.bat` → Pilih Mode 1 (Stealth)**
