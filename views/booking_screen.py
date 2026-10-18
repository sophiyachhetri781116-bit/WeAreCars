"""
Booking screen for creating new car rentals
"""
import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
from datetime import datetime
import time

# Import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from controllers.validation import validate_name, validate_address, validate_age, validate_days
from controllers.pricing import calculate_rental_price
from controllers.database import get_available_cars, add_customer, add_booking, add_new_rental
from views.summary_screen import SummaryScreen

class BookingScreen(ttk.Frame):
    """Screen for creating new car rentals"""
    
    def __init__(self, parent, app):
        super().__init__(parent)
        self.parent = parent
        self.app = app
        
        # Configure the frame
        self.configure(style='TFrame')
        self.pack(fill=tk.BOTH, expand=True)
        
        # Initialize all variables first to avoid errors
        self.initialize_variables()
        
        # Create the main form container
        self.create_form_container()
    
    def initialize_variables(self):
        """Initialize all variables before creating the UI elements"""
        # Customer variables
        self.first_name_var = tk.StringVar()
        self.last_name_var = tk.StringVar()
        self.address_var = tk.StringVar()
        self.age_var = tk.StringVar()
        self.license_var = tk.BooleanVar()
        
        # Rental details
        self.days_var = tk.StringVar(value="1")
        
        # Car selection
        self.car_type_var = tk.StringVar(value="City car")
        self.fuel_type_var = tk.StringVar(value="Petrol")
        
        # Options
        self.mileage_var = tk.BooleanVar(value=False)
        self.breakdown_var = tk.BooleanVar(value=False)
        
        # Price preview
        self.price_var = tk.StringVar(value="£25.00")
    
    def create_form_container(self):
        """Create the main form container with scrolling and modern design"""
        # Create a background with gradient
        self.bg_frame = ttk.Frame(self, style='TFrame')
        self.bg_frame.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Create a canvas for scrolling
        self.canvas = tk.Canvas(self, bg=self.app.bg_color, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas, style='TFrame')
        
        # Configure scrolling
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack the canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Create a colorful header section
        self.header_frame = tk.Frame(
            self.scrollable_frame,
            background=self.app.primary_color,  # Use primary color for header
            highlightbackground=self.app.secondary_color,
            highlightthickness=2,
            padx=20,
            pady=20
        )
        self.header_frame.grid(row=0, column=0, columnspan=3, sticky="ew", padx=20, pady=(20, 30))
        
        # Add form title
        self.title_label = tk.Label(
            self.header_frame,
            text="New Car Rental Booking",
            font=("Arial", 24, "bold"),
            foreground="white",
            background=self.app.primary_color
        )
        self.title_label.pack(side=tk.LEFT, anchor="w")
        
        # Add a car icon or emoji to make it more appealing
        self.car_emoji = tk.Label(
            self.header_frame,
            text="🚗",  # Car emoji
            font=("Arial", 28),
            foreground="white",
            background=self.app.primary_color
        )
        self.car_emoji.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Create a frame to hold the paned window - this helps with expansion
        self.pane_container = ttk.Frame(self.scrollable_frame)
        self.pane_container.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.scrollable_frame.grid_rowconfigure(1, weight=1)
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        
        # Create sections using paned windows for horizontal layout with full width
        self.paned_window = ttk.PanedWindow(self.pane_container, orient="horizontal")
        self.paned_window.pack(fill=tk.BOTH, expand=True)
        
        # Create three colorful frames for a horizontal layout
        self.create_customer_section()  # Left section
        self.create_car_rental_section()  # Middle section
        self.create_options_and_price_section()  # Right section
        
        # Create buttons section
        self.create_buttons_section()
        
        # Configure grid for the scrollable frame to expand properly
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame.grid_rowconfigure(1, weight=1)
    
    def create_customer_section(self):
        """Create customer information section with improved visuals"""
        # Create a card-like container with rounded appearance
        self.customer_container = tk.Frame(
            self.paned_window,
            background=self.app.content_bg,
            highlightbackground=self.app.primary_color,
            highlightthickness=1,
            padx=20,  # Increased padding
            pady=20,  # Increased padding
            bd=0
        )
        self.paned_window.add(self.customer_container, weight=1)
        
        # Section header
        section_bg = "#e1f5fe"  # Light blue background for section header
        self.customer_header = tk.Frame(
            self.customer_container,
            background=section_bg,
            padx=15,  # Increased padding
            pady=15    # Increased padding
        )
        self.customer_header.pack(fill=tk.X, pady=(0, 15))  # Increased spacing
        
        # Add icon and title
        self.customer_icon = tk.Label(
            self.customer_header,
            text="👤",  # Person emoji
            font=("Arial", 18),  # Larger font
            background=section_bg,
            foreground=self.app.primary_color
        )
        self.customer_icon.pack(side=tk.LEFT, padx=(0, 5))
        
        self.customer_title = tk.Label(
            self.customer_header,
            text="Customer Information",
            font=("Arial", 16, "bold"),  # Larger font
            background=section_bg,
            foreground=self.app.primary_color
        )
        self.customer_title.pack(side=tk.LEFT)
        
        # Customer form fields with more spacing
        self.customer_form = ttk.Frame(self.customer_container, style="Content.TFrame")
        self.customer_form.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # First name
        ttk.Label(
            self.customer_form,
            text="First Name *",
            style="Content.TLabel",
            font=("Arial", 12, "bold")  # Larger font
        ).grid(row=0, column=0, sticky="w", pady=(10, 5))  # Increased spacing
        
        self.first_name_entry = ttk.Entry(
            self.customer_form,
            textvariable=self.first_name_var,
            width=30  # Wider entry
        )
        self.first_name_entry.grid(row=1, column=0, sticky="ew", pady=(0, 15))  # Increased spacing
        
        # Last name
        ttk.Label(
            self.customer_form,
            text="Last Name *",
            style="Content.TLabel",
            font=("Arial", 12, "bold")  # Larger font
        ).grid(row=2, column=0, sticky="w", pady=(10, 5))  # Increased spacing
        
        ttk.Entry(
            self.customer_form,
            textvariable=self.last_name_var,
            width=30  # Wider entry
        ).grid(row=3, column=0, sticky="ew", pady=(0, 15))  # Increased spacing
        
        # Address
        ttk.Label(
            self.customer_form,
            text="Address *",
            style="Content.TLabel",
            font=("Arial", 12, "bold")  # Larger font
        ).grid(row=4, column=0, sticky="w", pady=(10, 5))  # Increased spacing
        
        ttk.Entry(
            self.customer_form,
            textvariable=self.address_var,
            width=30  # Wider entry
        ).grid(row=5, column=0, sticky="ew", pady=(0, 15))  # Increased spacing
        
        # Age
        ttk.Label(
            self.customer_form,
            text="Age *",
            style="Content.TLabel",
            font=("Arial", 12, "bold")  # Larger font
        ).grid(row=6, column=0, sticky="w", pady=(10, 5))  # Increased spacing
        
        ttk.Entry(
            self.customer_form,
            textvariable=self.age_var,
            width=10
        ).grid(row=7, column=0, sticky="w", pady=(0, 15))  # Increased spacing
        
        # Valid driving license
        license_frame = ttk.Frame(self.customer_form, style="Content.TFrame")
        license_frame.grid(row=8, column=0, sticky="w", pady=(10, 15))  # Increased spacing
        
        ttk.Checkbutton(
            license_frame,
            text="Valid Driving License *",
            variable=self.license_var,
            style="TCheckbutton"
        ).pack(side=tk.LEFT)
        
        # For better appearance in the customer form
        self.customer_form.columnconfigure(0, weight=1)
    
    def create_car_rental_section(self):
        """Create car selection and rental details section"""
        # Create a card-like container
        self.car_container = tk.Frame(
            self.paned_window,
            background=self.app.content_bg,
            highlightbackground=self.app.secondary_color,
            highlightthickness=1,
            padx=20,  # Increased padding
            pady=20,  # Increased padding
            bd=0
        )
        self.paned_window.add(self.car_container, weight=1)
        
        # Section header
        section_bg = "#A5E160"  # Light amber background for section header
        self.car_header = tk.Frame(
            self.car_container,
            background=section_bg,
            padx=15,  # Increased padding
            pady=15    # Increased padding
        )
        self.car_header.pack(fill=tk.X, pady=(0, 15))  # Increased spacing
        
        # Add icon and title
        self.car_icon = tk.Label(
            self.car_header,
            text="🚘",  # Car emoji
            font=("Arial", 18),  # Larger font
            background=section_bg,
            foreground=self.app.secondary_color
        )
        self.car_icon.pack(side=tk.LEFT, padx=(0, 5))
        
        self.car_title = tk.Label(
            self.car_header,
            text="Car Selection",
            font=("Arial", 16, "bold"),  # Larger font
            background=section_bg,
            foreground=self.app.secondary_color
        )
        self.car_title.pack(side=tk.LEFT)
        
        # Car selection form with more spacing
        self.car_form = ttk.Frame(self.car_container, style="Content.TFrame")
        self.car_form.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Car type
        ttk.Label(
            self.car_form,
            text="Car Type *",
            style="Content.TLabel",
            font=("Arial", 12, "bold")  # Larger font
        ).grid(row=0, column=0, sticky="w", pady=(10, 5))  # Increased spacing
        
        self.car_types = ["City car", "Family car", "Sports car", "SUV"]
        self.car_type_combobox = ttk.Combobox(
            self.car_form,
            textvariable=self.car_type_var,
            values=self.car_types,
            state="readonly",
            width=20  # Wider combobox
        )
        self.car_type_combobox.grid(row=1, column=0, sticky="ew", pady=(0, 5))
        self.car_type_combobox.current(0)  # Default to first option
        
        # Car type price info
        self.car_type_info = ttk.Label(
            self.car_form,
            text="No extra charge",
            foreground=self.app.secondary_color,
            style="Content.TLabel",
            font=("Arial", 11, "italic")  # Slightly larger font
        )
        self.car_type_info.grid(row=2, column=0, sticky="w", pady=(0, 15))  # Increased spacing
        
        # Fuel type
        ttk.Label(
            self.car_form,
            text="Fuel Type *",
            style="Content.TLabel",
            font=("Arial", 12, "bold")  # Larger font
        ).grid(row=3, column=0, sticky="w", pady=(10, 5))  # Increased spacing
        
        self.fuel_types = ["Petrol", "Diesel", "Hybrid", "Full electric"]
        self.fuel_type_combobox = ttk.Combobox(
            self.car_form,
            textvariable=self.fuel_type_var,
            values=self.fuel_types,
            state="readonly",
            width=20  # Wider combobox
        )
        self.fuel_type_combobox.grid(row=4, column=0, sticky="ew", pady=(0, 5))
        self.fuel_type_combobox.current(0)  # Default to first option
        
        # Fuel type price info
        self.fuel_type_info = ttk.Label(
            self.car_form,
            text="No extra charge",
            foreground=self.app.secondary_color,
            style="Content.TLabel",
            font=("Arial", 11, "italic")  # Slightly larger font
        )
        self.fuel_type_info.grid(row=5, column=0, sticky="w", pady=(0, 20))  # Increased spacing
        
        # Rental days section
        ttk.Separator(self.car_form, orient="horizontal").grid(row=6, column=0, sticky="ew", pady=15)
        
        days_frame = ttk.Frame(self.car_form, style="Content.TFrame")
        days_frame.grid(row=7, column=0, sticky="ew", pady=(10, 5))  # Increased spacing
        
        ttk.Label(
            days_frame,
            text="Number of Days *",
            style="Content.TLabel",
            font=("Arial", 12, "bold")  # Larger font
        ).pack(side=tk.LEFT)
        
        days_price = ttk.Label(
            days_frame,
            text="(£25 per day)",
            foreground=self.app.accent_color,
            style="Content.TLabel",
            font=("Arial", 11, "italic")  # Slightly larger font
        )
        days_price.pack(side=tk.LEFT, padx=(5, 0))
        
        # Days spinbox with cleaner styling
        self.days_spinbox = ttk.Spinbox(
            self.car_form,
            from_=1,
            to=28,
            textvariable=self.days_var,
            width=8  # Wider spinbox
        )
        self.days_spinbox.grid(row=8, column=0, sticky="w", pady=(0, 15))  # Increased spacing
        
        # Bind events for updates
        self.car_type_var.trace_add("write", self.update_car_type_info)
        self.fuel_type_var.trace_add("write", self.update_fuel_type_info)
        self.days_var.trace_add("write", self.update_price_preview)
        
        # Initialize info texts
        self.update_car_type_info()
        self.update_fuel_type_info()
        
        # For better appearance
        self.car_form.columnconfigure(0, weight=1)
    
    def create_options_and_price_section(self):
        """Create optional extras and price section"""
        # Create a card-like container
        self.options_container = tk.Frame(
            self.paned_window,
            background=self.app.content_bg,
            highlightbackground=self.app.accent_color,
            highlightthickness=1,
            padx=20,  # Increased padding
            pady=20,  # Increased padding
            bd=0
        )
        self.paned_window.add(self.options_container, weight=1)
        
        # Section header
        section_bg = "#9D847E"  # Light green background for section header
        self.options_header = tk.Frame(
            self.options_container,
            background=section_bg,
            padx=15,  # Increased padding
            pady=15    # Increased padding
        )
        self.options_header.pack(fill=tk.X, pady=(0, 15))  # Increased spacing
        
        # Add icon and title
        self.options_icon = tk.Label(
            self.options_header,
            text="✓",  # Checkmark
            font=("Arial", 18),  # Larger font
            background=section_bg,
            foreground=self.app.accent_color
        )
        self.options_icon.pack(side=tk.LEFT, padx=(0, 5))
        
        self.options_title = tk.Label(
            self.options_header,
            text="Options & Pricing",
            font=("Arial", 16, "bold"),  # Larger font
            background=section_bg,
            foreground=self.app.accent_color
        )
        self.options_title.pack(side=tk.LEFT)
        
        # Options form with more spacing
        self.options_form = ttk.Frame(self.options_container, style="Content.TFrame")
        self.options_form.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Optional extras with improved styling
        extras_label = ttk.Label(
            self.options_form,
            text="Optional Extras",
            style="Content.TLabel",
            font=("Arial", 12, "bold")  # Larger font
        )
        extras_label.grid(row=0, column=0, sticky="w", pady=(10, 15))  # Increased spacing
        
        # Unlimited mileage - with colorful indicator
        mileage_frame = ttk.Frame(self.options_form, style="Content.TFrame")
        mileage_frame.grid(row=1, column=0, sticky="w", pady=(0, 10))  # Increased spacing
        
        mileage_color = tk.Frame(mileage_frame, bg=self.app.secondary_color, width=6, height=25)  # Larger indicator
        mileage_color.pack(side=tk.LEFT, padx=(0, 10))  # Increased spacing
        
        self.mileage_check = ttk.Checkbutton(
            mileage_frame,
            text="Unlimited Mileage",
            variable=self.mileage_var,
            style="TCheckbutton",
            command=self.update_price_preview
        )
        self.mileage_check.pack(side=tk.LEFT)
        
        mileage_price = ttk.Label(
            mileage_frame,
            text="(+ £10 per day)",
            foreground=self.app.secondary_color,
            style="Content.TLabel",
            font=("Arial", 11, "italic")  # Slightly larger font
        )
        mileage_price.pack(side=tk.LEFT, padx=(5, 0))
        
        # Breakdown cover - with colorful indicator
        breakdown_frame = ttk.Frame(self.options_form, style="Content.TFrame")
        breakdown_frame.grid(row=2, column=0, sticky="w", pady=(0, 20))  # Increased spacing
        
        breakdown_color = tk.Frame(breakdown_frame, bg=self.app.accent_color, width=6, height=25)  # Larger indicator
        breakdown_color.pack(side=tk.LEFT, padx=(0, 10))  # Increased spacing
        
        self.breakdown_check = ttk.Checkbutton(
            breakdown_frame,
            text="Breakdown Cover",
            variable=self.breakdown_var,
            style="TCheckbutton",
            command=self.update_price_preview
        )
        self.breakdown_check.pack(side=tk.LEFT)
        
        breakdown_price = ttk.Label(
            breakdown_frame,
            text="(+ £2 per day)",
            foreground=self.app.accent_color,
            style="Content.TLabel",
            font=("Arial", 11, "italic")  # Slightly larger font
        )
        breakdown_price.pack(side=tk.LEFT, padx=(5, 0))
        
        # Separator before price summary
        ttk.Separator(self.options_form, orient="horizontal").grid(row=3, column=0, sticky="ew", pady=20)  # Increased spacing
        
        # Price preview section with improved visual emphasis
        price_title = ttk.Label(
            self.options_form,
            text="Price Summary",
            style="Content.TLabel",
            font=("Arial", 12, "bold")  # Larger font
        )
        price_title.grid(row=4, column=0, sticky="w", pady=(0, 15))  # Increased spacing
        
        # Create a highlighted price box
        price_box = tk.Frame(
            self.options_form,
            background="#BB95B6",  # Light blue background for price box
            padx=20,  # Increased padding
            pady=20,  # Increased padding
            highlightbackground=self.app.primary_color,
            highlightthickness=2  # Thicker border
        )
        price_box.grid(row=5, column=0, sticky="ew", padx=5, pady=10)  # Increased spacing
        
        # Price label
        ttk.Label(
            price_box,
            text="Total Estimated Price:",
            font=("Arial", 13),  # Larger font
            style="Content.TLabel",
            background="#e3f2fd"
        ).pack(side=tk.TOP, anchor="w")
        
        # Price value with larger font and bold
        self.price_value = tk.Label(
            price_box,
            textvariable=self.price_var,
            font=("Arial", 24, "bold"),  # Larger font
            foreground=self.app.primary_color,
            background="#e3f2fd"
        )
        self.price_value.pack(side=tk.TOP, anchor="center", pady=15)  # Increased spacing
        
        # Price note
        ttk.Label(
            price_box,
            text="Final price displayed at checkout",
            font=("Arial", 10, "italic"),
            foreground="#757575",
            style="Content.TLabel",
            background="#e3f2fd"
        ).pack(side=tk.BOTTOM, anchor="e")
        
        # For better appearance
        self.options_form.columnconfigure(0, weight=1)
    
    def create_buttons_section(self):
        """Create attractive buttons for form actions"""
        # Create a gradient-like container for buttons
        self.buttons_container = tk.Frame(
            self.scrollable_frame,
            background=self.app.bg_color,
            padx=20,
            pady=20
        )
        self.buttons_container.grid(row=2, column=0, columnspan=3, sticky="ew", padx=20, pady=(20, 30))
        
        # Left side buttons
        self.left_buttons = tk.Frame(self.buttons_container, background=self.app.bg_color)
        self.left_buttons.pack(side=tk.LEFT)
        
        # Clear form button with icon
        self.clear_button = tk.Button(
            self.left_buttons,
            text=" Clear Form",
            command=self.clear_form,
            bg=self.app.bg_color,
            fg=self.app.dark_color,
            relief=tk.FLAT,
            padx=15,
            pady=10,
            font=("Arial", 11),
            compound=tk.LEFT
        )
        self.clear_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Right side buttons
        self.right_buttons = tk.Frame(self.buttons_container, background=self.app.bg_color)
        self.right_buttons.pack(side=tk.RIGHT)
        
        # Preview button
        self.preview_button = tk.Button(
            self.right_buttons,
            text="Preview Booking",
            command=self.continue_booking,
            bg=self.app.secondary_color,
            fg="white",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=10,
            relief=tk.FLAT,
            cursor="hand2"
        )
        self.preview_button.pack(side=tk.LEFT, padx=(0, 15))
        
        # Add a prominent Complete Booking button
        self.complete_button = tk.Button(
            self.right_buttons,
            text="COMPLETE BOOKING",
            command=self.direct_complete_booking,
            background=self.app.primary_color,
            foreground="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=12,
            cursor="hand2",
            relief=tk.FLAT
        )
        self.complete_button.pack(side=tk.RIGHT)
        
        # Add hover effects to buttons
        for button in [self.clear_button, self.preview_button, self.complete_button]:
            self.add_button_hover_effect(button)
    
    def update_car_type_info(self, *args):
        """Update car type price info text"""
        car_type = self.car_type_var.get()
        
        if car_type == "City car":
            self.car_type_info.config(text="No extra charge")
        elif car_type == "Family car":
            self.car_type_info.config(text="+ £50")
        elif car_type == "Sports car":
            self.car_type_info.config(text="+ £75")
        elif car_type == "SUV":
            self.car_type_info.config(text="+ £65")
        
        self.update_price_preview()
    
    def update_fuel_type_info(self, *args):
        """Update fuel type price info text"""
        fuel_type = self.fuel_type_var.get()
        
        if fuel_type in ["Petrol", "Diesel"]:
            self.fuel_type_info.config(text="No extra charge")
        elif fuel_type == "Hybrid":
            self.fuel_type_info.config(text="+ £30")
        elif fuel_type == "Full electric":
            self.fuel_type_info.config(text="+ £50")
        
        self.update_price_preview()
    
    def update_price_preview(self, *args):
        """Update the price preview based on current selections"""
        try:
            # Get number of days (validate first)
            days_str = self.days_var.get()
            valid, _, days = validate_days(days_str)
            
            if not valid:
                days = 1  # Default to 1 day if invalid
            
            # Get car and fuel types
            car_type = self.car_type_var.get()
            fuel_type = self.fuel_type_var.get()
            
            # Get optional extras
            unlimited_mileage = self.mileage_var.get()
            breakdown_cover = self.breakdown_var.get()
            
            # Calculate price
            price_breakdown = calculate_rental_price(
                days, car_type, fuel_type, unlimited_mileage, breakdown_cover
            )
            
            # Update price display
            self.price_var.set(f"£{price_breakdown['total_price']:.2f}")
            
        except Exception as e:
            # In case of error, show default price
            self.price_var.set("£25.00")
    
    def clear_form(self):
        """Clear all form fields"""
        # Reset customer info
        self.first_name_var.set("")
        self.last_name_var.set("")
        self.address_var.set("")
        self.age_var.set("")
        self.license_var.set(False)
        
        # Reset rental details
        self.days_var.set("1")
        
        # Reset car selection
        self.car_type_combobox.current(0)
        self.fuel_type_combobox.current(0)
        
        # Reset options
        self.mileage_var.set(False)
        self.breakdown_var.set(False)
        
        # Update price
        self.update_price_preview()
        
        # Set focus to first field
        self.first_name_entry.focus_set()
    
    def continue_booking(self):
        """Validate form and continue to summary if valid"""
        # Validate all required fields
        errors = []
        
        # Validate first name
        valid, message = validate_name(self.first_name_var.get())
        if not valid:
            errors.append(f"First Name: {message}")
        
        # Validate last name
        valid, message = validate_name(self.last_name_var.get())
        if not valid:
            errors.append(f"Last Name: {message}")
        
        # Validate address
        valid, message = validate_address(self.address_var.get())
        if not valid:
            errors.append(f"Address: {message}")
        
        # Validate age
        valid, message, age = validate_age(self.age_var.get())
        if not valid:
            errors.append(f"Age: {message}")
        
        # Validate driving license
        if not self.license_var.get():
            errors.append("Valid Driving License: Required to proceed with booking")
        
        # Validate days
        valid, message, days = validate_days(self.days_var.get())
        if not valid:
            errors.append(f"Number of Days: {message}")
        
        # Check if we have available cars
        available_cars = get_available_cars()
        if not available_cars:
            errors.append("No cars are currently available for rental")
        
        # If there are errors, show them and return
        if errors:
            error_message = "Please correct the following errors:\n\n" + "\n".join(errors)
            messagebox.showerror("Validation Error", error_message)
            return
        
        # If we get here, form is valid - calculate final price
        car_type = self.car_type_var.get()
        fuel_type = self.fuel_type_var.get()
        unlimited_mileage = self.mileage_var.get()
        breakdown_cover = self.breakdown_var.get()
        
        price_breakdown = calculate_rental_price(
            days, car_type, fuel_type, unlimited_mileage, breakdown_cover
        )
        
        # Create booking data dictionary
        booking_data = {
            "customer": {
                "first_name": self.first_name_var.get(),
                "last_name": self.last_name_var.get(),
                "address": self.address_var.get(),
                "age": age,
                "has_license": self.license_var.get()
            },
            "rental": {
                "days": days,
                "car_type": car_type,
                "fuel_type": fuel_type,
                "unlimited_mileage": unlimited_mileage,
                "breakdown_cover": breakdown_cover,
                "price": price_breakdown
            }
        }
        
        # Show summary screen 
        self.show_summary(booking_data)
    
    def show_summary(self, booking_data):
        """Show booking summary popup"""
        summary_window = tk.Toplevel(self.app.root)
        summary_window.title("Booking Summary")
        summary_window.geometry("600x500")
        summary_window.transient(self.app.root)  # Make it a child of main window
        summary_window.grab_set()  # Make it modal
        
        # Pass data to summary screen
        summary_screen = SummaryScreen(summary_window, self.app, booking_data, self.finalize_booking)
    
    def finalize_booking(self, booking_data):
        """Finalize booking and save to database"""
        try:
            # Add customer to database
            customer_id = add_customer(
                booking_data["customer"]["first_name"],
                booking_data["customer"]["last_name"],
                booking_data["customer"]["address"],
                booking_data["customer"]["age"],
                booking_data["customer"]["has_license"]
            )
            
            # Find an available car of the selected type and fuel
            available_cars = get_available_cars()
            selected_car = None
            
            for car in available_cars:
                if (car["car_type"] == booking_data["rental"]["car_type"] and 
                    car["fuel_type"] == booking_data["rental"]["fuel_type"]):
                    selected_car = car
                    break
            
            if not selected_car:
                # If no exact match, find any car of the selected type
                for car in available_cars:
                    if car["car_type"] == booking_data["rental"]["car_type"]:
                        selected_car = car
                        break
            
            if not selected_car:
                # If still no match, just use the first available car
                selected_car = available_cars[0]
            
            # Add booking to database
            start_date = datetime.now().strftime("%Y-%m-%d")
            
            # Record booking in database
            booking_id = add_booking(
                customer_id,
                selected_car["id"],
                booking_data["rental"]["days"],
                booking_data["rental"]["unlimited_mileage"],
                booking_data["rental"]["breakdown_cover"],
                start_date,
                booking_data["rental"]["price"]["total_price"]
            )
            
            # Add to the demo rental list for display in the rented cars screen
            rental_data = {
                "car_type": booking_data["rental"]["car_type"],
                "fuel_type": booking_data["rental"]["fuel_type"],
                "days": booking_data["rental"]["days"],
                "start_date": start_date,
                "price": booking_data["rental"]["price"]["total_price"]
            }
            
            add_new_rental(booking_data["customer"], rental_data)
            
            # Show success message
            messagebox.showinfo("Booking Confirmed", 
                               f"Booking has been successfully created for "
                               f"{booking_data['customer']['first_name']} "
                               f"{booking_data['customer']['last_name']}.")
            
            # Clear the form for next booking
            self.clear_form()
            
            # Try to switch to the rented cars tab to show the new booking
            try:
                # Try different ways to access the notebook
                if hasattr(self.app, 'notebook'):
                    self.app.notebook.select(1)  # Select the second tab (rented cars)
                elif hasattr(self.app, 'main_dashboard') and hasattr(self.app.main_dashboard, 'notebook'):
                    self.app.main_dashboard.notebook.select(1)
                
                # Try to refresh the car list if we can find it
                if hasattr(self.app, 'car_list_screen'):
                    self.app.car_list_screen.load_rental_data()
                elif hasattr(self.app, 'main_dashboard') and hasattr(self.app.main_dashboard, 'car_list_screen'):
                    self.app.main_dashboard.car_list_screen.load_rental_data()
            except:
                # If we can't switch tabs or refresh, just continue silently
                pass
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving the booking: {str(e)}")
            return False
        
        return True
    
    def direct_complete_booking(self):
        """Validate form and complete booking directly without preview"""
        # Validate all required fields
        errors = []
        
        # Validate first name
        valid, message = validate_name(self.first_name_var.get())
        if not valid:
            errors.append(f"First Name: {message}")
        
        # Validate last name
        valid, message = validate_name(self.last_name_var.get())
        if not valid:
            errors.append(f"Last Name: {message}")
        
        # Validate address
        valid, message = validate_address(self.address_var.get())
        if not valid:
            errors.append(f"Address: {message}")
        
        # Validate age
        valid, message, age = validate_age(self.age_var.get())
        if not valid:
            errors.append(f"Age: {message}")
        
        # Validate driving license
        if not self.license_var.get():
            errors.append("Valid Driving License: Required to proceed with booking")
        
        # Validate days
        valid, message, days = validate_days(self.days_var.get())
        if not valid:
            errors.append(f"Number of Days: {message}")
        
        # Check if we have available cars
        available_cars = get_available_cars()
        if not available_cars:
            errors.append("No cars are currently available for rental")
        
        # If there are errors, show them and return
        if errors:
            error_message = "Please correct the following errors:\n\n" + "\n".join(errors)
            messagebox.showerror("Validation Error", error_message)
            return
        
        # If we get here, form is valid - calculate final price
        car_type = self.car_type_var.get()
        fuel_type = self.fuel_type_var.get()
        unlimited_mileage = self.mileage_var.get()
        breakdown_cover = self.breakdown_var.get()
        
        price_breakdown = calculate_rental_price(
            days, car_type, fuel_type, unlimited_mileage, breakdown_cover
        )
        
        # Create booking data dictionary
        booking_data = {
            "customer": {
                "first_name": self.first_name_var.get(),
                "last_name": self.last_name_var.get(),
                "address": self.address_var.get(),
                "age": age,
                "has_license": self.license_var.get()
            },
            "rental": {
                "days": days,
                "car_type": car_type,
                "fuel_type": fuel_type,
                "unlimited_mileage": unlimited_mileage,
                "breakdown_cover": breakdown_cover,
                "price": price_breakdown
            }
        }
        
        # Show a confirmation dialog
        confirm = messagebox.askyesno(
            "Confirm Booking",
            f"Are you sure you want to book a {car_type} ({fuel_type}) for {days} days?\n"
            f"Total price: £{price_breakdown['total_price']:.2f}\n\n"
            f"Customer: {self.first_name_var.get()} {self.last_name_var.get()}"
        )
        
        if confirm:
            # Finalize the booking directly
            self.finalize_booking(booking_data)
    
    def add_button_hover_effect(self, button):
        """Add hover effect to a button"""
        original_bg = button.cget("background")
        original_fg = button.cget("foreground")
        hover_bg = self.lighten_color(original_bg) if original_bg != self.app.bg_color else self.app.primary_color
        hover_fg = "white" if original_bg == self.app.bg_color else original_fg
        
        button.bind("<Enter>", lambda e: self.on_button_hover(button, hover_bg, hover_fg))
        button.bind("<Leave>", lambda e: self.on_button_leave(button, original_bg, original_fg))
    
    def lighten_color(self, hex_color):
        """Lighten a hex color by 20%"""
        # Convert hex to RGB
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        # Lighten RGB values
        lighter_rgb = tuple(min(255, int(c + (255 - c) * 0.2)) for c in rgb)
        
        # Convert back to hex
        return f"#{lighter_rgb[0]:02x}{lighter_rgb[1]:02x}{lighter_rgb[2]:02x}"
    
    def on_button_hover(self, button, bg_color, fg_color):
        """Button hover effect"""
        button.config(background=bg_color, foreground=fg_color, cursor="hand2")
    
    def on_button_leave(self, button, bg_color, fg_color):
        """Button leave effect"""
        button.config(background=bg_color, foreground=fg_color, cursor="") 