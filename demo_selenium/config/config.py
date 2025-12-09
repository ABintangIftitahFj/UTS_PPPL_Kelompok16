"""
Configuration file for Selenium tests
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Test configuration"""
    BASE_URL = os.getenv('BASE_URL', 'https://mathsteam.id')
    BROWSER = os.getenv('BROWSER', 'chrome')
    HEADLESS = os.getenv('HEADLESS', 'False').lower() == 'true'
    IMPLICIT_WAIT = int(os.getenv('IMPLICIT_WAIT', '10'))
    EXPLICIT_WAIT = int(os.getenv('EXPLICIT_WAIT', '20'))
    
    # Test credentials (if needed)
    TEST_USERNAME = os.getenv('TEST_USERNAME', '')
    TEST_PASSWORD = os.getenv('TEST_PASSWORD', '')