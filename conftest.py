"""
Pytest configuration and fixtures for MathsTeam regression testing
"""
import pytest
import os
from datetime import datetime
from utils.driver_manager import DriverManager
from config.config import Config

def pytest_configure(config):
    """Configure pytest settings"""
    Config.create_directories()

@pytest.fixture(scope="session")
def driver_manager():
    """Session-scoped driver manager fixture"""
    manager = DriverManager()
    yield manager
    # Cleanup is handled by individual test fixtures

@pytest.fixture(scope="function")
def driver(driver_manager):
    """Function-scoped driver fixture - new driver for each test"""
    driver_instance = driver_manager.get_driver()
    yield driver_instance
    
    # Take screenshot on test failure
    if hasattr(pytest, "current_test_failed") and pytest.current_test_failed:
        if Config.SCREENSHOTS_ON_FAILURE:
            test_name = pytest.current_test_name
            driver_manager.take_screenshot(f"FAILED_{test_name}")
    
    # Ensure driver is properly closed
    try:
        driver_manager.quit_driver()
    except Exception as e:
        print(f"Warning during driver cleanup: {e}")
        # Force cleanup if normal quit fails
        driver_manager.force_quit_all_drivers()

@pytest.fixture(scope="class")
def class_driver(driver_manager):
    """Class-scoped driver fixture - shared driver for test class"""
    driver_instance = driver_manager.get_driver()
    yield driver_instance
    driver_manager.quit_driver()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results for screenshot on failure"""
    outcome = yield
    rep = outcome.get_result()
    
    # Store test name and result for screenshot capture
    pytest.current_test_name = item.name
    pytest.current_test_failed = rep.when == "call" and rep.failed

def pytest_addoption(parser):
    """Add custom command line options"""
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to use for testing (chrome, firefox, edge)"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run tests in headless mode"
    )
    parser.addoption(
        "--base-url",
        action="store",
        default=Config.BASE_URL,
        help="Base URL for testing"
    )

@pytest.fixture(scope="session")
def browser_config(request):
    """Session-scoped browser configuration"""
    return {
        'browser': request.config.getoption("--browser"),
        'headless': request.config.getoption("--headless"),
        'base_url': request.config.getoption("--base-url")
    }

# Custom markers
def pytest_configure(config):
    """Register custom markers"""
    config.addinivalue_line(
        "markers", "smoke: mark test as smoke test"
    )
    config.addinivalue_line(
        "markers", "regression: mark test as regression test"
    )
    config.addinivalue_line(
        "markers", "critical: mark test as critical functionality"
    )
    config.addinivalue_line(
        "markers", "login: mark test as login-related"
    )
    config.addinivalue_line(
        "markers", "dashboard: mark test as dashboard-related"
    )
    config.addinivalue_line(
        "markers", "navigation: mark test as navigation-related"
    )

# Test data fixtures
@pytest.fixture
def valid_credentials():
    """Valid login credentials"""
    return {
        'email': Config.LOGIN_EMAIL,
        'password': Config.LOGIN_PASSWORD
    }

@pytest.fixture
def invalid_credentials():
    """Invalid login credentials for negative testing"""
    return [
        {'email': 'invalid@email.com', 'password': 'wrongpassword'},
        {'email': Config.LOGIN_EMAIL, 'password': 'wrongpassword'},
        {'email': 'invalid@email.com', 'password': Config.LOGIN_PASSWORD},
        {'email': '', 'password': ''},
        {'email': 'invalid-email', 'password': '123'},
    ]

@pytest.fixture
def test_urls():
    """Common URLs for testing"""
    base_url = Config.BASE_URL.rstrip('/')
    return {
        'home': base_url,
        'login': f"{base_url}/login",
        'dashboard': f"{base_url}/dashboard",
    }