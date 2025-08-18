#!/bin/bash

# Cookie Helper Launcher
# Script untuk membantu setup cookie Shopee

echo "🍪 Shopee Cookie Helper"
echo "======================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment tidak ditemukan!"
    echo "📝 Jalankan setup terlebih dahulu: ./setup_macos.sh"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if cookie_helper.py exists
if [ ! -f "cookie_helper.py" ]; then
    echo "❌ cookie_helper.py not found!"
    exit 1
fi

echo "✅ Ready to help with cookie setup!"
echo ""

# Run the cookie helper
python cookie_helper.py

# Deactivate virtual environment when done
deactivate

echo ""
echo "👋 Cookie helper session ended."
