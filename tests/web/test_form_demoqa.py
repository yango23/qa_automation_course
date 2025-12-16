"""Тесты для формы DemoQA Practice Form."""

import os
from typing import TYPE_CHECKING

from pages.form_page import FormPage

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver


def test_fill_form_success(browser: "WebDriver") -> None:
    """
    E2E тест заполнения формы DemoQA.

    Основной сценарий:
    1. Открыть страницу формы.
    2. Заполнить все обязательные поля.
    3. Загрузить тестовый файл.
    4. Отправить форму.
    5. Убедиться, что модальное окно результата содержит наши данные.
    """

    # Инициализируем Page Object и открываем страницу формы.
    page = FormPage(browser)
    page.open()

    # Шаг 1: Заполняем основные текстовые поля и радиокнопки.
    page.fill_name("Ivan", "Petrov")
    page.fill_email("ivanpetrov@example.com")
    page.choose_gender("Male")
    page.fill_mobile("7599172463")
    page.fill_subject("Maths")
    page.choose_hobby("Sports")

    # Шаг 2: Готовим файл для загрузки.
    # Файл создаётся "на лету" в каталоге tests/resources, если его ещё нет.
    resources_dir = os.path.join(os.path.dirname(__file__), "..", "resources")
    os.makedirs(resources_dir, exist_ok=True)
    sample_file = os.path.join(resources_dir, "sample_pic.png")
    if not os.path.exists(sample_file):
        # Создаём минимальный "валидный" PNG‑файл (заголовок + сигнатура).
        with open(sample_file, "wb") as f:
            f.write(b"\x89PNG\r\n\x1a\n")

    page.upload_picture(sample_file)

    # Шаг 3: Заполняем адрес и выпадающие списки "State / City".
    page.fill_address("Test address 123")
    page.choose_state_and_city("NCR", "Delhi")

    # Шаг 4: Сабмитим форму.
    page.submit()

    # Шаг 5: Проверяем успех по заголовку модального окна.
    title = page.wait_for_modal()
    assert "Thanks for submitting the form" in title

    # Дополнительно проверяем содержимое таблицы в модальном окне.
    table_text = page.get_modal_table_text()
    assert "Ivan Petrov" in table_text
    assert "ivanpetrov@example.com" in table_text