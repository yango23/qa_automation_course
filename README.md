QA Automation Course — mobile & web tests (Python, Appium, PyTest)
==================================================================

Overview
--------
Sample project for mobile (Appium) and web (Selenium/PyTest) automation on Python.
Repository root is exactly `QA_Automation_course`; nothing outside is tracked.
Uses GitHub Copilot and Cursor to assist authoring tests.
All code includes clear English comments explaining test steps and Page Object patterns.
Includes a DemoQA E2E web test; mobile scenarios go to `tests/mobile`.

Stack
-----
- Python 3.10+
- PyTest
- Selenium + webdriver-manager (Chrome)
- Appium Python Client + Node.js / Appium Server 2.x

Structure
---------
- `pages/` — Page Objects for web tests (example: `form_page.py` for demoqa.com).
- `mobile_pages/` — Page Objects for mobile tests (Appium).
  - `base_page.py` — base class with common element search methods.
  - `settings_main_page.py` — Android Settings main screen.
  - `network_internet_page.py` — Network & internet screen.
- `mobile_utils/` — utilities for mobile tests (artifacts, screenshots).
- `tests/web/` — web tests, example `test_form_demoqa.py`.
- `tests/mobile/` — mobile tests (Appium), example `test_open_settings.py`.
- `tests/resources/` — test data/files (for form uploads).
- `conftest.py` — common PyTest fixtures.
- `tests/web/conftest.py` — fixtures for web tests (browser).
- `tests/mobile/conftest.py` — fixtures for mobile tests (Appium driver).
- `requirements.txt` — dependencies list.

Setup
-----
1) Install Python 3.10+ and Node.js LTS.  
2) (Recommended) Create and activate a virtual env.  
3) Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```
4) Install Appium Server 2.x and drivers (for mobile):
   ```
   npm install -g appium appium-doctor
   appium driver install uiautomator2   # Android example
   appium-doctor --android              # env check
   ```

Run DemoQA web test
-------------------
1) Ensure Chrome is installed (webdriver-manager pulls driver).  
2) Run:
   ```
   pytest tests/web/test_form_demoqa.py -s -v
   ```
   The test fills DemoQA form, uploads file from `tests/resources/`, submits, and checks the result modal.

Mobile tests (Appium)
---------------------
- Tests are located in `tests/mobile/`.
- Ensure Appium Server is running (`appium`) and device/emulator is available.
- Configure environment variables (optional):
  ```
  ANDROID_DEVICE_NAME="Android Emulator"
  ANDROID_UDID="emulator-5554"
  APPIUM_SERVER_URL="http://127.0.0.1:4723"
  ```
- Run tests:
   ```
   pytest tests/mobile -s -v
   ```
- On test failure, screenshot and page source are automatically saved to `artifacts/` folder.

Git tips
--------
- Status: `git status -sb`
- Commit: `git add -A && git commit -m "Update tests/readme"`
- Push: `git push origin master`

Contacts
--------
If you need additional scenarios or fixes — feel free to reach out, we'll extend the project.
