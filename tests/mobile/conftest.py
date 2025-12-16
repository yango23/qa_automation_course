"""Конфигурация pytest для мобильных тестов (Appium)."""

import os
from typing import Generator

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options

from mobile_utils.artifacts import dump_visible_texts, save_artifacts


def make_driver() -> webdriver.Remote:
    """
    Создаёт и настраивает Appium WebDriver для Android.

    Все параметры берутся из переменных окружения (если заданы),
    либо используют разумные значения по умолчанию.
    """
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.device_name = os.getenv("ANDROID_DEVICE_NAME", "Android Emulator")
    options.udid = os.getenv("ANDROID_UDID", "emulator-5554")
    options.no_reset = True  # не переустанавливаем приложение между тестами
    options.new_command_timeout = 300  # таймаут бездействия сессии в секундах

    # Адрес Appium‑сервера можно переопределить через APPIUM_SERVER_URL.
    server_url = os.getenv("APPIUM_SERVER_URL", "http://127.0.0.1:4723")
    driver = webdriver.Remote(server_url, options=options)

    # Важно: implicit wait лучше не использовать, чтобы не мешать явным ожиданиям.
    driver.implicitly_wait(0)
    return driver


@pytest.fixture
def driver() -> Generator[webdriver.Remote, None, None]:
    """
    Фикстура для создания и закрытия Appium WebDriver.

    - setup: создаём драйвер через make_driver();
    - yield: отдаём его в тест;
    - teardown: по завершении теста гарантированно вызываем driver.quit().
    """
    drv = make_driver()
    yield drv
    drv.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Хук pytest: сохраняет артефакты при падении теста.

    Если тест падает на этапе выполнения (when == "call"), автоматически:
    - делает скриншот экрана;
    - сохраняет текущий page source;
    - выводит в лог все видимые текстовые элементы.
    """
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        drv = item.funcargs.get("driver")
        if drv:
            save_artifacts(drv, prefix="settings_fail")
            dump_visible_texts(drv)