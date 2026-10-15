"""Run with Blender --background --python scripts/blender-import.py."""
import bpy,json,pathlib
root=pathlib.Path(__file__).resolve().parents[1]
asset=root/'public/models/anatomy.glb'
assert asset.is_file(), asset
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.gltf(filepath=str(asset))
report={'blender':bpy.app.version_string,'meshes':sum(o.type=='MESH' for o in bpy.context.scene.objects),'armatures':sum(o.type=='ARMATURE' for o in bpy.context.scene.objects),'status':'native import verified; unrigged'}
(root/'docs/blender-inspection.json').write_text(json.dumps(report,indent=2))
(root/'artifacts').mkdir(exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(root/'artifacts/anatomy-import.blend'))
print(json.dumps(report))
