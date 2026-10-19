import bpy, json
arms = [o for o in bpy.data.objects if o.type == "ARMATURE"]
report = {"armatures": []}
for arm in arms:
    bones = [{"name": b.name, "parent": b.parent.name if b.parent else None} for b in arm.data.bones]
    report["armatures"].append({"object": arm.name, "boneCount": len(bones), "bonesSample": bones[:40]})
# meshes with sourceName custom props if present
meshes = []
for o in bpy.data.objects:
    if o.type != "MESH":
        continue
    sn = o.get("sourceName") or o.get("source_name") or None
    meshes.append({"name": o.name, "sourceName": sn, "verts": len(o.data.vertices), "polys": len(o.data.polygons)})
report["meshCount"] = len(meshes)
report["meshesWithSourceName"] = [m for m in meshes if m["sourceName"]][:30]
report["meshNamesSample"] = [m["name"] for m in meshes[:40]]
# search subscapularis / BP4795
hits = [m for m in meshes if m["name"] and ("subscap" in m["name"].lower() or "4795" in m["name"] or (m["sourceName"] and ("subscap" in str(m["sourceName"]).lower() or "4795" in str(m["sourceName"]))))]
report["subscapHits"] = hits
print(json.dumps(report, indent=2)[:8000])
