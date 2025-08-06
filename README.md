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

## Quick Installation

1. **Clone or download** this repository to your Raspberry Pi
2. **Run the installation script**:
   ```bash
   chmod +x install_raspi.sh
   ./install_raspi.sh
   ```
3. **Add your media files** to the `ads` directory
4. **Test the player**:
   ```bash
   python3 ads_player.py
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

## Usage

### Running the Player

```bash
# Direct execution
python3 ads_player.py

# Or with virtual environment
source ads_player_env/bin/activate
python ads_player.py
```

### Keyboard Controls

- **ESC or Q**: Quit the player
- **SPACE**: Skip to next ad
- **R**: Reload ads from directory
- **S**: Shuffle current ads

### Auto-start on Boot

Enable the systemd service:

```bash
sudo systemctl enable ads_player.service
sudo systemctl start ads_player.service
```

Monitor the service:

```bash
# Check status
sudo systemctl status ads_player.service

# View logs
sudo journalctl -u ads_player.service -f

# Stop service
sudo systemctl stop ads_player.service
```

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
├── config.json           # Configuration file
├── requirements.txt      # Python dependencies
├── install_raspi.sh      # Installation script
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
