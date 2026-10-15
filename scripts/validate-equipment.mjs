import fs from 'node:fs';import assert from 'node:assert/strict';
import validator from 'gltf-validator';import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';import {Box3,Vector3} from 'three';
const file='public/models/equipment/detailed-hex-dumbbell.glb';const bytes=fs.readFileSync(file);const result=await validator.validateBytes(new Uint8Array(bytes),{uri:file,maxIssues:100});assert.equal(result.issues.numErrors,0);assert.equal(result.issues.numWarnings,0);
const g=await new GLTFLoader().parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),'');g.scene.updateMatrixWorld(true);
const heads=[];g.scene.traverse(o=>{if(o.name.includes('Dumbbell_HexHead')){const box=new Box3().setFromObject(o),center=box.getCenter(new Vector3()),size=box.getSize(new Vector3());assert.ok(Math.abs(center.y)<1e-5&&Math.abs(center.z)<1e-5);assert.ok(Math.abs(size.x-.078)<.0001);heads.push({name:o.name,center:center.toArray(),size:size.toArray()});}});assert.equal(heads.length,2);
const box=new Box3().setFromObject(g.scene),dimensions=box.getSize(new Vector3());assert.ok(dimensions.x>.30&&dimensions.x<.33);assert.ok(dimensions.y<.15&&dimensions.z<.15);
const report={file,validator:{errors:result.issues.numErrors,warnings:result.issues.numWarnings},dimensionsMetres:dimensions.toArray(),heads,origin:'original project geometry; external candidate not imported'};
fs.writeFileSync('docs/evidence/equipment-validation.json',JSON.stringify(report,null,2));console.log(JSON.stringify(report,null,2));
