"""Базовый класс для Page Object паттерна в мобильных тестах."""
from __future__ import annotations

from typing import TYPE_CHECKING

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

from appium.webdriver.common.appiumby import AppiumBy

if TYPE_CHECKING:
    from appium.webdriver.webdriver import WebDriver
    from selenium.webdriver.remote.webelement import WebElement


class BasePage:
    """Базовый класс для всех Page Object в мобильных тестах."""

    def __init__(self, driver: "WebDriver", timeout: int = 20) -> None:
        """Инициализация базового Page Object.

        Args:
            driver: Appium WebDriver instance
            timeout: Timeout для явных ожиданий в секундах
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # ====== Helpers ======

    def find_text_contains(self, text: str) -> "WebElement":
        """Находит элемент по частичному совпадению текста.

        Args:
            text: Текст для поиска

        Returns:
            Найденный WebElement

        Raises:
            NoSuchElementException: Если элемент не найден
        """
        return self.driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiSelector().textContains("{text}")'
        )

    def scroll_to_text_contains(self, text: str) -> "WebElement":
        """Прокручивает до элемента с указанным текстом.

        Args:
            text: Текст для поиска

        Returns:
            Найденный WebElement после прокрутки

        Raises:
            NoSuchElementException: Если элемент не найден даже после прокрутки
        """
        ui = (
            'new UiScrollable(new UiSelector().scrollable(true))'
            f'.scrollIntoView(new UiSelector().textContains("{text}"))'
        )
        return self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, ui)

    def click_text_contains(self, text: str, do_scroll: bool = True) -> "WebElement":
        """Кликает по элементу с указанным текстом.

        Если элемент не найден и do_scroll=True, пытается прокрутить до него.

        Args:
            text: Текст для поиска
            do_scroll: Прокручивать ли до элемента, если он не найден

        Returns:
            Кликнутый WebElement

        Raises:
            NoSuchElementException: Если элемент не найден
        """
        try:
            el = self.find_text_contains(text)
        except Exception:
            if not do_scroll:
                raise
            el = self.scroll_to_text_contains(text)
        el.click()
        return el

    def wait_text_contains(
        self, text: str, timeout_msg: str | None = None
    ) -> "WebElement":
        """Ждёт появления элемента с указанным текстом на экране.

        Args:
            text: Текст для поиска
            timeout_msg: Кастомное сообщение об ошибке при таймауте

        Returns:
            Найденный WebElement

        Raises:
            TimeoutException: Если элемент не появился в течение timeout
        """
        try:
            return self.wait.until(lambda d: self.find_text_contains(text))
        except TimeoutException as e:
            msg = timeout_msg or f"Timeout waiting for textContains: {text!r}"
            raise TimeoutException(msg) from e