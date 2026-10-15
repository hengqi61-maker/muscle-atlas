import fs from'node:fs';import path from'node:path';import{GLTFLoader}from'three/addons/loaders/GLTFLoader.js';import{AnimationMixer,Vector3,Box3,LoopOnce}from'three';
const out=path.resolve(process.argv[process.argv.indexOf('--out')+1]),cfg=JSON.parse(fs.readFileSync('src/data/pulldown-config.json')),b=fs.readFileSync('public/models/anatomy-pulldown.glb'),g=await new GLTFLoader().parseAsync(b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength),'');
const mixer=new AnimationMixer(g.scene),a=mixer.clipAction(g.animations[0]);a.setLoop(LoopOnce,1);a.clampWhenFinished=true;a.play();const meshes=[];g.scene.traverse(o=>{if(o.userData.sourceName)meshes.push(o)});
const top=new Map(),result=meshes.map(m=>{const weights={};const w=m.geometry.getAttribute('skinWeight'),j=m.geometry.getAttribute('skinIndex');if(w)for(let i=0;i<w.count;i++)for(let k=0;k<4;k++){const v=w.array[i*4+k];if(v>0){const n=m.skeleton.bones[j.array[i*4+k]].name;weights[n]=(weights[n]||0)+v/w.count}}return{sourceName:m.userData.sourceName,node:m.name,vertexCount:m.geometry.attributes.position.count,meanBoneWeights:weights,samples:[]}});
for(let frame=0;frame<=20;frame++){
 const time=frame/5;a.paused=false;a.enabled=true;mixer.setTime(time);g.scene.updateMatrixWorld(true);new Set(meshes.map(m=>m.skeleton)).forEach(s=>s?.update());
 for(let mi=0;mi<meshes.length;mi++){
  const m=meshes[mi],points=[],center=new Vector3(),box=new Box3();let inside=0,xz=0,gap=null,motion=0,max=0;
  for(let i=0;i<m.geometry.attributes.position.count;i++){
   const p=m.localToWorld(m.getVertexPosition(i,new Vector3()));if(!p.toArray().every(Number.isFinite))throw Error('Nonfinite '+m.name);points.push(p);center.add(p);box.expandByPoint(p);
   if(frame){const d=p.distanceTo(top.get(m)[i]);motion+=d;max=Math.max(max,d)}
   if(Math.abs(p.x)<.275&&p.z>.49&&p.z<.87){xz++;const d=p.y-(cfg.footPlatformY+.02);gap=gap===null?d:Math.min(gap,d);if(Math.abs(p.y-cfg.footPlatformY)<.02)inside++}
  }
  if(frame===0)top.set(m,points);center.divideScalar(points.length);result[mi].samples.push({time_s:time,centroid_m:center.toArray(),bboxMin_m:box.min.toArray(),bboxMax_m:box.max.toArray(),meanVertexDisplacementFromTop_m:motion/points.length,maxVertexDisplacementFromTop_m:max,platformBoxInteriorVertexCount:inside,platformXZOverlapVertexCount:xz,minPlatformTopSignedGap_m:gap});
 }
}
fs.writeFileSync(path.join(out,'mesh-kinematics.json'),JSON.stringify({method:'Actual deformed source vertices,21times; boneweights mean over mesh. Modelmetres x lateral/yup/z anterior. Pointinside proves penetration; zero points does not prove triangleclearance. Signedgap only in platformXZ rectangle; negative not always boxinterior. Displacement notactivation.',meshes:result},null,2));console.log({meshes:result.length,samples:21});
