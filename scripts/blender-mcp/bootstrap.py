"""Start only a new disposable GUI instance; never attach/restart an existing user scene."""
import bpy,addon_utils,os,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from guard import load_policy,check
policy,token,scripts=load_policy()
assert os.environ.get('BLENDERMCP_NO_UPDATE_CHECK')=='1'
module=addon_utils.enable('blender_mcp',default_set=True)
assert module is not None,'Addon enable failed'
prefs=bpy.context.preferences.addons['blender_mcp'].preferences
prefs.telemetry_consent=False;prefs.auto_start_server=False
original=module.BlenderMCPServer._execute_command_internal
def guarded(self,command):
 try:check(command,scripts,token)
 except PermissionError as e:return {'status':'error','message':str(e)}
 return original(self,command)
module.BlenderMCPServer._execute_command_internal=guarded
for name in bpy.context.scene.bl_rna.properties.keys():
 if name.startswith('blendermcp_use_'):setattr(bpy.context.scene,name,False)
bpy.context.scene.blendermcp_port=policy['port']
bpy.ops.wm.save_userpref() # dedicated BLENDER_USER_CONFIG, not the user's active preferences
server=module.BlenderMCPServer(host='127.0.0.1',port=policy['port']);bpy.types.blendermcp_server=server;server.start()
assert server.running
Path(policy['workspace'],'bootstrap-status.json').write_text(json.dumps({'blender':bpy.app.version_string,'addon':list(module.bl_info['version']),'host':server.host,'port':server.port,'telemetryConsent':prefs.telemetry_consent,'scriptCount':len(scripts),'guard':'token + both-end command/script SHA allowlist','sceneFile':bpy.data.filepath},indent=2))
