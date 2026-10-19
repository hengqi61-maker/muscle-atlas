"""Blender actual-GLB bounds calibration and native render evidence (no rig edits)."""
import bpy,json,sys,hashlib,time,math
from pathlib import Path
from mathutils import Vector
import numpy as np
args=sys.argv[sys.argv.index('--')+1:]
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(path):
 bpy.ops.wm.read_factory_settings(use_empty=False);bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False);bpy.ops.import_scene.gltf(filepath=str(path))
 rigs=[o for o in bpy.data.objects if o.type=='ARMATURE'];assert len(rigs)==1;rig=rigs[0]
 meshes=[o for o in bpy.data.objects if o.type=='MESH'];anatomy=[o for o in meshes if o.get('sourceName')]
 assert len(anatomy)==467 and len({o['sourceName'] for o in anatomy})==467
 tracks=list(rig.animation_data.nla_tracks);clips=[]
 for track in tracks:
  for strip in track.strips:
   if strip.action.name in ['CurlProbe','PulldownProbe']:clips.append((strip.action.name,track,strip))
 assert len(clips)==2
 return rig,meshes,anatomy,tracks,clips
def activate(rig,tracks,track):
 rig.animation_data.action=None
 for t in tracks:t.mute=t!=track
 track.mute=False

def at(strip,index):
 frame=float(strip.frame_start)+(float(strip.frame_end)-float(strip.frame_start))*index/120
 bpy.context.scene.frame_set(math.floor(frame),subframe=frame%1);bpy.context.view_layer.update()

def bounds(meshes,verify=False):
 deps=bpy.context.evaluated_depsgraph_get();points=[];checks=[]
 for obj in meshes:
  evaluated=obj.evaluated_get(deps);corners=[evaluated.matrix_world@Vector(c) for c in evaluated.bound_box];points.extend(corners)
  if verify:
   mesh=evaluated.to_mesh();coords=np.empty(len(mesh.vertices)*3,dtype=np.float32);mesh.vertices.foreach_get('co',coords);coords=coords.reshape((-1,3))
   lo=coords.min(axis=0);hi=coords.max(axis=0);box=np.array([list(c) for c in evaluated.bound_box]);error=float(max(np.max(abs(lo-box.min(axis=0))),np.max(abs(hi-box.max(axis=0)))))
   checks.append({'name':obj.name,'vertices':len(mesh.vertices),'bboxVertexMaxErrorMetres':error});evaluated.to_mesh_clear();assert error<1e-5,(obj.name,error)
 lo=[min(p[k] for p in points) for k in range(3)];hi=[max(p[k] for p in points) for k in range(3)]
 return lo,hi,checks

def cameras(lo,hi):
 center=(Vector(lo)+Vector(hi))/2;height=hi[2]-lo[2];directions={'front':Vector((0,-1,.08)),'back':Vector((0,1,.08)),'side':Vector((1,0,.08))};specs={};max_extent=0
 corners=[Vector((x,y,z)) for x in [lo[0],hi[0]] for y in [lo[1],hi[1]] for z in [lo[2],hi[2]]]
 for name,direction in directions.items():
  location=center+direction.normalized()*height*3;rotation=(center-location).to_track_quat('-Z','Y');inv=rotation.inverted()
  for c in corners:
   p=inv@(c-center);max_extent=max(max_extent,abs(p.x),abs(p.y))
  specs[name]={'target':list(center),'camera':list(location),'rotationQuaternion':list(rotation)}
 for spec in specs.values():spec['orthoScale']=2*max_extent*1.10
 return specs,height

if args[0]=='--calibrate':
 output=Path(args[1]).resolve();output.mkdir(parents=True,exist_ok=True);inputs=[Path(a).resolve() for a in args[2:]];start=time.monotonic();assets=[];baseTargets={}
 for assetindex,path in enumerate(inputs):
  rig,meshes,anatomy,tracks,clips=load(path);poses=[];checks=[]
  for name,track,strip in clips:
   activate(rig,tracks,track)
   if assetindex==0:baseTargets[name]={}
   for index in range(121):
    at(strip,index);lo,hi,validation=bounds(meshes,verify=index==0);checks.extend([{'clip':name,**v} for v in validation]);poses.append({'clip':name,'sample':index,'lo':lo,'hi':hi})
    if assetindex==0:baseTargets[name][str(index)]={view:list(rig.matrix_world@rig.pose.bones[bone].head) for view,bone in [('right-shoulder','RightHumerus'),('left-elbow','LeftForearm'),('right-elbow','RightForearm')]}
  assets.append({'sha256':sha(path),'source':str(path),'meshCount':len(meshes),'sourceIdentityCount':len(anatomy),'extras':[{'name':o.name,'vertices':len(o.data.vertices),'triangles':sum(len(p.vertices)-2 for p in o.data.polygons),'hideRender':o.hide_render} for o in meshes if not o.get('sourceName')],'bounds':poses,'bboxVerification':checks})
 lo=[min(p['lo'][k] for a in assets for p in a['bounds']) for k in range(3)];hi=[max(p['hi'][k] for a in assets for p in a['bounds']) for k in range(3)];specs,height=cameras(lo,hi);proof=[]
 for asset in assets:
  for pose in asset['bounds']:
   for name,spec in specs.items():
    from mathutils import Quaternion
    inv=Quaternion(spec['rotationQuaternion']).inverted();target=Vector(spec['target']);ratio=0
    for x in [pose['lo'][0],pose['hi'][0]]:
     for y in [pose['lo'][1],pose['hi'][1]]:
      for z in [pose['lo'][2],pose['hi'][2]]:
       q=inv@(Vector((x,y,z))-target);ratio=max(ratio,abs(q.x)/(spec['orthoScale']/2),abs(q.y)/(spec['orthoScale']/2))
    assert ratio<1;proof.append({'asset':asset['sha256'],'clip':pose['clip'],'sample':pose['sample'],'view':name,'maxNormalizedProjectedExtent':ratio})
 contract={'version':'phase2-camera-v1','blenderVersion':bpy.app.version_string,'scriptSha256':sha(__file__),'coordinates':'Blender Z-up metres','units':'metres','method':'All evaluated visible mesh bounding-box corners at both clips x121 x3 assets; first pose each clip/asset compared against every actual evaluated mesh vertex bbox','assets':assets,'union':{'lo':lo,'hi':hi},'fullBodyCameras':specs,'baselineLocalTargets':baseTargets,'height':height,'clippingProof':{'clippedSamples':0,'maxNormalizedExtent':max(p['maxNormalizedProjectedExtent'] for p in proof),'samples':proof},'wallSeconds':time.monotonic()-start}
 (output/'camera-contract.json').write_text(json.dumps(contract,indent=2));print('CALIBRATED',contract['wallSeconds'],flush=True);raise SystemExit(0)

source=Path(args[0]).resolve();out=Path(args[1]).resolve();contractpath=Path(args[2]).resolve();smoke=len(args)>3 and args[3]=='--smoke';out.mkdir(parents=True,exist_ok=True);contract=json.loads(contractpath.read_text());sourcehash=sha(source);assert sourcehash in [a['sha256'] for a in contract['assets']]
rig,meshes,anatomy,tracks,clips=load(source);scene=bpy.context.scene;scene.render.engine='BLENDER_EEVEE';original_samples=scene.eevee.taa_render_samples;scene.eevee.taa_render_samples=8;scene.render.resolution_x=512;scene.render.resolution_y=512;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
scene.world.use_nodes=True;scene.world.node_tree.nodes.get('Background').inputs[0].default_value=(.025,.03,.04,1)
mat=bpy.data.materials.new('Phase2_Clean_diagnostic');mat.use_nodes=True;mat.node_tree.nodes.clear();bs=mat.node_tree.nodes.new('ShaderNodeBsdfPrincipled');output=mat.node_tree.nodes.new('ShaderNodeOutputMaterial');mat.node_tree.links.new(bs.outputs['BSDF'],output.inputs['Surface']);bs.inputs['Base Color'].default_value=(.66,.72,.76,1);bs.inputs['Roughness'].default_value=.6
for mesh in meshes:mesh.data.materials.clear();mesh.data.materials.append(mat);assert not mesh.hide_render
bpy.ops.object.camera_add();cam=bpy.context.object;cam.data.type='ORTHO';scene.camera=cam
for loc,power,size in [((3,-4,5),1200,5),((-3,-2,3),900,4),((1,4,4),1100,4)]:
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.data.energy=power;o.data.shape='DISK';o.data.size=size;o.rotation_euler=(Vector((0,0,1))-o.location).to_track_quat('-Z','Y').to_euler()
def view(name,clip,index):
 from mathutils import Quaternion
 if name in contract['fullBodyCameras']:
  spec=contract['fullBodyCameras'][name];cam.location=spec['camera'];cam.rotation_euler=Quaternion(spec['rotationQuaternion']).to_euler();cam.data.ortho_scale=spec['orthoScale']
 else:
  target=Vector(contract['baselineLocalTargets'][clip][str(index)][name]);direction=Vector({'right-shoulder':(.4,-1,.1),'left-elbow':(-.35,-1,.1),'right-elbow':(.35,-1,.1)}[name]);cam.location=target+direction.normalized()*contract['height']*3;cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=contract['height']*(.28 if name=='right-shoulder' else .24)
 return {'camera':list(cam.location),'rotationEuler':list(cam.rotation_euler),'orthoScale':cam.data.ortho_scale}
results=[]
for name,track,strip in clips:
 if smoke and name!='PulldownProbe':continue
 activate(rig,tracks,track);d=out/name;d.mkdir(exist_ok=True);trajectory=[]
 if not smoke:
  for index in range(121):
   at(strip,index);trajectory.append({'sample':index,'frame':scene.frame_current+scene.frame_subframe,'bones':{b.name:[float(x) for row in (rig.matrix_world@b.matrix) for x in row] for b in rig.pose.bones}})
  maximum=max(abs(a-b) for t in trajectory[1:] for key in trajectory[0]['bones'] for a,b in zip(t['bones'][key],trajectory[0]['bones'][key]));assert maximum>1e-4
  (d/'trajectory.json').write_text(json.dumps({'matrixOrder':'row-major','coordinates':'Blender Z-up metres','samples':trajectory,'maxMatrixDeltaFromStart':maximum}))
 views=[]
 for index in ([0] if smoke else [0,30,60,90,120]):
  at(strip,index)
  for camera in (['front','back','side'] if smoke else ['front','back','side','right-shoulder','left-elbow','right-elbow']):
   settings=view(camera,name,index);scene.render.filepath=str(d/f'{camera}-{index:03d}.png');bpy.ops.render.render(write_still=True);views.append({'sample':index,'view':camera,**settings})
 if not smoke:
  seq=d/'sequence';seq.mkdir(exist_ok=True)
  for i in range(31):
   index=i*4;at(strip,index);view('front',name,index);scene.render.filepath=str(seq/f'{i:04d}.png');bpy.ops.render.render(write_still=True)
 results.append({'clip':name,'importFramesPerSecond':scene.render.fps,'durationSeconds':(float(strip.frame_end)-float(strip.frame_start))/scene.render.fps,'sampleCount':len(trajectory),'maxMatrixDeltaFromStart':None if smoke else maximum,'views':views})
bpy.ops.wm.save_as_mainfile(filepath=str(out/'scene.blend'))
(out/'native.json').write_text(json.dumps({'source':str(source),'sourceSha256':sourcehash,'cameraContractSha256':sha(contractpath),'scriptSha256':sha(__file__),'blenderVersion':bpy.app.version_string,'renderSamples':8,'factoryRenderSamples':original_samples,'meshCount':len(meshes),'sourceMeshCount':len(anatomy),'sourceIdentityCount':len(anatomy),'helperScope':'bpy.data mesh total includes importer custom_shape helper; source GLB contains exactly 467 mesh nodes, no props','nonAnatomyMeshes':[o.name for o in meshes if not o.get('sourceName')],'boneCount':len(rig.pose.bones),'material':'Same Clean diagnosis; all467 source meshes visible; importer helper collection visibility unchanged','clips':results,'status':'SMOKE_NOT_REVIEWED' if smoke else 'RENDERED_NOT_REVIEWED'},indent=2))
