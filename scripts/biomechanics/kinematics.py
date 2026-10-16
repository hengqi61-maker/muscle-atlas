"""Muscle Atlas kinematics exchange v1. No anatomical calibration is inferred."""
import json
from itertools import pairwise
from pathlib import Path

import jsonschema
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = ROOT / "schemas/kinematics/packet-v1.schema.json"


def matrix(values):
    """glTF/Three flat column-major representation -> 4x4 ndarray."""
    m = np.asarray(values, dtype=float).reshape((4, 4), order="F")
    if not np.isfinite(m).all() or not np.allclose(m[3], [0, 0, 0, 1], atol=1e-8):
        raise ValueError("Nonfinite/non-affine transform")
    r = m[:3, :3]
    if not np.allclose(r.T @ r, np.eye(3), atol=1e-5) or not np.isclose(np.linalg.det(r), 1, atol=1e-5):
        raise ValueError("Transform must be rigid, right-handed, determinant +1 (no reflection/scale)")
    return m


def flat(m):
    return np.asarray(m).reshape(16, order="F").tolist()


def convert_units(transform, scale):
    if not np.isfinite(scale) or scale <= 0:
        raise ValueError("Positive unit scale required; reflection is not unit conversion")
    result = matrix(flat(transform)).copy()
    result[:3, 3] *= scale
    return result


def map_transform(source, world_alignment, frame_offset, unit_scale=1):
    a, b = matrix(flat(world_alignment)), matrix(flat(frame_offset))
    return a @ convert_units(source, unit_scale) @ b


def unmap_transform(target, world_alignment, frame_offset, unit_scale=1):
    a, b = matrix(flat(world_alignment)), matrix(flat(frame_offset))
    return convert_units(np.linalg.inv(a) @ matrix(flat(target)) @ np.linalg.inv(b), 1 / unit_scale)


def reference_offset(source_reference, target_reference, world_alignment, unit_scale=1):
    a = matrix(flat(world_alignment))
    return np.linalg.inv(convert_units(source_reference, unit_scale)) @ np.linalg.inv(a) @ matrix(flat(target_reference))


def validate(packet):
    issues = [e.json_path + ": " + e.message for e in jsonschema.Draft202012Validator(
        json.loads(SCHEMA.read_text())).iter_errors(packet)]
    if issues:
        return issues
    nodes = packet["nodes"]
    by_id = {n["id"]: n for n in nodes}
    if len(by_id) != len(nodes):
        issues.append("Duplicate node id")
    if packet["coverage"]["sides"] == ["right"] and packet["coverage"]["mirrored"]:
        issues.append("Right-only source cannot become independently validated left data")
    if packet["coverage"]["mirrored"] and packet["coverage"]["independentlyValidated"]:
        issues.append("Mirrored data is never independent validation")
    for node in nodes:
        parent = node["parentId"]
        if parent is not None and parent not in by_id:
            issues.append(f"Missing parent {parent} for {node['id']}")
        seen = {node["id"]}
        while parent in by_id:
            if parent in seen:
                issues.append(f"Hierarchy cycle at {node['id']}")
                break
            seen.add(parent)
            parent = by_id[parent]["parentId"]
    for label, transforms in [("reference", {n["id"]: n for n in nodes})] + [
            (str(s["timeSeconds"]), s["transforms"]) for s in packet["samples"]]:
        if set(transforms) != set(by_id):
            issues.append(f"{label}: exact joint set required (missing/mismatched joint)")
            continue
        for name, tr in transforms.items():
            try:
                local, world = matrix(tr["localMatrix"]), matrix(tr["worldMatrix"])
                parent = by_id[name]["parentId"]
                expected = matrix(transforms[parent]["worldMatrix"]) @ local if parent in transforms else local
                if not np.allclose(world, expected, atol=1e-5):
                    issues.append(f"{label}: local/world mismatch {name}")
            except (ValueError, TypeError) as error:
                issues.append(f"{label}: {name}: {error}")
    times = [s["timeSeconds"] for s in packet["samples"]]
    if not all(np.isfinite(times)) or any(b <= a for a, b in pairwise(times)):
        issues.append("Sample times must be finite and strictly increasing")
    return issues
