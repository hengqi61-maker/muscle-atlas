import bpy, json
report = {"targets": [], "face914": None, "weightSamples": [], "limitations": []}
# find right subscapularis / BP4795
cands = []
for o in bpy.data.objects:
    if o.type != "MESH":
        continue
    blob = " ".join([o.name, str(o.get("sourceName") or ""), str(o.get("source_name") or ""), str(o.get("id") or "")])
    low = blob.lower()
    if "4795" in low or "subscapularis" in low and "right" in low:
        cands.append(o)
    elif "subscapularis" in low:
        cands.append(o)
report["candidateNames"] = [o.name for o in cands]
for o in cands:
    entry = {
        "name": o.name,
        "sourceName": o.get("sourceName") or o.get("source_name"),
        "verts": len(o.data.vertices),
        "polys": len(o.data.polygons),
        "parent": o.parent.name if o.parent else None,
        "armature": None,
        "vertexGroups": [g.name for g in o.vertex_groups][:40],
    }
    # armature modifier
    for m in o.modifiers:
        if m.type == "ARMATURE" and m.object:
            entry["armature"] = m.object.name
    # sample weights on a few verts
    samples = []
    for vi in list(range(0, min(len(o.data.vertices), 8))):
        v = o.data.vertices[vi]
        weights = []
        for g in o.vertex_groups:
            try:
                w = g.weight(vi)
            except RuntimeError:
                continue
            if w > 1e-6:
                weights.append({"group": g.name, "w": round(w, 4)})
        samples.append({"vert": vi, "weights": sorted(weights, key=lambda x: -x["w"])[:6]})
    entry["weightSamples"] = samples
    # face / polygon 914
    if len(o.data.polygons) > 914:
        p = o.data.polygons[914]
        verts = list(p.vertices)
        center = [sum(o.data.vertices[i].co[j] for i in verts)/len(verts) for j in range(3)]
        entry["face914"] = {"polyIndex": 914, "vertIndices": verts, "centerLocal": [round(c, 6) for c in center], "materialIndex": p.material_index}
        report["face914"] = {"object": o.name, **entry["face914"]}
    else:
        entry["face914"] = None
        report["limitations"].append(f"{o.name} has only {len(o.data.polygons)} polys; index 914 absent on this mesh")
    report["targets"].append(entry)
if not cands:
    report["limitations"].append("No mesh matched subscapularis/BP4795 via name/sourceName; MCP name search only")
print(json.dumps(report, indent=2)[:12000])
