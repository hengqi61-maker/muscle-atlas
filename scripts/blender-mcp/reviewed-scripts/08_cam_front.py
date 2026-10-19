import bpy, math, json, mathutils
view = "front"
cam = bpy.data.objects.get("MCP_VIEW_CAM")
if cam is None:
    data = bpy.data.cameras.new("MCP_VIEW_CAM")
    cam = bpy.data.objects.new("MCP_VIEW_CAM", data)
    bpy.context.scene.collection.objects.link(cam)
bpy.context.scene.camera = cam
objs = [o for o in bpy.data.objects if o.type in ("MESH", "ARMATURE")]
if not objs:
    raise RuntimeError("no objects")
mins = mathutils.Vector((1e9, 1e9, 1e9)); maxs = mathutils.Vector((-1e9, -1e9, -1e9))
for o in objs:
    for corner in o.bound_box:
        w = o.matrix_world @ mathutils.Vector(corner)
        mins = mathutils.Vector((min(mins.x, w.x), min(mins.y, w.y), min(mins.z, w.z)))
        maxs = mathutils.Vector((max(maxs.x, w.x), max(maxs.y, w.y), max(maxs.z, w.z)))
center = (mins + maxs) / 2
size = (maxs - mins).length or 2.0
dist = size * 1.35
positions = {
  "front": (center.x, center.y - dist, center.z + size * 0.05),
  "side": (center.x + dist, center.y, center.z + size * 0.05),
  "back": (center.x, center.y + dist, center.z + size * 0.05),
  "detail": (center.x + size * 0.15, center.y - size * 0.35, center.z + size * 0.25),
}
cam.location = positions[view]
direction = center - cam.location
cam.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
cam.data.lens = 85 if view == "detail" else 50
# Prefer looking through camera for offscreen capture if addon uses scene.camera
print(json.dumps({"view": view, "cam": list(cam.location), "center": [round(c, 4) for c in center], "size": round(size, 4)}))
