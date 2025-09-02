#!/bin/bash
# SHOPEE ULTIMATE REAL URL BOT - FINAL DEPLOYMENT SCRIPT FOR RDP
# Complete solution with exact Shopee Live URL structure

echo "=============================================================================="
echo "   SHOPEE ULTIMATE REAL URL BOT - FINAL DEPLOYMENT"
echo "   Complete Authentication Bypass + Real URL Structure + Device Diversity"
echo "=============================================================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "[SETUP] Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install selenium webdriver-manager requests
else
    echo "[SETUP] Activating existing virtual environment..."
    source venv/bin/activate
fi

# Check dependencies
echo "[CHECK] Verifying dependencies..."
python3 -c "import selenium, webdriver_manager; print('Dependencies OK')" || {
    echo "[INSTALL] Installing missing dependencies..."
    pip install selenium webdriver-manager requests
}

# Create necessary directories
mkdir -p sessions/real_url_viewers
mkdir -p logs

echo
echo "Available launch options:"
echo "1. Real URL Bot (Recommended) - Exact Shopee Live URL structure"
echo "2. Device Fingerprint Bot - Advanced device spoofing"
echo "3. Auth Bypass Bot - Authentication bypass only"
echo "4. Custom configuration"
echo

read -p "Select option (1-4): " choice

case $choice in
    1)
        echo "[LAUNCH] Starting Real URL Bot with exact Shopee Live structure..."
        read -p "Enter Shopee Live Session ID: " session_id
        read -p "Enter viewer count (default 3): " viewer_count
        viewer_count=${viewer_count:-3}
        
        echo
        echo "Starting Real URL Bot..."
        echo "Session: $session_id"
        echo "Viewers: $viewer_count" 
        echo "URL Structure: EXACT Shopee Live format"
        echo
        
        python3 real_url_bot.py $session_id $viewer_count
        ;;
    2)
        echo "[LAUNCH] Starting Device Fingerprint Bot..."
        read -p "Enter Shopee Live Session ID: " session_id
        read -p "Enter device count (default 3): " device_count
        device_count=${device_count:-3}
        
        python3 device_fingerprint_bot.py $session_id $device_count
        ;;
    3)
        echo "[LAUNCH] Starting Auth Bypass Bot..."
        read -p "Enter Shopee Live Session ID: " session_id
        read -p "Enter viewer count (default 3): " viewer_count
        viewer_count=${viewer_count:-3}
        
        python3 auth_bypass_bot.py $session_id $viewer_count
        ;;
    4)
        echo "[CUSTOM] Custom configuration..."
        read -p "Enter bot script name: " bot_script
        read -p "Enter session ID: " session_id
        read -p "Enter parameters: " params
        
        python3 $bot_script $session_id $params
        ;;
    *)
        echo "Invalid option. Launching Real URL Bot (default)..."
        read -p "Enter Shopee Live Session ID: " session_id
        python3 real_url_bot.py $session_id 3
        ;;
esac

echo
echo "Bot execution completed."
echo "Check logs/ directory for detailed logs."
