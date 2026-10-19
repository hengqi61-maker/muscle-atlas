"""Supplement: actual source-rest vs evaluated LBS geometry, disposable scenes.
Usage blender -b --python-exit-code 1 --python THIS -- asset.glb output-dir
No source objects are removed or hidden after GLB import. Static copies only.
"""
import bpy,sys,json,hashlib,math
from pathlib import Path
from mathutils import Vector
args=sys.argv[sys.argv.index('--')+1:];asset=Path(args[0]).resolve();out=Path(args[1]).resolve();assert not out.exists();out.mkdir(parents=True)
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();reference=json.loads(Path(args[2]).read_text()) if len(args)>2 else None;bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(asset));sourceScene=bpy.context.scene;sourceScene.name='SOURCE_UNCHANGED';rig=next(o for o in sourceScene.objects if o.type=='ARMATURE');anatomy=[o for o in bpy.data.objects if o.type=='MESH' and o.get('sourceName')];assert len(anatomy)==467
baseline=[(o.name,o.hide_render,o.data.name,len(o.data.vertices),len(o.data.polygons)) for o in anatomy];records=[]
for sourceName,clip,index in [('right subscapularis','PulldownProbe',0),('left brachioradialis','CurlProbe',75)]:
 source=next(o for o in anatomy if o['sourceName']==sourceName);rig.animation_data.action=None;track=next(t for t in rig.animation_data.nla_tracks if any(s.action.name==clip for s in t.strips))
 for t in rig.animation_data.nla_tracks:t.mute=t!=track
 strip=next(s for s in track.strips if s.action.name==clip);frame=float(strip.frame_start)+(float(strip.frame_end)-float(strip.frame_start))*index/120;sourceScene.frame_set(math.floor(frame),subframe=frame%1);bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get();ev=source.evaluated_get(deps);posedmesh=ev.to_mesh();rest=[list(source.matrix_world@v.co) for v in source.data.vertices];posed=[list(ev.matrix_world@v.co) for v in posedmesh.vertices];faces=[list(p.vertices) for p in posedmesh.polygons];restfaces=[list(p.vertices) for p in source.data.polygons];assert len(rest)==len(posed) and faces==restfaces
 stem=sourceName.replace(' ','-')+'-'+clip+'-'+str(index);data={'assetSha256':sha(asset),'sourceName':sourceName,'bpId':source.get('bpId'),'fmaId':source.get('fmaId'),'clip':clip,'sampleIndexOf121':index,'blenderFrame':frame,'sourceTimeSeconds':frame/sourceScene.render.fps,'coordinateSystem':'Blender Z-up metres, source/evaluated world positions before comparison-only centering','restCoordinates':rest,'actualEvaluatedCoordinates':posed,'polygons':faces,'vertexIndexScope':'Blender imported source/evaluated meshes, correspondence checked equal counts/faces; NOT asserted upstream source or GLB exported vertex IDs','scope':'Static diagnostic copies, true source rest and actual evaluated LBS; not whole-body rendering, not medical validation; source objects/data unmodified'}
 (out/(stem+'.json')).write_text(json.dumps(data,separators=(',',':')));ev.to_mesh_clear()
 scene=bpy.data.scenes.new(stem);bpy.context.window.scene=scene;scene.render.engine='BLENDER_EEVEE';scene.eevee.taa_render_samples=8;scene.render.resolution_x=1024;scene.render.resolution_y=512;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.world=bpy.data.worlds.new(stem+' world');scene.world.use_nodes=True;scene.world.node_tree.nodes.new('ShaderNodeBackground') if not scene.world.node_tree.nodes.get('Background') else None
 background=scene.world.node_tree.nodes.get('Background');background.inputs[0].default_value=(.025,.03,.04,1)
 mat=bpy.data.materials.new(stem+' diagnostic');mat.use_nodes=True;mat.node_tree.nodes.clear();bs=mat.node_tree.nodes.new('ShaderNodeBsdfPrincipled');output=mat.node_tree.nodes.new('ShaderNodeOutputMaterial');mat.node_tree.links.new(bs.outputs['BSDF'],output.inputs['Surface']);bs.inputs['Base Color'].default_value=(.33,.48,.59,1);bs.inputs['Roughness'].default_value=.7
 # Camera looks along -Y. Keep source world orientation; center panels only.
 allpts=[Vector(p) for p in rest+posed];lo=Vector(tuple(min(p[k] for p in allpts) for k in range(3)));hi=Vector(tuple(max(p[k] for p in allpts) for k in range(3)));span=max(hi.x-lo.x,hi.z-lo.z,hi.y-lo.y);scale=span*1.55
 if reference:scale=next(r['orthographicScale']/2 for r in reference['records'] if r['sourceName']==sourceName)
 separation=scale*.9
 transforms=[]
 for side,coords in [('REST',rest),('ACTUAL LBS',posed)]:
  pts=[Vector(p) for p in coords];center=(Vector(tuple(min(p[k] for p in pts) for k in range(3)))+Vector(tuple(max(p[k] for p in pts) for k in range(3))))/2;offset=Vector(((-1 if side=='REST' else 1)*separation/2,0,0));mesh=bpy.data.meshes.new(stem+' '+side);mesh.from_pydata([tuple(Vector(p)-center+offset) for p in coords],[],faces);mesh.materials.append(mat);obj=bpy.data.objects.new(stem+' '+side,mesh);scene.collection.objects.link(obj);transforms.append({'side':side,'centeringTranslation':list(offset-center),'scaleApplied':1.0})
 cameraData=bpy.data.cameras.new(stem+' camera');cam=bpy.data.objects.new(stem+' camera',cameraData);scene.collection.objects.link(cam);cam.location=(0,-scale*4,scale*.03);cam.rotation_euler=(Vector((0,0,scale*.03))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=scale*2;scene.camera=cam
 for loc,power in [((scale,-scale*2,scale*2),scale*scale*100),((-scale,-scale,scale),scale*scale*50)]:
  light=bpy.data.lights.new('softbox','AREA');light.energy=power;light.shape='DISK';light.size=scale*2;ob=bpy.data.objects.new('softbox',light);scene.collection.objects.link(ob);ob.location=loc;ob.rotation_euler=(-ob.location).to_track_quat('-Z','Y').to_euler()
 def label(text,location,size):
  curve=bpy.data.curves.new('caption','FONT');curve.body=text;curve.size=size;curve.align_x='CENTER';o=bpy.data.objects.new('caption',curve);scene.collection.objects.link(o);o.location=location;o.rotation_euler=(math.pi/2,0,0)
 label(sourceName+' | '+str(source.get('bpId'))+' / '+str(source.get('fmaId')),(0,-scale*.7,scale*.46),scale*.045)
 label(clip+' sample '+str(index)+'/120 | source SHA '+sha(asset)[:16],(0,-scale*.7,scale*.38),scale*.036)
 for sign,text in [(-1,'SOURCE REST'),(1,'ACTUAL EVALUATED LBS')]:label(text,(sign*separation/2,-scale*.7,-scale*.36),scale*.04)
 label('ISOLATED DIAGNOSTIC COPIES | same scale | NOT whole-body or medical validation',(0,-scale*.7,-scale*.44),scale*.025)
 scene.render.filepath=str(out/(stem+'.png'));bpy.ops.render.render(write_still=True);records.append({'sourceName':sourceName,'bpId':source.get('bpId'),'fmaId':source.get('fmaId'),'clip':clip,'sample':index,'blenderFrame':frame,'image':stem+'.png','coordinates':stem+'.json','comparisonTransforms':transforms,'orthographicScale':cam.data.ortho_scale});bpy.context.window.scene=sourceScene
assert baseline==[(o.name,o.hide_render,o.data.name,len(o.data.vertices),len(o.data.polygons)) for o in anatomy]
bpy.ops.wm.save_as_mainfile(filepath=str(out/'isolated-diagnostics.blend'));(out/'manifest.json').write_text(json.dumps({'status':'SUPPLEMENTAL_RENDER_NOT_REVIEWED','assetSha256':sha(asset),'cameraReferenceManifestSha256':sha(Path(args[2])) if reference else None,'scriptSha256':sha(__file__),'sourceIdentityCount':467,'sourceObjectsNotDeletedOrHidden':True,'blenderVersion':bpy.app.version_string,'renderSamples':8,'resolution':[1024,512],'records':records,'files':[{'path':p.name,'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(out.iterdir()) if p.is_file()]},indent=2));(out/'render-isolated-executed.py').write_bytes(Path(__file__).read_bytes())
