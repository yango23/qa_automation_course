from mobile_pages.settings_main_page import SettingsMainPage
from mobile_pages.network_internet_page import NetworkInternetPage
from mobile_pages.internet_page import InternetPage
from mobile_utils.artifacts import save_artifacts


def test_open_internet(driver):
    # Открываем Settings через intent
    driver.execute_script(
        "mobile: shell",
        {"command": "am", "args": ["start", "-a", "android.settings.SETTINGS"]}
    )

    # Главный экран Settings
    SettingsMainPage(driver).wait_loaded().open_network_and_internet()

    # Экран Network & internet
    net = NetworkInternetPage(driver).wait_loaded()
    net.open_internet()

    # Экран Internet
    InternetPage(driver).wait_loaded()