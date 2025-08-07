#!/bin/bash
# Simple Setup Script - Run from project directory
# One command to setup everything: ./setup.sh

echo "🎬 Raspberry Pi Ads Player - Simple Setup"
echo "========================================="

# Run the auto install script from current directory
if [[ -f "auto_install.sh" ]]; then
    chmod +x auto_install.sh
    ./auto_install.sh
else
    echo "❌ auto_install.sh not found in current directory"
    echo "Please run this from the project root directory"
    exit 1
fi