"""
Dashboard/Home Page Object for MathsTeam website
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.config import Config

class DashboardPage(BasePage):
    """Dashboard page object with navigation and content verification"""
    
    # Page URL
    DASHBOARD_URL = f"{Config.BASE_URL}dashboard"
    HOME_URL = Config.BASE_URL
    
    # Navigation elements
    NAVBAR = (By.CSS_SELECTOR, ".navbar, nav")
    LOGO = (By.CSS_SELECTOR, ".logo, .brand, img[alt*='logo']")
    MENU_ITEMS = (By.CSS_SELECTOR, ".nav-item, .menu-item, .navbar-nav li")
    
    # Main content elements
    MAIN_CONTENT = (By.CSS_SELECTOR, "main, .main-content, .content")
    PAGE_TITLE = (By.CSS_SELECTOR, "h1, .page-title, .dashboard-title")
    WELCOME_MESSAGE = (By.CSS_SELECTOR, ".welcome, .greeting")
    
    # User-related elements
    USER_PROFILE = (By.CSS_SELECTOR, ".user-profile, .profile-dropdown, .user-menu")
    USER_NAME = (By.CSS_SELECTOR, ".user-name, .username, .profile-name")
    LOGOUT_LINK = (By.XPATH, "//a[contains(text(), 'Logout')] | //button[contains(text(), 'Logout')] | //a[contains(text(), 'Keluar')]")
    
    # Common navigation links
    HOME_LINK = (By.XPATH, "//a[contains(text(), 'Home')] | //a[contains(text(), 'Beranda')]")
    PROFILE_LINK = (By.XPATH, "//a[contains(text(), 'Profile')] | //a[contains(text(), 'Profil')]")
    SETTINGS_LINK = (By.XPATH, "//a[contains(text(), 'Settings')] | //a[contains(text(), 'Pengaturan')]")
    
    # Content sections
    CARDS = (By.CSS_SELECTOR, ".card, .widget, .panel")
    STATISTICS = (By.CSS_SELECTOR, ".stat, .statistic, .metric")
    CHARTS = (By.CSS_SELECTOR, ".chart, .graph, canvas")
    
    # Footer
    FOOTER = (By.CSS_SELECTOR, "footer, .footer")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def navigate_to_dashboard(self):
        """Navigate to dashboard page"""
        self.navigate_to(self.DASHBOARD_URL)
        self.wait_for_page_to_load()
    
    def navigate_to_home(self):
        """Navigate to home page"""
        self.navigate_to(self.HOME_URL)
        self.wait_for_page_to_load()
    
    def is_on_dashboard(self):
        """
        Check if currently on dashboard/home page
        
        Returns:
            bool: True if on dashboard page
        """
        current_url = self.get_current_url()
        
        # Check URL patterns
        if any(pattern in current_url.lower() for pattern in ['dashboard', 'home', 'beranda']):
            return True
        
        # Check if we're on the base URL (home page)
        if current_url.rstrip('/') == Config.BASE_URL.rstrip('/'):
            return True
        
        # Check for dashboard-specific elements
        if self.is_element_visible(self.PAGE_TITLE, timeout=5):
            return True
        
        return False
    
    def get_page_title_text(self):
        """
        Get the main page title text
        
        Returns:
            str: Page title text or None if not found
        """
        try:
            return self.get_text(self.PAGE_TITLE, timeout=5)
        except:
            return None
    
    def get_welcome_message(self):
        """
        Get welcome message text
        
        Returns:
            str: Welcome message or None if not found
        """
        try:
            return self.get_text(self.WELCOME_MESSAGE, timeout=5)
        except:
            return None
    
    def get_user_name(self):
        """
        Get logged-in user name
        
        Returns:
            str: User name or None if not found
        """
        try:
            return self.get_text(self.USER_NAME, timeout=5)
        except:
            return None
    
    def is_navbar_present(self):
        """
        Check if navigation bar is present
        
        Returns:
            bool: True if navbar is present
        """
        return self.is_element_visible(self.NAVBAR, timeout=5)
    
    def is_logo_present(self):
        """
        Check if logo is present
        
        Returns:
            bool: True if logo is present
        """
        return self.is_element_visible(self.LOGO, timeout=5)
    
    def get_menu_items(self):
        """
        Get all navigation menu items
        
        Returns:
            list: List of menu item texts
        """
        try:
            menu_elements = self.find_elements(self.MENU_ITEMS, timeout=5)
            return [item.text.strip() for item in menu_elements if item.text.strip()]
        except:
            return []
    
    def get_cards_count(self):
        """
        Count number of cards/widgets on the page
        
        Returns:
            int: Number of cards found
        """
        cards = self.find_elements(self.CARDS, timeout=5)
        return len(cards)
    
    def click_home_link(self):
        """Click home navigation link"""
        try:
            self.click_element(self.HOME_LINK)
            self.wait_for_page_to_load()
            return True
        except:
            return False
    
    def click_profile_link(self):
        """Click profile navigation link"""
        try:
            self.click_element(self.PROFILE_LINK)
            self.wait_for_page_to_load()
            return True
        except:
            return False
    
    def click_settings_link(self):
        """Click settings navigation link"""
        try:
            self.click_element(self.SETTINGS_LINK)
            self.wait_for_page_to_load()
            return True
        except:
            return False
    
    def logout(self):
        """
        Logout from the application
        
        Returns:
            bool: True if logout was successful
        """
        try:
            self.click_element(self.LOGOUT_LINK)
            self.wait_for_page_to_load()
            return True
        except:
            return False
    
    def is_user_logged_in(self):
        """
        Check if user is logged in by looking for user-specific elements
        
        Returns:
            bool: True if user appears to be logged in
        """
        # Check for user profile elements
        if self.is_element_visible(self.USER_PROFILE, timeout=5):
            return True
        
        # Check for logout link
        if self.is_element_visible(self.LOGOUT_LINK, timeout=5):
            return True
        
        # Check if we're not on login page
        current_url = self.get_current_url()
        if "login" not in current_url.lower():
            return True
        
        return False
    
    def verify_page_loaded(self):
        """
        Verify that the dashboard page has loaded properly
        
        Returns:
            bool: True if page appears to be loaded correctly
        """
        checks = [
            self.is_navbar_present(),
            self.is_element_visible(self.MAIN_CONTENT, timeout=10),
            self.get_page_title() != ""  # Page has a title
        ]
        
        return any(checks)  # At least one check should pass