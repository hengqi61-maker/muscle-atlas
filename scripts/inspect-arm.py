import bpy,json,pathlib
from mathutils import Vector
root=pathlib.Path(__file__).resolve().parents[1]
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.gltf(filepath=str(root/'public/models/anatomy.glb'))
report=[]
for o in bpy.context.scene.objects:
 if o.type=='MESH' and any(s in o.name for s in ['left biceps','left triceps','left brachialis','left deltoid','left forearm','left flexor','left extensor','left hand','left pronator','left supinator']):
  pts=[v.co for v in o.data.vertices]
  report.append({'name':o.name,'localMin':[min(v[i] for v in pts) for i in range(3)],'localMax':[max(v[i] for v in pts) for i in range(3)],'matrix':[list(row) for row in o.matrix_world]})
(root/'docs/evidence/arm-bounds.json').write_text(json.dumps(report,indent=2))
