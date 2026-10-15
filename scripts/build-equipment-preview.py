"""Export this project's original hex dumbbell independently, no rig or anatomy."""
import bpy,pathlib,sys,json,hashlib
root=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'scripts'))
from grip_geometry import create_hex_dumbbell
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
create_hex_dumbbell((0,0,0),None,None)
path=root/'public/models/equipment/detailed-hex-dumbbell.glb';path.parent.mkdir(parents=True,exist_ok=True)
bpy.context.view_layer.update()
points=[o.matrix_world@v.co for o in bpy.context.scene.objects if o.type=='MESH' for v in o.data.vertices]
dimensions=[max(p[i] for p in points)-min(p[i] for p in points) for i in range(3)]
bpy.ops.export_scene.gltf(filepath=str(path),export_format='GLB',export_animations=False,export_extras=True)
(root/'docs/evidence/equipment-manifest.json').write_text(json.dumps({'asset':'equipment/detailed-hex-dumbbell.glb','sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'origin':'original project geometry, not downloaded','dimensionsMetresBlenderXYZ':dimensions,'details':['bevelled hex rubber heads','geometry knurled28mm steel handle','collars','inset badge and original8mark'],'reference':'Public real-scale hex dumbbell dimensions; source candidate403not imported'},indent=2))
