import tkinter as tk
from tkinter import ttk
import os
import sys
from PIL import Image, ImageTk
import sqlite3
import time

# Import our custom modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from views.splash_screen import SplashScreen
from views.login_screen import LoginScreen
from views.main_dashboard import MainDashboard
from controllers.database import initialize_database

class WeAreCarsApp:
    """Main application class for WeAreCars rental system"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("WeAreCars Rental System")
        self.root.geometry("1200x800")  # Larger default size
        self.root.minsize(900, 700)  # Increased minimum size
        
        # Center the window on screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 1200) // 2
        y = (screen_height - 800) // 2
        self.root.geometry(f"1200x800+{x}+{y}")
        
        # Set icon
        try:
            self.root.iconbitmap(os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "car_icon.ico"))
        except tk.TclError:
            pass  # .ico icons are not supported on every platform
        
        # Configure the theme and styles
        self.setup_theme()
        
        # Initialize database
        initialize_database()
        
        # Make the window responsive
        self.setup_responsive_layout()
        
        # Start with splash screen
        self.current_frame = None
        self.show_splash_screen()
        
        self.root.mainloop()
    
    def setup_responsive_layout(self):
        """Setup responsive layout that adjusts to window size"""
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
    
    def setup_theme(self):
        """Setup theme, styles and colors for the application"""
        # Colors - Enhanced with more vibrant palette
        self.primary_color = "#1a5fb4"  # Richer blue
        self.secondary_color = "#ff7800"  # Brighter orange
        self.accent_color = "#26a269"  # Green accent
        self.accent2_color = "#c01c28"  # Red accent
        self.bg_color = "#f6f5f4"  # Light background
        self.content_bg = "#ffffff"  # White content background
        self.light_color = "#ffffff"  # White
        self.dark_color = "#241f31"  # Dark text
        self.border_color = "#d3d7cf"  # Border color
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')  # Use clam theme as base
        
        # Configure common elements
        style.configure('TFrame', background=self.bg_color)
        style.configure('Content.TFrame', background=self.content_bg, relief='flat')
        
        # Button styles
        style.configure('TButton', 
                        background=self.primary_color, 
                        foreground=self.light_color, 
                        font=('Arial', 11, 'bold'),
                        padding=8)
        style.map('TButton', 
                 background=[('active', self.secondary_color)],
                 foreground=[('active', self.light_color)])
        
        # Primary action button style
        style.configure('Primary.TButton',
                       background=self.secondary_color,
                       foreground=self.light_color,
                       font=('Arial', 11, 'bold'),
                       padding=8)
        style.map('Primary.TButton',
                 background=[('active', self.accent_color)],
                 foreground=[('active', self.light_color)])
        
        # Accent button style
        style.configure('Accent.TButton',
                       background=self.accent_color,
                       foreground=self.light_color,
                       font=('Arial', 11, 'bold'),
                       padding=8)
        style.map('Accent.TButton',
                 background=[('active', '#2ec27e')],  # Lighter green on hover
                 foreground=[('active', self.light_color)])
        
        # Danger button style
        style.configure('Danger.TButton',
                       background=self.accent2_color,
                       foreground=self.light_color,
                       font=('Arial', 11, 'bold'),
                       padding=8)
        style.map('Danger.TButton',
                 background=[('active', '#e01b24')],  # Lighter red on hover
                 foreground=[('active', self.light_color)])
        
        # Label styles
        style.configure('TLabel', 
                        background=self.bg_color, 
                        foreground=self.dark_color, 
                        font=('Arial', 11))
        
        style.configure('Content.TLabel',
                       background=self.content_bg,
                       foreground=self.dark_color,
                       font=('Arial', 11))
        
        style.configure('Header.TLabel', 
                       font=('Arial', 16, 'bold'), 
                       foreground=self.primary_color,
                       background=self.bg_color)
        
        style.configure('Title.TLabel', 
                       font=('Arial', 22, 'bold'), 
                       foreground=self.primary_color,
                       background=self.bg_color)
        
        style.configure('Subtitle.TLabel',
                       font=('Arial', 14),
                       foreground=self.secondary_color,
                       background=self.bg_color)
        
        # Frame with border
        style.configure('Card.TFrame',
                       background=self.content_bg,
                       relief='solid',
                       borderwidth=1)
        
        # LabelFrame style
        style.configure('TLabelframe',
                       background=self.content_bg,
                       foreground=self.primary_color,
                       font=('Arial', 12, 'bold'))
        
        style.configure('TLabelframe.Label',
                       background=self.bg_color,
                       foreground=self.primary_color,
                       font=('Arial', 12, 'bold'))
        
        # Entry style
        style.configure('TEntry',
                       fieldbackground=self.light_color,
                       foreground=self.dark_color,
                       bordercolor=self.border_color,
                       lightcolor=self.border_color,
                       darkcolor=self.border_color,
                       borderwidth=1,
                       font=('Arial', 11))
        
        # Combobox style
        style.configure('TCombobox',
                       fieldbackground=self.light_color,
                       foreground=self.dark_color,
                       bordercolor=self.border_color,
                       arrowcolor=self.primary_color,
                       font=('Arial', 11))
        
        # Notebook (tabs) style
        style.configure('TNotebook',
                       background=self.bg_color,
                       tabmargins=[2, 5, 2, 0])
        
        style.configure('TNotebook.Tab',
                       background=self.bg_color,
                       foreground=self.dark_color,
                       padding=[15, 5],
                       font=('Arial', 11))
        
        style.map('TNotebook.Tab',
                 background=[('selected', self.primary_color)],
                 foreground=[('selected', self.light_color)],
                 expand=[('selected', [1, 1, 1, 0])])
        
        # Treeview style (for tables)
        style.configure('Treeview',
                       background=self.content_bg,
                       foreground=self.dark_color,
                       rowheight=30,
                       fieldbackground=self.content_bg,
                       font=('Arial', 11))
        
        style.configure('Treeview.Heading',
                       background=self.primary_color,
                       foreground=self.light_color,
                       font=('Arial', 11, 'bold'),
                       relief='flat')
        
        style.map('Treeview.Heading',
                 background=[('active', self.secondary_color)])
        
        # Checkbutton style
        style.configure('TCheckbutton',
                       background=self.bg_color,
                       foreground=self.dark_color,
                       font=('Arial', 11))
        
        style.map('TCheckbutton',
                 background=[('active', self.bg_color)])
        
        # Set the default background
        self.root.configure(background=self.bg_color)
    
    def show_splash_screen(self):
        """Show splash screen and schedule login screen"""
        if self.current_frame:
            self.current_frame.destroy()
        
        self.current_frame = SplashScreen(self.root, self)
        self.root.after(4000, self.show_login_screen)  # Longer display time
    
    def show_login_screen(self):
        """Show login screen"""
        if self.current_frame:
            self.current_frame.destroy()
        
        self.current_frame = LoginScreen(self.root, self)
    
    def show_main_dashboard(self):
        """Show main dashboard after successful login"""
        if self.current_frame:
            self.current_frame.destroy()
        
        self.current_frame = MainDashboard(self.root, self)


if __name__ == "__main__":
    app = WeAreCarsApp() 