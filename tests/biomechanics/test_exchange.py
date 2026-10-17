import copy
import json
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/biomechanics"))
from kinematics import (
    convert_units,
    flat,
    map_transform,
    matrix,
    reference_offset,
    unmap_transform,
    validate,
)


def rotation(axis, degrees):
    radians = np.deg2rad(degrees)
    c, s = np.cos(radians), np.sin(radians)
    m = np.eye(4)
    if axis == "x":
        m[:3, :3] = [[1, 0, 0], [0, c, -s], [0, s, c]]
    elif axis == "y":
        m[:3, :3] = [[c, 0, s], [0, 1, 0], [-s, 0, c]]
    else:
        m[:3, :3] = [[c, -s, 0], [s, c, 0], [0, 0, 1]]
    return m


def packet():
    return json.loads((ROOT / "research/opensim/mac-pulldown-default.packet.json").read_text())


@pytest.mark.parametrize("file", ["mac-pulldown-default.packet.json", "mac-pulldown-bind.packet.json"])
def test_actual_mac_reference_packets(file):
    data = json.loads((ROOT / "research/opensim" / file).read_text())
    assert not validate(data)
    assert len(data["nodes"]) == 16
    assert {"left", "right"} <= set(data["coverage"]["sides"])
    assert not data["referencePose"]["anatomicallyCalibrated"]


def test_column_major_and_basis_direction():
    m = rotation("z", 90)
    np.testing.assert_allclose(matrix(flat(m)) @ [1, 0, 0, 1], [0, 1, 0, 1], atol=1e-12)
    assert flat(m)[0:3] == pytest.approx([0, 1, 0])


def test_noncommuting_ninety_degree_rotations():
    x, y = rotation("x", 90), rotation("y", 90)
    assert not np.allclose(x @ y, y @ x)
    source = rotation("z", 30)
    np.testing.assert_allclose(map_transform(source, x, y), x @ source @ y, atol=1e-12)
    assert not np.allclose(x @ source @ y, y @ source @ x)


def test_mm_to_metres_does_not_scale_orientation():
    source = rotation("y", 45)
    source[:3, 3] = [1000, -2000, 500]
    output = convert_units(source, .001)
    np.testing.assert_allclose(output[:3, 3], [1, -2, .5])
    np.testing.assert_allclose(output[:3, :3], source[:3, :3])


@pytest.mark.parametrize("angle", [-90, -13, 0, 45, 90, 179])
def test_roundtrip_and_reference_alignment(angle):
    source = rotation("x", angle)
    source[:3, 3] = [.3, -.2, .7]
    a, target_reference = rotation("z", 90), rotation("y", -45)
    a[:3, 3] = [1, 2, 3]
    b = reference_offset(source, target_reference, a)
    result = map_transform(source, a, b)
    np.testing.assert_allclose(result, target_reference, atol=1e-12)
    np.testing.assert_allclose(unmap_transform(result, a, b), source, atol=1e-12)
    assert np.linalg.det(result[:3, :3]) == pytest.approx(1)


def test_mirror_and_negative_unit_conversion_rejected():
    mirror = np.eye(4)
    mirror[0, 0] = -1
    with pytest.raises(ValueError, match="reflection"):
        map_transform(np.eye(4), mirror, np.eye(4))
    with pytest.raises(ValueError):
        convert_units(np.eye(4), -1)


def test_blender_z_up_to_gltf_y_up_conjugation():
    c = rotation("x", -90)
    source = rotation("z", 37)
    source[:3, 3] = [.3, .4, .5]
    converted = map_transform(source, c, np.linalg.inv(c))
    point = np.array([.1, .2, .3, 1])
    np.testing.assert_allclose(converted @ (c @ point), c @ (source @ point), atol=1e-12)
    np.testing.assert_allclose(c @ [0, 0, 1, 0], [0, 1, 0, 0], atol=1e-12)


def test_roundtrip_with_units_and_nonzero_frame_offsets():
    source = rotation("x", 90)
    source[:3, 3] = [1000, 2000, -500]
    a, b = rotation("y", 90), rotation("z", -90)
    b[:3, 3] = [.1, .2, .3]
    mapped = map_transform(source, a, b, .001)
    np.testing.assert_allclose(unmap_transform(mapped, a, b, .001), source, atol=1e-10)


@pytest.mark.parametrize("fault", ["missing-parent", "duplicate", "cycle", "world", "nan", "sha", "mirrored", "units", "joint-set", "time"])
def test_bad_packet_rejected(fault):
    data = copy.deepcopy(packet())
    if fault == "missing-parent":
        data["nodes"][1]["parentId"] = "absent"
    elif fault == "duplicate":
        data["nodes"].append(copy.deepcopy(data["nodes"][0]))
    elif fault == "cycle":
        data["nodes"][0]["parentId"] = data["nodes"][1]["id"]
    elif fault == "world":
        data["nodes"][1]["worldMatrix"][12] += 2
    elif fault == "nan":
        data["nodes"][1]["localMatrix"][0] = float("nan")
    elif fault == "sha":
        data["source"]["sha256"] = "unknown"
    elif fault == "mirrored":
        data["coverage"].update(mirrored=True, independentlyValidated=True)
    elif fault == "units":
        data["coordinates"]["lengthUnit"] = "mm"
    else:
        transforms = {n["id"]: {k: n[k] for k in ["localMatrix", "worldMatrix"]} for n in data["nodes"]}
        if fault == "joint-set":
            transforms.pop(next(iter(transforms)))
        row = {"timeSeconds": 0, "phase": "test", "origin": "operator-specified", "transforms": transforms}
        data["samples"] = [row] if fault == "joint-set" else [row, copy.deepcopy(row)]
    assert validate(data)
