import bpy, json, hashlib
from pathlib import Path
from mathutils import Euler
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "artifacts" / "grasp-v1"
glb = OUT / "grasp-controller.glb"
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(glb))
rig = next(o for o in bpy.data.objects if o.type == "ARMATURE")
print("bones", len(rig.data.bones), "finger", sum(1 for b in rig.data.bones if any(x in b.name for x in ("Thumb","Index","Middle","Ring","Little"))))
# find lumbricals
lum = next(o for o in bpy.data.objects if o.type=="MESH" and "lumbricals of left" in o.name)
print("lum verts", len(lum.data.vertices), "groups", [g.name for g in lum.vertex_groups if any(x in g.name for x in ("Thumb","Index","Hand","Finger"))])

def eval_pts():
    deps = bpy.context.evaluated_depsgraph_get()
    ev = lum.evaluated_get(deps)
    me = ev.to_mesh()
    pts = [ev.matrix_world @ v.co for v in me.vertices]
    ev.to_mesh_clear()
    return pts

bpy.context.view_layer.objects.active = rig
bpy.ops.object.mode_set(mode="POSE")
for pb in rig.pose.bones:
    if any(x in pb.name for x in ("Thumb","Index","Middle","Ring","Little")):
        pb.rotation_mode="XYZ"; pb.rotation_euler=(0,0,0)
bpy.ops.object.mode_set(mode="OBJECT")
bpy.context.view_layer.update()
open_pts = eval_pts()
bpy.ops.object.mode_set(mode="POSE")
for pb in rig.pose.bones:
    if "LeftIndex" in pb.name or "LeftMiddle" in pb.name or "LeftThumb" in pb.name:
        pb.rotation_mode="XYZ"; pb.rotation_euler=Euler((1.1,0,0),"XYZ")
bpy.ops.object.mode_set(mode="OBJECT")
bpy.context.view_layer.update()
closed_pts = eval_pts()
deltas=[(closed_pts[i]-open_pts[i]).length for i in range(len(open_pts))]
deltas.sort()
print("maxDelta", max(deltas) if deltas else None, "p50", deltas[len(deltas)//2] if deltas else None, "p90", deltas[int(len(deltas)*0.9)] if deltas else None)
# weight mass on new bones
mass={}
for g in lum.vertex_groups:
    s=0
    for i in range(len(lum.data.vertices)):
        try: s+=g.weight(i)
        except RuntimeError: pass
    if s>1e-6 and any(x in g.name for x in ("Thumb","Index","Middle","Ring","Little","Hand","Wrist")):
        mass[g.name]=round(s,3)
print("weightMass", mass)
(OUT/"verify-deform.json").write_text(json.dumps({
    "fingerBones": sum(1 for b in rig.data.bones if any(x in b.name for x in ("Thumb","Index","Middle","Ring","Little"))),
    "maxDeltaM": max(deltas) if deltas else None,
    "p50": deltas[len(deltas)//2] if deltas else None,
    "p90": deltas[int(len(deltas)*0.9)] if deltas else None,
    "weightMass": mass,
}, indent=2))
