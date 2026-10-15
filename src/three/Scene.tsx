import {Suspense,useMemo,useRef,useEffect} from 'react';
import {Canvas,useFrame,type ThreeEvent} from '@react-three/fiber';
import {OrbitControls,Grid,useGLTF} from '@react-three/drei';
import * as THREE from 'three';
import {clone} from 'three/addons/utils/SkeletonUtils.js';
import {useAtlas} from '../stores/useAtlas';
import {appearance,resolveState} from './materials';
import {advance,DURATION} from './animation';
import {byMesh} from '../data/catalogue';
import LatPulldownMachine from './LatPulldownMachine';
import {latPulldownAnatomyRelations} from '../data/latPulldown';

function Anatomy({model}:{model:'anatomy'|'rigged'|'pulldown'}){
 const animated=model!=='anatomy';const seated=model==='pulldown';
 const {scene,animations}=useGLTF(seated?'/models/anatomy-pulldown.glb':animated?'/models/anatomy-curl.glb':'/models/anatomy.glb');
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
   const role=seated&&mode==='exercise'?latPulldownAnatomyRelations.find(r=>r.anatomyId===entry?.anatomyId)?.role:animated&&mode==='exercise'&&name.includes('left')?
    name.includes('biceps brachii')?'primary':(name.includes('brachialis')||name.includes('brachioradialis'))?'secondary':(name.includes('deltoid')||((name.includes('flexor')||name.includes('extensor'))&&o.userData.rigRegion))?'stabilizer':undefined:undefined;
   const state=resolveState(o.userData.anatomyId,selected,hovered,hidden,role);
   if(!entry){o.visible=o.userData.visualLayer!=='contact-marker';return;}
   const a=appearance(state,style);o.visible=a.visible;
   const color=entry.isTendon&&(state==='default'||state==='dimmed')?'#d4c5ad':a.color;
   const material=new THREE.MeshStandardMaterial({...a,color});materials.push(material);o.material=material;
  }});
  return ()=>materials.forEach(m=>m.dispose());
 },[root,style,selected,hovered,hidden,animated,mode,seated]);
 useEffect(()=>{if(animated){if(!animations.length)throw new Error('动画资源缺少 clip');const action=mixer.clipAction(animations[0]);action.setLoop(THREE.LoopOnce,1);action.clampWhenFinished=true;action.reset().play();}return ()=>{mixer.stopAllAction();mixer.uncacheRoot(root);};},[mixer,root,animated,animations]);
 useFrame(()=>{if(!animated)return;
  const s=useAtlas.getState();const action=mixer.clipAction(animations[0]);action.paused=false;action.enabled=true;mixer.setTime(Math.min(s.time,DURATION));root.updateMatrixWorld(true);
  root.traverse(o=>{if(o instanceof THREE.SkinnedMesh){
   if(s.morphMode==='manual'&&o.morphTargetInfluences&&o.morphTargetDictionary?.BicepsBulge!==undefined)o.morphTargetInfluences[o.morphTargetDictionary.BicepsBulge]=s.morphWeight;
   o.skeleton.update();o.computeBoundingSphere();
  }});
 });
 const pick=(e:ThreeEvent<PointerEvent>|ThreeEvent<MouseEvent>,hover=false)=>{
  if(!e.object.userData.entry)return;e.stopPropagation();
  useAtlas.getState().set(hover?{hovered:e.object.userData.anatomyId}:{selected:e.object.userData.anatomyId});
 };
 if(seated)return <primitive object={root} onClick={pick} onPointerOver={(e:ThreeEvent<PointerEvent>)=>pick(e,true)} onPointerOut={()=>useAtlas.getState().set({hovered:null})}/>;
 return <group scale={factor} position={[-center.x*factor,-center.y*factor+.3,-center.z*factor]}>
  <primitive object={root} onClick={pick} onPointerOver={(e:ThreeEvent<PointerEvent>)=>pick(e,true)} onPointerOut={()=>useAtlas.getState().set({hovered:null})}/>
 </group>;
}
function Clock(){useFrame((_,delta)=>{const s=useAtlas.getState();if(s.playing){const time=advance(s.time,delta,s.speed,s.loop);s.set({time,playing:s.loop||time<DURATION});}});return null;}
function CameraControls(){
 const ref=useRef<React.ComponentRef<typeof OrbitControls>>(null);
 const reset=useAtlas(s=>s.reset),focus=useAtlas(s=>s.focus),model=useAtlas(s=>s.model);
 useEffect(()=>{const controls=ref.current;if(!controls)return;
  if(focus==='grip'){controls.object.position.set(.95,1.15,1.55);controls.target.set(.40,.90,.55);}
  else if(focus==='arm'){controls.object.position.set(1.7,1.25,2.1);controls.target.set(.44,.90,.15);}
  else if(focus==='back'){controls.object.position.set(-.4,1.1,-3.3);controls.target.set(0,.30,.10);}
  else if(focus==='side'){controls.object.position.set(4,1.1,.1);controls.target.set(0,.30,.10);}
  else if(model==='pulldown'){controls.object.position.set(3,1.4,5.3);controls.target.set(0,.15,.1);}
  else{controls.object.position.set(0,1,5.8);controls.target.set(0,.3,0);}
  controls.update();
 },[reset,focus,model]);
 return <OrbitControls ref={ref} makeDefault minDistance={.8} maxDistance={12} target={[0,.3,0]}/>;
}
export default function Scene(){const model=useAtlas(s=>s.model);return <Canvas camera={{position:[0,1,5.8],fov:42}} dpr={[1,2]} onPointerMissed={()=>useAtlas.getState().set({selected:null})}>
 <color attach="background" args={['#111922']}/><ambientLight intensity={.8}/><directionalLight position={[3,5,5]} intensity={2.5}/><directionalLight position={[-4,2,-3]} intensity={1.5} color="#8eaed1"/>
 <Suspense fallback={null}>{model==='pulldown'?<group position={[0,-1.45,0]} scale={1.45}><Anatomy model={model}/><LatPulldownMachine/></group>:<Anatomy key={model} model={model}/>}</Suspense>
 <Grid position={[0,-1.5,0]} args={[10,10]} cellColor="#2b3947" sectionColor="#43515e" fadeDistance={12} infiniteGrid/><CameraControls/><Clock/>
 </Canvas>;}
