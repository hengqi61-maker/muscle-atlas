"""Reproducible manual two-bone experiment on the actual source anatomy.
No auto-weight fallback. Morph is an illustrative artistic correction, not measured physiology.
Run with Blender --background --python scripts/build-curl-rig.py.
"""
import bpy,math,json,pathlib,hashlib
from mathutils import Vector,Quaternion,Matrix
root=pathlib.Path(__file__).resolve().parents[1]
source=root/'public/models/anatomy.glb'
assert hashlib.sha256(source.read_bytes()).hexdigest()=='6e84529b60b64cc8f8d5cef665fda932e359e828b66d0c2dd44ec1bd9d0bd01f'
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.gltf(filepath=str(source))
meshes=[o for o in bpy.context.scene.objects if o.type=='MESH']
mapping={r['name']:r for r in json.loads((root/'public/models/mesh_mapping.json').read_text())}
# Imported raw atlas is sideways in Blender: canonical Z-up metres, front -Y.
for o in meshes:
 o.parent=None;o.matrix_world.identity()
 for v in o.data.vertices:
  x,y,z=v.co;v.co=Vector((x,z,-y))/1000
 o.data.update()
 r=mapping[o.name];o['sourceName']=o.name;o['sourceDataset']=r['source'];o['fmaId']=r['fmaId'];o['bpId']=r['bpId']
 for p in o.data.polygons:p.use_smooth=True
# Landmarks manually estimated from source muscle extents, not scanned joint centres.
shoulder=Vector((.173,-.067,1.305));elbow=Vector((.213,-.060,1.034));wrist=Vector((.231,-.105,.802))
arm_data=bpy.data.armatures.new('LeftCurlSkeleton');rig=bpy.data.objects.new('LeftCurlRig',arm_data);bpy.context.collection.objects.link(rig)
bpy.context.view_layer.objects.active=rig;rig.select_set(True)
bpy.ops.object.mode_set(mode='EDIT')
upper=arm_data.edit_bones.new('UpperArm');upper.head=shoulder;upper.tail=elbow
fore=arm_data.edit_bones.new('Forearm');fore.head=elbow;fore.tail=wrist;fore.parent=upper;fore.use_connect=True
bpy.ops.object.mode_set(mode='OBJECT')
rig['scope']='left arm only; manually estimated landmarks; illustrative skin and morph'
rig.show_in_front=True
arm=[];biceps=[]
for o in meshes:
 vs=[v.co for v in o.data.vertices];minz=min(v.z for v in vs);maxz=max(v.z for v in vs);maxx=max(v.x for v in vs)
 upper_muscle=any(k in o.name for k in ['biceps brachii','triceps brachii','brachialis'])
 distal='left' in o.name and maxx>.175 and maxz<1.175 and minz>.60
 if 'left' not in o.name or not(upper_muscle or distal):continue
 arm.append(o);o['rigRegion']='left-arm'
 u=o.vertex_groups.new(name='UpperArm');f=o.vertex_groups.new(name='Forearm')
 for v in o.data.vertices:
  # Shared transition plane provides continuous weights across mesh boundaries.
  t=max(0.,min(1.,(1.092-v.co.z)/.092));w=t*t*(3-2*t)
  if w<1:u.add([v.index],1-w,'REPLACE')
  if w>0:f.add([v.index],w,'REPLACE')
 modifier=o.modifiers.new('TwoBoneSkin','ARMATURE');modifier.object=rig;modifier.use_deform_preserve_volume=False
 o.parent=None
 if 'biceps brachii' in o.name:
  biceps.append(o);basis=o.shape_key_add(name='Basis');bulge=o.shape_key_add(name='BicepsBulge')
  zlo=minz;zhi=maxz
  # Local longitudinal bins locate cross-section centre without distorting endpoints.
  bins={}
  for v in o.data.vertices:
   idx=min(23,int((v.co.z-zlo)/(zhi-zlo)*24));bins.setdefault(idx,[]).append(v.co)
  centers={idx:sum(points,Vector())/len(points) for idx,points in bins.items()}
  for v in o.data.vertices:
   t=(v.co.z-zlo)/(zhi-zlo);env=math.sin(math.pi*t)**2
   idx=min(23,int(t*24));c=centers[idx]
   bulge.data[v.index].co.x+=.24*env*(v.co.x-c.x)
   bulge.data[v.index].co.y+=.24*env*(v.co.y-c.y)-.002*env
  bulge.slider_min=0;bulge.slider_max=1
# glTF uses linear blend skinning. Bake pose-space corrections toward a
# quaternion-interpolated bend to reduce the observed elbow pinching.
corrected=[]
for o in arm:
 weights=[]
 for v in o.data.vertices:
  t=max(0.,min(1.,(1.092-v.co.z)/.092));weights.append(t*t*(3-2*t))
 if not any(.001<w<.999 for w in weights):continue
 corrected.append(o)
 if not o.data.shape_keys:o.shape_key_add(name='Basis')
 for degrees in [45,90,120]:
  key=o.shape_key_add(name=f'ElbowCorrective{degrees}')
  q=Quaternion((1,0,0),-math.radians(degrees));r=q.to_matrix();identity=Matrix.Identity(3)
  for v,w in zip(o.data.vertices,weights):
   if w<=.001 or w>=.999:continue
   n=Quaternion((1-w+w*q.w,w*q.x,w*q.y,w*q.z));n.normalize()
   desired=elbow+n@(v.co-elbow)
   a=identity*(1-w)+r*w;b=(elbow-r@elbow)*w
   key.data[v.index].co=a.inverted()@(desired-b)

# Compact dumbbell, independent steel handle and rubber heads; hand is supplied anatomy.
def mat(name,color,metal=.0):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=.35;return m
steel=mat('HandleSteel',(.35,.42,.45),.85);rubber=mat('DumbbellRubber',(.035,.045,.055))
grip=Vector((.224,-.117,.754))
for name,offset,radius,depth,material in [('Dumbbell_Handle',0,.012,.15,steel),('Dumbbell_Inner',-.083,.055,.05,rubber),('Dumbbell_Outer',.083,.055,.05,rubber)]:
 bpy.ops.mesh.primitive_cylinder_add(vertices=32,radius=radius,depth=depth,location=grip+Vector((offset,0,0)),rotation=(0,math.pi/2,0))
 o=bpy.context.object;o.name=name;bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
 group=o.vertex_groups.new(name='Forearm');group.add(list(range(len(o.data.vertices))),1.,'REPLACE');o.parent=None
 modifier=o.modifiers.new('GripSkin','ARMATURE');modifier.object=rig;o.data.materials.append(material)
 for p in o.data.polygons:p.use_smooth=True
# Bake both channels; no Blender Drivers are required in the runtime.
scene=bpy.context.scene;scene.render.fps=30;scene.frame_start=0;scene.frame_end=120
bone=rig.pose.bones['Forearm'];bone.rotation_mode='QUATERNION';rest=arm_data.bones['Forearm'].matrix_local.to_quaternion()
for frame in range(0,121):
 t=frame/30;theta=math.radians(120)*(1-math.cos(t/4*2*math.pi))/2
 bone.rotation_quaternion=rest.inverted()@Quaternion((1,0,0),-theta)@rest
 bone.keyframe_insert(data_path='rotation_quaternion',frame=frame,group='Curl')
 degrees=math.degrees(theta)
 for o in corrected:
  for target in [45,90,120]:
   width=30 if (target==120 or (target==90 and degrees>90)) else 45
   key=o.data.shape_keys.key_blocks[f'ElbowCorrective{target}'];key.value=max(0.,1-abs(degrees-target)/width);key.keyframe_insert(data_path='value',frame=frame,group='ElbowCorrections')
 for o in biceps:
  key=o.data.shape_keys.key_blocks['BicepsBulge'];key.value=theta/math.radians(120);key.keyframe_insert(data_path='value',frame=frame,group='BicepsBulge')
scene.frame_set(0)
(root/'artifacts').mkdir(exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(root/'artifacts/curl-rig.blend'))
# Scene mode bakes bones and morph weights into the same glTF clip.
bpy.ops.export_scene.gltf(filepath=str(root/'public/models/anatomy-curl.glb'),export_format='GLB',export_animations=True,export_animation_mode='SCENE',export_frame_range=True,export_frame_step=1,export_force_sampling=True,export_skins=True,export_morph=True,export_morph_animation=True,export_extras=True,export_yup=True,export_anim_scene_split_object=False)
report={'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'sourceMeshes':len(meshes),'armMeshes':len(arm),'bicepsMeshes':[o.name for o in biceps],'riggedMeshes':[o.name for o in arm],'bones':['UpperArm','Forearm'],'landmarks':{'shoulder':list(shoulder),'elbow':list(elbow),'wrist':list(wrist)},'duration':4,'poseCorrectiveMeshes':len(corrected),'morph':'24% radial artistic envelope, taper to zero at endpoints; not physiological','scope':'left arm, original independent meshes; rest of body static'}
(root/'docs/evidence/curl-build.json').write_text(json.dumps(report,indent=2))
