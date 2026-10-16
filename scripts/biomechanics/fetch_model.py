"""Download one immutable official model, verify bytes; never install plugins."""
import hashlib
import urllib.request
from pathlib import Path

COMMIT = "52094cc61c3e795552c658e34a73d083f4662c6b"
SHA256 = "892bd333a1e1e6a2b77902b54218f12727eefd2306ca82bbda81621c926271fe"
URL = f"https://raw.githubusercontent.com/opensim-org/opensim-core/{COMMIT}/OpenSim/Tests/shared/ThoracoscapularShoulderModel.osim"
DEST = Path(__file__).resolve().parents[2] / "artifacts/opensim-models/ThoracoscapularShoulderModel.osim"

if __name__ == "__main__":
    data = DEST.read_bytes() if DEST.exists() else urllib.request.urlopen(URL, timeout=30).read()
    if hashlib.sha256(data).hexdigest() != SHA256:
        raise ValueError("Model hash mismatch; existing file retained, no silent replacement")
    DEST.parent.mkdir(parents=True, exist_ok=True)
    if not DEST.exists():
        DEST.write_bytes(data)
    print(f"Verified {SHA256} {DEST}")
