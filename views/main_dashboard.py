"""
Main dashboard view with tabs for bookings and car lists
"""
import tkinter as tk
from tkinter import ttk
import os
import sys
from datetime import datetime

# Import controllers
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from controllers.database import get_rented_cars
from views.booking_screen import BookingScreen
from views.car_list import CarListScreen

class MainDashboard(ttk.Frame):
    """Main dashboard with tabs for different functions"""
    
    def __init__(self, parent, app):
        super().__init__(parent)
        self.parent = parent
        self.app = app
        
        # Configure the main dashboard frame
        self.configure(style='TFrame')
        self.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=1, relheight=1)
        
        # Create layout elements
        self.create_header()
        self.create_tabs()
        self.create_status_bar()
    
    def create_header(self):
        """Create header with logo and navigation"""
        self.header_frame = ttk.Frame(self, style='TFrame')
        self.header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Logo or title
        logo_frame = ttk.Frame(self.header_frame, style='TFrame')
        logo_frame.pack(side=tk.LEFT)
        
        # Check if logo exists
        logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                 "assets", "car_logo_.png")
        
        if not os.path.exists(logo_path):
            self.logo_label = ttk.Label(
                logo_frame, 
                text="WeAreCars", 
                font=("Arial", 20, "bold"),
                foreground=self.app.primary_color,
                style='TLabel'
            )
            self.logo_label.pack(side=tk.LEFT)
        else:
            # Load and display logo (if it exists)
            from PIL import Image, ImageTk
            img = Image.open(logo_path)
            img = img.resize((120, 40), Image.LANCZOS)
            self.logo_img = ImageTk.PhotoImage(img)
            self.logo_label = ttk.Label(
                logo_frame, 
                image=self.logo_img,
                style='TLabel'
            )
            self.logo_label.pack(side=tk.LEFT)
        
        # Staff info and logout
        user_frame = ttk.Frame(self.header_frame, style='TFrame')
        user_frame.pack(side=tk.RIGHT)
        
        self.staff_label = ttk.Label(
            user_frame,
            text="Logged in as: Staff",
            style='TLabel'
        )
        self.staff_label.pack(side=tk.LEFT, padx=10)
        
        self.logout_button = ttk.Button(
            user_frame,
            text="Logout",
            command=self.logout,
            style='TButton'
        )
        self.logout_button.pack(side=tk.LEFT)
    
    def create_tabs(self):
        """Create tab navigation for different screens"""
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.booking_frame = ttk.Frame(self.notebook, style='TFrame')
        self.cars_frame = ttk.Frame(self.notebook, style='TFrame')
        
        self.notebook.add(self.booking_frame, text="New Booking")
        self.notebook.add(self.cars_frame, text="Rented Cars")
        
        # Create content for each tab
        self.booking_screen = BookingScreen(self.booking_frame, self.app)
        self.car_list_screen = CarListScreen(self.cars_frame, self.app)
    
    def create_status_bar(self):
        """Create status bar at bottom of screen"""
        self.status_frame = ttk.Frame(self, style='TFrame')
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=5)
        
        # Current date/time
        current_time = datetime.now().strftime("%d-%m-%Y %H:%M")
        self.time_label = ttk.Label(
            self.status_frame,
            text=f"Date: {current_time}",
            style='TLabel'
        )
        self.time_label.pack(side=tk.LEFT)
        
        # Version info
        self.version_label = ttk.Label(
            self.status_frame,
            text="WeAreCars Rental System v1.0",
            style='TLabel'
        )
        self.version_label.pack(side=tk.RIGHT)
        
        # Update the time every minute
        self.update_time()
    
    def update_time(self):
        """Update the time in status bar"""
        current_time = datetime.now().strftime("%d-%m-%Y %H:%M")
        self.time_label.config(text=f"Date: {current_time}")
        # Schedule next update in 60 seconds
        self.after(60000, self.update_time)
    
    def logout(self):
        """Handle logout and return to login screen"""
        self.app.show_login_screen() 