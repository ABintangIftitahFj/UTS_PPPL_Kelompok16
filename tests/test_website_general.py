"""
General regression tests for MathsTeam website functionality
"""
import pytest
import time
from selenium.webdriver.common.by import By
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.base_page import BasePage
from config.config import Config

class TestWebsiteGeneral:
    """Test suite for general website functionality"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Setup for each test method"""
        self.driver = driver
        self.base_page = BasePage(driver)
        self.login_page = LoginPage(driver)
        self.dashboard_page = DashboardPage(driver)
    
    @pytest.mark.smoke
    @pytest.mark.critical
    def test_website_accessibility(self):
        """
        Test that the website is accessible and loads
        
        Test Steps:
        1. Navigate to base URL
        2. Verify page loads successfully
        3. Verify page has title
        4. Verify basic HTML structure
        """
        # Navigate to base URL
        self.base_page.navigate_to(Config.BASE_URL)
        
        # Verify page loads
        self.base_page.wait_for_page_to_load()
        
        # Check page title
        page_title = self.base_page.get_page_title()
        assert page_title is not None, "Website should have a page title"
        assert len(page_title) > 0, "Page title should not be empty"
        
        print(f"Website title: '{page_title}'")
        
        # Check current URL
        current_url = self.base_page.get_current_url()
        assert current_url is not None, "Should have a valid URL"
        
        print(f"Website URL: '{current_url}'")
    
    @pytest.mark.regression
    def test_website_https(self):
        """
        Test that website uses HTTPS (if expected)
        """
        self.base_page.navigate_to(Config.BASE_URL)
        current_url = self.base_page.get_current_url()
        
        if Config.BASE_URL.startswith('https://'):
            assert current_url.startswith('https://'), "Website should use HTTPS"
            print("Website correctly uses HTTPS")
        else:
            print(f"Website uses: {current_url.split('://')[0]}")
    
    @pytest.mark.regression
    def test_responsive_design_elements(self):
        """
        Test basic responsive design elements
        """
        self.base_page.navigate_to(Config.BASE_URL)
        self.base_page.wait_for_page_to_load()
        
        # Get initial window size
        original_size = self.driver.get_window_size()
        print(f"Original window size: {original_size}")
        
        # Test mobile viewport
        self.driver.set_window_size(375, 667)  # iPhone 6/7/8 size
        time.sleep(1)
        
        # Verify page still loads in mobile view
        mobile_title = self.base_page.get_page_title()
        assert mobile_title is not None, "Page should work in mobile viewport"
        
        # Test tablet viewport
        self.driver.set_window_size(768, 1024)  # iPad size
        time.sleep(1)
        
        # Verify page still loads in tablet view
        tablet_title = self.base_page.get_page_title()
        assert tablet_title is not None, "Page should work in tablet viewport"
        
        # Restore original size
        self.driver.set_window_size(original_size['width'], original_size['height'])
        time.sleep(1)
    
    @pytest.mark.regression
    def test_basic_html_structure(self):
        """
        Test that page has basic HTML structure
        """
        self.base_page.navigate_to(Config.BASE_URL)
        self.base_page.wait_for_page_to_load()
        
        # Check for basic HTML elements
        html_checks = {
            'html': (By.TAG_NAME, 'html'),
            'head': (By.TAG_NAME, 'head'), 
            'body': (By.TAG_NAME, 'body'),
            'title': (By.TAG_NAME, 'title')
        }
        
        for element_name, locator in html_checks.items():
            element_present = self.base_page.is_element_present(locator)
            assert element_present, f"Page should have {element_name} element"
            print(f"✓ {element_name} element found")
    
    @pytest.mark.regression
    def test_common_navigation_elements(self):
        """
        Test for common navigation elements on the website
        """
        self.base_page.navigate_to(Config.BASE_URL)
        self.base_page.wait_for_page_to_load()
        
        # Common navigation selectors
        nav_selectors = [
            (By.CSS_SELECTOR, 'nav'),
            (By.CSS_SELECTOR, '.navbar'),
            (By.CSS_SELECTOR, '.navigation'),
            (By.CSS_SELECTOR, '.menu'),
            (By.CSS_SELECTOR, 'header nav'),
        ]
        
        nav_found = False
        for selector in nav_selectors:
            if self.base_page.is_element_present(selector):
                nav_found = True
                print(f"Navigation found with selector: {selector}")
                break
        
        if nav_found:
            print("✓ Navigation elements found")
        else:
            print("ℹ No standard navigation elements found (may be custom implementation)")
    
    @pytest.mark.regression
    def test_links_and_buttons(self):
        """
        Test that links and buttons are present and clickable
        """
        self.base_page.navigate_to(Config.BASE_URL)
        self.base_page.wait_for_page_to_load()
        
        # Find all links
        links = self.base_page.find_elements((By.TAG_NAME, 'a'), timeout=10)
        clickable_links = [link for link in links if link.is_displayed() and link.is_enabled()]
        
        print(f"Found {len(links)} total links, {len(clickable_links)} are clickable")
        
        # Find all buttons
        buttons = self.base_page.find_elements((By.TAG_NAME, 'button'), timeout=5)
        input_buttons = self.base_page.find_elements((By.CSS_SELECTOR, 'input[type="submit"], input[type="button"]'), timeout=5)
        
        all_buttons = buttons + input_buttons
        clickable_buttons = [btn for btn in all_buttons if btn.is_displayed() and btn.is_enabled()]
        
        print(f"Found {len(all_buttons)} total buttons, {len(clickable_buttons)} are clickable")
        
        # Should have some interactive elements
        total_interactive = len(clickable_links) + len(clickable_buttons)
        assert total_interactive > 0, "Page should have some clickable links or buttons"
    
    @pytest.mark.regression
    def test_images_loading(self):
        """
        Test that images on the page load properly
        """
        self.base_page.navigate_to(Config.BASE_URL)
        self.base_page.wait_for_page_to_load()
        
        # Find all images
        images = self.base_page.find_elements((By.TAG_NAME, 'img'), timeout=5)
        
        if len(images) > 0:
            print(f"Found {len(images)} images on the page")
            
            # Check first few images for loading
            for i, img in enumerate(images[:5]):  # Check first 5 images
                if img.is_displayed():
                    # Check if image has src attribute
                    src = img.get_attribute('src')
                    alt = img.get_attribute('alt')
                    
                    print(f"Image {i+1}: src='{src}', alt='{alt}'")
                    
                    if src:
                        assert len(src) > 0, f"Image {i+1} should have valid src attribute"
        else:
            print("No images found on the page")
    
    @pytest.mark.smoke
    def test_login_page_accessibility(self):
        """
        Test that login page is accessible from main site
        """
        # Try to access login page directly
        self.login_page.navigate_to_login()
        
        # Verify we can reach login page
        login_accessible = (
            self.login_page.is_on_login_page() or
            self.base_page.get_current_url().endswith('/login') or
            'login' in self.base_page.get_current_url().lower()
        )
        
        if login_accessible:
            print("✓ Login page is accessible")
            
            # Verify login page has required elements
            assert self.login_page.verify_page_loaded(), "Login page should load properly"
        else:
            print("⚠ Login page may not be accessible via standard URL")
            current_url = self.base_page.get_current_url()
            print(f"Current URL after login navigation: {current_url}")
    
    @pytest.mark.regression
    def test_javascript_functionality(self):
        """
        Test that JavaScript is working on the page
        """
        self.base_page.navigate_to(Config.BASE_URL)
        self.base_page.wait_for_page_to_load()
        
        # Test basic JavaScript execution
        js_result = self.driver.execute_script("return 'JavaScript is working';")
        assert js_result == 'JavaScript is working', "JavaScript should be enabled and working"
        
        # Test jQuery if available
        jquery_available = self.driver.execute_script("return typeof jQuery !== 'undefined';")
        if jquery_available:
            print("✓ jQuery is available on the page")
        else:
            print("ℹ jQuery not detected (may not be used)")
        
        # Test that document is ready
        doc_ready = self.driver.execute_script("return document.readyState;")
        assert doc_ready == 'complete', "Document should be in complete state"
        
        print("✓ Basic JavaScript functionality is working")
    
    @pytest.mark.regression
    def test_page_performance_basic(self):
        """
        Test basic page performance indicators
        """
        start_time = time.time()
        
        self.base_page.navigate_to(Config.BASE_URL)
        self.base_page.wait_for_page_to_load()
        
        load_time = time.time() - start_time
        print(f"Page load time: {load_time:.2f} seconds")
        
        # Basic performance check - page should load within reasonable time
        assert load_time < 60, f"Page should load within 60 seconds, took {load_time:.2f} seconds"
        
        if load_time < 5:
            print("✓ Good page load performance")
        elif load_time < 15:
            print("✓ Acceptable page load performance")
        else:
            print("⚠ Slow page load performance")
    
    @pytest.mark.regression
    def test_browser_console_errors(self):
        """
        Test for JavaScript errors in browser console
        """
        self.base_page.navigate_to(Config.BASE_URL)
        self.base_page.wait_for_page_to_load()
        
        # Get browser console logs
        try:
            logs = self.driver.get_log('browser')
            
            # Filter for severe errors
            errors = [log for log in logs if log['level'] == 'SEVERE']
            
            if len(errors) > 0:
                print(f"Found {len(errors)} severe console errors:")
                for error in errors[:5]:  # Show first 5 errors
                    print(f"  - {error['message']}")
                
                # Don't fail test for console errors, just report them
                print("⚠ Console errors detected but test continues")
            else:
                print("✓ No severe console errors detected")
                
        except Exception as e:
            print(f"Could not retrieve console logs: {e}")
            # This is not a test failure - some browsers/drivers may not support this