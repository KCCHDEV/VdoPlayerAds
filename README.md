# Raspberry Pi Ads Player

A professional digital signage solution optimized for Raspberry Pi, supporting both **16:9 landscape** and **6:19 portrait** screen orientations. Perfect for displaying advertisements, announcements, or any rotating media content.

## Features

- ✅ **Dual Orientation Support**: Automatically detects and adapts to 16:9 (landscape) and 6:19 (portrait) screens
- ✅ **Hardware Accelerated**: Optimized for Raspberry Pi GPU with OMXPlayer and VLC support
- ✅ **Multiple Media Formats**: Images (JPG, PNG, BMP) and Videos (MP4, AVI, MOV, MKV)
- ✅ **Auto-scaling**: Maintains aspect ratios while fitting content to screen
- ✅ **Configurable**: JSON-based configuration for easy customization
- ✅ **Auto-start**: Systemd service for automatic startup on boot
- ✅ **Remote Control**: Keyboard shortcuts for manual control
- ✅ **Logging**: Comprehensive logging for monitoring and debugging

## Hardware Requirements

- **Raspberry Pi 3B+ or newer** (Raspberry Pi 4 recommended)
- **16GB+ microSD card** (Class 10 or better)
- **HDMI display** in either:
  - 16:9 aspect ratio (1920x1080, 1366x768, etc.)
  - 6:19 aspect ratio (1080x1920, etc.)
- **Power supply** appropriate for your Pi model

## Super Easy Setup

**Option 1: Auto Install (Recommended)**
```bash
./auto_install.sh
```
One command installs everything automatically!

**Option 2: Simple Setup**
```bash
./setup.sh
```
Alternative auto-installer from project directory.

**Option 3: Interactive Menu**
```bash
./quick_start.sh
```
Choose option 10 for full installation, then option 1 to start!

**Option 4: Manual Install**
```bash
./install_raspi.sh && ./start.sh
```

## Manual Installation

If you prefer manual installation:

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3 python3-pip omxplayer vlc ffmpeg

# Install Python packages
pip3 install pygame Pillow requests opencv-python numpy

# Clone and setup
git clone <repository-url>
cd ads_player
mkdir ads
```

## Configuration

Edit `config.json` to customize the player:

```json
{
    "ads_directory": "ads",
    "display_duration": 10,
    "force_orientation": null,
    "fullscreen": true,
    "shuffle_ads": false,
    "hardware_acceleration": true
}
```

### Key Configuration Options

- `ads_directory`: Directory containing your media files
- `display_duration`: Seconds to display each ad
- `force_orientation`: Set to "16:9" or "6:19" to override auto-detection
- `fullscreen`: Run in fullscreen mode
- `shuffle_ads`: Randomize ad order
- `hardware_acceleration`: Use GPU acceleration (recommended)

## Adding Media Content

1. Copy your images and videos to the `ads` directory:
   ```bash
   cp /path/to/your/media/* ads/
   ```

2. Supported formats:
   - **Images**: .jpg, .jpeg, .png, .bmp
   - **Videos**: .mp4, .avi, .mov, .mkv, .wmv

3. The player will automatically detect and load new files when restarted or when pressing 'R'

## Easy Management

### Simple Commands

```bash
# Start the ads player
./start.sh

# Stop the ads player
./stop.sh

# Interactive menu with all options
./quick_start.sh

# Advanced management
python3 manage.py start      # Start player
python3 manage.py stop       # Stop player
python3 manage.py restart    # Restart player
python3 manage.py status     # Show status
python3 manage.py enable     # Enable auto-start on boot
python3 manage.py disable    # Disable auto-start
python3 manage.py test       # Create test images
python3 manage.py list       # List media files
python3 manage.py logs       # View logs
```

### Adding Your Media

```bash
# Copy files to ads directory
cp /path/to/your/images/* ads/

# Or use the manager
python3 manage.py add --file /path/to/your/video.mp4

# Create test content
python3 manage.py test
```

### Keyboard Controls (when running)

- **ESC or Q**: Quit the player
- **SPACE**: Skip to next ad
- **R**: Reload ads from directory
- **S**: Shuffle current ads

## Screen Orientation Setup

### 16:9 Landscape Displays
- Default configuration works out of the box
- Supports resolutions: 1920x1080, 1366x768, 1280x720, etc.

### 6:19 Portrait Displays
- Automatically detected when height > width
- Common with rotated monitors or specialized portrait displays
- May require display rotation in `/boot/config.txt`:
  ```
  display_rotate=1  # 90 degrees
  # or
  display_rotate=3  # 270 degrees
  ```

## Troubleshooting

### Video Playback Issues
- Ensure OMXPlayer is installed: `sudo apt install omxplayer`
- Check GPU memory split: `sudo raspi-config` → Advanced → Memory Split → 128
- For newer Pi models, consider using VLC as primary player

### Display Issues
- Check HDMI connection and cable
- Verify display resolution: `tvservice -s`
- Test with different resolutions in config

### Performance Issues
- Increase GPU memory split to 256MB
- Use hardware-accelerated video formats (H.264)
- Reduce image resolution for faster loading

### Permission Issues
```bash
# Fix file permissions
chmod +x ads_player.py
chmod +x install_raspi.sh

# Fix directory permissions
chmod -R 755 ads/
```

## Advanced Configuration

### Custom Resolution Override
```json
{
    "force_orientation": "16:9",
    "custom_resolution": [1920, 1080]
}
```

### Video Player Priority
```json
{
    "raspberry_pi": {
        "enable_omxplayer": true,
        "enable_vlc_fallback": true
    }
}
```

### Scheduling and Timing
```json
{
    "orientation_specific": {
        "16:9": {"display_duration": 10},
        "6:19": {"display_duration": 8}
    }
}
```

## File Structure

```
ads_player/
├── ads_player.py          # Main application
├── video_player.py        # Video playback module
├── manage.py             # Easy management script
├── config.json           # Configuration file
├── requirements.txt      # Python dependencies
├── auto_install.sh       # Automatic installer (recommended)
├── setup.sh              # Simple setup script
├── install_raspi.sh      # Manual installation script
├── quick_start.sh        # Interactive menu
├── start.sh              # Simple start script
├── stop.sh               # Simple stop script
├── test_images.py        # Test content generator
├── ads/                  # Media directory
├── ads_player.log        # Application logs
└── README.md            # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test on actual Raspberry Pi hardware
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs: `tail -f ads_player.log`
3. Test with minimal configuration
4. Create an issue with system details and logs

---

**Made for Raspberry Pi enthusiasts and digital signage professionals** 🥧📺
