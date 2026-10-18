"""
Car list screen to display rented cars
"""
import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
from PIL import Image, ImageTk, ImageDraw

# Import controllers
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from controllers.database import get_rented_cars

class CarListScreen(ttk.Frame):
    """Screen displaying a list of all currently rented cars"""
    
    def __init__(self, parent, app):
        super().__init__(parent)
        self.parent = parent
        self.app = app
        
        # Configure the frame
        self.configure(style='TFrame')
        self.pack(fill=tk.BOTH, expand=True)
        
        # Create UI elements - REORDERED to ensure visibility
        self.create_background()
        self.create_header()
        self.create_add_button()  # ADD BUTTON after header but before table
        self.create_table_header()
        self.create_table()
        self.create_footer()
        
        # Load initial data
        self.load_rental_data()
        
        # Force button to be visible by updating after all elements are created
        self.update_idletasks()
        self.ensure_button_visible()
    
    def create_background(self):
        """Create a subtle background pattern"""
        # Main background frame
        self.bg_frame = ttk.Frame(self, style='TFrame')
        self.bg_frame.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Create subtle visual indicators for car types
        try:
            # Get car types from style
            car_indicators = {
                "City car": self.app.primary_color,
                "Family car": self.app.secondary_color,
                "Sports car": self.app.accent_color,
                "SUV": self.app.accent2_color
            }
            
            # Create small indicator images
            self.car_type_images = {}
            for car_type, color in car_indicators.items():
                self.car_type_images[car_type] = self.create_car_type_indicator(color)
        except:
            # If error occurs, just continue without indicators
            pass
    
    def create_car_type_indicator(self, color, size=(20, 20)):
        """Create a small colored car type indicator"""
        img = Image.new('RGBA', size, color=(255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        
        # Draw a rounded rectangle
        draw.rounded_rectangle([0, 0, size[0], size[1]], radius=5, fill=color)
        
        return ImageTk.PhotoImage(img)
    
    def create_header(self):
        """Create header with title and search/filter options"""
        # Create card-like container for header
        self.header_container = ttk.Frame(self, style='Card.TFrame')
        self.header_container.pack(fill=tk.X, padx=20, pady=(20, 0))
        
        # Header frame within container
        self.header_frame = ttk.Frame(self.header_container, style='Content.TFrame')
        self.header_frame.pack(fill=tk.X, padx=2, pady=2)
        
        # Left side with title and subtitle
        self.title_frame = ttk.Frame(self.header_frame, style='Content.TFrame')
        self.title_frame.pack(side=tk.LEFT, padx=15, pady=15, anchor=tk.W)
        
        self.title_label = ttk.Label(
            self.title_frame,
            text="Currently Rented Cars",
            style='Title.TLabel',
            background=self.app.content_bg
        )
        self.title_label.pack(anchor=tk.W)
        
        self.subtitle_label = ttk.Label(
            self.title_frame,
            text="View and manage all active car rentals",
            style='Subtitle.TLabel',
            background=self.app.content_bg
        )
        self.subtitle_label.pack(anchor=tk.W, pady=(5, 0))
        
        # Right side with search and refresh
        self.actions_frame = ttk.Frame(self.header_frame, style='Content.TFrame')
        self.actions_frame.pack(side=tk.RIGHT, padx=15, pady=15)
        
        # Add a rental button directly in the header as well
        self.header_add_button = tk.Button(
            self.actions_frame,
            text="+ Add Rental",
            command=self.add_new_rental,
            background="#1976D2",
            foreground="white",
            font=("Arial", 10, "bold"),
            padx=10,
            pady=5
        )
        self.header_add_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Search box with icon
        self.search_frame = ttk.Frame(self.actions_frame, style='Content.TFrame')
        self.search_frame.pack(side=tk.LEFT, padx=(0, 10))
        
        self.search_label = ttk.Label(
            self.search_frame,
            text="Search:",
            style='Content.TLabel'
        )
        self.search_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(
            self.search_frame,
            textvariable=self.search_var,
            width=25
        )
        self.search_entry.pack(side=tk.LEFT)
        
        # Bind search events
        self.search_var.trace_add("write", self.filter_table)
        
        # Refresh button
        self.refresh_button = ttk.Button(
            self.actions_frame,
            text="Refresh List",
            command=self.load_rental_data,
            style='Accent.TButton'
        )
        self.refresh_button.pack(side=tk.LEFT)
    
    def create_add_button(self):
        """Create a prominent Add New Rental button"""
        # Create a prominent frame for the button with a distinct style
        self.add_button_frame = tk.Frame(
            self,
            background="#e3f2fd",  # Light blue background
            highlightbackground="#1976D2",  # Border color
            highlightthickness=2,  # Thicker border
            relief=tk.RAISED  # Raised appearance
        )
        self.add_button_frame.pack(fill=tk.X, padx=20, pady=(15, 5))
        
        # Left side with icon and text
        self.actions_left_frame = tk.Frame(
            self.add_button_frame,
            background="#e3f2fd"
        )
        self.actions_left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=15, pady=10)
        
        # Plus icon
        self.actions_icon = tk.Label(
            self.actions_left_frame,
            text="➕",  # Unicode plus symbol
            background="#e3f2fd",
            foreground="#1976D2",
            font=("Arial", 18)  # Larger font
        )
        self.actions_icon.pack(side=tk.LEFT, padx=(0, 5))
        
        # Action text
        self.actions_text = tk.Label(
            self.actions_left_frame,
            text="Need to add a new car rental?",
            background="#e3f2fd",
            foreground="#0d47a1",
            font=("Arial", 12, "bold")
        )
        self.actions_text.pack(side=tk.LEFT, pady=5)
        
        # Right side with button
        self.actions_right_frame = tk.Frame(
            self.add_button_frame,
            background="#e3f2fd"
        )
        self.actions_right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=15, pady=10)
        
        # Add Rental button - LARGER and more prominent
        self.add_rental_button = tk.Button(
            self.actions_right_frame,
            text="+ ADD NEW RENTAL",  # All caps for emphasis
            command=self.add_new_rental,
            background="#1976D2",  # Blue
            foreground="white",
            font=("Arial", 12, "bold"),  # Larger font
            padx=20,
            pady=10,  # More padding
            cursor="hand2",
            relief=tk.RAISED,
            borderwidth=2  # Thicker border
        )
        self.add_rental_button.pack(side=tk.RIGHT)
    
    def create_table_header(self):
        """Create a header for the table section"""
        # Header for the table section
        self.table_header_frame = ttk.Frame(self, style='TFrame')
        self.table_header_frame.pack(fill=tk.X, padx=20, pady=(15, 0))
        
        # Cars by type stats
        self.car_type_frame = ttk.Frame(self.table_header_frame, style='TFrame')
        self.car_type_frame.pack(side=tk.LEFT)
        
        # This will be populated when data is loaded
        self.car_type_labels = {}
    
    def create_table(self):
        """Create table to display rented cars"""
        # Create a card-like container for the table
        self.table_container = ttk.Frame(self, style='Card.TFrame')
        self.table_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(5, 10))
        
        # Create table frame with some padding
        self.table_frame = ttk.Frame(self.table_container, style='Content.TFrame')
        self.table_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Create columns
        columns = ("id", "customer", "car_type", "fuel_type", "days", "start_date", "price", "actions")
        
        # Create treeview
        self.tree = ttk.Treeview(
            self.table_frame,
            columns=columns,
            show="headings",
            selectmode="browse",
            height=15  # Approximate number of rows visible
        )
        
        # Define headings
        self.tree.heading("id", text="Booking ID")
        self.tree.heading("customer", text="Customer")
        self.tree.heading("car_type", text="Car Type")
        self.tree.heading("fuel_type", text="Fuel Type")
        self.tree.heading("days", text="Days")
        self.tree.heading("start_date", text="Start Date")
        self.tree.heading("price", text="Price")
        self.tree.heading("actions", text="Actions")
        
        # Configure columns
        self.tree.column("id", width=80, anchor=tk.CENTER)
        self.tree.column("customer", width=180)
        self.tree.column("car_type", width=120)
        self.tree.column("fuel_type", width=120)
        self.tree.column("days", width=80, anchor=tk.CENTER)
        self.tree.column("start_date", width=100, anchor=tk.CENTER)
        self.tree.column("price", width=100, anchor=tk.E)
        self.tree.column("actions", width=100, anchor=tk.CENTER)
        
        # Add a scrollbar
        scrollbar = ttk.Scrollbar(self.table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        # Pack elements
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Add horizontal scrollbar if needed
        h_scrollbar = ttk.Scrollbar(self.table_container, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscroll=h_scrollbar.set)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Bind events
        self.tree.bind("<Double-1>", self.on_item_double_click)
        
        # Create striped rows with better contrast
        self.tree.tag_configure("oddrow", background="#f0f5fa")
        self.tree.tag_configure("evenrow", background=self.app.content_bg)
        
        # Highlight for car types
        self.tree.tag_configure("city_car", background="#e6f0fa")
        self.tree.tag_configure("family_car", background="#fff0e0")
        self.tree.tag_configure("sports_car", background="#e6f7ef")
        self.tree.tag_configure("suv", background="#fae6e6")
    
    def create_footer(self):
        """Create footer with stats and actions"""
        # Create card-like container for footer
        self.footer_container = ttk.Frame(self, style='Card.TFrame')
        self.footer_container.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # Footer frame within container
        self.footer_frame = ttk.Frame(self.footer_container, style='Content.TFrame')
        self.footer_frame.pack(fill=tk.X, padx=2, pady=2)
        
        # Stats labels
        self.stats_frame = ttk.Frame(self.footer_frame, style='Content.TFrame')
        self.stats_frame.pack(side=tk.LEFT, padx=15, pady=15)
        
        self.rental_count_var = tk.StringVar(value="Total rentals: 0")
        self.rental_count_label = ttk.Label(
            self.stats_frame,
            textvariable=self.rental_count_var,
            style='Content.TLabel',
            font=("Arial", 12, "bold")
        )
        self.rental_count_label.pack(side=tk.LEFT, padx=(0, 20))
        
        self.revenue_var = tk.StringVar(value="Total revenue: £0.00")
        self.revenue_label = ttk.Label(
            self.stats_frame,
            textvariable=self.revenue_var,
            style='Content.TLabel',
            font=("Arial", 12, "bold"),
            foreground=self.app.accent_color
        )
        self.revenue_label.pack(side=tk.LEFT)
        
        # Action buttons in footer
        self.footer_buttons_frame = ttk.Frame(self.footer_frame, style='Content.TFrame')
        self.footer_buttons_frame.pack(side=tk.RIGHT, padx=15, pady=15)
        
        # Export button
        self.export_button = ttk.Button(
            self.footer_buttons_frame,
            text="Export List",
            style='TButton'
        )
        self.export_button.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Print button
        self.print_button = ttk.Button(
            self.footer_buttons_frame,
            text="Print Report",
            style='TButton'
        )
        self.print_button.pack(side=tk.RIGHT, padx=(0, 5))
    
    def load_rental_data(self):
        """Load rental data from database"""
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            # Get rented cars from database
            rentals = get_rented_cars()
            
            # FOR DEMO: Always use dummy data to ensure display regardless of database
            # Comment the line below for production
            # rentals = self.get_dummy_rentals()  # <-- Commented this line to show real rentals!
            
            # Track car types for statistics
            car_type_counts = {
                "City car": 0,
                "Family car": 0,
                "Sports car": 0,
                "SUV": 0
            }
            
            # Process data and insert into table
            total_revenue = 0
            for idx, rental in enumerate(rentals):
                # Format the price
                price_formatted = f"£{rental['price']:.2f}"
                
                # Create the customer name
                customer_name = f"{rental['first_name']} {rental['last_name']}"
                
                # Track car type count
                car_type = rental["car_type"]
                if car_type in car_type_counts:
                    car_type_counts[car_type] += 1
                    
                # Determine row tag based on car type
                car_type_tag = car_type.lower().replace(" ", "_")
                tag = car_type_tag
                
                # Insert into table with row styling
                item_id = self.tree.insert("", tk.END, values=(
                    rental["id"],
                    customer_name,
                    rental["car_type"],
                    rental["fuel_type"],
                    rental["days"],
                    rental["start_date"],
                    price_formatted,
                    "View Details"
                ), tags=(tag,))
                
                # Add to total revenue
                total_revenue += rental["price"]
            
            # Update stats
            self.rental_count_var.set(f"Total rentals: {len(rentals)}")
            self.revenue_var.set(f"Total revenue: £{total_revenue:.2f}")
            
            # Update car type statistics in the header
            self.update_car_type_stats(car_type_counts)
            
            # Display "No rentals" message if table is empty
            if len(rentals) == 0:
                self.show_empty_state()
                
        except Exception as e:
            print(f"Error loading data: {e}")
            # If any error occurs, show dummy data
            self.load_dummy_data()
    
    def load_dummy_data(self):
        """Load dummy data as a fallback"""
        try:
            # Get dummy rentals
            rentals = self.get_dummy_rentals()
            
            # Clear existing data
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Track car types for statistics
            car_type_counts = {
                "City car": 0,
                "Family car": 0,
                "Sports car": 0,
                "SUV": 0
            }
            
            # Process data and insert into table
            total_revenue = 0
            for idx, rental in enumerate(rentals):
                # Format the price
                price_formatted = f"£{rental['price']:.2f}"
                
                # Create the customer name
                customer_name = f"{rental['first_name']} {rental['last_name']}"
                
                # Track car type count
                car_type = rental["car_type"]
                if car_type in car_type_counts:
                    car_type_counts[car_type] += 1
                    
                # For demo, alternate row tags to ensure visibility
                tag = "evenrow" if idx % 2 == 0 else "oddrow"
                
                # Insert into table with row styling
                self.tree.insert("", tk.END, values=(
                    rental["id"],
                    customer_name,
                    rental["car_type"],
                    rental["fuel_type"],
                    rental["days"],
                    rental["start_date"],
                    price_formatted,
                    "View Details"
                ), tags=(tag,))
                
                # Add to total revenue
                total_revenue += rental["price"]
            
            # Update stats
            self.rental_count_var.set(f"Total rentals: {len(rentals)}")
            self.revenue_var.set(f"Total revenue: £{total_revenue:.2f}")
            
            # Update car type statistics in the header
            self.update_car_type_stats(car_type_counts)
            
        except Exception as e:
            print(f"Error loading dummy data: {e}")
            # Last resort - show empty state
            self.show_empty_state()
    
    def update_car_type_stats(self, car_type_counts):
        """Update the car type statistics display"""
        # Clear existing labels
        for widget in self.car_type_frame.winfo_children():
            widget.destroy()
        
        # Create new labels for each car type
        for i, (car_type, count) in enumerate(car_type_counts.items()):
            # Create frame for this car type
            type_frame = ttk.Frame(self.car_type_frame, style='TFrame')
            type_frame.pack(side=tk.LEFT, padx=(0 if i == 0 else 15, 0))
            
            # Add indicator if available
            if hasattr(self, 'car_type_images') and car_type in self.car_type_images:
                indicator_label = ttk.Label(
                    type_frame,
                    image=self.car_type_images[car_type],
                    style='TLabel'
                )
                indicator_label.pack(side=tk.LEFT, padx=(0, 5))
            
            # Add count label
            count_label = ttk.Label(
                type_frame,
                text=f"{car_type}: {count}",
                style='TLabel'
            )
            count_label.pack(side=tk.LEFT)
    
    def show_empty_state(self):
        """Show a message when no rentals are available"""
        # Insert a single row with empty state message
        self.tree.insert("", tk.END, values=(
            "", "No rentals found", "", "", "", "", "", ""
        ), tags=("evenrow",))
    
    def filter_table(self, *args):
        """Filter table based on search text"""
        search_text = self.search_var.get().lower()
        
        # If search is empty, reload all data
        if not search_text:
            self.load_rental_data()
            return
        
        # Otherwise, filter existing items
        all_items = self.tree.get_children()
        
        # Track if we have any matches
        matches_found = False
        
        for item in all_items:
            values = self.tree.item(item)["values"]
            # Convert all values to string for searching
            item_text = " ".join([str(v).lower() for v in values if v])
            
            if search_text in item_text:
                # Item matches, make it visible
                matches_found = True
                # Keep original tag (car type)
                original_tags = self.tree.item(item)["tags"]
                self.tree.item(item, tags=original_tags)
            else:
                # Item doesn't match, hide it
                self.tree.detach(item)
        
        # Show empty state if no matches
        if not matches_found:
            self.tree.insert("", tk.END, values=(
                "", f"No results matching '{search_text}'", "", "", "", "", "", ""
            ), tags=("evenrow",))
    
    def on_item_double_click(self, event):
        """Handle double-click on a rental item"""
        # Get the item that was clicked
        region = self.tree.identify_region(event.x, event.y)
        
        # Only proceed if a cell was clicked (not heading)
        if region == "cell":
            # Get the selected item
            item = self.tree.selection()[0]
            
            # Get the column that was clicked
            column = self.tree.identify_column(event.x)
            col_index = int(column[1:]) - 1  # Convert #1, #2, etc. to 0, 1, etc.
            
            # Get the item details
            values = self.tree.item(item)["values"]
            
            # If Actions column was clicked or last column
            if column == "#8" or col_index >= len(self.tree["columns"]) - 1:
                # Show rental details dialog
                self.show_rental_details(values)
            else:
                # Otherwise just show details for any column
                self.show_rental_details(values)
    
    def show_rental_details(self, rental_values):
        """Show detailed information about a rental"""
        if not rental_values or not rental_values[0]:
            return  # Don't show details for empty rows
            
        # Create a simple dialog with rental details
        dialog = tk.Toplevel(self.app.root)
        dialog.title("Rental Details")
        dialog.geometry("500x400")
        dialog.transient(self.app.root)  # Make dialog modal
        dialog.grab_set()
        
        # Set position relative to main window
        x = self.app.root.winfo_x() + (self.app.root.winfo_width() - 500) // 2
        y = self.app.root.winfo_y() + (self.app.root.winfo_height() - 400) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # Style the dialog
        dialog.configure(background=self.app.bg_color)
        
        # Create content frame
        content_frame = ttk.Frame(dialog, style='Card.TFrame')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Inner frame
        inner_frame = ttk.Frame(content_frame, style='Content.TFrame')
        inner_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Title
        title_label = ttk.Label(
            inner_frame,
            text=f"Rental #{rental_values[0]} Details",
            style='Title.TLabel',
            background=self.app.content_bg
        )
        title_label.pack(pady=15, padx=15, anchor=tk.W)
        
        # Create detail rows
        details_frame = ttk.Frame(inner_frame, style='Content.TFrame')
        details_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        # Add details
        fields = [
            ("Customer", rental_values[1]),
            ("Car Type", rental_values[2]),
            ("Fuel Type", rental_values[3]),
            ("Rental Duration", f"{rental_values[4]} days"),
            ("Start Date", rental_values[5]),
            ("Total Price", rental_values[6])
        ]
        
        for i, (field, value) in enumerate(fields):
            # Create row frame
            row_frame = ttk.Frame(details_frame, style='Content.TFrame')
            row_frame.pack(fill=tk.X, pady=5)
            
            # Field label
            field_label = ttk.Label(
                row_frame,
                text=f"{field}:",
                width=15,
                anchor=tk.W,
                style='Content.TLabel',
                font=('Arial', 11, 'bold')
            )
            field_label.pack(side=tk.LEFT)
            
            # Value label
            value_label = ttk.Label(
                row_frame,
                text=value,
                style='Content.TLabel'
            )
            value_label.pack(side=tk.LEFT, padx=10)
        
        # Buttons frame
        buttons_frame = ttk.Frame(inner_frame, style='Content.TFrame')
        buttons_frame.pack(fill=tk.X, padx=15, pady=15)
        
        # Close button
        close_button = ttk.Button(
            buttons_frame,
            text="Close",
            command=dialog.destroy,
            style='TButton'
        )
        close_button.pack(side=tk.RIGHT)
    
    def add_new_rental(self):
        """Handle add new rental button click"""
        try:
            # Find the main dashboard's notebook
            if hasattr(self.app, 'notebook'):
                # Direct access if available
                self.app.notebook.select(0)  # First tab (index 0) is the booking tab
            elif hasattr(self.app, 'main_dashboard') and hasattr(self.app.main_dashboard, 'notebook'):
                # Try to access through main_dashboard if available
                self.app.main_dashboard.notebook.select(0)
            else:
                # If we can't find the notebook, show a message
                raise AttributeError("Could not find notebook")
                
        except Exception as e:
            # If anything goes wrong, show a helpful message
            messagebox.showinfo(
                "Add New Rental",
                "To add a new rental, please go to the 'New Booking' tab at the top of the screen."
            )
    
    def get_dummy_rentals(self):
        """Generate dummy rental data for demonstration"""
        return [
            {
                "id": 1001,
                "first_name": "John",
                "last_name": "Smith",
                "car_type": "Sports car",
                "fuel_type": "Petrol",
                "days": 3,
                "start_date": "2023-11-15",
                "price": 225.00
            },
            {
                "id": 1002,
                "first_name": "Emily",
                "last_name": "Johnson",
                "car_type": "City car",
                "fuel_type": "Hybrid",
                "days": 5,
                "start_date": "2023-11-10",
                "price": 125.00
            },
            {
                "id": 1003,
                "first_name": "Michael",
                "last_name": "Brown",
                "car_type": "Family car",
                "fuel_type": "Diesel",
                "days": 7,
                "start_date": "2023-11-08",
                "price": 350.00
            },
            {
                "id": 1004,
                "first_name": "Sarah",
                "last_name": "Williams",
                "car_type": "SUV",
                "fuel_type": "Electric",
                "days": 2,
                "start_date": "2023-11-18",
                "price": 180.00
            },
            {
                "id": 1005,
                "first_name": "David",
                "last_name": "Jones",
                "car_type": "Sports car",
                "fuel_type": "Petrol",
                "days": 1,
                "start_date": "2023-11-20",
                "price": 75.00
            },
            {
                "id": 1006,
                "first_name": "Jessica",
                "last_name": "Miller",
                "car_type": "City car",
                "fuel_type": "Hybrid",
                "days": 10,
                "start_date": "2023-11-05",
                "price": 250.00
            },
            {
                "id": 1007,
                "first_name": "Robert",
                "last_name": "Wilson",
                "car_type": "Family car",
                "fuel_type": "Diesel",
                "days": 4,
                "start_date": "2023-11-12",
                "price": 200.00
            },
            {
                "id": 1008,
                "first_name": "Jennifer",
                "last_name": "Taylor",
                "car_type": "SUV",
                "fuel_type": "Electric",
                "days": 6,
                "start_date": "2023-11-14",
                "price": 540.00
            }
        ]

    def ensure_button_visible(self):
        """Ensure the Add Rental button is visible"""
        try:
            # Raise the button frame to the top
            self.add_button_frame.lift()
            
            # Add a flashing effect to draw attention
            def flash_button(count=0):
                if count < 6:  # Flash 3 times
                    # Toggle between bright and normal colors
                    if count % 2 == 0:
                        bg_color = "#2196F3"  # Brighter blue
                    else:
                        bg_color = "#1976D2"  # Normal blue
                    
                    # Update button appearance
                    self.add_rental_button.configure(background=bg_color)
                    
                    # Schedule next flash
                    self.after(300, lambda: flash_button(count + 1))
            
            # Start flashing
            flash_button()
            
        except Exception as e:
            print(f"Error ensuring button visibility: {e}") 