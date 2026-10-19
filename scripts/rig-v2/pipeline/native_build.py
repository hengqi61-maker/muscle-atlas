"""Fresh scene reconstruction from immutable source + shared rig + explicit weights."""
import bpy,json,hashlib,os,struct,math,time
from pathlib import Path
import numpy as np
from mathutils import Vector,Matrix
ROOT=Path(os.environ['PIPELINE_ROOT']);OUT=Path(os.environ['PIPELINE_OUT']);definition=json.loads(Path(os.environ['PIPELINE_DEFINITION']).read_text());OUT.mkdir(parents=True,exist_ok=True)
def read(p):return json.loads((ROOT/p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def digest(vs):return hashlib.sha256(b''.join(struct.pack('<3f',*v) for v in vs)).hexdigest()
for p,h in definition['inputHashes'].items():assert sha(ROOT/p)==h,(p,'input SHA mismatch')
canonical=read(definition['canonicalRig']);registry=read(definition['attachmentRegistry']);records={r['name']:r for r in registry};mapping=read(definition['meshMapping']);observed=read(definition['trajectory']);clip=next(c for c in observed['clips'] if c['name']==definition['clip'])
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False);bpy.ops.import_scene.gltf(filepath=str(ROOT/definition['sourceGlb']))
meshes=sorted([o for o in bpy.context.scene.objects if o.type=='MESH'],key=lambda o:o.name);assert len(meshes)==467 and set(o.name for o in meshes)==set(records)
preservation=[]
for o in meshes:
 r=records[o.name];assert digest([v.co[:] for v in o.data.vertices])==r['sourceVertexSha256'];faces=[list(p.vertices) for p in o.data.polygons];o.parent=None;o.matrix_world.identity()
 for v in o.data.vertices:x,y,z=v.co;v.co=Vector((x,z,-y))/1000
 assert digest([v.co[:] for v in o.data.vertices])==r['canonicalVertexSha256'];o['sourceName']=o.name
 for k in ['fmaId','bpId','source']:o[k]=str(r['source'].get(k,''))
 for p in o.data.polygons:p.use_smooth=True
 groups={name:o.vertex_groups.new(name=name) for name in r['bones']}
 for i,weights in enumerate(r['vertexWeights']):
  assert abs(sum(weights.values())-1)<1e-6
  for name,w in weights.items():groups[name].add([i],w,'REPLACE')
 preservation.append({'sourceName':o.name,'canonicalVertexSha256':digest([v.co[:] for v in o.data.vertices]),'facesSha256':hashlib.sha256(json.dumps(faces,separators=(',',':')).encode()).hexdigest(),'vertexCount':len(o.data.vertices),'polygonCount':len(faces)})
arm=bpy.data.armatures.new('MuscleAtlasV2Skeleton');rig=bpy.data.objects.new(canonical['rig'],arm);bpy.context.collection.objects.link(rig);bpy.context.view_layer.objects.active=rig;rig.select_set(True);bpy.ops.object.mode_set(mode='EDIT')
for b in canonical['bones']:
 eb=arm.edit_bones.new(b['name']);eb.head=b['headM'];eb.tail=b['tailM'];eb.use_deform=b['deform'];eb.matrix=Matrix(b['restWorldMatrix'])
 if b['parent']:eb.parent=arm.edit_bones[b['parent']]
bpy.ops.object.mode_set(mode='OBJECT')
for o in meshes:mod=o.modifiers.new('CanonicalSourceSkin','ARMATURE');mod.object=rig
scene=bpy.context.scene;scene.render.fps=30;scene.frame_start=0;scene.frame_end=120
for p in rig.pose.bones:p.rotation_mode='QUATERNION'
for sample in clip['samples']:
 for name,transform in sample['bones'].items():
  p=rig.pose.bones[name];p.location=transform['location'];p.rotation_quaternion=transform['quaternionWxyz'];p.scale=transform['scale'];p.keyframe_insert(data_path='rotation_quaternion',frame=sample['frame'],group=p.name)
action=rig.animation_data.action;action.name=clip['name']
trajectory=[];diagnostics=[];deps=bpy.context.evaluated_depsgraph_get()
# Full 121-pose bone observation; geometry at five phases, explicit coverage.
for f in range(121):
 scene.frame_set(f);bpy.context.view_layer.update();trajectory.append({'frame':f,'timeSeconds':f/30,'bones':{p.name:{'worldMatrix':[float(p.matrix[r][c]) for c in range(4) for r in range(4)]} for p in rig.pose.bones}})
 if f not in [0,30,60,90,120]:continue
 rows=[]
 for o in meshes:
  rest=np.asarray([v.co[:] for v in o.data.vertices]);ev=o.evaluated_get(deps);me=ev.to_mesh();posed=np.asarray([v.co[:] for v in me.vertices]);o.data.calc_loop_triangles();tri=np.asarray([t.vertices[:] for t in o.data.loop_triangles]);a=np.linalg.norm(np.cross(rest[tri[:,1]]-rest[tri[:,0]],rest[tri[:,2]]-rest[tri[:,0]]),axis=1);b=np.linalg.norm(np.cross(posed[tri[:,1]]-posed[tri[:,0]],posed[tri[:,2]]-posed[tri[:,0]]),axis=1);ratio=b[a>2e-12]/a[a>2e-12];count=int((ratio<.05).sum());edges=np.asarray([e.vertices[:] for e in o.data.edges]);r=np.linalg.norm(rest[edges[:,1]]-rest[edges[:,0]],axis=1);p=np.linalg.norm(posed[edges[:,1]]-posed[edges[:,0]],axis=1);stretch=float((p[r>1e-7]/r[r>1e-7]).max());ev.to_mesh_clear()
  if count or stretch>3:rows.append({'sourceName':o.name,'countBelowFivePercent':count,'eligibleTriangles':len(ratio),'severeAlarm':count>3 or count>.01*len(ratio),'maxEdgeRatio':stretch})
 diagnostics.append({'frame':f,'meshes':rows})
(OUT/'trajectory.json').write_text(json.dumps(trajectory,separators=(',',':')));(OUT/'source-preservation.json').write_text(json.dumps(preservation,indent=2));(OUT/'geometry.json').write_text(json.dumps({'thresholds':{'areaRatio':.05,'absoluteCountStrictlyGreater':3,'fractionStrictlyGreater':.01,'maxEdgeRatioAlarm':3},'coverage':'all source triangles at 5 phases; not full121 geometry; existing independent audit remains authoritative','samples':diagnostics},indent=2))
scene.frame_set(0);bpy.ops.export_scene.gltf(filepath=str(OUT/'motion.glb'),export_format='GLB',export_animations=True,export_animation_mode='ACTIONS',export_force_sampling=True,export_skins=True,export_morph=False,export_extras=True,export_yup=True)
world=bpy.data.worlds.new('PipelineWorld');scene.world=world;world.use_nodes=True;bg=world.node_tree.nodes.new('ShaderNodeBackground');wo=world.node_tree.nodes.new('ShaderNodeOutputWorld');world.node_tree.links.new(bg.outputs[0],wo.inputs['Surface']);bg.inputs[0].default_value=(.04,.055,.07,1);bg.inputs[1].default_value=.5
for loc in [(2,-3,4),(-3,-1,2),(0,3,3)]:
 bpy.ops.object.light_add(type='AREA',location=loc);l=bpy.context.object;l.data.energy=800;l.data.size=4;l.rotation_euler=(Vector((0,0,.9))-l.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add();cam=bpy.context.object;scene.camera=cam;cam.data.type='ORTHO';scene.render.engine='BLENDER_EEVEE';scene.render.resolution_x=384;scene.render.resolution_y=384;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
clean=bpy.data.materials.new('CleanDiagnostic');clean.diffuse_color=(.48,.62,.69,1);original={o.name:list(o.data.materials) for o in meshes}
def render(path,view):
 if view in ['left-hand','right-hand']:
  L='Left' if view=='left-hand' else 'Right';target=rig.pose.bones[L+'Hand'].head.copy();loc=target+Vector((.25,-.6,.1));cam.data.ortho_scale=.28
 else:target=Vector((0,-.07,.84));loc={'front':(0,-4,.84),'side':(4,0,.84),'back':(0,4,.84)}[view];cam.data.ortho_scale=1.95
 cam.location=loc;cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();scene.render.filepath=str(path);bpy.ops.render.render(write_still=True)
for style in ['Real','Clean']:
 for o in meshes:
  o.data.materials.clear()
  for mat in (original[o.name] if style=='Real' else [clean]):o.data.materials.append(mat)
 for f in [0,30,60,90,120]:
  scene.frame_set(f)
  for view in ['front','side','back','left-hand','right-hand']:render(OUT/f'{style}-{view}-{f:03d}.png',view)
# Video is actual production Blender render, 31 observed poses / 4 seconds.
seq=OUT/'sequence';seq.mkdir(exist_ok=True)
for i,f in enumerate(range(0,121,4)):scene.frame_set(f);render(seq/f'{i:03d}.png','front')
scene.frame_set(0);bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'motion.blend'))
(OUT/'native-summary.json').write_text(json.dumps({'blenderVersion':bpy.app.version_string,'meshCount':len(meshes),'boneCount':len(arm.bones),'clip':clip['name'],'sourceIdentityExact':True,'referenceRestMatrices':{b.name:[list(row) for row in b.matrix_local] for b in arm.bones},'weightsSha256':sha(ROOT/definition['attachmentRegistry']),'nativeRenderFrames':81},indent=2))
print('PIPELINE_NATIVE_COMPLETE',OUT)
