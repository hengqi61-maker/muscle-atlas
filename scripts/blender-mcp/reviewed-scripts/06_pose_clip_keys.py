import bpy, json
report = {"actions": [], "nla": [], "blender": bpy.app.version_string}
for act in bpy.data.actions:
    entry = {"name": act.name}
    # Blender 5+: Action.layers / slots; legacy fcurves may be absent
    fcount = None
    if hasattr(act, "fcurves"):
        try:
            fcount = len(act.fcurves)
        except Exception:
            fcount = None
    if fcount is None and hasattr(act, "layers"):
        try:
            fcount = sum(len(getattr(strip, "channelbag", lambda: None)() or []) for layer in act.layers for strip in getattr(layer, "strips", []))
        except Exception:
            fcount = -1
    # channelbags API fallback
    if fcount in (None, -1, 0) and hasattr(act, "slots"):
        entry["slots"] = [getattr(s, "name_display", getattr(s, "identifier", str(s))) for s in act.slots]
        entry["slotCount"] = len(act.slots)
    entry["fcurvesOrChannels"] = fcount
    report["actions"].append(entry)
for obj in bpy.data.objects:
    if obj.animation_data and obj.animation_data.nla_tracks:
        for tr in obj.animation_data.nla_tracks:
            for st in tr.strips:
                report["nla"].append({
                    "object": obj.name,
                    "track": tr.name,
                    "strip": st.name,
                    "action": st.action.name if st.action else None,
                    "frame_start": st.frame_start,
                    "frame_end": st.frame_end,
                })
names = [a.name for a in bpy.data.actions]
report["curlLike"] = [n for n in names if "curl" in n.lower()]
report["pulldownLike"] = [n for n in names if "pull" in n.lower() or "pulldown" in n.lower()]
# also scan object/custom props / shape keys
sk = []
for o in bpy.data.objects:
    if o.type == "MESH" and o.data.shape_keys:
        for kb in o.data.shape_keys.key_blocks:
            if any(x in kb.name.lower() for x in ("curl", "pull", "pose", "probe")):
                sk.append({"object": o.name, "key": kb.name})
report["shapeKeyHits"] = sk[:40]
print(json.dumps(report, indent=2)[:8000])
