"""Мобильные тесты для открытия экрана настроек Android."""

from mobile_pages.settings_main_page import SettingsMainPage
from mobile_pages.network_internet_page import NetworkInternetPage
from mobile_utils.artifacts import save_artifacts


def test_open_android_settings(driver) -> None:
    """
    Базовый сценарий:
    1. Открыть системное приложение Settings через shell‑команду (как `adb shell`).
    2. Проверить, не попали ли мы сразу на экран Network & internet.
    3. Если нет — открыть Settings → раздел Network & internet обычным кликом по меню.
    4. Убедиться, что экран Network & internet действительно загрузился.
    5. Сохранить артефакты успешного прогона (скриншот + page source).
    """

    # 1) Открываем Settings через mobile: shell (аналог adb shell)
    driver.execute_script(
        "mobile: shell",
        {"command": "am", "args": ["start", "-a", "android.settings.SETTINGS"]},
    )

    # 2) Быстрый путь: возможно, система сразу открыла нужный экран
    #    Например, если раньше пользователь уже был в Network & internet.
    net = NetworkInternetPage(driver)
    try:
        net.wait_loaded()
        # Если якоря Network & internet нашлись — тест можно считать успешным.
        save_artifacts(driver, prefix="settings_direct_ok")
        return
    except Exception:
        # Иначе игнорируем и идём по "нормальному" сценарию через главный экран.
        pass

    # 3) Обычный путь:
    #    главный экран Settings → клик по пункту "Network & internet".
    settings = SettingsMainPage(driver).wait_loaded()
    settings.open_network_and_internet()

    # 4) После клика по пункту меню ещё раз убеждаемся, что экран Network & internet открыт.
    NetworkInternetPage(driver).wait_loaded()

    # 5) На удачный сценарий тоже полезно сохранять артефакты —
    #    по ним удобно разбирать, как выглядел экран в момент прогона.
    save_artifacts(driver, prefix="settings_ok")