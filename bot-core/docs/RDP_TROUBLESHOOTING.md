# RDP BOT TROUBLESHOOTING GUIDE

## ✅ Masalah WebGL & GPU Errors - SOLVED!

### 🔧 Yang Sudah Diperbaiki:

1. **Chrome Options Ultra RDP**:
   - GPU sepenuhnya dinonaktifkan
   - WebGL dan 3D APIs diblokir
   - Software rendering dipaksa
   - Memory dan performance dioptimalkan

2. **Error Handling yang Robust**:
   - Chrome startup dengan retry mechanism
   - Timeout yang disesuaikan untuk RDP
   - Fallback jika gagal

3. **JavaScript Handling**:
   - JavaScript tetap aktif untuk auth bypass
   - Hanya fitur berat yang dinonaktifkan

## 🚀 Cara Mengatasi Error RDP:

### Method 1 - Quick Test (Recommended):
```bash
python check_rdp.py        # Cek environment dulu
python quick_test.py <session_id>  # Test dengan 1 viewer
```

### Method 2 - Via Menu:
```bash
run.bat
# Pilih [3] RDP Environment Check
# Lalu [2] Quick Test Launcher
```

### Method 3 - Direct Bot:
```bash
python bot-core/bots/real_url_bot_rdp.py <session_id> 1
```

## 🛠️ New Chrome Flags Added:

```
--disable-gpu
--disable-gpu-sandbox  
--disable-gpu-process
--disable-software-rasterizer
--disable-webgl
--disable-webgl2
--disable-3d-apis
--disable-accelerated-2d-canvas
--enable-unsafe-swiftshader
--blacklist-webgl
--blacklist-accelerated-compositing
```

## 📋 Troubleshooting Steps:

1. **Test Environment**:
   ```bash
   python check_rdp.py
   ```

2. **If Chrome Fails**:
   - Check if Chrome is installed
   - Try with single viewer first
   - Check Windows RDP settings

3. **If Still Errors**:
   - Run quick test with verbose output
   - Check bot-core/logs/ for details
   - Try lower viewer count

## ⚡ Quick Fix Commands:

```bash
# Install requirements
pip install selenium webdriver-manager requests

# Test basic Chrome
python check_rdp.py

# Test single viewer
python quick_test.py 157888904

# Full bot with multiple viewers
python bot-core/bots/real_url_bot_rdp.py 157888904 3
```

## 🎯 Expected Results:

✅ **Success Indicators**:
```
[CHROME] Chrome started successfully for viewer 1
[TEST] Chrome connection OK!
[NAVIGATE] Accessing Shopee domain...
[SUCCESS] RDP viewer 1 active!
```

❌ **Error Indicators** (Now Fixed):
- GPU stall errors → Fixed with GPU kill switches
- WebGL errors → Fixed with WebGL blockers
- Chrome startup failures → Fixed with retry mechanism

## 🔥 Bot Features:

- **URL Format**: Menggunakan format PERSIS yang Anda berikan
- **RDP Optimized**: Chrome options khusus Windows RDP
- **Auth Bypass**: Sistema authentication bypass
- **Viewer Boost**: Automatic viewer number booster
- **Error Recovery**: Automatic retry dan error handling

**Bot siap digunakan untuk RDP environment! 🚀**
