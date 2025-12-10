# tests/web/test_form_demoqa.py

import os
from pages.form_page import FormPage, FormPage


def test_fill_form_sucsess(browser):
    """
    E2E тест: открыть форму DemoQA, заполнить данные, загрузить файл и проверить результат.
    Шаги:
      setup: фикстура browser создаёт драйвер
      action: заполняем поля и сабмитим
      assert: проверяем, что открыто модальное окно с заголовком "Thanks for submitting the form"
      teardown: driver.quit() — в фикстуре
    """

    page = FormPage(browser)
    page.open()

    #Заполняем поля
    page.fill_name("Ivan","Petrov")
    page.fill_email("invepetrov@ecxample.com")
    page.choose_gender("Male")
    page.fill_mobile("7599172463")
    page.fill_subject("Maths")
    page.choose_hobby("Sports")

    # Создаём небольшой файл для загрузки (в папке tests/resources)
    resources_dir = os.path.join(os.path.dirname(__file__), "..", "resources")
    os.makedirs(resources_dir, exist_ok=True)
    sample_file = os.path.join(resources_dir, "sample_pic.png")
    # создаём пустой файл (или заранее положи картинку туда)
    if not os.path.exists(sample_file):
        with open(sample_file, "wb") as f:
            f.write(b"\x89PNG\r\n\x1a\n")

    page.upload_picture(sample_file)
    page.fill_adress("Test adress 123")
    page.choose_state_and_city("NCR", "Delhi")

    # Сабмит формы
    page.submit()

    # Проверяем, что модальное окно с заголовком появилось
    title = page.wait_for_modal()
    assert "Thanks for submitting the form" in title

    # Дополнительно можно проверить, что в таблице есть наше имя
    table_tesxt = page.get_modal_table_text()
    assert "Ivan Petrov" in table_tesxt
    assert "invepetrov@ecxample.com" in table_tesxt