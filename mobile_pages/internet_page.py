"""Page Object для экрана Internet (после Network & internet)."""
from __future__ import annotations

from mobile_pages.base_page import BasePage


class InternetPage(BasePage):
    """
    Экран 'Internet' может отличаться, поэтому проверяем несколько якорей.
    """

    POSSIBLE_ANCHORS = [
        "Internet",
        "Wi-Fi",        # иногда с необычным дефисом
        "Wi-Fi",
        "Mobile data",
        "SIMs",
    ]

    def wait_loaded(self) -> "InternetPage":
        last_error = None
        for anchor in self.POSSIBLE_ANCHORS:
            try:
                self.wait_text_contains(anchor)
                return self
            except Exception as e:
                last_error = e

        raise AssertionError(
            "Internet page did not load. None of anchors were found."
        ) from last_error