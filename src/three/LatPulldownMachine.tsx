import {useMemo} from 'react';
import * as THREE from 'three';
import {latPulldownFrame} from './pulldownMotion';
import {useAtlas} from '../stores/useAtlas';
import config from '../data/pulldown-config.json';
import {DURATION} from './animation';
type V3 = [number,number,number];
const STEEL='#596a77', FRAME='#26343e', DARK='#101b24', CHROME='#b3c7d2', PAD='#17242d';
function Beam({from,to,r=.025,color=STEEL}:{from:V3;to:V3;r?:number;color?:string}){
 const {center,quaternion,length}=useMemo(()=>{
  const start=new THREE.Vector3(...from),end=new THREE.Vector3(...to);
  const delta=end.clone().sub(start);
  return {center:start.clone().add(end).multiplyScalar(.5),length:delta.length(),quaternion:new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0,1,0),delta.normalize())};
 },[...from,...to]);
 return <mesh position={center} quaternion={quaternion} castShadow>
  <cylinderGeometry args={[r,r,length,12]}/><meshStandardMaterial color={color} roughness={.35} metalness={.62}/>
 </mesh>;
}
function Box({position,size,color=FRAME}:{position:V3;size:V3;color?:string}){
 return <mesh position={position} castShadow receiveShadow><boxGeometry args={size}/><meshStandardMaterial color={color} metalness={.28} roughness={.52}/></mesh>;
}
function Pulley({z}:{z:number}){
 return <group position={[0,2.20,z]}>
  <mesh rotation={[0,0,Math.PI/2]} castShadow><cylinderGeometry args={[.088,.088,.042,32]}/><meshStandardMaterial color={DARK} metalness={.22}/></mesh>
  <mesh rotation={[0,0,Math.PI/2]}><cylinderGeometry args={[.027,.027,.06,20]}/><meshStandardMaterial color={CHROME} metalness={.75} roughness={.25}/></mesh>
 </group>;
}
/** Machine presentation driven by the same configuration and time as the baked seated rig. */
export default function LatPulldownMachine(){
 const time=useAtlas(s=>s.time);
 const {barY,weightY}=latPulldownFrame(time/DURATION);
 return <group name="LatPulldownMachine">
  {/* Dual-upright cable tower and stabilizing feet */}
  {[-.76,.76].map(x=><group key={x}>
    <Box position={[x,1.12,-.60]} size={[.085,2.23,.09]}/>
    <Box position={[x,.055,-.19]} size={[.12,.11,1.27]}/>
    <Box position={[x,2.25,-.60]} size={[.15,.09,.21]}/>
  </group>)}
  <Box position={[0,2.27,-.60]} size={[1.64,.09,.12]}/>
  <Box position={[0,2.19,-.06]} size={[.11,.10,1.18]}/>
  <Beam from={[-.76,.25,-.6]} to={[.76,.25,-.6]} r={.021}/>
  <Pulley z={-.62}/><Pulley z={.42}/>
  {/* Seat, pedestal and thigh restraint */}
  <Box position={[0,.36,.34]} size={[.07,.64,.07]}/>
  <Box position={[0,.64,.34]} size={[.52,.085,.42]} color={PAD}/>
  <Box position={[0,.80,.43]} size={[.46,.12,.15]} color={PAD}/>
  {[-.27,.27].map(x=><Beam key={x} from={[x,.79,.42]} to={[x,.95,.42]} r={.016} color={CHROME}/>)}
  <Beam from={[-.34,.89,.42]} to={[.34,.89,.42]} r={.065} color={PAD}/>
  <Box position={[0,config.footPlatformY,.68]} size={[.55,.04,.38]}/>
  {/* Weight guide rods and fixed lower block */}
  {[-.20,.20].map(x=><Beam key={x} from={[x,.27,-.68]} to={[x,1.93,-.68]} r={.014} color={CHROME}/>)}
  <Box position={[0,.20,-.68]} size={[.53,.12,.31]}/>
  <group name="MovingWeightStack" position={[0,weightY,-.68]}>
   {Array.from({length:6},(_,i)=><Box key={i} position={[0,i*.064,0]} size={[.50,.049,.26]} color={i===5?'#607482':'#1c2a34'}/>)}
   <Beam from={[0,.00,0]} to={[0,.69,0]} r={.011} color={CHROME}/>
  </group>
  {/* Wide lat bar with angled outer grips; bar and raised weights share one progress signal */}
  <group name="MovingLatBar" position={[0,barY,config.gripZ]}>
   <Beam from={[-.30,0,0]} to={[.30,0,0]} r={.019} color={CHROME}/>
   {[-1,1].map(side=><group key={side}>
     <Beam from={[side*.30,0,0]} to={[side*.46,-.126,0]} r={.019} color={CHROME}/>
     <Beam from={[side*.32,-.01575,0]} to={[side*.46,-.126,0]} r={.024} color={DARK}/>
   </group>)}
   <Beam from={[0,.09,0]} to={[0,0,0]} r={.013} color={CHROME}/>
  </group>
  {/* Cable is connected to the moving endpoints; it is a straight taut demonstration, not pulley dynamics. */}
  <Beam from={[0,2.20,.42]} to={[0,barY+.09,config.gripZ]} r={.005} color={CHROME}/>
  <Beam from={[0,2.288,-.62]} to={[0,2.288,.42]} r={.005} color={CHROME}/>
  <Beam from={[0,2.20,-.62]} to={[0,weightY+.69,-.68]} r={.005} color={CHROME}/>
 </group>;
}
