"""Базовый класс для Page Object паттерна в мобильных тестах."""
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
    Базовый класс для всех Page Object в мобильных тестах.

    Здесь собраны самые частые операции:
    - инициализация драйвера и явных ожиданий;
    - поиск элементов по тексту;
    - клики по тексту с автоскроллом;
    - ожидание появления текста на экране.
    """

    def __init__(self, driver: "WebDriver", timeout: int = 20) -> None:
        """
        Инициализация базового Page Object.

        :param driver: живой экземпляр Appium WebDriver
        :param timeout: таймаут для явных ожиданий (секунды)
        """
        self.driver = driver
        # WebDriverWait будем переиспользовать во всех ожиданиях
        self.wait = WebDriverWait(driver, timeout)

    # ====== Поиск элементов ======

    def find_text_contains(self, text: str) -> "WebElement":
        """
        Находит элемент по частичному совпадению текста.

        Важно: такой поиск менее стабильный, чем по id, но в экранах настроек
        Android часто нет удобных resource-id, поэтому используем текст.
        """
        return self.driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiSelector().textContains("{text}")',
        )

    def scroll_to_text_contains(self, text: str) -> "WebElement":
        """
        Прокручивает список до элемента с указанным текстом и возвращает его.

        Используется, когда нужный пункт меню Settings скрыт ниже первого экрана.
        """
        ui = (
            'new UiScrollable(new UiSelector().scrollable(true))'
            f'.scrollIntoView(new UiSelector().textContains("{text}"))'
        )
        return self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, ui)

    def find_by_id_and_text(self, res_id: str, text: str) -> "WebElement":
        """
        Находит элемент в списке по связке `resource-id + видимый текст`.

        Это более надёжный способ, чем поиск только по тексту.
        Полезно для списков, где все элементы имеют одинаковый id, но разный label.
        """
        return self.driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector()'
            f'.resourceId("{res_id}")'
            f'.text("{text}")',
        )

    # ====== Действия ======

    def click_text_contains(self, text: str, do_scroll: bool = True) -> "WebElement":
        """
        Кликает по элементу с указанным текстом.

        :param text: текст, по которому ищем элемент
        :param do_scroll: если True — сначала пробуем найти без скролла,
                          если не нашли — прокручиваем экран до элемента.
        """
        try:
            el = self.find_text_contains(text)
        except Exception:
            if not do_scroll:
                # Явно даём знать вызывающему коду, что элемент не найден
                raise
            el = self.scroll_to_text_contains(text)
        el.click()
        return el

    def click_by_id_and_text(self, res_id: str, text: str) -> "WebElement":
        """
        Кликает по элементу списка настроек по `resource-id` и точному `text`.

        Пример: все пункты списка имеют id `android:id/title`,
        а различаются только текстом ("Internet", "Wi‑Fi" и т.д.).
        """
        el = self.find_by_id_and_text(res_id, text)
        el.click()
        return el

    # ====== Ожидания ======

    def wait_text_contains(
        self,
        text: str,
        timeout_msg: str | None = None,
    ) -> "WebElement":
        """
        Ждёт появления элемента с указанным текстом на экране.

        Удобно использовать как "якорь" того, что нужный экран действительно открылся.
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
        Ждёт появления хотя бы одного текста из списка.

        Полезно для разных версий Android, где заголовок экрана может немного отличаться
        (например, "Network & internet" / "Internet" / "Wi‑Fi").
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