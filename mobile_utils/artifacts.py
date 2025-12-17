"""Utilities for saving mobile test artifacts.

Includes:
- screenshots of failed/successful scenarios;
- page source dumps;
- list of all visible texts on screen.
"""

from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING
import sys

from appium.webdriver.common.appiumby import AppiumBy

if TYPE_CHECKING:
    from appium.webdriver.webdriver import WebDriver

# All artifacts are stored in local "artifacts" folder next to project
ARTIFACTS_DIR = Path("artifacts")


def save_artifacts(driver: "WebDriver", prefix: str = "mobile") -> None:
    """
    Save screenshot and page source for current screen.

    Args:
        driver: Active Appium WebDriver session
        prefix: Prefix for file names (e.g., "FAILED" or "settings_ok")
    """
    ARTIFACTS_DIR.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    png_path = ARTIFACTS_DIR / f"{prefix}_{ts}.png"
    xml_path = ARTIFACTS_DIR / f"{prefix}_{ts}.xml"

    # Screenshot of screen
    driver.save_screenshot(str(png_path))
    # Full XML of current screen
    xml_path.write_text(driver.page_source, encoding="utf-8")

    print(f"[ARTIFACT] screenshot: {png_path}")
    print(f"[ARTIFACT] page_source: {xml_path}")


def dump_visible_texts(driver: "WebDriver", limit: int = 60) -> None:
    """
    Print all visible text elements on screen to console.

    This greatly helps with debugging: quickly see which texts
    are actually rendered on screen without manually tapping the app.
    """
    text_views = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")
    texts = [el.text.strip() for el in text_views if el.text and el.text.strip()]

    print("\n===== VISIBLE TEXTS =====")
    encoding = sys.stdout.encoding or "utf-8"
    for text in texts[:limit]:
        # Protect against UnicodeEncodeError in Windows console (cp1251, etc.)
        safe = text.encode(encoding, errors="replace").decode(encoding)
        print(repr(safe))
    if len(texts) > limit:
        print(f"... +{len(texts) - limit} more")
    print("=========================\n")
