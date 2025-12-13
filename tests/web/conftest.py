"""Конфигурация pytest для веб-тестов."""
from typing import Generator

import pytest

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service as ChromeService
    from webdriver_manager.chrome import ChromeDriverManager

    WEB_DEPS_AVAILABLE = True
except ImportError:
    WEB_DEPS_AVAILABLE = False


@pytest.fixture(scope="function")
def browser() -> Generator[webdriver.Chrome, None, None]:
    """Фикстура для создания и закрытия браузера Chrome для веб-тестов.

    Yields:
        Chrome WebDriver instance
    """
    if not WEB_DEPS_AVAILABLE:
        pytest.skip("Web dependencies (selenium, webdriver-manager) are not installed")

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()), options=options
    )
    yield driver
    driver.quit()

