import fs from 'node:fs';
import assert from 'node:assert/strict';
import validator from 'gltf-validator';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {AnimationMixer,Vector3,SkinnedMesh,Quaternion,Raycaster} from 'three';
const file='public/models/anatomy-curl.glb';const data=fs.readFileSync(file);
const validation=await validator.validateBytes(new Uint8Array(data),{uri:file,maxIssues:100});
fs.writeFileSync('docs/evidence/curl-validator.json',JSON.stringify(validation,null,2));
assert.equal(validation.issues.numErrors,0,'glTF Validator errors');
const gltf=await new GLTFLoader().parseAsync(data.buffer.slice(data.byteOffset,data.byteOffset+data.byteLength),'');
const mixer=new AnimationMixer(gltf.scene);assert.equal(gltf.animations.length,1);mixer.clipAction(gltf.animations[0]).play();
const skinned=[];gltf.scene.traverse(o=>{if(o instanceof SkinnedMesh)skinned.push(o);});assert.ok(skinned.length>=44);
const biceps=skinned.filter(o=>o.name.includes('biceps_brachii'));assert.equal(biceps.length,2);
for(const m of skinned){const a=m.geometry.attributes;assert.ok(a.skinIndex&&a.skinWeight);for(let i=0;i<a.skinWeight.count;i++){const sum=a.skinWeight.getX(i)+a.skinWeight.getY(i)+a.skinWeight.getZ(i)+a.skinWeight.getW(i);assert.ok(Math.abs(sum-1)<1e-4);}}
const forearm=gltf.scene.getObjectByName('Forearm');const upper=gltf.scene.getObjectByName('UpperArm');assert.ok(forearm&&upper);
function pose(time){mixer.setTime(time);gltf.scene.updateMatrixWorld(true);for(const m of skinned)m.skeleton.update();}
function sample(m,index){return m.localToWorld(m.getVertexPosition(index,new Vector3()));}
pose(0);const baseRotation=forearm.getWorldQuaternion(new Quaternion());const baseUpper=upper.getWorldPosition(new Vector3()).toArray();const baseElbow=forearm.getWorldPosition(new Vector3()).toArray();
const target=skinned.find(o=>o.name==='left_brachioradialis');assert.ok(target);
const positions=[];for(let i=0;i<target.geometry.attributes.position.count;i++)positions.push(sample(target,i));
const topology=Array.from(target.geometry.index.array);let blended=0;for(let i=0;i<target.geometry.attributes.skinWeight.count;i++){const w=target.geometry.attributes.skinWeight; if(w.getX(i)>0&&w.getY(i)>0)blended++;}assert.ok(blended>0,'actual source muscle must have mixed weights');
const palm=gltf.scene.getObjectByName('CurlPalmAnchor'),handle=gltf.scene.getObjectByName('CurlHandleAnchor');assert.ok(palm&&handle);
function anchor(m){const v=new Vector3();for(let i=0;i<m.geometry.attributes.position.count;i++)v.add(m.localToWorld(m.getVertexPosition(i,new Vector3())));return v.divideScalar(m.geometry.attributes.position.count);}
let maxGripError=0;
const snapshots=[];
for(const [angle,time] of [[0,0],[45,Math.acos(.25)/Math.PI*2],[90,4/3],[120,2],[0,4]]){
 pose(time);
 const measuredAngle=forearm.getWorldQuaternion(new Quaternion()).angleTo(baseRotation)*180/Math.PI;assert.ok(Math.abs(measuredAngle-angle)<.02);
 maxGripError=Math.max(maxGripError,anchor(palm).distanceTo(anchor(handle)));
 const weights=biceps.map(m=>m.morphTargetInfluences[0]);assert.ok(Math.abs(weights[0]-angle/120)<.002);
 assert.deepEqual(upper.getWorldPosition(new Vector3()).toArray(),baseUpper);
 assert.deepEqual(forearm.getWorldPosition(new Vector3()).toArray(),baseElbow);
 const ratios=[];const compressed=[];for(let i=0;i<topology.length;i+=3){for(let e=0;e<3;e++){const a=topology[i+e],b=topology[i+(e+1)%3];const rest=positions[a].distanceTo(positions[b]);if(rest>1e-6){const ratio=sample(target,a).distanceTo(sample(target,b))/rest;ratios.push(ratio);if(ratio<.2)compressed.push({restLength:rest,ratio});}}}
 ratios.sort((a,b)=>a-b);
 snapshots.push({angle,measuredAngle,time,morphWeights:weights,upperPosition:baseUpper,elbowPosition:baseElbow,probeVertex:sample(target,0).toArray(),compressedEdges:compressed.length,edgesMeasured:ratios.length,compressedSamples:compressed.slice(0,3),edgeRatio:{min:ratios[0],p50:ratios[Math.floor(ratios.length*.5)],p95:ratios[Math.floor(ratios.length*.95)],max:ratios.at(-1)}});
}
pose(4/3);target.computeBoundingSphere();
const triangle=topology.slice(0,3).map(i=>sample(target,i));
const center=triangle[0].clone().add(triangle[1]).add(triangle[2]).multiplyScalar(1/3);
const normal=triangle[1].clone().sub(triangle[0]).cross(triangle[2].clone().sub(triangle[0])).normalize();
const ray=new Raycaster(center.clone().addScaledVector(normal,.015),normal.clone().negate(),0,.03);
const rayHits=ray.intersectObject(target,false);assert.ok(rayHits.length>0,'paused deformed source mesh must be raycastable');
pose(0);const m=biceps[0];const base=sample(m,100);m.morphTargetInfluences[0]=1;const morphOnly=sample(m,100).distanceTo(base);assert.ok(morphOnly>1e-6,'independent morph must move tissue');m.morphTargetInfluences[0]=0;
assert.ok(maxGripError<1e-5);
const report={maxGripErrorMetres:maxGripError,file,validator:{errors:validation.issues.numErrors,warnings:validation.issues.numWarnings},skinnedMeshes:skinned.length,joints:skinned[0].skeleton.bones.map(b=>b.name),clips:gltf.animations.map(c=>({name:c.name,duration:c.duration,tracks:c.tracks.map(t=>t.name)})),blendedVertices:blended,independentMorphDisplacement:morphOnly,posedRaycastHits:rayHits.length,snapshots,limitation:'edge ratios are diagnostics, not proof of physiological correctness or absence of all collisions'};
fs.writeFileSync('docs/evidence/curl-runtime.json',JSON.stringify(report,null,2));console.log(JSON.stringify(report,null,2));
