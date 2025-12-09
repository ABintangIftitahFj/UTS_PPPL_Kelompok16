# Demo Selenium - Testing Documentation

## 📚 Struktur Project

```
demo_selenium/
├── config/
│   ├── __init__.py
│   └── config.py              # Konfigurasi environment & settings
├── pages/                      # Page Object Models
│   ├── __init__.py
│   ├── base_page.py           # Base class untuk semua pages
│   ├── login_page.py          # Page object untuk halaman login
│   └── kelola_siswa_page.py   # Page object untuk kelola siswa
├── tests/                      # Test cases
│   ├── __init__.py
│   ├── test_simple.py         # Test dasar (accessibility, login)
│   └── test_kelola_siswa.py   # Test CRUD kelola siswa
├── .env                        # Environment variables
├── .venv/                      # Virtual environment
├── requirements.txt            # Dependencies
└── readme.md                   # Dokumentasi ini
```

## 🚀 Setup & Installation

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
Edit file `.env`:
```properties
BASE_URL=https://mathsteam.id/
BROWSER=chrome
HEADLESS=False
IMPLICIT_WAIT=10
EXPLICIT_WAIT=20

# Test Credentials
TEST_USERNAME=admin@tes.com
TEST_PASSWORD=12345678
```

## 🧪 Running Tests

### Run All Tests
```bash
pytest -v
```

### Run Specific Test File
```bash
# Test simple (login, accessibility)
pytest -v tests/test_simple.py

# Test kelola siswa
pytest -v tests/test_kelola_siswa.py
```

### Run dengan Output Detail
```bash
pytest -v -s tests/test_simple.py
```

### Run Specific Test Function
```bash
pytest -v tests/test_kelola_siswa.py::test_add_siswa
```

### Run dengan HTML Report
```bash
pytest --html=report.html tests/
```

### Run dengan Allure Report
```bash
# Generate allure results
pytest --alluredir=./allure-results tests/

# View report
allure serve ./allure-results
```

## 📝 Test Cases

### Test Simple (test_simple.py)
1. ✅ `test_website_accessibility` - Mengecek apakah website dapat diakses
2. ✅ `test_login_page_elements` - Mengecek element form login tersedia
3. ✅ `test_invalid_login` - Test login dengan kredensial invalid

### Test Kelola Siswa (test_kelola_siswa.py)
1. ✅ `test_access_kelola_siswa_page` - Akses halaman kelola siswa
2. ✅ `test_add_siswa` - Tambah data siswa baru
3. ✅ `test_edit_siswa` - Edit data siswa
4. ✅ `test_delete_siswa` - Hapus data siswa
5. ✅ `test_kelola_siswa_full_flow` - Test complete CRUD flow

## 🔧 Customization

### Menyesuaikan Locator

Jika element locator tidak sesuai dengan website Anda, edit file page object:

**Contoh - Edit `pages/kelola_siswa_page.py`:**
```python
# Gunakan Chrome DevTools (F12) untuk inspect element
# Kemudian update locator sesuai dengan HTML actual

# Contoh locator:
ADD_SISWA_BUTTON = (By.ID, "btn-add-siswa")  # Jika punya ID
ADD_SISWA_BUTTON = (By.CLASS_NAME, "btn-primary")  # Jika punya class
ADD_SISWA_BUTTON = (By.XPATH, "//button[text()='Tambah Siswa']")  # Jika perlu XPath
```

### Menambahkan Page Object Baru

1. Buat file baru di `pages/`, misal `dashboard_page.py`
2. Extend dari `BasePage`:
```python
from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from config.config import Config

class DashboardPage(BasePage):
    # Locators
    MENU_ITEM = (By.ID, "menu")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = f"{Config.BASE_URL}dashboard"
    
    def open_dashboard(self):
        self.open(self.url)
```

3. Buat test file di `tests/`, misal `test_dashboard.py`

## 🐛 Troubleshooting

### Test tidak menemukan element
- **Solusi**: Periksa locator dengan Chrome DevTools (F12)
- Update locator di file page object

### Login gagal
- **Solusi**: Cek credentials di `.env`
- Pastikan URL BASE_URL benar

### ChromeDriver error
- **Solusi**: Library `webdriver-manager` otomatis download driver
- Jika masih error, update Chrome browser ke versi terbaru

### Test terlalu cepat/element belum muncul
- **Solusi**: Tambahkan wait time di `.env`:
```
EXPLICIT_WAIT=30
IMPLICIT_WAIT=15
```

## 📊 Best Practices

1. **Gunakan Page Object Model (POM)** - Pisahkan locator & logic dari test
2. **DRY Principle** - Jangan repeat code, gunakan fixtures
3. **Descriptive Names** - Gunakan nama test yang jelas & deskriptif
4. **Independent Tests** - Setiap test harus bisa run sendiri
5. **Clean Up** - Gunakan fixtures untuk setup & teardown

## 📖 Resources

- [Selenium Documentation](https://www.selenium.dev/documentation/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Page Object Pattern](https://www.selenium.dev/documentation/test_practices/encouraged/page_object_models/)

## ✅ Expected Output

```
tests/test_simple.py::test_website_accessibility PASSED
✅ Website accessible: https://mathsteam.id/login
✅ Page title: MathsTeam - Login

tests/test_kelola_siswa.py::test_access_kelola_siswa_page PASSED
✅ Successfully accessed Kelola Siswa page

tests/test_kelola_siswa.py::test_add_siswa PASSED
✅ Successfully attempted to add siswa: Test Siswa Automation
```

## 🎯 Next Steps

1. Sesuaikan locator dengan HTML actual website
2. Tambahkan test case sesuai requirement
3. Integrate dengan CI/CD pipeline
4. Generate test reports (HTML/Allure)