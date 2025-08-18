#!/bin/bash

# Setup script untuk Digital Ocean Ubuntu
# Bot Shopee Live Streaming

echo "🚀 Setting up Shopee Bot di Digital Ocean Ubuntu..."

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3 dan pip
sudo apt install python3 python3-pip python3-venv git curl -y

# Clone repository (ganti dengan repo Anda)
git clone https://github.com/your-repo/shopee-bot.git
cd shopee-bot

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Set permissions
chmod +x run.sh
chmod +x validate.sh

# Create systemd service untuk auto-start
sudo tee /etc/systemd/system/shopee-bot.service > /dev/null <<EOF
[Unit]
Description=Shopee Live Bot
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=/home/$USER/shopee-bot
Environment=PATH=/home/$USER/shopee-bot/venv/bin
ExecStart=/home/$USER/shopee-bot/venv/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

echo "✅ Setup complete!"
echo "📝 Edit input.csv dengan cookies Anda"
echo "🏃 Jalankan: systemctl --user enable shopee-bot"
