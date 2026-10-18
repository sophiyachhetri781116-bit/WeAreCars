"""
Input validation for the car rental application
"""
import re

def validate_name(name):
    """
    Validate a person's name
    
    Args:
        name (str): Name to validate
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not name or not name.strip():
        return False, "Name cannot be empty"
    
    if len(name.strip()) < 2:
        return False, "Name must be at least 2 characters"
        
    if not re.match(r"^[A-Za-z \-']+$", name):
        return False, "Name can only contain letters, spaces, hyphens, and apostrophes"
    
    return True, ""

def validate_address(address):
    """
    Validate an address
    
    Args:
        address (str): Address to validate
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not address or not address.strip():
        return False, "Address cannot be empty"
    
    if len(address.strip()) < 5:
        return False, "Address must be at least 5 characters"
    
    return True, ""

def validate_age(age_str):
    """
    Validate customer age
    
    Args:
        age_str (str): Age as string to validate
        
    Returns:
        tuple: (is_valid, error_message, age_int)
    """
    try:
        age = int(age_str)
        if age < 18:
            return False, "Customer must be at least 18 years old", None
        if age > 120:
            return False, "Please enter a valid age", None
        return True, "", age
    except ValueError:
        return False, "Age must be a number", None

def validate_days(days_str):
    """
    Validate rental days
    
    Args:
        days_str (str): Number of days as string to validate
        
    Returns:
        tuple: (is_valid, error_message, days_int)
    """
    try:
        days = int(days_str)
        if days < 1:
            return False, "Minimum rental period is 1 day", None
        if days > 28:
            return False, "Maximum rental period is 28 days", None
        return True, "", days
    except ValueError:
        return False, "Number of days must be a number", None 