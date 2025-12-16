from __future__ import annotations

from mobile_pages.base_page import BasePage


class NetworkInternetPage(BasePage):
    """Page Object для экрана раздела настроек *Network & internet*."""

    # Возможные якоря, по которым можно понять, что экран действительно открылся.
    ANCHORS = [
        "Network & internet",
        "Internet",
        "Wi-Fi",
        "Mobile network",
    ]

    def wait_loaded(self) -> "NetworkInternetPage":
        """
        Ждём, пока откроется экран Network & internet.

        На разных версиях Android текст заголовка может отличаться, поэтому
        проверяем сразу несколько вариантов из списка ANCHORS.
        """
        self.wait_any_text_contains(
            self.ANCHORS,
            timeout_msg="Network & internet page did not load",
        )
        return self

    def open_internet(self) -> "NetworkInternetPage":
        """
        Открывает пункт меню "Internet" внутри раздела Network & internet.

        На стандартных настройках Android заголовки пунктов списка обычно имеют
        resource-id `android:id/title`, а различаются только текстом.
        """
        self.click_by_id_and_text("android:id/title", "Internet")
        return self