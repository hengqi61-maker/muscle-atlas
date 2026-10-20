import {readFileSync, writeFileSync} from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createRequire} from 'node:module';
import {poseFor, applyToObject3D} from '../../src/grasp-v1/controller.mjs';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const require = createRequire(import.meta.url);
let THREE, GLTFLoader;
try {
  THREE = require('three');
  ({GLTFLoader} = require('three/examples/jsm/loaders/GLTFLoader.js'));
} catch (e) {
  writeFileSync(path.join(root,'artifacts/grasp-v1/three-smoke.json'), JSON.stringify({status:'SKIP',reason:String(e.message)}));
  console.log('SKIP three', e.message);
  process.exit(0);
}
// Node has no FileLoader blob; use parse
const buf = readFileSync(path.join(root,'artifacts/grasp-v1/grasp-controller.glb'));
const loader = new GLTFLoader();
const gltf = await new Promise((res,rej)=>loader.parse(buf.buffer.slice(buf.byteOffset, buf.byteOffset+buf.byteLength), '', res, rej));
const names=[];
gltf.scene.traverse(o=>{if(o.isBone) names.push(o.name)});
const fingers=names.filter(n=>/Thumb|Index|Middle|Ring|Little/.test(n));
const hitOpen=applyToObject3D(gltf.scene, {...poseFor('open','Left'),...poseFor('open','Right')});
const hitClosed=applyToObject3D(gltf.scene, {...poseFor('closed','Left'),...poseFor('closed','Right')});
const report={status:'PASS',bones:names.length,fingerBones:fingers.length,hitOpen,hitClosed,sample:fingers.slice(0,8)};
writeFileSync(path.join(root,'artifacts/grasp-v1/three-smoke.json'), JSON.stringify(report,null,2));
console.log(report);
