"""Page Object для формы DemoQA Practice Form."""
import os
from typing import TYPE_CHECKING

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver


class FormPage:
    """Page Object для страницы формы DemoQA."""

    URL = "https://demoqa.com/automation-practice-form"

    # Локаторы (id, css или xpath)
    FIRST_NAME = (By.ID, "firstName")
    LAST_NAME = (By.ID, "lastName")
    EMAIL = (By.ID, "userEmail")
    GENDER_LABEL = "//label[text()='{gender}']"
    MOBILE = (By.ID, "userNumber")
    SUBJECT_INPUT = (By.ID, "subjectsInput")
    HOBBY_LABEL = "//label[text()='{hobby}']"
    UPLOAD = (By.ID, "uploadPicture")
    ADDRESS = (By.ID, "currentAddress")
    STATE = (By.ID, "react-select-3-input")
    CITY = (By.ID, "react-select-4-input")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, '[id="submit"]')

    MODAL_TITLE = (By.ID, "example-modal-sizes-title-lg")
    MODAL_TABLE = (By.CSS_SELECTOR, ".table-responsive")

    def __init__(self, driver: "WebDriver", timeout: int = 10) -> None:
        """Инициализация Page Object.

        Args:
            driver: WebDriver instance
            timeout: Timeout для явных ожиданий в секундах
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self) -> None:
        """Открывает страницу формы."""
        self.driver.get(self.URL)
        self.driver.execute_script("window.scrollTo(0, 200);")

    def fill_name(self, first: str, last: str) -> None:
        """Вводит имя и фамилию.

        Args:
            first: Имя
            last: Фамилия
        """
        self.wait.until(EC.visibility_of_element_located(self.FIRST_NAME)).send_keys(first)
        self.wait.until(EC.visibility_of_element_located(self.LAST_NAME)).send_keys(last)

    def fill_email(self, email: str) -> None:
        """Вводит email.

        Args:
            email: Email адрес
        """
        self.wait.until(EC.visibility_of_element_located(self.EMAIL)).send_keys(email)

    def choose_gender(self, gender_text: str) -> None:
        """Выбирает пол по тексту.

        Args:
            gender_text: Текст для выбора (например, "Male", "Female", "Other")
        """
        xpath = (By.XPATH, self.GENDER_LABEL.format(gender=gender_text))
        self.wait.until(EC.element_to_be_clickable(xpath)).click()

    def fill_mobile(self, mobile: str) -> None:
        """Вводит номер телефона.

        Args:
            mobile: Номер телефона
        """
        self.wait.until(EC.visibility_of_element_located(self.MOBILE)).send_keys(mobile)

    def fill_subject(self, subject: str) -> None:
        """Вводит предмет.

        Args:
            subject: Название предмета
        """
        subject_field = self.wait.until(EC.element_to_be_clickable(self.SUBJECT_INPUT))
        subject_field.click()
        subject_field.send_keys(subject)
        subject_field.send_keys(Keys.RETURN)

    def choose_hobby(self, hobby_text: str) -> None:
        """Выбирает хобби по тексту.

        Args:
            hobby_text: Текст для выбора (например, "Sports", "Reading", "Music")
        """
        xpath = (By.XPATH, self.HOBBY_LABEL.format(hobby=hobby_text))
        self.wait.until(EC.element_to_be_clickable(xpath)).click()

    def upload_picture(self, file_path: str) -> None:
        """Загружает файл изображения.

        Args:
            file_path: Путь к файлу для загрузки

        Raises:
            FileNotFoundError: Если файл не найден
        """
        abs_path = os.path.abspath(file_path)
        if not os.path.exists(abs_path):
            raise FileNotFoundError(f"File not found: {abs_path}")
        self.wait.until(EC.presence_of_element_located(self.UPLOAD)).send_keys(abs_path)

    def fill_address(self, address_text: str) -> None:
        """Вводит адрес.

        Args:
            address_text: Текст адреса
        """
        self.wait.until(EC.visibility_of_element_located(self.ADDRESS)).send_keys(address_text)

    def choose_state_and_city(self, state: str, city: str) -> None:
        """Выбирает штат и город.

        DemoQA использует кастомные селекты на базе react-select.
        Можно ввести текст в вспомогательный input и нажать Enter.

        Args:
            state: Название штата
            city: Название города
        """
        state_input = self.wait.until(EC.element_to_be_clickable(self.STATE))
        state_input.send_keys(state)
        state_input.send_keys(Keys.RETURN)

        city_input = self.wait.until(EC.element_to_be_clickable(self.CITY))
        city_input.send_keys(city)
        city_input.send_keys(Keys.RETURN)

    def submit(self) -> None:
        """Прокручивает до кнопки и нажимает сабмит через JavaScript."""
        button = self.wait.until(EC.element_to_be_clickable(self.SUBMIT_BUTTON))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
        self.driver.execute_script("arguments[0].click();", button)

    def wait_for_modal(self) -> str:
        """Ждёт появления модального окна и возвращает текст заголовка.

        Returns:
            Текст заголовка модального окна
        """
        title = self.wait.until(EC.visibility_of_element_located(self.MODAL_TITLE)).text
        return title

    def get_modal_table_text(self) -> str:
        """Возвращает текст таблицы результатов.

        Returns:
            Текст таблицы результатов
        """
        return self.wait.until(EC.visibility_of_element_located(self.MODAL_TABLE)).text