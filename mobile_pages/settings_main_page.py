"""Page Object для главного экрана настроек Android.

На этом экране обычно отображаются основные разделы системных настроек:
- Network & internet;
- Connected devices;
- Apps и т.д.
"""
from __future__ import annotations

from mobile_pages.base_page import BasePage


class SettingsMainPage(BasePage):
    """Page Object для главного экрана настроек Android."""

    # Якоря: любой из этих текстов означает, что мы действительно на главном экране Settings.
    ANCHORS = [
        "Network & internet",
        "Connected devices",
        "Apps",
        "Notifications",
        "Battery",
        "Storage",
        "Search Settings",  # на Pixel / Android 13 часто есть строка поиска
    ]

    def wait_loaded(self) -> "SettingsMainPage":
        """
        Ждём, пока откроется главный экран Settings.

        Используем несколько возможных текстов-якорей, чтобы покрыть разные версии Android.
        """
        self.wait_any_text_contains(
            self.ANCHORS,
            timeout_msg="Settings main page did not load",
        )
        return self

    def open_network_and_internet(self) -> None:
        """
        Открывает раздел "Network & internet" из главного экрана Settings.

        Если пункт скрыт за пределами первого экрана, метод сам проскроллит до него.
        """
        self.click_text_contains("Network & internet", do_scroll=True)