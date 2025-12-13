"""Page Object для экрана Network & internet в настройках Android."""
from __future__ import annotations

from typing import TYPE_CHECKING

from mobile_pages.base_page import BasePage

if TYPE_CHECKING:
    from appium.webdriver.webdriver import WebDriver


class NetworkInternetPage(BasePage):
    """
    Это уже следующий экран после клика 'Network & internet'.
    Якорь может отличаться по версии Android, поэтому делаем несколько вариантов.
    """

    """Page Object для экрана Network & internet в настройках Android."""

    POSSIBLE_ANCHORS = [
        "Network & internet",
        "Internet",
        "Wi-Fi",  # бывает на разных экранах
        "Mobile network",
    ]

    def wait_loaded(self) -> "NetworkInternetPage":
        """Ждёт загрузки экрана Network & internet.

        Проверяет наличие характерных элементов экрана.
        Якорь может отличаться по версии Android, поэтому проверяем несколько вариантов.

        Returns:
            Self для цепочки вызовов

        Raises:
            AssertionError: Если экран не загрузился (ни один якорь не найден)
        """
        last_error = None
        for anchor in self.POSSIBLE_ANCHORS:
            try:
                self.wait_text_contains(anchor, timeout_msg=None)
                return self
            except Exception as e:
                last_error = e

        # Если ни один якорь не появился
        raise AssertionError(
            "Network & internet page did not load. None of anchors were found."
        ) from last_error

    def open_internet(self) -> "NetworkInternetPage":
        """Открывает раздел 'Internet' (если доступен).

        Returns:
            Self для цепочки вызовов
        """
        self.click_text_contains("Internet", do_scroll=True)
        return self

    def open_wifi(self) -> "NetworkInternetPage":
        """Открывает раздел 'Wi-Fi' (если доступен).

        Returns:
            Self для цепочки вызовов
        """
        self.click_text_contains("Wi-Fi", do_scroll=True)
        return self