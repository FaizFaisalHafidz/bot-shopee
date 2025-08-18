#!/bin/bash

echo
echo "========================================"
echo "   SIMPLE SHOPEE BOT - DIRECT APPROACH"
echo "========================================"
echo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[ERROR]${NC} Python3 tidak ditemukan!"
    echo "Silakan install Python3 terlebih dahulu:"
    echo "brew install python3"
    echo "atau download dari: https://www.python.org/downloads/"
    echo
    exit 1
fi

echo -e "${GREEN}[SUCCESS]${NC} Python3 found: $(python3 --version)"

# Check if required packages are installed
echo -e "${YELLOW}[INFO]${NC} Checking dependencies..."

if ! python3 -c "import selenium" &> /dev/null; then
    echo -e "${YELLOW}[INSTALL]${NC} Installing selenium..."
    pip3 install selenium
    if [ $? -ne 0 ]; then
        echo -e "${RED}[ERROR]${NC} Failed to install selenium!"
        exit 1
    fi
fi

if ! python3 -c "import undetected_chromedriver" &> /dev/null; then
    echo -e "${YELLOW}[INSTALL]${NC} Installing undetected-chromedriver..."
    pip3 install undetected-chromedriver
    if [ $? -ne 0 ]; then
        echo -e "${YELLOW}[WARNING]${NC} Failed to install undetected-chromedriver, using regular selenium"
    fi
fi

echo -e "${GREEN}[SUCCESS]${NC} All dependencies ready!"
echo

# Check for input.csv
if [ ! -f "input.csv" ]; then
    echo -e "${RED}[ERROR]${NC} File input.csv tidak ditemukan!"
    echo "Pastikan file input.csv berisi cookie akun Shopee ada di folder ini."
    echo "Format: SPC_U=...; SPC_T_ID=...; csrftoken=...; (satu baris per akun)"
    echo
    exit 1
fi

echo -e "${GREEN}[SUCCESS]${NC} Found input.csv file"
echo

echo "========================================"
echo "        MENJALANKAN SIMPLE BOT"
echo "========================================"
echo
echo "Mode: NO API Verification (Direct)"
echo "Strategi: Cookie Injection + Direct Navigation"
echo "Target: Bypass Shopee detection dengan cara sederhana"
echo

# Run the simple bot
python3 simple_direct_bot.py

if [ $? -ne 0 ]; then
    echo
    echo -e "${RED}[ERROR]${NC} Bot mengalami error!"
    echo "Coba jalankan ulang atau cek log error di atas."
else
    echo
    echo -e "${GREEN}[SUCCESS]${NC} Simple Bot selesai!"
fi

echo
read -p "Press Enter to continue..."
