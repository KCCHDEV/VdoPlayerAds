#!/usr/bin/env python3
"""
Generate sample test images for the Raspberry Pi Ads Player
Creates images optimized for both 16:9 and 6:19 screen orientations
"""

import os
from PIL import Image, ImageDraw, ImageFont
import random

def create_test_image(width, height, text, filename, orientation):
    """Create a test image with specified dimensions and text"""
    
    # Create image with random background color
    bg_colors = [
        (255, 100, 100),  # Red
        (100, 255, 100),  # Green
        (100, 100, 255),  # Blue
        (255, 255, 100),  # Yellow
        (255, 100, 255),  # Magenta
        (100, 255, 255),  # Cyan
        (200, 150, 100),  # Brown
        (150, 100, 200),  # Purple
    ]
    
    bg_color = random.choice(bg_colors)
    image = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(image)
    
    # Try to load a font, fall back to default if not available
    try:
        font_size = min(width, height) // 20
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
    except:
        try:
            font_size = min(width, height) // 30
            font = ImageFont.load_default()
        except:
            font = None
    
    # Add orientation indicator
    orientation_text = f"Sample Ad - {orientation} Format"
    text_lines = [orientation_text, text, f"{width}x{height}"]
    
    # Calculate text positioning
    y_offset = height // 4
    for i, line in enumerate(text_lines):
        if font:
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
        else:
            text_width = len(line) * 10
            text_height = 20
        
        x = (width - text_width) // 2
        y = y_offset + (i * (text_height + 20))
        
        # Draw text with shadow
        shadow_offset = 3
        draw.text((x + shadow_offset, y + shadow_offset), line, fill=(0, 0, 0), font=font)
        draw.text((x, y), line, fill=(255, 255, 255), font=font)
    
    # Add some decorative elements
    # Corner triangles
    triangle_size = min(width, height) // 10
    draw.polygon([(0, 0), (triangle_size, 0), (0, triangle_size)], fill=(255, 255, 255, 128))
    draw.polygon([(width, height), (width-triangle_size, height), (width, height-triangle_size)], fill=(255, 255, 255, 128))
    
    # Save the image
    filepath = os.path.join("ads", filename)
    image.save(filepath, "PNG")
    print(f"Created: {filepath}")

def main():
    """Generate test images for both orientations"""
    print("🎨 Generating test images for Raspberry Pi Ads Player...")
    
    # Ensure ads directory exists
    os.makedirs("ads", exist_ok=True)
    
    # 16:9 landscape images
    landscape_resolutions = [
        (1920, 1080),
        (1366, 768),
        (1280, 720),
    ]
    
    for i, (width, height) in enumerate(landscape_resolutions):
        create_test_image(
            width, height, 
            f"Landscape Ad #{i+1}\nGreat for horizontal displays!",
            f"landscape_{width}x{height}_ad{i+1}.png",
            "16:9"
        )
    
    # 6:19 portrait images
    portrait_resolutions = [
        (1080, 1920),
        (768, 1366),
        (720, 1280),
    ]
    
    for i, (width, height) in enumerate(portrait_resolutions):
        create_test_image(
            width, height,
            f"Portrait Ad #{i+1}\nPerfect for vertical displays!",
            f"portrait_{width}x{height}_ad{i+1}.png",
            "6:19"
        )
    
    # Create some generic ads
    generic_ads = [
        "Welcome to Digital Signage!",
        "Your Ad Could Be Here",
        "Raspberry Pi Powered",
        "Professional Display Solution",
        "Auto-Scaling Content"
    ]
    
    for i, text in enumerate(generic_ads):
        # Create both orientations for generic ads
        create_test_image(1920, 1080, text, f"generic_16_9_ad{i+1}.png", "16:9")
        create_test_image(1080, 1920, text, f"generic_6_19_ad{i+1}.png", "6:19")
    
    print("✅ Test image generation complete!")
    print(f"📁 Images saved to: {os.path.abspath('ads')}")
    print("🚀 You can now test the ads player with these sample images:")
    print("   python3 ads_player.py")

if __name__ == "__main__":
    main()