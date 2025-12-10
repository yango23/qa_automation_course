# pages/from_page.py
import os.path
from calendar import firstweekday
from xml.etree.ElementPath import xpath_tokenizer

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import element_to_be_clickable
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class FormPage:
    URL = "https://demoqa.com/automation-practice-form"

    # локаторы (id, css или xpath)
    FIRST_NAME = (By.ID, "firstName")
    LAST_NAME = (By.ID, "lastName")
    EMAIL = (By.ID, "userEmail")
    GENDER_LABEL = "//label[text()='{gender}']"
    MOBILE = (By.ID, "userNumber")
    SUBJECTS = (By.ID, "subjectInput")
    HOBBY_LABEL = "//label[text()='{hobby}']"
    UPLOAD = (By.ID, "uploadPicture")
    ADDRESS = (By.ID, "currentAddress")
    STATE = (By.ID, "react-select-3-input")
    CITY = (By.ID, "react-select-4-input")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, '[id="submit"]')

    MODAL_TITLE = (By.ID, "example-modal-sizes-title-lg")
    MODAL_TABLE = (By.CSS_SELECTOR, ".table-responsive")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        self.driver.get(self.URL)
        self.driver.execute_script("window.scrollTo(0, 200);")

    def fill_name(self, first, last):
        """Вводим имя и фамилию"""
        self.wait.until(EC.visibility_of_element_located(self.FIRST_NAME)).send_keys(first)
        self.driver.find_element(*self.LAST_NAME).send_keys(last)

    def fill_email(self, email):
        self.driver.find_element(*self.EMAIL).send_keys(email)

    def choose_gender(self, gender_text):
        xpath = (By.XPATH, self.GENDER_LABEL.format(gender=gender_text))
        self.wait.until(EC.element_to_be_clickable(xpath)).click()

    def fill_mobile(self, mobile):
        self.driver.find_element(*self.MOBILE).send_keys(mobile)

    SUBJECT_INPUT = (By.ID, "subjectsInput")

    def fill_subject(self, subject):
        """Вводим предмет."""
        subject_field = self.wait.until(EC.element_to_be_clickable(self.SUBJECT_INPUT))
        subject_field.click()
        subject_field.send_keys(subject)
        subject_field.send_keys(Keys.RETURN)

    def choose_hobby(self, hobby_text):
        xpath = (By.XPATH, self.HOBBY_LABEL.format(hobby=hobby_text))
        self.wait.until(EC.element_to_be_clickable(xpath)).click()

    def upload_picture(self, file_path):
        abs_path = os.path.abspath(file_path)
        assert os.path.exists(abs_path), f"File not found: {abs_path}"
        self.driver.find_element(*self.UPLOAD).send_keys(abs_path)

    def fill_adress(self, adress_text):
        self.driver.find_element(*self.ADDRESS).send_keys(adress_text)

    def choose_state_and_city(self, state, city):
        """
        Выбор State и City: demoqa использует кастомные селекты на базе react-select.
        Можно ввести текст в вспомогательный input и нажать Enter.
        """
        s_input = self.driver.find_element(*self.STATE)
        s_input.send_keys(state)
        s_input.send_keys("\n")

        c_input = self.driver.find_element(*self.CITY)
        c_input.send_keys(city)
        c_input.send_keys("\n")

    def submit(self):
        """Прокручиваем до кнопки и жмем сабмит через JavaScript."""
        button = self.wait.until(EC.element_to_be_clickable(self.SUBMIT_BUTTON))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
        self.driver.execute_script("arguments[0].click();", button)

    def wait_for_modal(self):
        """Ждём появления результата и возвращаем текст заголовка."""
        title = self.wait.until(EC.visibility_of_element_located(self.MODAL_TITLE)).text
        return title

    def get_modal_table_text(self):
        """Возвращаем текст таблицы результатов."""
        return self.wait.until(EC.visibility_of_element_located(self.MODAL_TABLE)).text