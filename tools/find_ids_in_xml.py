import sys
from pathlib import Path
import xml.etree.ElementTree as ET


def pick_latest_xml(artifacts_dir: Path) -> Path | None:
    xmls = sorted(artifacts_dir.glob("*.xml"), key=lambda p: p.stat().st_mtime, reverse=True)
    return xmls[0] if xmls else None


def main():
    artifacts = Path("artifacts")

    # 1) Определяем, какой XML читать:
    # - если передали путь аргументом: python tools/find_ids_in_xml.py artifacts\file.xml
    # - иначе берём самый свежий XML из папки artifacts
    if len(sys.argv) >= 2:
        xml_path = Path(sys.argv[1])
    else:
        xml_path = pick_latest_xml(artifacts)

    if not xml_path or not xml_path.exists():
        print("Не найден XML. Запусти тест, чтобы появился artifacts/*.xml")
        print("Или укажи путь явно: python tools/find_ids_in_xml.py artifacts\\xxx.xml")
        return

    print(f"[OK] читаю XML: {xml_path}")

    # 2) Парсим XML (это “снимок” всего экрана)
    root = ET.parse(xml_path).getroot()

    # 3) Собираем элементы, у которых есть хоть какие-то полезные атрибуты
    items = []
    for el in root.iter():
        rid = el.attrib.get("resource-id", "")
        text = el.attrib.get("text", "")
        desc = el.attrib.get("content-desc", "")
        cls = el.attrib.get("class", "")
        if any([rid, text, desc]):
            items.append((rid, text, desc, cls))

    print(f"[INFO] элементов с (resource-id/text/content-desc): {len(items)}")

    # 4) Печатаем примеры (первые 40)
    print("\n--- TOP 40 ---")
    for i, (rid, text, desc, cls) in enumerate(items[:40], start=1):
        print(f"{i:02d}. class={cls!r}")
        if rid:
            print(f"    resource-id: {rid!r}")
        if text:
            print(f"    text: {text!r}")
        if desc:
            print(f"    content-desc: {desc!r}")

    print("\nПодсказка: если хочешь найти конкретное слово, скажи мне какое (например 'Internet'/'Wi-Fi'),")
    print("и я сделаю фильтр, который печатает только совпадения.")


if __name__ == "__main__":
    main()