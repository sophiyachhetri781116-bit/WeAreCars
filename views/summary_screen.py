"""
Booking summary screen for reviewing rental details before finalizing
"""
import tkinter as tk
from tkinter import ttk
from datetime import datetime

class SummaryScreen(ttk.Frame):
    """Summary screen for reviewing booking details"""
    
    def __init__(self, parent, app, booking_data, on_confirm_callback):
        super().__init__(parent)
        self.parent = parent
        self.app = app
        self.booking_data = booking_data
        self.on_confirm_callback = on_confirm_callback
        
        # Configure the frame
        self.configure(style='TFrame')
        self.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create UI elements
        self.create_title()
        self.create_summary()
        self.create_buttons()
    
    def create_title(self):
        """Create summary title section"""
        self.title_frame = ttk.Frame(self, style='TFrame')
        self.title_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.title_label = ttk.Label(
            self.title_frame,
            text="Booking Summary",
            style='Title.TLabel'
        )
        self.title_label.pack(side=tk.LEFT)
        
        # Add current date
        current_date = datetime.now().strftime("%d-%m-%Y")
        self.date_label = ttk.Label(
            self.title_frame,
            text=f"Date: {current_date}",
            style='TLabel'
        )
        self.date_label.pack(side=tk.RIGHT)
    
    def create_summary(self):
        """Create summary content sections"""
        # Main content frame
        self.content_frame = ttk.Frame(self, style='TFrame')
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Customer section
        self.customer_frame = ttk.LabelFrame(
            self.content_frame,
            text="Customer Details",
            style='TLabelframe'
        )
        self.customer_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Customer details
        customer = self.booking_data["customer"]
        customer_details = [
            {"label": "Name:", "value": f"{customer['first_name']} {customer['last_name']}"},
            {"label": "Address:", "value": customer['address']},
            {"label": "Age:", "value": str(customer['age'])},
            {"label": "Valid License:", "value": "Yes" if customer['has_license'] else "No"}
        ]
        
        # Create customer detail rows
        for idx, detail in enumerate(customer_details):
            label = ttk.Label(
                self.customer_frame,
                text=detail["label"],
                font=("Arial", 10, "bold"),
                style='TLabel'
            )
            label.grid(row=idx, column=0, padx=(10, 5), pady=5, sticky="w")
            
            value = ttk.Label(
                self.customer_frame,
                text=detail["value"],
                style='TLabel'
            )
            value.grid(row=idx, column=1, padx=5, pady=5, sticky="w")
        
        # Rental section
        self.rental_frame = ttk.LabelFrame(
            self.content_frame,
            text="Rental Details",
            style='TLabelframe'
        )
        self.rental_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Rental details
        rental = self.booking_data["rental"]
        rental_details = [
            {"label": "Car Type:", "value": rental['car_type']},
            {"label": "Fuel Type:", "value": rental['fuel_type']},
            {"label": "Rental Period:", "value": f"{rental['days']} day(s)"},
            {"label": "Unlimited Mileage:", "value": "Yes" if rental['unlimited_mileage'] else "No"},
            {"label": "Breakdown Cover:", "value": "Yes" if rental['breakdown_cover'] else "No"}
        ]
        
        # Create rental detail rows
        for idx, detail in enumerate(rental_details):
            label = ttk.Label(
                self.rental_frame,
                text=detail["label"],
                font=("Arial", 10, "bold"),
                style='TLabel'
            )
            label.grid(row=idx, column=0, padx=(10, 5), pady=5, sticky="w")
            
            value = ttk.Label(
                self.rental_frame,
                text=detail["value"],
                style='TLabel'
            )
            value.grid(row=idx, column=1, padx=5, pady=5, sticky="w")
        
        # Price breakdown section
        self.price_frame = ttk.LabelFrame(
            self.content_frame,
            text="Price Breakdown",
            style='TLabelframe'
        )
        self.price_frame.pack(fill=tk.X)
        
        # Price details
        price = self.booking_data["rental"]["price"]
        price_details = [
            {"label": "Base Price:", "value": f"£{price['base_price']:.2f}"},
            {"label": "Car Type Surcharge:", "value": f"£{price['car_type_surcharge']:.2f}"},
            {"label": "Fuel Type Surcharge:", "value": f"£{price['fuel_type_surcharge']:.2f}"}
        ]
        
        # Add optional extras if selected
        if rental['unlimited_mileage']:
            price_details.append({"label": "Unlimited Mileage:", "value": f"£{price['unlimited_mileage_price']:.2f}"})
        
        if rental['breakdown_cover']:
            price_details.append({"label": "Breakdown Cover:", "value": f"£{price['breakdown_cover_price']:.2f}"})
        
        # Add divider
        price_details.append({"label": "", "value": ""})
        
        # Add total
        price_details.append({"label": "Total Price:", "value": f"£{price['total_price']:.2f}"})
        
        # Create price detail rows
        for idx, detail in enumerate(price_details):
            # If empty row, add a separator
            if not detail["label"] and not detail["value"]:
                separator = ttk.Separator(self.price_frame, orient="horizontal")
                separator.grid(row=idx, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
                continue
            
            # Use bold font for total
            font = ("Arial", 12, "bold") if "Total" in detail["label"] else ("Arial", 10, "bold")
            foreground = self.app.primary_color if "Total" in detail["label"] else None
            
            label = ttk.Label(
                self.price_frame,
                text=detail["label"],
                font=font,
                foreground=foreground,
                style='TLabel'
            )
            label.grid(row=idx, column=0, padx=(10, 5), pady=5, sticky="w")
            
            value = ttk.Label(
                self.price_frame,
                text=detail["value"],
                font=font,
                foreground=foreground,
                style='TLabel'
            )
            value.grid(row=idx, column=1, padx=5, pady=5, sticky="e")
    
    def create_buttons(self):
        """Create action buttons"""
        self.buttons_frame = ttk.Frame(self, style='TFrame')
        self.buttons_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Back button
        self.back_button = ttk.Button(
            self.buttons_frame,
            text="Back to Form",
            command=self.on_back,
            style='TButton'
        )
        self.back_button.pack(side=tk.LEFT)
        
        # Confirm button
        self.confirm_button = ttk.Button(
            self.buttons_frame,
            text="Confirm Booking",
            command=self.on_confirm,
            style='TButton'
        )
        self.confirm_button.pack(side=tk.RIGHT)
    
    def on_back(self):
        """Handle back button click"""
        self.parent.destroy()
    
    def on_confirm(self):
        """Handle confirm button click"""
        # Call the callback to finalize the booking
        success = self.on_confirm_callback(self.booking_data)
        
        # If successful, close the window
        if success:
            self.parent.destroy() 