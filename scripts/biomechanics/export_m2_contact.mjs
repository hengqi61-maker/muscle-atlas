/** Frozen M2 source triangles and exact 12-sided production grip geometry. */
import fs from 'node:fs';
import crypto from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {AnimationMixer, CylinderGeometry, LoopOnce, Matrix4, Quaternion, Vector3} from 'three';
const frozen='0914d4fad3fbe107ea90c08473b6d2a448345ba6';
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const read=p=>execFileSync('git',['show',`${frozen}:${p}`],{maxBuffer:100*1024*1024});
const bytes=read('public/models/anatomy-pulldown.glb');
const configBytes=read('src/data/pulldown-config.json');
const config=JSON.parse(configBytes);
const machine=read('src/three/LatPulldownMachine.tsx');
// Guard against silent divergence from the frozen runtime representation.
if(!machine.includes('cylinderGeometry args={[r,r,length,12]}') ||
   !machine.includes('from={[side*.32,-.01575,0]} to={[side*.46,-.126,0]} r={.024}'))
 throw Error('Frozen runtime geometry requires adapter review');
const gltf=await new GLTFLoader().parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),'');
const originalBytes=read('public/models/anatomy.glb');
const original=await new GLTFLoader().parseAsync(originalBytes.buffer.slice(originalBytes.byteOffset,originalBytes.byteOffset+originalBytes.byteLength),'');
const originals=new Map();original.scene.traverse(m=>{if(m.isMesh)originals.set(m.userData.name||m.name,m);});
const sources=[];gltf.scene.traverse(m=>{if(m.isMesh&&/adductor pollicis/.test(m.userData.sourceName??''))sources.push(m);});
if(sources.length<2)throw Error(`Expected bilateral actual adductor sources, got ${sources.length}`);
for(const mesh of sources){const raw=originals.get(mesh.userData.sourceName);if(!raw||raw.geometry.attributes.position.count!==mesh.geometry.attributes.position.count||JSON.stringify(Array.from(raw.geometry.index.array))!==JSON.stringify(Array.from(mesh.geometry.index.array)))throw Error('Original topology mismatch');}
const mixer=new AnimationMixer(gltf.scene);const action=mixer.clipAction(gltf.animations[0]);action.setLoop(LoopOnce,1);action.clampWhenFinished=true;action.play();
const packet={schemaVersion:'1.0.0',coordinates:'right-handed-metres-seconds-column-major-active',
 variant:'frozen-M2-wide-pronated',provenance:`commit=${frozen}; GLB=${sha(bytes)}; originalGLB=${sha(originalBytes)}; config=${sha(configBytes)}; coordinates in shared equipment/anatomy model-root metres before common presentation scale 1.45 and translation [0,-1.45,0]; wrist/palm frames UNKNOWN, unused by detector; side assigned by posed centroid X, not anatomical calibration`,toleranceM:1e-8,samples:[]};
for(let k=0;k<=120;k++){
 const time=k*4/120;mixer.setTime(time);gltf.scene.updateMatrixWorld(true);
 for(const mesh of sources)if(mesh.isSkinnedMesh)mesh.skeleton.update();
 const barY=config.barTopY-config.barTravel*(1-Math.cos(time/4*2*Math.PI))/2;
 // One sample per side; strictly increasing separate packets preserve same real time.
 for(const side of [-1,1]){
  const a=new Vector3(side*.32,barY-.01575,config.gripZ),b=new Vector3(side*.46,barY-.126,config.gripZ);
  const delta=b.clone().sub(a),length=delta.length();
  const matrix=new Matrix4().compose(a.clone().add(b).multiplyScalar(.5),
   new Quaternion().setFromUnitVectors(new Vector3(0,1,0),delta.normalize()),new Vector3(1,1,1));
  const geo=new CylinderGeometry(.024,.024,length,12);
  const vertices=Array.from({length:geo.attributes.position.count},(_,i)=>new Vector3().fromBufferAttribute(geo.attributes.position,i).toArray());
  const triangles=Array.from({length:geo.index.count/3},(_,i)=>[0,1,2].map(j=>geo.index.getX(i*3+j)));
  const matching=sources.map(mesh=>{
   const posed=Array.from({length:mesh.geometry.attributes.position.count},(_,i)=>mesh.localToWorld(mesh.getVertexPosition(i,new Vector3())).toArray());
   return {mesh,posed,meanX:posed.reduce((sum,p)=>sum+p[0],0)/posed.length};
  }).filter(row=>Math.sign(row.meanX)===side);
  if(!matching.length)throw Error('Missing source side');
  const hands=[{side:side>0?'left':'right',skeletonId:`M2:${sha(bytes)}`,frameStatus:'unknown',wristWorldMatrix:null,palmWorldMatrix:null,
   sources:matching.map(({mesh,posed})=>({sourceId:mesh.userData.sourceName,originalMeshSha256:sha(Buffer.from(JSON.stringify({positions:Array.from(originals.get(mesh.userData.sourceName).geometry.attributes.position.array),indices:Array.from(mesh.geometry.index.array)}))),posedWorldVertices:posed,
    triangles:Array.from({length:mesh.geometry.index.count/3},(_,i)=>[0,1,2].map(j=>mesh.geometry.index.getX(i*3+j)))}))}];
  (packet[side>0?'leftSamples':'rightSamples']??=[]).push({timeSeconds:time,prop:{id:`M2-grip-${side}`,worldMatrix:matrix.toArray(),dimensionsM:[.048,length,.048],vertices,triangles},hands});
 }
}
const out=process.argv[2]??'artifacts/v2/m2';fs.mkdirSync(out,{recursive:true});
for(const side of ['left','right']){
 const {leftSamples,rightSamples,...base}=packet;
 fs.writeFileSync(`${out}/${side}.contact.json`,JSON.stringify({...base,samples:packet[`${side}Samples`]}));
}
console.log(JSON.stringify({frozen,glbSha256:sha(bytes),configSha256:sha(configBytes),sourceIds:sources.map(m=>m.userData.sourceName),samplesPerSide:121}));
