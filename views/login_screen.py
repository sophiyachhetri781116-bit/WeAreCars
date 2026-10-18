"""
Login screen for staff authentication
"""
import tkinter as tk
from tkinter import ttk, messagebox
import os
from PIL import Image, ImageTk
import sys

# Import controllers
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from controllers.auth import validate_login

class LoginScreen(ttk.Frame):
    """Login screen for staff authentication"""
    
    def __init__(self, parent, app):
        super().__init__(parent)
        self.parent = parent
        self.app = app
        
        # Configure the login screen frame
        self.configure(style='TFrame')
        self.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=1, relheight=1)
        
        # Create content wrapper frame
        self.content_frame = ttk.Frame(self, style='TFrame')
        self.content_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=500, height=600)
        
        # Load logo
        self.logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                     "assets", "car logo.png")
        
        if not os.path.exists(self.logo_path):
            # Create text-based logo
            self.logo_label = ttk.Label(
                self.content_frame, 
                text="WeAreCars", 
                font=("Arial", 40, "bold"),
                foreground=app.primary_color,
                style='TLabel'
            )
        else:
            # Load and display image logo
            img = Image.open(self.logo_path)
            img = img.resize((250, 150), Image.LANCZOS)
            self.logo_img = ImageTk.PhotoImage(img)
            self.logo_label = ttk.Label(
                self.content_frame, 
                image=self.logo_img,
                style='TLabel'
            )
        
        self.logo_label.pack(pady=(20, 10))
        
        # Login title
        self.title_label = ttk.Label(
            self.content_frame, 
            text="Staff Login", 
            style='Title.TLabel'
        )
        self.title_label.pack(pady=(10, 30))
        
        # Username field
        self.username_frame = ttk.Frame(self.content_frame, style='TFrame')
        self.username_frame.pack(fill=tk.X, padx=50, pady=10)
        
        self.username_label = ttk.Label(
            self.username_frame, 
            text="Username", 
            style='TLabel'
        )
        self.username_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.username_var = tk.StringVar()
        self.username_entry = ttk.Entry(
            self.username_frame, 
            textvariable=self.username_var,
            width=40,
            font=("Arial", 12)
        )
        self.username_entry.pack(fill=tk.X)
        
        # Password field
        self.password_frame = ttk.Frame(self.content_frame, style='TFrame')
        self.password_frame.pack(fill=tk.X, padx=50, pady=10)
        
        self.password_label = ttk.Label(
            self.password_frame, 
            text="Password", 
            style='TLabel'
        )
        self.password_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(
            self.password_frame, 
            textvariable=self.password_var,
            width=40,
            font=("Arial", 12),
            show="•"  # Hide password characters
        )
        self.password_entry.pack(fill=tk.X)
        
        # Error message display
        self.error_var = tk.StringVar()
        self.error_label = ttk.Label(
            self.content_frame,
            textvariable=self.error_var,
            foreground="red",
            style='TLabel'
        )
        self.error_label.pack(pady=10)
        
        # Login button
        self.login_button = ttk.Button(
            self.content_frame,
            text="Login",
            command=self.login,
            style='TButton',
            width=20
        )
        self.login_button.pack(pady=20)
        
        # Help text
        self.help_frame = ttk.Frame(self.content_frame, style='TFrame')
        self.help_frame.pack(fill=tk.X, padx=50, pady=(30, 0))
        
        self.help_label = ttk.Label(
            self.help_frame,
            text="Forgot your login details? Please contact your system administrator.",
            wraplength=400,
            justify=tk.CENTER,
            style='TLabel'
        )
        self.help_label.pack()
        
        # Set focus to username field and bind Enter key
        self.username_entry.focus_set()
        self.username_entry.bind("<Return>", lambda event: self.password_entry.focus_set())
        self.password_entry.bind("<Return>", lambda event: self.login())
        
        # Add animation for button hover
        self.login_button.bind("<Enter>", self.on_button_hover)
        self.login_button.bind("<Leave>", self.on_button_leave)
    
    def login(self):
        """Handle login attempt"""
        username = self.username_var.get().strip()
        password = self.password_var.get()
        
        if not username:
            self.show_error("Please enter your username")
            self.username_entry.focus_set()
            return
        
        if not password:
            self.show_error("Please enter your password")
            self.password_entry.focus_set()
            return
        
        # Validate credentials
        if validate_login(username, password):
            self.error_var.set("")
            # Show success animation before proceeding
            self.show_success_animation()
        else:
            self.show_error("Invalid username or password")
            self.password_entry.delete(0, tk.END)
            self.password_entry.focus_set()
    
    def show_error(self, message):
        """Display error message"""
        self.error_var.set(message)
    
    def show_success_animation(self):
        """Show a success animation before proceeding to main dashboard"""
        # Hide login elements
        for widget in self.content_frame.winfo_children():
            widget.pack_forget()
        
        # Create success message
        success_label = ttk.Label(
            self.content_frame, 
            text="Login Successful!", 
            font=("Arial", 20, "bold"),
            foreground="green",
            style='TLabel'
        )
        success_label.pack(pady=(200, 20))
        
        # Create loading spinner or animation here
        loading_label = ttk.Label(
            self.content_frame, 
            text="Loading dashboard...", 
            style='TLabel'
        )
        loading_label.pack()
        
        # After delay, proceed to main dashboard
        self.parent.after(1500, self.app.show_main_dashboard)
    
    def on_button_hover(self, event):
        """Handle button hover animation"""
        # This is handled by ttk.Style in the main app
        pass
    
    def on_button_leave(self, event):
        """Handle button leave animation"""
        # This is handled by ttk.Style in the main app
        pass 