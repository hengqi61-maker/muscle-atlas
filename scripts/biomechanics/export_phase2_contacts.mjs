/** Read-only frozen original source geometry; never writes assets or finger poses. */
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import zlib from 'node:zlib';
import {execFileSync} from 'node:child_process';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {AnimationMixer,CylinderGeometry,LoopOnce,Matrix4,Quaternion,Vector3} from 'three';
const frozen='0914d4fad3fbe107ea90c08473b6d2a448345ba6';
const producer=execFileSync('git',['rev-parse','HEAD'],{encoding:'utf8'}).trim();
const read=p=>execFileSync('git',['show',`${frozen}:${p}`],{maxBuffer:100*1024*1024});
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const hashGeometry=(vertices,triangles)=>{
 const data=Buffer.alloc(vertices.length*24+triangles.length*12);let offset=0;
 for(const row of vertices)for(const x of row){data.writeDoubleLE(x,offset);offset+=8;}
 for(const row of triangles)for(const x of row){data.writeUInt32LE(x,offset);offset+=4;}
 return sha(data);
};
const parse=async b=>new GLTFLoader().parseAsync(b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength),'');
const originalBytes=read('public/models/anatomy.glb'),raw=await parse(originalBytes),originals=new Map();
raw.scene.traverse(m=>{if(m.isMesh)originals.set(m.userData.name||m.name,m);});
const positions=g=>Array.from({length:g.attributes.position.count},(_,i)=>new Vector3().fromBufferAttribute(g.attributes.position,i).toArray());
const triangles=g=>Array.from({length:(g.index?.count??g.attributes.position.count)/3},(_,i)=>[0,1,2].map(j=>g.index?g.index.getX(i*3+j):i*3+j));
const out=path.resolve(process.argv[2]??'artifacts/phase2/contact-frames');fs.mkdirSync(out,{recursive:true});
const configBytes=read('src/data/pulldown-config.json'),config=JSON.parse(configBytes);
const machine=read('src/three/LatPulldownMachine.tsx').toString();
if(!machine.includes('cylinderGeometry args={[r,r,length,12]}')||!machine.includes('from={[side*.32,-.01575,0]} to={[side*.46,-.126,0]} r={.024}'))throw Error('Review frozen machine adapter');
const manifest={sourceCommit:frozen,producerCommit:producer,exporterSha256:sha(fs.readFileSync(new URL(import.meta.url))),
 originalAssetSha256:sha(originalBytes),machineCodeSha256:sha(Buffer.from(machine)),configSha256:sha(configBytes),
 scope:'Original intrinsic hand, digit and thumb muscle/tendon meshes selected by source names; not complete skin/bone geometry. No finger edits. Model-root metres before shared scene presentation transforms.',
 handFrameEvidence:'Existing LeftHand/RightHand bone frames only where present; wrist/palm anatomical frames unknown. Curl has only UpperArm/Forearm bones, so hand frame unknown.',
 frames:[],assets:{},sourceRegistry:{},unknownSources:[]};
for(const exercise of ['pulldown','curl']){
 const file=`public/models/anatomy-${exercise}.glb`,bytes=read(file),gltf=await parse(bytes);manifest.assets[exercise]={path:file,sha256:sha(bytes)};
 const sources=[],equipment=[];gltf.scene.traverse(m=>{if(!m.isMesh)return;
  if(/hand|pollicis|digitorum|indicis|digiti minimi/.test(m.userData.sourceName??''))sources.push(m);
  if(m.userData.equipment==='original-detailed-hex-dumbbell')equipment.push(m);
 });
 const registry=new Map();for(const mesh of sources){
  const name=mesh.userData.sourceName,original=originals.get(name),indices=triangles(mesh.geometry);
  if(!original||original.geometry.attributes.position.count!==mesh.geometry.attributes.position.count||JSON.stringify(triangles(original.geometry))!==JSON.stringify(indices)){
   manifest.unknownSources.push({exercise,sourceId:name,reason:'Original indexed topology not proven identical; excluded from original-triangle claims',
    originalVertexCount:original?.geometry.attributes.position.count??null,posedVertexCount:mesh.geometry.attributes.position.count,
    originalIndexCount:original?.geometry.index?.count??null,posedIndexCount:mesh.geometry.index?.count??null});continue;
  }
  const side=/\bleft\b/.test(name)?'left':/\bright\b/.test(name)?'right':null;if(!side)throw Error('Unknown source laterality');
  const region=/pollicis/.test(name)?'thumb':/interossei|lumbricals|digitorum|indicis|digiti/.test(name)?'finger':'hand-other';
  registry.set(mesh,{side,indices,sourceId:name,region,originalMeshSha256:hashGeometry(positions(original.geometry),indices)});
  manifest.sourceRegistry[name]={side,region,vertices:mesh.geometry.attributes.position.count,triangles:indices.length,
   originalMeshSha256:registry.get(mesh).originalMeshSha256,hashSerialization:'float64-le-xyz-then-uint32-le-triples',originalTopologyVerified:true};
 }
 const mixer=new AnimationMixer(gltf.scene),action=mixer.clipAction(gltf.animations[0]);action.setLoop(LoopOnce,1);action.clampWhenFinished=true;action.play();
 for(let frame=0;frame<=120;frame++){
  const time=4*frame/120;mixer.setTime(time);gltf.scene.updateMatrixWorld(true);for(const m of sources)if(m.isSkinnedMesh)m.skeleton.update();
  const hands=['left','right'].map(side=>{
   const bone=gltf.scene.getObjectByName(side==='left'?'LeftHand':'RightHand');const handMatrix=bone?.isBone?bone.matrixWorld:null;
   return {side,skeletonId:`${exercise}:${sha(bytes)}`,frameStatus:'unknown',wristWorldMatrix:null,palmWorldMatrix:null,
    independentlyExported:true,handWorldMatrix:handMatrix?.toArray()??null,
    sources:sources.filter(m=>registry.get(m)?.side===side).map(m=>{
     const r=registry.get(m),world=Array.from({length:m.geometry.attributes.position.count},(_,i)=>m.localToWorld(m.getVertexPosition(i,new Vector3())).toArray());
     const result={sourceId:r.sourceId,originalMeshSha256:r.originalMeshSha256,posedWorldVertices:world,triangles:r.indices,
      originalTriangleIds:r.indices.map((_,i)=>i),geometryKind:'actual-source-triangles',region:r.region,posedGeometrySha256:hashGeometry(world,r.indices)};
     if(handMatrix){const inverse=handMatrix.clone().invert();result.posedHandVertices=world.map(p=>new Vector3(...p).applyMatrix4(inverse).toArray());}
     return result;
    })};
  });
  const props=[];
  if(exercise==='pulldown')for(const side of [-1,1]){
   const barY=config.barTopY-config.barTravel*(1-Math.cos(time/4*2*Math.PI))/2;
   const a=new Vector3(side*.32,barY-.01575,config.gripZ),b=new Vector3(side*.46,barY-.126,config.gripZ),delta=b.clone().sub(a),length=delta.length();
   const matrix=new Matrix4().compose(a.clone().add(b).multiplyScalar(.5),new Quaternion().setFromUnitVectors(new Vector3(0,1,0),delta.normalize()),new Vector3(1,1,1));
   const g=new CylinderGeometry(.024,.024,length,12),vertices=positions(g),indices=triangles(g);
   props.push({side:side>0?'left':'right',id:`actual-M2-grip-${side}`,worldMatrix:matrix.toArray(),dimensionsM:[.048,length,.048],
    vertices,triangles:indices,geometryKind:'actual-convex-mesh',geometrySha256:hashGeometry(vertices,indices)});
  }
  else{
   const vertices=[],indices=[],parts=[];for(const mesh of equipment){const start=vertices.length,first=indices.length;
    for(const p of positions(mesh.geometry))vertices.push(mesh.localToWorld(new Vector3(...p)).toArray());
    for(const face of triangles(mesh.geometry))indices.push(face.map(i=>i+start));parts.push({name:mesh.name,firstTriangle:first,count:indices.length-first});
   }
   if(!vertices.length)throw Error('Missing real dumbbell');
   const dimensionsM=[0,1,2].map(axis=>Math.max(...vertices.map(p=>p[axis]))-Math.min(...vertices.map(p=>p[axis])));
   props.push({side:'both',id:'actual-detailed-dumbbell',worldMatrix:new Matrix4().toArray(),dimensionsM,vertices,triangles:indices,
    geometryKind:'actual-triangle-surface',geometrySha256:hashGeometry(vertices,indices)});
   manifest.dumbbellParts=parts;
  }
  for(const {side,...prop} of props){
   const packet={schemaVersion:'1.1.0',coordinates:'right-handed-metres-seconds-column-major-active',variant:`frozen-${exercise}-original-fingers`,
    provenance:`Actual original source triangles at frozen ${frozen}; model-root coordinates, all presentation transforms excluded equally from hand and prop`,toleranceM:1e-8,
    inputProvenance:{producerCommit:producer,assetSha256:sha(bytes),originalAssetSha256:sha(originalBytes),coordinateFrame:'actual GLB model-root axes, metres; anatomical axes uncalibrated',hashSerialization:'float64-le-xyz-then-uint32-le-triples',evidenceKind:'actual-export'},
    timeline:{clipId:gltf.animations[0].name,durationSeconds:4,expectedTimesSeconds:[time],interpolation:'gltf-animation',scope:'discrete-samples-not-continuous-collision'},
    samples:[{timeSeconds:time,prop,hands:side==='both'?hands:hands.filter(h=>h.side===side)}]};
   const payload=Buffer.from(JSON.stringify(packet)+'\n'),compressed=zlib.gzipSync(payload,{level:6});
   const name=`${exercise}-${side}-${String(frame).padStart(3,'0')}.json.gz`;fs.writeFileSync(path.join(out,name),compressed);
   manifest.frames.push({file:name,exercise,side,frame,timeSeconds:time,inputSha256:sha(compressed),payloadSha256:sha(payload)});
  }
 }
}
const encoded=JSON.stringify(manifest,null,2)+'\n';fs.writeFileSync(path.join(out,'manifest.json'),encoded);console.log(JSON.stringify({frames:manifest.frames.length,sources:Object.keys(manifest.sourceRegistry).length,manifestSha256:sha(Buffer.from(encoded))}));
