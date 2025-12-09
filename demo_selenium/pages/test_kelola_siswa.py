from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from config.config import Config

class KelolaSiswaPage(BasePage):
    """Kelola Siswa Page Object Model"""

USERNAME_INPUT = (By.ID, "email")
PASSWORD_INPUT = (By.ID, "password")
LOGIN_BUTTON = (By.XPATH, "//button[@type='submit']")
ERROR_MESSAGE = (By.CLASS_NAME, "alert-danger")

def __init__(self, driver):
        super().__init__(driver)
        self.url = f"{Config.BASE_URL}login"

    def open_kelola_siswa_page(self):
        """Navigate to kelola siswa page"""
        self.open(self.url)

    def enter_username(self, username):
        """Enter username"""
        self.type_text(self.USERNAME_INPUT, username)

    def enter_password(self, password):
        """Enter password"""
        self.type_text(self.PASSWORD_INPUT, password)

    def click_login_button(self):
        """Click login button"""
        self.click(self.LOGIN_BUTTON)

    def login(self, username, password):
        """Perform complete login"""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()

    def is_error_displayed(self):
        """Check if error message is displayed"""
        return self.is_element_visible(self.ERROR_MESSAGE)

    def get_error_message(self):
        """Get error message text"""
        return self.get_text(self.ERROR_MESSAGE)

    def see_siswa(self):
        """See siswa"""
        self.click(self.SEE_SISWA_BUTTON)

    def add_siswa(self):
        """Add siswa"""
        self.click(self.ADD_SISWA_BUTTON)

    def edit_siswa(self):
        """Edit siswa"""
        self.click(self.EDIT_SISWA_BUTTON)

    def delete_siswa(self):
        """Delete siswa"""
        self.click(self.DELETE_SISWA_BUTTON)
