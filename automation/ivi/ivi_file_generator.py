from pathlib import Path
from datetime import datetime
import random
import re
import uuid

from automation.config.config import IVI_MAX_FILES_PER_USER

VIN_ALLOWED = "ABCDEFGHJKLMNPRSTUVWXYZ0123456789"  # I,O,Q nélkül

BASE_DIR = Path(__file__).resolve().parents[2]
TEMPLATE_PATH = BASE_DIR / "input_file" / "ivi" / "template" / "ivi_temp.xml"
GENERATED_DIR = BASE_DIR / "input_file" / "ivi" / "generated"


def _generate_vin_17(prefix: str = "WF0") -> str:
    prefix = "".join(ch for ch in prefix.upper() if ch in VIN_ALLOWED)[:3]
    if len(prefix) < 3:
        prefix = (prefix + "WF0")[:3]

    # 3 + 14 = 17
    ts = datetime.now().strftime("%m%d%H%M%S")[-8:]  # 8
    rnd = "".join(random.choice(VIN_ALLOWED) for _ in range(6))  # 6
    return prefix + ts + rnd


def _cleanup_old_files():
    max_keep = max(0, int(IVI_MAX_FILES_PER_USER))
    if max_keep <= 0:
        return

    files = sorted(
        GENERATED_DIR.glob("ivi_*.xml"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,  # legújabb elöl
    )

    # max_keep utániakat töröljük (legrégebbiek)
    for old_file in files[max_keep:]:
        try:
            old_file.unlink()
            print(f"[CLEANUP] Törölve: {old_file.name}")
        except Exception as e:
            print(f"[CLEANUP][HIBA] {old_file.name}: {e}")


def create_ivi_file(username: str = "user") -> Path:
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)

    xml = TEMPLATE_PATH.read_text(encoding="utf-8")
    vin = _generate_vin_17("WF0")
    ref_id = str(uuid.uuid4())

    xml = re.sub(
        r"<VehicleIdentificationNumber>.*?</VehicleIdentificationNumber>",
        f"<VehicleIdentificationNumber>{vin}</VehicleIdentificationNumber>",
        xml,
        count=1,
        flags=re.DOTALL,
    )
    xml = re.sub(
        r"<IVIReferenceId>.*?</IVIReferenceId>",
        f"<IVIReferenceId>{ref_id}</IVIReferenceId>",
        xml,
        count=1,
        flags=re.DOTALL,
    )

    out = GENERATED_DIR / f"ivi_{vin}.xml"
    out.write_text(xml, encoding="utf-8")

    # fájl létrehozás UTÁN cleanup
    _cleanup_old_files()

    return out


#if __name__ == "__main__":
    # Kézi tesztfuttatás:
    # python automation/ivi/ivi_file_generator.py
#    inp = input("Felhasználónév (opcionális, Enter=buttters39764): ").strip()
#    test_user = inp or "buttters39764"

#    generated = create_ivi_file(test_user)

#    print("[OK] IVI fájl legenerálva")
#    print(f"User: {test_user}")
#    print(f"File: {generated}")
#    print(f"Exists: {generated.exists()}")
#    print(f"Max megtartott fájlok (config): {IVI_MAX_FILES_PER_USER}")
