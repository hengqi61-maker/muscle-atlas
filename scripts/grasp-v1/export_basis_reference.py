"""Actual Blender local-pose reference; source GLB read only, fresh evidence directory."""
import bpy,sys,json,hashlib,os
from pathlib import Path
from mathutils import Matrix,Euler
root=Path(__file__).resolve().parents[2]
out=Path(sys.argv[sys.argv.index('--')+1]).resolve();out.mkdir(parents=True,exist_ok=False)
asset=root/os.environ.get('GRASP_ASSET','artifacts/grasp-v1/grasp-controller.glb');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(asset)==os.environ.get('GRASP_ASSET_SHA','40e3dbcbbe3423381dd2885936dd3f1c7d4355bcc6b4f0c30eb9245537be1dff')
args=sys.argv[sys.argv.index('--')+1:];input_path=Path(args[1]).resolve() if len(args)>1 else root/'artifacts/grasp-v1/p3-basis/pose-input.json';cases=json.loads(input_path.read_text())
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(asset),bone_heuristic='BLENDER')
rig=next(o for o in bpy.data.objects if o.type=='ARMATURE');assert len(rig.pose.bones)==57
C=Matrix(((1,0,0,0),(0,0,1,0),(0,-1,0,0),(0,0,0,1)))
def matrix(m):return [m[row][col] for col in range(4) for row in range(4)]
rest={b.name:matrix(C@rig.matrix_world@b.matrix@C.inverted()) for b in rig.pose.bones}
rows=[]
for case in cases:
 for pb in rig.pose.bones:pb.matrix_basis=Matrix.Identity(4)
 for name,p in case['pose'].items():
  pb=rig.pose.bones[name];pb.rotation_mode='XYZ';pb.rotation_euler=Euler((p['x'],p['y'],p['z']),'XYZ')
 bpy.context.view_layer.update()
 rows.append({'name':case['name'],'matrices':{n:matrix(C@rig.matrix_world@rig.pose.bones[n].matrix@C.inverted()) for n in case['pose']}})
r={'assetSha256':sha(asset),'blender':bpy.app.version_string,'importBoneHeuristic':'BLENDER','coordinates':'World RH glTF Y-up; column-major','rest':rest,'cases':rows,'scope':'Actual Blender EulerXYZ basis, no source mutation, no grasp or anatomical approval'}
(out/'blender-reference.json').write_text(json.dumps(r,indent=2));(out/'executed.py').write_bytes(Path(__file__).read_bytes());print('BLENDER_POSE_REFERENCE',len(rows))
