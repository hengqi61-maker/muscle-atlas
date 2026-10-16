"""R1 illustrative canonical rig; run via Blender Agent runpy.run_path(absolute path)."""
import bpy, math, json, pathlib, hashlib, struct, sys
import numpy as np
from mathutils import Vector, Quaternion
ROOT=pathlib.Path(__file__).resolve().parents[2]
OUT=ROOT/'artifacts/rig-v2'; OUT.mkdir(parents=True,exist_ok=True)
CFG=ROOT/'config/rig-v2'; CFG.mkdir(parents=True,exist_ok=True)
source=ROOT/'public/models/anatomy.glb'
assert hashlib.sha256(source.read_bytes()).hexdigest()=='6e84529b60b64cc8f8d5cef665fda932e359e828b66d0c2dd44ec1bd9d0bd01f'
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.gltf(filepath=str(source))
meshes=sorted([o for o in bpy.context.scene.objects if o.type=='MESH'],key=lambda o:o.name)
assert len(meshes)==467
mapping={r['name']:r for r in json.loads((ROOT/'public/models/mesh_mapping.json').read_text())}
def digest(points):return hashlib.sha256(b''.join(struct.pack('<3f',*p) for p in points)).hexdigest()
raw={o.name:digest([v.co[:] for v in o.data.vertices]) for o in meshes}
for o in meshes:
 o.parent=None;o.matrix_world.identity()
 for v in o.data.vertices:x,y,z=v.co;v.co=Vector((x,z,-y))/1000
 o.data.update();o['sourceName']=o.name
 for k in ['fmaId','bpId','source']:o[k]=str(mapping[o.name].get(k,''))
 for p in o.data.polygons:p.use_smooth=True
arm=bpy.data.armatures.new('MuscleAtlasV2Skeleton');rig=bpy.data.objects.new('MuscleAtlasV2Rig',arm);bpy.context.collection.objects.link(rig)
bpy.context.view_layer.objects.active=rig;rig.select_set(True);bpy.ops.object.mode_set(mode='EDIT')
def bone(n,h,t,p=None,deform=True):
 b=arm.edit_bones.new(n);b.head=h;b.tail=t;b.use_deform=deform
 if p:b.parent=arm.edit_bones[p]
 b.align_roll(Vector((0,-1,0)));return b
bone('Pelvis',(0,-.1,.80),(0,-.1,.95));bone('Spine',(0,-.1,.95),(0,-.08,1.14),'Pelvis');bone('Thorax',(0,-.08,1.14),(0,-.067,1.36),'Spine');bone('Neck',(0,-.067,1.36),(0,-.067,1.46),'Thorax');bone('Head',(0,-.067,1.46),(0,-.067,1.64),'Neck')
for s,L in [(1,'Left'),(-1,'Right')]:
 bone(L+'Clavicle',(0,-.067,1.31),(s*.09,-.067,1.31),'Thorax');bone(L+'Scapula',(s*.09,-.067,1.31),(s*.173,-.067,1.305),L+'Clavicle');bone(L+'Humerus',(s*.173,-.067,1.305),(s*.213,-.060,1.034),L+'Scapula');bone(L+'Forearm',(s*.213,-.060,1.034),(s*.231,-.105,.815),L+'Humerus');bone(L+'Wrist',(s*.231,-.105,.815),(s*.231,-.110,.795),L+'Forearm');bone(L+'Hand',(s*.231,-.110,.795),(s*.231,-.134,.735),L+'Wrist');bone(L+'FingerSocket',(s*.231,-.134,.735),(s*.231,-.134,.710),L+'Hand',False)
 bone(L+'Thigh',(s*.10,-.10,.83),(s*.11,-.08,.45),'Pelvis');bone(L+'Shin',(s*.11,-.08,.45),(s*.10,-.08,.11),L+'Thigh');bone(L+'Ankle',(s*.10,-.08,.11),(s*.10,-.08,.07),L+'Shin');bone(L+'Foot',(s*.10,-.08,.07),(s*.10,-.23,.04),L+'Ankle')
bpy.ops.object.mode_set(mode='OBJECT')
def smooth(t):t=max(0,min(1,t));return t*t*(3-2*t)
registry=[]
for o in meshes:
 pts=[v.co for v in o.data.vertices];n=o.name;side=1 if 'left' in n else -1 if 'right' in n else 0
 if n in ['left flexor pollicis brevis','right flexor pollicis brevis']:side=1 if sum(v.x for v in pts)>0 else -1
 L='Left' if side==1 else 'Right';lo=min(v.z for v in pts);hi=max(v.z for v in pts);wide=max(abs(v.x) for v in pts)
 cuff=any(k in n for k in ['infraspinatus','subscapularis','supraspinatus','teres minor','teres major'])
 upper=any(k in n for k in ['biceps brachii','triceps brachii','brachialis','deltoid'])
 region='axial-proxy';method='longitudinal axial transition; unvalidated attachment proxy'
 if side and (upper or (wide>.175 and hi<1.175 and lo>.60)):
  region='arm-proxy';method='shared longitudinal shoulder elbow wrist transitions; geometric proxy'
  def fn(v,L=L):
   sh=smooth((1.335-v.z)/.12);f=smooth((1.092-v.z)/.092);h=smooth((.835-v.z)/.060)
   return {L+'Scapula':1-sh,L+'Humerus':sh*(1-f),L+'Forearm':sh*f*(1-h),L+'Hand':sh*f*h}
 elif side and cuff:
  region='scapulohumeral-proxy';xs=sorted(side*v.x for v in pts);a=xs[int(.1*(len(xs)-1))];b=xs[int(.9*(len(xs)-1))]
  def fn(v,L=L,s=side,a=a,b=b):
   t=smooth((s*v.x-a)/max(b-a,.001));return {L+'Scapula':1-t,L+'Humerus':t}
 elif side and hi<1.0 and lo<.60:
  region='leg-proxy'
  def fn(v,L=L):
   t=smooth((.86-v.z)/.12);s=smooth((.51-v.z)/.10);f=smooth((.15-v.z)/.09)
   return {'Pelvis':1-t,L+'Thigh':t*(1-s),L+'Shin':t*s*(1-f),L+'Foot':t*s*f}
 else:
  def fn(v,n=n,L=L,side=side):
   spine=smooth((v.z-.90)/.16);thorax=smooth((v.z-1.08)/.12);neck=smooth((v.z-1.34)/.08);head=smooth((v.z-1.44)/.06)
   attach=0;target=L+'Scapula'
   if side and 'latissimus' in n:attach=smooth((v.z-1.08)/.18)*smooth((abs(v.x)-.08)/.10)*.85;target=L+'Humerus'
   elif side and 'pectoralis major' in n:attach=smooth((abs(v.x)-.10)/.08)*smooth((v.z-1.15)/.12)*.65;target=L+'Humerus'
   elif side and any(k in n for k in ['rhomboid','trapezius','levator scapulae','serratus anterior']):attach=smooth((abs(v.x)-.045)/.12)*.8
   w={'Pelvis':(1-spine),'Spine':spine*(1-thorax),'Thorax':spine*thorax*(1-neck),'Neck':spine*thorax*neck*(1-head),'Head':spine*thorax*neck*head}
   w={k:x*(1-attach) for k,x in w.items()};w[target]=w.get(target,0)+attach;return w
 weights=[];groups={}
 for v in o.data.vertices:
  ws={k:x for k,x in fn(v.co).items() if x>1e-7};total=sum(ws.values());ws={k:x/total for k,x in ws.items()};weights.append(ws)
  for k,w in ws.items():
   if k not in groups:groups[k]=o.vertex_groups.new(name=k)
   groups[k].add([v.index],w,'REPLACE')
 mod=o.modifiers.new('CanonicalSourceSkin','ARMATURE');mod.object=rig
 # Endpoint region is deliberately queryable, never claimed a calibrated origin/insertion.
 ids=sorted(range(len(pts)),key=lambda i:pts[i].z);count=max(1,len(ids)//10)
 record={'name':n,'source':mapping[n],'region':region,'confidence':'unvalidated-geometric-proxy','method':method,'proximalRegion':{'vertexIndices':ids[-count:],'definition':'highest Z decile in canonical rest, not anatomical origin'},'distalRegion':{'vertexIndices':ids[:count],'definition':'lowest Z decile in canonical rest, not anatomical insertion'},'bones':list(groups),'vertexWeights':weights,'sourceVertexSha256':raw[n],'canonicalVertexSha256':digest([v.co[:] for v in o.data.vertices])}
 registry.append(record);o['rigRegion']=region;o['bindingConfidence']='unvalidated-geometric-proxy'
# Portable corrections are scoped by joint/skin weights, independent of clip identity.
# Blender preserve-volume is deliberately disabled: exported linear skin matches native baseline.
scene=bpy.context.scene;scene.render.fps=30;scene.frame_start=0;scene.frame_end=120
for clip in ['CurlProbe','PulldownProbe']:
 action=bpy.data.actions.new(clip);rig.animation_data_create();rig.animation_data.action=action
 for frame in range(0,121,4):
  phase=(1-math.cos(2*math.pi*frame/120))/2
  for p in rig.pose.bones:p.rotation_mode='QUATERNION';p.rotation_quaternion=Quaternion();p.location=(0,0,0);p.scale=(1,1,1)
  for s,L in [(1,'Left'),(-1,'Right')]:
   def rot(name,axis,angle):
    rest=arm.bones[name].matrix_local.to_quaternion();rig.pose.bones[name].rotation_quaternion=rest.inverted()@Quaternion(axis,angle)@rest
   if clip=='CurlProbe':rot(L+'Forearm',(1,0,0),-math.radians(100)*phase)
   else:
    rot(L+'Clavicle',(0,1,0),-s*math.radians(5)*(1-phase));rot(L+'Scapula',(0,1,0),-s*math.radians(15)*(1-phase));rot(L+'Humerus',(0,1,0),-s*math.radians(115-65*phase));rot(L+'Forearm',(1,0,0),-math.radians(25+65*phase))
  for p in rig.pose.bones:p.keyframe_insert(data_path='rotation_quaternion',frame=frame,group=p.name)
 track=rig.animation_data.nla_tracks.new();track.name=clip;strip=track.strips.new(clip,0,action);strip.action_frame_start=0;strip.action_frame_end=120;track.mute=True
rig.animation_data.action=None
contract={'schema':'muscle-atlas-rig-v2-internal-r1','status':'experimental illustrative prototype, not biomechanical calibration or final Windows exchange','rig':rig.name,'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'sourceMeshCount':len(meshes),'blenderConvention':{'unit':'metre','up':'+Z','front':'-Y','left':'+X','handedness':'right','boneLongitudinalAxis':'+Y local','matrixStorage':'row-major nested lists','quaternionOrder':'xyzw'},'exportConvention':{'format':'glTF 2 GLB','up':'+Y','conversion':'Blender exporter export_yup true','clips':['CurlProbe','PulldownProbe']},'bones':[]}
for b in arm.bones:
 q=b.matrix_local.to_quaternion();parent=b.parent.matrix_local if b.parent else None;local=parent.inverted()@b.matrix_local if parent else b.matrix_local
 assert all(math.isfinite(x) for row in b.matrix_local for x in row);assert abs(b.matrix_local.to_3x3().determinant()-1)<1e-5
 contract['bones'].append({'name':b.name,'parent':b.parent.name if b.parent else None,'deform':b.use_deform,'headM':list(b.head_local),'tailM':list(b.tail_local),'restWorldMatrix':list(map(list,b.matrix_local)),'restParentLocalMatrix':list(map(list,local)),'restWorldQuaternionXyzw':[q.x,q.y,q.z,q.w],'landmarkConfidence':'manual geometry estimate; uncalibrated'})
(CFG/'canonical-rig.json').write_text(json.dumps(contract,indent=2));(CFG/'attachment-registry.json').write_text(json.dumps(registry,separators=(',',':')))
# Verify unchanged base through exact stored canonical hash and inverse coordinate roundtrip tolerance.
preservation=[]
for o in meshes:
 error=0
 for v in o.data.vertices:
  x,y,z=v.co;back=(x*1000,-z*1000,y*1000);recanonical=Vector((back[0],back[2],-back[1]))/1000;error=max(error,(recanonical-v.co).length)
 preservation.append({'name':o.name,'baseHashStable':digest([v.co[:] for v in o.data.vertices])==next(r['canonicalVertexSha256'] for r in registry if r['name']==o.name),'inverseTransformRoundtripMaxM':error,'vertexCount':len(o.data.vertices),'polygonCount':len(o.data.polygons),'sourceHash':raw[o.name]})
(OUT/'source-preservation.json').write_text(json.dumps({'all467Preserved':all(r['baseHashStable'] for r in preservation),'meshes':preservation},indent=2))
# Actual evaluated triangles and edges; threshold flags are engineering diagnostics only.
diag=[];deps=bpy.context.evaluated_depsgraph_get()
for clip in ['CurlProbe','PulldownProbe']:
 rig.animation_data.action=bpy.data.actions[clip]
 for frame in [0,30,60,90,120]:
  scene.frame_set(frame);bad=[];minratio=1.;maxratio=1.;collapsed=0
  for o in meshes:
   ev=o.evaluated_get(deps);me=ev.to_mesh();rest=np.array([v.co[:] for v in o.data.vertices]);posed=np.array([v.co[:] for v in me.vertices]);o.data.calc_loop_triangles();tri=np.array([t.vertices[:] for t in o.data.loop_triangles]);a=np.linalg.norm(np.cross(rest[tri[:,1]]-rest[tri[:,0]],rest[tri[:,2]]-rest[tri[:,0]]),axis=1);b=np.linalg.norm(np.cross(posed[tri[:,1]]-posed[tri[:,0]],posed[tri[:,2]]-posed[tri[:,0]]),axis=1);ratio=b[a>2e-12]/a[a>2e-12];c=int((ratio<.05).sum());collapsed+=c
   edges=np.array([e.vertices[:] for e in o.data.edges]);r=np.linalg.norm(rest[edges[:,1]]-rest[edges[:,0]],axis=1);p=np.linalg.norm(posed[edges[:,1]]-posed[edges[:,0]],axis=1);rat=p[r>1e-7]/r[r>1e-7];mn=float(rat.min());mx=float(rat.max());minratio=min(minratio,mn);maxratio=max(maxratio,mx)
   if c or mn<.25 or mx>3:bad.append({'name':o.name,'collapsedTriangles':c,'minEdgeRatio':mn,'maxEdgeRatio':mx})
   ev.to_mesh_clear()
  diag.append({'clip':clip,'frame':frame,'collapsedTrianglesBelowFivePercent':collapsed,'minEdgeRatio':minratio,'maxEdgeRatio':maxratio,'flaggedMeshes':bad,'collisionStatus':'not evaluated here; dedicated collision audit required; source anatomical overlap is not automatically collision'})
(OUT/'deformation-diagnostics.json').write_text(json.dumps(diag,indent=2))
rig.animation_data.action=None
for t in rig.animation_data.nla_tracks:t.mute=False
scene.frame_set(0)
bpy.ops.export_scene.gltf(filepath=str(ROOT/'public/experimental/rig-v2/unified-rig-prototype.glb'),export_format='GLB',export_animations=True,export_animation_mode='NLA_TRACKS',export_frame_range=True,export_frame_step=1,export_force_sampling=True,export_skins=True,export_morph=False,export_extras=True,export_yup=True)
for t in rig.animation_data.nla_tracks:t.mute=True
# Render source anatomy with calm diagnostic lighting; floor provides orientation only.
world=bpy.data.worlds.new('R1World');scene.world=world;world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(.055,.065,.08,1);world.node_tree.nodes['Background'].inputs[1].default_value=.4
for loc,power,size in [((2,-3,4),900,4),((-3,-1,2),700,3),((0,3,3),1000,3)]:
 bpy.ops.object.light_add(type='AREA',location=loc);light=bpy.context.object;light.data.energy=power;light.data.shape='DISK';light.data.size=size;light.rotation_euler=(Vector((0,0,.9))-light.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add();camera=bpy.context.object;scene.camera=camera;camera.data.type='ORTHO';camera.data.ortho_scale=1.95
scene.render.engine='BLENDER_EEVEE';scene.render.resolution_x=640;scene.render.resolution_y=640;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
def render(name,loc):
 camera.location=loc;camera.rotation_euler=(Vector((0,-.07,.84))-camera.location).to_track_quat('-Z','Y').to_euler();scene.render.filepath=str(OUT/(name+'.png'));bpy.ops.render.render(write_still=True)
rig.animation_data.action=None
for p in rig.pose.bones:p.rotation_quaternion=Quaternion()
bpy.context.view_layer.update()
for view,loc in [('front',(0,-4,.84)),('side',(4,0,.84)),('back',(0,4,.84))]:render('rest-'+view,loc)
for clip in ['CurlProbe','PulldownProbe']:
 rig.animation_data.action=bpy.data.actions[clip]
 for frame in [0,30,60,90,120]:scene.frame_set(frame);render(clip+'-'+str(frame).zfill(3),(2,-4,.95))
rig.animation_data.action=bpy.data.actions['CurlProbe'];scene.frame_set(0)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'unified-rig-prototype.blend'))
(OUT/'build-summary.json').write_text(json.dumps({'sourceMeshes':len(meshes),'boneCount':len(arm.bones),'clips':['CurlProbe','PulldownProbe'],'allSourceBasePreserved':True,'limitations':['All attachment masks are uncalibrated geometric proxies','No finger deformation or invented skin surface','Probe motion is isolated kinematic demonstration, not validated exercise','Linear skin stretch/collapse flags remain review evidence','No clinical or muscle-force claim']},indent=2))
print('RIG_V2_BUILD_COMPLETE',len(meshes),len(arm.bones))
