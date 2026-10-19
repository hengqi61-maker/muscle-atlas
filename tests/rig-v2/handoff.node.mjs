import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import { Matrix4, Quaternion, Vector3 } from 'three';
import {root,modelPath,sha256,observe} from '../../scripts/rig-v2/export-handoff.mjs';
const data=JSON.parse(await fs.readFile(path.join(root,'docs/rig-v2/handoff/mac-observation-v0.1.json')));
const near=(a,b,e=2e-5)=>assert.ok(Math.abs(a-b)<e,`${a} != ${b}`);
const matrixNear=(a,b)=>a.elements.forEach((v,i)=>near(v,b.elements[i]));
test('actual source SHA and deterministic loader observations',async()=>{
 assert.equal(data.source.modelSha256,sha256(await fs.readFile(path.join(root,modelPath))));
 assert.equal(sha256(JSON.stringify(await observe())),sha256(JSON.stringify(data)));
 assert.equal(data.bones.length,27);assert.equal(data.clips.length,2);
});
test('topological names, actual affine composition, proper rotations, finite frames',()=>{
 const names=new Set();for(const b of data.bones){if(b.parentBone)assert.ok(names.has(b.parentBone));assert.ok(!names.has(b.name));names.add(b.name)}
 for(const group of [data.reference,...data.clips.flatMap(c=>{assert.equal(c.frames.length,121);near(c.frames.at(-1).timeSeconds,c.durationSeconds);assert.deepEqual(c.fixedPhaseFrameIndices,[0,30,60,90,120]);return c.frames.map(f=>f.bones)})]){
  assert.equal(group.length,27);
  for(const b of group){for(const key of ['localMatrix','worldMatrix','parentWorldMatrix','localQuaternionXyzw','worldQuaternionXyzw'])assert.ok(b[key].every(Number.isFinite));
   const local=new Matrix4().fromArray(b.localMatrix),world=new Matrix4().fromArray(b.worldMatrix),parent=new Matrix4().fromArray(b.parentWorldMatrix);
   matrixNear(parent.multiply(local),world);near(new Quaternion().fromArray(b.localQuaternionXyzw).length(),1);near(new Quaternion().fromArray(b.worldQuaternionXyzw).length(),1);
   near(local.determinant(),1);near(world.determinant(),1);
  }
 }
 for(const stem of ['Humerus','Forearm','Hand'])for(const side of ['Left','Right'])assert.ok(names.has(side+stem));
});
test('metre/mm and proper Z-up/Y-up conjugation round trip; noncommuting rotations',()=>{
 const basis=new Matrix4().makeRotationX(-Math.PI/2),inv=basis.clone().invert();near(basis.determinant(),1);
 const pose=new Matrix4().compose(new Vector3(.1,.2,.3),new Quaternion().setFromAxisAngle(new Vector3(1,0,0),.4).multiply(new Quaternion().setFromAxisAngle(new Vector3(0,1,0),.7)),new Vector3(1,1,1));
 const converted=basis.clone().multiply(pose).multiply(inv);matrixNear(inv.clone().multiply(converted).multiply(basis),pose);
 const p=new Vector3().setFromMatrixPosition(converted),mm=p.clone().multiplyScalar(1000);near(mm.distanceTo(p.clone().multiplyScalar(1000)),0);near(mm.multiplyScalar(.001).distanceTo(p),0);
 const a=new Matrix4().makeRotationX(.4),b=new Matrix4().makeRotationY(.7);assert.ok(a.clone().multiply(b).elements.some((v,i)=>Math.abs(v-b.clone().multiply(a).elements[i])>.01));
 const yup=new Vector3(0,0,1).applyMatrix4(basis);near(yup.y,1);near(yup.z,0);
});
