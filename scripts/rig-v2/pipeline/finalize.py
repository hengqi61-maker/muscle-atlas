"""Finalize already completed native runs with the required real browser stage.
This supports joining concurrent independent native workers with serial GPU browser consumers.
It never changes any source, geometry result or native output and fails closed.
"""
import os,json,subprocess,hashlib,argparse
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
p=argparse.ArgumentParser();p.add_argument('output',type=Path);p.add_argument('--join-browser',action='store_true',help='Join actual completed independent consumer stage; validate its asset identity and PASS report');p.add_argument('--join-geometry',action='store_true',help='Join actual completed full geometry stage; preserve FAIL');a=p.parse_args();out=a.output.resolve();manifest=json.loads((out/'manifest.json').read_text());env=dict(os.environ,E3_BROWSER_ASSET=str(out/'motion.glb'),E3_BROWSER_OUT=str(out/'three-consumer'))
def atomic_write(value):
 temporary=out/'manifest.tmp'
 temporary.write_text(json.dumps(value,indent=2))
 os.replace(temporary,out/'manifest.json')
manifest['pipelineStatus']='IN_PROGRESS'
manifest.setdefault('softwareTests',{})['status']='IN_PROGRESS'
atomic_write(manifest)
try:
 if a.join_browser:
  report=json.loads((out/'three-consumer/report.json').read_text());assert report['assetSha256']==hashlib.sha256((out/'motion.glb').read_bytes()).hexdigest() and report['status']=='SOFTWARE_TEST_PASS' and report['screenshotsPerClip']==50 and report['errors']==[]
 else:
  with (out/'browser.log').open('w') as log:subprocess.run(['node','--test','tests/rig-v2/pipeline-browser.node.mjs'],cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
 if a.join_geometry:
  report=json.loads((out/'geometry-authoritative.json').read_text());assert report['assetSha256']==hashlib.sha256((out/'motion.glb').read_bytes()).hexdigest() and report['thresholds']['edgeRatioStrictlyGreater']==2 and report['meshCount']==467 and all(len(c['samples'])==121 for c in report['clips'])
 else:
  with (out/'geometry-authoritative.log').open('w') as log:subprocess.run(['node','scripts/rig-v2/pipeline/geometry.mjs',str(out)],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,check=True)
 subprocess.run(['node','scripts/rig-v2/pipeline/validate.mjs',str(out)],cwd=ROOT,check=True)
 geometry=json.loads((out/'geometry-authoritative.json').read_text());manifest['motionGeometry']={'status':geometry['status'],'scope':geometry['coverage'],'fullAnatomicalPass':False,'report':'geometry-authoritative.json'}
 manifest['softwareTests']['scope']='native structural assertions, actual Khronos validator(errors=0; warnings preserved), and actual Chrome Three.js consumer';manifest['outputs']['browser']='three-consumer';manifest['executionStages']=[{'name':'native-reconstruction','script':'scripts/rig-v2/pipeline/native_build.py','sha256':manifest['inputHashes']['scripts/rig-v2/pipeline/native_build.py'],'command':manifest['build']['command']},{'name':'native-video-encode','command':'ffmpeg -framerate 7.5 -i sequence/%03d.png -c:v libx264 -pix_fmt yuv420p motion.mp4'},{'name':'actual-three-consumer','script':'tests/rig-v2/pipeline-browser.node.mjs','sha256':hashlib.sha256((ROOT/'tests/rig-v2/pipeline-browser.node.mjs').read_bytes()).hexdigest(),'command':'E3_BROWSER_ASSET=<run>/motion.glb E3_BROWSER_OUT=<run>/three-consumer node --test tests/rig-v2/pipeline-browser.node.mjs'},{'name':'actual-derived-glb-full-geometry','script':'scripts/rig-v2/pipeline/geometry.mjs','sha256':hashlib.sha256((Path(__file__).parent/'geometry.mjs').read_bytes()).hexdigest(),'command':'node scripts/rig-v2/pipeline/geometry.mjs <run>'},{'name':'khronos-glb-validator','script':'scripts/rig-v2/pipeline/validate.mjs','sha256':hashlib.sha256((Path(__file__).parent/'validate.mjs').read_bytes()).hexdigest(),'command':'node scripts/rig-v2/pipeline/validate.mjs <run>'},{'name':'evidence-finalizer','script':'scripts/rig-v2/pipeline/finalize.py','sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}];manifest['orchestrationProvenance']=('Measured complete build_motion.py CLI execution: native reconstruction, encode, browser, geometry and finalize/validator' if 'producerScriptHashes' in manifest else 'Measured staged native build then serial finalize/browser; integrated driver is not claimed as initially executed for this run');manifest['files']=[]
 for p in sorted(out.rglob('*')):
  if p.is_file() and p.name!='manifest.json':manifest['files'].append({'path':p.relative_to(out).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size})
 manifest['softwareTests']['status']='SOFTWARE_TEST_PASS';manifest['pipelineStatus']='EVIDENCE_COMPLETE';atomic_write(manifest)
except Exception as error:
 manifest['pipelineStatus']='FAILED'
 manifest['softwareTests']['status']='SOFTWARE_TEST_FAIL'
 manifest['softwareTests']['failure']=str(error)
 atomic_write(manifest)
 raise
