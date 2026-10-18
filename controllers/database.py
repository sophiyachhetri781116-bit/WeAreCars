import sqlite3
import os

DATABASE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "wearecars.db")

def get_connection():
    """Get a connection to the SQLite database"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # Enable row factory for easier column access
    return conn

def initialize_database():
    """Initialize the database with required tables if they don't exist"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create customers table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        address TEXT NOT NULL,
        age INTEGER NOT NULL,
        has_license BOOLEAN NOT NULL
    )
    ''')
    
    # Create cars table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cars (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        car_type TEXT NOT NULL,
        fuel_type TEXT NOT NULL,
        status TEXT DEFAULT 'available'
    )
    ''')
    
    # Create bookings table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        car_id INTEGER NOT NULL,
        days INTEGER NOT NULL,
        unlimited_mileage BOOLEAN DEFAULT 0,
        breakdown_cover BOOLEAN DEFAULT 0,
        start_date TEXT NOT NULL,
        price REAL NOT NULL,
        status TEXT DEFAULT 'active',
        FOREIGN KEY (customer_id) REFERENCES customers (id),
        FOREIGN KEY (car_id) REFERENCES cars (id)
    )
    ''')
    
    # Insert sample car data if table is empty
    cursor.execute("SELECT COUNT(*) FROM cars")
    if cursor.fetchone()[0] == 0:
        car_data = [
            ('City car', 'Petrol'), 
            ('City car', 'Diesel'), 
            ('City car', 'Hybrid'), 
            ('City car', 'Full electric'),
            ('Family car', 'Petrol'), 
            ('Family car', 'Diesel'), 
            ('Family car', 'Hybrid'), 
            ('Family car', 'Full electric'),
            ('Sports car', 'Petrol'), 
            ('Sports car', 'Diesel'), 
            ('Sports car', 'Hybrid'), 
            ('Sports car', 'Full electric'),
            ('SUV', 'Petrol'), 
            ('SUV', 'Diesel'), 
            ('SUV', 'Hybrid'), 
            ('SUV', 'Full electric')
        ]
        cursor.executemany("INSERT INTO cars (car_type, fuel_type) VALUES (?, ?)", car_data)
    
    conn.commit()
    conn.close()
    
def get_available_cars():
    """Get a list of all available cars"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cars WHERE status = 'available'")
    cars = cursor.fetchall()
    conn.close()
    return cars

# Global storage for demo rentals
DEMO_RENTALS = [
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
    }
]

def get_rented_cars():
    """Get all currently rented cars"""
    # In a real application, this would query a database
    # For demo, return the global list of demo rentals
    return DEMO_RENTALS

def add_new_rental(customer_data, rental_data):
    """Add a new rental to the demo data"""
    # Generate a new ID (increment from the highest existing ID)
    new_id = max([r["id"] for r in DEMO_RENTALS]) + 1
    
    # Create a new rental entry
    new_rental = {
        "id": new_id,
        "first_name": customer_data["first_name"],
        "last_name": customer_data["last_name"],
        "car_type": rental_data["car_type"],
        "fuel_type": rental_data["fuel_type"],
        "days": rental_data["days"],
        "start_date": rental_data["start_date"],
        "price": rental_data["price"]
    }
    
    # Add to the global list
    DEMO_RENTALS.insert(0, new_rental)  # Add at the beginning to show newest first
    
    return new_id

def add_customer(first_name, last_name, address, age, has_license):
    """Add a new customer to the database"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO customers (first_name, last_name, address, age, has_license)
    VALUES (?, ?, ?, ?, ?)
    """, (first_name, last_name, address, age, has_license))
    customer_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return customer_id

def add_booking(customer_id, car_id, days, unlimited_mileage, breakdown_cover, start_date, price):
    """Add a new booking to the database"""
    # In a demo application, we'll simulate adding to a database
    # by printing to console for demonstration
    print(f"Adding booking: Customer #{customer_id}, Car #{car_id}, {days} days, £{price}")
    
    # For demonstration, return a booking ID
    return 2000 