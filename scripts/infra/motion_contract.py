"""Validate additive reference/profile metadata and sampled transforms.

No automatic milestone approval and no conversion of rig quaternions to anatomy.
"""
import argparse
import json
import math
import re
from pathlib import Path


def finite_vector(value, size):
    return (isinstance(value, list) and len(value) == size
            and all(isinstance(v, (int, float)) and not isinstance(v, bool)
                    and math.isfinite(v) for v in value))


def validate(document, profile):
    errors = []
    if document.get("schemaVersion") != 1:
        errors.append("schemaVersion must be 1")
    for field, length in [("candidateCommit", 40), ("assetSha256", 64)]:
        if not re.fullmatch(rf"[0-9a-f]{{{length}}}", document.get(field, "")):
            errors.append(f"invalid {field}")
    if document.get("coordinateFrame") != "glb-model-y-up-metres":
        errors.append("explicit model frame required; scene coordinates cannot be mixed")
    joints = profile.get("requiredJoints", [])
    if not joints or len(set(joints)) != len(joints):
        errors.append("profile requires distinct requiredJoints")
    references = profile.get("references", [])
    ids = [r.get("id") for r in references]
    if len(set(ids)) != len(ids):
        errors.append("duplicate reference id")
    for ref in references:
        for field in ["id", "title", "url", "accessed", "evidenceType", "supports", "doesNotSupport"]:
            if not ref.get(field):
                errors.append(f"reference missing {field}")
        if ref.get("evidenceType") not in ["primary-abstract", "primary-fulltext", "engineering-invariant", "measured-dataset"]:
            errors.append("unknown evidenceType")
    for limit in profile.get("angleLimits", []):
        if (limit.get("referenceId") not in ids
                or not limit.get("angleDefinition") or not limit.get("applicability")):
            errors.append("range requires reference, angleDefinition and applicability")
        if not finite_vector(limit.get("range_deg"), 2) or limit["range_deg"][0] > limit["range_deg"][1]:
            errors.append("invalid angle range")
    rows = document.get("samples", [])
    if not isinstance(rows, list) or len(rows) < 21:
        return errors + ["at least 21 samples required"]
    previous = None
    for index, row in enumerate(rows):
        time = row.get("time_s")
        if not finite_vector([time], 1) or time < 0 or (previous is not None and time <= previous):
            errors.append(f"sample {index}: invalid/nonincreasing time")
        if finite_vector([time], 1):
            previous = time
        transforms = row.get("joints", {})
        for name in joints:
            transform = transforms.get(name, {})
            if not finite_vector(transform.get("position_m"), 3):
                errors.append(f"sample {index}: missing/nonfinite position {name}")
            q = transform.get("quaternion_xyzw")
            if not finite_vector(q, 4) or abs(math.hypot(*q) - 1) > .001:
                errors.append(f"sample {index}: invalid quaternion {name}")
        for limit in profile.get("angleLimits", []):
            angle = row.get("angles_deg", {}).get(limit.get("name"))
            if not finite_vector([angle], 1):
                errors.append(f"sample {index}: missing calibrated angle {limit.get('name')}")
            elif finite_vector(limit.get("range_deg"), 2) and not limit["range_deg"][0] <= angle <= limit["range_deg"][1]:
                errors.append(f"sample {index}: angle outside declared range {limit.get('name')}")
    return errors


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("samples", type=Path)
    parser.add_argument("profile", type=Path)
    args = parser.parse_args()
    issues = validate(json.loads(args.samples.read_text(encoding="utf-8-sig")),
                      json.loads(args.profile.read_text(encoding="utf-8-sig")))
    print(json.dumps({"errors": issues, "scope": "Data contract only; no clinical or milestone approval"}, indent=2))
    raise SystemExit(bool(issues))
