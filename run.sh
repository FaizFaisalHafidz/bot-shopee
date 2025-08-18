#!/bin/bash

# Shopee Live Bot Launcher for macOS
# Script untuk menjalankan bot dengan virtual environment

echo "🚀 Starting Shopee Live Bot for macOS..."
echo "📋 Checking requirements..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python3 first."
    echo "💡 Install using: brew install python3"
    exit 1
fi

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt not found!"
    exit 1
fi

# Check if input.csv exists
if [ ! -f "input.csv" ]; then
    echo "❌ input.csv not found! Please create input.csv with account cookies."
    exit 1
fi

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

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📦 Installing dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies!"
    exit 1
fi

# Check if main.py exists
if [ ! -f "main.py" ]; then
    echo "❌ main.py not found!"
    exit 1
fi

echo "✅ All requirements satisfied!"
echo "🎯 Launching Shopee Live Bot..."
echo ""

# Run the bot
python main.py

# Deactivate virtual environment when done
deactivate
