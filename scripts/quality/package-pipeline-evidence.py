"""Archive already-generated evidence without granting motion/owner approval."""
import argparse,hashlib,json,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def package(output,folders,extra,candidate):
 output=Path(output).resolve()
 if not output.is_relative_to(ROOT):raise ValueError('Archive output must remain project-local')
 if len(candidate)!=40 or any(c not in '0123456789abcdef' for c in candidate):raise ValueError('Full candidate commit required')
 if output.exists():raise ValueError('Refuse overwriting existing evidence archive')
 paths=set()
 for folder in folders:
  folder=Path(folder).resolve()
  if not folder.is_relative_to(ROOT) or output.is_relative_to(folder):raise ValueError('Folder must be project-local and cannot contain output')
  inventory=folder/'manifest.json'
  if inventory.exists():
   m=json.loads(inventory.read_text());entries=m.get('files',[])
   if isinstance(entries,list):
    for e in entries:
     p=(folder/e['path']).resolve()
     if not p.is_relative_to(folder) or not p.is_file() or sha(p)!=e['sha256']:raise ValueError('Changed/escaped evidence '+e['path'])
  for p in folder.rglob('*'):
   if p.is_file():
    if not p.resolve().is_relative_to(ROOT):raise ValueError('Evidence symlink escapes project')
    paths.add(p)
 for p in extra:
  p=Path(p).resolve()
  if not p.is_relative_to(ROOT) or not p.is_file():raise ValueError('Invalid extra evidence')
  paths.add(p)
 manifest={'codeCandidate':candidate,'ownerApproval':'PENDING','approvalMeaning':'Archive integrity only; never motion acceptance','packagerSha256':sha(Path(__file__)),'files':{p.relative_to(ROOT).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(paths)}}
 output.parent.mkdir(parents=True,exist_ok=True)
 with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED,compresslevel=4) as z:
  for p in sorted(paths):z.write(p,p.relative_to(ROOT).as_posix())
  z.writestr('PACKAGE-MANIFEST.json',json.dumps(manifest,indent=2))
 digest=sha(output);output.with_suffix(output.suffix+'.sha256').write_text(digest+'  '+output.name+'\n');return {'path':str(output.relative_to(ROOT)),'bytes':output.stat().st_size,'sha256':digest,'files':len(paths)}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',required=True,type=Path);p.add_argument('--folder',action='append',default=[],type=Path);p.add_argument('--extra',action='append',default=[],type=Path);p.add_argument('--candidate',required=True);a=p.parse_args();print(json.dumps(package(a.output,a.folder,a.extra,a.candidate)))
