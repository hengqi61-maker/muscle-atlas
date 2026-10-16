"""Independent original GLB import versus stored canonical base vertices/topology."""
import bpy,pathlib,json,hashlib,numpy as np
ROOT=pathlib.Path(__file__).resolve().parents[2];OUT=ROOT/'artifacts/rig-v2'
bpy.ops.wm.open_mainfile(filepath=str(OUT/'unified-rig-prototype.blend'))
base={o['sourceName']:{'coordinates':np.array([v.co[:] for v in o.data.vertices]),'polygons':[tuple(p.vertices) for p in o.data.polygons],'ids':{k:o.get(k) for k in ['fmaId','bpId','source']}} for o in bpy.context.scene.objects if o.type=='MESH'}
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(ROOT/'public/models/anatomy.glb'))
rows=[]
for o in bpy.context.scene.objects:
 if o.type!='MESH':continue
 b=base[o.name];raw=np.array([v.co[:] for v in o.data.vertices]);expected=raw[:,[0,2,1]]/1000;expected[:,2]*=-1
 delta=np.linalg.norm(expected-b['coordinates'],axis=1);topology=b['polygons']==[tuple(p.vertices) for p in o.data.polygons]
 rows.append({'name':o.name,'vertices':len(raw),'maximumCanonicalDeviationM':float(delta.max()),'polygonVertexOrderUnchanged':topology,'baseGeometryPreservedWithinFloat32Roundoff':bool(delta.max()<1e-7 and topology),'sourceIds':b['ids']})
assert len(rows)==467 and all(r['baseGeometryPreservedWithinFloat32Roundoff'] for r in rows)
(OUT/'independent-source-preservation.json').write_text(json.dumps({'method':'fresh original GLB import compared against saved native base mesh; full vertices and polygon indices; no evaluated deformation','sourceSha256':hashlib.sha256((ROOT/'public/models/anatomy.glb').read_bytes()).hexdigest(),'all467Passed':True,'maximumToleranceM':1e-7,'meshes':rows},indent=2))
print('INDEPENDENT_SOURCE_467_PASS')
