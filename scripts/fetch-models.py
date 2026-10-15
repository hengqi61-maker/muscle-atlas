"""Verified public upstream importer. No credentials, no retries, atomic writes."""
import hashlib,json,pathlib,urllib.request
root=pathlib.Path(__file__).resolve().parents[1]
files={'anatomy.glb':'a112885444785a9dd93c5753b46ac790e6e036b3','mesh_mapping.json':'6e702859c44aa0a36eb3b44d988076c48675c493'}
for name,expected in files.items():
 data=urllib.request.urlopen('https://johanbellander.github.io/BodyExplorer/'+name,timeout=120).read()
 actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
 if actual!=expected: raise RuntimeError(f'Upstream version changed: {name}: {actual}')
 target=root/'public/models'/name
 temp=target.with_suffix(target.suffix+'.tmp');temp.write_bytes(data);temp.replace(target)
 if name=='mesh_mapping.json': (root/'src/data/mesh_mapping.json').write_bytes(data)
 print(name,len(data),actual)
