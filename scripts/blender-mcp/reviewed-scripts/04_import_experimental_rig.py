import bpy, os
from pathlib import Path
src = Path(os.environ["BLENDER_MCP_ATLAS_GLB"]).resolve()
assert src.is_file() and "experimental" in str(src), "Only experimental GLB copy allowed"
# clear default cube if any
for obj in list(bpy.data.objects):
    bpy.data.objects.remove(obj, do_unlink=True)
bpy.ops.import_scene.gltf(filepath=str(src))
print("IMPORTED", src.name, "objects", len(bpy.data.objects), "armatures", len([o for o in bpy.data.objects if o.type=="ARMATURE"]))
