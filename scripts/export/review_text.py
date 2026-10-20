"""Export a source-first UTF-8 review document, never binary assets or raw evidence dumps."""
import argparse,hashlib,subprocess
from pathlib import Path
root=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
files=[root/x for x in ['docs/CURRENT_STATE.md','docs/PRD.md','docs/architecture.md','package.json']]
files+=sorted(x for x in (root/'src').rglob('*') if x.suffix in {'.ts','.tsx','.mjs','.css','.html'} and x.is_file())
files+=sorted((root/'tests').glob('*.test.ts'))
files+=[root/x for x in ['docs/grasp-v1/continuation-report.md','docs/assets-and-licenses.md']]
parts=['Muscle Atlas source review\nBase commit: '+subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()+'\nWorking-tree modifications may be included. Historical binary evidence is linked, not embedded. No claim of anatomical approval.\n']
for f in files:
 if f.exists():
  data=f.read_text(encoding='utf-8');parts.append('\n\n===== FILE: '+f.relative_to(root).as_posix()+' =====\n'+data)
a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(''.join(parts),encoding='utf-8');print(str(a.output),a.output.stat().st_size,'bytes SHA256',hashlib.sha256(a.output.read_bytes()).hexdigest())
