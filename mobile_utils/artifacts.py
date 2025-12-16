"""Утилиты для сохранения артефактов мобильных тестов.

Сюда относятся:
- скриншоты упавших/успешных сценариев;
- дампы page source;
- список всех видимых текстов на экране.
"""

from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

from appium.webdriver.common.appiumby import AppiumBy

if TYPE_CHECKING:
    from appium.webdriver.webdriver import WebDriver

# Все артефакты складываем в локальную папку "artifacts" рядом с проектом.
ARTIFACTS_DIR = Path("artifacts")


def save_artifacts(driver: "WebDriver", prefix: str = "mobile") -> None:
    """
    Сохраняет скриншот и page source для текущего экрана.

    :param driver: активная сессия Appium WebDriver
    :param prefix: префикс для имени файлов (например, "FAILED" или "settings_ok")
    """
    ARTIFACTS_DIR.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    png_path = ARTIFACTS_DIR / f"{prefix}_{ts}.png"
    xml_path = ARTIFACTS_DIR / f"{prefix}_{ts}.xml"

    # Скриншот экрана.
    driver.save_screenshot(str(png_path))
    # Полный XML текущего экрана.
    xml_path.write_text(driver.page_source, encoding="utf-8")

    print(f"[ARTIFACT] screenshot: {png_path}")
    print(f"[ARTIFACT] page_source: {xml_path}")


def dump_visible_texts(driver: "WebDriver", limit: int = 60) -> None:
    """
    Печатает в консоль все видимые текстовые элементы на экране.

    Это сильно помогает при отладке: можно быстро понять, какие тексты
    реально отрисованы на экране, без ручного "тыкания" в приложение.
    """
    text_views = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")
    texts = [el.text.strip() for el in text_views if el.text and el.text.strip()]

    print("\n===== VISIBLE TEXTS =====")
    for text in texts[:limit]:
        print(repr(text))
    if len(texts) > limit:
        print(f"... +{len(texts) - limit} more")
    print("=========================\n")

