"""Independent cross-model diagnostic; uncalibrated differences are questions."""
import argparse
import json
from pathlib import Path

import numpy as np
from kinematics import (
    flat,
    map_transform,
    matrix,
    reference_offset,
    unmap_transform,
    validate,
)


def rotation_angle(m):
    return float(np.rad2deg(np.arccos(np.clip((np.trace(m[:3, :3]) - 1) / 2, -1, 1))))


def compare(source, reference, mapping):
    issues = validate(source) + validate(reference)
    if issues:
        raise ValueError(issues[:10])
    src = {n["id"]: n for n in source["nodes"]}
    ref = {n["id"]: n for n in reference["nodes"]}
    a = matrix(mapping["worldAlignment"])
    if mapping["status"] != "uncalibrated-diagnostic":
        raise ValueError("This prototype supports uncalibrated diagnostics only; no medical PASS")
    rows, calibration = [], []
    for pair in mapping["pairs"]:
        source_id, target_id = pair["source"], pair["target"]
        if source_id not in src or target_id not in ref:
            raise ValueError(f"Missing/mismatched node: {source_id} -> {target_id}")
        left, right = src[source_id]["side"], ref[target_id]["side"]
        if left in ["left", "right"] and right in ["left", "right"] and left != right:
            raise ValueError("Cross-side mapping rejected; no mirrored independent validation")
        s0, t0 = matrix(src[source_id]["worldMatrix"]), matrix(ref[target_id]["worldMatrix"])
        offset = reference_offset(s0, t0, a)
        aligned = map_transform(s0, a, offset)
        roundtrip = unmap_transform(aligned, a, offset)
        calibration.append({"source": source_id, "target": target_id, "frameOffset": flat(offset),
                            "referenceResidualMaxAbs": float(np.max(np.abs(aligned - t0))),
                            "roundtripResidualMaxAbs": float(np.max(np.abs(roundtrip - s0))),
                            "status": "Algebraic alignment only; anatomical offset/centre calibration absent"})
        anchor = mapping["sourceAnchor"]
        anchor0 = matrix(src[anchor]["worldMatrix"])
        relative0 = np.linalg.inv(anchor0) @ s0
        for sample in source["samples"]:
            world = matrix(sample["transforms"][source_id]["worldMatrix"])
            anchor_world = matrix(sample["transforms"][anchor]["worldMatrix"])
            relative = np.linalg.inv(anchor_world) @ world
            delta = np.linalg.inv(relative0) @ relative
            rows.append({"time_s": sample["timeSeconds"], "phase": sample["phase"], "source": source_id, "target": target_id,
                         "relativeRotationFromOwnReference_deg": rotation_angle(delta),
                         "relativeOriginDisplacementFromOwnReference_m": float(np.linalg.norm(relative[:3, 3] - relative0[:3, 3])),
                         "verdict": "INCONCLUSIVE", "question": "Anatomical axes, segment proportions, joint centre and matching task not calibrated"})
    source_ids = {p["source"] for p in mapping["pairs"]}
    unsupported = [n for n in src if n not in source_ids]
    return {"schemaVersion": "1.0.0", "sourceAssetSha256": source["source"].get("assetSha256", source["source"]["sha256"]),
            "referenceModelSha256": reference["source"]["sha256"], "mappingStatus": mapping["status"],
            "overallVerdict": "INCONCLUSIVE", "mayApproveMotion": False,
            "calibration": calibration, "rows": rows, "unmappedSourceNodes": unsupported,
            "referencePoseTests": len(reference["samples"]),
            "limitations": ["OpenSim operator sweeps are not corresponding Mac clip phases; no sample-by-sample human error is computed",
                            "Reference alignment is guaranteed algebra, not anatomical validation",
                            "Right model cannot independently validate left limb; forearm/wrist/finger topology differs",
                            "Rigid frames and generic muscle paths cannot certify Blender tissue surfaces or collisions"]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("reference", type=Path)
    parser.add_argument("mapping", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    load = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
    report = compare(load(args.source), load(args.reference), load(args.mapping))
    args.out.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"rows": len(report["rows"]), "overallVerdict": report["overallVerdict"], "mayApproveMotion": False}))
