"""Finalize already completed native runs with the required real browser stage.
This supports joining concurrent independent native workers with serial GPU browser consumers.
It never changes any source, geometry result or native output and fails closed.
"""
import os,json,subprocess,hashlib,argparse
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
p=argparse.ArgumentParser();p.add_argument('output',type=Path);a=p.parse_args();out=a.output.resolve();manifest=json.loads((out/'manifest.json').read_text());env=dict(os.environ,E3_BROWSER_ASSET=str(out/'motion.glb'),E3_BROWSER_OUT=str(out/'three-consumer'))
with (out/'browser.log').open('w') as log:subprocess.run(['node','--test','tests/rig-v2/pipeline-browser.node.mjs'],cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
manifest['softwareTests']['scope']='native structural assertions and actual Chrome Three.js consumer';manifest['outputs']['browser']='three-consumer';manifest['executionStages']=[{'name':'native-reconstruction','script':'scripts/rig-v2/pipeline/native_build.py','sha256':manifest['inputHashes']['scripts/rig-v2/pipeline/native_build.py'],'command':manifest['build']['command']},{'name':'native-video-encode','command':'ffmpeg -framerate 7.5 -i sequence/%03d.png -c:v libx264 -pix_fmt yuv420p motion.mp4'},{'name':'actual-three-consumer','script':'tests/rig-v2/pipeline-browser.node.mjs','sha256':hashlib.sha256((ROOT/'tests/rig-v2/pipeline-browser.node.mjs').read_bytes()).hexdigest(),'command':'E3_BROWSER_ASSET=<run>/motion.glb E3_BROWSER_OUT=<run>/three-consumer node --test tests/rig-v2/pipeline-browser.node.mjs'},{'name':'evidence-finalizer','script':'scripts/rig-v2/pipeline/finalize.py','sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}];manifest['orchestrationProvenance']='Both measured runs used native build then serial finalize/browser; integrated current build_motion.py browser stage added afterwards and not claimed as initially executed';manifest['files']=[]
for p in sorted(out.rglob('*')):
 if p.is_file() and p.name!='manifest.json':manifest['files'].append({'path':p.relative_to(out).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size})
(out/'manifest.json').write_text(json.dumps(manifest,indent=2))
