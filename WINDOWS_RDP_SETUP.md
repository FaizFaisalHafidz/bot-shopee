# 🖥️ Windows RDP Setup Guide - Shopee Bot

## 🎯 Server Specification (Per RDP)

**Recommended VPS Provider: Vultr**
- **OS**: Windows Server 2019/2022
- **RAM**: 4GB (recommended)
- **CPU**: 2 vCPU  
- **Storage**: 80GB SSD
- **Location**: Singapore (optimal for Shopee Indonesia)
- **Cost**: $20/month per server

## 🚀 Multi-RDP Setup Strategy

### Server Distribution:
```
RDP Server 1 (Singapore): Akun 1-9   → IP: xxx.xxx.1.xxx
RDP Server 2 (Singapore): Akun 10-18 → IP: xxx.xxx.2.xxx  
RDP Server 3 (Tokyo):     Akun 19-27 → IP: xxx.xxx.3.xxx
```

**Total Investment**: $60/month untuk 27 akun dari 3 IP berbeda

## 📝 Step-by-Step Setup

### Step 1: Order VPS Windows
1. Register di [vultr.com](https://vultr.com)
2. Pilih **"Deploy New Server"**
3. Server Type: **"Cloud Compute"**
4. Location: **"Singapore"** (atau Tokyo untuk server ke-3)
5. Server Image: **"Windows Server 2019"**
6. Server Size: **"$20/mo - 2 vCPU, 4GB Memory"**
7. Klik **"Deploy Now"**
8. Wait 5-10 minutes

### Step 2: Connect via RDP
1. Di Vultr panel, klik server yang baru dibuat
2. Copy **IP Address**, **Username**, dan **Password**
3. Buka **"Remote Desktop Connection"** di Windows
4. Masukkan IP address
5. Login dengan credentials dari Vultr

### Step 3: Setup Bot di RDP Server
1. **Install Python**:
   - Download dari python.org
   - Pilih Python 3.11.x
   - Centang "Add to PATH"

2. **Install Chrome Browser**:
   - Untuk harvest cookies dari 9 akun Shopee
   - Login masing-masing akun dan save cookies

3. **Upload Bot Files**:
   - Copy semua file bot ke RDP server
   - Extract di folder: `C:\shopee-bot\`

4. **Setup Cookies**:
   - Edit `input.csv` dengan 9 akun cookies
   - Setiap RDP server punya akun berbeda

5. **Test Bot**:
   - Buka Command Prompt
   - Navigate: `cd C:\shopee-bot`
   - Run: `python main.py`

## 🎮 Daily Operations

### Login ke RDP:
```
RDP-1: mstsc /v:IP_SERVER_1
RDP-2: mstsc /v:IP_SERVER_2  
RDP-3: mstsc /v:IP_SERVER_3
```

### Run Bot di Setiap RDP:
```
1. Open Command Prompt
2. cd C:\shopee-bot
3. python main.py
4. Pilih mode (1=Like, 2=Viewer, 3=ATC)
5. Input Session ID live Shopee
6. Bot mulai bekerja otomatis
```

## 📊 Expected Results

**Per Live Session:**
- **Total Likes**: 27 likes otomatis
- **Total Viewers**: +27 real viewers
- **Total ATC**: 27 add to cart
- **Execution Time**: 2-5 menit per batch
- **IP Diversity**: 3 different IPs

## 💡 Pro Tips

1. **Stagger Bot Execution**: Jangan jalankan 3 server bersamaan, beri jeda 30 detik
2. **Monitor Performance**: Cek log di setiap RDP untuk memastikan semua berjalan
3. **Rotate Sessions**: Gunakan session ID berbeda setiap hari
4. **Backup Cookies**: Save cookies file secara berkala

## 🔧 Troubleshooting

**Jika bot error:**
1. Cek koneksi internet RDP
2. Validate cookies dengan `python validate_cookies.py`  
3. Restart RDP server jika perlu
4. Contact support untuk bantuan teknis

## 💰 Monthly Costs

- 3x Windows RDP Server: $60/month
- ROI: Significant increase in live engagement
- Alternative: Start dengan 1 server ($20), scale up later

---
**Support**: Contact untuk bantuan setup atau troubleshooting
