# Shopee Live Multi-Account Bot v3.0

🚀 **Advanced multi-account system untuk scaling hingga 100+ viewers dengan auto-login**

Bot terbaru dengan sistem manajemen akun otomatis, login paralel, dan scaling yang powerful untuk kebutuhan komersial.

## ✨ New Features v3.0

- 👥 **Multi-Account Management** - CSV-based account database
- 🔑 **Auto-Login System** - Otomatis login semua akun
- 📊 **Scalability** - Support hingga 100+ viewers concurrent
- 🎯 **Session Management** - Auto-hunt active sessions
- 📈 **Statistics & Monitoring** - Real-time performance tracking
- 🛡️ **Account Protection** - Session persistence & cookie management

## 📁 Project Structure

```
bot-live-shopee/
├── 👥 multi_account_bot.py    # Main bot dengan multi-account support
├── ⚙️  bot_manager.sh          # Management dashboard
├── accounts/
│   └── shopee_accounts.csv    # Database akun (phone, password, status)
├── config/
│   └── bot_config.json        # Bot configuration
├── sessions/
│   └── viewer_*/              # Session data untuk setiap viewer
├── logs/
│   └── bot.log                # Activity logs
└── requirements.txt           # Python dependencies
```

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Install dependencies
pip install -r requirements.txt

# Make bot manager executable
chmod +x bot_manager.sh
```

### 2. Add Accounts
```bash
# Run bot manager
./bot_manager.sh

# Pilih option 2 (Account Manager)
# Add accounts manual atau edit CSV file
```

### 3. Run Multi-Account Bot
```bash
# Option 1 di bot manager
# Bot akan auto-login semua akun dan scale ke target viewers
```

## 📊 Account Management

### CSV Format (accounts/shopee_accounts.csv)
```csv
phone,password,status,cookies,last_login,notes
+6283185597189,@Sendi1x#,active,,2025-09-02,Test account 1
+6281234567890,password123,active,,2025-09-02,Account 2
+6287654321098,mypass456,inactive,,2025-09-01,Backup account
```

### Account Status
- **active** - Siap digunakan untuk bot
- **inactive** - Tidak akan digunakan
- **banned** - Akun di-suspend Shopee
- **error** - Error saat login terakhir

## 🎯 Bot Configuration

### config/bot_config.json
```json
{
  "bot_settings": {
    "max_concurrent_viewers": 100,
    "window_grid": "10x10",
    "delays": {
      "between_logins": 3,
      "page_load": 5
    },
    "chrome_options": {
      "disable_images": true,
      "user_data_dir": "sessions/"
    }
  },
  "target_session": {
    "auto_hunt": true
  },
  "account_management": {
    "rotate_accounts": true,
    "save_cookies": true
  }
}
```

## 🔥 Advanced Features

### 1. Auto-Login System
- Otomatis login ke semua akun aktif
- Session persistence dengan cookies
- Error handling dan retry mechanism

### 2. Smart Scaling
- Automatic account rotation
- Grid window positioning (10x10 layout)
- Resource optimization

### 3. Session Management
- Auto-hunt active live sessions
- Session validation sebelum deployment
- Multiple session support

### 4. Monitoring & Statistics
- Real-time viewer count tracking
- Login success rate monitoring
- Performance metrics dan logging

## 💪 Scaling Guide

### For 100+ Viewers:
1. **Prepare Accounts**: 100+ active Shopee accounts
2. **System Requirements**: 
   - 8GB+ RAM
   - Multi-core processor
   - SSD storage recommended
   - Stable internet (100+ Mbps)
3. **RDP Setup**: Windows RDP optimal untuk scaling
4. **Account Distribution**: 1 account = 1 viewer (typical)

### Account Preparation Strategy:
```bash
# 1. Register accounts dengan phone numbers berbeda
# 2. Verify semua accounts
# 3. Add ke CSV file
# 4. Test login dengan Account Manager
# 5. Deploy dengan Multi-Account Bot
```

## 🛠️ Bot Manager Commands

| Option | Function | Description |
|--------|----------|-------------|
| 1 | Multi-Account Bot | Main bot dengan auto-login |
| 2 | Account Manager | Add/edit/test accounts |
| 3 | Session Hunter | Find active live sessions |
| 4 | Bot Configuration | Edit settings |
| 5 | View Statistics | Performance metrics |
| 6 | Stop All Bots | Emergency stop |
| 7 | Clean Sessions | Clear session data |
| 8 | Help & Guide | Documentation |

## 📈 Performance Optimization

### System Optimization:
- Use SSD storage untuk session data
- Monitor RAM usage (target: <80%)
- Disable unnecessary Chrome features
- Use image/CSS blocking untuk performance

### Account Optimization:
- Distribute accounts across different IPs (advanced)
- Use fresh accounts untuk best success rate
- Regular account health monitoring
- Rotate accounts untuk avoid detection

## 🔧 Troubleshooting

### Common Issues:

**🚫 Login Failed**
```bash
# Check account credentials di CSV
# Verify account status (not banned)
# Test manual login di browser
# Check for 2FA/captcha requirements
```

**🚫 Chrome Crashes**
```bash
# Reduce concurrent viewers
# Clean session data (option 7)
# Check system resources
# Update Chrome browser
```

**🚫 Session Not Found**
```bash
# Use Session Hunter (option 3)
# Check live stream masih aktif
# Try different session IDs
# Hunt at peak hours (19:00-23:00 WIB)
```

**🚫 Low Success Rate**
```bash
# Verify account quality
# Check internet stability
# Reduce concurrent logins
# Clean old session data
```

## 📊 Success Metrics

### Target Performance:
- **Login Success Rate**: >90%
- **Live Connection Rate**: >85%
- **Session Stability**: >95% uptime
- **Resource Usage**: <80% RAM, <70% CPU

### Monitoring KPIs:
- Active viewers count
- Account health status
- Session duration
- Error rate tracking

## 🚨 Important Notes

### Account Management:
- **Never share accounts** between different operators
- **Use unique phone numbers** untuk setiap account
- **Regular password updates** recommended
- **Monitor for Shopee policy changes**

### Legal & Ethical:
- Bot untuk educational/testing purposes
- Follow Shopee Terms of Service
- Respect platform rate limits
- Use responsibly dan ethically

### Security:
- Keep account credentials secure
- Use VPN untuk additional privacy (advanced)
- Regular security audits
- Monitor for suspicious account activity

## 🎯 Business Use Cases

### Service Provider Setup:
1. **Account Pool**: 100-500 accounts for multiple clients
2. **Session Rotation**: Multiple live sessions support
3. **Client Dashboard**: Statistics dan reporting
4. **Automated Scaling**: Dynamic viewer adjustment

### ROI Optimization:
- **Cost per viewer**: Optimize account acquisition cost
- **Session efficiency**: Maximize viewer duration
- **Resource utilization**: Optimal hardware usage
- **Success rate**: Minimize failed attempts

## 📞 Support & Updates

### Getting Help:
1. Check troubleshooting guide
2. Review log files (logs/bot.log)
3. Test dengan minimal setup
4. Check system requirements

### Updates & Maintenance:
- Regular dependency updates
- Chrome version compatibility
- Account health monitoring
- Performance optimization tuning

---

## 🏆 **READY FOR COMMERCIAL DEPLOYMENT!**

✅ **Multi-Account System** - Support 100+ viewers  
✅ **Auto-Login Management** - Zero manual intervention  
✅ **Scalable Architecture** - Enterprise-ready  
✅ **Performance Monitoring** - Real-time insights  
✅ **Session Management** - Auto session discovery  
✅ **Resource Optimization** - Maximum efficiency  

**Bot siap untuk deployment komersial dengan sistem manajemen akun otomatis!** 🚀
