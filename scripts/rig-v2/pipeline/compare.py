"""Compare independent builds using predeclared semantic tolerances, not file equality."""
import json,struct,hashlib,argparse,math
from pathlib import Path
def load(p):return json.loads(Path(p).read_text())
def glb(p):
 data=Path(p).read_bytes();n=struct.unpack_from('<I',data,12)[0];j=json.loads(data[20:20+n]);off=20+n;size=struct.unpack_from('<I',data,off)[0];return j,data[off+8:off+8+size]
def digest(data):return hashlib.sha256(data).hexdigest()
def trajectory_error(a,b):
 if len(a)!=121 or len(b)!=121:raise ValueError('Both trajectories must contain exactly121 samples')
 error=0
 expected=None
 for frame,(sa,sb) in enumerate(zip(a,b)):
  if sa['frame']!=frame or sb['frame']!=frame or sa['timeSeconds']!=sb['timeSeconds'] or abs(sa['timeSeconds']-frame/30)>1e-12:raise ValueError('Sample frame/time mismatch')
  if not math.isfinite(sa['timeSeconds']):raise ValueError('Nonfinite time')
  ka=set(sa['bones']);kb=set(sb['bones'])
  if len(ka)!=27 or ka!=kb or (expected is not None and ka!=expected):raise ValueError('Bone key mismatch')
  expected=ka
  for name in ka:
   x=sa['bones'][name]['worldMatrix'];y=sb['bones'][name]['worldMatrix']
   if len(x)!=16 or len(y)!=16 or not all(isinstance(v,(int,float)) and math.isfinite(v) for v in x+y):raise ValueError('Invalid matrix length or nonfinite element')
   error=max(error,max(abs(u-v) for u,v in zip(x,y)))
 return error

def assess(a,b):
 A=load(a/'manifest.json');B=load(b/'manifest.json');tol=A['predeclaredComparison']['matrixElementAbsolute'];assert A['inputHashes']==B['inputHashes'];src=load(a/'source-preservation.json')==load(b/'source-preservation.json');ja,ba=glb(a/'motion.glb');jb,bb=glb(b/'motion.glb')
 def structure(j):return {'nodes':[(n.get('name'),n.get('children'),n.get('skin'),n.get('mesh'),n.get('extras')) for n in j['nodes']],'skins':j['skins'],'animations':j['animations'],'meshes':j['meshes'],'accessors':j['accessors'],'bufferViews':j['bufferViews']}
 structural=structure(ja)==structure(jb);ta=load(a/'trajectory.json');tb=load(b/'trajectory.json');err=trajectory_error(ta,tb);weights=load(a/'native-summary.json')['weightsSha256']==load(b/'native-summary.json')['weightsSha256'];media=all(len(m['outputs']['keyframes'])==50 and all((p/f).is_file() and (p/f).read_bytes()[:8]==bytes([137,80,78,71,13,10,26,10]) for f in m['outputs']['keyframes']) and (p/'motion.mp4').stat().st_size>0 for m,p in [(A,a),(B,b)]);stageA=[(s['name'],s.get('sha256')) for s in A.get('executionStages',[])];stageB=[(s['name'],s.get('sha256')) for s in B.get('executionStages',[])];stages=bool(stageA) and stageA==stageB;passed=src and structural and ba==bb and weights and err<=tol and media and stages
 return {'status':'BUILD_PASS' if passed else 'BUILD_FAIL','executionStageHashesMatch':stages,'sourceGeometryAndFaceHashesExact':src,'glbStructureIdentitySkinInverseBindAnimationsExact':structural,'binaryBufferExact':ba==bb,'binaryBufferSha256':[digest(ba),digest(bb)],'baseWeightsRegistryExact':weights,'trajectory121SamplesMaxMatrixError':err,'predeclaredTolerance':tol,'bothRuns50KeyframesAndRealVideo':media,'geometryQuality':'FAIL or INCONCLUSIVE preserved independently; repeatability does not imply anatomy acceptance','byteHashEqualityRequired':True,'binaryRequirementReason':'Both current independent outputs are byte-identical; require exact buffer equality instead of accepting accessor descriptions without numeric content comparison'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('a',type=Path);p.add_argument('b',type=Path);p.add_argument('--output',type=Path,required=True);x=p.parse_args();r=assess(x.a,x.b);x.output.parent.mkdir(parents=True,exist_ok=True);x.output.write_text(json.dumps(r,indent=2));print(json.dumps(r));raise SystemExit(0 if r['status']=='BUILD_PASS' else 1)
