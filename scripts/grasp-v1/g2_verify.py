"""G2: evaluated-triangle pulldown-bar contact, classed close-ups, seam checks.

Reads the isolated G1 export. Does not rewrite frozen R1 or production GLBs.
"""
from __future__ import annotations

import hashlib
import json
import math
import struct
from pathlib import Path

import bpy
from mathutils import Euler, Vector

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "artifacts" / "grasp-v1" / "g2"
OUT.mkdir(parents=True, exist_ok=True)
FRAMES = OUT / "frames"
FRAMES.mkdir(exist_ok=True)
GLB = ROOT / "artifacts" / "grasp-v1" / "grasp-controller.glb"
assert GLB.is_file(), GLB
GLB_SHA = hashlib.sha256(GLB.read_bytes()).hexdigest()
assert GLB_SHA == "40e3dbcbbe3423381dd2885936dd3f1c7d4355bcc6b4f0c30eb9245537be1dff"

DIGITS = ["Thumb", "Index", "Middle", "Ring", "Little"]
CHAIN = {
    "Thumb": ["CMC", "MCP", "IP"],
    "Index": ["MCP", "PIP", "DIP"],
    "Middle": ["MCP", "PIP", "DIP"],
    "Ring": ["MCP", "PIP", "DIP"],
    "Little": ["MCP", "PIP", "DIP"],
}
FLEX = {"CMC": 0.35, "MCP": 1.15, "PIP": 1.25, "DIP": 0.85, "IP": 1.05}
THUMB_CMC_OPP = 0.55
PRESETS = {
    "open": {"curl": 0.0, "thumb": 0.0, "spread": 0.25},
    "half": {"curl": 0.45, "thumb": 0.35, "spread": 0.12},
    "closed": {"curl": 1.0, "thumb": 0.85, "spread": 0.0},
    "pulldown-bar": {"curl": 0.72, "thumb": 0.62, "spread": 0.06},
}
# Historical lat-pulldown grip radius (M2). Fixture is at rest-pose hands, not overhead travel.
BAR_RADIUS = 0.024
NEAR_M = 0.008
STRETCH_GATE = 2.0
AREA_COLLAPSE = 0.05

CLASS_COLORS = {
    "thenar": (0.85, 0.35, 0.20),
    "hypothenar": (0.20, 0.45, 0.85),
    "digit-muscle-set": (0.20, 0.75, 0.35),
    "long-tendon-thumb": (0.90, 0.80, 0.15),
    "wrist-retinaculum": (0.55, 0.55, 0.55),
    "accidental-forearm": (0.95, 0.10, 0.85),
    "other-hand": (0.70, 0.70, 0.70),
}


def classify(name: str) -> str:
    n = name.lower()
    if any(k in n for k in ("foot", "halluc", " of left leg", " of right leg", "plantar")):
        return "excluded-lower"
    if "interosseous membrane" in n:
        return "accidental-forearm"
    if "retinaculum" in n and "wrist" in n:
        return "wrist-retinaculum"
    if any(k in n for k in ("pollicis longus", "extensor pollicis", "abductor pollicis longus")):
        return "long-tendon-thumb"
    if any(k in n for k in (
        "abductor pollicis brevis", "flexor pollicis brevis", "opponens pollicis", "adductor pollicis",
    )):
        return "thenar"
    if "digiti minimi" in n and "hand" in n:
        return "hypothenar"
    if any(k in n for k in ("lumbrical", "interossei")) and "hand" in n:
        return "digit-muscle-set"
    return "other-hand"


def spatial_side(obj) -> str:
    pts = [obj.matrix_world @ v.co for v in obj.data.vertices]
    return "Left" if sum(p.x for p in pts) / max(len(pts), 1) > 0 else "Right"


def bone_name(side, digit, joint):
    return f"{side}{digit}{joint}"


def apply_params(rig, p):
    bpy.context.view_layer.objects.active = rig
    bpy.ops.object.mode_set(mode="POSE")
    for pb in rig.pose.bones:
        if any(d in pb.name for d in DIGITS):
            pb.rotation_mode = "XYZ"
            pb.rotation_euler = (0, 0, 0)
    for side, sign in (("Left", 1.0), ("Right", -1.0)):
        for di, digit in enumerate(DIGITS):
            spread = (di - 2) * 0.12 * p["spread"]
            curl = p["thumb"] if digit == "Thumb" else p["curl"]
            for joint in CHAIN[digit]:
                pb = rig.pose.bones[bone_name(side, digit, joint)]
                pb.rotation_mode = "XYZ"
                flex = FLEX[joint] * curl
                opp = THUMB_CMC_OPP * p["thumb"] if digit == "Thumb" and joint == "CMC" else 0.0
                pb.rotation_euler = Euler((flex, opp * sign, spread * sign), "XYZ")
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.context.view_layer.update()


def apply_pose(rig, preset):
    apply_params(rig, PRESETS[preset])


def apply_cycle(rig, t):
    u = t * 2 if t <= 0.5 else (1 - t) * 2
    a, b = PRESETS["open"], PRESETS["closed"]
    apply_params(rig, {k: a[k] + (b[k] - a[k]) * u for k in a})


def evaluated(obj):
    deps = bpy.context.evaluated_depsgraph_get()
    ev = obj.evaluated_get(deps)
    me = ev.to_mesh()
    mw = ev.matrix_world.copy()
    return ev, me, mw


def world_geom(obj):
    ev, me, mw = evaluated(obj)
    verts = [mw @ v.co for v in me.vertices]
    me.calc_loop_triangles()
    tris = []
    for lt in me.loop_triangles:
        i, j, k = lt.vertices
        tris.append((verts[i], verts[j], verts[k]))
    edges = [(e.vertices[0], e.vertices[1]) for e in me.edges]
    ev.to_mesh_clear()
    return verts, tris, edges


def tint(obj, rgb, roughness=0.55):
    mat = bpy.data.materials.new(name=f"g2-{obj.name[:50]}")
    mat.diffuse_color = (rgb[0], rgb[1], rgb[2], 1.0)
    mat.use_nodes = True
    bsdf = next((n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED"), None)
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (rgb[0], rgb[1], rgb[2], 1.0)
        bsdf.inputs["Roughness"].default_value = roughness
    obj.data.materials.clear()
    obj.data.materials.append(mat)


def cyl_signed(p, origin, axis, radius, half):
    rel = p - origin
    t = rel.dot(axis)
    axial = abs(t) - half
    radial_vec = rel - axis * t
    radial = radial_vec.length - radius
    if axial <= 0 and radial <= 0:
        return max(radial, axial)
    if axial <= 0:
        return radial
    if radial <= 0:
        return axial
    return math.hypot(radial, axial)


def sample_points(tri):
    a, b, c = tri
    return (a, b, c, (a + b + c) / 3, (a + b) / 2, (b + c) / 2, (c + a) / 2)


def sector_frame(axis):
    ref = Vector((0, 0, 1))
    if abs(axis.dot(ref)) > 0.9:
        ref = Vector((0, 1, 0))
    n1 = (ref - axis * ref.dot(axis)).normalized()
    n2 = axis.cross(n1).normalized()
    return n1, n2


def measure_contact(meshes, origin, axis, radius, half):
    n1, n2 = sector_frame(axis)
    bins = [0] * 8
    rows = []
    for rec, obj in meshes:
        verts, tris, _ = world_geom(obj)
        min_s = 1e9
        inside = 0
        near = 0
        nearest = None
        for ti, tri in enumerate(tris):
            for p in sample_points(tri):
                s = cyl_signed(p, origin, axis, radius, half)
                if s < min_s:
                    min_s = s
                    nearest = {"triangle": ti, "point": [round(p.x, 5), round(p.y, 5), round(p.z, 5)], "signedM": s}
                if s <= 0:
                    inside += 1
                if s <= NEAR_M:
                    near += 1
                    rel = p - origin
                    rv = rel - axis * rel.dot(axis)
                    ang = math.atan2(rv.dot(n2), rv.dot(n1))
                    bins[int((ang + math.pi) / (2 * math.pi) * 8) % 8] += 1
        rows.append({
            "sourceName": rec["sourceName"],
            "class": rec["class"],
            "side": rec["side"],
            "triangles": len(tris),
            "vertices": len(verts),
            "minSignedM": None if min_s == 1e9 else min_s,
            "insideSamples": inside,
            "nearSamples": near,
            "nearest": nearest,
        })
    occupied = sum(1 for c in bins if c > 0)
    return {
        "meshes": rows,
        "wrapBins": bins,
        "wrapOccupied": occupied,
        "wrapScore": occupied / 8,
        "verdict": None,
    }


def seam_check(obj, rest_verts, rest_tris):
    posed_verts, posed_tris, edges = world_geom(obj)
    stretches = []
    for i, j in edges:
        if i >= len(rest_verts) or j >= len(rest_verts):
            continue
        a = (rest_verts[i] - rest_verts[j]).length
        b = (posed_verts[i] - posed_verts[j]).length
        if a > 1e-6:
            stretches.append(b / a)
    flips = 0
    collapses = 0
    area_ratios = []
    for rt, pt in zip(rest_tris, posed_tris):
        rn = (rt[1] - rt[0]).cross(rt[2] - rt[0])
        pn = (pt[1] - pt[0]).cross(pt[2] - pt[0])
        ra, pa = rn.length, pn.length
        if ra > 1e-10:
            ratio = pa / ra
            area_ratios.append(ratio)
            if ratio < AREA_COLLAPSE:
                collapses += 1
            if rn.dot(pn) < 0:
                flips += 1
    stretches.sort()
    n = len(stretches)
    return {
        "edgeCount": n,
        "stretchP50": stretches[n // 2] if n else None,
        "stretchP99": stretches[int(n * 0.99)] if n else None,
        "stretchMax": stretches[-1] if n else None,
        "stretchOver2": sum(1 for s in stretches if s > STRETCH_GATE),
        "flippedTris": flips,
        "collapsedTris": collapses,
        "areaRatioP50": sorted(area_ratios)[len(area_ratios) // 2] if area_ratios else None,
        "triCount": len(posed_tris),
    }


def look_at(cam, target, location):
    cam.location = location
    direction = target - cam.location
    cam.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def render_shot(scene, path):
    scene.render.filepath = str(path)
    bpy.ops.render.render(write_still=True)
    return {"file": path.name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "bytes": path.stat().st_size}


bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(GLB))
rig = next(o for o in bpy.data.objects if o.type == "ARMATURE")
meshes = [o for o in bpy.data.objects if o.type == "MESH"]

hand_recs = []
for o in meshes:
    name = o.get("sourceName") or o.name
    cls = classify(name)
    if cls == "other-hand" and not any(k in name.lower() for k in (
        "hand", "pollicis", "lumbrical", "interosse", "digiti minimi", "retinaculum",
    )):
        continue
    rec = {"sourceName": name, "class": cls, "side": spatial_side(o), "object": o.name}
    if cls == "excluded-lower":
        continue
    hand_recs.append((rec, o))

assert 30 <= len(hand_recs) <= 42, len(hand_recs)
for rec, o in hand_recs:
    tint(o, CLASS_COLORS[rec["class"]])

# Hide non-hand for close-ups; keep a copy of visibility.
hand_set = {o for _, o in hand_recs}
for o in meshes:
    o.hide_render = o not in hand_set
    o.hide_viewport = o not in hand_set

apply_pose(rig, "open")
rest = {}
for rec, o in hand_recs:
    v, t, e = world_geom(o)
    rest[o.name] = {"verts": v, "tris": t, "edges": e}

# Palm centroids from thenar + hypothenar + palmar interossei at open.
def class_centroid(side, classes):
    pts = []
    for rec, o in hand_recs:
        if rec["side"] != side or rec["class"] not in classes:
            continue
        pts.extend(rest[o.name]["verts"])
    if not pts:
        return None
    return sum(pts, Vector()) / len(pts)

left_palm = class_centroid("Left", {"thenar", "hypothenar", "digit-muscle-set"})
right_palm = class_centroid("Right", {"thenar", "hypothenar", "digit-muscle-set"})
assert left_palm and right_palm, (left_palm, right_palm)
# One horizontal pulldown-diameter bar at rest-pose hand height (not overhead travel).
axis = Vector((1.0, 0.0, 0.0))
origin = Vector((0.0, (left_palm.y + right_palm.y) * 0.5, (left_palm.z + right_palm.z) * 0.5))
half = 0.34

bar_fix = {
    "radiusM": BAR_RADIUS,
    "origin": [origin.x, origin.y, origin.z],
    "axis": [axis.x, axis.y, axis.z],
    "halfLengthM": half,
    "space": "blender_Z_up",
    "gltfYup": {
        "origin": [origin.x, origin.z, -origin.y],
        "axis": [axis.x, axis.z, -axis.y],
        "note": "Blender (x,y,z) -> glTF (x,z,-y) because G1 export used export_yup=True.",
    },
    "note": "Rest-pose hand-height fixture using historical pulldown grip radius 24mm. Not overhead pulldown travel. Sole contact solid for G2.",
}
(OUT / "bar-fixture.json").write_text(json.dumps(bar_fix, indent=2) + "\n")

# Visible bar
depth = half * 2
bpy.ops.mesh.primitive_cylinder_add(radius=BAR_RADIUS, depth=depth, location=origin)
bar = bpy.context.active_object
bar.name = "PulldownBarG2"
# Align cylinder +Z to axis
bar.rotation_euler = Vector((0, 0, 1)).rotation_difference(axis).to_euler()
tint(bar, (0.22, 0.24, 0.28), roughness=0.85)
bar.hide_render = False
bar.hide_viewport = False

# Contact + seams per preset
contact_presets = {}
seams = {}
displacements = {}
for preset in PRESETS:
    apply_pose(rig, preset)
    contact_presets[preset] = measure_contact(hand_recs, origin, axis, BAR_RADIUS, half)
    seam_rows = []
    disp_rows = []
    for rec, o in hand_recs:
        seam_rows.append({**{k: rec[k] for k in ("sourceName", "class", "side")}, **seam_check(o, rest[o.name]["verts"], rest[o.name]["tris"])})
        pv, _, _ = world_geom(o)
        rv = rest[o.name]["verts"]
        deltas = [(pv[i] - rv[i]).length for i in range(min(len(pv), len(rv)))]
        deltas.sort()
        n = len(deltas)
        disp_rows.append({
            "sourceName": rec["sourceName"],
            "class": rec["class"],
            "side": rec["side"],
            "maxDeltaM": deltas[-1] if n else None,
            "p50": deltas[n // 2] if n else None,
            "p90": deltas[int(n * 0.9)] if n else None,
        })
    seams[preset] = seam_rows
    displacements[preset] = disp_rows

CONTACT_CLASSES = {"thenar", "hypothenar", "digit-muscle-set", "long-tendon-thumb", "wrist-retinaculum"}
open_pack = contact_presets["open"]
open_min = min((r["minSignedM"] for r in open_pack["meshes"] if r["class"] in CONTACT_CLASSES and r["minSignedM"] is not None), default=None)
for preset, pack in contact_presets.items():
    hand_rows = [r for r in pack["meshes"] if r["class"] in CONTACT_CLASSES]
    mins = [r["minSignedM"] for r in hand_rows if r["minSignedM"] is not None]
    pmin = min(mins) if mins else None
    inside = sum(r["insideSamples"] for r in hand_rows)
    # Embedded at open + similar when closed is impalement, not a formed grip.
    if open_min is not None and open_min <= -0.01 and pmin is not None and pmin <= -0.01:
        pack["verdict"] = "PERSISTENT_INTERSECTION"
    elif pmin is not None and pmin > 0.004 and pack["wrapOccupied"] < 4:
        pack["verdict"] = "GAP_NO_WRAP"
    elif pack["wrapOccupied"] >= 4 and pmin is not None and -0.004 <= pmin <= 0.004:
        pack["verdict"] = "SURFACE_WRAP_CANDIDATE"
    else:
        pack["verdict"] = "INCONCLUSIVE_CONTACT"
    pack["handOnlyMinSignedM"] = pmin
    pack["handOnlyInsideSamples"] = inside
    pack["handOnlyMeshes"] = hand_rows

# Render setup
scene = bpy.context.scene
scene.render.engine = "BLENDER_EEVEE"
scene.render.resolution_x = 720
scene.render.resolution_y = 540
scene.render.film_transparent = False
scene.render.image_settings.file_format = "PNG"
world = bpy.data.worlds.new("G2World")
scene.world = world
world.use_nodes = True
bg = next((n for n in world.node_tree.nodes if n.type == "BACKGROUND"), None)
if bg:
    bg.inputs[0].default_value = (0.10, 0.12, 0.14, 1.0)
    bg.inputs[1].default_value = 0.55
cam_data = bpy.data.cameras.new("G2Cam")
cam = bpy.data.objects.new("G2Cam", cam_data)
bpy.context.collection.objects.link(cam)
scene.camera = cam
cam.data.clip_start = 0.01
cam.data.clip_end = 8.0
key = bpy.data.objects.new("G2Key", bpy.data.lights.new("G2Key", "AREA"))
key.data.energy = 400
key.data.size = 0.6
key.location = (0.2, -0.9, 1.2)
bpy.context.collection.objects.link(key)
fill = bpy.data.objects.new("G2Fill", bpy.data.lights.new("G2Fill", "AREA"))
fill.data.energy = 160
fill.data.size = 0.8
fill.location = (0.3, 0.4, 1.0)
bpy.context.collection.objects.link(fill)
rim = bpy.data.objects.new("G2Rim", bpy.data.lights.new("G2Rim", "AREA"))
rim.data.energy = 120
rim.location = (-0.4, -0.3, 0.5)
bpy.context.collection.objects.link(rim)


def bone_world(name):
    pb = rig.pose.bones[name]
    return rig.matrix_world @ pb.matrix.to_translation()

shots = []


def framed(kind, side="Left"):
    hand = bone_world(f"{side}Hand")
    if kind == "palm":
        return hand, hand + Vector((0.05 if side == "Left" else -0.05, -0.20, 0.07)), 50
    if kind == "digits":
        tip = hand + Vector((0.0, 0.0, -0.05))
        return tip, tip + Vector((0.04 if side == "Left" else -0.04, -0.14, -0.10)), 50
    if kind == "context":
        return Vector((0.0, -0.12, 0.85)), Vector((0.0, -1.55, 1.05)), 35
    return origin, Vector((0.0, -0.95, 0.95)), 35


for preset in PRESETS:
    apply_pose(rig, preset)
    look_at(cam, *framed("context")[:2])
    cam.data.lens = 35
    path = OUT / f"shot-context-{preset}.png"
    shots.append({**render_shot(scene, path), "preset": preset, "side": "both", "kind": "context"})
    for side_name, side in (("left", "Left"), ("right", "Right")):
        for kind in ("palm", "digits"):
            target, loc, lens = framed(kind, side)
            look_at(cam, target, loc)
            cam.data.lens = lens
            path = OUT / f"shot-{side_name}-{kind}-{preset}.png"
            shots.append({**render_shot(scene, path), "preset": preset, "side": side_name, "kind": kind, "target": list(target), "camera": list(loc)})
    target, loc, lens = framed("bar")
    look_at(cam, target, loc)
    cam.data.lens = lens
    path = OUT / f"shot-bar-{preset}.png"
    shots.append({**render_shot(scene, path), "preset": preset, "side": "both", "kind": "bar"})

# Class isolation at pulldown-bar, left palm.
apply_pose(rig, "pulldown-bar")
for cls in ("thenar", "hypothenar", "digit-muscle-set", "long-tendon-thumb"):
    for rec, o in hand_recs:
        o.hide_render = rec["class"] != cls or rec["side"] != "Left"
    bar.hide_render = False
    target, loc, lens = framed("palm", "Left")
    look_at(cam, target, loc)
    cam.data.lens = lens
    path = OUT / f"shot-class-{cls}.png"
    shots.append({**render_shot(scene, path), "preset": "pulldown-bar", "side": "left", "kind": f"class-{cls}"})
for rec, o in hand_recs:
    o.hide_render = False
bar.hide_render = False

# open → closed → open, left palm
for i in range(36):
    t = i / 35
    apply_cycle(rig, t)
    target, loc, lens = framed("palm", "Left")
    look_at(cam, target, loc)
    cam.data.lens = lens
    scene.render.filepath = str(FRAMES / f"frame-{i:03d}.png")
    bpy.ops.render.render(write_still=True)

# Identity: rest POSITION of imported export (bind) hashed for the 467 source meshes still present.
source_meshes = [o for o in meshes if o.get("sourceName")]
pos_sha = hashlib.sha256(
    b"".join(
        struct.pack("<3f", *v.co)
        for o in sorted(source_meshes, key=lambda x: x.get("sourceName") or "")
        for v in o.data.vertices
    )
).hexdigest()

summary = {
    "phase": "G2-posed-contact",
    "engine": "Blender 5.2 evaluated depsgraph triangles",
    "glbSha256": GLB_SHA,
    "bindPositionConcatSha256": pos_sha,
    "handMeshCount": len(hand_recs),
    "classes": {cls: [r["sourceName"] for r, _ in hand_recs if r["class"] == cls] for cls in CLASS_COLORS},
    "bar": bar_fix,
    "contact": contact_presets,
    "seams": seams,
    "displacementsVsOpen": displacements,
    "shots": shots,
    "limits": [
        "No finger skin shell. digit-muscle-set is lumbrical/interosseous collections, not phalanx pads.",
        "Bar is a rest-pose hand-height cylinder with pulldown grip radius; not pulldown travel.",
        "interosseous membrane of forearm is accidental G1 weight target; excluded from wrap verdict classes.",
        "Pulldown/curl historical FAIL unchanged. Grasp is not whole-body PASS.",
    ],
}
(OUT / "posed-contact.json").write_text(json.dumps(summary, indent=2) + "\n")
print("G2_WRITTEN", OUT / "posed-contact.json")
print("HANDS", len(hand_recs), "SHOTS", len(shots))
for preset, pack in contact_presets.items():
    print(preset, "handMin", pack.get("handOnlyMinSignedM"), "inside", pack.get("handOnlyInsideSamples"), "wrap", pack["wrapOccupied"], pack["verdict"])
