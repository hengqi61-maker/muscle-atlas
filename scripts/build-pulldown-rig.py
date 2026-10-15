"""Actual source mesh seated bilateral IK, baked against shared machine anchors.
Fixed bone lengths, no reach clamping or stretch fallback: unreachable geometry fails.
"""
import bpy,json,math,pathlib,sys,hashlib
from mathutils import Vector,Matrix,Quaternion
root=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'scripts'))
from grip_geometry import contact_marker
config=json.loads((root/'src/data/pulldown-config.json').read_text());T=Vector(config['bodyTranslation']);offset=Vector(config['palmOffsetBlender'])
source=root/'public/models/anatomy.glb';assert hashlib.sha256(source.read_bytes()).hexdigest()=='6e84529b60b64cc8f8d5cef665fda932e359e828b66d0c2dd44ec1bd9d0bd01f'
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False);bpy.ops.import_scene.gltf(filepath=str(source))
meshes=[o for o in bpy.context.scene.objects if o.type=='MESH'];mapping={r['name']:r for r in json.loads((root/'public/models/mesh_mapping.json').read_text())}
for o in meshes:
 o.parent=None;o.matrix_world.identity()
 for v in o.data.vertices:x,y,z=v.co;v.co=Vector((x,z,-y))/1000+T
 entry=mapping[o.name];o['sourceName']=o.name;o['sourceDataset']=entry['source'];o['fmaId']=entry['fmaId'];o['bpId']=entry['bpId']
 for p in o.data.polygons:p.use_smooth=True
 o.data.update()
armature=bpy.data.armatures.new('PulldownSkeleton');rig=bpy.data.objects.new('PulldownRig',armature);bpy.context.collection.objects.link(rig)
bpy.context.view_layer.objects.active=rig;rig.select_set(True);bpy.ops.object.mode_set(mode='EDIT')
def bone(name,head,tail,parent=None):
 b=armature.edit_bones.new(name);b.head=head;b.tail=tail
 if parent:b.parent=armature.edit_bones[parent]
 return b
bone('SpineRoot',Vector((0,-.1,.95))+T,Vector((0,-.1,1.35))+T)
bone('Thorax',Vector((0,-.1,.95))+T,Vector((0,-.1,1.40))+T,'SpineRoot')
landmarks={}
for side,label in [(1,'Left'),(-1,'Right')]:
 s=Vector((side*.173,-.067,1.305))+T;e=Vector((side*.213,-.060,1.034))+T;w=Vector((side*.231,-.105,.802))+T
 grip=w+offset
 u='UpperArm' if side==1 else 'RightUpperArm';f='Forearm' if side==1 else 'RightForearm';h=label+'Hand'
 scap=label+'Scapula';bone(scap,Vector((side*.055,-.015,1.22))+T,s,'Thorax')
 bone(u,s,e,scap);bone(f,e,w,u);bone(h,w,grip,f)
 hip=Vector((side*.10,-.10,.83))+T;knee=Vector((side*.11,-.08,.45))+T;ankle=Vector((side*.10,-.08,.09))+T;toe=Vector((side*.10,-.23,.04))+T
 bone(label+'Thigh',hip,knee,'SpineRoot');bone(label+'Shin',knee,ankle,label+'Thigh');bone(label+'Foot',ankle,toe,label+'Shin')
 landmarks[side]={'shoulder':s,'elbow':e,'wrist':w,'grip':grip,'hip':hip,'knee':knee,'ankle':ankle,'toe':toe,'names':(u,f,h)}
bpy.ops.object.mode_set(mode='OBJECT')
def smooth(t):t=max(0,min(1,t));return t*t*(3-2*t)
def skin(o,weights):
 groups={name:o.vertex_groups.new(name=name) for name in armature.bones.keys()}
 for v in o.data.vertices:
  values=weights(v.co);assert abs(sum(values.values())-1)<1e-6
  for name,weight in values.items():
   if weight>1e-6:groups[name].add([v.index],weight,'REPLACE')
 modifier=o.modifiers.new('SeatedAnatomySkin','ARMATURE');modifier.object=rig
arm_names=[];leg_names=[]
for o in meshes:
 side=1 if 'left' in o.name else -1 if 'right' in o.name else 0
 if not side:
  skin(o,lambda co:{'Thorax':smooth((co.z-T.z-.9)/.20),'SpineRoot':1-smooth((co.z-T.z-.9)/.20)})
  continue
 label='Left' if side==1 else 'Right';lm=landmarks[side];u,f,h=lm['names']
 pts=[v.co-T for v in o.data.vertices];minz=min(v.z for v in pts);maxz=max(v.z for v in pts);maxx=max(abs(v.x) for v in pts)
 upper=any(k in o.name for k in ['biceps brachii','triceps brachii','brachialis','deltoid'])
 distal=maxx>.175 and maxz<1.175 and minz>.60
 if upper or distal:
  o['rigRegion']=label.lower()+'-arm';arm_names.append(o.name)
  def weights(co,u=u,f=f,h=h,label=label):
   z=co.z-T.z;shoulder=smooth((1.335-z)/.12);fore=smooth((1.092-z)/.092);hand=smooth((.830-z)/.050)
   return {label+'Scapula':1-shoulder,u:shoulder*(1-fore),f:shoulder*fore*(1-hand),h:shoulder*fore*hand}
  skin(o,weights)
 elif maxz<1.0 and minz<.60:
  o['rigRegion']=label.lower()+'-leg';leg_names.append(o.name)
  def weights(co,label=label):
   z=co.z-T.z;thigh=smooth((.86-z)/.12);shin=smooth((.51-z)/.10);foot=smooth((.15-z)/.09)
   return {'SpineRoot':1-thigh,label+'Thigh':thigh*(1-shin),label+'Shin':thigh*shin*(1-foot),label+'Foot':thigh*shin*foot}
  skin(o,weights)
 else:
  # Qualitative attachment masks: medial origins stay on thorax/root;
  # lateral insertions follow humerus or shoulder girdle. No activation morph.
  def weights(co,name=o.name,label=label,u=u):
   v=co-T;chest=smooth((v.z-.9)/.20);lateral=smooth((abs(v.x)-.045)/.12)
   if 'latissimus' in name:
    attach=smooth((v.z-1.08)/.18)*smooth((abs(v.x)-.08)/.10)*.85;target=u
   elif 'teres major' in name:
    attach=smooth((abs(v.x)-.09)/.075);return {label+'Scapula':1-attach,u:attach}
   elif any(n in name for n in ['rhomboid','trapezius','levator scapulae','serratus anterior']):
    attach=lateral*.8;target=label+'Scapula'
   elif 'pectoralis major' in name:
    attach=smooth((abs(v.x)-.10)/.08)*smooth((v.z-1.15)/.12)*.65;target=u
   else:attach=0;target=label+'Scapula'
   return {'SpineRoot':(1-attach)*(1-chest),'Thorax':(1-attach)*chest,target:attach}
  skin(o,weights)
for side,label in [(1,'Left'),(-1,'Right')]:
 lm=landmarks[side];contact_marker(lm['grip'],rig,label+'Hand',label+'PalmContact')
# Transform a bone's rest axes to a desired head/direction, then key its local basis.
def pose_direction(name,head,tail):
 rest=armature.bones[name];delta=(rest.tail_local-rest.head_local).rotation_difference(tail-head)
 matrix=delta.to_matrix().to_4x4()@rest.matrix_local.to_quaternion().to_matrix().to_4x4();matrix.translation=head
 p=rig.pose.bones[name];p.rotation_mode='QUATERNION';p.matrix=matrix;bpy.context.view_layer.update()
def pose_hand(name,head,rotation):
 matrix=rotation.to_matrix().to_4x4()@armature.bones[name].matrix_local.to_quaternion().to_matrix().to_4x4();matrix.translation=head
 p=rig.pose.bones[name];p.rotation_mode='QUATERNION';p.matrix=matrix;bpy.context.view_layer.update()
def key(name,frame):
 p=rig.pose.bones[name]
 for field in ['location','rotation_quaternion','scale']:p.keyframe_insert(data_path=field,frame=frame)
def solve(s,w,u,f,pole):
 d=(w-s).length;assert abs(u-f)+.001<d<u+f-.001,('unreachable IK',d,u,f)
 axis=(w-s).normalized();a=(u*u-f*f+d*d)/(2*d);height=math.sqrt(u*u-a*a);p=(pole-axis*pole.dot(axis)).normalized();return s+axis*a+p*height
scene=bpy.context.scene;scene.render.fps=30;scene.frame_start=0;scene.frame_end=120
samples=[]
for frame in range(121):
 phase=(1-math.cos(2*math.pi*frame/120))/2;bar=config['barTopY']-config['barTravel']*phase
 chest_rotation=Quaternion((1,0,0),math.radians(-6))
 chest_head=armature.bones['Thorax'].head_local.copy()
 pose_hand('Thorax',chest_head,chest_rotation);key('Thorax',frame)
 for side,label in [(1,'Left'),(-1,'Right')]:
  lm=landmarks[side];u,f,h=lm['names'];grip=Vector((side*config['gripHalfWidth'],-config['gripZ'],bar-config['gripDrop']));hand_rotation=Quaternion((0,1,0),side*math.atan2(.126,.16));w=grip-hand_rotation@offset;scap=label+'Scapula'
  scap_rest=armature.bones[scap].head_local
  scap_head=chest_head+chest_rotation@(scap_rest-chest_head)+Vector((0,.004*phase,.010-.014*phase))
  scap_rotation=chest_rotation@Quaternion((0,1,0),-side*math.radians(15-12*phase))
  s=scap_head+scap_rotation@(lm['shoulder']-scap_rest)
  pose_hand(scap,scap_head,scap_rotation);key(scap,frame)
  e=solve(s,w,(lm['elbow']-lm['shoulder']).length,(lm['wrist']-lm['elbow']).length,Vector((side*.8,.15,-.8)))
  pose_direction(u,s,e);pose_direction(f,e,w);pose_hand(h,w,hand_rotation)
  for name in [u,f,h]:key(name,frame)
  hip=lm['hip'];thigh_length=(lm['knee']-hip).length;shin_length=(lm['ankle']-lm['knee']).length
  knee=hip+Vector((0,-1,-.10)).normalized()*thigh_length;ankle=knee+Vector((0,0,-shin_length));toe=ankle+(lm['toe']-lm['ankle'])
  for name,head,tail in [(label+'Thigh',hip,knee),(label+'Shin',knee,ankle),(label+'Foot',ankle,toe)]:pose_direction(name,head,tail);key(name,frame)
  if frame in [0,30,60,90,120]:samples.append({'frame':frame,'side':label,'targetGrip':list(grip),'wrist':list(w),'elbow':list(e),'ankle':list(ankle),'shoulderWristDistance':(w-s).length})
scene.frame_set(0);(root/'artifacts').mkdir(exist_ok=True);bpy.ops.wm.save_as_mainfile(filepath=str(root/'artifacts/pulldown-rig.blend'))
bpy.ops.export_scene.gltf(filepath=str(root/'public/models/anatomy-pulldown.glb'),export_format='GLB',export_animation_mode='SCENE',export_animations=True,export_frame_range=True,export_force_sampling=True,export_skins=True,export_morph=True,export_extras=True,export_yup=True,export_anim_scene_split_object=False)
(root/'docs/evidence/pulldown-build.json').write_text(json.dumps({'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'sourceMeshes':len(meshes),'armMeshes':arm_names,'legMeshes':leg_names,'samples':samples,'config':config,'scope':'Baked two-arm analytic IK, fixed bone lengths, moving shoulder girdle and attachment-aware back skinning; original source hands; illustrative uncalibrated shoulder angles, no force or activation simulation'},indent=2))
