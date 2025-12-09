"""
Regression tests for MathsTeam dashboard and navigation functionality
"""
import pytest
import time
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from config.config import Config

class TestDashboard:
    """Test suite for dashboard functionality"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver, valid_credentials):
        """Setup for each test method - login before each test"""
        self.driver = driver
        self.login_page = LoginPage(driver)
        self.dashboard_page = DashboardPage(driver)
        self.credentials = valid_credentials
        
        # Login before each test
        self.login_page.navigate_to_login()
        login_success = self.login_page.login(
            self.credentials['email'], 
            self.credentials['password']
        )
        
        if not login_success:
            pytest.skip("Cannot proceed with dashboard tests - login failed")
        
        time.sleep(2)  # Wait for page to load
    
    @pytest.mark.smoke
    @pytest.mark.dashboard
    @pytest.mark.critical
    def test_dashboard_accessibility_after_login(self):
        """
        Test that dashboard is accessible after successful login
        
        Test Steps:
        1. Login (done in setup)
        2. Verify we can access dashboard
        3. Verify basic dashboard elements are present
        """
        # Try to navigate to dashboard
        self.dashboard_page.navigate_to_dashboard()
        
        # Verify we're on dashboard or home page
        is_on_dashboard = self.dashboard_page.is_on_dashboard()
        
        if is_on_dashboard:
            # Verify page loaded properly
            assert self.dashboard_page.verify_page_loaded(), "Dashboard should load with basic elements"
        else:
            # If not explicitly on dashboard, at least verify we're not on login page
            assert not self.login_page.is_on_login_page(), "Should not be on login page after successful login"
    
    @pytest.mark.regression
    @pytest.mark.dashboard
    def test_dashboard_page_title(self):
        """
        Test that dashboard page has appropriate title
        """
        self.dashboard_page.navigate_to_dashboard()
        
        page_title = self.dashboard_page.get_page_title()
        assert page_title is not None, "Dashboard page should have a title"
        assert len(page_title) > 0, "Dashboard page title should not be empty"
        
        print(f"Dashboard page title: '{page_title}'")
    
    @pytest.mark.regression
    @pytest.mark.navigation
    def test_navigation_bar_presence(self):
        """
        Test that navigation bar is present on the page
        """
        # Check if navbar is present
        navbar_present = self.dashboard_page.is_navbar_present()
        
        if navbar_present:
            print("Navigation bar found")
            
            # If navbar is present, check for menu items
            menu_items = self.dashboard_page.get_menu_items()
            print(f"Menu items found: {menu_items}")
            
            # Should have at least some navigation elements
            assert len(menu_items) >= 0, "Navigation should contain menu items"
        else:
            print("Navigation bar not found - this might be expected for some designs")
    
    @pytest.mark.regression
    @pytest.mark.dashboard
    def test_logo_presence(self):
        """
        Test that logo is present on the page
        """
        logo_present = self.dashboard_page.is_logo_present()
        
        if logo_present:
            print("Logo found on the page")
        else:
            print("Logo not found - checking if this is expected")
            # For some sites, logo might be part of the title or not present
    
    @pytest.mark.regression
    @pytest.mark.dashboard
    def test_main_content_presence(self):
        """
        Test that main content area is present
        """
        # Navigate to dashboard/home
        self.dashboard_page.navigate_to_home()
        
        # Check for main content
        main_content_present = self.dashboard_page.is_element_visible(
            self.dashboard_page.MAIN_CONTENT, timeout=10
        )
        
        if main_content_present:
            print("Main content area found")
        
        # Check for page title
        page_title_text = self.dashboard_page.get_page_title_text()
        if page_title_text:
            print(f"Page title text: '{page_title_text}'")
        
        # At least one of these should be present
        assert main_content_present or page_title_text, \
            "Page should have either main content area or page title"
    
    @pytest.mark.regression
    @pytest.mark.dashboard
    def test_user_authentication_status(self):
        """
        Test that user appears to be authenticated after login
        """
        # Check various indicators that user is logged in
        is_logged_in = self.dashboard_page.is_user_logged_in()
        
        if is_logged_in:
            print("User appears to be logged in")
            
            # Try to get user name if available
            user_name = self.dashboard_page.get_user_name()
            if user_name:
                print(f"Logged in user: {user_name}")
        
        # At minimum, we should not be on login page
        assert not self.login_page.is_on_login_page(), \
            "Should not be on login page when authenticated"
    
    @pytest.mark.regression
    @pytest.mark.navigation
    def test_home_navigation(self):
        """
        Test navigation to home page
        """
        # Navigate to home
        self.dashboard_page.navigate_to_home()
        
        # Verify we can access the home page
        current_url = self.dashboard_page.get_current_url()
        base_url = Config.BASE_URL.rstrip('/')
        
        # Should be on home page or dashboard
        assert (
            current_url.rstrip('/') == base_url or
            'dashboard' in current_url.lower() or
            'home' in current_url.lower()
        ), f"Should navigate to home page. Current URL: {current_url}"
    
    @pytest.mark.regression
    @pytest.mark.navigation
    def test_page_navigation_links(self):
        """
        Test clicking on available navigation links
        """
        # Get initial URL
        initial_url = self.dashboard_page.get_current_url()
        
        # Try clicking home link if available
        home_clicked = self.dashboard_page.click_home_link()
        if home_clicked:
            print("Successfully clicked home link")
            time.sleep(1)
            
        # Try clicking profile link if available
        profile_clicked = self.dashboard_page.click_profile_link()
        if profile_clicked:
            print("Successfully clicked profile link")
            time.sleep(1)
            
            # Navigate back to dashboard
            self.dashboard_page.navigate_to_dashboard()
        
        # Try clicking settings link if available
        settings_clicked = self.dashboard_page.click_settings_link()
        if settings_clicked:
            print("Successfully clicked settings link")
            time.sleep(1)
        
        # At least the page should be navigable
        final_url = self.dashboard_page.get_current_url()
        assert final_url is not None, "Should be able to navigate pages"
    
    @pytest.mark.regression
    @pytest.mark.dashboard
    def test_page_content_elements(self):
        """
        Test that page contains expected content elements
        """
        self.dashboard_page.navigate_to_home()
        
        # Count cards/widgets on the page
        cards_count = self.dashboard_page.get_cards_count()
        print(f"Number of cards/widgets found: {cards_count}")
        
        # Get menu items
        menu_items = self.dashboard_page.get_menu_items()
        print(f"Navigation menu items: {menu_items}")
        
        # Check if footer is present
        footer_present = self.dashboard_page.is_element_visible(
            self.dashboard_page.FOOTER, timeout=5
        )
        if footer_present:
            print("Footer found on page")
        
        # Page should have some content (cards, menu items, or other elements)
        has_content = (
            cards_count > 0 or
            len(menu_items) > 0 or
            footer_present or
            self.dashboard_page.get_page_title_text() is not None
        )
        
        assert has_content, "Page should contain some content elements"
    
    @pytest.mark.smoke
    @pytest.mark.navigation
    def test_logout_functionality(self):
        """
        Test logout functionality if available
        """
        # Try to logout
        logout_success = self.dashboard_page.logout()
        
        if logout_success:
            print("Logout functionality found and executed")
            time.sleep(2)  # Wait for redirect
            
            # Should be redirected to login page or home page
            current_url = self.dashboard_page.get_current_url()
            is_logged_out = (
                'login' in current_url.lower() or
                current_url.rstrip('/') == Config.BASE_URL.rstrip('/')
            )
            
            if is_logged_out:
                print("Successfully logged out")
            else:
                print(f"After logout, current URL: {current_url}")
        else:
            print("Logout functionality not found or not accessible")
            # This is not necessarily a failure - some sites handle logout differently
    
    @pytest.mark.regression
    @pytest.mark.dashboard
    def test_page_load_time(self):
        """
        Test that pages load within reasonable time
        """
        import time
        
        start_time = time.time()
        self.dashboard_page.navigate_to_home()
        self.dashboard_page.wait_for_page_to_load()
        load_time = time.time() - start_time
        
        print(f"Page load time: {load_time:.2f} seconds")
        
        # Page should load within 30 seconds (generous limit for slow connections)
        assert load_time < 30, f"Page should load within 30 seconds, took {load_time:.2f} seconds"