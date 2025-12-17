"""Page Object for Network & internet settings screen."""
from __future__ import annotations

from mobile_pages.base_page import BasePage


class NetworkInternetPage(BasePage):
    """Page Object for Network & internet settings screen."""

    # Possible anchors to confirm the screen has actually opened
    ANCHORS = [
        "Network & internet",
        "Internet",
        "Wi-Fi",
        "Mobile network",
    ]

    def wait_loaded(self) -> "NetworkInternetPage":
        """
        Wait for Network & internet screen to open.

        On different Android versions, screen title text may vary, so we check
        multiple options from the ANCHORS list.
        """
        self.wait_any_text_contains(
            self.ANCHORS,
            timeout_msg="Network & internet page did not load",
        )
        return self

    def open_internet(self) -> "NetworkInternetPage":
        """
        Open "Internet" menu item within Network & internet section.

        On standard Android settings, list item titles usually have
        resource-id `android:id/title` and differ only by text.
        """
        self.click_by_id_and_text("android:id/title", "Internet")
        return self
