#!/bin/bash
# Raspberry Pi Ads Player Installation Script
# This script installs all necessary dependencies and optimizations for the ads player

echo "🚀 Installing Raspberry Pi Ads Player..."

# Update system
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Python dependencies
echo "🐍 Installing Python and pip..."
sudo apt install -y python3 python3-pip python3-venv

# Install multimedia libraries and hardware acceleration
echo "🎬 Installing multimedia libraries..."
sudo apt install -y \
    omxplayer \
    vlc \
    ffmpeg \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libfreetype6-dev \
    libportmidi-dev \
    libjpeg-dev \
    python3-dev \
    python3-numpy \
    libatlas-base-dev

# Install GPU memory split for better video performance
echo "🎯 Optimizing GPU memory..."
sudo raspi-config nonint do_memory_split 128

# Enable hardware acceleration
echo "⚡ Enabling hardware acceleration..."
sudo raspi-config nonint do_camera 0

# Create virtual environment
echo "🔧 Setting up Python virtual environment..."
python3 -m venv ads_player_env
source ads_player_env/bin/activate

# Install Python packages
echo "📦 Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

# Create ads directory
echo "📁 Creating ads directory..."
mkdir -p ads

# Set up systemd service for auto-start
echo "🚀 Setting up auto-start service..."
cat > ads_player.service << EOF
[Unit]
Description=Raspberry Pi Ads Player
After=graphical.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/ads_player
Environment=DISPLAY=:0
ExecStart=/home/pi/ads_player/ads_player_env/bin/python /home/pi/ads_player/ads_player.py
Restart=always
RestartSec=5

[Install]
WantedBy=graphical.target
EOF

# Copy service file to systemd
sudo cp ads_player.service /etc/systemd/system/
sudo systemctl daemon-reload

echo "✅ Installation complete!"
echo ""
echo "🎯 Next steps:"
echo "1. Add your ads (images/videos) to the 'ads' directory"
echo "2. Modify config.json for your specific needs"
echo "3. Test the player: python3 ads_player.py"
echo "4. Enable auto-start: sudo systemctl enable ads_player.service"
echo "5. Start service: sudo systemctl start ads_player.service"
echo ""
echo "📋 Useful commands:"
echo "   Status: sudo systemctl status ads_player.service"
echo "   Stop:   sudo systemctl stop ads_player.service"
echo "   Logs:   sudo journalctl -u ads_player.service -f"
echo ""
echo "🎮 Controls while running:"
echo "   ESC/Q: Quit"
echo "   SPACE: Next ad"
echo "   R: Reload ads"
echo "   S: Shuffle ads"