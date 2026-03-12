import json
import uuid
from datetime import datetime
from pathlib import Path
import xml.etree.ElementTree as ET


VIN_PREFIX = "WF0EXXSK1AU"

BASE_DIR = Path(__file__).resolve().parents[2]
TEMPLATE_PATH = BASE_DIR / "input_file" / "ivi" / "template" / "ivi_temp.xml"
GENERATED_DIR = BASE_DIR / "input_file" / "ivi" / "generated"
STATE_PATH = BASE_DIR / "input_file" / "ivi" / "ivi_state.json"

def get_next_counter() -> int:
    if not STATE_PATH.exists():
        STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
        STATE_PATH.write_text('{"last_counter": 0}', encoding="utf-8")

    with open(STATE_PATH, "r", encoding="utf-8") as f:
        state = json.load(f)

    last_counter = state.get("last_counter", 0)
    next_counter = last_counter + 1

    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump({"last_counter": next_counter}, f, indent=2)

    return next_counter

def generate_next_vin(counter: int) -> str:
    serial = str(counter).zfill(6)
    return f"{VIN_PREFIX}{serial}"


def create_ivi_file() -> Path:
    counter = get_next_counter()
    vin = generate_next_vin(counter)

    tree = ET.parse(TEMPLATE_PATH)
    root = tree.getroot()

    vin_element = root.find(".//VehicleIdentificationNumber")
    if vin_element is not None:
        vin_element.text = vin

    ref_element = root.find(".//IVIReferenceId")
    if ref_element is not None:
        ref_element.text = str(uuid.uuid4())

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = f"ivi_{timestamp}_{vin}.xml"
    output_path = GENERATED_DIR / filename

    GENERATED_DIR.mkdir(parents=True, exist_ok=True)

    tree.write(output_path, encoding="utf-8", xml_declaration=True)

    return output_path

if __name__ == "__main__":
    output = create_ivi_file()
    print("Generált fájl:", output)