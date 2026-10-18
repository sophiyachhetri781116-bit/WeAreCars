#!/usr/bin/env python3
"""
Asset generation script for WeAreCars application.
This creates a basic car icon and logo as placeholder assets.
"""

import os
from PIL import Image, ImageDraw, ImageFont

def create_car_icon(output_path, size=(128, 128)):
    """Create a simple car icon"""
    # Create a new image with transparent background
    img = Image.new('RGBA', size, color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Colors
    primary_color = (0, 77, 153, 255)  # Dark blue
    secondary_color = (255, 140, 0, 255)  # Orange
    
    # Calculate centers and dimensions
    width, height = size
    center_x, center_y = width // 2, height // 2
    
    # Draw car body (rounded rectangle)
    car_width = int(width * 0.8)
    car_height = int(height * 0.3)
    car_top = center_y - int(car_height * 0.5)
    car_left = center_x - int(car_width * 0.5)
    
    # Draw car body
    draw.rounded_rectangle(
        [car_left, car_top, car_left + car_width, car_top + car_height],
        radius=10,
        fill=primary_color
    )
    
    # Draw car roof
    roof_width = int(car_width * 0.6)
    roof_height = int(car_height * 1.3)
    roof_top = car_top - int(roof_height * 0.6)
    roof_left = center_x - int(roof_width * 0.5)
    
    draw.rounded_rectangle(
        [roof_left, roof_top, roof_left + roof_width, car_top],
        radius=8,
        fill=primary_color
    )
    
    # Draw windows
    window_width = int(roof_width * 0.8)
    window_height = int((car_top - roof_top) * 0.7)
    window_top = roof_top + int((car_top - roof_top) * 0.15)
    window_left = center_x - int(window_width * 0.5)
    
    draw.rounded_rectangle(
        [window_left, window_top, window_left + window_width, window_top + window_height],
        radius=4,
        fill=(200, 230, 255, 255)
    )
    
    # Draw wheels
    wheel_radius = int(height * 0.12)
    wheel_y = car_top + car_height
    
    # Left wheel
    left_wheel_x = car_left + int(car_width * 0.2)
    draw.ellipse(
        [left_wheel_x - wheel_radius, wheel_y - wheel_radius, 
         left_wheel_x + wheel_radius, wheel_y + wheel_radius],
        fill=(40, 40, 40, 255)
    )
    
    # Right wheel
    right_wheel_x = car_left + int(car_width * 0.8)
    draw.ellipse(
        [right_wheel_x - wheel_radius, wheel_y - wheel_radius, 
         right_wheel_x + wheel_radius, wheel_y + wheel_radius],
        fill=(40, 40, 40, 255)
    )
    
    # Draw wheel centers
    inner_radius = int(wheel_radius * 0.6)
    
    # Left wheel center
    draw.ellipse(
        [left_wheel_x - inner_radius, wheel_y - inner_radius, 
         left_wheel_x + inner_radius, wheel_y + inner_radius],
        fill=secondary_color
    )
    
    # Right wheel center
    draw.ellipse(
        [right_wheel_x - inner_radius, wheel_y - inner_radius, 
         right_wheel_x + inner_radius, wheel_y + inner_radius],
        fill=secondary_color
    )
    
    # Save in various formats
    img.save(output_path)
    
    # Save as ICO for Windows
    ico_path = os.path.splitext(output_path)[0] + '.ico'
    img.save(ico_path, format='ICO', sizes=[(16, 16), (32, 32), (48, 48), (128, 128)])
    
    return img

def create_logo(output_path, size=(400, 200)):
    """Create a text-based logo for WeAreCars"""
    # Create a new image with white background
    img = Image.new('RGBA', size, color=(255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Colors
    primary_color = (0, 77, 153, 255)  # Dark blue
    secondary_color = (255, 140, 0, 255)  # Orange
    
    try:
        # Try to load Arial font
        font = ImageFont.truetype("arial.ttf", 60)
        small_font = ImageFont.truetype("arial.ttf", 30)
    except IOError:
        # Fallback to default font
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Calculate text position
    width, height = size
    
    # Draw company name
    text = "WeAreCars"
    text_width = draw.textlength(text, font=font)
    text_x = (width - text_width) // 2
    draw.text((text_x, 40), text, fill=primary_color, font=font)
    
    # Draw tagline
    tagline = "Your premium car rental solution"
    tagline_width = draw.textlength(tagline, font=small_font)
    tagline_x = (width - tagline_width) // 2
    draw.text((tagline_x, 120), tagline, fill=secondary_color, font=small_font)
    
    # Save the image
    img.save(output_path)
    
    return img

def main():
    """Generate all assets"""
    # Create assets directory if it doesn't exist
    assets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
    os.makedirs(assets_dir, exist_ok=True)
    
    # Create car icon
    icon_path = os.path.join(assets_dir, "car_icon.png")
    print(f"Creating car icon at {icon_path}")
    create_car_icon(icon_path)
    
    # Create logo
    logo_path = os.path.join(assets_dir, "logo_placeholder.png")
    print(f"Creating logo at {logo_path}")
    create_logo(logo_path)
    
    print("Asset generation complete!")

if __name__ == "__main__":
    main() 