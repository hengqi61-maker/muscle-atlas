import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {inspect} from '../../scripts/infra/validate-assets.mjs';
function glb(json,bin){
  let s=JSON.stringify(json);s+=' '.repeat((4-Buffer.byteLength(s)%4)%4);
  const jsonLength=Buffer.byteLength(s),b=Buffer.alloc(20+jsonLength+(bin?8+bin.length:0));b.write('glTF');b.writeUInt32LE(2,4);b.writeUInt32LE(b.length,8);b.writeUInt32LE(jsonLength,12);b.writeUInt32LE(0x4e4f534a,16);b.write(s,20);if(bin){b.writeUInt32LE(bin.length,20+jsonLength);b.writeUInt32LE(0x004e4942,24+jsonLength);bin.copy(b,28+jsonLength);}return b;
}
async function fixture(name,json,fn,bin){
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'atlas-validator-'));const file=path.join(dir,name);
  try{fs.writeFileSync(file,glb(json,bin));await fn(await inspect(file));}finally{fs.rmSync(dir,{recursive:true});}
}
test('missing required curl joints fails independently of JSON parse',()=>fixture('curl.glb',{asset:{version:'2.0'},scenes:[{nodes:[0]}],nodes:[{}],scene:0},r=>assert.ok(r.errors.some(e=>e.includes('missing joint')))));
test('nonunit node quaternion fails',()=>fixture('generic.glb',{asset:{version:'2.0'},scenes:[{nodes:[0]}],nodes:[{rotation:[0,0,0,2]}],scene:0},r=>assert.ok(r.errors.length)));
test('cyclic hierarchy is rejected before runtime traversal',()=>fixture('cycle.glb',{asset:{version:'2.0'},scenes:[{nodes:[0]}],nodes:[{children:[1]},{children:[0]}],scene:0},r=>assert.ok(r.errors.length)));
test('CUBICSPLINE zero quaternion tangents are legal derivatives',async()=>{
  const bin=Buffer.alloc(104);[0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0].forEach((v,i)=>bin.writeFloatLE(v,i*4));
  const doc={asset:{version:'2.0'},buffers:[{byteLength:104}],bufferViews:[{buffer:0,byteOffset:0,byteLength:8},{buffer:0,byteOffset:8,byteLength:96}],accessors:[{bufferView:0,componentType:5126,count:2,type:'SCALAR',min:[0],max:[1]},{bufferView:1,componentType:5126,count:6,type:'VEC4'}],nodes:[{name:'Joint'}],scenes:[{nodes:[0]}],scene:0,animations:[{samplers:[{input:0,output:1,interpolation:'CUBICSPLINE'}],channels:[{sampler:0,target:{node:0,path:'rotation'}}]}]};
  await fixture('cubic.glb',doc,r=>assert.deepEqual(r.errors,[]),bin);
});
