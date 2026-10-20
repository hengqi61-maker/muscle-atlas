"""Isolated correction of PR21 ordering, weight conservation and palm-space consistency.
Original assets and base geometry remain immutable. Spatial attachment remains uncalibrated.
"""
import bpy,sys,json,hashlib,struct,math
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'artifacts/grasp-fix';OUT.mkdir(parents=True,exist_ok=True)
SRC=ROOT/'public/experimental/rig-v2/unified-rig-prototype.glb'
assert hashlib.sha256(SRC.read_bytes()).hexdigest()=='ef803a4bbb3c644504c124519e39ba0b3b760ec139eaf60d277ef7f7f5d23274'
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(SRC),bone_heuristic='BLENDER')
rig=next(o for o in bpy.data.objects if o.type=='ARMATURE');meshes=[o for o in bpy.data.objects if o.type=='MESH' and o.get('sourceName')];assert len(meshes)==467
sha=lambda o:hashlib.sha256(b''.join(struct.pack('<3f',*v.co)for v in o.data.vertices)).hexdigest()
before={o['sourceName']:sha(o)for o in meshes};canonical={b.name:[list(r)for r in b.matrix_local]for b in rig.data.bones}
# Retain API/30-joint names; fix shared ordering. Positions are engineering references, not anatomical landmarks.
order=['Little','Ring','Middle','Index'];across_at={'Little':-.018,'Ring':0.,'Middle':.018,'Index':.036,'Thumb':.04675}
chains={'Thumb':['CMC','MCP','IP'],**{d:['MCP','PIP','DIP']for d in order}}
frames={};bpy.context.view_layer.objects.active=rig;bpy.ops.object.mode_set(mode='EDIT')
for side,sign in [('Left',1),('Right',-1)]:
 socket=rig.data.edit_bones[side+'FingerSocket'];origin=socket.head.copy();distal=(socket.tail-socket.head).normalized();across=Vector((sign,0,0));across=(across-distal*across.dot(distal)).normalized();palmar=across.cross(distal).normalized()
 if palmar.y>0:palmar=-palmar
 frames[side]=(origin,distal,across,palmar)
 socket.use_deform=False
 for digit in ['Thumb','Index','Middle','Ring','Little']:
  cursor=origin+across*across_at[digit]+distal*.006;direction=(distal*.92+palmar*.08).normalized()
  if digit=='Thumb':cursor=origin+across*across_at[digit]+palmar*.008+distal*.004;direction=(distal*.55+across*.75+palmar*.15).normalized()
  parent=socket
  for joint in chains[digit]:
   b=rig.data.edit_bones.new(side+digit+joint);b.head=cursor;b.tail=cursor+direction*(.062/3);b.parent=parent;b.use_connect=parent!=socket;b.align_roll(palmar);cursor=b.tail.copy();parent=b
bpy.ops.object.mode_set(mode='OBJECT')
assert {n:[list(r)for r in rig.data.bones[n].matrix_local]for n in canonical}==canonical
changes=[];max_mass_error=0.;max_other_error=0.;max_row_sum_error=0.;rootinv=rig.matrix_world.inverted()
for o in meshes:
 name=o['sourceName'].lower()
 # Forearm membrane and wrist retinacula are not finger segments. Preserve their source weights.
 if any(x in name for x in ['foot','halluc','leg','interosseous membrane','retinaculum']):continue
 if not any(x in name for x in ['hand','pollicis','lumbrical','interossei']):continue
 local=rootinv@o.matrix_world;points=[local@v.co for v in o.data.vertices];side='Left'if sum(p.x for p in points)>0 else'Right';origin,distal,across,palmar=frames[side]
 donors=[g for g in o.vertex_groups if g.name in [side+'Hand',side+'Wrist',side+'FingerSocket']]
 if not donors:continue
 for d in chains:
  for j in chains[d]:
   if not o.vertex_groups.get(side+d+j):o.vertex_groups.new(name=side+d+j)
 touched=0
 for v,p in zip(o.data.vertices,points):
  old={o.vertex_groups[g.group].name:g.weight for g in v.groups};s=sum(old.values());hw=sum(old.get(g.name,0)for g in donors)
  if hw<.12:continue
  delta=p-origin;u=delta.dot(across);length=delta.dot(distal)
  # Shared bone/assignment ordering; nearest finger transverse reference, thumb radial zone.
  digit=min(across_at,key=lambda d:abs(u-across_at[d]));sl=max(0.,min(.999,length/.07));joint=chains[digit][min(2,int(sl*3))];keep=max(.15,.55*(1-sl));transfer=0.
  for g in donors:
   cur=old.get(g.name,0)
   if cur: g.add([v.index],cur*keep,'REPLACE');transfer+=cur*(1-keep)
  target=o.vertex_groups[side+digit+joint];target.add([v.index],transfer,'ADD')
  new={o.vertex_groups[g.group].name:g.weight for g in v.groups};max_mass_error=max(max_mass_error,abs(sum(new.values())-s));max_row_sum_error=max(max_row_sum_error,abs(sum(new.values())-1))
  for n,w in old.items():
   if n not in [g.name for g in donors]:max_other_error=max(max_other_error,abs(new.get(n,0)-w))
  touched+=1
 if touched:changes.append({'sourceName':o['sourceName'],'side':side,'vertices':touched})
assert max_mass_error<1e-6 and max_other_error==0
assert before=={o['sourceName']:sha(o)for o in meshes}
bpy.context.view_layer.update();blend=OUT/'mapping-fix.blend';bpy.ops.wm.save_as_mainfile(filepath=str(blend));glb=OUT/'mapping-fix.glb';bpy.ops.export_scene.gltf(filepath=str(glb),export_format='GLB',export_extras=True,export_skins=True,export_animations=False,export_morph=False)
report={'sourceSha256':hashlib.sha256(SRC.read_bytes()).hexdigest(),'candidateSha256':hashlib.sha256(glb.read_bytes()).hexdigest(),'sourceMeshCount':len(meshes),'sourceBasePositionHashes':before,'allBaseGeometryUnchanged':True,'canonical27MatricesUnchanged':True,'boneCount':len(rig.data.bones),'maxWeightMassError':max_mass_error,'maxUnrelatedWeightError':max_other_error,'maxRowSumError':max_row_sum_error,'touched':changes,'attachmentStatus':'UNCALIBRATED_SPATIAL_HYPOTHESIS','graspStatus':'NOT_ACCEPTED','scope':'Correct ordering, conserved donor mass, same rig-local palm frame; no shell, source geometry or production changes.'}
(OUT/'build-report.json').write_text(json.dumps(report,indent=2));print('CANDIDATE',report['candidateSha256'],'mass',max_mass_error,'other',max_other_error,'meshes',len(changes))
