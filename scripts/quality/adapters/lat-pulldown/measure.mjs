import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';import {AnimationMixer,Vector3,Quaternion,LoopOnce,SkinnedMesh} from 'three';
const out=path.resolve(process.argv[process.argv.indexOf('--out')+1]||'.'),cfg=JSON.parse(fs.readFileSync('src/data/pulldown-config.json'));
const b=fs.readFileSync('public/models/anatomy-pulldown.glb'),g=await new GLTFLoader().parseAsync(b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength),'');
const mixer=new AnimationMixer(g.scene),action=mixer.clipAction(g.animations[0]);action.setLoop(LoopOnce,1);action.clampWhenFinished=true;action.play();const meshes=[];g.scene.traverse(o=>{if(o instanceof SkinnedMesh)meshes.push(o)});const skeleton=meshes[0].skeleton;
const rows=[],detail=[];const world=v=>v.clone().multiplyScalar(1.45).add(new Vector3(0,-1.45,0));
for(let f=0;f<=120;f++){
 const time=f/30,phase=(1-Math.cos(2*Math.PI*time/4))/2,bar=cfg.barTopY-cfg.barTravel*phase,stack=.42+cfg.barTravel*phase;
 action.paused=false;action.enabled=true;mixer.setTime(time);g.scene.updateMatrixWorld(true);meshes.forEach(m=>m.skeleton.update());
 const row={time_s:time,phase,bar_y_m:bar,stack_y_m:stack},joints={};
 for(const bone of skeleton.bones){const p=bone.getWorldPosition(new Vector3()),q=bone.getWorldQuaternion(new Quaternion());joints[bone.name]={position_m:p.toArray(),scenePosition_m:world(p).toArray(),quaternion_xyzw:q.toArray(),scale:bone.scale.toArray()};for(const [i,axis]of ['x','y','z'].entries())row[bone.name+'_'+axis+'_m']=p.getComponent(i);}
 const contacts=[];
 for(const [i,name]of ['LeftPalmContact','RightPalmContact'].entries()){
  const m=g.scene.getObjectByName(name),v=new Vector3();for(let k=0;k<m.geometry.attributes.position.count;k++)v.add(m.localToWorld(m.getVertexPosition(k,new Vector3())));v.divideScalar(m.geometry.attributes.position.count);
  const target=new Vector3((i===0?1:-1)*cfg.gripHalfWidth,bar-cfg.gripDrop,cfg.gripZ);row[name+'_error_m']=v.distanceTo(target);contacts.push({name,actual_m:v.toArray(),target_m:target.toArray()});
 }
 // Centerline cable route per production component; moving endpoint paths, not pulley wrap simulation.
 const endpoints={frontCableTop:[0,2.20,.42],barCableEnd:[0,bar+.09,cfg.gripZ],bridgeBack:[0,2.288,-.62],bridgeFront:[0,2.288,.42],rearCableTop:[0,2.20,-.62],stackCableEnd:[0,stack+.69,-.68]};
 row.frontCableLength_m=new Vector3(...endpoints.frontCableTop).distanceTo(new Vector3(...endpoints.barCableEnd));row.rearCableLength_m=new Vector3(...endpoints.rearCableTop).distanceTo(new Vector3(...endpoints.stackCableEnd));row.straightCableTotal_m=row.frontCableLength_m+row.rearCableLength_m+1.04;
 detail.push({time_s:time,joints,contacts,machine:{barY_m:bar,stackY_m:stack,endpoints}});rows.push(row);
}
const keys=Object.keys(rows[0]);fs.writeFileSync(path.join(out,'joint-trajectories.csv'),keys.join(',')+'\n'+rows.map(r=>keys.map(k=>r[k]).join(',')).join('\n')+'\n');fs.writeFileSync(path.join(out,'transforms.json'),JSON.stringify({coordinateSystem:'GLB/model x right,y up,z anterior; metres. Production parent scene=1.45*model+(0,-1.45,0). Quaternions xyzw world/model. Machine sampled same formula as frozen component; not instrumented GPU objects.',sampleCount:121,samples:detail},null,2));console.log({samples:rows.length,columns:keys.length,cableTotalRange_m:[Math.min(...rows.map(r=>r.straightCableTotal_m)),Math.max(...rows.map(r=>r.straightCableTotal_m))]});
