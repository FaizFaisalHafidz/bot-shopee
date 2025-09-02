#!/bin/bash
# SETUP SCRIPT - Recreate environment after git clone
# Recreates virtual environment and installs dependencies

echo "=============================================================================="
echo "   SHOPEE BOT - ENVIRONMENT SETUP"
echo "   Recreating virtual environment and installing dependencies"
echo "=============================================================================="
echo

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ ERROR: Python 3 not found!"
    echo "Please install Python 3.7+ first:"
    echo "  - Windows: https://www.python.org/downloads/"
    echo "  - macOS: brew install python3"
    echo "  - Linux: sudo apt install python3 python3-venv"
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Create virtual environment
echo "[SETUP] Creating virtual environment..."
python3 -m venv venv
echo "✅ Virtual environment created"

# Activate virtual environment
echo "[SETUP] Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"

# Upgrade pip
echo "[SETUP] Upgrading pip..."
pip install --upgrade pip
echo "✅ Pip upgraded"

# Install Python dependencies
echo "[SETUP] Installing Python dependencies..."
pip install selenium webdriver-manager requests
echo "✅ Python dependencies installed"

# Install Node.js dependencies (for Chrome extension)
if [ -f "package.json" ]; then
    echo "[SETUP] Installing Node.js dependencies..."
    if command -v npm &> /dev/null; then
        npm install
        echo "✅ Node.js dependencies installed"
    else
        echo "⚠️ npm not found, skipping Node.js dependencies"
        echo "Install Node.js if you need Chrome extension features"
    fi
fi

# Create necessary directories
echo "[SETUP] Creating necessary directories..."
mkdir -p sessions/real_url_viewers
mkdir -p sessions/device_profiles
mkdir -p sessions/chrome_profiles
mkdir -p logs
mkdir -p accounts
echo "✅ Directories created"

# Verify installation
echo "[VERIFY] Verifying installation..."
python3 -c "import selenium, webdriver_manager, requests; print('✅ All Python dependencies OK')" || {
    echo "❌ Dependency verification failed"
    exit 1
}

echo
echo "=============================================================================="
echo "   SETUP COMPLETED SUCCESSFULLY"
echo "=============================================================================="
echo "Environment ready for Shopee bot deployment!"
echo
echo "Available launchers:"
echo "  🚀 ./ultimate_launcher.sh - Complete launcher with all options"
echo "  🎯 python3 real_url_bot.py <session_id> <viewer_count> - Direct execution"
echo
echo "Example usage:"
echo "  ./ultimate_launcher.sh"
echo "  python3 real_url_bot.py 157658364 3"
echo
echo "=============================================================================="
