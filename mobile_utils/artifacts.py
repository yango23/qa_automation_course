"""Утилиты для сохранения артефактов тестирования (скриншоты, page source)."""
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

from appium.webdriver.common.appiumby import AppiumBy

if TYPE_CHECKING:
    from appium.webdriver.webdriver import WebDriver

ARTIFACTS_DIR = Path("artifacts")


def save_artifacts(driver: "WebDriver", prefix: str = "mobile") -> None:
    """Сохраняет скриншот и page source для отладки.

    Args:
        driver: Appium WebDriver instance
        prefix: Префикс для имен файлов (по умолчанию "mobile")
    """
    ARTIFACTS_DIR.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    png_path = ARTIFACTS_DIR / f"{prefix}_{ts}.png"
    xml_path = ARTIFACTS_DIR / f"{prefix}_{ts}.xml"

    driver.save_screenshot(str(png_path))
    xml_path.write_text(driver.page_source, encoding="utf-8")

    print(f"[ARTIFACT] screenshot: {png_path}")
    print(f"[ARTIFACT] page_source: {xml_path}")


def dump_visible_texts(driver: "WebDriver", limit: int = 60) -> None:
    """Выводит в консоль видимые тексты с экрана для отладки.

    Args:
        driver: Appium WebDriver instance
        limit: Максимальное количество текстов для вывода
    """
    text_views = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")
    texts = [el.text.strip() for el in text_views if el.text and el.text.strip()]

    print("\n===== VISIBLE TEXTS =====")
    for text in texts[:limit]:
        print(repr(text))
    if len(texts) > limit:
        print(f"... +{len(texts) - limit} more")
    print("=========================\n")