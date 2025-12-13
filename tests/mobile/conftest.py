"""Конфигурация pytest для мобильных тестов."""
import os
from typing import Generator

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options

from mobile_utils.artifacts import dump_visible_texts, save_artifacts


def make_driver() -> webdriver.Remote:
    """Создаёт и настраивает Appium WebDriver для Android.

    Returns:
        Настроенный Appium WebDriver instance
    """
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.device_name = os.getenv("ANDROID_DEVICE_NAME", "Android Emulator")
    options.udid = os.getenv("ANDROID_UDID", "emulator-5554")
    options.no_reset = True
    options.new_command_timeout = 300

    # Appium server URL
    server_url = os.getenv("APPIUM_SERVER_URL", "http://127.0.0.1:4723")
    driver = webdriver.Remote(server_url, options=options)

    # Важно: implicit wait лучше не использовать (мешает явным ожиданиям)
    driver.implicitly_wait(0)
    return driver


@pytest.fixture
def driver() -> Generator[webdriver.Remote, None, None]:
    """Фикстура для создания и закрытия Appium WebDriver.

    Yields:
        Appium WebDriver instance
    """
    drv = make_driver()
    yield drv
    drv.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Хук pytest: сохраняет артефакты при падении теста.

    Если тест упал — автоматически сохраняет screenshot + page_source + видимые тексты.
    """
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        drv = item.funcargs.get("driver")
        if drv:
            save_artifacts(drv, prefix="settings_fail")
            dump_visible_texts(drv)