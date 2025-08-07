#!/usr/bin/env python3
"""
Video Player Module for Raspberry Pi Ads Player
Optimized for hardware acceleration on Raspberry Pi
"""

import pygame
import subprocess
import threading
import time
import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class VideoPlayer:
    def __init__(self, screen, screen_width, screen_height):
        """Initialize video player with screen reference"""
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.is_playing = False
        self.current_process = None
        
    def get_video_info(self, video_path):
        """Get video information using ffprobe"""
        try:
            cmd = [
                'ffprobe', '-v', 'quiet', '-print_format', 'json',
                '-show_format', '-show_streams', video_path
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                import json
                info = json.loads(result.stdout)
                return info
        except Exception as e:
            logger.error(f"Error getting video info: {e}")
        return None
    
    def play_video_omxplayer(self, video_path, duration=None):
        """Play video using omxplayer (Raspberry Pi optimized)"""
        try:
            # OMXPlayer command for Raspberry Pi hardware acceleration
            cmd = [
                'omxplayer',
                '--no-osd',           # No on-screen display
                '--no-keys',          # Disable keyboard input
                '--aspect-mode', 'letterbox',  # Maintain aspect ratio
                '--vol', '0',         # Mute audio for ads
                video_path
            ]
            
            # Add timeout if duration specified
            if duration:
                cmd.extend(['--timeout', str(duration)])
            
            logger.info(f"Starting OMXPlayer for: {os.path.basename(video_path)}")
            self.current_process = subprocess.Popen(cmd)
            self.is_playing = True
            
            # Wait for video to finish or timeout
            self.current_process.wait()
            self.is_playing = False
            
        except FileNotFoundError:
            logger.warning("OMXPlayer not found, falling back to alternative method")
            self.play_video_pygame(video_path, duration)
        except Exception as e:
            logger.error(f"Error playing video with OMXPlayer: {e}")
            self.is_playing = False
    
    def play_video_vlc(self, video_path, duration=None):
        """Play video using VLC (alternative method)"""
        try:
            cmd = [
                'cvlc',               # Command-line VLC
                '--intf', 'dummy',    # No interface
                '--no-audio',         # No audio for ads
                '--fullscreen',       # Fullscreen mode
                '--play-and-exit',    # Exit after playing
                video_path
            ]
            
            logger.info(f"Starting VLC for: {os.path.basename(video_path)}")
            self.current_process = subprocess.Popen(cmd)
            self.is_playing = True
            
            if duration:
                # Kill process after duration
                time.sleep(duration)
                self.stop_video()
            else:
                self.current_process.wait()
            
            self.is_playing = False
            
        except FileNotFoundError:
            logger.warning("VLC not found, falling back to pygame")
            self.play_video_pygame(video_path, duration)
        except Exception as e:
            logger.error(f"Error playing video with VLC: {e}")
            self.is_playing = False
    
    def play_video_pygame(self, video_path, duration=None):
        """Fallback video player using pygame (basic functionality)"""
        try:
            # For pygame, we'll show a video placeholder
            # Real video playback would require pygame_gui or similar
            logger.info(f"Pygame video placeholder for: {os.path.basename(video_path)}")
            
            self.is_playing = True
            start_time = time.time()
            
            # Create a simple animated placeholder
            font = pygame.font.Font(None, 48)
            
            while self.is_playing:
                current_time = time.time()
                elapsed = current_time - start_time
                
                if duration and elapsed >= duration:
                    break
                
                # Animated background
                color_intensity = int(128 + 127 * abs(time.time() % 2 - 1))
                self.screen.fill((color_intensity // 4, color_intensity // 6, color_intensity // 8))
                
                # Display video info
                filename = os.path.basename(video_path)
                text1 = font.render(f"VIDEO: {filename}", True, (255, 255, 255))
                text2 = font.render(f"Time: {elapsed:.1f}s", True, (200, 200, 200))
                
                text1_rect = text1.get_rect(center=(self.screen_width//2, self.screen_height//2 - 30))
                text2_rect = text2.get_rect(center=(self.screen_width//2, self.screen_height//2 + 30))
                
                self.screen.blit(text1, text1_rect)
                self.screen.blit(text2, text2_rect)
                pygame.display.flip()
                
                # Handle events
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.is_playing = False
                
                time.sleep(0.1)  # Small delay
            
            self.is_playing = False
            
        except Exception as e:
            logger.error(f"Error in pygame video player: {e}")
            self.is_playing = False
    
    def play_video(self, video_path, duration=None):
        """Main video playback method - tries different players"""
        if not os.path.exists(video_path):
            logger.error(f"Video file not found: {video_path}")
            return
        
        # Try different video players in order of preference for Raspberry Pi
        try:
            # First try OMXPlayer (best for Raspberry Pi)
            self.play_video_omxplayer(video_path, duration)
        except:
            try:
                # Then try VLC
                self.play_video_vlc(video_path, duration)
            except:
                # Finally fall back to pygame
                self.play_video_pygame(video_path, duration)
    
    def stop_video(self):
        """Stop current video playback"""
        self.is_playing = False
        if self.current_process and self.current_process.poll() is None:
            try:
                self.current_process.terminate()
                self.current_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.current_process.kill()
            except Exception as e:
                logger.error(f"Error stopping video: {e}")
        self.current_process = None
    
    def is_video_playing(self):
        """Check if video is currently playing"""
        return self.is_playing