import re
import uuid
from datetime import datetime
from pathlib import Path
import xml.etree.ElementTree as ET

from automation.config.config import IVI_MAX_FILES_PER_USER


BASE_DIR = Path(__file__).resolve().parents[2]
TEMPLATE_PATH = BASE_DIR / "input_file" / "ivi" / "template" / "ivi_temp.xml"
GENERATED_DIR = BASE_DIR / "input_file" / "ivi" / "generated"


def build_user_prefix(username: str) -> str:
    local_part = username.split("@")[0].lower()
    cleaned = re.sub(r"[^a-z0-9]", "", local_part)

    if len(cleaned) >= 3:
        return cleaned[:3]

    return cleaned.ljust(3, "x") if cleaned else "usr"


def generate_vin(username: str) -> str:
    user_prefix = build_user_prefix(username)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
    return f"{user_prefix}{timestamp}"


def cleanup_user_files(user_prefix: str) -> None:
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)

    user_files = sorted(
        GENERATED_DIR.glob(f"ivi_{user_prefix}*.xml"),
        key=lambda path: path.stat().st_mtime
    )

    while len(user_files) > IVI_MAX_FILES_PER_USER:
        oldest_file = user_files.pop(0)
        oldest_file.unlink(missing_ok=True)


def create_ivi_file(username: str) -> Path:
    vin = generate_vin(username)
    user_prefix = build_user_prefix(username)

    tree = ET.parse(TEMPLATE_PATH)
    root = tree.getroot()

    vin_element = root.find(".//VehicleIdentificationNumber")
    if vin_element is not None:
        vin_element.text = vin

    ref_element = root.find(".//IVIReferenceId")
    if ref_element is not None:
        ref_element.text = str(uuid.uuid4())

    filename = f"ivi_{vin}.xml"
    output_path = GENERATED_DIR / filename

    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    tree.write(output_path, encoding="utf-8", xml_declaration=True)

    cleanup_user_files(user_prefix)

    return output_path


if __name__ == "__main__":
    test_username = "buttters@ext.dmz"
    output = create_ivi_file(test_username)
    print("Generált fájl:", output)