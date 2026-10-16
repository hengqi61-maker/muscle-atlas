import React, {Suspense, useEffect, useMemo, useRef, useState} from 'react';
import {createRoot} from 'react-dom/client';
import {Canvas, useFrame, type ThreeEvent} from '@react-three/fiber';
import {Bounds, OrbitControls, useGLTF} from '@react-three/drei';
import * as THREE from 'three';
import './style.css';
import {byMesh} from '../../data/catalogue';
import {createSkinnedBounds} from '../../three/skinnedBounds';

const ASSET='/experimental/rig-v2/unified-rig-prototype.glb';
type Identity={id:string;name:string;node:string;extras:Record<string,unknown>};
declare global { interface Window { __rigV2?:{scene:THREE.Object3D;mixer:THREE.AnimationMixer}; } }
type Inventory={identities:Identity[];clips:{name:string;duration:number}[];bones:number;skinned:number};
function identity(o:THREE.Object3D):Identity|null {
  const d=o.userData;
  const source=typeof d.sourceName==='string'?byMesh.get(THREE.PropertyBinding.sanitizeNodeName(d.sourceName)):undefined;
  const id=source?.anatomyId ?? d.anatomyId ?? d.anatomy_id ?? d.muscleId ?? d.muscle_id ?? d.sourceId ?? d.source_id;
  return id!==undefined?{id:String(id),name:String(source?.name??d.displayName??d.display_name??d.sourceName??d.name??o.name),node:o.name,extras:d}:null;
}
class Boundary extends React.Component<{children:React.ReactNode},{error:string|null}>{
  state={error:null as string|null};
  static getDerivedStateFromError(e:Error){return {error:e.message};}
  render(){return this.state.error?<div role="alert" className="failure">Asset loading failed. No replacement model is shown.<pre>{this.state.error}</pre></div>:this.props.children;}
}
function Model({clip,playing,loop,time,seekVersion,style,onInventory,onTime,onPick,onPlaying}:{clip:string;playing:boolean;loop:boolean;time:number;seekVersion:number;style:string;onInventory:(v:Inventory)=>void;onTime:(v:number)=>void;onPick:(v:Identity)=>void;onPlaying:(v:boolean)=>void}){
  const gltf=useGLTF(ASSET);
  const mixer=useMemo(()=>new THREE.AnimationMixer(gltf.scene),[gltf.scene]);
  const action=useRef<THREE.AnimationAction|null>(null);
  const bounds=useMemo(()=>{const updates:(()=>void)[]=[];gltf.scene.traverse(o=>{if(o instanceof THREE.SkinnedMesh){o.frustumCulled=true;updates.push(createSkinnedBounds(o));}});return updates;},[gltf.scene]);
  const updateBounds=()=>{gltf.scene.updateMatrixWorld(true);for(const update of bounds)update();};
  useEffect(()=>{
    const identities:Identity[]=[];let bones=0,skinned=0;
    gltf.scene.traverse(o=>{if(o instanceof THREE.Bone)bones++;if(o instanceof THREE.SkinnedMesh)skinned++;if(o instanceof THREE.Mesh){const i=identity(o);if(i)identities.push(i);o.castShadow=true;o.receiveShadow=true;}});
    window.__rigV2={scene:gltf.scene,mixer};
    onInventory({identities,clips:gltf.animations.map(c=>({name:c.name,duration:c.duration})),bones,skinned});
    return ()=>{mixer.stopAllAction();delete window.__rigV2;};
  },[gltf,mixer,onInventory]);
  useEffect(()=>{mixer.stopAllAction();const c=gltf.animations.find(c=>c.name===clip);action.current=c?mixer.clipAction(c).reset().play():null;mixer.setTime(0);updateBounds();},[clip,gltf,mixer]);
  useEffect(()=>{if(action.current){action.current.setLoop(loop?THREE.LoopRepeat:THREE.LoopOnce,loop?Infinity:1);action.current.clampWhenFinished=true;}},[loop,clip]);
  useEffect(()=>{const finished=()=>onPlaying(false);mixer.addEventListener('finished',finished);return ()=>mixer.removeEventListener('finished',finished);},[mixer,onPlaying]);
  useEffect(()=>{action.current?.reset().play();mixer.setTime(time);updateBounds();onTime(time);},[time,seekVersion,clip,mixer,onTime]);
  useEffect(()=>{const current=action.current;if(playing&&current&&current.time>=current.getClip().duration){current.reset().play();mixer.update(0);updateBounds();onTime(0);}},[playing,mixer,onTime]);
  useEffect(()=>{gltf.scene.traverse(o=>{if(o instanceof THREE.Mesh){const materials=Array.isArray(o.material)?o.material:[o.material];for(const m of materials){if(m instanceof THREE.MeshStandardMaterial){m.roughness=style==='Clean'?.88:.56;m.metalness=0;}}}});},[style,gltf]);
  useFrame((_,delta)=>{if(playing&&action.current){mixer.update(delta);updateBounds();onTime(action.current.time);}});
  function pick(e:ThreeEvent<MouseEvent>){let o:THREE.Object3D|null=e.object;while(o){const i=identity(o);if(i){e.stopPropagation();onPick(i);return;}o=o.parent;}}
  return <primitive object={gltf.scene} onClick={pick}/>;
}
function App(){
  const [inventory,setInventory]=useState<Inventory|null>(null),[clip,setClip]=useState(''),[playing,setPlaying]=useState(false),[loop,setLoop]=useState(true),[time,setTime]=useState(0),[liveTime,setLiveTime]=useState(0),[seekVersion,setSeekVersion]=useState(0),[style,setStyle]=useState('Clean'),[picked,setPicked]=useState<Identity|null>(null),[view,setView]=useState('Front');
  const camera=useRef<THREE.PerspectiveCamera|null>(null);const controls=useRef<React.ComponentRef<typeof OrbitControls>>(null);
  const duration=inventory?.clips.find(c=>c.name===clip)?.duration??0;
  useEffect(()=>{if(!camera.current||!controls.current)return;const target=controls.current.target;const distance=camera.current.position.distanceTo(target);const dir=view==='Side'?new THREE.Vector3(1,0,0):view==='Back'?new THREE.Vector3(0,0,-1):new THREE.Vector3(0,0,1);camera.current.position.copy(target).addScaledVector(dir,distance);controls.current.update();},[view]);
  return <main><header><div><p className="eyebrow">MUSCLE ATLAS / UNIFIED RIG</p><h1>V2 · R1 experimental</h1><p>Technical prototype · Not accepted · Separate from the formal application</p></div><span className="badge">R1 / REVIEW REQUIRED</span></header><section className="workspace"><div className="viewport"><Boundary><Suspense fallback={<div className="loading">Loading the actual rig asset…</div>}><Canvas camera={{position:[0,1,4],fov:38}} onCreated={({camera:c})=>{camera.current=c as THREE.PerspectiveCamera;}}><color attach="background" args={[style==='Clean'?'#e9ecef':'#20262c']}/><ambientLight intensity={style==='Clean'?1.7:0.7}/><directionalLight position={[3,5,5]} intensity={2.5}/><directionalLight position={[-3,2,-3]} intensity={1.4}/><Bounds fit clip observe margin={1.2}><Model clip={clip} playing={playing} loop={loop} time={time} seekVersion={seekVersion} style={style} onInventory={setInventory} onTime={setLiveTime} onPick={setPicked} onPlaying={setPlaying}/></Bounds><OrbitControls ref={controls} makeDefault/></Canvas></Suspense></Boundary><div className="views">{['Front','Side','Back'].map(v=><button key={v} aria-pressed={view===v} onClick={()=>setView(v)}>{v}</button>)}</div></div><aside><h2>Actual asset</h2><code>{ASSET}</code><dl><dt>Source muscle identities</dt><dd data-testid="identity-count">{inventory?.identities.length??'Loading'}</dd><dt>Skinned meshes / bones</dt><dd>{inventory?`${inventory.skinned} / ${inventory.bones}`:'—'}</dd><dt>Embedded clips</dt><dd>{inventory?.clips.length??'—'}</dd></dl><p className="note">Clean and Real use the same source geometry. Lighting and surface response change; this is not a claim of anatomical deformation fidelity.</p><label>Animation<select aria-label="Animation" value={clip} onChange={e=>{setClip(e.target.value);setTime(0);setPlaying(false);}}><option value="">Rest pose</option>{inventory?.clips.map(c=><option key={c.name} value={c.name}>{c.name}</option>)}</select></label><div className="row"><button disabled={!clip} onClick={()=>setPlaying(v=>!v)}>{playing?'Pause':'Play'}</button><button onClick={()=>{setPlaying(false);setTime(0);setClip('');}}>Rest</button><label className="inline"><input type="checkbox" checked={loop} onChange={e=>setLoop(e.target.checked)}/>Loop</label></div><label>Seek<input aria-label="Seek" type="range" min="0" max={duration||1} step="0.001" value={Math.min(liveTime,duration)} disabled={!clip} onInput={e=>{setPlaying(false);setTime(Number(e.currentTarget.value));setSeekVersion(v=>v+1);}}/></label><output data-testid="clip-time">{liveTime.toFixed(3)} / {duration.toFixed(3)} s</output><div className="row styles">{['Clean','Real'].map(s=><button key={s} aria-pressed={style===s} onClick={()=>setStyle(s)}>{s}</button>)}</div><h2>Picked source muscle</h2><p className="note">Click the visible mesh to inspect its actual embedded identity.</p>{picked?<div data-testid="picked-muscle"><strong>{picked.name}</strong><p>Stable ID: <code>{picked.id}</code></p><details><summary>Node extras</summary><pre>{JSON.stringify(picked.extras,null,2)}</pre></details></div>:<p data-testid="picked-muscle">No muscle selected</p>}<details><summary>Identity catalogue ({inventory?.identities.length??0})</summary><ul>{inventory?.identities.map(i=><li key={i.id}><button onClick={()=>setPicked(i)}>{i.id} · {i.name}</button></li>)}</ul></details></aside></section></main>;
}
createRoot(document.getElementById('rig-v2-root')!).render(<App/>);
