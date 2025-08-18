#!/bin/bash

# Shopee Live Bot Launcher with Configurable Viewers
# Script untuk menjalankan bot dengan pengaturan jumlah viewers

echo "🚀 Shopee Live Bot - Configurable Viewers"
echo "=========================================="
echo ""

# Function untuk menghitung akun berdasarkan input.csv
count_accounts() {
    if [ -f "input.csv" ]; then
        # Hitung baris yang tidak kosong dan tidak diawali dengan #
        local count=$(grep -v '^#' input.csv | grep -v '^[[:space:]]*$' | wc -l)
        echo $count
    else
        echo 0
    fi
}

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python3 first."
    echo "💡 Install using: brew install python3"
    exit 1
fi

# Check if input.csv exists
if [ ! -f "input.csv" ]; then
    echo "❌ input.csv not found! Please create input.csv with account cookies."
    exit 1
fi

# Count available accounts
TOTAL_ACCOUNTS=$(count_accounts)
echo "📊 Available accounts in input.csv: $TOTAL_ACCOUNTS"

if [ $TOTAL_ACCOUNTS -eq 0 ]; then
    echo "❌ No valid accounts found in input.csv!"
    echo "💡 Please add your Shopee cookies to input.csv"
    exit 1
fi

echo ""
echo "🎯 RDP Configuration Options:"
echo "1. Single RDP (1-9 viewers) - Current setup"
echo "2. Dual RDP (10-18 viewers) - 2 servers" 
echo "3. Triple RDP (19-27 viewers) - 3 servers"
echo "4. Custom viewers - Manual input"
echo ""

read -p "🔢 Choose configuration [1-4]: " config_choice

case $config_choice in
    1)
        MAX_VIEWERS=9
        echo "✅ Single RDP mode: Maximum 9 viewers"
        ;;
    2)
        MAX_VIEWERS=18
        echo "✅ Dual RDP mode: Maximum 18 viewers"
        ;;
    3)
        MAX_VIEWERS=27
        echo "✅ Triple RDP mode: Maximum 27 viewers"
        ;;
    4)
        read -p "🔢 Enter desired number of viewers (max $TOTAL_ACCOUNTS): " custom_viewers
        if [[ $custom_viewers =~ ^[0-9]+$ ]] && [ $custom_viewers -le $TOTAL_ACCOUNTS ]; then
            MAX_VIEWERS=$custom_viewers
            echo "✅ Custom mode: $MAX_VIEWERS viewers"
        else
            echo "❌ Invalid input. Using maximum available: $TOTAL_ACCOUNTS"
            MAX_VIEWERS=$TOTAL_ACCOUNTS
        fi
        ;;
    *)
        echo "❌ Invalid choice. Using Single RDP mode (9 viewers)"
        MAX_VIEWERS=9
        ;;
esac

# Limit viewers to available accounts
if [ $MAX_VIEWERS -gt $TOTAL_ACCOUNTS ]; then
    echo "⚠️  Requested $MAX_VIEWERS viewers, but only $TOTAL_ACCOUNTS accounts available"
    MAX_VIEWERS=$TOTAL_ACCOUNTS
fi

echo ""
echo "📋 Bot Configuration:"
echo "   • Available accounts: $TOTAL_ACCOUNTS"
echo "   • Target viewers: $MAX_VIEWERS"
echo "   • Utilization: $(($MAX_VIEWERS * 100 / $TOTAL_ACCOUNTS))%"
echo ""

# Create temporary input file with limited accounts
TEMP_INPUT="input_temp.csv"
echo "🔧 Creating temporary input file with $MAX_VIEWERS accounts..."

# Copy header comments
grep '^#' input.csv > $TEMP_INPUT 2>/dev/null || true

# Copy only the required number of accounts
grep -v '^#' input.csv | grep -v '^[[:space:]]*$' | head -n $MAX_VIEWERS >> $TEMP_INPUT

if [ ! -f "$TEMP_INPUT" ] || [ $(wc -l < $TEMP_INPUT) -lt $MAX_VIEWERS ]; then
    echo "❌ Failed to create temporary input file!"
    exit 1
fi

echo "✅ Temporary input created with $MAX_VIEWERS accounts"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment!"
        exit 1
    fi
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "📦 Installing dependencies..."
pip install -r requirements.txt > /dev/null 2>&1

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies!"
    exit 1
fi

# Check if main.py exists
if [ ! -f "main.py" ]; then
    echo "❌ main.py not found!"
    exit 1
fi

echo ""
echo "✅ Setup complete!"
echo "🎯 Launching Shopee Live Bot with $MAX_VIEWERS viewers..."
echo "💡 Bot will use accounts from temporary input file"
echo ""

# Backup original input and use temp input
mv input.csv input_backup.csv
mv $TEMP_INPUT input.csv

# Run the bot
python main.py

# Restore original input file
echo ""
echo "🔄 Restoring original input file..."
mv input.csv $TEMP_INPUT
mv input_backup.csv input.csv

# Clean up temp file
rm -f $TEMP_INPUT

# Deactivate virtual environment
deactivate

echo ""
echo "✅ Bot execution completed!"
echo "📊 Used $MAX_VIEWERS out of $TOTAL_ACCOUNTS available accounts"
