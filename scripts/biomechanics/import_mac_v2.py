"""Read the real Mac producer v0.1, validate all poses, publish compact keyframes."""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from kinematics import flat, matrix, rotation_from_xyzw, validate


def packet(data, raw_hash, producer, clip):
    definitions = {b["name"]: b for b in data["bones"]}

    def observations(rows):
        result = {}
        for row in rows:
            parent = definitions[row["name"]]["parentBone"]
            local, world = matrix(row["localMatrix"]), matrix(row["worldMatrix"])
            # A non-bone armature parent is absorbed into each exported root.
            result[row["name"]] = {"localMatrix": flat(local if parent else world), "worldMatrix": flat(world)}
            if not np.allclose(matrix(row["parentWorldMatrix"]) @ local, world, atol=1e-5):
                raise ValueError(f"Mac parent/world inconsistency: {row['name']}")
            for field in ["localQuaternionXyzw", "worldQuaternionXyzw"]:
                q = np.asarray(row[field])
                if not np.isfinite(q).all() or not np.isclose(np.linalg.norm(q), 1, atol=1e-4):
                    raise ValueError(f"Invalid Mac quaternion {field}: {row['name']}")
                expected = matrix(row["localMatrix"] if field.startswith("local") else row["worldMatrix"])[:3, :3]
                if not np.allclose(rotation_from_xyzw(q), expected, atol=1e-5):
                    raise ValueError(f"Quaternion order/rotation mismatch {field}: {row['name']}")
        return result

    reference = observations(data["reference"])
    nodes = [{"id": name, "parentId": bone["parentBone"],
              "side": "left" if name.startswith("Left") else "right" if name.startswith("Right") else "midline",
              **reference[name], "anatomicalAxesKnown": False} for name, bone in definitions.items()]
    source = data["source"]
    return {"schemaVersion": "1.0.0", "experimentId": "mac-r1-" + clip["name"],
            "source": {"kind": "blender-export", "uri": "git:codex/unified-rig-v2:docs/rig-v2/handoff/mac-observation-v0.1.json",
                       "sha256": raw_hash, "assetSha256": source["modelSha256"], "gitCommit": source["assetCommit"],
                       "producerCommit": producer, "software": "Mac Three " + source["threeVersion"] + "; authored diagnostic clip",
                       "licenseStatus": "Original anatomy terms retained; observation grants no new asset license"},
            "coordinates": {"lengthUnit": "m", "timeUnit": "s", "handedness": "right", "axes": {"x": "glTF numeric X", "y": "glTF up +Y", "z": "glTF numeric Z; anatomical frame uncalibrated"},
                            "matrixStorage": "column-major-16", "vectorConvention": "column-vectors", "transformMeaning": "T_parent_from_local; T_world_from_local", "rotationConvention": "active-right-handed-matrix"},
            "referencePose": {"kind": "default-node", "description": "Mac glTF defaults before mixer; independent inverse-bind and Blender row-major Z-up records not conflated", "anatomicallyCalibrated": False},
            "coverage": {"sides": ["left", "right", "midline"], "mirrored": False, "independentlyValidated": False},
            "evidence": {"type": "script-derived", "confidence": "high-numerical", "uncertainties": ["Authored diagnostic animation, not measured human motion", "No anatomical axis/shoulder-centre calibration or physiological validation", "Nested Blender row-major Z-up rest and attachment data deliberately remain in their original files"]},
            "nodes": nodes,
            "samples": [{"timeSeconds": row["timeSeconds"], "phase": f"authored-{clip['name']}-fraction-{row['phase']}",
                         "origin": "operator-specified", "transforms": observations(row["bones"])} for row in clip["frames"]],
            "attachments": []}


def convert(file, out, producer, expected_hash):
    raw = file.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != expected_hash:
        raise ValueError("Mac handoff SHA256 mismatch")
    data = json.loads(raw)
    if data["format"] != "muscle-atlas.initial-mac-observation" or data["version"] != "0.1.0":
        raise ValueError("Unsupported producer version")
    if data["conventions"]["gltf"]["matrixStorage"] != "column-major flat 16" or data["conventions"]["gltf"]["unit"] != "metre":
        raise ValueError("Explicit producer coordinate convention required")
    out.mkdir(parents=True, exist_ok=True)
    reports = []
    for clip in data["clips"]:
        result = packet(data, digest, producer, clip)
        issues = validate(result)
        if issues:
            raise ValueError(issues[:10])
        count = len(result["samples"])
        indices = clip["fixedPhaseFrameIndices"]
        result["samples"] = [result["samples"][i] for i in indices]
        (out / (clip["name"] + ".packet.json")).write_text(json.dumps(result, separators=(",", ":")) + "\n")
        reports.append({"clip": clip["name"], "validatedFrames": count, "exportedFrames": len(indices),
                        "nodes": len(result["nodes"]), "issues": [], "inputSha256": digest,
                        "assetSha256": result["source"]["assetSha256"], "producerCommit": producer,
                        "scope": "Independent numerical import/serialization check; no anatomy or motion-quality approval"})
    (out / "import-report.json").write_text(json.dumps(reports, indent=2) + "\n")
    print(json.dumps(reports, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--producer-commit", required=True)
    parser.add_argument("--expected-sha256", required=True)
    args = parser.parse_args()
    convert(args.input, args.out, args.producer_commit, args.expected_sha256)
