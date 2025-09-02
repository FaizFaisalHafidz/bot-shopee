#!/bin/bash
# Shopee Live Multi-Account Bot Manager v3.0

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║          SHOPEE LIVE MULTI-ACCOUNT BOT v3.0 MANAGER         ║"
echo "║                 SCALE TO 100+ VIEWERS                       ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Check and activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
    echo -e "${GREEN}✅ Virtual environment activated${NC}"
else
    echo -e "${YELLOW}⚠️ Virtual environment not found, using system Python${NC}"
fi

show_menu() {
    echo "Available tools:"
    echo ""
    echo "1. 👥 Multi-Account Bot      (100+ viewers with auto-login)"
    echo "2. 📊 Account Manager        (View/Edit accounts)"  
    echo "3. 🔍 Session Hunter         (Find active sessions)"
    echo "4. ⚙️  Bot Configuration     (Settings)"
    echo "5. 📈 View Statistics        (Bot performance)"
    echo "6. 🛑 Stop All Bots"
    echo "7. 🧹 Clean Sessions/Logs"
    echo "8. ❓ Help & Guide"
    echo "0. Exit"
    echo ""
}

run_multi_account_bot() {
    echo -e "${GREEN}👥 Starting Multi-Account Bot...${NC}"
    echo ""
    python3 multi_account_bot.py
}

manage_accounts() {
    echo -e "${BLUE}📊 Account Manager${NC}"
    echo ""
    
    if [ -f "accounts/shopee_accounts.csv" ]; then
        echo "Current accounts:"
        echo "================="
        head -10 accounts/shopee_accounts.csv | column -t -s','
        echo ""
        echo "Total accounts: $(tail -n +2 accounts/shopee_accounts.csv | wc -l)"
        echo ""
        echo "Options:"
        echo "1. Add new account"
        echo "2. View all accounts"
        echo "3. Edit accounts file"
        echo "4. Test account login"
        echo ""
        read -p "Select option (1-4): " acc_choice
        
        case $acc_choice in
            1) add_new_account ;;
            2) view_all_accounts ;;
            3) edit_accounts_file ;;
            4) test_account_login ;;
        esac
    else
        echo "No accounts file found. Creating template..."
        mkdir -p accounts
        echo "phone,password,status,cookies,last_login,notes" > accounts/shopee_accounts.csv
        echo "+6283185597189,@Sendi1x#,active,,2025-09-02,Test account 1" >> accounts/shopee_accounts.csv
        echo "Template created: accounts/shopee_accounts.csv"
    fi
}

add_new_account() {
    echo -e "${CYAN}➕ Add New Account${NC}"
    echo ""
    read -p "Phone number (with +62): " phone
    read -s -p "Password: " password
    echo ""
    read -p "Notes (optional): " notes
    
    echo "$phone,$password,active,,$(date +%Y-%m-%d),${notes:-Added via manager}" >> accounts/shopee_accounts.csv
    echo "✅ Account added successfully!"
}

view_all_accounts() {
    echo -e "${CYAN}📋 All Accounts${NC}"
    echo ""
    cat accounts/shopee_accounts.csv | column -t -s','
}

edit_accounts_file() {
    echo "Opening accounts file for editing..."
    if command -v nano &> /dev/null; then
        nano accounts/shopee_accounts.csv
    elif command -v vim &> /dev/null; then
        vim accounts/shopee_accounts.csv
    else
        echo "Please edit: accounts/shopee_accounts.csv manually"
        open accounts/shopee_accounts.csv 2>/dev/null || true
    fi
}

test_account_login() {
    echo -e "${YELLOW}🧪 Test Account Login${NC}"
    echo ""
    python3 -c "
import csv
print('Available accounts:')
with open('accounts/shopee_accounts.csv', 'r') as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader, 1):
        print(f'{i}. {row[\"phone\"]} - {row[\"status\"]}')
"
    echo ""
    echo "Note: Use Multi-Account Bot option 1 to test login functionality"
}

hunt_sessions() {
    echo -e "${BLUE}🔍 Starting Session Hunter...${NC}"
    python3 -c "
from multi_account_bot import SessionHunter
hunter = SessionHunter()
sessions = hunter.find_active_sessions()
print(f'Found {len(sessions)} active sessions')
for session in sessions:
    print(f'Session ID: {session[\"session_id\"]}')
    print(f'URL: {session[\"url\"]}')
    print('---')
"
}

configure_bot() {
    echo -e "${YELLOW}⚙️  Bot Configuration${NC}"
    echo ""
    
    if [ -f "config/bot_config.json" ]; then
        echo "Current configuration:"
        cat config/bot_config.json | python3 -m json.tool
        echo ""
        echo "Edit configuration? (y/n)"
        read -n 1 -r
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            if command -v nano &> /dev/null; then
                nano config/bot_config.json
            else
                echo "Please edit: config/bot_config.json manually"
                open config/bot_config.json 2>/dev/null || true
            fi
        fi
    else
        echo "Configuration file not found!"
    fi
}

view_statistics() {
    echo -e "${CYAN}📈 Bot Statistics${NC}"
    echo ""
    
    if [ -f "logs/bot.log" ]; then
        echo "Recent activity:"
        echo "==============="
        tail -20 logs/bot.log
        echo ""
        echo "Statistics:"
        echo "----------"
        echo "Login attempts: $(grep -c "Logging in viewer" logs/bot.log 2>/dev/null || echo "0")"
        echo "Successful logins: $(grep -c "login successful" logs/bot.log 2>/dev/null || echo "0")"
        echo "Live connections: $(grep -c "connected to live session" logs/bot.log 2>/dev/null || echo "0")"
        echo "Errors: $(grep -c "ERROR" logs/bot.log 2>/dev/null || echo "0")"
    else
        echo "No log file found. Run the bot first to generate statistics."
    fi
}

stop_all_bots() {
    echo -e "${RED}🛑 Stopping all bots...${NC}"
    
    # Kill Python bot processes
    pkill -f "python.*multi_account_bot" 2>/dev/null || true
    pkill -f "multi_account_bot.py" 2>/dev/null || true
    
    # Kill Chrome processes (ask user first)
    chrome_count=$(ps aux | grep -i chrome | grep -v grep | wc -l)
    if [ $chrome_count -gt 0 ]; then
        echo "Found $chrome_count Chrome processes"
        read -p "Kill all Chrome processes? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            pkill -f chrome 2>/dev/null || true
            echo "Chrome processes terminated"
        fi
    fi
    
    echo "Bot processes stopped"
}

clean_sessions() {
    echo -e "${YELLOW}🧹 Cleaning sessions and logs...${NC}"
    
    # Clean session directories
    if [ -d "sessions" ]; then
        read -p "Clean session data? This will log out all accounts (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf sessions/*
            echo "Session data cleaned"
        fi
    fi
    
    # Clean logs
    if [ -f "logs/bot.log" ]; then
        read -p "Clean log files? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            > logs/bot.log
            echo "Log files cleaned"
        fi
    fi
    
    echo "Cleanup completed"
}

show_help() {
    echo -e "${BLUE}❓ MULTI-ACCOUNT BOT GUIDE${NC}"
    echo ""
    echo "🎯 QUICK START:"
    echo "1. Add accounts to CSV (option 2)"
    echo "2. Run Multi-Account Bot (option 1)"
    echo "3. Bot will auto-login and scale to 100+ viewers"
    echo ""
    echo "📋 ACCOUNT MANAGEMENT:"
    echo "• CSV format: phone,password,status,cookies,last_login,notes"
    echo "• Phone format: +6283185597189"
    echo "• Status: active/inactive/banned"
    echo "• Bot auto-saves cookies for faster subsequent logins"
    echo ""
    echo "🔥 SCALING TIPS:"
    echo "• 1 account = 1 viewer (typical)"
    echo "• For 100 viewers, prepare 100 active accounts"
    echo "• Bot automatically manages login rotation"
    echo "• Session data saved for faster restarts"
    echo ""
    echo "🛡️ SECURITY TIPS:"
    echo "• Use different phone numbers for each account"
    echo "• Avoid using same IP for too many accounts"
    echo "• Consider using proxy rotation (advanced)"
    echo ""
    echo "⚡ PERFORMANCE TIPS:"
    echo "• Windows RDP recommended for scaling"
    echo "• 8GB+ RAM for 100+ viewers"
    echo "• Monitor CPU usage"
    echo "• Use SSD storage for session data"
    echo ""
    echo "🔧 TROUBLESHOOTING:"
    echo "• If login fails: Check account credentials"
    echo "• If Chrome crashes: Reduce concurrent viewers"
    echo "• If slow performance: Clean session data"
    echo ""
}

check_dependencies() {
    echo "🔍 Checking dependencies..."
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}❌ Python 3 not found${NC}"
        exit 1
    fi
    
    # Check required Python packages
    python3 -c "
try:
    import selenium, webdriver_manager, requests, concurrent.futures
    print('✅ All Python packages available')
except ImportError as e:
    print(f'❌ Missing package: {e}')
    print('Run: pip install selenium webdriver-manager requests')
    exit(1)
" || exit 1
    
    # Check Chrome
    if ! command -v google-chrome &> /dev/null && ! command -v chromium-browser &> /dev/null && ! ls /Applications/Google\ Chrome.app &> /dev/null; then
        echo -e "${YELLOW}⚠️ Chrome browser not found - please install Google Chrome${NC}"
    else
        echo "✅ Chrome browser available"
    fi
    
    echo "✅ Dependencies check completed"
}

# Main loop
echo "🔍 Checking system..."
check_dependencies
echo ""

while true; do
    show_menu
    read -p "Select option (0-8): " choice
    echo ""
    
    case $choice in
        1) run_multi_account_bot ;;
        2) manage_accounts ;;
        3) hunt_sessions ;;
        4) configure_bot ;;
        5) view_statistics ;;
        6) stop_all_bots ;;
        7) clean_sessions ;;
        8) show_help ;;
        0) 
            echo "👋 Goodbye!"
            exit 0
            ;;
        *)
            echo -e "${RED}❌ Invalid option${NC}"
            ;;
    esac
    
    echo ""
    read -p "Press ENTER to continue..."
    echo ""
done
