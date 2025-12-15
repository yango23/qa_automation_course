from __future__ import annotations
from mobile_pages.base_page import BasePage


class NetworkInternetPage(BasePage):
    """Page Object для экрана Network & internet."""

    ANCHORS = [
        "Network & internet",
        "Internet",
        "Wi-Fi",
        "Mobile network",
    ]

    def wait_loaded(self) -> "NetworkInternetPage":
        self.wait_any_text_contains(self.ANCHORS, timeout_msg="Network & internet page did not load")
        return self