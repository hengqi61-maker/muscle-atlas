"""One-time immutable R1 native action observation; never mutates the input."""
import bpy,json,hashlib,os
from pathlib import Path
root=Path(os.environ['PIPELINE_ROOT']);src=Path(os.environ['R1_BLEND'])
bpy.ops.wm.open_mainfile(filepath=str(src));rig=bpy.data.objects['MuscleAtlasV2Rig'];scene=bpy.context.scene
result={'sourceBlendSha256':hashlib.sha256(src.read_bytes()).hexdigest(),'sourceGitCommit':'fcb27068232ed1204786fd901bb8c58aa575a686','sourceGlbSha256':hashlib.sha256((root/'public/experimental/rig-v2/unified-rig-prototype.glb').read_bytes()).hexdigest(),'provenance':'Actual evaluated R1 native pose bone matrix_basis observations; authored diagnostic, not normative motion','clips':[]}
for name in ['CurlProbe','PulldownProbe']:
 action=bpy.data.actions[name];rig.animation_data.action=action
 if action.slots:rig.animation_data.action_slot=action.slots[0]
 for track in rig.animation_data.nla_tracks:track.mute=True
 frames=[]
 for f in range(121):
  scene.frame_set(f);bpy.context.view_layer.update()
  frames.append({'frame':f,'timeSeconds':f/30,'bones':{p.name:{'location':list(p.location),'quaternionWxyz':list(p.rotation_quaternion),'scale':list(p.scale)} for p in rig.pose.bones}})
 result['clips'].append({'name':name,'fps':30,'samples':frames})
(root/'config/rig-v2/motions/r1-observed-trajectories.json').write_text(json.dumps(result,separators=(',',':')))
