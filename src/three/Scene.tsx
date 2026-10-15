import {Suspense,useMemo,useRef,useEffect} from 'react';
import {Canvas,useFrame, type ThreeEvent} from '@react-three/fiber';
import {OrbitControls,Grid,useGLTF} from '@react-three/drei';
import * as THREE from 'three';
import {useAtlas} from '../stores/useAtlas';
import {appearance,resolveState} from './materials';
import {advance,elbowAngle,DURATION} from './animation';
import {curl} from '../data/anatomy';
import {byMesh} from '../data/catalogue';
import LatPulldownMachine from './LatPulldownMachine';
function Muscle({id,position,scale}:{id:string;position:[number,number,number];scale:[number,number,number]}){
 const s=useAtlas(); const role=s.mode==='exercise'?curl.relations.find(r=>r.muscleId===id)?.role:undefined;
 const a=appearance(resolveState(id,s.selected,s.hovered,s.hidden,role),s.style);
 return <mesh position={position} scale={scale} visible={a.visible} onClick={e=>{e.stopPropagation();s.set({selected:id});}} onPointerOver={e=>{e.stopPropagation();s.set({hovered:id});}} onPointerOut={()=>s.set({hovered:null})}><sphereGeometry args={[1,32,24]}/><meshStandardMaterial {...a}/></mesh>;
}
function Arm({side}:{side:number}){
 const joint=useRef<THREE.Group>(null);useFrame(()=>{if(joint.current)joint.current.rotation.x=elbowAngle(useAtlas.getState().time);});
 return <group position={[side*.67,1.65,0]} rotation={[0,0,side*.1]}>
 <Muscle id="deltoid" position={[0,0,0]} scale={[.22,.23,.22]}/>
 <Muscle id="biceps" position={[0,-.36,.08]} scale={[.15,.3,.14]}/>
 <Muscle id="triceps" position={[0,-.36,-.1]} scale={[.15,.31,.12]}/>
 <group ref={joint} position={[0,-.7,0]}>
 <Muscle id="forearm" position={[0,-.3,0]} scale={[.12,.3,.12]}/>
 <mesh position={[0,-.68,0]}><sphereGeometry args={[.105,20,16]}/><meshStandardMaterial color="#cfbda8"/></mesh>
 <group position={[0,-.72,0]} rotation={[0,0,Math.PI/2]}><mesh><cylinderGeometry args={[.04,.04,.5]}/><meshStandardMaterial color="#c9d2d8" metalness={.8} roughness={.3}/></mesh>{[-.23,.23].map(y=><mesh key={y} position={[0,y,0]}><cylinderGeometry args={[.15,.15,.12,24]}/><meshStandardMaterial color="#242f39"/></mesh>)}</group>
 </group></group>;
}
function Prototype(){return <group position={[0,-1,0]}>
 <mesh position={[0,2.25,0]} scale={[.25,.32,.24]}><sphereGeometry args={[1,32,24]}/><meshStandardMaterial color="#b6bcc3"/></mesh>
 <mesh position={[0,1.46,-.04]} scale={[.52,.65,.23]}><sphereGeometry args={[1,32,24]}/><meshStandardMaterial color="#33414b"/></mesh>
 {[-1,1].map(side=><group key={side}><Muscle id="pectoralis" position={[side*.25,1.65,.2]} scale={[.25,.24,.13]}/><Muscle id="quadriceps" position={[side*.25,.35,.05]} scale={[.2,.47,.2]}/><Muscle id="quadriceps" position={[side*.25,-.42,0]} scale={[.13,.38,.14]}/><Arm side={side}/></group>)}
 <Muscle id="abs" position={[0,1.08,.22]} scale={[.25,.32,.1]}/>
 </group>;}
function Anatomy(){
 const {scene}=useGLTF('/models/anatomy.glb'); const root=useMemo(()=>(()=>{const clone=scene.clone(true);clone.rotation.x=-Math.PI/2;clone.updateMatrixWorld(true);return clone;})(),[scene]);const s=useAtlas();
 const box=useMemo(()=>new THREE.Box3().setFromObject(root),[root]);const size=box.getSize(new THREE.Vector3());const center=box.getCenter(new THREE.Vector3());const factor=3.5/size.y;
 useEffect(()=>{root.traverse(o=>{if(o instanceof THREE.Mesh){const entry=byMesh.get(o.name);const id=entry?.anatomyId||o.name;o.userData.anatomyId=id;const a=appearance(resolveState(id,s.selected,s.hovered,s.hidden),s.style);o.visible=a.visible;o.material=new THREE.MeshStandardMaterial({...a,color:entry?.isTendon&&a.color===(s.style==='real'?'#943a3f':'#9aabb8')?'#d4c5ad':a.color});}});return ()=>{root.traverse(o=>{if(o instanceof THREE.Mesh)(o.material as THREE.Material).dispose();});};},[root,s.style,s.selected,s.hovered,s.hidden]);
 const pick=(e:ThreeEvent<PointerEvent>|ThreeEvent<MouseEvent>,hover=false)=>{e.stopPropagation();s.set(hover?{hovered:e.object.userData.anatomyId||e.object.name}:{selected:e.object.userData.anatomyId||e.object.name});};
 return <group scale={factor} position={[-center.x*factor,-center.y*factor+.3,-center.z*factor]}><primitive object={root} onClick={pick} onPointerOver={(e:ThreeEvent<PointerEvent>)=>pick(e,true)} onPointerOut={()=>s.set({hovered:null})}/></group>;
}
function Clock(){useFrame((_,delta)=>{const s=useAtlas.getState();if(s.playing){const time=advance(s.time,delta,s.speed,s.loop);s.set({time,playing:s.loop||time<DURATION});}});return null;}
function CameraControls(){const ref=useRef<React.ComponentRef<typeof OrbitControls>>(null);const reset=useAtlas(s=>s.reset);useEffect(()=>{ref.current?.reset();},[reset]);return <OrbitControls ref={ref} makeDefault minDistance={2} maxDistance={12} target={[0,.3,0]}/>;}
export default function Scene(){const model=useAtlas(s=>s.model);const latDemo=useAtlas(s=>s.mode==='exercise'&&s.exerciseId==='lat-pulldown');return <Canvas camera={{position:[0,1,5.8],fov:42}} dpr={[1,2]} onPointerMissed={()=>useAtlas.getState().set({selected:null})}><color attach="background" args={['#111922']}/><ambientLight intensity={.8}/><directionalLight position={[3,5,5]} intensity={2.5}/><directionalLight position={[-4,2,-3]} intensity={1.5} color="#8eaed1"/><Suspense fallback={null}>{latDemo?<group position={[0,-.8,0]}><LatPulldownMachine progress={useAtlas.getState().time/DURATION}/></group>:model==='anatomy'?<Anatomy/>:<Prototype/>}</Suspense><Grid position={[0,latDemo?-.8:-1.95,0]} args={[10,10]} cellColor="#2b3947" sectionColor="#43515e" fadeDistance={12} infiniteGrid/><CameraControls/><Clock/></Canvas>;}
