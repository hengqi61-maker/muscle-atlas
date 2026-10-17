"""Adapt the actual Mac raw observation; never invent anatomy or animation samples."""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from kinematics import flat, matrix, validate


def import_observation(file, asset, producer_commit, pose="default-node"):
    raw = file.read_bytes()
    data = json.loads(raw.decode("utf-8-sig"))
    report = next(r for r in data["reports"] if r["path"].endswith(asset))
    if len(report["skins"]) != 1:
        raise ValueError("Exactly one skin required for this adapter; static atlas is not a skeleton")
    joints = report["skins"][0]["joints"]
    names = {b["name"] for b in joints}
    matrices = {b["name"]: matrix(b["world" if pose == "default-node" else "inverseBindDerivedWorld"]["matrixColumnMajor"]) for b in joints}
    nodes = []
    for joint in joints:
        name = joint["name"]
        parent = joint.get("parent") if joint.get("parent") in names else None
        world = matrices[name]
        local = np.linalg.inv(matrices[parent]) @ world if parent else world
        side = "right" if name.startswith("Right") else "left" if name.startswith("Left") or name in ["UpperArm", "Forearm"] else "midline"
        nodes.append({"id": name, "parentId": parent, "side": side, "localMatrix": flat(local),
                      "worldMatrix": flat(world), "anatomicalAxesKnown": False})
    packet = {
        "schemaVersion": "1.0.0", "experimentId": "mac-legacy-" + asset + "-" + pose,
        "source": {"kind": "gltf-observation", "uri": "git:codex/unified-rig-v2:docs/rig-v2/exports/legacy-observations.json",
                   "sha256": hashlib.sha256(raw).hexdigest(), "assetSha256": report["sha256"],
                   "gitCommit": data["commit"], "producerCommit": producer_commit,
                   "software": "Mac Three/glTF raw observation; Windows adapter v1", "licenseStatus": "Source asset terms remain separate; numeric observation only"},
        "coordinates": {"lengthUnit": "m", "timeUnit": "s", "handedness": "right",
                        "axes": {"x": "GLB numeric X; anatomical alignment uncalibrated", "y": "GLB up", "z": "GLB numeric Z"},
                        "matrixStorage": "column-major-16", "vectorConvention": "column-vectors",
                        "transformMeaning": "T_parent_from_local; T_world_from_local", "rotationConvention": "active-right-handed-matrix"},
        "referencePose": {"kind": pose, "description": "Actual Mac observed pose; distinct from animation time0 and anatomical reference", "anatomicallyCalibrated": False},
        "coverage": {"sides": sorted({n["side"] for n in nodes}), "mirrored": False, "independentlyValidated": False},
        "evidence": {"type": "script-derived", "confidence": "high-numerical", "uncertainties": ["Numerical observation only; anatomical axes, attachments and cross-model calibration unknown"]},
        "nodes": nodes, "samples": [], "attachments": []}
    issues = validate(packet)
    if issues:
        raise ValueError(issues)
    return packet


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--asset", default="anatomy-pulldown.glb")
    parser.add_argument("--producer-commit", required=True)
    parser.add_argument("--pose", choices=["default-node", "inverse-bind-derived"], default="default-node")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    packet = import_observation(args.input, args.asset, args.producer_commit, args.pose)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(packet, indent=2) + "\n")
    print(json.dumps({"nodes": len(packet["nodes"]), "issues": [], "pose": args.pose}))
