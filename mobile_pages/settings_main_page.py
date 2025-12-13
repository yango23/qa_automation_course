"""Page Object для главного экрана настроек Android."""
from __future__ import annotations

from typing import TYPE_CHECKING

from mobile_pages.base_page import BasePage

if TYPE_CHECKING:
    from appium.webdriver.webdriver import WebDriver


class SettingsMainPage(BasePage):
    """Page Object для главного экрана настроек Android."""

    def wait_loaded(self) -> "SettingsMainPage":
        """Ждёт загрузки экрана настроек.

        Проверяет наличие характерных элементов главного экрана настроек.

        Returns:
            Self для цепочки вызовов

        Raises:
            TimeoutException: Если экран не загрузился
        """
        # Проверяем наличие характерных элементов главного экрана
        possible_anchors = [
            "Network & internet",
            "Connected devices",
            "Apps",
            "Notifications",
            "Battery",
            "Storage",
        ]
        last_error = None
        for anchor in possible_anchors:
            try:
                self.wait_text_contains(anchor, timeout_msg=None)
                return self
            except Exception as e:
                last_error = e

        # Если ни один якорь не появился, но экран может быть загружен
        # Проверяем наличие любого текста на экране
        try:
            self.wait_text_contains("Settings", timeout_msg=None)
            return self
        except Exception:
            if last_error:
                raise AssertionError(
                    "Settings main page did not load. None of anchors were found."
                ) from last_error
            raise

    def open_network_and_internet(self) -> None:
        """Открывает раздел 'Network & internet'.

        Returns:
            None (переход на следующий экран)
        """
        self.click_text_contains("Network & internet", do_scroll=True)
