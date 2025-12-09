"""
WebDriver utilities for managing browser instances
"""
import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from config.config import Config

class DriverManager:
    """Manages WebDriver instances for different browsers"""
    
    def __init__(self):
        self.driver = None
        Config.create_directories()
    
    def get_driver(self, browser_name=None):
        """
        Initialize and return WebDriver instance
        
        Args:
            browser_name (str): Browser name (chrome, firefox, edge)
        
        Returns:
            WebDriver: Configured WebDriver instance
        """
        if browser_name is None:
            browser_name = Config.BROWSER
        
        browser_name = browser_name.lower()
        
        if browser_name == 'chrome':
            self.driver = self._get_chrome_driver()
        elif browser_name == 'firefox':
            self.driver = self._get_firefox_driver()
        elif browser_name == 'edge':
            self.driver = self._get_edge_driver()
        else:
            raise ValueError(f"Unsupported browser: {browser_name}")
        
        # Configure common driver settings
        self.driver.implicitly_wait(Config.IMPLICIT_WAIT)
        self.driver.maximize_window()
        
        return self.driver
    
    def _get_chrome_driver(self):
        """Initialize Chrome WebDriver"""
        options = ChromeOptions()
        
        if Config.HEADLESS:
            options.add_argument('--headless')
        
        # Additional Chrome options for stability
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        
        service = ChromeService(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)
    
    def _get_firefox_driver(self):
        """Initialize Firefox WebDriver"""
        options = FirefoxOptions()
        
        if Config.HEADLESS:
            options.add_argument('--headless')
        
        service = FirefoxService(GeckoDriverManager().install())
        return webdriver.Firefox(service=service, options=options)
    
    def _get_edge_driver(self):
        """Initialize Edge WebDriver"""
        options = EdgeOptions()
        
        if Config.HEADLESS:
            options.add_argument('--headless')
        
        service = EdgeService(EdgeChromiumDriverManager().install())
        return webdriver.Edge(service=service, options=options)
    
    def take_screenshot(self, test_name="test"):
        """
        Take screenshot and save to reports directory
        
        Args:
            test_name (str): Name of the test for screenshot filename
        
        Returns:
            str: Path to saved screenshot
        """
        if not self.driver:
            return None
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{test_name}_{timestamp}.png"
        filepath = os.path.join(Config.SCREENSHOTS_PATH, filename)
        
        try:
            self.driver.save_screenshot(filepath)
            return filepath
        except Exception as e:
            print(f"Failed to take screenshot: {e}")
            return None
    
    def quit_driver(self):
        """Quit the WebDriver instance safely"""
        if self.driver:
            try:
                # Close all browser windows
                self.driver.close()
                # Quit the driver completely
                self.driver.quit()
            except Exception as e:
                print(f"Warning: Issue closing driver: {e}")
            finally:
                self.driver = None
    
    def force_quit_all_drivers(self):
        """Force quit all browser processes - emergency cleanup"""
        import subprocess
        import platform
        
        try:
            if platform.system() == "Windows":
                # Kill Chrome processes
                subprocess.run(["taskkill", "/F", "/IM", "chrome.exe"], 
                             capture_output=True, check=False)
                subprocess.run(["taskkill", "/F", "/IM", "chromedriver.exe"], 
                             capture_output=True, check=False)
                # Kill Firefox processes
                subprocess.run(["taskkill", "/F", "/IM", "firefox.exe"], 
                             capture_output=True, check=False)
                subprocess.run(["taskkill", "/F", "/IM", "geckodriver.exe"], 
                             capture_output=True, check=False)
                # Kill Edge processes  
                subprocess.run(["taskkill", "/F", "/IM", "msedge.exe"], 
                             capture_output=True, check=False)
            else:
                # Linux/Mac - kill processes
                subprocess.run(["pkill", "-f", "chrome"], capture_output=True, check=False)
                subprocess.run(["pkill", "-f", "chromedriver"], capture_output=True, check=False)
                subprocess.run(["pkill", "-f", "firefox"], capture_output=True, check=False)
                subprocess.run(["pkill", "-f", "geckodriver"], capture_output=True, check=False)
        except Exception as e:
            print(f"Warning: Could not force quit browsers: {e}")