"""
Kelola Siswa Page Object Model
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.config import Config
import time


class KelolaSiswaPage(BasePage):
    """Kelola Siswa page object"""
    
    # Locators - Menu Navigation
    MENU_SISWA = (By.XPATH, "//a[contains(text(), 'Siswa') or contains(@href, 'siswa')]")
    
    # Locators - Buttons
    ADD_SISWA_BUTTON = (By.XPATH, "//button[contains(text(), 'Tambah') or contains(text(), 'Add')]")
    EDIT_SISWA_BUTTON = (By.XPATH, "//button[contains(text(), 'Edit') or @title='Edit']")
    DELETE_SISWA_BUTTON = (By.XPATH, "//button[contains(text(), 'Hapus') or contains(text(), 'Delete')]")
    SAVE_BUTTON = (By.XPATH, "//button[@type='submit' or contains(text(), 'Simpan') or contains(text(), 'Save')]")
    CONFIRM_DELETE_BUTTON = (By.XPATH, "//button[contains(text(), 'Ya') or contains(text(), 'Confirm')]")
    
    # Locators - Form Fields
    NAMA_INPUT = (By.ID, "nama")
    NIS_INPUT = (By.ID, "nis")
    KELAS_INPUT = (By.ID, "kelas")
    
    # Locators - Table
    TABLE_SISWA = (By.XPATH, "//table")
    FIRST_ROW_SISWA = (By.XPATH, "//table/tbody/tr[1]")
    
    # Locators - Success Message
    SUCCESS_MESSAGE = (By.CLASS_NAME, "alert-success")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = f"{Config.BASE_URL}admin/siswa"
    
    def open_kelola_siswa_page(self):
        """Navigate to kelola siswa page"""
        self.open(self.url)
    
    def click_menu_siswa(self):
        """Click menu siswa from navigation"""
        self.click(self.MENU_SISWA)
        time.sleep(1)  # Wait for page load
    
    def click_add_siswa(self):
        """Click add siswa button"""
        self.click(self.ADD_SISWA_BUTTON)
        time.sleep(0.5)
    
    def fill_siswa_form(self, nama, nis, kelas):
        """Fill siswa form"""
        self.type_text(self.NAMA_INPUT, nama)
        self.type_text(self.NIS_INPUT, nis)
        self.type_text(self.KELAS_INPUT, kelas)
    
    def click_save(self):
        """Click save button"""
        self.click(self.SAVE_BUTTON)
        time.sleep(1)
    
    def add_new_siswa(self, nama, nis, kelas):
        """Complete flow to add new siswa"""
        self.click_add_siswa()
        self.fill_siswa_form(nama, nis, kelas)
        self.click_save()
    
    def click_edit_siswa(self):
        """Click edit button for first siswa in table"""
        self.click(self.EDIT_SISWA_BUTTON)
        time.sleep(0.5)
    
    def click_delete_siswa(self):
        """Click delete button for first siswa"""
        self.click(self.DELETE_SISWA_BUTTON)
        time.sleep(0.5)
    
    def confirm_delete(self):
        """Confirm delete action"""
        self.click(self.CONFIRM_DELETE_BUTTON)
        time.sleep(1)
    
    def is_table_visible(self):
        """Check if siswa table is visible"""
        return self.is_element_visible(self.TABLE_SISWA)
    
    def is_success_message_displayed(self):
        """Check if success message is displayed"""
        return self.is_element_visible(self.SUCCESS_MESSAGE)
    
    def get_success_message(self):
        """Get success message text"""
        return self.get_text(self.SUCCESS_MESSAGE)
