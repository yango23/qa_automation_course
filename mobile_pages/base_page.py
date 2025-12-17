"""Base Page Object class for mobile tests."""
from __future__ import annotations

from typing import TYPE_CHECKING, Iterable

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

from appium.webdriver.common.appiumby import AppiumBy

if TYPE_CHECKING:
    from appium.webdriver.webdriver import WebDriver
    from selenium.webdriver.remote.webelement import WebElement


class BasePage:
    """
    Base class for all Page Objects in mobile tests.

    Provides common operations:
    - driver and explicit wait initialization;
    - element search by text;
    - text-based clicks with auto-scroll;
    - waiting for text to appear on screen.
    """

    def __init__(self, driver: "WebDriver", timeout: int = 20) -> None:
        """
        Initialize base Page Object.

        Args:
            driver: Active Appium WebDriver instance
            timeout: Timeout for explicit waits (seconds)
        """
        self.driver = driver
        # Reuse WebDriverWait for all wait operations
        self.wait = WebDriverWait(driver, timeout)

    # ====== Element Search ======

    def find_text_contains(self, text: str) -> "WebElement":
        """
        Find element by partial text match.

        Note: This search is less stable than by id, but Android Settings screens
        often lack convenient resource-ids, so we use text instead.
        """
        return self.driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiSelector().textContains("{text}")',
        )

    def scroll_to_text_contains(self, text: str) -> "WebElement":
        """
        Scroll list to element with specified text and return it.

        Used when the needed Settings menu item is hidden below the first screen.
        """
        ui = (
            'new UiScrollable(new UiSelector().scrollable(true))'
            f'.scrollIntoView(new UiSelector().textContains("{text}"))'
        )
        return self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, ui)

    def find_by_id_and_text(self, res_id: str, text: str) -> "WebElement":
        """
        Find element in list by combination of `resource-id + visible text`.

        This is more reliable than text-only search.
        Useful for lists where all elements share the same id but have different labels.
        """
        return self.driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector()'
            f'.resourceId("{res_id}")'
            f'.text("{text}")',
        )

    # ====== Actions ======

    def click_text_contains(self, text: str, do_scroll: bool = True) -> "WebElement":
        """
        Click element with specified text.

        Args:
            text: Text to search for element
            do_scroll: If True, try to find without scrolling first,
                       if not found, scroll screen to element.
        """
        try:
            el = self.find_text_contains(text)
        except Exception:
            if not do_scroll:
                # Explicitly notify caller that element was not found
                raise
            el = self.scroll_to_text_contains(text)
        el.click()
        return el

    def click_by_id_and_text(self, res_id: str, text: str) -> "WebElement":
        """
        Click settings list item by `resource-id` and exact `text`.

        Example: All list items have id `android:id/title`,
        but differ only by text ("Internet", "Wi-Fi", etc.).
        """
        el = self.find_by_id_and_text(res_id, text)
        el.click()
        return el

    # ====== Waits ======

    def wait_text_contains(
        self,
        text: str,
        timeout_msg: str | None = None,
    ) -> "WebElement":
        """
        Wait for element with specified text to appear on screen.

        Useful as an "anchor" to confirm that the expected screen has actually opened.
        """
        try:
            return self.wait.until(lambda d: self.find_text_contains(text))
        except TimeoutException as e:
            msg = timeout_msg or f"Timeout waiting for textContains: {text!r}"
            raise TimeoutException(msg) from e

    def wait_any_text_contains(
        self,
        texts: Iterable[str],
        timeout_msg: str | None = None,
    ) -> "WebElement":
        """
        Wait for at least one text from list to appear.

        Useful for different Android versions where screen title may vary slightly
        (e.g., "Network & internet" / "Internet" / "Wi-Fi").
        """
        last_error: Exception | None = None

        def _probe(_driver):
            nonlocal last_error
            for t in texts:
                try:
                    return self.find_text_contains(t)
                except Exception as e:
                    last_error = e
            return False

        try:
            return self.wait.until(_probe)
        except TimeoutException as e:
            msg = timeout_msg or f"Timeout waiting any of: {list(texts)!r}"
            raise TimeoutException(msg) from (last_error or e)
