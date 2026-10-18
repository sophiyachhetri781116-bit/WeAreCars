"""
Splash screen for the WeAreCars application
"""
import tkinter as tk
from tkinter import ttk
import os
from PIL import Image, ImageTk, ImageDraw, ImageFilter
import time
import threading
import math

class SplashScreen(ttk.Frame):
    """Splash screen with welcome message and animations"""
    
    def __init__(self, parent, app):
        super().__init__(parent)
        self.parent = parent
        self.app = app
        
        # Configure the splash screen frame
        self.configure(style='TFrame')
        self.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=1, relheight=1)
        
        # Get the window dimensions
        self.width = parent.winfo_width() or 1200
        self.height = parent.winfo_height() or 800
        
        # Create a canvas for drawing
        self.canvas = tk.Canvas(self, bg=app.bg_color, highlightthickness=0, width=self.width, height=self.height)
        self.canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=1, relheight=1)
        
        # Create background gradient with fallback
        try:
            self.create_background()
        except Exception as e:
            print(f"Error creating background: {e}")
            # Create a simple background as fallback
            self.canvas.create_rectangle(0, 0, self.width, self.height, fill=app.bg_color, outline="")
        
        # Load or create car icon with fallback
        try:
            self.icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                        "assets", "rent car photo.avif")
            
            if os.path.exists(self.icon_path):
                self.car_img = Image.open(self.icon_path)
                self.car_img = self.car_img.resize((150, 150), Image.LANCZOS)
                self.car_icon = ImageTk.PhotoImage(self.car_img)
            else:
                # Create a simple icon as fallback
                self.car_icon = self.create_simple_icon()
        except Exception as e:
            print(f"Error loading car icon: {e}")
            # Create a simple icon as fallback
            self.car_icon = self.create_simple_icon()
        
        # Load logo image with fallback
        try:
            self.logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                        "assets", "logo_placeholder.png")
            
            if os.path.exists(self.logo_path):
                img = Image.open(self.logo_path)
                img = img.resize((350, 100), Image.LANCZOS)
                self.logo_img = ImageTk.PhotoImage(img)
            else:
                self.logo_img = None
        except Exception as e:
            print(f"Error loading logo: {e}")
            self.logo_img = None
        
        # Show elements with animations
        self.show_elements()
    
    def create_simple_icon(self):
        """Create a simple car icon as fallback"""
        icon_img = Image.new('RGBA', (150, 150), color=(255, 255, 255, 0))
        draw = ImageDraw.Draw(icon_img)
        
        # Draw a car shape
        primary_color = self.hex_to_rgb(self.app.primary_color)
        secondary_color = self.hex_to_rgb(self.app.secondary_color)
        
        # Car body (rectangle with rounded corners)
        draw.rectangle([30, 50, 120, 100], fill=primary_color, outline=(0, 0, 0))
        
        # Car top
        draw.rectangle([50, 30, 100, 50], fill=primary_color, outline=(0, 0, 0))
        
        # Wheels
        draw.ellipse([30, 90, 60, 120], fill=secondary_color, outline=(0, 0, 0))
        draw.ellipse([90, 90, 120, 120], fill=secondary_color, outline=(0, 0, 0))
        
        return ImageTk.PhotoImage(icon_img)
    
    def create_background(self):
        """Create a gradient background with waves"""
        # Create a gradient image
        gradient_img = Image.new('RGB', (self.width, self.height), color=self.hex_to_rgb(self.app.bg_color))
        draw = ImageDraw.Draw(gradient_img)
        
        # Create gradient from primary color to background color
        primary = self.hex_to_rgb(self.app.primary_color)
        secondary = self.hex_to_rgb(self.app.bg_color)
        
        for y in range(self.height):
            # Calculate gradient ratio
            ratio = y / self.height
            r = int(primary[0] * (1 - ratio) + secondary[0] * ratio)
            g = int(primary[1] * (1 - ratio) + secondary[1] * ratio)
            b = int(primary[2] * (1 - ratio) + secondary[2] * ratio)
            
            draw.line([(0, y), (self.width, y)], fill=(r, g, b))
        
        # Add some decorative elements
        accent_color = self.hex_to_rgb(self.app.secondary_color)
        
        # Draw circles
        for i in range(5):
            size = 30 + i * 10
            x = 100 + i * 50
            y = 100 - i * 10
            draw.ellipse([x, y, x+size, y+size], fill=(accent_color[0], accent_color[1], accent_color[2], 128))
        
        # Convert to PhotoImage and display on canvas
        self.bg_image = ImageTk.PhotoImage(gradient_img)
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw", tags="background")
    
    def hex_to_rgb(self, hex_color):
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def show_elements(self):
        """Show all splash screen elements with animations"""
        # Get dimensions
        center_x = self.width // 2
        
        # Create car icon
        icon_id = self.canvas.create_image(center_x, 180, image=self.car_icon, tags="car_icon")
        
        # Create logo (either image or text)
        if self.logo_img:
            # Create an image logo
            self.canvas.create_image(center_x, 320, image=self.logo_img, tags="logo")
        else:
            # Create a text-based logo with shadow effect
            # Shadow
            self.canvas.create_text(center_x + 2, 322, 
                                   text="WeAreCars", 
                                   font=("Arial", 54, "bold"), 
                                   fill="#00000044",  # Semi-transparent black
                                   tags="logo_shadow")
            # Main text
            self.canvas.create_text(center_x, 320, 
                                   text="WeAreCars", 
                                   font=("Arial", 54, "bold"), 
                                   fill=self.app.secondary_color, 
                                   tags="logo")
        
        # Add tagline
        self.canvas.create_text(center_x, 380, 
                               text="Your Premium Car Rental Solution", 
                               font=("Arial", 20, "italic"), 
                               fill=self.app.dark_color, 
                               tags="tagline")
        
        # Create a card-like container for content
        card_x1 = center_x - 350
        card_x2 = center_x + 350
        card_y1 = 420
        card_y2 = 650  # Increase card height to provide more space
        
        # Card background
        self.canvas.create_rectangle(
            card_x1, card_y1, card_x2, card_y2,
            fill=self.app.content_bg,
            outline=self.app.border_color,
            width=1,
            tags="card"
        )
        
        # Add welcome message
        self.canvas.create_text(center_x, card_y1 + 30, 
                               text="Welcome to WeAreCars Rental System", 
                               font=("Arial", 18, "bold"), 
                               fill=self.app.primary_color, 
                               tags="welcome")
        
        # Add divider line
        self.canvas.create_line(card_x1 + 30, card_y1 + 60, card_x2 - 30, card_y1 + 60, 
                               width=2, fill=self.app.primary_color, tags="divider")
        
        # Instructions text
        instructions = [
            "• View and manage all car rentals",
            "• Add new customers and bookings",
            "• Track rental details and payments",
            "• Generate reports and analytics"
        ]
        
        # Add instructions
        for i, instruction in enumerate(instructions):
            y_pos = card_y1 + 100 + i * 30
            self.canvas.create_text(center_x, y_pos, 
                                  text=instruction, 
                                  font=("Arial", 14), 
                                  fill=self.app.dark_color, 
                                  tags=f"instruction{i}")
        
        # Add loading bar - positioned further down with more space
        bar_y = card_y2 - 70  # More space before loading bar
        self.loading_bar_bg = self.canvas.create_rectangle(
            card_x1 + 50, bar_y, card_x2 - 50, bar_y + 20,
            outline=self.app.primary_color, fill=self.app.bg_color, width=2,
            tags="loading_bg"
        )
        
        self.loading_bar = self.canvas.create_rectangle(
            card_x1 + 52, bar_y + 2, card_x1 + 52, bar_y + 18,
            outline="", fill=self.app.secondary_color,
            tags="loading_bar"
        )
        
        # Add loading text with more space below the loading bar
        # Create a background rectangle for the loading text
        text_bg_padding = 8
        self.loading_text_bg = self.canvas.create_rectangle(
            center_x - 60, bar_y + 45 - 12 - text_bg_padding,  
            center_x + 60, bar_y + 45 + 12 + text_bg_padding,
            fill=self.app.bg_color,
            outline="",
            tags="loading_text_bg"
        )
        
        # Position the loading text over its background
        self.loading_text = self.canvas.create_text(
            center_x, bar_y + 45,  # Increased space between bar and text
            text="Loading... 0%",
            font=("Arial", 12, "bold"),  # Made font bold for better visibility
            fill=self.app.primary_color,  # Changed to primary color for better contrast
            tags="loading_text"
        )
        
        # Animate loading bar
        self.animate_loading_bar()
    
    def animate_loading_bar(self):
        """Animate the loading bar from 0% to 100%"""
        if not hasattr(self, 'canvas') or not self.winfo_exists():
            return
            
        try:
            # Get loading bar coordinates
            x1, y1, _, y2 = self.canvas.coords(self.loading_bar)
            x2 = x1  # Start width is 0
            
            # Get background bar coordinates for full width
            bg_x1, _, bg_x2, _ = self.canvas.coords(self.loading_bar_bg)
            
            # Calculate total width
            total_width = bg_x2 - bg_x1 - 4  # Subtract border padding
            
            # Define animation duration and steps
            duration_ms = 3000  # 3 seconds
            steps = 100
            width_per_step = total_width / steps
            delay_ms = duration_ms / steps
            
            def update_bar(step=0):
                if not hasattr(self, 'canvas') or not self.winfo_exists():
                    return
                
                if step <= steps:
                    # Calculate new width
                    new_x2 = x1 + (width_per_step * step)
                    
                    # Update loading bar
                    self.canvas.coords(self.loading_bar, x1, y1, new_x2, y2)
                    
                    # Update loading text
                    percent = int((step / steps) * 100)
                    self.canvas.itemconfigure(self.loading_text, text=f"Loading... {percent}%")
                    
                    # Make sure text background is behind the text
                    self.canvas.tag_lower(self.loading_text_bg, self.loading_text)
                    
                    # Schedule next update
                    self.after(int(delay_ms), lambda: update_bar(step + 1))
            
            # Start animation
            update_bar()
            
        except Exception as e:
            print(f"Error in animate_loading_bar: {e}")
            # If animation fails, at least show a full loading bar
            try:
                bg_x1, y1, bg_x2, y2 = self.canvas.coords(self.loading_bar_bg)
                self.canvas.coords(self.loading_bar, bg_x1+2, y1+2, bg_x2-2, y2-2)
                self.canvas.itemconfigure(self.loading_text, text="Loading... 100%")
            except:
                pass 