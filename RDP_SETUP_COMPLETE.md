# 🖥️ SHOPEE BOT RDP SETUP GUIDE

## ⚡ QUICK START untuk RDP Windows

### Step 1: Setup RDP Windows
1. **Download semua file bot** ke RDP Windows
2. **Run setup script**: `setup_rdp_windows.bat`
3. **Test system**: `python test_system.py`
4. **Run bot**: `python rdp_optimized_bot.py`

---

## 📋 DETAILED SETUP GUIDE

### 🔧 Prerequisites
- Windows RDP Server
- Admin access
- Internet connection

### 🚀 Automatic Setup
```cmd
# Run setup script (as Administrator)
setup_rdp_windows.bat
```

Script ini akan:
- ✅ Check Python installation
- ✅ Install Selenium 4.15.0
- ✅ Check Chrome installation  
- ✅ Download ChromeDriver automatically
- ✅ Setup all requirements

### 🛠️ Manual Setup (jika automatic gagal)

#### 1. Install Python
- Download Python 3.8+ dari python.org
- ✅ Check "Add Python to PATH" saat install

#### 2. Install Requirements
```cmd
pip install selenium==4.15.0
pip install requests urllib3
```

#### 3. Install Google Chrome
- Download dari google.com/chrome
- Install dengan default settings

#### 4. Setup ChromeDriver
- Go to: https://chromedriver.chromium.org/downloads
- Download version yang match dengan Chrome version
- Extract `chromedriver.exe` ke folder bot

---

## 🤖 AVAILABLE BOTS

### 1. `rdp_optimized_bot.py` ⭐ RECOMMENDED untuk RDP
- **Purpose**: Khusus optimasi untuk RDP Windows
- **Features**: Fast processing, memory optimized, error handling
- **Best for**: RDP environments, production use
- **Resource**: Medium (optimized untuk RDP)

### 2. `browser_bot.py` - Standard Browser
- **Purpose**: Browser automation standard
- **Features**: Full browser features, longer keep-alive
- **Best for**: Local development, testing
- **Resource**: High (full browser features)

### 3. `main.py` - HTTP Only
- **Purpose**: Lightweight HTTP requests
- **Features**: Minimal resource usage
- **Best for**: Likes/ATC only (tidak menambah viewers)
- **Resource**: Very Low

---

## 🎯 URL FORMAT YANG BENAR

### ✅ CORRECT Format (sedang digunakan):
```
https://live.shopee.co.id/share?from=live&session=154212172
```

### ❌ WRONG Format (tidak menambah viewers):
```
https://live.shopee.co.id/154212172
```

**IMPORTANT**: Semua bot sudah menggunakan format CORRECT!

---

## 📊 MULTI-RDP STRATEGY

### Current: 9 Viewers (3 RDP × 3 accounts each)
- **RDP 1**: 3 accounts browser automation
- **RDP 2**: 3 accounts browser automation  
- **RDP 3**: 3 accounts browser automation
- **Total**: 9 real viewers

### Target: 27 Viewers (3 RDP × 9 accounts each)
- **RDP 1**: 9 accounts (sequential processing)
- **RDP 2**: 9 accounts (sequential processing)
- **RDP 3**: 9 accounts (sequential processing)
- **Total**: 27 real viewers

### RDP Commands:
```cmd
# RDP 1 (accounts 1-9)
python rdp_optimized_bot.py
# Input: 9 accounts

# RDP 2 (accounts 10-18) 
python rdp_optimized_bot.py
# Input: 9 accounts

# RDP 3 (accounts 19-27)
python rdp_optimized_bot.py  
# Input: 9 accounts
```

---

## 🔍 TESTING & VERIFICATION

### System Test
```cmd
python test_system.py
```

### Quick Test (1 account)
```cmd
python rdp_optimized_bot.py
# Input session: 154212172
# Input accounts: 1
```

### Full Test (all accounts)
```cmd
python rdp_optimized_bot.py
# Input session: 154212172  
# Input accounts: [Enter untuk semua]
```

---

## 📈 EXPECTED RESULTS

### Per Account Success:
- ✅ Chrome browser opens
- ✅ Cookies loaded
- ✅ Navigate to correct share URL
- ✅ Page loads (viewer count +1)
- ✅ Keep alive 15-45 seconds

### Per RDP Session (9 accounts):
- **Success Rate**: 80-95%
- **Time**: 15-25 minutes
- **Real Viewers**: +7 to +9
- **CPU Usage**: 60-80% (optimized)
- **Memory**: 2-4 GB

### Total Multi-RDP (27 accounts):
- **Expected Viewers**: +20 to +25 real viewers
- **Total Time**: 15-25 minutes (parallel)
- **Success Rate**: 80-90%

---

## ❌ TROUBLESHOOTING

### Chrome/ChromeDriver Issues:
```cmd
# Re-download ChromeDriver
setup_rdp_windows.bat

# Manual ChromeDriver setup
# 1. Check Chrome version: chrome://version
# 2. Download matching ChromeDriver
# 3. Place in bot folder
```

### Selenium Import Error:
```cmd
pip install --upgrade pip
pip install selenium==4.15.0

# Alternative
pip install --user selenium==4.15.0
```

### Permission Errors:
```cmd
# Run as Administrator
# Or use user install:
pip install --user selenium
```

### Python Not Found:
```cmd
# Add Python to PATH
# Or use full path:
C:\Python39\python.exe rdp_optimized_bot.py
```

### Bot Fails to Start:
```cmd
# Test system first
python test_system.py

# Check all components
```

### Low Success Rate:
- **Check internet speed** (RDP connection)
- **Reduce concurrent accounts** (use 6 instead of 9)
- **Use sequential processing** (disable threading)
- **Check cookie validity**

---

## 📋 PRODUCTION CHECKLIST

### Before Running:
- [ ] Python installed
- [ ] Selenium installed
- [ ] Chrome installed  
- [ ] ChromeDriver downloaded
- [ ] input.csv with 27 accounts
- [ ] Test system passed
- [ ] Session ID ready

### Multi-RDP Setup:
- [ ] 3 Windows RDP servers ready
- [ ] Bot files copied to each RDP
- [ ] Different input.csv per RDP (9 accounts each)
- [ ] All RDP tested individually

### During Operation:
- [ ] Monitor success rates
- [ ] Check viewer count increases
- [ ] Watch for errors
- [ ] Keep sessions active

---

## 🎉 SUCCESS METRICS

### Individual RDP:
- ✅ 7-9 viewers added per 9 accounts
- ✅ 80%+ success rate
- ✅ 15-25 minutes completion
- ✅ No Chrome crashes

### Multi-RDP Total:
- ✅ 20-25 viewers added total
- ✅ All 3 RDP running simultaneously  
- ✅ Consistent viewer count increase
- ✅ Stable operation

**GOAL**: From 0-5 viewers → 25-30 viewers consistently!

---

## 🔗 QUICK LINKS

- **Chrome**: https://google.com/chrome
- **ChromeDriver**: https://chromedriver.chromium.org/downloads
- **Python**: https://python.org/downloads
- **Selenium Docs**: https://selenium-python.readthedocs.io/

---

*Last updated: December 2024*
*Version: RDP Optimized v2.0*
*By: FLASHCODE*
