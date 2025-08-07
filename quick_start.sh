#!/bin/bash
# Quick Start Script for Raspberry Pi Ads Player
# One-command setup and start

echo "🎬 Raspberry Pi Ads Player - Quick Start"
echo "=========================================="

# Check if we're on Raspberry Pi
if [[ -f /proc/device-tree/model ]] && grep -q "Raspberry Pi" /proc/device-tree/model; then
    echo "✅ Raspberry Pi detected"
else
    echo "⚠️  Warning: Not detected as Raspberry Pi, some features may not work optimally"
fi

# Function to show menu
show_menu() {
    echo ""
    echo "📋 Quick Actions:"
    echo "1) 🚀 Start Ads Player"
    echo "2) 🛑 Stop Ads Player"
    echo "3) 🔄 Restart Ads Player"
    echo "4) 📊 Show Status"
    echo "5) ⚡ Enable Auto-Start on Boot"
    echo "6) 🚫 Disable Auto-Start"
    echo "7) 🎨 Create Test Images"
    echo "8) 📁 List Media Files"
    echo "9) 📋 View Logs"
    echo "10) 🔧 Full Installation"
    echo "0) 🚪 Exit"
    echo ""
    read -p "Choose an option (0-10): " choice
}

# Function to wait for user
wait_user() {
    echo ""
    read -p "Press Enter to continue..."
}

# Main menu loop
while true; do
    show_menu
    
    case $choice in
        1)
            echo "🚀 Starting Ads Player..."
            python3 manage.py start
            wait_user
            ;;
        2)
            echo "🛑 Stopping Ads Player..."
            python3 manage.py stop
            wait_user
            ;;
        3)
            echo "🔄 Restarting Ads Player..."
            python3 manage.py restart
            wait_user
            ;;
        4)
            echo "📊 Checking Status..."
            python3 manage.py status
            wait_user
            ;;
        5)
            echo "⚡ Enabling Auto-Start..."
            python3 manage.py install
            python3 manage.py enable
            wait_user
            ;;
        6)
            echo "🚫 Disabling Auto-Start..."
            python3 manage.py disable
            wait_user
            ;;
        7)
            echo "🎨 Creating Test Images..."
            python3 manage.py test
            wait_user
            ;;
        8)
            echo "📁 Listing Media Files..."
            python3 manage.py list
            wait_user
            ;;
        9)
            echo "📋 Showing Recent Logs..."
            python3 manage.py logs
            wait_user
            ;;
        10)
            echo "🔧 Running Full Installation..."
            if [[ -f "install_raspi.sh" ]]; then
                chmod +x install_raspi.sh
                ./install_raspi.sh
            else
                echo "❌ install_raspi.sh not found"
            fi
            wait_user
            ;;
        0)
            echo "👋 Goodbye!"
            exit 0
            ;;
        *)
            echo "❌ Invalid option. Please choose 0-10."
            sleep 1
            ;;
    esac
done