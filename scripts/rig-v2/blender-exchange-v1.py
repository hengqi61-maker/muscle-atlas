"""Run in Blender via runpy; emits native rigid observations, never edits source."""
import bpy, hashlib, json, os
from pathlib import Path
ROOT=Path(os.environ.get('RIG_EXCHANGE_ROOT',Path(__file__).resolve().parents[2]))
SOURCE=Path(os.environ.get('RIG_EXCHANGE_BLEND',ROOT/'artifacts/rig-v2/unified-rig-prototype.blend'))
OUT=ROOT/'docs/rig-v2/handoff/v1'; OUT.mkdir(parents=True,exist_ok=True)
TOLERANCE=2e-5  # declared before observing float32 bpy matrices

def flat(m): return [float(m[r][c]) for c in range(4) for r in range(4)]
def delta(a,b): return max(abs(a[r][c]-b[r][c]) for r in range(4) for c in range(4))
def export():
 before=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
 bpy.ops.wm.open_mainfile(filepath=str(SOURCE)); rig=bpy.data.objects['MuscleAtlasV2Rig']; scene=bpy.context.scene
 def pose(rest=False):
  world={b.name:rig.matrix_world @ (b.matrix_local if rest else rig.pose.bones[b.name].matrix) for b in rig.data.bones}
  return [{'name':b.name,'parentBone':b.parent.name if b.parent else None,'worldMatrix':flat(world[b.name]),'localMatrix':flat(world[b.parent.name].inverted()@world[b.name] if b.parent else world[b.name])} for b in rig.data.bones]
 result={'sourceBlendSha256':before,'blenderVersion':bpy.app.version_string,'fps':scene.render.fps/scene.render.fps_base,'rest':pose(True),'clips':[],'tolerance':TOLERANCE,'actions':[(a.name,list(a.frame_range)) for a in bpy.data.actions]}
 for action in bpy.data.actions:
  if action.name not in ['CurlProbe','PulldownProbe']: continue
  rig.animation_data.action=action
  if action.slots: rig.animation_data.action_slot=action.slots[0]
  start,end=action.frame_range; frames=[]
  for i in range(5):
   frame=start+(end-start)*i/4; scene.frame_set(int(frame),subframe=frame-int(frame));bpy.context.view_layer.update()
   frames.append({'phase':i/4,'timeSeconds':(frame-start)/result['fps'],'bones':pose()})
  result['clips'].append({'name':action.name,'frames':frames})
 # Actual native import round trip: remove animation influence in isolated copy,
 # write one nontrivial observed clip frame into bpy pose matrices, save/reopen.
 desired=result['clips'][-1]['frames'][1]['bones'];rig.animation_data_clear()
 for p in rig.pose.bones:p.matrix_basis.identity()
 from mathutils import Matrix
 for entry in desired:
  vals=entry['worldMatrix'];world=Matrix([[vals[c*4+r] for c in range(4)] for r in range(4)])
  rig.pose.bones[entry['name']].matrix=rig.matrix_world.inverted()@world
  bpy.context.view_layer.update()
 scratch=ROOT/'artifacts/rig-v2/exchange-v1-roundtrip.blend';scratch.parent.mkdir(parents=True,exist_ok=True)
 bpy.ops.wm.save_as_mainfile(filepath=str(scratch));bpy.ops.wm.open_mainfile(filepath=str(scratch));rig=bpy.data.objects['MuscleAtlasV2Rig'];bpy.context.view_layer.update()
 observed={b['name']:b for b in pose()};error=max(abs(x-y) for entry in desired for x,y in zip(entry['worldMatrix'],observed[entry['name']]['worldMatrix']))
 result['nativeWriteRead']={'sourceFrame':'PulldownProbe 25%','isolatedNativePath':'artifacts/rig-v2/exchange-v1-roundtrip.blend','maxMatrixElementError':error,'tolerance':TOLERANCE,'passed':error<=TOLERANCE,'sourceShaUnchanged':hashlib.sha256(SOURCE.read_bytes()).hexdigest()==before}
 (OUT/'native-observations.json').write_text(json.dumps(result,indent=2));assert error<=TOLERANCE, result['nativeWriteRead']
 assert result['nativeWriteRead']['sourceShaUnchanged']
if __name__=='__main__': export()

def import_gltf_packet():
 """Read Windows v1 glTF packet, unmap actual A/B, write and reopen native pose."""
 from mathutils import Matrix
 def mat(values):return Matrix([[values[c*4+r] for c in range(4)] for r in range(4)])
 native=json.loads((OUT/'native-observations.json').read_text());before=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
 mapping=json.loads((OUT/'native-gltf-mapping.json').read_text());packet=json.loads((OUT/'gltf-PulldownProbe.packet.json').read_text());sample=packet['samples'][1]
 A=mat(mapping['worldAlignmentA']);offset={n['targetId']:mat(n['frameOffsetB']) for n in mapping['nodes']}
 target={name:A.inverted()@mat(t['worldMatrix'])@offset[name].inverted() for name,t in sample['transforms'].items()}
 bpy.ops.wm.open_mainfile(filepath=str(SOURCE));rig=bpy.data.objects['MuscleAtlasV2Rig'];rig.animation_data_clear()
 for p in rig.pose.bones:p.matrix_basis.identity()
 for bone in rig.data.bones:
  rig.pose.bones[bone.name].matrix=rig.matrix_world.inverted()@target[bone.name];bpy.context.view_layer.update()
 scratch=ROOT/'artifacts/rig-v2/exchange-v1-gltf-import.blend';bpy.ops.wm.save_as_mainfile(filepath=str(scratch));bpy.ops.wm.open_mainfile(filepath=str(scratch));rig=bpy.data.objects['MuscleAtlasV2Rig'];bpy.context.view_layer.update()
 error=max(delta(rig.matrix_world@rig.pose.bones[name].matrix,w) for name,w in target.items())
 report={'packet':'gltf-PulldownProbe.packet.json','phase':sample['phase'],'sampleTimeSeconds':sample['timeSeconds'],'method':'Actual inverse A/B mapping, bpy pose write, isolated save, reopen, evaluated read','maxMatrixElementError':error,'predeclaredTolerance':TOLERANCE,'passed':error<=TOLERANCE,'sourceShaUnchanged':before==hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'isolatedNativePath':'artifacts/rig-v2/exchange-v1-gltf-import.blend'}
 (OUT/'native-gltf-import-report.json').write_text(json.dumps(report,indent=2));assert report['passed'] and report['sourceShaUnchanged'],report
