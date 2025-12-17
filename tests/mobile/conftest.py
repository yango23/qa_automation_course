"""Pytest configuration for mobile tests (Appium)."""

import os
from typing import Generator

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options

from mobile_utils.artifacts import dump_visible_texts, save_artifacts


def make_driver() -> webdriver.Remote:
    """
    Create and configure Appium WebDriver for Android.

    All parameters are taken from environment variables (if set),
    or use reasonable default values.
    """
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.device_name = os.getenv("ANDROID_DEVICE_NAME", "Android Emulator")
    options.udid = os.getenv("ANDROID_UDID", "emulator-5554")
    options.no_reset = True  # Don't reinstall app between tests
    options.new_command_timeout = 300  # Session idle timeout in seconds

    # Appium server URL can be overridden via APPIUM_SERVER_URL.
    server_url = os.getenv("APPIUM_SERVER_URL", "http://127.0.0.1:4723")
    driver = webdriver.Remote(server_url, options=options)

    # Important: implicit wait should not be used to avoid interfering with explicit waits.
    driver.implicitly_wait(0)
    return driver


@pytest.fixture
def driver() -> Generator[webdriver.Remote, None, None]:
    """
    Fixture for creating and closing Appium WebDriver.

    - setup: create driver via make_driver();
    - yield: provide it to test;
    - teardown: after test completion, always call driver.quit().
    """
    drv = make_driver()
    try:
        yield drv
    finally:
        # 1) Close Settings so next test always starts clean
        try:
            drv.terminate_app("com.android.settings")
        except Exception:
            # Fallback: force-stop via shell
            try:
                drv.execute_script(
                    "mobile: shell",
                    {"command": "am", "args": ["force-stop", "com.android.settings"]},
                )
            except Exception:
                pass

        # 2) Close Appium session
        drv.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest hook: saves artifacts on test failure.

    If test fails during execution (when == "call"), automatically:
    - takes screenshot of screen;
    - saves current page source;
    - outputs all visible text elements to log.
    """
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        drv = item.funcargs.get("driver")
        if drv:
            save_artifacts(drv, prefix="settings_fail")
            dump_visible_texts(drv)
