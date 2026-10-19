"""Baseline custom inventory versus pinned helper inventory + additive topology QA.
Both use identical exporter and input; this measures automation coverage, not prompts or anatomy.
"""
import bpy, pathlib, sys, json, hashlib, struct
args=sys.argv[sys.argv.index('--')+1:];mode,src,dst=args
root=pathlib.Path(__file__).resolve().parents[2];out=pathlib.Path(dst);out.mkdir(parents=True,exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def base():
 tris=0;mats=set();kinds={}
 for o in bpy.context.scene.objects:
  kinds[o.type]=kinds.get(o.type,0)+1
  if o.type=='MESH':
   dg=bpy.context.evaluated_depsgraph_get();eo=o.evaluated_get(dg);me=eo.to_mesh();me.calc_loop_triangles();tris+=len(me.loop_triangles);eo.to_mesh_clear();mats|={s.material.name for s in o.material_slots if s.material}
 return {'objects':kinds,'tris':tris,'materials':len(mats),'images':len(bpy.data.images),'missing_images':[],'actions':len(bpy.data.actions)}
bpy.ops.wm.open_mainfile(filepath=src,load_ui=False)
if mode=='baseline':inventory=base();qa={'status':'NOT_RUN_BASELINE_HAS_NO_FLOATING_CHECK'}
elif mode=='skill':
 for rel in ['blender-pipeline-automation/scripts','blender-asset-qa/scripts']:sys.path.insert(0,str(root/'.agents/skills'/rel))
 import batch_process,qa_check
 result=batch_process.run(inp=[src],op='report')
 assert result['ok'] and result['files']==1 and len(result['results'])==1,result
 inventory={k:v for k,v in result['results'][0].items() if k not in ('file','sec','ok')}
 qa=qa_check.run(objects=['PilotBase','PilotFloater'],profile='render',uv=False)
 assert qa['ok'] and len(qa['floating'])==1 and qa['floating'][0]['object']=='PilotFloater' and not qa['pass'],qa
else:raise ValueError(mode)
# Both exports deliberately identical; no upstream mutation/convert/export preset is adopted.
res=bpy.ops.export_scene.gltf(filepath=str(out/'motion.glb'),export_format='GLB',export_extras=True,export_animations=False)
assert res=={'FINISHED'}
raw=(out/'motion.glb').read_bytes();ln,typ=struct.unpack_from('<II',raw,12);g=json.loads(raw[20:20+ln]);binary=raw[28+ln:]
report={'mode':mode,'inputSha256':sha(pathlib.Path(src)),'blender':bpy.app.version_string,'blenderBuild':bpy.app.build_hash.decode(),'inventory':inventory,'qa':qa,'outputSha256':sha(out/'motion.glb'),'binarySha256':hashlib.sha256(binary).hexdigest(),'gltf':g,'manualInterventions':0,'geometryMutated':False}
(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print('@@JSON@@'+json.dumps({'ok':True,'mode':mode,'inventory':inventory,'qaPassed':qa.get('pass'),'floating':qa.get('floating')}))
