"""Run with Windows dependencies; RIG_CONTRACT_ROOT selects its untouched checkout."""
import importlib.util, json, os, unittest
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('mac_exchange',ROOT/'scripts/rig-v2/exchange-v1.py');adapter=importlib.util.module_from_spec(spec);spec.loader.exec_module(adapter)
k=adapter.load_contract(os.environ.get('RIG_CONTRACT_ROOT',ROOT))
class Exchange(unittest.TestCase):
 def test_actual_packets(self):
  files=list((ROOT/'docs/rig-v2/handoff/v1').glob('*.packet.json'));self.assertEqual(len(files),7)
  for p in files:
   packet=json.loads(p.read_text());self.assertEqual(k.validate(packet),[],p.name);self.assertEqual(len(packet['nodes']),27)
   if packet['samples']:self.assertEqual(len(packet['samples']),5)
 def test_noncommuting_units_and_frame_offsets(self):
  # Nonidentity A and B; 90-degree rotations deliberately do not commute.
  def rx():return np.array([[1,0,0,0],[0,0,-1,0],[0,1,0,0],[0,0,0,1]],float)
  def ry():return np.array([[0,0,1,0],[0,1,0,0],[-1,0,0,0],[0,0,0,1]],float)
  a,b=rx(),ry();s=rx()@ry();s[:3,3]=[100,200,300]
  self.assertFalse(np.allclose(a@b,b@a))
  t=k.map_transform(s,a,b,.001);np.testing.assert_allclose(k.unmap_transform(t,a,b,.001),s,atol=1e-10)
  np.testing.assert_allclose(k.convert_units(s,.001)[:3,3],[.1,.2,.3])
  np.testing.assert_allclose(k.reference_offset(s,t,a,.001),b,atol=1e-10)
 def test_real_roundtrips_and_source_preservation(self):
  report=json.loads((ROOT/'docs/rig-v2/handoff/v1/validation-report.json').read_text())
  self.assertLess(report['mathematicalRoundtripMaxError'],2e-5)
  self.assertLess(report['actualNativeToGltfPhaseMaxElementError'],2e-5)
  self.assertTrue(report['nativeWriteRead']['passed']);self.assertTrue(report['nativeWriteRead']['sourceShaUnchanged'])
  self.assertLess(report['nativeWriteRead']['maxMatrixElementError'],2e-5)
  imported=json.loads((ROOT/'docs/rig-v2/handoff/v1/native-gltf-import-report.json').read_text())
  self.assertTrue(imported['passed']);self.assertTrue(imported['sourceShaUnchanged']);self.assertLess(imported['maxMatrixElementError'],2e-5)
if __name__=='__main__':unittest.main()
