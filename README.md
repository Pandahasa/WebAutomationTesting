# Web Automation Framework

A production-grade web automation testing framework built with Python, Selenium, and pytest.

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![Selenium](https://img.shields.io/badge/selenium-latest-green)
![pytest](https://img.shields.io/badge/pytest-latest-orange)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

---

## 🎯 Features

### Core Framework
- ✅ **Page Object Model (POM)** - Maintainable test architecture
- ✅ **Data-Driven Testing** - CSV-based test data
- ✅ **Multi-Browser Support** - Chrome & Firefox
- ✅ **Headless Execution** - Perfect for CI/CD
- ✅ **Explicit Waits** - Robust, reliable tests

### Reporting & Debugging
- 📊 **HTML Reports** - Beautiful, self-contained reports
- 📸 **Screenshot on Failure** - Automatic failure capture
- 📝 **Comprehensive Logging** - DEBUG & INFO levels
- 🔍 **Detailed Artifacts** - Reports, logs, screenshots

### CI/CD Integration
- 🚀 **GitHub Actions** - Automated testing on every push
- ☁️ **Cloud Execution** - Ubuntu-based CI pipeline
- 📦 **Artifact Storage** - Downloadable test results
- ⚡ **Fast Feedback** - Results in minutes

---

## 📁 Project Structure

```
web_automation_framework/
├── .github/
│   └── workflows/
│       └── main.yml          # GitHub Actions CI/CD workflow
├── pages/
│   ├── __init__.py
│   ├── LoginPage.py          # Login page object
│   ├── InventoryPage.py      # Products page object
│   └── CheckoutFlowPage.py   # Checkout flow pages
├── tests/
│   ├── conftest.py           # pytest fixtures & hooks
│   ├── test_login.py         # Login test cases
│   └── test_checkout.py      # E2E checkout test
├── utils/
│   ├── __init__.py
│   ├── BasePage.py           # Base page with common methods
│   └── DataUtils.py          # Data reading utilities
├── data/
│   └── login_data.csv        # Test data files
├── config/                   # Configuration files
├── reports/                  # Generated HTML reports
│   └── screenshots/          # Failure screenshots
├── logs/                     # Test execution logs
├── pytest.ini                # pytest configuration
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository:**
```bash
git clone <your-repo-url>
cd web_automation_framework
```

2. **Create virtual environment:**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

4. **Verify installation:**
```bash
pytest --version
```

---

## 🧪 Running Tests

### Run All Tests
```bash
pytest
```

### Run Specific Test File
```bash
pytest tests/test_login.py
```

### Run Tests by Marker
```bash
pytest -m smoke       # Critical path tests
pytest -m login       # Login tests only
pytest -m checkout    # Checkout tests only
```

### Run with Different Browser
```bash
pytest --browser=firefox
```

### Run in Headless Mode
```bash
pytest --headless
```

### Combined Options
```bash
pytest -m smoke --browser=chrome --headless -v
```

---

## 📊 Test Reports

After running tests, find generated artifacts in:

- **HTML Report:** `reports/report.html`
- **Log File:** `logs/test_run.log`
- **Screenshots:** `reports/screenshots/` (on failures)

### View HTML Report:
```bash
open reports/report.html  # macOS
# or
start reports/report.html  # Windows
# or
xdg-open reports/report.html  # Linux
```

---

## 🎨 Test Cases

### Current Test Coverage

| Test Suite | Test Cases | Description |
|------------|-----------|-------------|
| **Login Tests** | 6 tests | Valid/invalid login scenarios |
| **Checkout Tests** | 1 test | Full E2E checkout flow |
| **Total** | **7 tests** | Complete user journey coverage |

### Test Scenarios

#### Login Tests (`test_login.py`)
- ✅ Valid user login
- ✅ Locked out user
- ✅ Invalid credentials
- ✅ Data-driven from CSV

#### Checkout Test (`test_checkout.py`)
- ✅ Login → Add to cart → Checkout → Complete order
- ✅ Page chaining demonstration
- ✅ Smoke test (critical path)

---

## 🏗️ Architecture

### Design Patterns

#### 1. Page Object Model (POM)
```python
# pages/LoginPage.py
class LoginPage(BasePage):
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    
    def login(self, username, password):
        self.do_send_keys(self.USERNAME_INPUT, username)
        self.do_send_keys(self.PASSWORD_INPUT, password)
        self.do_click(self.LOGIN_BUTTON)
```

#### 2. Page Chaining
```python
# Tests flow naturally
cart_page = inventory_page.go_to_cart()
checkout_page = cart_page.proceed_to_checkout()
```

#### 3. Data-Driven Testing
```python
@pytest.mark.parametrize("username, password, expected", test_data)
def test_login(driver, username, password, expected):
    # Single test, multiple data sets
```

---

## 🔧 Configuration

### pytest.ini
- Test markers (smoke, regression, etc.)
- HTML report settings
- Logging configuration

### conftest.py
- Browser fixture (Chrome/Firefox)
- Screenshot on failure
- Command-line options

---

## 🤝 Contributing

### Adding New Tests

1. **Create Page Object** (if needed):
```bash
touch pages/NewPage.py
```

2. **Add Test File**:
```bash
touch tests/test_new_feature.py
```

3. **Run Tests**:
```bash
pytest tests/test_new_feature.py -v
```

### Code Style

- Follow PEP 8
- Use descriptive names
- Add docstrings
- Keep methods small

---

## 📚 Documentation

- [CI/CD Setup Guide](CICD_SETUP_GUIDE.md) - GitHub Actions configuration
- [Phase 5 Verification](PHASE5_VERIFICATION.md) - Reporting features

---

## 🐛 Troubleshooting

### Tests Failing Locally?

1. **Check browser driver:**
```bash
# webdriver-manager handles this automatically
```

2. **Verify dependencies:**
```bash
pip install -r requirements.txt
```

3. **Check Python version:**
```bash
python --version  # Should be 3.10+
```

### Headless Mode Issues?

```bash
# Test headless locally
pytest --headless -v
```

---

## 📈 CI/CD

This framework includes a **GitHub Actions workflow** that:

1. ✅ Runs on every push to `main`
2. ✅ Runs on every pull request
3. ✅ Generates test reports
4. ✅ Uploads artifacts for 7 days

See [CICD_SETUP_GUIDE.md](CICD_SETUP_GUIDE.md) for setup instructions.

---

## 🎓 Learning Resources

- [Selenium Documentation](https://www.selenium.dev/documentation/)
- [pytest Documentation](https://docs.pytest.org/)
- [Page Object Model](https://www.selenium.dev/documentation/test_practices/encouraged/page_object_models/)
- [GitHub Actions](https://docs.github.com/en/actions)

---

## 📝 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgments

Built following industry best practices for test automation:
- Page Object Model design pattern
- Explicit waits for reliability
- Data-driven testing approach
- Comprehensive logging and reporting
- CI/CD integration

---

## 📧 Support

For questions or issues:
1. Check the documentation
2. Review existing test examples
3. Examine log files and reports

---

**Happy Testing! 🚀**

---

*Built with ❤️ using Python, Selenium, and pytest*
