"""Independently reconstruct glTF reference matrices without Three/Blender."""
import argparse
import hashlib
import json
import struct
from pathlib import Path

import numpy as np
from kinematics import matrix, rotation_from_xyzw


def verify(file, packet):
    if packet["referencePose"]["kind"] != "default-node":
        raise ValueError("This verifier compares default-node pose only")
    raw = file.read_bytes()
    if hashlib.sha256(raw).hexdigest() != packet["source"]["assetSha256"]:
        raise ValueError("Actual GLB does not match packet asset hash")
    magic, version, length = struct.unpack_from("<4sII", raw)
    if magic != b"glTF" or version != 2 or length != len(raw):
        raise ValueError("Invalid GLB header")
    offset, document = 12, None
    while offset < len(raw):
        size, kind = struct.unpack_from("<II", raw, offset)
        if kind == 0x4E4F534A:
            document = json.loads(raw[offset + 8:offset + 8 + size])
        offset += 8 + size
    nodes, parents = document["nodes"], {}
    for i, node in enumerate(nodes):
        for child in node.get("children", []):
            if child in parents:
                raise ValueError("Multiple glTF parents")
            parents[child] = i
    names = {n.get("name"): i for i, n in enumerate(nodes) if "name" in n}
    cache = {}

    def world(i, visited=None):
        if i in cache:
            return cache[i]
        visited = set() if visited is None else visited
        if i in visited:
            raise ValueError("glTF cycle")
        visited = visited | {i}
        node = nodes[i]
        if "matrix" in node:
            local = np.asarray(node["matrix"]).reshape((4, 4), order="F")
        else:
            local = np.eye(4)
            local[:3, :3] = rotation_from_xyzw(node.get("rotation", [0, 0, 0, 1])) @ np.diag(node.get("scale", [1, 1, 1]))
            local[:3, 3] = node.get("translation", [0, 0, 0])
        cache[i] = world(parents[i], visited) @ local if i in parents else local
        return cache[i]

    errors = {n["id"]: float(np.max(np.abs(world(names[n["id"]]) - matrix(n["worldMatrix"])))) for n in packet["nodes"]}
    if max(errors.values()) > 1e-5:
        raise ValueError(f"GLB reference differs from exported observation: {errors}")
    skins = document.get("skins", [])
    return {"method": "Independent Python glTF JSON/TRS reconstruction; no Three/Blender evaluation", "glbSha256": hashlib.sha256(raw).hexdigest(),
            "skins": len(skins), "jointPaletteSizes": [len(s["joints"]) for s in skins],
            "sourceNodes": sum(bool(n.get("extras", {}).get("sourceName")) for n in nodes),
            "jointsCompared": len(errors), "maximumWorldMatrixDifference": max(errors.values()),
            "scope": "Default node reference only; animation interpolation, weights and soft-tissue quality are separate"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("glb", type=Path)
    parser.add_argument("packet", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = verify(args.glb, json.loads(args.packet.read_text()))
    args.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result))
