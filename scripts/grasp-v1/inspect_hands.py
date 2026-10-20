"""G0: inspect actual R1 copy hand meshes, bones, and weights. Read-only."""
import bpy, json, hashlib
from pathlib import Path
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "artifacts" / "grasp-v1"
OUT.mkdir(parents=True, exist_ok=True)
src = ROOT / "public" / "experimental" / "rig-v2" / "unified-rig-prototype.glb"
assert src.is_file()
sha = hashlib.sha256(src.read_bytes()).hexdigest()

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(src))

arms = [o for o in bpy.data.objects if o.type == "ARMATURE"]
meshes = [o for o in bpy.data.objects if o.type == "MESH"]
hand_keys = (
    "hand", "pollicis", "lumbrical", "interosse", "digiti minimi",
    "thenar", "hypothenar", "retinaculum", "wrist", "finger",
)
hand_meshes = []
for o in meshes:
    blob = " ".join([o.name, str(o.get("sourceName") or "")]).lower()
    if any(k in blob for k in hand_keys):
        hand_meshes.append(o)

def mesh_info(o):
    xs = [o.matrix_world @ v.co for v in o.data.vertices]
    groups = [g.name for g in o.vertex_groups]
    sample = []
    if o.vertex_groups:
        for vi in range(0, min(len(o.data.vertices), 12)):
            ws = []
            for g in o.vertex_groups:
                try:
                    w = g.weight(vi)
                except RuntimeError:
                    continue
                if w > 1e-6:
                    ws.append({"g": g.name, "w": round(w, 4)})
            sample.append({"v": vi, "w": sorted(ws, key=lambda x: -x["w"])[:4]})
    mins = Vector((min(p.x for p in xs), min(p.y for p in xs), min(p.z for p in xs)))
    maxs = Vector((max(p.x for p in xs), max(p.y for p in xs), max(p.z for p in xs)))
    return {
        "name": o.name,
        "sourceName": o.get("sourceName"),
        "bpId": o.get("bpId"),
        "verts": len(o.data.vertices),
        "polys": len(o.data.polygons),
        "groups": groups,
        "bounds": {"min": list(mins), "max": list(maxs)},
        "weightSample": sample,
    }

bones = []
for arm in arms:
    for b in arm.data.bones:
        bones.append({
            "armature": arm.name,
            "name": b.name,
            "parent": b.parent.name if b.parent else None,
            "deform": b.use_deform,
            "head": list(arm.matrix_world @ b.head_local),
            "tail": list(arm.matrix_world @ b.tail_local),
        })

report = {
    "glbSha256": sha,
    "objectCount": len(bpy.data.objects),
    "meshCount": len(meshes),
    "armatures": [a.name for a in arms],
    "boneCount": len(bones),
    "bones": bones,
    "fingerLikeBones": [b for b in bones if any(k in b["name"].lower() for k in ("finger", "thumb", "index", "middle", "ring", "little", "mcp", "pip", "dip"))],
    "handMeshCount": len(hand_meshes),
    "handMeshes": [mesh_info(o) for o in sorted(hand_meshes, key=lambda o: o.name)],
    "feasibility": {
        "independentDigitsOnFrozen27": False,
        "reason": "Canonical 27 bones end at Hand + non-deform FingerSocket; no MCP/PIP/DIP/CMC bones exist.",
        "skinShellPresent": False,
        "note": "Hand coverage is muscle/tendon sets, not a continuous finger skin. Additive child bones can move spatially partitioned muscle vertices; this is not clinical digit kinematics.",
    },
}
(OUT / "g0-hand-inspect.json").write_text(json.dumps(report, indent=2))
print("WROTE", OUT / "g0-hand-inspect.json")
print("meshes", report["meshCount"], "bones", report["boneCount"], "handMeshes", report["handMeshCount"])
print("fingerLike", [b["name"] for b in report["fingerLikeBones"]])
