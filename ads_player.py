#!/usr/bin/env python3
"""
Raspberry Pi Ads Player
Supports both 16:9 and 6:19 screen orientations
Optimized for Raspberry Pi hardware
"""

import pygame
import os
import sys
import json
import time
import random
import threading
from pathlib import Path
from typing import List, Tuple, Optional
import subprocess
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ads_player.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AdsPlayer:
    def __init__(self, config_file: str = "config.json"):
        """Initialize the ads player with configuration"""
        self.config = self.load_config(config_file)
        self.screen = None
        self.clock = None
        self.running = False
        self.current_ad_index = 0
        self.ads_list = []
        self.screen_width = 0
        self.screen_height = 0
        self.orientation = "16:9"  # Default orientation
        
        # Initialize pygame
        pygame.init()
        pygame.mixer.init()
        
        # Detect screen resolution and orientation
        self.detect_screen_orientation()
        
        # Load ads content
        self.load_ads_content()
        
    def load_config(self, config_file: str) -> dict:
        """Load configuration from JSON file"""
        default_config = {
            "ads_directory": "ads",
            "display_duration": 10,  # seconds per ad
            "transition_effect": "fade",
            "autodetect_orientation": True,
            "force_orientation": None,  # "16:9" or "6:19"
            "fullscreen": True,
            "background_color": [0, 0, 0],
            "supported_formats": [".jpg", ".jpeg", ".png", ".bmp", ".mp4", ".avi", ".mov"],
            "hardware_acceleration": True,
            "fps": 30,
            "volume": 0.7,
            "loop_ads": True,
            "shuffle_ads": False
        }
        
        try:
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    config = json.load(f)
                # Merge with defaults
                for key, value in default_config.items():
                    if key not in config:
                        config[key] = value
                return config
            else:
                # Create default config file
                with open(config_file, 'w') as f:
                    json.dump(default_config, f, indent=4)
                logger.info(f"Created default config file: {config_file}")
                return default_config
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return default_config
    
    def detect_screen_orientation(self):
        """Detect screen resolution and determine orientation"""
        try:
            # Try to get display info
            if self.config.get("force_orientation"):
                self.orientation = self.config["force_orientation"]
                if self.orientation == "16:9":
                    self.screen_width, self.screen_height = 1920, 1080
                else:  # 6:19
                    self.screen_width, self.screen_height = 1080, 1920
            else:
                # Auto-detect screen resolution
                info = pygame.display.Info()
                self.screen_width = info.current_w
                self.screen_height = info.current_h
                
                # Determine orientation based on aspect ratio
                aspect_ratio = self.screen_width / self.screen_height
                if aspect_ratio > 1:  # Landscape
                    self.orientation = "16:9"
                else:  # Portrait
                    self.orientation = "6:19"
            
            logger.info(f"Screen resolution: {self.screen_width}x{self.screen_height}")
            logger.info(f"Detected orientation: {self.orientation}")
            
        except Exception as e:
            logger.error(f"Error detecting screen: {e}")
            # Fallback to default
            self.screen_width, self.screen_height = 1920, 1080
            self.orientation = "16:9"
    
    def setup_display(self):
        """Setup pygame display"""
        try:
            if self.config["fullscreen"]:
                self.screen = pygame.display.set_mode(
                    (self.screen_width, self.screen_height), 
                    pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
                )
            else:
                self.screen = pygame.display.set_mode(
                    (self.screen_width, self.screen_height)
                )
            
            pygame.display.set_caption("Raspberry Pi Ads Player")
            self.clock = pygame.time.Clock()
            
            # Hide cursor in fullscreen mode
            if self.config["fullscreen"]:
                pygame.mouse.set_visible(False)
                
            logger.info("Display setup complete")
            
        except Exception as e:
            logger.error(f"Error setting up display: {e}")
            sys.exit(1)
    
    def load_ads_content(self):
        """Load all ads content from the ads directory"""
        ads_dir = Path(self.config["ads_directory"])
        
        if not ads_dir.exists():
            ads_dir.mkdir(parents=True, exist_ok=True)
            logger.warning(f"Created ads directory: {ads_dir}")
            return
        
        supported_formats = self.config["supported_formats"]
        self.ads_list = []
        
        for file_path in ads_dir.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in supported_formats:
                self.ads_list.append(str(file_path))
        
        if self.config["shuffle_ads"]:
            random.shuffle(self.ads_list)
        
        logger.info(f"Loaded {len(self.ads_list)} ads from {ads_dir}")
        
        if not self.ads_list:
            logger.warning("No ads found! Please add media files to the ads directory.")
    
    def scale_image_to_fit(self, image: pygame.Surface) -> pygame.Surface:
        """Scale image to fit screen while maintaining aspect ratio"""
        img_width, img_height = image.get_size()
        screen_ratio = self.screen_width / self.screen_height
        img_ratio = img_width / img_height
        
        if img_ratio > screen_ratio:
            # Image is wider, scale by width
            new_width = self.screen_width
            new_height = int(self.screen_width / img_ratio)
        else:
            # Image is taller, scale by height
            new_height = self.screen_height
            new_width = int(self.screen_height * img_ratio)
        
        return pygame.transform.scale(image, (new_width, new_height))
    
    def display_image(self, image_path: str):
        """Display an image ad"""
        try:
            image = pygame.image.load(image_path)
            scaled_image = self.scale_image_to_fit(image)
            
            # Center the image on screen
            x = (self.screen_width - scaled_image.get_width()) // 2
            y = (self.screen_height - scaled_image.get_height()) // 2
            
            # Fill background
            self.screen.fill(self.config["background_color"])
            self.screen.blit(scaled_image, (x, y))
            pygame.display.flip()
            
            logger.info(f"Displaying image: {os.path.basename(image_path)}")
            
        except Exception as e:
            logger.error(f"Error displaying image {image_path}: {e}")
    
    def display_video(self, video_path: str):
        """Display a video ad using the video player module"""
        try:
            from video_player import VideoPlayer
            
            if not hasattr(self, 'video_player'):
                self.video_player = VideoPlayer(self.screen, self.screen_width, self.screen_height)
            
            # Play video for the configured duration
            duration = self.config["display_duration"]
            self.video_player.play_video(video_path, duration)
            
        except ImportError:
            logger.error("Video player module not available")
            # Fallback to placeholder
            self.screen.fill(self.config["background_color"])
            font = pygame.font.Font(None, 74)
            text = font.render(f"VIDEO: {os.path.basename(video_path)}", True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.screen_width//2, self.screen_height//2))
            self.screen.blit(text, text_rect)
            pygame.display.flip()
        except Exception as e:
            logger.error(f"Error playing video {video_path}: {e}")
    
    def is_video_file(self, file_path: str) -> bool:
        """Check if file is a video"""
        video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv']
        return Path(file_path).suffix.lower() in video_extensions
    
    def display_current_ad(self):
        """Display the current ad"""
        if not self.ads_list:
            # No ads available, show message
            self.screen.fill(self.config["background_color"])
            font = pygame.font.Font(None, 74)
            text = font.render("No Ads Available", True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.screen_width//2, self.screen_height//2))
            self.screen.blit(text, text_rect)
            pygame.display.flip()
            return
        
        current_ad = self.ads_list[self.current_ad_index]
        
        if self.is_video_file(current_ad):
            self.display_video(current_ad)
        else:
            self.display_image(current_ad)
    
    def next_ad(self):
        """Move to the next ad"""
        if self.ads_list:
            self.current_ad_index = (self.current_ad_index + 1) % len(self.ads_list)
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    self.next_ad()
                elif event.key == pygame.K_r:
                    # Reload ads
                    self.load_ads_content()
                elif event.key == pygame.K_s:
                    # Shuffle ads
                    if self.ads_list:
                        random.shuffle(self.ads_list)
                        self.current_ad_index = 0
    
    def run(self):
        """Main game loop"""
        self.setup_display()
        self.running = True
        
        last_ad_change = time.time()
        display_duration = self.config["display_duration"]
        
        logger.info("Starting ads player...")
        logger.info(f"Controls: ESC/Q=Quit, SPACE=Next Ad, R=Reload, S=Shuffle")
        
        while self.running:
            current_time = time.time()
            
            self.handle_events()
            
            # Check if it's time to change ads
            if current_time - last_ad_change >= display_duration:
                self.next_ad()
                last_ad_change = current_time
            
            # Display current ad
            self.display_current_ad()
            
            # Control frame rate
            self.clock.tick(self.config["fps"])
        
        logger.info("Ads player stopped")
        pygame.quit()

def main():
    """Main entry point"""
    try:
        player = AdsPlayer()
        player.run()
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()