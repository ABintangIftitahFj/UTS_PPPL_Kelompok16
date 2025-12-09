"""
Base Page class implementing Page Object Model pattern
"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from config.config import Config

class BasePage:
    """Base page class with common functionality"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.EXPLICIT_WAIT)
    
    def navigate_to(self, url):
        """Navigate to a specific URL"""
        self.driver.get(url)
    
    def find_element(self, locator, timeout=None):
        """
        Find element with explicit wait
        
        Args:
            locator (tuple): Locator tuple (By.ID, 'element_id')
            timeout (int): Wait timeout, uses default if None
        
        Returns:
            WebElement: Found element
        """
        if timeout:
            wait = WebDriverWait(self.driver, timeout)
        else:
            wait = self.wait
        
        try:
            return wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            raise TimeoutException(f"Element not found: {locator}")
    
    def find_elements(self, locator, timeout=None):
        """
        Find multiple elements with explicit wait
        
        Args:
            locator (tuple): Locator tuple (By.CLASS_NAME, 'class_name')
            timeout (int): Wait timeout, uses default if None
        
        Returns:
            list: List of WebElements
        """
        if timeout:
            wait = WebDriverWait(self.driver, timeout)
        else:
            wait = self.wait
        
        try:
            wait.until(EC.presence_of_element_located(locator))
            return self.driver.find_elements(*locator)
        except TimeoutException:
            return []
    
    def click_element(self, locator, timeout=None):
        """
        Click element with explicit wait for clickability
        
        Args:
            locator (tuple): Locator tuple
            timeout (int): Wait timeout
        """
        if timeout:
            wait = WebDriverWait(self.driver, timeout)
        else:
            wait = self.wait
        
        element = wait.until(EC.element_to_be_clickable(locator))
        element.click()
    
    def send_keys_to_element(self, locator, text, clear_first=True, timeout=None):
        """
        Send keys to element with explicit wait
        
        Args:
            locator (tuple): Locator tuple
            text (str): Text to send
            clear_first (bool): Clear field before typing
            timeout (int): Wait timeout
        """
        element = self.find_element(locator, timeout)
        if clear_first:
            element.clear()
        element.send_keys(text)
    
    def get_text(self, locator, timeout=None):
        """
        Get text from element
        
        Args:
            locator (tuple): Locator tuple
            timeout (int): Wait timeout
        
        Returns:
            str: Element text
        """
        element = self.find_element(locator, timeout)
        return element.text
    
    def get_attribute(self, locator, attribute_name, timeout=None):
        """
        Get attribute value from element
        
        Args:
            locator (tuple): Locator tuple
            attribute_name (str): Name of attribute
            timeout (int): Wait timeout
        
        Returns:
            str: Attribute value
        """
        element = self.find_element(locator, timeout)
        return element.get_attribute(attribute_name)
    
    def is_element_visible(self, locator, timeout=5):
        """
        Check if element is visible
        
        Args:
            locator (tuple): Locator tuple
            timeout (int): Wait timeout
        
        Returns:
            bool: True if element is visible
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def is_element_present(self, locator):
        """
        Check if element is present in DOM
        
        Args:
            locator (tuple): Locator tuple
        
        Returns:
            bool: True if element is present
        """
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
    
    def wait_for_page_to_load(self, timeout=None):
        """
        Wait for page to load completely
        
        Args:
            timeout (int): Wait timeout
        """
        if timeout:
            wait = WebDriverWait(self.driver, timeout)
        else:
            wait = self.wait
        
        wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
    
    def scroll_to_element(self, locator):
        """
        Scroll to element
        
        Args:
            locator (tuple): Locator tuple
        """
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
    
    def get_page_title(self):
        """Get current page title"""
        return self.driver.title
    
    def get_current_url(self):
        """Get current URL"""
        return self.driver.current_url