"""Tests for DemoQA Practice Form."""

import os
from typing import TYPE_CHECKING

from pages.form_page import FormPage

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver


def test_fill_form_success(browser: "WebDriver") -> None:
    """
    E2E test for filling DemoQA form.

    Main scenario:
    1. Open form page.
    2. Fill all required fields.
    3. Upload test file.
    4. Submit form.
    5. Verify that result modal contains our data.
    """

    # Initialize Page Object and open form page
    page = FormPage(browser)
    page.open()

    # Step 1: Fill main text fields and radio buttons
    page.fill_name("Ivan", "Petrov")
    page.fill_email("ivanpetrov@example.com")
    page.choose_gender("Male")
    page.fill_mobile("7599172463")
    page.fill_subject("Maths")
    page.choose_hobby("Sports")

    # Step 2: Prepare file for upload
    # File is created on-the-fly in tests/resources directory if it doesn't exist
    resources_dir = os.path.join(os.path.dirname(__file__), "..", "resources")
    os.makedirs(resources_dir, exist_ok=True)
    sample_file = os.path.join(resources_dir, "sample_pic.png")
    if not os.path.exists(sample_file):
        # Create minimal "valid" PNG file (header + signature)
        with open(sample_file, "wb") as f:
            f.write(b"\x89PNG\r\n\x1a\n")

    page.upload_picture(sample_file)

    # Step 3: Fill address and dropdown selects "State / City"
    page.fill_address("Test address 123")
    page.choose_state_and_city("NCR", "Delhi")

    # Step 4: Submit form
    page.submit()

    # Step 5: Verify success by modal window title
    title = page.wait_for_modal()
    assert "Thanks for submitting the form" in title

    # Additionally verify table content in modal window
    table_text = page.get_modal_table_text()
    assert "Ivan Petrov" in table_text
    assert "ivanpetrov@example.com" in table_text
