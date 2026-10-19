"""Reproducible isolated motion builder; no production asset replacement."""
import argparse,json,hashlib,os,subprocess,time,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def build_motion(exercise_definition,canonical_rig,attachment_registry,output_directory):
 definition=Path(exercise_definition).resolve();d=json.loads(definition.read_text());out=Path(output_directory).resolve()
 if out.exists() and any(out.iterdir()):raise ValueError('Output must be a fresh empty directory')
 out.mkdir(parents=True,exist_ok=True)
 assert (ROOT/d['canonicalRig']).resolve()==Path(canonical_rig).resolve()
 assert (ROOT/d['attachmentRegistry']).resolve()==Path(attachment_registry).resolve()
 env=dict(os.environ,PIPELINE_ROOT=str(ROOT),PIPELINE_OUT=str(out),PIPELINE_DEFINITION=str(definition));binary=d['blenderExecutable'];cmd=[binary,'-b','--python-exit-code','1','--python',str(Path(__file__).with_name('native_build.py'))];started=time.time()
 with (out/'build.log').open('w') as log:subprocess.run(cmd,env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
 subprocess.run([d['ffmpegExecutable'],'-y','-framerate','7.5','-i',str(out/'sequence/%03d.png'),'-c:v','libx264','-pix_fmt','yuv420p',str(out/'motion.mp4')],stdout=(out/'encode.log').open('w'),stderr=subprocess.STDOUT,check=True)
 browser_env=dict(os.environ,E3_BROWSER_ASSET=str(out/'motion.glb'),E3_BROWSER_OUT=str(out/'three-consumer'))
 with (out/'browser.log').open('w') as log:subprocess.run(['node','--test','tests/rig-v2/pipeline-browser.node.mjs'],cwd=ROOT,env=browser_env,stdout=log,stderr=subprocess.STDOUT,check=True)
 subprocess.run(['node','scripts/rig-v2/pipeline/geometry.mjs',str(out)],cwd=ROOT,check=True)
 native=json.loads((out/'native-summary.json').read_text());geometry=json.loads((out/'geometry.json').read_text());failed=any(r['severeAlarm'] or r['maxEdgeRatio']>3 for s in geometry['samples'] for r in s['meshes']);assert native['meshCount']==467 and native['boneCount']==27 and native['sourceIdentityExact'];assert len(list(out.glob('*.png')))==50
 manifest={'schemaVersion':'1.0.0','producerScriptHashes':{p.name:sha(p) for p in Path(__file__).parent.glob('*.py')},'definitionSha256':sha(definition),'blenderVersion':native['blenderVersion'],'experiment':'E3 fresh reconstruction, not anatomy acceptance','build':{'status':'BUILD_PASS','seconds':time.time()-started,'command':cmd},'softwareTests':{'status':'IN_PROGRESS','scope':'native structural assertions, Khronos validator, real Chrome consumer; independent QA separate'},'motionGeometry':{'status':json.loads((out/'geometry-authoritative.json').read_text())['status'],'scope':'All derived GLB triangles and edges at121times; original >2 stretch threshold','fullAnatomicalPass':False},'reviews':{'biomechanics':'PENDING','visual':'PENDING','exerciseScience':'PENDING','softwareQa':'PENDING','ownerApproval':'PENDING'},'inputHashes':d['inputHashes'],'outputs':{'glb':'motion.glb','blend':'motion.blend','trajectory':'trajectory.json','video':'motion.mp4','keyframes':sorted(p.name for p in out.glob('*.png'))},'files':[],'predeclaredComparison':d['comparisonTolerance']}
 for p in sorted(out.rglob('*')):
  if p.is_file():manifest['files'].append({'path':p.relative_to(out).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size})
 (out/'manifest.json').write_text(json.dumps(manifest,indent=2))
 subprocess.run([sys.executable,str(Path(__file__).with_name('finalize.py')),str(out),'--join-browser','--join-geometry'],cwd=ROOT,check=True)
 return json.loads((out/'manifest.json').read_text())
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--definition',required=True);p.add_argument('--output',required=True);a=p.parse_args();d=json.loads(Path(a.definition).read_text());m=build_motion(a.definition,ROOT/d['canonicalRig'],ROOT/d['attachmentRegistry'],a.output);print(json.dumps({'build':m['build'],'motionGeometry':m['motionGeometry']}))
