"""
Authentication module for staff login
"""

# Fixed credentials as per requirements
VALID_USERNAME = "sta001"
VALID_PASSWORD = "givemethekeys123"

def validate_login(username, password):
    """
    Validate staff login credentials
    
    Args:
        username (str): Staff username
        password (str): Staff password
        
    Returns:
        bool: True if credentials are valid, False otherwise
    """
    return username == VALID_USERNAME and password == VALID_PASSWORD 