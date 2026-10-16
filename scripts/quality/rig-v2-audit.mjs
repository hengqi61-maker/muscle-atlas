import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {AnimationMixer,LoopOnce,Vector3,Matrix4} from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
export const determinant = a => new Matrix4().fromArray(a).determinant();
export function triangleMetrics(a,b,c,restArea){const ab=b.clone().sub(a),ac=c.clone().sub(a);const area=ab.cross(ac).length()/2;return {area,ratio:restArea>0?area/restArea:null,collapsed:restArea>1e-14&&area/restArea<1e-4};}
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..');
export async function audit(){
 const modelPath='public/experimental/rig-v2/unified-rig-prototype.glb', bytes=await fs.readFile(path.join(root,modelPath));
 const raw=JSON.parse(bytes.subarray(20,20+bytes.readUInt32LE(12)));const canonical=JSON.parse(await fs.readFile(path.join(root,'config/rig-v2/canonical-rig.json')));
 const source=await fs.readFile(path.join(root,'public/models/anatomy.glb'));const sourceRaw=JSON.parse(source.subarray(20,20+source.readUInt32LE(12)));
 const mapping=JSON.parse(await fs.readFile(path.join(root,'public/models/mesh_mapping.json')));const byName=new Map(mapping.map(m=>[m.name,m]));
 const proofBytes=await fs.readFile(path.join(root,'artifacts/rig-v2/independent-source-preservation.json')),proof=JSON.parse(proofBytes);
 const errors=[];const check=(ok,msg)=>{if(!ok)errors.push(msg)};
 check(hash(source)===canonical.sourceSha256,'Original source hash mismatch');
 const proofNames=new Set(proof.meshes.map(m=>m.name));check(proofNames.size===467&&proof.meshes.every(m=>{const ref=byName.get(m.name);return ref&&['fmaId','bpId','source'].every(k=>String(ref[k]??'')===String(m.sourceIds?.[k]??''))}), 'Native proof source IDs mismatch');
 const sourceNames=new Set(sourceRaw.nodes.filter(n=>n.mesh!==undefined).map(n=>n.name));
 const meshNodes=raw.nodes.filter(n=>n.mesh!==undefined);check(meshNodes.length===467,'Expected 467 source meshes');
 check(new Set(meshNodes.map(n=>n.extras?.sourceName)).size===467,'Source names are not one-to-one');
 for(const n of meshNodes){const m=byName.get(n.extras?.sourceName);check(sourceNames.has(n.extras?.sourceName)&&m&&['fmaId','bpId','source'].every(k=>String(m[k]??'')===n.extras[k]),`Source correspondence mismatch: ${n.name}`)}
 check(proof.sourceSha256===hash(source)&&proof.meshes?.length===467&&proof.all467Passed&&proof.meshes.every(m=>m.maximumCanonicalDeviationM===0&&m.polygonVertexOrderUnchanged&&m.baseGeometryPreservedWithinFloat32Roundoff),'Linked full native base geometry proof failed');
 check(raw.skins.length===1&&new Set(meshNodes.map(n=>n.skin)).size===1,'Meshes do not share exactly one skin');
 const gltf=await new GLTFLoader().parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),'');gltf.scene.updateMatrixWorld(true);
 const bones=[],meshes=[];gltf.scene.traverse(n=>{if(n.isBone)bones.push(n);if(n.isSkinnedMesh)meshes.push(n)});
 check(bones.length===27,'Expected 27 bones');
 for(const c of canonical.bones){const b=bones.find(b=>b.name===c.name);check(b&&(b.parent?.isBone?b.parent.name:null)===c.parent,`Hierarchy mismatch ${c.name}`);if(b){check(b.matrixWorld.determinant()>0,`Non right handed rest ${b.name}`);if(/^(Left|Right)/.test(b.name))check(b.getWorldPosition(new Vector3()).x*(b.name.startsWith('Left')?1:-1)>=-1e-7,`Side mismatch ${b.name}`)}}
 let weights=0,badWeights=0;const prepared=[];
 for(const mesh of meshes){const g=mesh.geometry,p=g.attributes.position,w=g.attributes.skinWeight,j=g.attributes.skinIndex;for(let i=0;i<p.count;i++){let sum=0;for(let k=0;k<4;k++){const v=w.array[i*4+k];sum+=v;if(!Number.isFinite(v)||v<0||j.array[i*4+k]>=bones.length)badWeights++}if(Math.abs(sum-1)>1e-5)badWeights++;weights++}
 const count=g.index?g.index.count:p.count,priority=/deltoid|supraspinatus|infraspinatus|subscapularis|teres |pectoralis|latissimus|biceps brachii|triceps brachii|brachialis/.test(mesh.userData.sourceName??mesh.name),limit=priority?1024:128,triangles=[];
 for(let t=0;t<count/3;t+=Math.max(1,Math.ceil(count/3/limit))){const ids=[0,1,2].map(k=>g.index?g.index.getX(t*3+k):t*3+k),v=ids.map(i=>new Vector3().fromBufferAttribute(p,i));const area=triangleMetrics(...v,1).area;triangles.push({ids,area,edges:[v[0].distanceTo(v[1]),v[1].distanceTo(v[2]),v[2].distanceTo(v[0])]})}prepared.push({mesh,triangles,priority})}
 check(!badWeights,`${badWeights} invalid weights`);
 const restSegments=new Map(bones.map(b=>[b.name,b.position.length()]));
 const clips=[];
 for(const clip of gltf.animations){const mixer=new AnimationMixer(gltf.scene),action=mixer.clipAction(clip);action.setLoop(LoopOnce,1);action.clampWhenFinished=true;action.play();let previous=null;const frames=[];
 for(let frame=0;frame<=120;frame++){mixer.setTime(clip.duration*frame/120);gltf.scene.updateMatrixWorld(true);meshes.forEach(m=>m.skeleton.update());let severeAreaCount=0,severeAreaMeshAlarms=[],collapsed=0,nonfinite=0,minAreaRatio=Infinity,maxEdgeStretch=0,maxVertexStep=0;const positions=[];const worst=[];
 for(const {mesh,triangles} of prepared){const cache=new Map();const point=i=>{if(!cache.has(i)){const v=mesh.getVertexPosition(i,new Vector3()).applyMatrix4(mesh.matrixWorld);cache.set(i,v);positions.push(...v.toArray());if(!v.toArray().every(Number.isFinite))nonfinite++}return cache.get(i)};
 let localMin=Infinity,localMax=0,localSevere=0,eligible=0;for(const t of triangles){const v=t.ids.map(point),metrics=triangleMetrics(...v,t.area);if(metrics.collapsed)collapsed++;if(t.area>1e-14){eligible++;if(metrics.ratio<.05){localSevere++;severeAreaCount++}}if(metrics.ratio!==null){minAreaRatio=Math.min(minAreaRatio,metrics.ratio);localMin=Math.min(localMin,metrics.ratio)}for(let k=0;k<3;k++)if(t.edges[k]>1e-8){const r=v[k].distanceTo(v[(k+1)%3])/t.edges[k];maxEdgeStretch=Math.max(maxEdgeStretch,r);localMax=Math.max(localMax,r)}}if(localSevere>3||localSevere/eligible>.01)severeAreaMeshAlarms.push({name:mesh.userData.sourceName??mesh.name,sourceIds:{fmaId:mesh.userData.fmaId,bpId:mesh.userData.bpId},count:localSevere,eligible,fraction:localSevere/eligible});if(localMin<.05||localMax>2)worst.push({name:mesh.userData.sourceName??mesh.name,minAreaRatio:localMin,maxEdgeStretch:localMax})}
 if(previous)for(let i=0;i<positions.length;i+=3)maxVertexStep=Math.max(maxVertexStep,Math.hypot(positions[i]-previous[i],positions[i+1]-previous[i+1],positions[i+2]-previous[i+2]));previous=positions;
 const boneChecks=bones.map(b=>({name:b.name,determinant:b.matrixWorld.determinant(),localLength:b.position.length(),lengthDrift:Math.abs(b.position.length()-restSegments.get(b.name))}));check(boneChecks.every(b=>Number.isFinite(b.determinant)&&b.determinant>0),`${clip.name}/${frame} invalid bone transform`);
 const maxSegmentLengthDrift=Math.max(...boneChecks.map(b=>b.lengthDrift));check(maxSegmentLengthDrift<1e-6,`${clip.name}/${frame} segment length drift`);
 frames.push({frame,phase:frame/120,maxSegmentLengthDrift,severeAreaCount,severeAreaMeshAlarms,nonfinite,collapsed,minAreaRatio,maxEdgeStretch,maxVertexStep,continuityStatus:'Measured consecutive surface sample displacement; no unsupported biological speed limit',worst});
 }mixer.stopAllAction();mixer.uncacheRoot(gltf.scene);const violations=frames.filter(f=>f.nonfinite||f.collapsed||f.severeAreaMeshAlarms.length||f.maxEdgeStretch>2);clips.push({name:clip.name,status:violations.length?'AUTOFAIL':'NO_SAMPLED_NUMERIC_VIOLATION',frames,violatingFrames:violations.length})}
 check(gltf.animations.length===2&&['CurlProbe','PulldownProbe'].every(n=>gltf.animations.some(c=>c.name===n)), 'Expected two authoring probes');
 return {schema:'independent-actual-glb-audit-v1',status:errors.length||clips.some(c=>c.status==='AUTOFAIL')?'AUTOFAIL':'INCONCLUSIVE',modelPath,modelSha256:hash(bytes),sourceSha256:hash(source),fullBaseGeometryProof:{path:'artifacts/rig-v2/independent-source-preservation.json',sha256:hash(proofBytes),scope:'Independent native base-mesh exact comparison; linked evidence, not re-proven from exported skin'},meshCount:meshes.length,boneCount:bones.length,skinCount:raw.skins.length,weightsChecked:weights,badWeights,errors,method:{posesPerClip:121,trianglesPerMesh:'deterministic evenly spaced; 1024 priority shoulder/cuff/axilla/elbow meshes; 128 others',collapse:'numeric near-zero: area ratio < 0.0001; unchanged M2 severe engineering alarm: area ratio < 0.05 with >3 OR >1% eligible sampled triangles per mesh; not a medical threshold',stretch:'edge ratio > 2 (100% elongation), gross numerical deformation screen, not a biological threshold',limitations:'Finite surface samples cannot prove all triangles; interpenetration, anatomical attachments, strain tolerance and acceptable motion remain INCONCLUSIVE. Native clips are authored diagnostic poses, not approved exercise motions. No left/right biological symmetry assumption.'},clips};
}
if(process.argv[1]===fileURLToPath(import.meta.url)){const result=await audit();await fs.mkdir(path.join(root,'artifacts/rig-v2/independent-audit'),{recursive:true});await fs.writeFile(path.join(root,'artifacts/rig-v2/independent-audit/report.json'),JSON.stringify(result,null,2));console.log(JSON.stringify({status:result.status,errors:result.errors,clips:result.clips.map(c=>({name:c.name,status:c.status,violatingFrames:c.violatingFrames}))}));if(result.status==='AUTOFAIL')process.exitCode=1}
