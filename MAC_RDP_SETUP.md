# 🚀 Mac RDP Setup Script untuk Shopee Bot

## Step 1: Install Microsoft Remote Desktop
1. Buka App Store
2. Search "Microsoft Remote Desktop"  
3. Install aplikasi (gratis)

## Step 2: Add New Connection
1. Buka Microsoft Remote Desktop
2. Klik tombol "+" atau "Add PC"
3. Masukkan informasi RDP:

```
PC name: [IP ADDRESS dari seller]
User name: [USERNAME dari seller]  
Password: [PASSWORD dari seller]
Friendly name: "Shopee Bot RDP-1"
```

## Step 3: Advanced Settings (Optional)
- Gateway: Kosongkan (kecuali diminta seller)
- Port: 3389 (default)
- Display: Full Screen atau Custom
- Local Resources: Enable clipboard, drives

## Step 4: Test Connection
1. Double-click connection yang baru dibuat
2. Jika muncul certificate warning, klik "Continue"
3. Tunggu sampai Windows desktop muncul

## Step 5: Setup Bot di RDP
1. Install Python 3.11 di Windows RDP
2. Install Google Chrome
3. Upload bot files ke RDP
4. Setup cookies dari akun Shopee

---
Setelah berhasil connect, lanjut ke setup bot di Windows.
