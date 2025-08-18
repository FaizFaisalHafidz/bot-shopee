#!/bin/bash

# Advanced Bot Launcher untuk macOS dengan Virtual Environment
# Script untuk menjalankan advanced bot dengan fitur lengkap

echo "🚀 Shopee Live Bot Advanced - macOS"
echo "====================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment tidak ditemukan!"
    echo "📝 Jalankan setup terlebih dahulu: ./setup_macos.sh"
    exit 1
fi

# Check if input.csv exists
if [ ! -f "input.csv" ]; then
    echo "❌ input.csv not found! Please create input.csv with account cookies."
    exit 1
fi

# Check if advanced_bot.py exists
if [ ! -f "advanced_bot.py" ]; then
    echo "❌ advanced_bot.py not found!"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
echo "📋 Checking dependencies..."
python -c "import requests" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 Installing missing dependencies..."
    pip install -r requirements.txt
fi

echo "✅ All requirements satisfied!"
echo "🎯 Launching Advanced Shopee Live Bot..."
echo ""

# Run the advanced bot
python advanced_bot.py

# Deactivate virtual environment when done
deactivate

echo ""
echo "👋 Advanced Bot session ended."
