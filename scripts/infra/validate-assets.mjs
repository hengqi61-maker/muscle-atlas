// Additive diagnostics only. Never exports/replaces production rigs.
import fs from 'node:fs';
import crypto from 'node:crypto';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import validator from 'gltf-validator';
export async function inspect(file) {
  const bytes=fs.readFileSync(file), errors=[];
  const validation=await validator.validateBytes(new Uint8Array(bytes),{uri:file,maxIssues:50});
  if(validation.issues.numErrors) errors.push(`gltf-validator: ${validation.issues.numErrors} errors`);
  if(validation.issues.messages.some(m=>m.code==='NODE_LOOP'||m.code==='NODE_PARENT_OVERRIDE'))return {file,errors,validation:validation.issues};
  const g=await new GLTFLoader().parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),'');
  const bones=[],skins=[];
  g.scene.traverse(o=>{
    if(o.isBone) bones.push({name:o.name,parent:o.parent?.isBone?o.parent.name:null,position:o.position.toArray(),quaternion_xyzw:o.quaternion.toArray()});
    if(![...o.position,...o.quaternion,...o.scale].every(Number.isFinite)) errors.push(`nonfinite transform: ${o.name}`);
    if(Math.abs(o.quaternion.length()-1)>1e-3) errors.push(`invalid quaternion: ${o.name}`);
    if(o.isMesh)for(const [name,a] of Object.entries(o.geometry.attributes))if(!Array.from(a.array).every(Number.isFinite))errors.push(`nonfinite ${name}: ${o.name}`);
    if(o.isSkinnedMesh){skins.push(o.skeleton.bones.map(b=>b.name));const a=o.geometry.attributes;
      for(const key of ['position','skinIndex','skinWeight']){
        if(!a[key]) errors.push(`missing ${key}: ${o.name}`);
        else if(!Array.from(a[key].array).every(Number.isFinite)) errors.push(`nonfinite ${key}: ${o.name}`);
      }
      if(a.skinIndex&&Array.from(a.skinIndex.array).some(v=>v<0||v>=o.skeleton.bones.length)) errors.push(`joint index: ${o.name}`);
      if(a.skinWeight)for(let i=0;i<a.skinWeight.count;i++){const w=[0,1,2,3].map(k=>a.skinWeight.getComponent(i,k));if(w.some(v=>v<0)||Math.abs(w.reduce((a,b)=>a+b,0)-1)>1e-3){errors.push(`invalid weights: ${o.name}`);break;}}
    }
  });
  for(const clip of g.animations)for(const t of clip.tracks){
    if(![...t.times,...t.values].every(Number.isFinite)) errors.push(`nonfinite track: ${t.name}`);
    for(let i=1;i<t.times.length;i++)if(t.times[i]<=t.times[i-1]) errors.push(`nonincreasing track: ${t.name}`);
    if(t.name.endsWith('.quaternion')){
      const cubic=!!t.createInterpolant.isInterpolantFactoryMethodGLTFCubicSpline;
      // CUBICSPLINE tangents are derivatives, not unit quaternions.
      for(let i=cubic?4:0;i<t.values.length;i+=cubic?12:4)if(Math.abs(Math.hypot(...t.values.slice(i,i+4))-1)>1e-3){errors.push(`invalid rotation: ${t.name}`);break;}
    }
  }
  const required=file.includes('pulldown')?['SpineRoot','Thorax','LeftScapula','RightScapula','UpperArm','Forearm','LeftHand','RightUpperArm','RightForearm','RightHand']:file.includes('curl')?['UpperArm','Forearm']:[];
  if(required.length&&(!skins.length||!g.animations.length))errors.push('expected skinned animated asset');
  for(const name of required)if(!bones.some(b=>b.name===name))errors.push(`missing joint: ${name}`);
  return {file,sha256:crypto.createHash('sha256').update(bytes).digest('hex'),errors,warnings:validation.issues.numWarnings,validatorIssues:validation.issues,bones,skinnedMeshCount:skins.length,distinctJointSets:new Set(skins.map(s=>JSON.stringify(s))).size,clips:g.animations.map(c=>({name:c.name,duration_s:c.duration,tracks:c.tracks.length})),scope:'Structural validity only; anatomical ranges need reference profiles. No collision or clinical certification.'};
}
if(process.argv[1]?.endsWith('validate-assets.mjs')){
  const files=process.argv.slice(2);if(!files.length)throw Error('Pass GLB paths');
  const reports=[];for(const f of files)reports.push(await inspect(f));
  console.log(JSON.stringify(reports,null,2));if(reports.some(r=>r.errors.length))process.exitCode=1;
}
