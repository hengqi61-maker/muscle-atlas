import fs from 'node:fs';import assert from 'node:assert/strict';
import validator from 'gltf-validator';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {AnimationMixer,Vector3,SkinnedMesh} from 'three';
const config=JSON.parse(fs.readFileSync('src/data/pulldown-config.json'));
const bytes=fs.readFileSync('public/models/anatomy-pulldown.glb');
const validation=await validator.validateBytes(new Uint8Array(bytes),{uri:'anatomy-pulldown.glb',maxIssues:200});fs.writeFileSync('docs/evidence/pulldown-validator.json',JSON.stringify(validation,null,2));assert.equal(validation.issues.numErrors,0);
const g=await new GLTFLoader().parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),'');
assert.equal(g.animations.length,1);assert.equal(g.animations[0].duration,4);
const mixer=new AnimationMixer(g.scene);mixer.clipAction(g.animations[0]).play();
const skinned=[];g.scene.traverse(o=>{if(o instanceof SkinnedMesh)skinned.push(o);});
const markerNames=['LeftPalmContact','RightPalmContact'];const markers=markerNames.map(n=>g.scene.getObjectByName(n));assert.ok(markers.every(m=>m instanceof SkinnedMesh));
const sourceMeshes=[];g.scene.traverse(o=>{if(o.userData.sourceName)sourceMeshes.push(o);});assert.equal(sourceMeshes.length,467);
const skeleton=skinned[0].skeleton;const lengths=new Map(skeleton.bones.map(b=>[b.name,b.scale.clone()]));
const lat=sourceMeshes.find(m=>m.userData.sourceName.includes('left latissimus'));
assert.ok(lat instanceof SkinnedMesh,'latissimus must be skinned');
const latRest=Array.from({length:lat.geometry.attributes.position.count},(_,i)=>lat.geometry.attributes.position.array.slice(i*3,i*3+3));
const latSamples=[];const shoulders=[];
const rows=[];let maxGripError=0,maxBoneLengthError=0,maxGripAxisError=0;
for(let frame=0;frame<=120;frame++){
 const time=frame/30,phase=(1-Math.cos(time/4*Math.PI*2))/2,barY=config.barTopY-config.barTravel*phase;
 mixer.setTime(time);g.scene.updateMatrixWorld(true);skinned.forEach(m=>m.skeleton.update());
 const contacts=markers.map((m,i)=>{
  // Mean the actual deformed marker vertices, removing sphere sampling bias.
  const v=new Vector3();for(let j=0;j<m.geometry.attributes.position.count;j++)v.add(m.localToWorld(m.getVertexPosition(j,new Vector3())));v.divideScalar(m.geometry.attributes.position.count);
  const target=new Vector3((i===0?1:-1)*config.gripHalfWidth,barY-config.gripDrop,config.gripZ);const error=v.distanceTo(target);maxGripError=Math.max(maxGripError,error);return {hand:markerNames[i],position:v.toArray(),target:target.toArray(),error};
 });
 for(const [index,name] of ['LeftHand','RightHand'].entries()){
  const i=skeleton.bones.findIndex(b=>b.name===name);const delta=skeleton.bones[i].matrixWorld.clone().multiply(skeleton.boneInverses[i]);
  const axis=new Vector3(1,0,0).transformDirection(delta);const angle=(index===0?1:-1)*Math.atan2(.126,.16);const expected=new Vector3(Math.cos(angle),-Math.sin(angle),0);
  maxGripAxisError=Math.max(maxGripAxisError,axis.angleTo(expected)*180/Math.PI);
 }
 for(const bone of skeleton.bones){const error=bone.scale.distanceTo(lengths.get(bone.name));maxBoneLengthError=Math.max(maxBoneLengthError,error);}
 if(frame===0||frame===60){
  latSamples.push(latRest.map((_,i)=>lat.localToWorld(lat.getVertexPosition(i,new Vector3())).clone()));
  shoulders.push(skeleton.bones.find(b=>b.name==='UpperArm').getWorldPosition(new Vector3()));
 }
 if(frame%30===0)rows.push({time,contacts});
}
assert.ok(maxGripError<.001,`grip error ${maxGripError} exceeds1mm`);assert.ok(maxBoneLengthError<.0001,`bone scale changed ${maxBoneLengthError}`);
assert.ok(maxGripAxisError<.02,`hand/rod axis error ${maxGripAxisError}deg`);
const shifts=latRest.map((p,i)=>({rest:p,displacement:latSamples[0][i].distanceTo(latSamples[1][i])}));
const insertion=shifts.filter(v=>Math.abs(v.rest[0])>.15&&v.rest[1]>1.0);
const origin=shifts.filter(v=>v.rest[1]<.90);
assert.ok(insertion.length>0&&origin.length>0,'attachment sample regions exist');
const mean=a=>a.reduce((s,v)=>s+v.displacement,0)/a.length;
const backMotion={insertionMeanMetres:mean(insertion),lowerOriginMeanMetres:mean(origin),shoulderExcursionMetres:shoulders[0].distanceTo(shoulders[1])};
assert.ok(backMotion.insertionMeanMetres>.015,'lat insertion must move');assert.ok(backMotion.lowerOriginMeanMetres<.003,'lumbar origin must remain stable');assert.ok(backMotion.shoulderExcursionMetres>.015,'shoulder girdle must move');
const report={backMotion,maxGripAxisErrorDegrees:maxGripAxisError,validator:{errors:validation.issues.numErrors,warnings:validation.issues.numWarnings},sourceMeshes:sourceMeshes.length,skinnedMeshes:skinned.length,bones:skeleton.bones.map(b=>b.name),maxGripErrorMetres:maxGripError,maxBoneScaleError:maxBoneLengthError,framesChecked:121,samples:rows,limitations:'shared anchor accuracy does not prove skin/tool collision clearance, physiological shoulder mechanics or all seated soft-tissue quality'};
fs.writeFileSync('docs/evidence/pulldown-runtime.json',JSON.stringify(report,null,2));console.log(JSON.stringify(report,null,2));
