"""Guarded stdio MCP endpoint using the pinned upstream BlenderConnection transport."""
import asyncio,fcntl,json,os,socket
from pathlib import Path
from guard import load_policy,check
for key,value in {'BLENDER_MCP_SAFE_MODE':'1','DISABLE_TELEMETRY':'true','BLENDER_MCP_DISABLE_TELEMETRY':'1','BLENDERMCP_NO_UPDATE_CHECK':'1'}.items():
 if os.environ.get(key)!=value:raise RuntimeError('Required safety environment missing: '+key)
policy,token,scripts=load_policy();lock=open(Path(os.environ['BLENDER_MCP_LOCAL_POLICY']).parent/'client.lock','a');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
from mcp.server.fastmcp import FastMCP,Image
from blender_mcp import server as upstream
from blender_mcp.safe_mode import validate_code
for entry in scripts.values():validate_code(entry['code'])
class AuthSocket:
 def __init__(self,inner):self.inner=inner
 def sendall(self,data):
  command=json.loads(data);check(command,scripts);command['_local_auth']=token
  return self.inner.sendall(json.dumps(command).encode())
 def __getattr__(self,name):return getattr(self.inner,name)
original=upstream.BlenderConnection.connect
def connect(self):
 if self.host not in ('127.0.0.1','localhost') or self.port!=policy['port']:raise PermissionError('Loopback fixed port only')
 ok=original(self)
 if ok and not isinstance(self.sock,AuthSocket):self.sock=AuthSocket(self.sock)
 return ok
upstream.BlenderConnection.connect=connect
conn=upstream.BlenderConnection(host='127.0.0.1',port=policy['port'])
mcp=FastMCP('mcp-for-blender 2.2.0 / local reviewed-script policy',instructions='Interactive local observation only. Cloud/model-generation tools are absent. Use approved_scripts to fetch exact reviewed code; unregistered code is denied. No general Python sandbox is claimed. A single client lock prevents Cursor/Codex concurrent ownership.')
@mcp.tool()
def get_scene_info()->str:
 """Query actual Blender objects without generated Python."""
 return json.dumps(conn.send_command('get_scene_info'))
@mcp.tool()
def get_object_info(name:str)->str:
 """Read an actual Blender object by exact name."""
 return json.dumps(conn.send_command('get_object_info',{'name':name}))
@mcp.tool()
def approved_scripts()->str:
 """List exact reviewed scripts; these are the only accepted execute_blender_code inputs."""
 return json.dumps(list(scripts.values()))
@mcp.tool()
def execute_blender_code(code:str)->str:
 """Run an exact SHA-registered local script with upstream Safe Mode still enabled."""
 validate_code(code);check({'type':'execute_code','params':{'code':code}},scripts)
 return json.dumps(conn.send_command('execute_code',{'code':code}))
@mcp.tool()
def get_viewport_screenshot(max_size:int=800)->Image:
 """Capture the actual Blender viewport. No upload/telemetry or external service."""
 if not 64<=max_size<=1600:raise ValueError('Screenshot range64..1600')
 path=Path(policy['workspace'])/'viewport-current.png'
 conn.send_command('get_viewport_screenshot',{'max_size':max_size,'filepath':str(path),'format':'png'})
 return Image(data=path.read_bytes(),format='png')
if __name__=='__main__':mcp.run()
