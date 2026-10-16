"""Supplementary native animation and triangle collision evidence, no asset mutation."""
import bpy,pathlib,json,runpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
ROOT=pathlib.Path(__file__).resolve().parents[2];OUT=ROOT/'artifacts/rig-v2'
bpy.ops.wm.open_mainfile(filepath=str(OUT/'unified-rig-prototype.blend'))
scene=bpy.context.scene;rig=bpy.data.objects['MuscleAtlasV2Rig'];meshes=[o for o in scene.objects if o.type=='MESH'];deps=bpy.context.evaluated_depsgraph_get()
def tree(o):
 ev=o.evaluated_get(deps);m=ev.to_mesh();m.calc_loop_triangles();vertices=[ev.matrix_world@v.co for v in m.vertices];polygons=[t.vertices[:] for t in m.loop_triangles];result=BVHTree.FromPolygons(vertices,polygons,all_triangles=True,epsilon=1e-7);ev.to_mesh_clear();return result
pairs=[]
# Anatomical tissues normally overlap. Explicitly report actual triangle intersections,
# preserving rest baseline separately rather than calling each overlap a collision defect.
for L in ['left','right']:
 for arm in [L+' biceps brachii',L+' brachialis',L+' brachioradialis']:
  if arm not in bpy.data.objects:continue
  for body in ['costal part of '+L+' pectoralis major',L+' latissimus dorsi']:
   if body in bpy.data.objects:pairs.append((arm,body))
collisions=[]
for clip in ['CurlProbe','PulldownProbe']:
 rig.animation_data.action=bpy.data.actions[clip]
 for frame in [0,30,60,90,120]:
  scene.frame_set(frame);rows=[]
  for a,b in pairs:
   overlaps=tree(bpy.data.objects[a]).overlap(tree(bpy.data.objects[b]));rows.append({'meshA':a,'meshB':b,'intersectingTrianglePairs':len(overlaps),'examples':overlaps[:8]})
  collisions.append({'clip':clip,'frame':frame,'pairs':rows})
(OUT/'collision-diagnostics.json').write_text(json.dumps({'scope':'selected arm/torso actual triangle intersections, not whole-body clearance; preexisting anatomical intersections require review','epsilonM':1e-7,'samples':collisions},indent=2))
# Check reusable correction algorithm on the real pose binding, without silently
# installing unreviewed morph targets into the R1 asset.
cf=runpy.run_path(str(ROOT/'scripts/rig-v2/corrective_framework.py'));checks=[]
rig.animation_data.action=bpy.data.actions['CurlProbe'];scene.frame_set(60)
transforms={b.name:rig.pose.bones[b.name].matrix@b.matrix_local.inverted() for b in rig.data.bones}
for name in ['left brachioradialis','right brachioradialis','left brachialis']:
 o=bpy.data.objects[name];groups={g.index:g.name for g in o.vertex_groups};rows=[]
 for v in o.data.vertices:
  binding=[(groups[g.group],g.weight) for g in v.groups if g.weight>0]
  if len(binding)>1:
   delta,metric=cf['inverse_lbs_delta'](v.co,transforms,binding);rows.append(metric)
 checks.append({'mesh':name,'multiBoneVertices':len(rows),'minimumDeterminant':min(r['determinant'] for r in rows),'maxProposedDeltaM':max(r['deltaMagnitudeM'] for r in rows),'installed':False})
(OUT/'corrective-framework-probe.json').write_text(json.dumps({'status':'real-pose numerical probe; not installed/validated correction','meshes':checks},indent=2))
scene.render.resolution_x=384;scene.render.resolution_y=384;scene.render.resolution_percentage=100
for clip in ['CurlProbe','PulldownProbe']:
 folder=OUT/(clip+'-sequence');folder.mkdir(exist_ok=True);rig.animation_data.action=bpy.data.actions[clip]
 for i,frame in enumerate(range(0,121,4)):
  scene.frame_set(frame);scene.render.filepath=str(folder/(str(i).zfill(3)+'.png'));bpy.ops.render.render(write_still=True)
print('V2_SUPPLEMENT_COMPLETE')
