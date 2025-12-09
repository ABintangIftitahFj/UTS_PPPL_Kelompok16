# MathsTeam Regression Testing Suite

Automated regression testing suite untuk website https://mathsteam.id/ menggunakan Selenium WebDriver dan pytest.

## 📋 Deskripsi

Testing suite ini dirancang untuk melakukan regression testing pada website MathsTeam dengan fokus pada:
- Functionality testing (login, dashboard, navigation)
- UI/UX testing 
- Performance testing dasar
- Cross-browser compatibility

## 🛠️ Teknologi yang Digunakan

- **Python 3.8+**
- **Selenium WebDriver** - Browser automation
- **pytest** - Testing framework
- **WebDriver Manager** - Automatic driver management
- **pytest-html** - HTML test reports
- **Allure** - Advanced reporting (optional)

## 📁 Struktur Proyek

```
tugas setelah uts/
├── config/
│   └── config.py          # Konfigurasi testing
├── pages/
│   ├── base_page.py       # Base page object class
│   ├── login_page.py      # Login page object
│   └── dashboard_page.py  # Dashboard page object
├── tests/
│   ├── test_login.py      # Test cases untuk login
│   ├── test_dashboard.py  # Test cases untuk dashboard
│   └── test_website_general.py  # Test cases umum
├── utils/
│   └── driver_manager.py  # WebDriver management
├── reports/               # Test reports dan screenshots
├── .env                   # Environment variables
├── conftest.py           # pytest configuration
├── pytest.ini           # pytest settings
└── requirements.txt      # Python dependencies
```

## 🚀 Setup dan Instalasi

### 1. Clone/Download Project
```bash
# Jika menggunakan git
git clone [repository-url]
cd "tugas setelah uts"

# Atau extract files ke folder ini
```

### 2. Install Dependencies
```bash
# Install semua dependencies
pip install -r requirements.txt
```

### 3. Konfigurasi Environment
Edit file `.env` jika perlu mengubah konfigurasi:
```env
BASE_URL=https://mathsteam.id/
LOGIN_EMAIL=admin@tes.com
LOGIN_PASSWORD=12345678
BROWSER=chrome
HEADLESS=false
```

## 🎯 Menjalankan Tests

### Menjalankan Semua Tests
```bash
# Jalankan semua test cases
pytest

# Dengan output verbose
pytest -v

# Dengan HTML report
pytest --html=reports/report.html --self-contained-html
```

### Menjalankan Tests Berdasarkan Marker
```bash
# Smoke tests (test critical functionality)
pytest -m smoke

# Regression tests
pytest -m regression

# Login tests saja
pytest -m login

# Dashboard tests saja  
pytest -m dashboard

# Critical functionality tests
pytest -m critical
```

### Menjalankan Tests Tertentu
```bash
# Jalankan file test tertentu
pytest tests/test_login.py

# Jalankan test method tertentu
pytest tests/test_login.py::TestLogin::test_valid_login

# Jalankan test class tertentu
pytest tests/test_login.py::TestLogin
```

### Browser Options
```bash
# Jalankan dengan Firefox
pytest --browser=firefox

# Jalankan dalam headless mode
pytest --headless

# Jalankan dengan browser tertentu
pytest --browser=edge
```

## 📊 Test Reports

### HTML Reports
```bash
# Generate HTML report
pytest --html=reports/report.html --self-contained-html

# Report akan tersimpan di reports/report.html
```

### Allure Reports (Advanced)
```bash
# Generate Allure results
pytest --alluredir=reports/allure-results

# Serve Allure report
allure serve reports/allure-results
```

### Screenshots
- Screenshots otomatis diambil saat test gagal
- Tersimpan di folder `reports/screenshots/`
- Format: `FAILED_[test_name]_[timestamp].png`

## 🧪 Test Cases yang Tersedia

### Login Tests (`test_login.py`)
- ✅ `test_valid_login` - Login dengan kredensial valid
- ✅ `test_invalid_email_valid_password` - Login dengan email salah
- ✅ `test_valid_email_invalid_password` - Login dengan password salah
- ✅ `test_empty_credentials` - Login dengan field kosong
- ✅ `test_login_page_elements` - Verifikasi elemen login page
- ✅ `test_login_page_title` - Verifikasi title login page
- ✅ `test_multiple_invalid_login_attempts` - Multiple login gagal
- ✅ `test_login_and_logout_flow` - Flow login dan logout

### Dashboard Tests (`test_dashboard.py`)
- ✅ `test_dashboard_accessibility_after_login` - Akses dashboard setelah login
- ✅ `test_dashboard_page_title` - Title dashboard page
- ✅ `test_navigation_bar_presence` - Keberadaan navigation bar
- ✅ `test_logo_presence` - Keberadaan logo
- ✅ `test_main_content_presence` - Keberadaan main content
- ✅ `test_user_authentication_status` - Status autentikasi user
- ✅ `test_home_navigation` - Navigasi ke home page
- ✅ `test_page_navigation_links` - Testing navigation links
- ✅ `test_page_content_elements` - Testing content elements
- ✅ `test_logout_functionality` - Fungsi logout
- ✅ `test_page_load_time` - Performance testing

### General Website Tests (`test_website_general.py`)
- ✅ `test_website_accessibility` - Akses dasar website
- ✅ `test_website_https` - Testing HTTPS
- ✅ `test_responsive_design_elements` - Testing responsive design
- ✅ `test_basic_html_structure` - Struktur HTML dasar
- ✅ `test_common_navigation_elements` - Elemen navigasi
- ✅ `test_links_and_buttons` - Testing links dan buttons
- ✅ `test_images_loading` - Loading gambar
- ✅ `test_login_page_accessibility` - Akses login page
- ✅ `test_javascript_functionality` - Fungsi JavaScript
- ✅ `test_page_performance_basic` - Performance dasar
- ✅ `test_browser_console_errors` - Console errors

## 🔧 Konfigurasi

### Browser Support
- Chrome (default)
- Firefox
- Microsoft Edge

### Environment Variables
- `BASE_URL` - URL website yang akan ditest
- `LOGIN_EMAIL` - Email untuk login testing
- `LOGIN_PASSWORD` - Password untuk login testing
- `BROWSER` - Browser yang digunakan (chrome/firefox/edge)
- `HEADLESS` - Mode headless (true/false)
- `IMPLICIT_WAIT` - Implicit wait time (detik)
- `EXPLICIT_WAIT` - Explicit wait time (detik)

### Timeout Settings
- Implicit wait: 10 detik (default)
- Explicit wait: 20 detik (default)
- Test timeout: 300 detik (5 menit)

## 📝 Menambah Test Cases Baru

### 1. Buat Page Object Baru
```python
# pages/new_page.py
from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class NewPage(BasePage):
    # Locators
    ELEMENT_LOCATOR = (By.ID, "element-id")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def interact_with_element(self):
        self.click_element(self.ELEMENT_LOCATOR)
```

### 2. Buat Test File Baru
```python
# tests/test_new_feature.py
import pytest
from pages.new_page import NewPage

class TestNewFeature:
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.driver = driver
        self.new_page = NewPage(driver)
    
    @pytest.mark.regression
    def test_new_functionality(self):
        # Test implementation
        pass
```

## 🐛 Troubleshooting

### Driver Issues
```bash
# Update WebDriver
pip install --upgrade webdriver-manager

# Manual driver download jika diperlukan
# Chrome: https://chromedriver.chromium.org/
# Firefox: https://github.com/mozilla/geckodriver/releases
```

### Permission Issues
```bash
# Windows: Run as Administrator
# Linux/Mac: Check selenium permissions
```

### Browser Not Found
- Pastikan browser terinstall
- Update browser ke versi terbaru
- Cek PATH environment variable

### Timeout Issues
- Increase wait times in config.py
- Check internet connection
- Verify website accessibility

## 📈 Best Practices

1. **Page Object Model** - Gunakan POM untuk maintainability
2. **Explicit Waits** - Gunakan explicit waits daripada sleep()
3. **Test Data Management** - Pisahkan test data dari test logic
4. **Error Handling** - Handle exceptions dengan graceful
5. **Reporting** - Generate dan review test reports secara berkala

## 🤝 Kontribusi

1. Fork repository
2. Buat feature branch (`git checkout -b feature/new-test`)
3. Commit changes (`git commit -am 'Add new test'`)
4. Push branch (`git push origin feature/new-test`)
5. Create Pull Request

## 📞 Support

Jika mengalami masalah:
1. Check troubleshooting section di atas
2. Review test logs dan screenshots
3. Check browser console untuk errors
4. Verify website accessibility manually

## 📜 License

Project ini dibuat untuk keperluan akademik/pembelajaran.

---
**Dibuat untuk keperluan Tugas PPPL - Semester 5**