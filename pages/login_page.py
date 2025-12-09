"""
Login Page Object for MathsTeam website
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.config import Config

class LoginPage(BasePage):
    """Login page object with all login-related functionality"""
    
    # Page URL
    LOGIN_URL = f"{Config.BASE_URL}login"
    
    # Locators
    EMAIL_INPUT = (By.NAME, "email")
    PASSWORD_INPUT = (By.NAME, "password")
    LOGIN_BUTTON = (By.XPATH, "//button[@type='submit']")
    
    # Alternative selectors in case the above don't work
    EMAIL_INPUT_ALT = (By.ID, "email")
    PASSWORD_INPUT_ALT = (By.ID, "password")
    LOGIN_BUTTON_ALT = (By.CSS_SELECTOR, "input[type='submit']")
    LOGIN_BUTTON_ALT2 = (By.CSS_SELECTOR, ".btn-login")
    
    # Error and success elements
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".alert-danger, .error-message, .invalid-feedback")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".alert-success, .success-message")
    
    # Dashboard elements (to verify successful login)
    DASHBOARD_HEADER = (By.CSS_SELECTOR, "h1, .dashboard-title")
    USER_PROFILE = (By.CSS_SELECTOR, ".user-profile, .profile-dropdown")
    LOGOUT_BUTTON = (By.XPATH, "//a[contains(text(), 'Logout')] | //button[contains(text(), 'Logout')]")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def navigate_to_login(self):
        """Navigate to login page"""
        self.navigate_to(self.LOGIN_URL)
        self.wait_for_page_to_load()
    
    def enter_email(self, email):
        """
        Enter email in the email field
        
        Args:
            email (str): Email address to enter
        """
        try:
            self.send_keys_to_element(self.EMAIL_INPUT, email)
        except:
            # Try alternative locator
            self.send_keys_to_element(self.EMAIL_INPUT_ALT, email)
    
    def enter_password(self, password):
        """
        Enter password in the password field
        
        Args:
            password (str): Password to enter
        """
        try:
            self.send_keys_to_element(self.PASSWORD_INPUT, password)
        except:
            # Try alternative locator
            self.send_keys_to_element(self.PASSWORD_INPUT_ALT, password)
    
    def click_login_button(self):
        """Click the login button"""
        try:
            self.click_element(self.LOGIN_BUTTON)
        except:
            try:
                self.click_element(self.LOGIN_BUTTON_ALT)
            except:
                self.click_element(self.LOGIN_BUTTON_ALT2)
    
    def login(self, email=None, password=None):
        """
        Perform complete login process
        
        Args:
            email (str): Email address (uses config default if None)
            password (str): Password (uses config default if None)
        
        Returns:
            bool: True if login appears successful
        """
        if email is None:
            email = Config.LOGIN_EMAIL
        if password is None:
            password = Config.LOGIN_PASSWORD
        
        self.navigate_to_login()
        self.enter_email(email)
        self.enter_password(password)
        self.click_login_button()
        
        # Wait for page to load after login attempt
        self.wait_for_page_to_load()
        
        # Check if login was successful
        return self.is_login_successful()
    
    def is_login_successful(self):
        """
        Check if login was successful by looking for dashboard elements
        
        Returns:
            bool: True if login was successful
        """
        # Check if we're redirected away from login page
        current_url = self.get_current_url()
        if "login" not in current_url.lower():
            return True
        
        # Check for dashboard elements
        if self.is_element_visible(self.DASHBOARD_HEADER, timeout=5):
            return True
        
        if self.is_element_visible(self.USER_PROFILE, timeout=5):
            return True
        
        if self.is_element_visible(self.LOGOUT_BUTTON, timeout=5):
            return True
        
        return False
    
    def get_error_message(self):
        """
        Get error message if login failed
        
        Returns:
            str: Error message text or None if no error
        """
        try:
            return self.get_text(self.ERROR_MESSAGE, timeout=5)
        except:
            return None
    
    def get_success_message(self):
        """
        Get success message if present
        
        Returns:
            str: Success message text or None if no message
        """
        try:
            return self.get_text(self.SUCCESS_MESSAGE, timeout=5)
        except:
            return None
    
    def logout(self):
        """Logout from the application"""
        try:
            self.click_element(self.LOGOUT_BUTTON)
            self.wait_for_page_to_load()
            return True
        except:
            return False
    
    def is_on_login_page(self):
        """
        Check if currently on login page
        
        Returns:
            bool: True if on login page
        """
        current_url = self.get_current_url()
        return "login" in current_url.lower()
    
    def clear_login_fields(self):
        """Clear both email and password fields"""
        try:
            email_field = self.find_element(self.EMAIL_INPUT)
            email_field.clear()
        except:
            email_field = self.find_element(self.EMAIL_INPUT_ALT)
            email_field.clear()
        
        try:
            password_field = self.find_element(self.PASSWORD_INPUT)
            password_field.clear()
        except:
            password_field = self.find_element(self.PASSWORD_INPUT_ALT)
            password_field.clear()
    
    def verify_page_loaded(self):
        """
        Verify that the login page has loaded properly
        
        Returns:
            bool: True if page appears to be loaded correctly
        """
        checks = [
            self.is_on_login_page(),
            self.is_element_present(self.EMAIL_INPUT) or self.is_element_present(self.EMAIL_INPUT_ALT),
            self.is_element_present(self.PASSWORD_INPUT) or self.is_element_present(self.PASSWORD_INPUT_ALT),
            self.get_page_title() != ""  # Page has a title
        ]
        
        return sum(checks) >= 2  # At least 2 checks should pass