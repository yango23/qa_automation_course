import os
import time
from datetime import datetime

from selenium.webdriver.support.ui import WebDriverWait

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy


ARTIFACTS_DIR = "artifacts"


def save_artifacts(driver, prefix="mobile"):
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    png = os.path.join(ARTIFACTS_DIR, f"{prefix}_{ts}.png")
    xml = os.path.join(ARTIFACTS_DIR, f"{prefix}_{ts}.xml")

    driver.save_screenshot(png)
    with open(xml, "w", encoding="utf-8") as f:
        f.write(driver.page_source)

    print(f"[ARTIFACT] screenshot: {png}")
    print(f"[ARTIFACT] page_source: {xml}")


def dump_visible_texts(driver, limit=60):
    tvs = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")
    texts = [el.text.strip() for el in tvs if el.text and el.text.strip()]
    print("\n===== VISIBLE TEXTS =====")
    for t in texts[:limit]:
        print(repr(t))
    if len(texts) > limit:
        print(f"... +{len(texts) - limit} more")
    print("=========================\n")


def find_text_contains(driver, text: str):
    return driver.find_element(
        AppiumBy.ANDROID_UIAUTOMATOR,
        f'new UiSelector().textContains("{text}")'
    )


def scroll_to_text_contains(driver, text: str):
    ui = (
        'new UiScrollable(new UiSelector().scrollable(true))'
        f'.scrollIntoView(new UiSelector().textContains("{text}"))'
    )
    return driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, ui)


def test_open_android_settings():
    driver = None
    try:
        # 1) Создаём сессию. ВАЖНО: не указываем appPackage/appActivity вообще.
        # Пусть сессия стартует, а Settings откроем через shell-intent (как в adb).
        options = UiAutomator2Options()
        options.platform_name = "Android"
        options.automation_name = "UiAutomator2"
        options.device_name = "Android Emulator"
        options.udid = "emulator-5554"
        options.no_reset = True
        options.new_command_timeout = 300

        driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
        wait = WebDriverWait(driver, 20)

        print("[STEP] start Settings via intent (like adb)")
        # Аналог: adb shell am start -a android.settings.SETTINGS
        driver.execute_script(
            "mobile: shell",
            {
                "command": "am",
                "args": ["start", "-a", "android.settings.SETTINGS"]
            }
        )

        print("[STEP] wait for Settings main anchor: 'Search Settings'")
        # Ждём, пока появится строка поиска
        wait.until(lambda d: find_text_contains(d, "Search Settings"))

        dump_visible_texts(driver)

        print("[STEP] find & click 'Network & internet'")
        # На твоём скрине есть "Network & internet"
        try:
            el = find_text_contains(driver, "Network & internet")
        except Exception:
            # если вдруг не видно (на других устройствах/масштабах) — скроллим
            el = scroll_to_text_contains(driver, "Network & internet")

        el.click()

        print("[OK] clicked Network & internet")
        time.sleep(2)

    except Exception:
        if driver:
            save_artifacts(driver, prefix="settings_fail")
            dump_visible_texts(driver)
        raise
    finally:
        if driver:
            driver.quit()