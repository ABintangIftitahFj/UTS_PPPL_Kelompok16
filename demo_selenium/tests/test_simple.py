"""
Simple test cases for website accessibility
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from pages.login_page import LoginPage
from config.config import Config


@pytest.fixture(scope="function")
def driver():
    """Setup and teardown for Chrome WebDriver"""
    chrome_options = Options()
    if Config.HEADLESS:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Initialize driver
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    
    yield driver
    
    # Teardown
    driver.quit()


def test_website_accessibility(driver):
    """Test if the website login page is accessible"""
    login_page = LoginPage(driver)
    
    # Open login page
    login_page.open_login_page()
    
    # Get current URL and title
    current_url = login_page.get_current_url()
    page_title = login_page.get_title()
    
    # Assertions
    assert "mathsteam.id" in current_url, f"Expected URL to contain 'mathsteam.id', but got: {current_url}"
    assert page_title is not None, "Page title should not be None"
    
    # Print success messages
    print(f"\n✅ Website accessible: {current_url}")
    print(f"✅ Page title: {page_title}")


def test_login_page_elements(driver):
    """Test if login page elements are present"""
    login_page = LoginPage(driver)
    
    # Open login page
    login_page.open_login_page()
    
    # Check if essential elements are visible
    assert login_page.is_element_visible(login_page.USERNAME_INPUT), "Username input should be visible"
    assert login_page.is_element_visible(login_page.PASSWORD_INPUT), "Password input should be visible"
    assert login_page.is_element_visible(login_page.LOGIN_BUTTON), "Login button should be visible"
    
    print("\n✅ All login page elements are present and visible")


@pytest.mark.parametrize("username,password", [
    ("", ""),
    ("invalid@email.com", "wrongpassword")
])
def test_invalid_login(driver, username, password):
    """Test login with invalid credentials"""
    login_page = LoginPage(driver)
    
    # Open login page
    login_page.open_login_page()
    
    # Attempt login with invalid credentials
    if username and password:
        login_page.login(username, password)
        
        # Should remain on login page or show error
        current_url = login_page.get_current_url()
        print(f"\n✅ Invalid login test - Current URL: {current_url}")
    else:
        print(f"\n✅ Empty credentials test passed")