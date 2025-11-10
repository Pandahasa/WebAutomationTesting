# GitHub Actions CI/CD Setup Guide

## 🚀 Overview

This framework includes a **GitHub Actions workflow** that automatically runs all tests on every push and pull request to the `main` branch.

---

## 📋 Prerequisites

Before the CI/CD pipeline can work, you need to:

1. **Create a GitHub Repository** (if not already done)
2. **Push your code to GitHub**

---

## 🔧 Setup Instructions

### Step 1: Create a GitHub Repository

If you haven't already:

```bash
# Go to GitHub.com and create a new repository
# Then link it to your local repository:

git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git
```

### Step 2: Push Your Code

```bash
# Add all files
git add .

# Commit
git commit -m "Complete: Production-grade web automation framework with CI/CD"

# Push to GitHub (this will trigger the workflow)
git push -u origin main
```

### Step 3: Verify Workflow Runs

1. Go to your GitHub repository
2. Click on the **"Actions"** tab
3. You should see the workflow running!

---

## 🎯 What the Workflow Does

The GitHub Actions workflow (`.github/workflows/main.yml`) performs these steps:

### 1. **Environment Setup**

- ✅ Checks out your code
- ✅ Sets up Python 3.10
- ✅ Caches pip dependencies (faster subsequent runs)

### 2. **Dependency Installation**

- ✅ Installs all Python packages from `requirements.txt`
- ✅ Installs Google Chrome browser

### 3. **Test Execution**

- ✅ Runs: `pytest --browser=chrome --headless`
- ✅ Executes all 7 test cases
- ✅ Generates HTML report and logs

### 4. **Artifact Upload**

- ✅ Saves test reports and logs
- ✅ Available for download for 7 days
- ✅ Runs even if tests fail (for debugging)

---

## 🔔 When the Workflow Runs

The workflow automatically triggers on:

### 1. **Push to Main Branch**

```bash
git push origin main
```

Every push automatically runs all tests.

### 2. **Pull Requests to Main**

```bash
# Create a PR on GitHub
```

Tests run before code can be merged.

### 3. **Manual Trigger**

- Go to "Actions" tab on GitHub
- Select "Web Automation Test Suite CI"
- Click "Run workflow"

---

## 📊 Viewing Test Results

### In GitHub Actions:

1. **Go to Actions Tab** → Click on the workflow run
2. **View Logs** → See detailed test execution
3. **Check Status** → ✅ Green = All Pass, ❌ Red = Failures

### Download Test Artifacts:

1. Scroll to bottom of workflow run
2. Look for **"Artifacts"** section
3. Download **"pytest-test-artifacts"**
4. Unzip to see:
   - `reports/report.html` - Full HTML test report
   - `logs/test_run.log` - Detailed execution log
   - `reports/screenshots/` - Screenshots of failures

---

## 🎨 CI/CD Status Badge (Optional)

Add a status badge to your `README.md`:

```markdown
![CI Tests](https://github.com/YOUR-USERNAME/YOUR-REPO/actions/workflows/main.yml/badge.svg)
```

This shows the current test status in your README!

---

## 🛠️ Troubleshooting

### Tests Pass Locally But Fail in CI?

**Common causes:**

1. **Environment differences:**

   - CI uses Ubuntu, you might use macOS/Windows
   - Solution: Test locally with `--headless` flag

2. **Timing issues:**

   - CI might be slower
   - Solution: Increase wait times in `BasePage`

3. **Display issues:**
   - Headless mode behaves differently
   - Solution: Add headless-specific Chrome options

### How to Test Locally Like CI:

```bash
# Run tests exactly as CI does
pytest --browser=chrome --headless
```

---

## ⚙️ Customization

### Change Python Version:

Edit `.github/workflows/main.yml`:

```yaml
- name: Set up Python 3.10
  uses: actions/setup-python@v5
  with:
    python-version: "3.11" # Change to 3.11, 3.12, etc.
```

### Add Firefox Testing:

```yaml
- name: Install Firefox
  run: |
    sudo apt-get update
    sudo apt-get install -y firefox

- name: Run Pytest with Firefox
  run: |
    pytest --browser=firefox --headless
```

### Run Only Smoke Tests:

```yaml
- name: Run Pytest
  run: |
    pytest -m smoke --browser=chrome --headless
```

### Run on Schedule:

Add to the `on:` section:

```yaml
on:
  schedule:
    - cron: "0 0 * * *" # Run daily at midnight
```

---

## 📈 Advanced Features

### Parallel Test Execution:

Install pytest-xdist:

```bash
pip install pytest-xdist
```

Update workflow:

```yaml
- name: Run Pytest
  run: |
    pytest -n auto --browser=chrome --headless
```

### Matrix Testing (Multiple Browsers/Versions):

```yaml
strategy:
  matrix:
    python-version: ["3.9", "3.10", "3.11"]
    browser: ["chrome", "firefox"]
```

---

## 🎓 Learning Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [pytest Documentation](https://docs.pytest.org/)
- [Selenium with CI/CD](https://www.selenium.dev/documentation/test_practices/encouraged/continuous_integration/)

---

## ✅ Success Checklist

After pushing to GitHub, verify:

- [ ] Workflow appears in "Actions" tab
- [ ] Tests run automatically
- [ ] HTML report is generated
- [ ] Artifacts are uploaded
- [ ] Status badge shows in README (optional)
- [ ] Pull requests show test results

---

## 🎉 You Did It!

Your web automation framework is now **production-ready** with:

- ✅ Automated testing on every commit
- ✅ Cloud-based execution
- ✅ Detailed reports and logs
- ✅ Screenshot capture on failures
- ✅ Zero manual intervention needed

**Welcome to modern DevOps! 🚀**
