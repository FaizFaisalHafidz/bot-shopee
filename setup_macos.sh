#!/bin/bash

# Setup script untuk Shopee Live Bot di macOS
# Script ini akan menyiapkan virtual environment dan dependencies

echo "🍎 Shopee Live Bot Setup for macOS"
echo "=================================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 tidak ditemukan!"
    echo ""
    echo "Silakan install Python3 terlebih dahulu:"
    echo "1. Via Homebrew: brew install python3"
    echo "2. Via official installer: https://www.python.org/downloads/"
    echo ""
    exit 1
fi

# Show Python version
python_version=$(python3 --version)
echo "✅ $python_version ditemukan"

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 tidak ditemukan!"
    echo "Silakan install pip3: python3 -m ensurepip --upgrade"
    exit 1
fi

echo "✅ pip3 tersedia"

# Create virtual environment
echo ""
echo "📦 Membuat virtual environment..."
if [ -d "venv" ]; then
    echo "⚠️ Virtual environment sudah ada, menghapus yang lama..."
    rm -rf venv
fi

python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "❌ Gagal membuat virtual environment!"
    exit 1
fi

echo "✅ Virtual environment berhasil dibuat"

# Activate virtual environment
echo "🔧 Mengaktifkan virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrade pip..."
pip install --upgrade pip

# Install requirements
echo "📦 Installing dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    if [ $? -eq 0 ]; then
        echo "✅ Dependencies berhasil diinstall"
    else
        echo "❌ Gagal install dependencies"
        exit 1
    fi
else
    echo "⚠️ requirements.txt tidak ditemukan, install manual..."
    pip install requests
fi

# Check if input.csv exists
if [ ! -f "input.csv" ]; then
    echo ""
    echo "⚠️ File input.csv tidak ditemukan!"
    echo "📝 Membuat contoh input.csv..."
    
    cat > input.csv << 'EOF'
_gcl_au=1.1.669529887.1715354495; _fbp=fb.2.1715354495515.451566588; SPC_F=3yIwDla4UmPmbQ4j2Y00KsvxCwownztm; SPC_U=1254699641; csrftoken=0zUQkUHteX31OqbP28cPXJZOPuzx7WYB
EOF
    
    echo "✅ File input.csv contoh telah dibuat"
    echo "💡 Silakan ganti dengan cookie akun Shopee yang valid"
fi

# Create .gitignore if not exists
if [ ! -f ".gitignore" ]; then
    echo ""
    echo "📝 Membuat .gitignore..."
    cat > .gitignore << 'EOF'
# Virtual Environment
venv/
env/
.venv/

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so

# Logs
*.log
logs/

# OS
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
*.swp
*.swo

# Sensitive data
input.csv
config_local.json
EOF
    echo "✅ .gitignore berhasil dibuat"
fi

# Deactivate virtual environment
deactivate

echo ""
echo "🎉 Setup selesai!"
echo ""
echo "📋 Langkah selanjutnya:"
echo "1. Edit file input.csv dengan cookie akun Shopee yang valid"
echo "2. Jalankan bot dengan: ./run.sh"
echo "   atau: bash run.sh"
echo ""
echo "💡 Tips:"
echo "- Pastikan file run.sh executable: chmod +x run.sh"
echo "- Untuk development, aktifkan venv: source venv/bin/activate"
echo "- Untuk deaktivasi venv: deactivate"
echo ""
