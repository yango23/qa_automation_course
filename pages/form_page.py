"""Page Object for DemoQA Practice Form page."""
import os
from typing import TYPE_CHECKING

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver


class FormPage:
    """Page Object for DemoQA form page."""

    URL = "https://demoqa.com/automation-practice-form"

    # Locators (id, css or xpath)
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
        """Initialize Page Object.

        Args:
            driver: WebDriver instance
            timeout: Timeout for explicit waits in seconds
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self) -> None:
        """Open form page."""
        self.driver.get(self.URL)
        self.driver.execute_script("window.scrollTo(0, 200);")

    def fill_name(self, first: str, last: str) -> None:
        """Enter first and last name.

        Args:
            first: First name
            last: Last name
        """
        self.wait.until(EC.visibility_of_element_located(self.FIRST_NAME)).send_keys(first)
        self.wait.until(EC.visibility_of_element_located(self.LAST_NAME)).send_keys(last)

    def fill_email(self, email: str) -> None:
        """Enter email address.

        Args:
            email: Email address
        """
        self.wait.until(EC.visibility_of_element_located(self.EMAIL)).send_keys(email)

    def choose_gender(self, gender_text: str) -> None:
        """Select gender by text.

        Args:
            gender_text: Text to select (e.g., "Male", "Female", "Other")
        """
        xpath = (By.XPATH, self.GENDER_LABEL.format(gender=gender_text))
        self.wait.until(EC.element_to_be_clickable(xpath)).click()

    def fill_mobile(self, mobile: str) -> None:
        """Enter phone number.

        Args:
            mobile: Phone number
        """
        self.wait.until(EC.visibility_of_element_located(self.MOBILE)).send_keys(mobile)

    def fill_subject(self, subject: str) -> None:
        """Enter subject.

        Args:
            subject: Subject name
        """
        subject_field = self.wait.until(EC.element_to_be_clickable(self.SUBJECT_INPUT))
        subject_field.click()
        subject_field.send_keys(subject)
        subject_field.send_keys(Keys.RETURN)

    def choose_hobby(self, hobby_text: str) -> None:
        """Select hobby by text.

        Args:
            hobby_text: Text to select (e.g., "Sports", "Reading", "Music")
        """
        xpath = (By.XPATH, self.HOBBY_LABEL.format(hobby=hobby_text))
        self.wait.until(EC.element_to_be_clickable(xpath)).click()

    def upload_picture(self, file_path: str) -> None:
        """Upload image file.

        Args:
            file_path: Path to file for upload

        Raises:
            FileNotFoundError: If file not found
        """
        abs_path = os.path.abspath(file_path)
        if not os.path.exists(abs_path):
            raise FileNotFoundError(f"File not found: {abs_path}")
        self.wait.until(EC.presence_of_element_located(self.UPLOAD)).send_keys(abs_path)

    def fill_address(self, address_text: str) -> None:
        """Enter address.

        Args:
            address_text: Address text
        """
        self.wait.until(EC.visibility_of_element_located(self.ADDRESS)).send_keys(address_text)

    def choose_state_and_city(self, state: str, city: str) -> None:
        """Select state and city.

        DemoQA uses custom selects based on react-select.
        Can enter text in helper input and press Enter.

        Args:
            state: State name
            city: City name
        """
        state_input = self.wait.until(EC.element_to_be_clickable(self.STATE))
        state_input.send_keys(state)
        state_input.send_keys(Keys.RETURN)

        city_input = self.wait.until(EC.element_to_be_clickable(self.CITY))
        city_input.send_keys(city)
        city_input.send_keys(Keys.RETURN)

    def submit(self) -> None:
        """Scroll to button and click submit via JavaScript."""
        button = self.wait.until(EC.element_to_be_clickable(self.SUBMIT_BUTTON))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
        self.driver.execute_script("arguments[0].click();", button)

    def wait_for_modal(self) -> str:
        """Wait for result modal to appear and return title text.

        Returns:
            Modal title text
        """
        title = self.wait.until(EC.visibility_of_element_located(self.MODAL_TITLE)).text
        return title

    def get_modal_table_text(self) -> str:
        """Return result table text.

        Returns:
            Result table text
        """
        return self.wait.until(EC.visibility_of_element_located(self.MODAL_TABLE)).text
