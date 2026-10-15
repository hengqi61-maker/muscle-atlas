"""Read-only triangle/base-geometry audit against the immutable pre-M2 rig export."""
import hashlib,json,pathlib,struct,subprocess
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parents[1]
def glb(payload):
 size=struct.unpack_from('<I',payload,12)[0]
 return json.loads(payload[20:20+size]),payload[28+size:]
def accessor(g,b,index):
 a=g['accessors'][index];v=g['bufferViews'][a['bufferView']]
 return np.frombuffer(b,dtype={5126:'<f4',5123:'<u2',5125:'<u4'}[a['componentType']],count=a['count']*{'VEC3':3,'SCALAR':1,'VEC4':4}[a['type']],offset=v.get('byteOffset',0)+a.get('byteOffset',0)).reshape(a['count'],-1)
def audit():
 baseline=subprocess.check_output(['git','show','9c9c971:public/models/anatomy-pulldown.glb'],cwd=ROOT)
 candidate=(ROOT/'public/models/anatomy-pulldown.glb').read_bytes();g,b=glb(baseline);h,c=glb(candidate);nodes={o['name']:o for o in h['nodes']};rows=[]
 for o in g['nodes']:
  if 'mesh' not in o or o['name'].endswith('PalmContact'):continue
  p=g['meshes'][o['mesh']]['primitives'][0];q=h['meshes'][nodes[o['name']]['mesh']]['primitives'][0]
  v=accessor(g,b,p['attributes']['POSITION'])[accessor(g,b,p['indices']).flatten()];w=accessor(h,c,q['attributes']['POSITION'])[accessor(h,c,q['indices']).flatten()]
  assert v.shape==w.shape,o['name']
  error=float(abs(v-w).max());assert error==0,o['name']
  assert o['extras']['sourceName']==nodes[o['name']]['extras']['sourceName']
  rows.append({'name':o['name'],'triangleCount':len(v)//3,'maxBaseTriangleCoordinateErrorM':error})
 assert len(rows)==467
 return {'baselineGit':'9c9c971','baselineGlbSha256':hashlib.sha256(baseline).hexdigest(),'candidateGlbSha256':hashlib.sha256(candidate).hexdigest(),'sourceMeshesCompared':len(rows),'scope':'index-expanded base triangle positions, triangle order/count and sourceName; export vertex splitting permitted; no claim about posed anatomical fidelity','meshes':rows}
if __name__=='__main__':print(json.dumps(audit(),indent=2))
