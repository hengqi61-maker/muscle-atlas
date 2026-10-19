import importlib.util,tempfile,unittest,json,hashlib,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];spec=importlib.util.spec_from_file_location('p',ROOT/'scripts/quality/package-pipeline-evidence.py');p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
class Archive(unittest.TestCase):
 def test_actual_checksum_and_tamper_rejection(self):
  with tempfile.TemporaryDirectory(dir=ROOT/'artifacts') as name:
   folder=Path(name)/'run';folder.mkdir();f=folder/'evidence.txt';f.write_text('actual measured test payload')
   (folder/'manifest.json').write_text(json.dumps({'files':[{'path':f.name,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()}]}))
   out=Path(name)/'evidence.zip';r=p.package(out,[folder],[],'a'*40)
   with zipfile.ZipFile(out) as z:self.assertEqual(json.loads(z.read('PACKAGE-MANIFEST.json'))['ownerApproval'],'PENDING')
   f.write_text('tampered')
   with self.assertRaises(ValueError):p.package(Path(name)/'invalid.zip',[folder],[],'a'*40)
   self.assertFalse((Path(name)/'invalid.zip').exists())
if __name__=='__main__':unittest.main()
