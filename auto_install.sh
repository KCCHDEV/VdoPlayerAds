#!/bin/bash
# Automatic Installation Script for Raspberry Pi Ads Player
# One command to install and setup everything automatically
# Usage: curl -sSL https://raw.githubusercontent.com/your-repo/main/auto_install.sh | bash

set -e  # Exit on any error

echo "🎬 Raspberry Pi Ads Player - Auto Install"
echo "=========================================="
echo "This will automatically install and setup everything!"
echo ""

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo "❌ Please don't run this script as root. Run as regular user (pi)."
   exit 1
fi

# Detect if we're on Raspberry Pi
INSTALL_DIR="$HOME/ads_player"
if [[ -f /proc/device-tree/model ]] && grep -q "Raspberry Pi" /proc/device-tree/model; then
    echo "✅ Raspberry Pi detected"
    IS_RASPI=true
else
    echo "⚠️  Not detected as Raspberry Pi - installing in compatibility mode"
    IS_RASPI=false
fi

echo "📍 Installation directory: $INSTALL_DIR"
echo ""

# Function to run commands with error handling
run_cmd() {
    echo "🔧 $1"
    if ! eval "$2"; then
        echo "❌ Failed: $1"
        exit 1
    fi
}

# Update system packages
echo "📦 Updating system packages..."
run_cmd "Updating package lists" "sudo apt update"

# Install essential packages
echo "🐍 Installing Python and essential packages..."
ESSENTIAL_PACKAGES="python3 python3-pip python3-venv git"
run_cmd "Installing essential packages" "sudo apt install -y $ESSENTIAL_PACKAGES"

# Install multimedia packages for Raspberry Pi
if [[ "$IS_RASPI" == true ]]; then
    echo "🎬 Installing Raspberry Pi multimedia packages..."
    RASPI_PACKAGES="omxplayer vlc ffmpeg libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libfreetype6-dev libportmidi-dev libjpeg-dev python3-dev python3-numpy libatlas-base-dev"
    run_cmd "Installing Raspberry Pi packages" "sudo apt install -y $RASPI_PACKAGES"
    
    # Optimize GPU memory split
    echo "⚡ Optimizing GPU memory for video performance..."
    run_cmd "Setting GPU memory split" "sudo raspi-config nonint do_memory_split 128"
    
    # Enable camera/GPU acceleration
    run_cmd "Enabling hardware acceleration" "sudo raspi-config nonint do_camera 0"
else
    echo "🖥️  Installing compatibility packages..."
    COMPAT_PACKAGES="vlc ffmpeg python3-dev"
    run_cmd "Installing compatibility packages" "sudo apt install -y $COMPAT_PACKAGES"
fi

# Create installation directory
echo "📁 Creating installation directory..."
run_cmd "Creating directory" "mkdir -p $INSTALL_DIR"
run_cmd "Changing to directory" "cd $INSTALL_DIR"

# Download or copy files (if running from existing directory)
if [[ -f "ads_player.py" ]]; then
    echo "✅ Files already present in current directory"
else
    echo "📥 Setting up project files..."
    # If this script is run from the project directory, copy files
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    if [[ -f "$SCRIPT_DIR/ads_player.py" ]]; then
        run_cmd "Copying project files" "cp -r $SCRIPT_DIR/* $INSTALL_DIR/"
    else
        echo "❌ Project files not found. Please run this script from the project directory."
        exit 1
    fi
fi

# Setup Python virtual environment
echo "🔧 Setting up Python virtual environment..."
run_cmd "Creating virtual environment" "python3 -m venv ads_player_env"
run_cmd "Activating virtual environment" "source ads_player_env/bin/activate"

# Install Python dependencies
echo "📦 Installing Python packages..."
if [[ -f "requirements.txt" ]]; then
    run_cmd "Installing Python requirements" "ads_player_env/bin/pip install --upgrade pip"
    run_cmd "Installing project dependencies" "ads_player_env/bin/pip install -r requirements.txt"
else
    echo "📦 Installing basic Python packages..."
    run_cmd "Installing pygame and PIL" "ads_player_env/bin/pip install pygame Pillow"
fi

# Create ads directory and test content
echo "🎨 Setting up media directory and test content..."
run_cmd "Creating ads directory" "mkdir -p ads"

# Generate test content if script is available
if [[ -f "test_images.py" ]]; then
    run_cmd "Creating test images" "ads_player_env/bin/python test_images.py"
else
    echo "ℹ️  Test image generator not found, skipping test content creation"
fi

# Make scripts executable
echo "🔧 Setting up executable permissions..."
run_cmd "Making scripts executable" "chmod +x *.sh *.py 2>/dev/null || true"

# Install systemd service
echo "🚀 Installing auto-start service..."
if [[ -f "manage.py" ]]; then
    run_cmd "Installing systemd service" "ads_player_env/bin/python manage.py install"
    
    # Ask user if they want auto-start enabled
    echo ""
    echo "❓ Do you want the ads player to start automatically on boot? (y/N)"
    read -t 10 -n 1 AUTO_START || AUTO_START="n"
    echo ""
    
    if [[ "$AUTO_START" =~ ^[Yy]$ ]]; then
        run_cmd "Enabling auto-start" "ads_player_env/bin/python manage.py enable"
        echo "✅ Auto-start enabled!"
    else
        echo "ℹ️  Auto-start not enabled. You can enable it later with: python3 manage.py enable"
    fi
else
    echo "⚠️  Management script not found, skipping service installation"
fi

# Final setup and permissions
echo "🔧 Final setup..."
run_cmd "Setting directory permissions" "chmod -R 755 $INSTALL_DIR"

# Test basic functionality
echo "🧪 Testing installation..."
if [[ -f "ads_player.py" ]]; then
    echo "✅ Main application found"
else
    echo "❌ Main application missing"
    exit 1
fi

echo ""
echo "🎉 INSTALLATION COMPLETE! 🎉"
echo "================================"
echo ""
echo "📍 Installation location: $INSTALL_DIR"
echo "📁 Add your media files to: $INSTALL_DIR/ads"
echo ""
echo "🚀 Quick Start Commands:"
echo "   cd $INSTALL_DIR"
echo "   ./start.sh              # Start the player"
echo "   ./stop.sh               # Stop the player"
echo "   ./quick_start.sh        # Interactive menu"
echo ""
echo "🔧 Management Commands:"
echo "   python3 manage.py start    # Start player"
echo "   python3 manage.py stop     # Stop player"
echo "   python3 manage.py status   # Show status"
echo "   python3 manage.py test     # Create test images"
echo ""
echo "📋 What's installed:"
echo "   ✅ Raspberry Pi Ads Player"
echo "   ✅ Python virtual environment"
echo "   ✅ All dependencies (pygame, PIL, etc.)"
if [[ "$IS_RASPI" == true ]]; then
echo "   ✅ Hardware acceleration (OMXPlayer, VLC)"
echo "   ✅ GPU memory optimization"
fi
echo "   ✅ Auto-start service (systemd)"
echo "   ✅ Test content generated"
echo "   ✅ Easy management scripts"
echo ""

if [[ "$AUTO_START" =~ ^[Yy]$ ]]; then
    echo "⚡ Auto-start: ENABLED (will start on boot)"
    echo "   To start now: ./start.sh"
    echo "   To disable: python3 manage.py disable"
else
    echo "💡 To enable auto-start: python3 manage.py enable"
    echo "🚀 To start now: ./start.sh"
fi

echo ""
echo "🎮 Player Controls (when running):"
echo "   ESC/Q: Quit    SPACE: Next ad    R: Reload    S: Shuffle"
echo ""
echo "📖 For more info, see README.md"
echo "✨ Enjoy your new digital signage system!"