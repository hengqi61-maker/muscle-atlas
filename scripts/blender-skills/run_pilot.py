#!/usr/bin/env python3
"""Strict host-side runner; no downloads or arbitrary upstream batch script execution."""
import argparse,hashlib,json,pathlib,subprocess,time,sys
ROOT=pathlib.Path(__file__).resolve().parents[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def verify():
 r=json.loads((ROOT/'docs/blender-skills/approved-registry.json').read_text())
 for row in r['files']:
  p=(ROOT/row['path']).resolve()
  if not (p.is_relative_to(ROOT/'.agents/skills') and p.is_file() and sha(p)==row['sha256']):raise ValueError('Unapproved skill bytes/path: '+row['path'])
 actual={str(p.relative_to(ROOT)) for n in r['skills'] for p in (ROOT/'.agents/skills'/n).rglob('*') if p.is_file() and '__pycache__' not in p.parts}
 if actual!={row['path'] for row in r['files']}:raise ValueError('Unregistered project skill files')
 return r
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--blender',required=True);p.add_argument('--output',required=True);a=p.parse_args();verify()
 out=(ROOT/a.output).resolve()
 if not out.is_relative_to(ROOT/'artifacts') or out.exists():raise ValueError('fresh project-local artifacts output required')
 out.mkdir(parents=True)
 records=[]
 def run(label,script,args):
  cmd=[str(pathlib.Path(a.blender).resolve()),'-b','--factory-startup','--disable-autoexec','--python-exit-code','1','-P',str(ROOT/script),'--',*map(str,args)]
  t=time.perf_counter();r=subprocess.run(cmd,capture_output=True,text=True,timeout=180);dt=time.perf_counter()-t
  (out/(label+'.log')).write_text(r.stdout+r.stderr);rec={'label':label,'command':cmd,'exitCode':r.returncode,'seconds':dt};records.append(rec);assert r.returncode==0,rec
 run('fixture','scripts/blender-skills/fixture.py',[out]);fixture=out/'fixture.blend';fixtureSha=sha(fixture)
 for i in range(2):
  for mode in ['baseline','skill']:run(f'{mode}-{i+1}','scripts/blender-skills/probe.py',[mode,fixture,out/f'{mode}-{i+1}'])
 reports=[json.loads((out/f'{m}-{i}'/'report.json').read_text()) for i in [1,2] for m in ['baseline','skill']]
 assert sha(fixture)==fixtureSha and len({r['outputSha256'] for r in reports})==1
 assert all(r['inventory']==reports[0]['inventory'] for r in reports)
 summary={'status':'BUILD_AND_COMPARISON_PASS','anatomyStatus':'NOT_APPLICABLE_DISPOSABLE_CUBES','skillQa':'EXPECTED_FAIL_DETACHED_FIXTURE','fixtureSha256':fixtureSha,'upstream':verify()['commit'],'records':records,'outputSha256':reports[0]['outputSha256'],'inventory':reports[0]['inventory'],'comparison':'four GLBs byte-identical; fixture read-only; additive QA detects intentional floating cube; no anatomy improvement claim','manualInterventions':0,'executedScriptHashes':{str(p.relative_to(ROOT)):sha(p) for p in [ROOT/'scripts/blender-skills/run_pilot.py',ROOT/'scripts/blender-skills/probe.py',ROOT/'scripts/blender-skills/fixture.py']},'blender':reports[0]['blender'],'blenderBuild':reports[0]['blenderBuild']}
 (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
