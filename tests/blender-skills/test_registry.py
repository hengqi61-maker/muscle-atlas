import importlib.util,pathlib,unittest,subprocess,hashlib,json
ROOT=pathlib.Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('pilot',ROOT/'scripts/blender-skills/run_pilot.py');pilot=importlib.util.module_from_spec(spec);spec.loader.exec_module(pilot)
class Registry(unittest.TestCase):
 def test_pinned_complete(self):
  r=pilot.verify();self.assertEqual(len(r['skills']),3);self.assertEqual(len(r['commit']),40)
  actual={str(p.relative_to(ROOT)) for n in r['skills'] for p in (ROOT/'.agents/skills'/n).rglob('*') if p.is_file() and '__pycache__' not in str(p)}
  self.assertEqual(actual,{f['path'] for f in r['files']})
 def test_protected_bytes_equal_frozen_phase1(self):
  names=subprocess.check_output(['git','ls-tree','-r','--name-only','1b06bf4'],cwd=ROOT,text=True).splitlines()
  protected=[n for n in names if n.startswith(('public/','config/rig-v2/','scripts/rig-v2/','docs/rig-v2/','docs/quality/'))]
  self.assertGreater(len(protected),20)
  for name in protected:
   before=subprocess.check_output(['git','show','1b06bf4:'+name],cwd=ROOT)
   self.assertEqual(hashlib.sha256(before).hexdigest(),hashlib.sha256((ROOT/name).read_bytes()).hexdigest(),name)
