"""Mobile tests for opening Android Settings screen."""

from mobile_pages.settings_main_page import SettingsMainPage
from mobile_pages.network_internet_page import NetworkInternetPage
from mobile_utils.artifacts import save_artifacts


def test_open_android_settings(driver) -> None:
    """
    Basic scenario:
    1. Open system Settings app via shell command (like `adb shell`).
    2. Check if we're already on Network & internet screen.
    3. If not, open Settings -> Network & internet section via menu click.
    4. Verify that Network & internet screen has actually loaded.
    5. Save successful run artifacts (screenshot + page source).
    """

    # 1) Open Settings via mobile: shell (analog of adb shell)
    driver.execute_script(
        "mobile: shell",
        {"command": "am", "args": ["start", "-a", "android.settings.SETTINGS"]},
    )

    # 2) Fast path: system might have opened the target screen directly
    #    For example, if user was previously in Network & internet.
    net = NetworkInternetPage(driver)
    try:
        net.wait_loaded()
        # If Network & internet anchors are found, test can be considered successful.
        save_artifacts(driver, prefix="settings_direct_ok")
        return
    except Exception:
        # Otherwise ignore and proceed with "normal" path via main screen.
        pass

    # 3) Normal path:
    #    Settings main screen -> click "Network & internet" menu item.
    settings = SettingsMainPage(driver).wait_loaded()
    settings.open_network_and_internet()

    # 4) After clicking menu item, verify again that Network & internet screen is open.
    NetworkInternetPage(driver).wait_loaded()

    # 5) It's useful to save artifacts on successful scenarios too —
    #    they help analyze how the screen looked at the moment of test run.
    save_artifacts(driver, prefix="settings_ok")
