QA Automation Course — mobile & web tests (Python, Appium, PyTest)
==================================================================

EN
--
- Sample project for mobile (Appium) and web (Selenium/PyTest) automation on Python.
- Repository root is exactly `QA_Automation_course`; nothing outside is tracked.
- Uses GitHub Copilot and Cursor to assist authoring tests.
- Includes a DemoQA E2E web test; mobile scenarios go to `tests/mobile`.

RU
--
- Базовый проект для мобильной (Appium) и веб-автоматизации (Selenium/PyTest) на Python.
- Корень репозитория — папка `QA_Automation_course`; лишние каталоги не пушатся.
- Для написания тестов используются GitHub Copilot и Cursor.
- Есть пример E2E веб-теста DemoQA; мобильные кейсы кладём в `tests/mobile`.

Stack / Стек
------------
- Python 3.10+
- PyTest
- Selenium + webdriver-manager (Chrome)
- Appium Python Client + Node.js / Appium Server 2.x

Structure / Структура
---------------------
- `pages/` — Page Object’ы (пример: `form_page.py` для demoqa.com).
- `tests/web/` — веб-тесты, пример `test_form_demoqa.py`.
- `tests/mobile/` — будущие мобильные тесты (Appium).
- `tests/resources/` — тестовые данные/файлы (для загрузки в форме).
- `conftest.py` — фикстуры PyTest (инициализация браузера).
- `requirements.txt` — список зависимостей.

Setup / Подготовка окружения
----------------------------
1) Install Python 3.10+ and Node.js LTS.  
2) (Recommended) Create and activate a virtual env.  
3) Install Python deps:
   ```
   pip install -r requirements.txt
   ```
4) Install Appium Server 2.x and drivers (for mobile):
   ```
   npm install -g appium appium-doctor
   appium driver install uiautomator2   # Android example
   appium-doctor --android              # env check
   ```

Run DemoQA web test / Запуск веб-теста
--------------------------------------
1) Ensure Chrome is installed (webdriver-manager pulls driver).  
2) Run:
   ```
   pytest tests/web/test_form_demoqa.py -s -v
   ```
   The test fills DemoQA form, uploads file from `tests/resources/`, submits, and checks the result modal.

Mobile tests (Appium) / Мобильные тесты
---------------------------------------
- Put scenarios in `tests/mobile/`.  
- Make sure Appium Server is running (`appium`) and device/emulator is available.  
- Typical run:
   ```
   pytest tests/mobile -s -v
   ```
  Prepare desired capabilities in tests/fixtures for your platform.

Git tips / Полезные команды Git
-------------------------------
- Status: `git status -sb`
- Commit: `git add -A && git commit -m "Update tests/readme"`
- Push: `git push origin master`

Contacts / Контакты
-------------------
Если нужны дополнительные сценарии или правки — пишите, расширим проект.
