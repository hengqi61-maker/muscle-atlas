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
const skeleton=skinned[0].skeleton;const lengths=new Map(skeleton.bones.map(b=>[b.name,b.position.length()]));
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
 for(const bone of skeleton.bones){const error=Math.abs(bone.position.length()-lengths.get(bone.name));maxBoneLengthError=Math.max(maxBoneLengthError,error);}
 if(frame%30===0)rows.push({time,contacts});
}
assert.ok(maxGripError<.001,`grip error ${maxGripError} exceeds1mm`);assert.ok(maxBoneLengthError<.0001,`bone length changed ${maxBoneLengthError}`);
assert.ok(maxGripAxisError<.02,`hand/rod axis error ${maxGripAxisError}deg`);
const report={maxGripAxisErrorDegrees:maxGripAxisError,validator:{errors:validation.issues.numErrors,warnings:validation.issues.numWarnings},sourceMeshes:sourceMeshes.length,skinnedMeshes:skinned.length,bones:skeleton.bones.map(b=>b.name),maxGripErrorMetres:maxGripError,maxBoneLengthErrorMetres:maxBoneLengthError,framesChecked:121,samples:rows,limitations:'shared anchor accuracy does not prove skin/tool collision clearance, physiological shoulder mechanics or all seated soft-tissue quality'};
fs.writeFileSync('docs/evidence/pulldown-runtime.json',JSON.stringify(report,null,2));console.log(JSON.stringify(report,null,2));
