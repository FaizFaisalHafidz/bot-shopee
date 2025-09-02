# 🚀 CARA INSTALL NODE.JS DI RDP WINDOWS

## Method 1: Download Installer (Mudah)
1. Buka browser di RDP
2. Pergi ke: https://nodejs.org/
3. Download **LTS version** (Long Term Support)
4. Run installer `.msi` 
5. Klik Next-Next sampai selesai
6. Restart Command Prompt

## Method 2: Via PowerShell (Cepat)
```powershell
# Buka PowerShell as Administrator
# Copy paste command ini:
winget install OpenJS.NodeJS
```

## Method 3: Portable Version (No Install)
1. Download: https://nodejs.org/dist/latest/win-x64/node.exe
2. Simpan di folder bot
3. Rename `node.exe` jadi `nodejs.exe`
4. Edit BAT file untuk pakai `nodejs.exe`

## ✅ Cek Instalasi
```cmd
node --version
npm --version
```

Harus muncul version number (contoh: v20.10.0)

## 🎯 Setelah Install Node.js:
1. Double click `start_viewer_bot.bat`
2. Bot akan auto-install Puppeteer
3. Masukkan Session ID
4. Bot langsung jalan!

---
**Catatan:** Node.js cuma perlu install 1x. Setelah itu bot bisa langsung jalan tanpa setup lagi.
