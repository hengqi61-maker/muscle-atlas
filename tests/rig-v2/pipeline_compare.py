import unittest,importlib.util,copy
from pathlib import Path
spec=importlib.util.spec_from_file_location('comparison',Path(__file__).resolve().parents[2]/'scripts/rig-v2/pipeline/compare.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def fixture():return [{'frame':i,'timeSeconds':i/30,'bones':{str(j):{'worldMatrix':[float(k%5==0) for k in range(16)]} for j in range(27)}} for i in range(121)]
class CompareTests(unittest.TestCase):
 def test_exact(self):self.assertEqual(m.trajectory_error(fixture(),fixture()),0)
 def test_reject_shorter(self):
  with self.assertRaises(ValueError):m.trajectory_error(fixture(),fixture()[:-1])
 def test_reject_time_mismatch(self):
  x=fixture();x[30]['timeSeconds']+=.1
  with self.assertRaises(ValueError):m.trajectory_error(fixture(),x)
 def test_reject_bone_mismatch(self):
  x=fixture();x[20]['bones']['other']=x[20]['bones'].pop('0')
  with self.assertRaises(ValueError):m.trajectory_error(fixture(),x)
 def test_reject_short_matrix(self):
  x=fixture();x[20]['bones']['0']['worldMatrix'].pop()
  with self.assertRaises(ValueError):m.trajectory_error(fixture(),x)
 def test_reject_nan(self):
  x=fixture();x[20]['bones']['0']['worldMatrix'][3]=float('nan')
  with self.assertRaises(ValueError):m.trajectory_error(fixture(),x)
 def test_reject_inf(self):
  x=fixture();x[20]['bones']['0']['worldMatrix'][3]=float('inf')
  with self.assertRaises(ValueError):m.trajectory_error(fixture(),x)
if __name__=='__main__':unittest.main()
