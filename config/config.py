"""
Configuration settings for MathsTeam regression testing
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for test settings"""
    
    # Base URL
    BASE_URL = os.getenv('BASE_URL', 'https://mathsteam.id/')
    
    # Login credentials
    LOGIN_EMAIL = os.getenv('LOGIN_EMAIL', 'admin@tes.com')
    LOGIN_PASSWORD = os.getenv('LOGIN_PASSWORD', '12345678')
    
    # Browser settings
    BROWSER = os.getenv('BROWSER', 'chrome').lower()
    HEADLESS = os.getenv('HEADLESS', 'false').lower() == 'true'
    
    # Wait times
    IMPLICIT_WAIT = int(os.getenv('IMPLICIT_WAIT', '10'))
    EXPLICIT_WAIT = int(os.getenv('EXPLICIT_WAIT', '20'))
    
    # Test settings
    SCREENSHOTS_ON_FAILURE = os.getenv('SCREENSHOTS_ON_FAILURE', 'true').lower() == 'true'
    REPORT_FORMAT = os.getenv('REPORT_FORMAT', 'html')
    
    # Paths
    SCREENSHOTS_PATH = os.path.join(os.getcwd(), 'reports', 'screenshots')
    REPORTS_PATH = os.path.join(os.getcwd(), 'reports')
    
    @classmethod
    def create_directories(cls):
        """Create necessary directories"""
        os.makedirs(cls.SCREENSHOTS_PATH, exist_ok=True)
        os.makedirs(cls.REPORTS_PATH, exist_ok=True)