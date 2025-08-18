#!/bin/bash

# Cookie Validator Launcher
# Script untuk memvalidasi cookie di input.csv

echo "🍪 Shopee Cookie Validator"
echo "=========================="
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

# Check if validate_cookies.py exists
if [ ! -f "validate_cookies.py" ]; then
    echo "❌ validate_cookies.py not found!"
    exit 1
fi

# Check if input.csv exists
if [ ! -f "input.csv" ]; then
    echo "❌ input.csv not found!"
    echo "💡 Create input.csv dengan cookie akun Shopee terlebih dahulu"
    exit 1
fi

echo "✅ Ready to validate cookies!"
echo ""

# Run the cookie validator
python validate_cookies.py

# Deactivate virtual environment when done
deactivate

echo ""
echo "👋 Validation completed."
