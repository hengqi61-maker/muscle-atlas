import hashlib
import json
import struct
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/biomechanics"))
from verify_mac_glb import verify


def fixture(tmp_path):
    doc = {"asset": {"version": "2.0"}, "nodes": [{"name": "Joint", "translation": [1, 2, 3]}], "skins": [{"joints": [0]}]}
    body = json.dumps(doc).encode()
    body += b" " * (-len(body) % 4)
    raw = struct.pack("<4sIIII", b"glTF", 2, len(body) + 20, len(body), 0x4E4F534A) + body
    file = tmp_path / "fixture.glb"
    file.write_bytes(raw)
    world = np.eye(4)
    world[:3, 3] = [1, 2, 3]
    packet = {"referencePose": {"kind": "default-node"}, "source": {"assetSha256": hashlib.sha256(raw).hexdigest()},
              "nodes": [{"id": "Joint", "worldMatrix": world.reshape(16, order="F").tolist()}]}
    return file, packet


def test_independent_trs_matches(tmp_path):
    file, packet = fixture(tmp_path)
    assert verify(file, packet)["maximumWorldMatrixDifference"] == 0


def test_wrong_asset_hash_rejected(tmp_path):
    file, packet = fixture(tmp_path)
    packet["source"]["assetSha256"] = "0" * 64
    with pytest.raises(ValueError, match="hash"):
        verify(file, packet)


def test_self_consistent_packet_cannot_override_actual_glb(tmp_path):
    file, packet = fixture(tmp_path)
    packet["nodes"][0]["worldMatrix"][12] = 8
    with pytest.raises(ValueError, match="differs"):
        verify(file, packet)
