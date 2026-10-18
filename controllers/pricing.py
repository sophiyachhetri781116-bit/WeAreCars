"""
Pricing calculator for car rentals
"""

# Base price per day
BASE_PRICE_PER_DAY = 25

# Car type surcharge
CAR_TYPE_SURCHARGES = {
    "City car": 0,
    "Family car": 50,
    "Sports car": 75,
    "SUV": 65
}

# Fuel type surcharge
FUEL_TYPE_SURCHARGES = {
    "Petrol": 0,
    "Diesel": 0,
    "Hybrid": 30,
    "Full electric": 50
}

# Optional extras
UNLIMITED_MILEAGE_PRICE_PER_DAY = 10
BREAKDOWN_COVER_PRICE_PER_DAY = 2

def calculate_rental_price(days, car_type, fuel_type, unlimited_mileage=False, breakdown_cover=False):
    """
    Calculate the total rental price based on selected options
    
    Args:
        days (int): Number of rental days
        car_type (str): Type of car (City car, Family car, Sports car, SUV)
        fuel_type (str): Type of fuel (Petrol, Diesel, Hybrid, Full electric)
        unlimited_mileage (bool): Whether unlimited mileage is included
        breakdown_cover (bool): Whether breakdown cover is included
        
    Returns:
        dict: Dictionary containing price breakdown and total price
    """
    # Validate inputs
    if not isinstance(days, int) or days < 1 or days > 28:
        raise ValueError("Days must be between 1 and 28")
    
    if car_type not in CAR_TYPE_SURCHARGES:
        raise ValueError(f"Invalid car type: {car_type}")
    
    if fuel_type not in FUEL_TYPE_SURCHARGES:
        raise ValueError(f"Invalid fuel type: {fuel_type}")
    
    # Calculate base price for rental days
    base_price = BASE_PRICE_PER_DAY * days
    
    # Add car type surcharge
    car_type_surcharge = CAR_TYPE_SURCHARGES[car_type]
    
    # Add fuel type surcharge
    fuel_type_surcharge = FUEL_TYPE_SURCHARGES[fuel_type]
    
    # Calculate optional extras
    unlimited_mileage_price = UNLIMITED_MILEAGE_PRICE_PER_DAY * days if unlimited_mileage else 0
    breakdown_cover_price = BREAKDOWN_COVER_PRICE_PER_DAY * days if breakdown_cover else 0
    
    # Calculate total price
    total_price = base_price + car_type_surcharge + fuel_type_surcharge + unlimited_mileage_price + breakdown_cover_price
    
    # Return price breakdown
    return {
        "base_price": base_price,
        "car_type_surcharge": car_type_surcharge,
        "fuel_type_surcharge": fuel_type_surcharge,
        "unlimited_mileage_price": unlimited_mileage_price,
        "breakdown_cover_price": breakdown_cover_price,
        "total_price": total_price
    } 