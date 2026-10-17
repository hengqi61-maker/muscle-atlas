"""Actual validator failure injection; synthetic prerequisites are NOT motion evidence."""
import hashlib,json,struct,subprocess,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
class FailurePropagation(unittest.TestCase):
 def test_validator_failure_cannot_leave_pass_manifest(self):
  with tempfile.TemporaryDirectory(prefix='pipeline-invalid-') as name:
   out=Path(name); raw=json.dumps({'asset':{'version':'2.0'},'scenes':[{}],'scene':99}).encode();raw+=b' '*((-len(raw))%4);blob=struct.pack('<III',0x46546c67,2,20+len(raw))+struct.pack('<II',len(raw),0x4e4f534a)+raw;(out/'motion.glb').write_bytes(blob);sha=hashlib.sha256(blob).hexdigest()
   (out/'three-consumer').mkdir();(out/'three-consumer/report.json').write_text(json.dumps({'assetSha256':sha,'status':'SOFTWARE_TEST_PASS','screenshotsPerClip':50,'errors':[],'fixture':'SYNTHETIC only to reach real invalid-scene validator; not a browser result'}))
   (out/'geometry-authoritative.json').write_text(json.dumps({'assetSha256':sha,'meshCount':467,'thresholds':{'edgeRatioStrictlyGreater':2},'clips':[{'samples':[{}]*121}],'fixture':'SYNTHETIC validator precondition; not geometry evidence'}))
   (out/'manifest.json').write_text(json.dumps({'build':{'status':'BUILD_PASS','command':[]},'softwareTests':{'status':'SOFTWARE_TEST_PASS','scope':'provisional includes Khronos'},'outputs':{},'inputHashes':{}}))
   result=subprocess.run(['python3',str(ROOT/'scripts/rig-v2/pipeline/finalize.py'),str(out),'--join-browser','--join-geometry'],cwd=ROOT,capture_output=True,text=True)
   self.assertNotEqual(result.returncode,0,result.stdout+result.stderr)
   manifest=json.loads((out/'manifest.json').read_text());self.assertNotEqual(manifest['softwareTests']['status'],'SOFTWARE_TEST_PASS','Failed validator left misleading PASS manifest')
if __name__=='__main__':unittest.main()
