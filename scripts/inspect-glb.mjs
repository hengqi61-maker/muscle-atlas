import fs from 'node:fs';import crypto from 'node:crypto';
const file=process.argv[2]||'public/models/anatomy.glb';const b=fs.readFileSync(file);
if(b.toString('utf8',0,4)!=='glTF'||b.readUInt32LE(8)!==b.length)throw Error('Invalid/incomplete GLB');
const j=JSON.parse(b.toString('utf8',20,20+b.readUInt32LE(12)));
const report={file,bytes:b.length,sha256:crypto.createHash('sha256').update(b).digest('hex'),meshes:j.meshes?.length||0,nodes:j.nodes?.length||0,skins:j.skins?.length||0,animations:j.animations?.length||0,extensions:j.extensionsUsed,names:j.nodes?.slice(0,8).map(n=>n.name)};
console.log(JSON.stringify(report,null,2));
fs.writeFileSync('docs/model-inspection.json',JSON.stringify(report,null,2));
