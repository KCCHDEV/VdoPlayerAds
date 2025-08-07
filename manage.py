#!/usr/bin/env python3
"""
Easy Management Script for Raspberry Pi Ads Player
Provides simple commands to start, stop, status, and manage the ads player
"""

import os
import sys
import subprocess
import time
import argparse
import json
from pathlib import Path

class AdsPlayerManager:
    def __init__(self):
        self.service_name = "ads_player.service"
        self.script_dir = Path(__file__).parent
        self.ads_dir = self.script_dir / "ads"
        self.config_file = self.script_dir / "config.json"
        
    def run_command(self, cmd, capture_output=True):
        """Run a system command safely"""
        try:
            if capture_output:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                return result.returncode == 0, result.stdout, result.stderr
            else:
                result = subprocess.run(cmd, shell=True)
                return result.returncode == 0, "", ""
        except Exception as e:
            return False, "", str(e)

    def start(self):
        """Start the ads player"""
        print("🚀 Starting Ads Player...")
        
        # Check if running as service first
        success, stdout, stderr = self.run_command(f"systemctl is-active {self.service_name}")
        if "active" in stdout:
            print("✅ Ads Player service is already running!")
            return True
        
        # Try to start as service
        success, _, _ = self.run_command(f"sudo systemctl start {self.service_name}")
        if success:
            print("✅ Ads Player service started successfully!")
            time.sleep(2)
            self.status()
            return True
        
        # Fall back to direct execution
        print("📱 Starting in direct mode (service not available)...")
        success, _, _ = self.run_command(f"cd {self.script_dir} && python3 ads_player.py", capture_output=False)
        return success

    def stop(self):
        """Stop the ads player"""
        print("🛑 Stopping Ads Player...")
        
        # Stop service
        success, _, _ = self.run_command(f"sudo systemctl stop {self.service_name}")
        if success:
            print("✅ Ads Player service stopped!")
        
        # Also kill any direct processes
        self.run_command("pkill -f ads_player.py")
        self.run_command("pkill -f omxplayer")
        self.run_command("pkill -f vlc")
        
        print("✅ All ads player processes stopped!")
        return True

    def restart(self):
        """Restart the ads player"""
        print("🔄 Restarting Ads Player...")
        self.stop()
        time.sleep(2)
        return self.start()

    def status(self):
        """Show ads player status"""
        print("📊 Ads Player Status:")
        print("=" * 50)
        
        # Service status
        success, stdout, stderr = self.run_command(f"systemctl is-active {self.service_name}")
        service_status = stdout.strip() if success else "inactive"
        print(f"Service Status: {service_status}")
        
        # Process check
        success, stdout, _ = self.run_command("pgrep -f ads_player.py")
        if success and stdout:
            print(f"Process ID: {stdout.strip()}")
        else:
            print("Process ID: Not running")
        
        # Ads count
        if self.ads_dir.exists():
            ads_count = len([f for f in self.ads_dir.iterdir() if f.is_file()])
            print(f"Ads Available: {ads_count}")
        else:
            print("Ads Available: 0 (directory not found)")
        
        # Config check
        if self.config_file.exists():
            print("Config File: ✅ Found")
        else:
            print("Config File: ❌ Missing")
        
        # Recent logs
        print("\n📋 Recent Logs:")
        success, stdout, _ = self.run_command(f"journalctl -u {self.service_name} --no-pager -n 5")
        if success and stdout:
            print(stdout)
        else:
            print("No service logs available")

    def enable_autostart(self):
        """Enable automatic startup on boot"""
        print("⚡ Enabling auto-start on boot...")
        success, _, _ = self.run_command(f"sudo systemctl enable {self.service_name}")
        if success:
            print("✅ Auto-start enabled! Ads Player will start on boot.")
        else:
            print("❌ Failed to enable auto-start. Make sure service is installed.")
        return success

    def disable_autostart(self):
        """Disable automatic startup on boot"""
        print("🚫 Disabling auto-start on boot...")
        success, _, _ = self.run_command(f"sudo systemctl disable {self.service_name}")
        if success:
            print("✅ Auto-start disabled.")
        else:
            print("❌ Failed to disable auto-start.")
        return success

    def install_service(self):
        """Install the systemd service"""
        print("🔧 Installing systemd service...")
        
        service_content = f"""[Unit]
Description=Raspberry Pi Ads Player
After=graphical.target

[Service]
Type=simple
User={os.getenv('USER', 'pi')}
WorkingDirectory={self.script_dir}
Environment=DISPLAY=:0
ExecStart={sys.executable} {self.script_dir}/ads_player.py
Restart=always
RestartSec=5

[Install]
WantedBy=graphical.target
"""
        
        # Write service file
        service_file = f"/tmp/{self.service_name}"
        with open(service_file, 'w') as f:
            f.write(service_content)
        
        # Install service
        success, _, _ = self.run_command(f"sudo cp {service_file} /etc/systemd/system/")
        if success:
            self.run_command("sudo systemctl daemon-reload")
            print("✅ Service installed successfully!")
            return True
        else:
            print("❌ Failed to install service.")
            return False

    def add_media(self, file_path):
        """Add media file to ads directory"""
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            return False
        
        # Create ads directory if it doesn't exist
        self.ads_dir.mkdir(exist_ok=True)
        
        # Copy file
        import shutil
        filename = os.path.basename(file_path)
        dest_path = self.ads_dir / filename
        
        try:
            shutil.copy2(file_path, dest_path)
            print(f"✅ Added media: {filename}")
            return True
        except Exception as e:
            print(f"❌ Failed to add media: {e}")
            return False

    def list_media(self):
        """List all media files"""
        print("📁 Media Files:")
        print("=" * 30)
        
        if not self.ads_dir.exists():
            print("No ads directory found")
            return
        
        files = list(self.ads_dir.iterdir())
        if not files:
            print("No media files found")
            return
        
        for i, file_path in enumerate(files, 1):
            if file_path.is_file():
                size = file_path.stat().st_size
                size_mb = size / (1024 * 1024)
                print(f"{i:2d}. {file_path.name} ({size_mb:.1f} MB)")

    def create_test_media(self):
        """Create test media files"""
        print("🎨 Creating test media files...")
        success, _, _ = self.run_command(f"cd {self.script_dir} && python3 test_images.py")
        if success:
            print("✅ Test media created!")
        else:
            print("❌ Failed to create test media. Make sure test_images.py exists.")
        return success

    def logs(self, lines=20):
        """Show recent logs"""
        print(f"📋 Recent Logs (last {lines} lines):")
        print("=" * 50)
        
        # Service logs
        success, stdout, _ = self.run_command(f"journalctl -u {self.service_name} --no-pager -n {lines}")
        if success and stdout:
            print(stdout)
        else:
            # Try log file
            log_file = self.script_dir / "ads_player.log"
            if log_file.exists():
                success, stdout, _ = self.run_command(f"tail -n {lines} {log_file}")
                if success:
                    print(stdout)
            else:
                print("No logs available")

def main():
    manager = AdsPlayerManager()
    
    parser = argparse.ArgumentParser(description="Easy Ads Player Manager")
    parser.add_argument('command', choices=[
        'start', 'stop', 'restart', 'status', 'enable', 'disable', 
        'install', 'add', 'list', 'test', 'logs'
    ], help='Command to execute')
    parser.add_argument('--file', help='File path for add command')
    parser.add_argument('--lines', type=int, default=20, help='Number of log lines to show')
    
    args = parser.parse_args()
    
    print(f"🎬 Raspberry Pi Ads Player Manager")
    print("=" * 40)
    
    if args.command == 'start':
        manager.start()
    elif args.command == 'stop':
        manager.stop()
    elif args.command == 'restart':
        manager.restart()
    elif args.command == 'status':
        manager.status()
    elif args.command == 'enable':
        manager.enable_autostart()
    elif args.command == 'disable':
        manager.disable_autostart()
    elif args.command == 'install':
        manager.install_service()
    elif args.command == 'add':
        if args.file:
            manager.add_media(args.file)
        else:
            print("❌ Please specify --file path")
    elif args.command == 'list':
        manager.list_media()
    elif args.command == 'test':
        manager.create_test_media()
    elif args.command == 'logs':
        manager.logs(args.lines)

if __name__ == "__main__":
    main()