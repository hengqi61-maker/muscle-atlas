import copy
import json
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/biomechanics"))
from compare_packets import compare
from kinematics import rotation_from_xyzw, validate


def packet(clip="PulldownProbe"):
    return json.loads((ROOT / f"research/opensim/mac-r1/{clip}.packet.json").read_text())


@pytest.mark.parametrize("clip", ["CurlProbe", "PulldownProbe"])
def test_real_r1_keyframes(clip):
    data = packet(clip)
    assert not validate(data)
    assert len(data["nodes"]) == 27
    assert len(data["samples"]) == 5
    assert [s["timeSeconds"] for s in data["samples"]] == [0, 1, 2, 3, 4]
    assert not data["referencePose"]["anatomicallyCalibrated"]


def mapping():
    return {"status": "uncalibrated-diagnostic", "sourceAnchor": "Thorax", "worldAlignment": np.eye(4).reshape(16).tolist(),
            "pairs": [{"source": "RightScapula", "target": "RightScapula"}, {"source": "RightHumerus", "target": "RightHumerus"}]}


def test_even_identical_pose_does_not_produce_medical_pass():
    data = packet()
    report = compare(data, data, mapping())
    assert report["overallVerdict"] == "INCONCLUSIVE"
    assert not report["mayApproveMotion"]
    assert len(report["rows"]) == 10
    assert max(r["roundtripResidualMaxAbs"] for r in report["calibration"]) < 1e-12


def test_cross_side_mapping_is_rejected():
    profile = mapping()
    profile["pairs"][0]["target"] = "LeftScapula"
    with pytest.raises(ValueError, match="Cross-side"):
        compare(packet(), packet(), profile)


def test_missing_mapping_node_is_rejected():
    profile = mapping()
    profile["pairs"][0]["target"] = "NotPresent"
    with pytest.raises(ValueError, match="Missing/mismatched"):
        compare(packet(), packet(), profile)


def test_attachment_nonfinite_is_rejected():
    data = copy.deepcopy(packet())
    data["attachments"] = [{"muscleId": "test", "pathPointId": "test", "parentFrame": "Thorax", "position_m": [float("nan"), 0, 0],
                            "evidence": {"type": "operator-specified", "confidence": "unvalidated", "uncertainties": ["test fixture"]}}]
    assert validate(data)


def test_quaternion_order_and_sign():
    identity = rotation_from_xyzw([0, 0, 0, 1])
    np.testing.assert_allclose(identity, np.eye(3))
    np.testing.assert_allclose(identity, rotation_from_xyzw([0, 0, 0, -1]))
    assert not np.allclose(identity, rotation_from_xyzw([1, 0, 0, 0]))
    with pytest.raises(ValueError):
        rotation_from_xyzw([0, 0, 0, 0])
