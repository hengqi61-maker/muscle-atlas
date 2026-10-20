"""Render actual inherited CCD trajectory on original PR21 source; diagnostic FAIL only."""
import bpy,sys,json,math,hashlib,struct,time,os
from pathlib import Path
from mathutils import Matrix,Vector
root=Path(__file__).resolve().parents[2];measure_only='--measure-only' in sys.argv;out=root/os.environ.get('GRASP_NATIVE_OUTPUT',('artifacts/grasp-v1/p3-basis/native-contact' if measure_only else 'artifacts/grasp-v1/p3-basis/native-official'));out.mkdir(parents=True,exist_ok=False)
asset=root/os.environ.get('GRASP_ASSET','artifacts/grasp-v1/grasp-controller.glb');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert sha(asset)==os.environ.get('GRASP_ASSET_SHA','40e3dbcbbe3423381dd2885936dd3f1c7d4355bcc6b4f0c30eb9245537be1dff')
input_path=root/os.environ.get('GRASP_SEQUENCE_INPUT','artifacts/grasp-v1/p3-basis/official-sequence/official-bar-align.json');r=json.loads(input_path.read_text());raw=asset.read_bytes();g=json.loads(raw[20:20+struct.unpack_from('<I',raw,12)[0]])
def mat(a):return Matrix([a[i::4] for i in range(4)])
parents={c:i for i,n in enumerate(g['nodes']) for c in n.get('children',[])};world={}
def wm(i):
 if i not in world:
  n=g['nodes'][i]
  if 'matrix'in n:L=mat(n['matrix'])
  else:
   from mathutils import Quaternion
   x,y,z,w=n.get('rotation',[0,0,0,1]);L=Matrix.LocRotScale(Vector(n.get('translation',[0,0,0])),Quaternion((w,x,y,z)),Vector(n.get('scale',[1,1,1])))
  world[i]=(wm(parents[i])@L) if i in parents else L
 return world[i]
reference={n['name']:wm(i) for i,n in enumerate(g['nodes']) if n.get('name')}
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(asset),bone_heuristic='BLENDER');scene=bpy.context.scene;rig=next(o for o in scene.objects if o.type=='ARMATURE');sources=[o for o in scene.objects if o.type=='MESH' and o.get('sourceName')];assert len(sources)==467;original={o.name:hashlib.sha256(b''.join(struct.pack('<3f',*v.co)for v in o.data.vertices)).hexdigest()for o in sources}
C=Matrix(((1,0,0,0),(0,0,1,0),(0,-1,0,0),(0,0,0,1)));ci=C.inverted();K={p.name:reference[p.name].inverted()@C@rig.matrix_world@p.matrix@ci for p in rig.pose.bones};restLocal={p.name:(p.bone.parent.matrix_local.inverted()@p.bone.matrix_local if p.parent else p.bone.matrix_local.copy())for p in rig.pose.bones}
def apply(row):
 desired={n:rig.matrix_world.inverted()@ci@mat(m)@K[n]@C for n,m in row['boneWorldMatrices'].items()}
 for p in rig.pose.bones:
  local=desired[p.parent.name].inverted()@desired[p.name] if p.parent else desired[p.name]
  p.matrix_basis=restLocal[p.name].inverted()@local
 bpy.context.view_layer.update()
if measure_only:
 import numpy as np,re
 selected=[o for o in sources if re.search(r'hand|pollicis|lumbrical|interosse|digiti minimi|retinaculum',o.get('sourceName',''),re.I) and not re.search(r'foot|halluc|plantar| of left leg| of right leg',o.get('sourceName',''),re.I)]
 ownership={}
 for o in selected:
  sums={'Left':0.,'Right':0.}
  for v in o.data.vertices:
   for a in v.groups:
    n=o.vertex_groups[a.group].name
    for side in sums:
     if n.startswith(side):sums[side]+=a.weight
  ownership[o.name]=max(sums,key=sums.get)
 results=[];deps=bpy.context.evaluated_depsgraph_get()
 for row in r['phases']:
  apply(row);record={'progress':row['progress'],'hands':[]}
  for hand in row['tissue']['byHand']:
   side=hand['side'];a=np.array(hand['segment']['from']);b=np.array(hand['segment']['to']);axis=b-a;half=np.linalg.norm(axis)/2;axis/=2*half;mid=(a+b)/2;radius=hand['segment']['radius']*math.cos(math.pi/12);minimum=float('inf');count=0
   for o in selected:
    if ownership[o.name]!=side:continue
    ev=o.evaluated_get(deps);mesh=ev.to_mesh();coords=np.empty(len(mesh.vertices)*3,dtype=np.float64);mesh.vertices.foreach_get('co',coords);points=coords.reshape((-1,3));M=np.array(C@ev.matrix_world);points=points@M[:3,:3].T+M[:3,3];ev.to_mesh_clear();rel=points-mid;t=rel@axis;axial=np.abs(t)-half;radial=np.linalg.norm(rel-t[:,None]*axis,axis=1)-radius;values=np.where((axial<=0)&(radial<=0),np.maximum(radial,axial),np.hypot(np.maximum(radial,0),np.maximum(axial,0)));minimum=min(minimum,float(values.min()));count+=len(values)
   record['hands'].append({'side':side,'minInscribedSolidSignedM':minimum,'vertices':count,'threeMinM':hand['tissue']['minSignedM'],'engineDifferenceM':abs(minimum-hand['tissue']['minSignedM'])})
  results.append(record)
 (out/'native-contact.json').write_text(json.dumps({'assetSha256':sha(asset),'trajectorySha256':sha(input_path),'samples':results,'method':'Actual Blender evaluated source vertices in shared metricworld; finite conservative12goninscribedsolid, same ownership and segments as Three. Vertex witnesses only; no positive grasp inference.','status':'FAIL_TISSUE_GRASP'if any(h['minInscribedSolidSignedM']<0 for f in results for h in f['hands'])else'INCONCLUSIVE','maxEngineDifferenceM':max(h['engineDifferenceM']for f in results for h in f['hands'])},indent=2));(out/'executed.py').write_bytes(Path(__file__).read_bytes());print('NATIVE_CONTACT_COMPLETE',len(results));sys.exit(0)
scene.render.engine='BLENDER_EEVEE';scene.eevee.taa_render_samples=8;scene.render.resolution_x=512;scene.render.resolution_y=512;scene.render.resolution_percentage=100
scene.world=bpy.data.worlds.new('Diagnostic world');scene.world.use_nodes=True;bg=scene.world.node_tree.nodes.get('Background') or scene.world.node_tree.nodes.new('ShaderNodeBackground');bg.inputs[0].default_value=(.035,.045,.055,1)
def material(name,color):
 m=bpy.data.materials.new(name);m.use_nodes=True;m.node_tree.nodes.clear();b=m.node_tree.nodes.new('ShaderNodeBsdfPrincipled');o=m.node_tree.nodes.new('ShaderNodeOutputMaterial');m.node_tree.links.new(b.outputs[0],o.inputs[0]);b.inputs['Base Color'].default_value=(*color,1);b.inputs['Roughness'].default_value=.7;return m
bodymat=material('Source tissue diagnostic',(.65,.73,.76));gripmat=material('Actual grip diagnostic',(.1,.12,.14))
for o in sources:o.data.materials.clear();o.data.materials.append(bodymat)
bars={}
for side in ['Left','Right']:
 s=r['phases'][0]['tissue']['byHand'][0 if side=='Left' else 1]['segment'];a=ci@Vector(s['from']);b=ci@Vector(s['to']);d=b-a;bpy.ops.mesh.primitive_cylinder_add(vertices=12,radius=s['radius'],depth=d.length,location=(a+b)/2);o=bpy.context.object;o.name='ActualAngledGrip'+side;o.rotation_euler=d.to_track_quat('Z','Y').to_euler();o.data.materials.append(gripmat);bars[side]=o
for pos in [(2,-4,4),(-2,2,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);bpy.context.object.data.energy=400;bpy.context.object.data.shape='DISK';bpy.context.object.data.size=3
bpy.ops.object.camera_add();cam=bpy.context.object;scene.camera=cam;cam.data.lens=42
bpy.ops.object.text_add();label=bpy.context.object;label.data.body='P2 ARM REACH PROBE / FAIL';label.parent=cam;label.location=(-.22,.17,-.6);label.rotation_euler=(0,0,0);label.data.size=.012
# Native bone origin roundtrip proof for every121 input row; no source coordinate edits.
error=0
for row in r['phases']:
 apply(row)
 for n,m in row['boneWorldMatrices'].items():
  p=C@(rig.matrix_world@rig.pose.bones[n].matrix.translation);target=mat(m).translation;error=max(error,(p-target).length)
frames=out/'sequence';frames.mkdir();start=time.monotonic()
for j,index in enumerate(range(0,121,4)):
 row=r['phases'][index];apply(row)
 for h in row['tissue']['byHand']:
  a=ci@Vector(h['segment']['from']);b=ci@Vector(h['segment']['to']);bars[h['side']].location=(a+b)/2
 target=ci@mat(row['boneWorldMatrices']['LeftHand']).translation
 cam.location=target+Vector((.17,-.29,.13));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();scene.render.filepath=str(frames/f'{j:04d}.png');bpy.ops.render.render(write_still=True)
assert all(hashlib.sha256(b''.join(struct.pack('<3f',*v.co)for v in o.data.vertices)).hexdigest()==original[o.name]for o in sources)
bpy.ops.wm.save_as_mainfile(filepath=str(out/'official-reach-diagnostic.blend'))
(out/'native-report.json').write_text(json.dumps({'assetSha256':sha(asset),'trajectorySha256':sha(input_path),'frames':31,'sampleCoverage':121,'maxBoneOriginRoundtripErrorM':error,'sourceIdentities':467,'allOriginalBaseGeometryUnchanged':True,'samples':8,'scope':'Original source tissues and actual two12gonsegments. Camera follows left hand. Inherited unconstrained CCD, NOT seated exercise, no skin shell, no grasp acceptance.','secondsRender':time.monotonic()-start},indent=2));(out/'executed.py').write_bytes(Path(__file__).read_bytes())
