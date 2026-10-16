import copy
import importlib.util
from pathlib import Path

import pytest

spec = importlib.util.spec_from_file_location(
    "contract", Path(__file__).resolve().parents[2] / "scripts/infra/motion_contract.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def fixture():
    data = {"schemaVersion": 1, "candidateCommit": "a" * 40, "assetSha256": "b" * 64,
            "coordinateFrame": "glb-model-y-up-metres",
            "samples": [{"time_s": i / 5, "joints": {"Elbow": {
                "position_m": [0, 0, 0], "quaternion_xyzw": [0, 0, 0, 1]}}}
                        for i in range(21)]}
    return data, {"requiredJoints": ["Elbow"], "references": [], "angleLimits": []}


def test_valid_and_quaternion_sign_equivalence():
    data, profile = fixture()
    data["samples"][3]["joints"]["Elbow"]["quaternion_xyzw"] = [0, 0, 0, -1]
    assert not module.validate(data, profile)


@pytest.mark.parametrize("fault", ["missing", "nan", "quaternion", "time", "frame", "short", "provenance"])
def test_corrupt_motion_rejected(fault):
    data, profile = fixture()
    if fault == "missing":
        data["samples"][2]["joints"].clear()
    elif fault == "nan":
        data["samples"][2]["joints"]["Elbow"]["position_m"][0] = float("nan")
    elif fault == "quaternion":
        data["samples"][2]["joints"]["Elbow"]["quaternion_xyzw"] = [0, 0, 0, 0]
    elif fault == "time":
        data["samples"][2]["time_s"] = 0
    elif fault == "frame":
        data["coordinateFrame"] = "scene"
    elif fault == "short":
        data["samples"] = data["samples"][:20]
    else:
        data["assetSha256"] = "unverified"
    assert module.validate(data, profile)


def test_declared_ranges_require_support_and_detect_exceedance():
    data, profile = fixture()
    profile["angleLimits"] = [{"name": "synthetic", "range_deg": [0, 10]}]
    assert module.validate(data, profile)
    ref = {"id": "test", "title": "Synthetic fixture", "url": "local:test",
           "accessed": "2026-10-15", "evidenceType": "engineering-invariant",
           "supports": "test interval only", "doesNotSupport": "human angles"}
    profile["references"] = [ref]
    profile["angleLimits"][0].update(referenceId="test", angleDefinition="synthetic scalar",
                                      applicability="test fixture only")
    for row in data["samples"]:
        row["angles_deg"] = {"synthetic": 5}
    assert not module.validate(data, profile)
    broken = copy.deepcopy(data)
    broken["samples"][0]["angles_deg"]["synthetic"] = 20
    assert module.validate(broken, profile)
