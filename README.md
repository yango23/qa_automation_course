QA Automation Course — мобильные и веб-автотесты (Python + Appium)
==================================================================

Коротко
-------
- Базовый проект для изучения мобильной (Appium) и веб-автоматизации (Selenium/PyTest) на Python.
- В репозитории хранится только содержимое папки `QA_Automation_course` — она является корнем проекта.
- Уже есть пример E2E веб-теста для формы на DemoQA; мобильные сценарии будут размещаться в `tests/mobile`.

Стек
----
- Python 3.10+  
- PyTest  
- Selenium + webdriver-manager (Chrome)  
- Appium Python Client (для мобильных тестов) + Node.js / Appium Server 2.x  

Структура
---------
- `pages/` — Page Object’ы, например `form_page.py` для demoqa.com.
- `tests/web/` — веб-тесты, пример `test_form_demoqa.py`.
- `tests/mobile/` — будущие мобильные тесты (Appium).
- `tests/resources/` — тестовые данные/файлы (используется для загрузки файла в форме).
- `conftest.py` — фикстуры PyTest (инициализация браузера).
- `requirements.txt` — список зависимостей.

Подготовка окружения
--------------------
1) Установите Python 3.10+ и Node.js LTS.  
2) (Рекомендуется) Создайте и активируйте виртуальное окружение.  
3) Установите зависимости Python:
   ```
   pip install -r requirements.txt
   ```
4) Установите Appium Server 2.x и драйверы (для мобильных тестов):
   ```
   npm install -g appium appium-doctor
   appium driver install uiautomator2   # пример для Android
   appium-doctor --android              # проверка окружения
   ```

Запуск веб-теста DemoQA
-----------------------
1) Убедитесь, что Chrome установлен (драйвер подтянется автоматически через webdriver-manager).  
2) Выполните:
   ```
   pytest tests/web/test_form_demoqa.py -s -v
   ```
   Тест открывает форму DemoQA, заполняет поля, загружает файл из `tests/resources/`, сабмитит и проверяет появление модального окна с результатом.

Мобильные тесты (Appium)
------------------------
- Поместите сценарии в `tests/mobile/`.  
- Перед запуском убедитесь, что Appium Server запущен (`appium`) и девайс/эмулятор доступен.  
- Типовой запуск:
   ```
   pytest tests/mobile -s -v
   ```
  (Подготовьте `desired capabilities` в тестах/фикстурах по нужной платформе.)

Полезные команды Git
--------------------
- Проверить статус: `git status -sb`
- Зафиксировать изменения: `git add -A && git commit -m "Обновить README"`
- Отправить в репозиторий: `git push origin master`

Контакты
--------
Если что-то пойдет не так или нужны дополнительные сценарии — дайте знать, расширим проект.
