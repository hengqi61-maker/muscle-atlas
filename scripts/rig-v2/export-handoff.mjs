import fs from 'node:fs/promises';
import crypto from 'node:crypto';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { AnimationMixer, Matrix4, Quaternion, Vector3, LoopOnce } from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
export const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
export const modelPath = 'public/experimental/rig-v2/unified-rig-prototype.glb';
export const sha256 = b => crypto.createHash('sha256').update(b).digest('hex');
export async function observe() {
 const bytes = await fs.readFile(path.join(root, modelPath));
 const gltf = await new GLTFLoader().parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength), '');
 gltf.scene.updateMatrixWorld(true);
 const bones=[]; gltf.scene.traverse(n=>{if(n.isBone) bones.push(n)});
 const snapshot=()=>bones.map(b=>{const p=new Vector3(),q=new Quaternion(),s=new Vector3();b.matrixWorld.decompose(p,q,s);return {name:b.name,localMatrix:b.matrix.toArray(),worldMatrix:b.matrixWorld.toArray(),localQuaternionXyzw:b.quaternion.toArray(),worldQuaternionXyzw:q.toArray(),parentWorldMatrix:b.parent?.matrixWorld.toArray()??new Matrix4().toArray()}});
 const reference=snapshot();
 const skins=[]; gltf.scene.traverse(n=>{if(n.isSkinnedMesh) skins.push({mesh:n.name,bindMatrix:n.bindMatrix.toArray(),bindMatrixInverse:n.bindMatrixInverse.toArray(),joints:n.skeleton.bones.map((b,i)=>({name:b.name,inverseBindMatrix:n.skeleton.boneInverses[i].toArray()}))})});
 const clips=[];
 for(const clip of gltf.animations){
  const mixer=new AnimationMixer(gltf.scene),action=mixer.clipAction(clip); action.setLoop(LoopOnce,1);action.clampWhenFinished=true;action.play();
  const frames=[];for(let i=0;i<=120;i++){const time=clip.duration*i/120;mixer.setTime(time);gltf.scene.updateMatrixWorld(true);frames.push({index:i,timeSeconds:time,phase:i/120,bones:snapshot()})}
  clips.push({name:clip.name,durationSeconds:clip.duration,trackCount:clip.tracks.length,kind:'authored diagnostic trajectory; not motion capture or normative biomechanics',fixedPhaseFrameIndices:[0,30,60,90,120],frames});
  mixer.stopAllAction();mixer.uncacheRoot(gltf.scene);
 }
 const canonicalBytes=await fs.readFile(path.join(root,'config/rig-v2/canonical-rig.json'));
 return {format:'muscle-atlas.initial-mac-observation',version:'0.1.0',status:'Initial Mac producer format; Windows owns final exchange schema',source:{assetCommit:'b904b4b200fc838cb7fabbf4ed2ef346faa73b53',modelPath,modelSha256:sha256(bytes),canonicalPath:'config/rig-v2/canonical-rig.json',canonicalSha256:sha256(canonicalBytes),threeVersion:'0.180.0'},conventions:{gltf:{unit:'metre',up:'+Y',handedness:'right',matrixStorage:'column-major flat 16',quaternionOrder:'xyzw',vectorAction:'column vector; world = parentWorld * local',localAxes:'numeric transform basis only; not calibrated anatomical axes'},referenceMeaning:'Default glTF node transforms before mixer evaluation; inverse bind matrices recorded separately, not asserted equal to default reference.',blender:JSON.parse(canonicalBytes).blenderConvention},bones:bones.map((b,i)=>({index:i,name:b.name,parentBone:b.parent?.isBone?b.parent.name:null,parentNode:b.parent?.name??null})),reference,skins,blenderReference:JSON.parse(canonicalBytes),attachmentRegistry:JSON.parse(await fs.readFile(path.join(root,'config/rig-v2/attachment-registry.json'))),clips};
}
if(process.argv[1]===fileURLToPath(import.meta.url)){const data=await observe();await fs.writeFile(path.join(root,'docs/rig-v2/handoff/mac-observation-v0.1.json'),JSON.stringify(data));console.log(`Exported ${data.bones.length} bones, ${data.clips.length} clips, 121 frames per clip; ${data.source.modelSha256}`)}
