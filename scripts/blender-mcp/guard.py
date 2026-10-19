"""Local policy around upstream2.2: exact reviewed scripts, authenticated socket, no cloud tools.
Not an OS sandbox. A same-user process that can read/change policy/token files is trusted.
"""
import hashlib,hmac,json,os,stat
from pathlib import Path
COMMANDS=frozenset({'ping','get_addon_info','get_scene_info','get_object_info','get_viewport_screenshot','get_telemetry_consent','execute_code'})
def load_policy():
 p=Path(os.environ['BLENDER_MCP_LOCAL_POLICY']).resolve();r=json.loads(p.read_text());t=Path(r['tokenFile']).resolve()
 if stat.S_IMODE(t.stat().st_mode)&0o077:raise PermissionError('Token file must be owner-only')
 scripts={}
 for row in r['scripts']:
  f=Path(row['path']).resolve()
  if not f.is_relative_to(p.parent) or not f.is_file():raise PermissionError('Script outside private policy directory')
  code=f.read_text();digest=hashlib.sha256(code.encode()).hexdigest()
  if digest!=row['sha256']:raise PermissionError('Reviewed script changed')
  scripts[digest]={'id':row['id'],'code':code}
 return r,t.read_text().strip(),scripts
def check(command,scripts,token=None):
 if token is not None and not hmac.compare_digest(str(command.get('_local_auth','')),token):raise PermissionError('Local authentication required')
 if command.get('type') not in COMMANDS:raise PermissionError('Command outside local observation policy')
 if command['type']=='execute_code':
  code=command.get('params',{}).get('code','')
  if hashlib.sha256(code.encode()).hexdigest() not in scripts:raise PermissionError('Script not in reviewed SHA registry')
 return True
