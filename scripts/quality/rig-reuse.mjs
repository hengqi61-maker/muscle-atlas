import fs from 'node:fs/promises';
import crypto from 'node:crypto';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
export function parseGlb(bytes){
 if(bytes.readUInt32LE(0)!==0x46546c67||bytes.readUInt32LE(4)!==2)throw Error('Expected GLB v2');
 let offset=12,json,bin;
 while(offset<bytes.length){const n=bytes.readUInt32LE(offset),type=bytes.readUInt32LE(offset+4),data=bytes.subarray(offset+8,offset+8+n);if(type===0x4e4f534a)json=JSON.parse(data.toString());if(type===0x004e4942)bin=data;offset+=8+n;}
 if(!json||!bin)throw Error('Missing GLB chunks');return {json,bin};
}
export function inspectReuse({json:g,bin}){
 const errors=[];const check=(ok,s)=>{if(!ok)errors.push(s)};
 const digestAccessor=id=>{const a=g.accessors[id];if(!a)throw Error(`Missing accessor ${id}`);if(a.sparse)throw Error('Sparse accessor requires explicit implementation');const v=g.bufferViews[a.bufferView];if(v.buffer!==0)throw Error('External buffers unsupported');const components={SCALAR:1,VEC2:2,VEC3:3,VEC4:4,MAT4:16}[a.type],width={5120:1,5121:1,5122:2,5123:2,5125:4,5126:4}[a.componentType];if(!components||!width)throw Error('Unsupported accessor layout');const size=components*width,start=(v.byteOffset??0)+(a.byteOffset??0),stride=v.byteStride??size;const canonical=Buffer.alloc(a.count*size);for(let i=0;i<a.count;i++)bin.copy(canonical,i*size,start+i*stride,start+i*stride+size);return {sha256:hash(canonical),count:a.count,type:a.type,componentType:a.componentType,normalized:!!a.normalized};};
 const meshNodes=g.nodes.map((n,i)=>({...n,nodeIndex:i})).filter(n=>n.mesh!==undefined);
 check(meshNodes.length===467,'Expected 467 original mesh nodes');
 check(new Set(meshNodes.map(n=>n.extras?.sourceName)).size===467,'Expected 467 unique sourceName identities');
 check(g.skins?.length===1,'Expected exactly one shared skin');
 check(meshNodes.every(n=>n.skin===0),'All meshes must reference shared skin 0');
 const skin=g.skins?.[0];check(skin?.joints.length===27,'Expected 27 shared joints');
 const jointSet=new Set(skin?.joints??[]),parent=new Map();g.nodes.forEach((n,i)=>(n.children??[]).forEach(c=>parent.set(c,i)));
 const hierarchy=(skin?.joints??[]).map(i=>({node:i,name:g.nodes[i].name,parentNode:jointSet.has(parent.get(i))?parent.get(i):null}));
 const meshes=meshNodes.map(n=>({sourceName:n.extras?.sourceName,fmaId:n.extras?.fmaId,bpId:n.extras?.bpId,skin:n.skin,primitives:g.meshes[n.mesh].primitives.map(p=>({positions:digestAccessor(p.attributes.POSITION),joints:digestAccessor(p.attributes.JOINTS_0),weights:digestAccessor(p.attributes.WEIGHTS_0),indices:p.indices===undefined?null:digestAccessor(p.indices),morphTargetCount:p.targets?.length??0}))}));
 const clips=(g.animations??[]).map(a=>{const channels=a.channels.map(c=>({node:c.target.node,name:g.nodes[c.target.node]?.name,path:c.target.path}));check(channels.every(c=>jointSet.has(c.node)),`${a.name}: nonshared-joint animation target`);check(channels.every(c=>['translation','rotation','scale'].includes(c.path)),`${a.name}: unexpected morph or unsupported channel`);return {name:a.name,channelCount:channels.length,channels,sharedSkinIndex:0,basePositionsAndWeights:'same immutable GLB accessors; no per-clip binding asset',morphChannels:channels.filter(c=>c.path==='weights').length};});
 check(clips.length===2&&clips.some(c=>c.name==='CurlProbe')&&clips.some(c=>c.name==='PulldownProbe'),'Expected both diagnostic clips');
 const targetSets=clips.map(c=>JSON.stringify(c.channels.map(t=>`${t.node}:${t.path}`).sort()));check(new Set(targetSets).size===1,'Diagnostic channel target sets differ');
 return {status:errors.length?'AUTO FAIL':'AUTO PASS',scope:'Structural reuse only; no anatomy, contact, or motion geometry approval',errors,sharedSkinCount:g.skins?.length,jointCount:skin?.joints.length,hierarchy,inverseBind:digestAccessor(skin.inverseBindMatrices),meshCount:meshNodes.length,meshes,clips,morphCorrection:{targetCount:meshes.reduce((s,m)=>s+m.primitives.reduce((q,p)=>q+p.morphTargetCount,0),0),note:'No independent corrective shapes installed in frozen R1. Absence is not successful deformation.'}};
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 const model=process.argv[2]??'public/experimental/rig-v2/unified-rig-prototype.glb';const output=process.argv[3]??'docs/rig-v2/pipeline/reuse-report.json';const bytes=await fs.readFile(model);const report={model,modelSha256:hash(bytes),...inspectReuse(parseGlb(bytes))};await fs.mkdir(path.dirname(output),{recursive:true});await fs.writeFile(output,JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({status:report.status,meshCount:report.meshCount,jointCount:report.jointCount,clips:report.clips.map(c=>({name:c.name,channels:c.channelCount})),errors:report.errors}));if(report.errors.length)process.exitCode=1;
}
