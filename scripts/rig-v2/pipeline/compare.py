"""Compare independent builds using predeclared semantic tolerances, not file equality."""
import json,struct,hashlib,argparse
from pathlib import Path
def load(p):return json.loads(Path(p).read_text())
def glb(p):
 data=Path(p).read_bytes();n=struct.unpack_from('<I',data,12)[0];j=json.loads(data[20:20+n]);off=20+n;size=struct.unpack_from('<I',data,off)[0];return j,data[off+8:off+8+size]
def digest(data):return hashlib.sha256(data).hexdigest()
def assess(a,b):
 A=load(a/'manifest.json');B=load(b/'manifest.json');tol=A['predeclaredComparison']['matrixElementAbsolute'];assert A['inputHashes']==B['inputHashes'];src=load(a/'source-preservation.json')==load(b/'source-preservation.json');ja,ba=glb(a/'motion.glb');jb,bb=glb(b/'motion.glb')
 def structure(j):return {'nodes':[(n.get('name'),n.get('children'),n.get('skin'),n.get('mesh'),n.get('extras')) for n in j['nodes']],'skins':j['skins'],'animations':j['animations'],'meshes':j['meshes'],'accessors':j['accessors'],'bufferViews':j['bufferViews']}
 structural=structure(ja)==structure(jb);ta=load(a/'trajectory.json');tb=load(b/'trajectory.json');err=max(abs(x-y) for sa,sb in zip(ta,tb) for name in sa['bones'] for x,y in zip(sa['bones'][name]['worldMatrix'],sb['bones'][name]['worldMatrix']));weights=load(a/'native-summary.json')['weightsSha256']==load(b/'native-summary.json')['weightsSha256'];media=all(len(m['outputs']['keyframes'])==50 and (p/'motion.mp4').stat().st_size>0 for m,p in [(A,a),(B,b)]);passed=src and structural and weights and err<=tol and media
 return {'status':'BUILD_PASS' if passed else 'BUILD_FAIL','sourceGeometryAndFaceHashesExact':src,'glbStructureIdentitySkinInverseBindAnimationsExact':structural,'binaryBufferExact':ba==bb,'binaryBufferSha256':[digest(ba),digest(bb)],'baseWeightsRegistryExact':weights,'trajectory121SamplesMaxMatrixError':err,'predeclaredTolerance':tol,'bothRuns50KeyframesAndRealVideo':media,'geometryQuality':'FAIL or INCONCLUSIVE preserved independently; repeatability does not imply anatomy acceptance','byteHashEqualityRequired':False}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('a',type=Path);p.add_argument('b',type=Path);p.add_argument('--output',type=Path,required=True);x=p.parse_args();r=assess(x.a,x.b);x.output.parent.mkdir(parents=True,exist_ok=True);x.output.write_text(json.dumps(r,indent=2));print(json.dumps(r));raise SystemExit(0 if r['status']=='BUILD_PASS' else 1)
