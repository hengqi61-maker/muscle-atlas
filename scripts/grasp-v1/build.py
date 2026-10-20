"""Isolated Grasp Controller v1: additive finger bones + parameterized poses.

Does not overwrite frozen R1 / production GLBs. Works on an experimental copy.
"""
from __future__ import annotations
import bpy, json, hashlib, math, struct
from pathlib import Path
from mathutils import Vector, Euler, Matrix

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "artifacts" / "grasp-v1"
OUT.mkdir(parents=True, exist_ok=True)
SRC = ROOT / "public" / "experimental" / "rig-v2" / "unified-rig-prototype.glb"
assert SRC.is_file()
SRC_SHA = hashlib.sha256(SRC.read_bytes()).hexdigest()
assert SRC_SHA == "ef803a4bbb3c644504c124519e39ba0b3b760ec139eaf60d277ef7f7f5d23274"

DIGITS = ["Thumb", "Index", "Middle", "Ring", "Little"]
FOUR = ["Index", "Middle", "Ring", "Little"]
CHAIN = {
    "Thumb": ["CMC", "MCP", "IP"],
    "Index": ["MCP", "PIP", "DIP"],
    "Middle": ["MCP", "PIP", "DIP"],
    "Ring": ["MCP", "PIP", "DIP"],
    "Little": ["MCP", "PIP", "DIP"],
}

# Heuristic flexion (radians). Not clinical ROM.
FLEX = {"CMC": 0.35, "MCP": 1.15, "PIP": 1.25, "DIP": 0.85, "IP": 1.05}
THUMB_CMC_OPP = 0.55

PRESETS = {
    "open": {"curl": 0.0, "thumb": 0.0, "spread": 0.25},
    "half": {"curl": 0.45, "thumb": 0.35, "spread": 0.12},
    "closed": {"curl": 1.0, "thumb": 0.85, "spread": 0.0},
    "pulldown-bar": {"curl": 0.72, "thumb": 0.62, "spread": 0.06},
    "rope-end": {"curl": 0.88, "thumb": 0.78, "spread": 0.02},
}


def sha_positions(obj):
    return hashlib.sha256(b"".join(struct.pack("<3f", *v.co) for v in obj.data.vertices)).hexdigest()


def bone_name(side, digit, joint):
    return f"{side}{digit}{joint}"


bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(SRC))

rig = next(o for o in bpy.data.objects if o.type == "ARMATURE")
meshes = [o for o in bpy.data.objects if o.type == "MESH"]
source_meshes = [o for o in meshes if o.get("sourceName")]
assert len(source_meshes) == 467, len(source_meshes)
before = {o.get("sourceName"): sha_positions(o) for o in source_meshes}

# --- additive bones ---
bpy.context.view_layer.objects.active = rig
bpy.ops.object.mode_set(mode="EDIT")
eb = rig.data.edit_bones
created = []
for side, sign in (("Left", 1.0), ("Right", -1.0)):
    hand = eb[f"{side}Hand"]
    socket = eb[f"{side}FingerSocket"]
    socket.use_deform = False
    origin = Vector(socket.head)
    # Distal along current socket (mostly -Z). Across-palm toward thumb = +X on left.
    distal = (Vector(socket.tail) - Vector(socket.head)).normalized()
    if distal.length < 1e-6:
        distal = Vector((0, 0, -1))
    across = Vector((sign, 0, 0))
    palmar = across.cross(distal).normalized()
    if palmar.y > 0:
        palmar = -palmar
    # Fit to observed muscle cloud (see G0 bounds).
    thumb_u = 0.055
    little_u = -0.018
    length = 0.062
    seg = length / 3
    for di, digit in enumerate(DIGITS):
        t = di / 4.0
        u = little_u * (1 - t) + thumb_u * t
        if digit == "Thumb":
            start = origin + across * (thumb_u * 0.85) + palmar * 0.008 + distal * 0.004
            ddir = (distal * 0.55 + across * 0.75 + palmar * 0.15).normalized()
        else:
            start = origin + across * u + distal * 0.006
            ddir = (distal * 0.92 + palmar * 0.08).normalized()
        parent = socket
        cursor = start
        for joint in CHAIN[digit]:
            name = bone_name(side, digit, joint)
            b = eb.new(name)
            b.head = cursor
            b.tail = cursor + ddir * seg
            b.parent = parent
            b.use_connect = parent != socket
            b.use_deform = True
            b.align_roll(palmar)
            created.append(name)
            parent = b
            cursor = Vector(b.tail)
bpy.ops.object.mode_set(mode="OBJECT")

# --- weights: only vertices already dominated by Hand/Wrist/FingerSocket ---
HANDISH = set()
for side in ("Left", "Right"):
    HANDISH.update({f"{side}Hand", f"{side}Wrist", f"{side}FingerSocket"})

hand_name_keys = (
    "hand", "pollicis", "lumbrical", "interosse", "digiti minimi of left hand",
    "digiti minimi of right hand", "opponens", "retinaculum of left wrist",
    "retinaculum of right wrist",
)


def is_hand_mesh(o):
    n = (o.get("sourceName") or o.name).lower()
    if "foot" in n or "halluc" in n or "leg" in n:
        return False
    return any(k in n for k in hand_name_keys)


def groups_map(o):
    return {g.name: g for g in o.vertex_groups}


touched = []
for o in source_meshes:
    if not is_hand_mesh(o):
        continue
    gmap = groups_map(o)
    if not any(n in gmap for n in HANDISH):
        continue
    # spatial side from centroid, not the known-swapped name
    cents = [o.matrix_world @ v.co for v in o.data.vertices]
    cx = sum(p.x for p in cents) / len(cents)
    side = "Left" if cx > 0 else "Right"
    sign = 1.0 if side == "Left" else -1.0
    socket = rig.data.bones[f"{side}FingerSocket"]
    origin = rig.matrix_world @ socket.head_local
    for gname in [bone_name(side, d, j) for d in DIGITS for j in CHAIN[d]]:
        if gname not in gmap:
            gmap[gname] = o.vertex_groups.new(name=gname)
    assigned = 0
    for v in o.data.vertices:
        wp = o.matrix_world @ v.co
        # existing handish weight
        hw = 0.0
        for n in HANDISH:
            if n in gmap:
                try:
                    hw += gmap[n].weight(v.index)
                except RuntimeError:
                    pass
        if hw < 0.12:
            continue
        u = (wp.x - origin.x) * sign  # + toward thumb
        vlen = origin.z - wp.z  # + distal (lower Z)
        # digit
        u_n = max(0.0, min(1.0, (u + 0.02) / 0.08))
        di = int(round(u_n * 4))
        di = max(0, min(4, di))
        # thumb override if clearly radial
        if u > 0.035:
            di = 4
        digit = DIGITS[di] if di < 4 else "Thumb"
        if u < 0.028 and di == 4:
            digit = "Index"
        sl = max(0.0, min(0.999, vlen / 0.07))
        si = min(2, int(sl * 3))
        joint = CHAIN[digit][si]
        target = bone_name(side, digit, joint)
        # keep a palm remainder on Hand
        palm_keep = max(0.15, 0.55 * (1.0 - sl))
        transfer = hw * (1.0 - palm_keep)
        if transfer <= 1e-6:
            continue
        gmap[target].add([v.index], transfer, "ADD")
        # reduce original Hand/Socket so rows stay ~normalized
        for n in ("LeftHand", "RightHand", f"{side}FingerSocket"):
            if n in gmap:
                try:
                    cur = gmap[n].weight(v.index)
                except RuntimeError:
                    continue
                if cur > 0:
                    gmap[n].add([v.index], max(0.0, cur * palm_keep / max(hw, 1e-6)), "REPLACE")
        assigned += 1
    touched.append({"name": o.get("sourceName"), "assigned": assigned, "side": side})

# normalize any row we touched
for rec in touched:
    o = next(m for m in source_meshes if m.get("sourceName") == rec["name"])
    gmap = groups_map(o)
    for v in o.data.vertices:
        weights = []
        for n, g in gmap.items():
            try:
                w = g.weight(v.index)
            except RuntimeError:
                continue
            if w > 1e-8:
                weights.append((n, w))
        tot = sum(w for _, w in weights)
        if tot <= 1e-8:
            continue
        for n, w in weights:
            gmap[n].add([v.index], w / tot, "REPLACE")

after = {o.get("sourceName"): sha_positions(o) for o in source_meshes}
assert after == before, "source POSITION changed"

# --- controller apply ---
def apply_pose(preset, left=True, right=True):
    p = PRESETS[preset]
    bpy.context.view_layer.objects.active = rig
    bpy.ops.object.mode_set(mode="POSE")
    for pb in rig.pose.bones:
        if any(d in pb.name for d in DIGITS):
            pb.rotation_mode = "XYZ"
            pb.rotation_euler = (0, 0, 0)
    for side, enable in (("Left", left), ("Right", right)):
        if not enable:
            continue
        sign = 1.0 if side == "Left" else -1.0
        for di, digit in enumerate(DIGITS):
            spread = (di - 2) * 0.12 * p["spread"]
            curl = p["thumb"] if digit == "Thumb" else p["curl"]
            for joint in CHAIN[digit]:
                name = bone_name(side, digit, joint)
                pb = rig.pose.bones[name]
                pb.rotation_mode = "XYZ"
                flex = FLEX[joint] * curl
                opp = THUMB_CMC_OPP * p["thumb"] if (digit == "Thumb" and joint == "CMC") else 0.0
                # local X flexion toward palm, Z spread
                pb.rotation_euler = Euler((flex, opp * sign, spread * sign), "XYZ")
    bpy.context.view_layer.update()
    bpy.ops.object.mode_set(mode="OBJECT")


def mesh_centroid(names):
    pts = []
    for o in source_meshes:
        if o.get("sourceName") in names or any(k in (o.get("sourceName") or "") for k in names):
            pts.extend(o.matrix_world @ v.co for v in o.data.vertices)
    if not pts:
        return Vector((0, 0, 0))
    return sum(pts, Vector()) / len(pts)


# fixtures
def add_cylinder(name, loc, radius, depth, rot=(0, math.pi / 2, 0)):
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, location=loc, rotation=rot)
    obj = bpy.context.active_object
    obj.name = name
    return obj


def add_sphere(name, loc, radius):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=loc)
    obj = bpy.context.active_object
    obj.name = name
    return obj


apply_pose("open")
# place props at rest palm
left_c = mesh_centroid(["set of lumbricals of left hand", "set of palmar interossei of left hand"])
right_c = mesh_centroid(["set of lumbricals of right hand", "set of palmar interossei of right hand"])
mid = (left_c + right_c) * 0.5
bar = add_cylinder("GraspBar", (mid.x, mid.y - 0.012, mid.z - 0.01), 0.014, 0.18)
rope_l = add_sphere("GraspRopeLeft", (left_c.x, left_c.y - 0.01, left_c.z - 0.008), 0.016)
rope_r = add_sphere("GraspRopeRight", (right_c.x, right_c.y - 0.01, right_c.z - 0.008), 0.016)
props = [bar, rope_l, rope_r]


def closest_points(mesh_obj, prop):
    # evaluated verts vs prop bound
    mw = mesh_obj.matrix_world
    pmw = prop.matrix_world
    pinv = pmw.inverted()
    best = 1e9
    inside = 0
    n = 0
    for v in mesh_obj.data.vertices:
        w = mw @ v.co
        local = pinv @ w
        if prop.name.startswith("GraspBar"):
            # cylinder along local Z after rot X=0, we rotated Y=90 so axis ~ X world
            # After rotation (0, pi/2, 0), blender cylinder axis is X.
            r = math.hypot(local.y, local.z)
            axial = abs(local.x)
            rad = 0.014
            half = 0.09
            dist = max(r - rad, axial - half, 0.0)
            if r <= rad and axial <= half:
                inside += 1
                dist = min(rad - r, half - axial)
                best = min(best, -dist)
            else:
                best = min(best, dist)
        else:
            r = local.length
            rad = 0.016
            if r <= rad:
                inside += 1
                best = min(best, r - rad)
            else:
                best = min(best, r - rad)
        n += 1
    return {"minSigned": best if n else None, "insideHits": inside, "tested": n}


# evaluate presets
reports = []
for preset in PRESETS:
    apply_pose(preset)
    bpy.context.view_layer.update()
    # measure left/right lumbricals vs bar and ropes
    row = {"preset": preset, "contacts": []}
    for mesh_name, prop in (
        ("set of lumbricals of left hand", bar),
        ("set of lumbricals of right hand", bar),
        ("set of lumbricals of left hand", rope_l),
        ("set of lumbricals of right hand", rope_r),
    ):
        o = next(m for m in source_meshes if m.get("sourceName") == mesh_name)
        c = closest_points(o, prop)
        c.update({"mesh": mesh_name, "prop": prop.name})
        row["contacts"].append(c)
    # bone euler dump
    bpy.ops.object.mode_set(mode="POSE")
    row["bones"] = {
        pb.name: [round(a, 5) for a in pb.rotation_euler]
        for pb in rig.pose.bones if any(d in pb.name for d in DIGITS)
    }
    bpy.ops.object.mode_set(mode="OBJECT")
    reports.append(row)

# export rest-open GLB (props excluded)
apply_pose("open")
for p in props:
    p.hide_render = True
    p.hide_viewport = True
export_path = OUT / "grasp-controller.glb"
bpy.ops.export_scene.gltf(
    filepath=str(export_path),
    export_format="GLB",
    use_selection=False,
    export_extras=True,
    export_yup=True,
    export_animations=False,
    export_skins=True,
    export_morph=False,
)
for p in props:
    p.hide_render = False
    p.hide_viewport = False

# render closeups
scene = bpy.context.scene
scene.render.engine = "BLENDER_EEVEE"
scene.render.resolution_x = 640
scene.render.resolution_y = 480
scene.render.film_transparent = False
cam_data = bpy.data.cameras.new("GraspCam")
cam = bpy.data.objects.new("GraspCam", cam_data)
bpy.context.collection.objects.link(cam)
scene.camera = cam
light = bpy.data.objects.new("GraspKey", bpy.data.lights.new("GraspKey", "AREA"))
light.data.energy = 400
light.location = (0.4, -0.6, 1.2)
bpy.context.collection.objects.link(light)

shots = []
for preset, target, label in (
    ("open", left_c, "left-open"),
    ("half", left_c, "left-half"),
    ("closed", left_c, "left-closed"),
    ("pulldown-bar", mid, "bar-both"),
    ("rope-end", left_c, "rope-left"),
    ("open", right_c, "right-open"),
    ("closed", right_c, "right-closed"),
):
    apply_pose(preset)
    cam.location = (target.x + 0.12, target.y - 0.18, target.z + 0.06)
    direction = target - cam.location
    cam.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
    cam.data.lens = 50
    path = OUT / f"shot-{label}.png"
    scene.render.filepath = str(path)
    bpy.ops.render.render(write_still=True)
    shots.append({"file": path.name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "preset": preset})

# interpolation video frames
vid_dir = OUT / "frames"
vid_dir.mkdir(exist_ok=True)
for i in range(24):
    t = i / 23
    # lerp open -> closed on both hands
    curl = t
    thumb = 0.85 * t
    apply_pose("open")
    bpy.ops.object.mode_set(mode="POSE")
    for side, sign in (("Left", 1.0), ("Right", -1.0)):
        for di, digit in enumerate(DIGITS):
            spread = (di - 2) * 0.12 * (0.25 * (1 - t))
            c = thumb if digit == "Thumb" else curl
            for joint in CHAIN[digit]:
                pb = rig.pose.bones[bone_name(side, digit, joint)]
                pb.rotation_mode = "XYZ"
                flex = FLEX[joint] * c
                opp = THUMB_CMC_OPP * thumb if (digit == "Thumb" and joint == "CMC") else 0.0
                pb.rotation_euler = Euler((flex, opp * sign, spread * sign), "XYZ")
    bpy.ops.object.mode_set(mode="OBJECT")
    cam.location = (mid.x + 0.16, mid.y - 0.22, mid.z + 0.08)
    direction = mid - cam.location
    cam.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
    fp = vid_dir / f"frame-{i:03d}.png"
    scene.render.filepath = str(fp)
    bpy.ops.render.render(write_still=True)

# identity + summary
identity = {
    "frozenSourceCount": 467,
    "positionShaUnchanged": after == before,
    "sourceSha256": SRC_SHA,
    "exportSha256": hashlib.sha256(export_path.read_bytes()).hexdigest() if export_path.exists() else None,
    "addedBones": created,
    "touchedMeshes": touched,
}
summary = {
    "controller": "grasp-v1",
    "presets": PRESETS,
    "limits": "Heuristic geometric proxy. Muscle-only hands; no finger skin shell. Not clinical ROM. Pulldown/curl motion FAIL unchanged.",
    "identity": identity,
    "presetReports": reports,
    "shots": shots,
    "glb": str(export_path.relative_to(ROOT)),
}
(OUT / "build-report.json").write_text(json.dumps(summary, indent=2))
print("EXPORT", export_path, identity["exportSha256"])
print("POSITION_UNCHANGED", identity["positionShaUnchanged"], "bones", len(created), "touched", len(touched))
