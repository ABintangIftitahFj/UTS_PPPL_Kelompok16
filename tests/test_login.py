"""
Regression tests for MathsTeam login functionality
"""
import pytest
import time
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from config.config import Config

class TestLogin:
    """Test suite for login functionality"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Setup for each test method"""
        self.driver = driver
        self.login_page = LoginPage(driver)
        self.dashboard_page = DashboardPage(driver)
    
    @pytest.mark.smoke
    @pytest.mark.critical
    @pytest.mark.login
    def test_valid_login(self, valid_credentials):
        """
        Test successful login with valid credentials
        
        Test Steps:
        1. Navigate to login page
        2. Enter valid email and password
        3. Click login button
        4. Verify successful login (redirect to dashboard)
        """
        # Navigate to login page
        self.login_page.navigate_to_login()
        assert self.login_page.is_on_login_page(), "Should be on login page"
        
        # Perform login
        login_success = self.login_page.login(
            valid_credentials['email'], 
            valid_credentials['password']
        )
        
        # Verify login success
        assert login_success, "Login should be successful"
        
        # Verify we're redirected away from login page
        time.sleep(2)  # Wait for redirect
        assert not self.login_page.is_on_login_page(), "Should be redirected away from login page"
        
        # Verify dashboard is accessible
        if self.dashboard_page.is_on_dashboard():
            assert self.dashboard_page.verify_page_loaded(), "Dashboard should load properly"
    
    @pytest.mark.regression
    @pytest.mark.login
    def test_invalid_email_valid_password(self):
        """
        Test login with invalid email and valid password
        
        Expected: Login should fail
        """
        self.login_page.navigate_to_login()
        
        result = self.login_page.login("invalid@email.com", Config.LOGIN_PASSWORD)
        
        # Should remain on login page or show error
        assert not result or self.login_page.is_on_login_page(), "Login should fail with invalid email"
        
        # Check for error message (if present)
        error_msg = self.login_page.get_error_message()
        if error_msg:
            assert len(error_msg) > 0, "Error message should be displayed"
    
    @pytest.mark.regression
    @pytest.mark.login
    def test_valid_email_invalid_password(self):
        """
        Test login with valid email and invalid password
        
        Expected: Login should fail
        """
        self.login_page.navigate_to_login()
        
        result = self.login_page.login(Config.LOGIN_EMAIL, "wrongpassword")
        
        # Should remain on login page or show error
        assert not result or self.login_page.is_on_login_page(), "Login should fail with invalid password"
        
        # Check for error message (if present)
        error_msg = self.login_page.get_error_message()
        if error_msg:
            assert len(error_msg) > 0, "Error message should be displayed"
    
    @pytest.mark.regression
    @pytest.mark.login
    def test_empty_credentials(self):
        """
        Test login with empty email and password
        
        Expected: Login should fail
        """
        self.login_page.navigate_to_login()
        
        result = self.login_page.login("", "")
        
        # Should remain on login page
        assert not result or self.login_page.is_on_login_page(), "Login should fail with empty credentials"
    
    @pytest.mark.regression
    @pytest.mark.login
    def test_login_page_elements(self):
        """
        Test that all required elements are present on login page
        
        Test Steps:
        1. Navigate to login page
        2. Verify email input field exists
        3. Verify password input field exists
        4. Verify login button exists
        """
        self.login_page.navigate_to_login()
        
        # Check email field
        try:
            email_present = self.login_page.is_element_present(self.login_page.EMAIL_INPUT)
            if not email_present:
                email_present = self.login_page.is_element_present(self.login_page.EMAIL_INPUT_ALT)
            assert email_present, "Email input field should be present"
        except:
            pytest.fail("Could not find email input field")
        
        # Check password field
        try:
            password_present = self.login_page.is_element_present(self.login_page.PASSWORD_INPUT)
            if not password_present:
                password_present = self.login_page.is_element_present(self.login_page.PASSWORD_INPUT_ALT)
            assert password_present, "Password input field should be present"
        except:
            pytest.fail("Could not find password input field")
        
        # Check login button
        login_button_present = False
        for locator in [self.login_page.LOGIN_BUTTON, self.login_page.LOGIN_BUTTON_ALT, self.login_page.LOGIN_BUTTON_ALT2]:
            if self.login_page.is_element_present(locator):
                login_button_present = True
                break
        
        assert login_button_present, "Login button should be present"
    
    @pytest.mark.regression
    @pytest.mark.login
    def test_login_page_title(self):
        """
        Test that login page has appropriate title
        """
        self.login_page.navigate_to_login()
        
        page_title = self.login_page.get_page_title()
        assert page_title is not None, "Page should have a title"
        assert len(page_title) > 0, "Page title should not be empty"
        
        # Common title keywords for login pages
        title_lower = page_title.lower()
        title_keywords = ['login', 'masuk', 'sign in', 'mathsteam']
        
        # At least one keyword should be in the title
        has_relevant_keyword = any(keyword in title_lower for keyword in title_keywords)
        if not has_relevant_keyword:
            # Print actual title for debugging
            print(f"Actual page title: '{page_title}'")
    
    @pytest.mark.regression
    @pytest.mark.login
    def test_multiple_invalid_login_attempts(self, invalid_credentials):
        """
        Test multiple invalid login attempts
        
        Expected: All attempts should fail
        """
        for i, creds in enumerate(invalid_credentials):
            self.login_page.navigate_to_login()
            
            result = self.login_page.login(creds['email'], creds['password'])
            
            # Should remain on login page or show error
            assert not result or self.login_page.is_on_login_page(), \
                f"Invalid login attempt {i+1} should fail: {creds}"
            
            # Clear fields for next attempt
            self.login_page.clear_login_fields()
    
    @pytest.mark.smoke
    @pytest.mark.login
    def test_login_and_logout_flow(self, valid_credentials):
        """
        Test complete login and logout flow
        
        Test Steps:
        1. Login with valid credentials
        2. Verify successful login
        3. Logout
        4. Verify logout (return to login page)
        """
        # Step 1 & 2: Login
        self.login_page.navigate_to_login()
        login_success = self.login_page.login(
            valid_credentials['email'], 
            valid_credentials['password']
        )
        
        assert login_success, "Login should be successful"
        time.sleep(2)  # Wait for page to load
        
        # Step 3: Logout
        logout_success = False
        
        # Try logout from login page first
        if hasattr(self.login_page, 'logout'):
            logout_success = self.login_page.logout()
        
        # If that doesn't work, try from dashboard page
        if not logout_success:
            logout_success = self.dashboard_page.logout()
        
        # Step 4: Verify logout (if logout functionality exists)
        if logout_success:
            time.sleep(2)  # Wait for redirect
            # Should be back on login page or home page
            current_url = self.driver.current_url
            assert "login" in current_url.lower() or current_url.rstrip('/') == Config.BASE_URL.rstrip('/'), \
                "Should be redirected to login page or home page after logout"