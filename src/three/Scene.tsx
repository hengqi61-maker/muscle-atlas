import {Suspense,useMemo,useRef,useEffect} from 'react';
import {Canvas,useFrame,useThree,type ThreeEvent} from '@react-three/fiber';
import {OrbitControls,Grid,useGLTF} from '@react-three/drei';
import * as THREE from 'three';
import {clone} from 'three/addons/utils/SkeletonUtils.js';
import {useAtlas} from '../stores/useAtlas';
import {appearance,resolveState} from './materials';
import {advance,DURATION} from './animation';
import {createSkinnedBounds} from './skinnedBounds';
import {byMesh} from '../data/catalogue';
import LatPulldownMachine from './LatPulldownMachine';
import {GraspRuntime} from '../grasp-v2/runtime';
import {useGrasp} from '../grasp-v2/store';
import {latPulldownAnatomyRelations} from '../data/latPulldown';

function Anatomy({model}:{model:'anatomy'|'rigged'|'pulldown'}){
 const grasp=useGrasp(s=>s.enabled);
 const version=useAtlas(s=>s.motionVersion);const playbackKind=useAtlas(s=>s.playbackKind);const experimental=(grasp||playbackKind==='diagnostic')&&model!=='anatomy';
 const animated=model!=='anatomy';const seated=model==='pulldown'&&!experimental;
 const {scene,animations}=useGLTF(grasp?'/experimental/grasp-controller.glb':experimental?(version==='e03'?'/artifacts/phase2/E03-equivalence-projection/motion.glb':'/experimental/rig-v2/unified-rig-prototype.glb'):seated?'/models/anatomy-pulldown.glb':animated?'/models/anatomy-curl.glb':'/models/anatomy.glb');
 const root=useMemo(()=>{
  const object=clone(scene);if(!animated)object.rotation.x=-Math.PI/2;
  object.updateMatrixWorld(true);
  object.traverse(o=>{if(o instanceof THREE.Mesh){
   const source=String(o.userData.sourceName||o.name);
   const entry=byMesh.get(THREE.PropertyBinding.sanitizeNodeName(source));
   o.userData.anatomyId=entry?.anatomyId||o.name;
   o.userData.entry=entry;
   // Animated geometry can leave its bind-pose bounding sphere. Keep accurate picking too.
   if(o instanceof THREE.SkinnedMesh)o.frustumCulled=false;
  }});
  return object;
 },[scene,animated]);
 const graspRuntime=useRef<GraspRuntime|null>(null);
 useEffect(()=>{graspRuntime.current=grasp?new GraspRuntime(root):null;return()=>{graspRuntime.current?.dispose();graspRuntime.current=null;};},[root,grasp]);
 const skins=useMemo(()=>{
  const meshes:THREE.SkinnedMesh[]=[];
  root.traverse(o=>{if(o instanceof THREE.SkinnedMesh)meshes.push(o);});
  return meshes;
 },[root]);
 const conservativeBounds=useMemo(()=>(seated||experimental)?skins.map(createSkinnedBounds):null,[skins,seated,experimental]);
 const appliedPose=useRef<{time:number;morphMode:string;morphWeight:number}|null>(null);
 const mixer=useMemo(()=>{
  const value=new THREE.AnimationMixer(root);
  return value;
 },[root,animations,animated]);
 const box=useMemo(()=>new THREE.Box3().setFromObject(root),[root]);
 const size=box.getSize(new THREE.Vector3()),center=box.getCenter(new THREE.Vector3()),factor=3.5/size.y;
 const style=useAtlas(s=>s.style),selected=useAtlas(s=>s.selected),hovered=useAtlas(s=>s.hovered),hidden=useAtlas(s=>s.hidden),mode=useAtlas(s=>s.mode);
 useEffect(()=>{
  const materials:THREE.Material[]=[];
  root.traverse(o=>{if(o instanceof THREE.Mesh){
   const entry=o.userData.entry;const name=String(entry?.name||'');
   const role=model==='pulldown'&&mode==='exercise'?latPulldownAnatomyRelations.find(r=>r.anatomyId===entry?.anatomyId)?.role:animated&&mode==='exercise'&&(experimental||name.includes('left'))?
    name.includes('biceps brachii')?'primary':(name.includes('brachialis')||name.includes('brachioradialis'))?'secondary':(name.includes('deltoid')||((name.includes('flexor')||name.includes('extensor'))&&o.userData.rigRegion))?'stabilizer':undefined:undefined;
   const state=resolveState(o.userData.anatomyId,selected,hovered,hidden,role);
   if(!entry){o.visible=o.userData.visualLayer!=='contact-marker'&&!(grasp&&/^Grasp(Bar|Rope)/.test(o.name));return;}
   const a=appearance(state,style);o.visible=a.visible;
   const color=entry.isTendon&&(state==='default'||state==='dimmed')?'#d4c5ad':a.color;
   const material=new THREE.MeshStandardMaterial({...a,color});materials.push(material);o.material=material;
  }});
  return ()=>materials.forEach(m=>m.dispose());
 },[root,style,selected,hovered,hidden,animated,mode,seated,experimental,model,grasp]);
 const activeClip=experimental?animations.find(c=>c.name===(model==='pulldown'?'PulldownProbe':'CurlProbe')):animations[0];
 useEffect(()=>{appliedPose.current=null;if(animated){if(!activeClip)throw new Error('动画资源缺少对应 clip');const action=mixer.clipAction(activeClip);action.setLoop(THREE.LoopOnce,1);action.clampWhenFinished=true;action.reset().play();}return ()=>{mixer.stopAllAction();mixer.uncacheRoot(root);};},[mixer,root,animated,activeClip]);
 useFrame((state,delta)=>{if(!animated)return;
  const s=useAtlas.getState();const time=Math.min(s.time,DURATION);const previous=appliedPose.current;
  if((!graspRuntime.current||!graspRuntime.current.needsUpdate)&&previous?.time===time&&previous.morphMode===s.morphMode&&previous.morphWeight===s.morphWeight)return;
  if(!activeClip)return;graspRuntime.current?.beforeMixer();const action=mixer.clipAction(activeClip);action.paused=false;action.enabled=true;mixer.setTime(experimental?time/DURATION*activeClip.duration:time);root.updateMatrixWorld(true);
  graspRuntime.current?.update(time,delta,state.clock.elapsedTime);
  for(const [index,o] of skins.entries()){
   if(s.morphMode==='manual'&&o.morphTargetInfluences&&o.morphTargetDictionary?.BicepsBulge!==undefined)o.morphTargetInfluences[o.morphTargetDictionary.BicepsBulge]=s.morphWeight;
   // Raycasting needs bounds of the current deformed vertices; refresh every changed pose,
   // including paused seeks and independent morph edits. WebGLRenderer updates
   // each shared skeleton once per render, so no per-mesh skeleton upload here.
   if(conservativeBounds)conservativeBounds[index]();else o.computeBoundingSphere();
  }
  appliedPose.current={time,morphMode:s.morphMode,morphWeight:s.morphWeight};
 });
 const pick=(e:ThreeEvent<PointerEvent>|ThreeEvent<MouseEvent>,hover=false)=>{
  if(!e.object.userData.entry)return;e.stopPropagation();
  useAtlas.getState().set(hover?{hovered:e.object.userData.anatomyId}:{selected:e.object.userData.anatomyId});
 };
 if(grasp||seated)return <primitive object={root} onClick={pick} onPointerOver={(e:ThreeEvent<PointerEvent>)=>pick(e,true)} onPointerOut={()=>useAtlas.getState().set({hovered:null})}/>;
 return <group scale={factor} position={[-center.x*factor,-center.y*factor+.3,-center.z*factor]}>
  <primitive object={root} onClick={pick} onPointerOver={(e:ThreeEvent<PointerEvent>)=>pick(e,true)} onPointerOut={()=>useAtlas.getState().set({hovered:null})}/>
 </group>;
}
function Clock(){useFrame((_,delta)=>{const s=useAtlas.getState();if(s.playing){const time=advance(s.time,delta,s.speed,s.loop);s.set({time,playing:s.loop||time<DURATION});}});return null;}
function CameraControls(){
 const world=useThree(s=>s.scene);
 const ref=useRef<React.ComponentRef<typeof OrbitControls>>(null);
 const version=useAtlas(s=>s.motionVersion);const playbackKind=useAtlas(s=>s.playbackKind);const reset=useAtlas(s=>s.reset),focus=useAtlas(s=>s.focus),model=useAtlas(s=>s.model);
 useEffect(()=>{const controls=ref.current;if(!controls)return;
  if(useGrasp.getState().enabled&&focus==='grip'){const hand=world.getObjectByName(`${useGrasp.getState().side}Hand`);if(hand){const point=hand.getWorldPosition(new THREE.Vector3());controls.target.copy(point);controls.object.position.copy(point).add(new THREE.Vector3(.16,.07,.24));}}
  else if(focus==='grip'){controls.object.position.set(.95,1.15,1.55);controls.target.set(.40,.90,.55);}
  else if(focus==='arm'){controls.object.position.set(1.7,1.25,2.1);controls.target.set(.44,.90,.15);}
  else if(focus==='back'){controls.object.position.set(-.4,1.1,-3.3);controls.target.set(0,.30,.10);}
  else if(focus==='side'){controls.object.position.set(4,1.1,.1);controls.target.set(0,.30,.10);}
  else if(model==='pulldown'&&playbackKind!=='diagnostic'){controls.object.position.set(3,1.4,5.3);controls.target.set(0,.15,.1);}
  else{controls.object.position.set(0,1,5.8);controls.target.set(0,.3,0);}
  controls.update();
 },[reset,focus,model,version,playbackKind]);
 return <OrbitControls ref={ref} makeDefault minDistance={.8} maxDistance={12} target={[0,.3,0]}/>;
}
export default function Scene(){const grasp=useGrasp(s=>s.enabled);const kind=useGrasp(s=>s.kind);const model=useAtlas(s=>s.model),version=useAtlas(s=>s.motionVersion),playbackKind=useAtlas(s=>s.playbackKind);return <Canvas camera={{position:[0,1,5.8],fov:42}} dpr={[1,2]} onPointerMissed={()=>useAtlas.getState().set({selected:null})}>
 <color attach="background" args={['#111922']}/><ambientLight intensity={.8}/><directionalLight position={[3,5,5]} intensity={2.5}/><directionalLight position={[-4,2,-3]} intensity={1.5} color="#8eaed1"/>
 <Suspense fallback={null}>{model==='pulldown'&&playbackKind!=='diagnostic'?<group position={[0,-1.45,0]} scale={1.45}><Anatomy model={model}/><LatPulldownMachine/></group>:<Anatomy key={model+version+playbackKind} model={model}/>}</Suspense>
 <Grid position={[0,-1.5,0]} args={[10,10]} cellColor="#2b3947" sectionColor="#43515e" fadeDistance={12} infiniteGrid/><CameraControls/><Clock/>
 </Canvas>;}
