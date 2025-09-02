# TEMP PROFILE SYSTEM GUIDE

## Overview
Sistem temporary profile dibuat untuk menghindari konflik dengan Chrome yang sedang berjalan dan memberikan isolation yang lebih baik untuk bot automation.

## Files yang Terlibat

### 1. Scripts Utama
- `create_temp_profiles.py` - Membuat copy temporary dari Chrome profiles
- `check_chrome_process.bat` - Check dan kill Chrome process jika diperlukan
- `run_with_temp_profiles.bat` - Launcher lengkap dengan temp profile system
- `cleanup_temp_profiles.bat` - Cleanup temporary files

### 2. Bot Scripts (Updated)
- `scripts/shopee_bot.py` - Updated untuk support temp profiles
- `scripts/detect_profiles_clean.py` - Detect existing Chrome profiles

## How It Works

### Step 1: Profile Detection
```
python scripts/detect_profiles_clean.py
```
- Scans Chrome User Data directories
- Extracts email and display name from Preferences files
- Creates `temp_profiles.json`

### Step 2: Create Temp Copies
```
python create_temp_profiles.py
```
- Creates `sessions/temp_bot_profiles/` directory
- Copies essential Chrome files (Preferences, Cookies, Login Data, etc.)
- Creates isolated profile copies for bot usage
- Generates `temp_bot_profiles.json` index

### Step 3: Chrome Process Check
```
check_chrome_process.bat
```
- Lists active Chrome processes
- Option to kill all Chrome processes if needed
- Prevents profile lock conflicts

### Step 4: Bot Execution
```
cd scripts && python shopee_bot.py
```
- Prioritizes temp profiles over regular profiles
- Uses Chrome executable detection
- Runs isolated Chrome instances

## Benefits

### 1. No Chrome Conflicts
- Temp profiles avoid "Chrome is already running" errors
- Original Chrome can stay open for normal browsing
- No profile locking issues

### 2. Better Isolation
- Each bot instance gets its own profile copy
- Changes don't affect original profiles
- Safer for automation

### 3. Easy Cleanup
- All temp files in dedicated directory
- Simple cleanup script removes all traces
- No permanent changes to system

## Usage Patterns

### Quick Start (Recommended)
```bash
run_with_temp_profiles.bat
```

### Manual Steps
```bash
# 1. Detect profiles
python scripts/detect_profiles_clean.py

# 2. Create temp copies  
python create_temp_profiles.py

# 3. Check Chrome processes
check_chrome_process.bat

# 4. Run bot
cd scripts && python shopee_bot.py

# 5. Cleanup when done
cleanup_temp_profiles.bat
```

### Development/Testing
```bash
# Use regular profiles (faster but less safe)
run_simplified.bat
```

## Files Created

### Temporary Files
- `sessions/temp_bot_profiles/temp_profile_1_email_at_gmail_com/` - Profile copies
- `temp_bot_profiles.json` - Temp profile index
- `temp_profiles.json` - Original profile detection results

### Logs
- `logs/bot.log` - Main bot logs
- Various debug logs as needed

## Troubleshooting

### Issue: Chrome processes won't die
- Use Task Manager to force kill chrome.exe
- Restart command prompt as Administrator
- Try `taskkill /f /im chrome.exe /t`

### Issue: Permission errors copying profiles
- Close all Chrome instances first
- Run as Administrator if needed
- Check if profiles are on network drive

### Issue: Bot can't find temp profiles
- Check if `temp_bot_profiles.json` exists
- Verify temp profile directories were created
- Re-run `create_temp_profiles.py`

### Issue: Login sessions not preserved
- Verify essential files were copied (Cookies, Login Data)
- Check Chrome version compatibility
- Original profiles must be properly logged in

## Notes

### Performance Impact
- Temp profile creation takes 30-60 seconds
- Each profile copy uses 50-200MB disk space
- Cleanup is instant

### Security Considerations  
- Temp profiles contain login credentials
- Auto-cleanup on script completion
- Don't commit temp files to version control

### Chrome Updates
- Bot uses actual Chrome executable (not Chromium)
- ChromeDriver auto-updated via webdriver-manager
- Profile format compatibility maintained

## File Structure After Setup
```
bot-live-shopee/
├── sessions/
│   └── temp_bot_profiles/
│       ├── temp_profile_1_email_at_gmail_com/
│       ├── temp_profile_2_email_at_gmail_com/
│       └── ...
├── temp_bot_profiles.json
├── temp_profiles.json
└── logs/
    └── bot.log
```
