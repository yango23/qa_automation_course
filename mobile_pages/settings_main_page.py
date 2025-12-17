"""Page Object for Android Settings main screen.

This screen typically displays main system settings sections:
- Network & internet;
- Connected devices;
- Apps, etc.
"""
from __future__ import annotations

from mobile_pages.base_page import BasePage


class SettingsMainPage(BasePage):
    """Page Object for Android Settings main screen."""

    # Anchors: any of these texts indicates we're on the Settings main screen
    ANCHORS = [
        "Network & internet",
        "Connected devices",
        "Apps",
        "Notifications",
        "Battery",
        "Storage",
        "Search Settings",  # Often present on Pixel / Android 13
    ]

    def wait_loaded(self) -> "SettingsMainPage":
        """
        Wait for Settings main screen to open.

        Uses multiple possible anchor texts to cover different Android versions.
        """
        self.wait_any_text_contains(
            self.ANCHORS,
            timeout_msg="Settings main page did not load",
        )
        return self

    def open_network_and_internet(self) -> None:
        """
        Open "Network & internet" section from Settings main screen.

        If the item is hidden beyond the first screen, method will auto-scroll to it.
        """
        self.click_text_contains("Network & internet", do_scroll=True)
