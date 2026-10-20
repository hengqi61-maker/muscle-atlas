"""Run discrete source-surface checks against supplied convex prop triangles."""
import argparse
import hashlib
import json
from pathlib import Path

import jsonschema
import numpy as np
from contact_geometry import convex_planes, triangle_contact

ROOT = Path(__file__).resolve().parents[2]


def rigid(values):
    matrix = np.asarray(values, float).reshape((4, 4), order="F")
    if (not np.isfinite(matrix).all()
            or not np.allclose(matrix[3], [0, 0, 0, 1], atol=1e-7, rtol=0)
            or not np.allclose(matrix[:3, :3].T @ matrix[:3, :3], np.eye(3), atol=1e-6)
            or not np.isclose(np.linalg.det(matrix[:3, :3]), 1., atol=1e-6)):
        raise ValueError("matrix must be proper rigid column-major transform")
    return matrix


def run(packet):
    schema = json.loads((ROOT / "schemas/contact/packet-v1.schema.json").read_text())
    jsonschema.validate(packet, schema)
    results = []
    previous = -float("inf")
    for sample in packet["samples"]:
        time = sample["timeSeconds"]
        if not np.isfinite(time) or time <= previous:
            raise ValueError("sample times must be finite and strictly increasing")
        previous = time
        prop = sample["prop"]
        transform = rigid(prop["worldMatrix"])
        planes = convex_planes(prop["vertices"], prop["triangles"])
        normals = np.array([n for n, _ in planes])
        distances = np.array([d for _, d in planes])
        for hand in sample["hands"]:
            for frame in ["wristWorldMatrix", "palmWorldMatrix"]:
                if hand[frame] is not None:
                    rigid(hand[frame])
                elif hand["frameStatus"] != "unknown":
                    raise ValueError("missing frame must be explicitly unknown")
            for source in hand["sources"]:
                vertices = np.asarray(source["posedWorldVertices"], float)
                triangles = np.asarray(source["triangles"], int)
                if (not np.isfinite(vertices).all() or triangles.min() < 0
                        or triangles.max() >= len(vertices)):
                    raise ValueError("invalid source topology or vertices")
                local = (vertices - transform[:3, 3]) @ transform[:3, :3]
                signed = local @ normals.T - distances
                gaps = signed[triangles].min(axis=1).max(axis=1)
                for index, triangle in enumerate(triangles):
                    result = ({"classification": "disjoint", "gapLowerBoundM": float(gaps[index])}
                              if gaps[index] > packet["toleranceM"] else
                              triangle_contact(local[triangle], planes, packet["toleranceM"]))
                    if "positionM" in result:
                        position = transform[:3, :3] @ result.pop("positionM") + transform[:3, 3]
                        result["positionWorldM"] = position.tolist()
                    results.append({"sourceId": source["sourceId"], "triangleIndex": index,
                                    "timeSeconds": time, "side": hand["side"],
                                    "propId": prop["id"], **result})
    return {"schemaVersion": "1.0.0", "results": results,
            "scope": "discrete triangle surface versus supplied closed convex prop mesh",
            "uncertainty": ["No continuous-time or grasp-quality certification",
                            "No tissue mechanics, force or exact minimum translation depth",
                            "Disjoint surfaces do not exclude a prop enclosed by a closed hand volume",
                            "Tolerance-expanded clipping; gap is separating-plane lower bound only"]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    raw = args.input.read_bytes()
    report = run(json.loads(raw))
    report["inputSha256"] = hashlib.sha256(raw).hexdigest()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
