/** P2: reuse PR#21 30 finger bones; reach official pulldown grips; measure tissue vs skeletal wrap. */
import {readFileSync, writeFileSync, mkdirSync} from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createRequire} from 'node:module';
import {officialBarTargets} from '../../src/grasp-v1/officialBar.mjs';
import {poseFor, applyToObject3D} from '../../src/grasp-v1/controller.mjs';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const config = JSON.parse(readFileSync(path.join(root, 'src/data/pulldown-config.json'), 'utf8'));
function latPulldownFrame(progress) {
  const p = Math.min(1, Math.max(0, progress));
  const phase = (1 - Math.cos(2 * Math.PI * p)) / 2;
  const barY = config.barTopY - config.barTravel * phase;
  return {
    phase, barY,
    leftGrip: [-config.gripHalfWidth, barY - config.gripDrop, config.gripZ],
    rightGrip: [config.gripHalfWidth, barY - config.gripDrop, config.gripZ],
  };
}

const out = path.join(root, process.env.GRASP_SEQUENCE_OUTPUT || 'artifacts/grasp-v1/p3-basis/official-sequence');
mkdirSync(out, {recursive: false});
const require = createRequire(import.meta.url);
const THREE = require('three');
const {GLTFLoader} = require('three/examples/jsm/loaders/GLTFLoader.js');

const glb = readFileSync(path.join(root, process.env.GRASP_ASSET || 'artifacts/grasp-v1/grasp-controller.glb'));
const loader = new GLTFLoader();
const gltf = await new Promise((res, rej) => loader.parse(
  glb.buffer.slice(glb.byteOffset, glb.byteOffset + glb.byteLength), '', res, rej,
));

const HAND_RE = /hand|pollicis|lumbrical|interosse|digiti minimi|retinaculum/i;
const SKIP_RE = /foot|halluc|plantar| of left leg| of right leg/i;
const meshes = [];
gltf.scene.traverse((o) => {
  const name = `${o.userData.sourceName || ''} ${o.name}`;
  if (o.isSkinnedMesh && HAND_RE.test(name) && !SKIP_RE.test(name)) meshes.push(o);
});

function bone(name) {
  const b = gltf.scene.getObjectByName(name);
  if (!b) throw new Error('missing bone ' + name);
  return b;
}

function ccd(chain, effectorName, target, iterations = 16) {
  const effector = bone(effectorName);
  for (let n = 0; n < iterations; n++) {
    for (const name of [...chain].reverse()) {
      const b = bone(name);
      gltf.scene.updateMatrixWorld(true);
      const origin = b.getWorldPosition(new THREE.Vector3());
      const toEff = effector.getWorldPosition(new THREE.Vector3()).sub(origin);
      const toTgt = target.clone().sub(origin);
      if (toEff.lengthSq() < 1e-10 || toTgt.lengthSq() < 1e-10) continue;
      const q = new THREE.Quaternion().setFromUnitVectors(toEff.normalize(), toTgt.normalize());
      const parent = b.parent;
      const parentQ = parent.getWorldQuaternion(new THREE.Quaternion());
      const worldQ = b.getWorldQuaternion(new THREE.Quaternion()).premultiply(q);
      b.quaternion.copy(parentQ.clone().invert().multiply(worldQ));
    }
  }
  gltf.scene.updateMatrixWorld(true);
}

function cylSigned(p, origin, axis, radius, half) {
  const rel = p.clone().sub(origin);
  const t = rel.dot(axis);
  const axial = Math.abs(t) - half;
  const radial = rel.clone().addScaledVector(axis, -t).length() - radius;
  if (axial <= 0 && radial <= 0) return Math.max(radial, axial);
  if (axial <= 0) return radial;
  if (radial <= 0) return axial;
  return Math.hypot(radial, axial);
}

function measureTissue(origin, axis, radius, half, side) {
  const v = new THREE.Vector3();
  let minS = Infinity;
  let inside = 0;
  let tested = 0;
  for (const m of meshes.filter(m=>ownership.get(m)===side)) {
    m.skeleton.update();
    const idx = m.geometry.index;
    const count = idx ? idx.count : m.geometry.attributes.position.count;
    const at = (i) => (idx ? idx.getX(i) : i);
    for (let i = 0; i < count; i += 3) {
      for (const k of [0, 1, 2]) {
        m.getVertexPosition(at(i + k), v).applyMatrix4(m.matrixWorld);
        const s = cylSigned(v, origin, axis, radius, half);
        tested += 1;
        if (s < minS) minS = s;
        if (s <= 0) inside += 1;
      }
    }
  }
  return {minSignedM: Number.isFinite(minS) ? minS : null, insideSamples: inside, tested};
}

function measureBones(origin, axis, radius, half) {
  const tips = [];
  for (const side of ['Left', 'Right']) {
    for (const name of [`${side}IndexDIP`, `${side}MiddleDIP`, `${side}RingDIP`, `${side}LittleDIP`, `${side}ThumbIP`, `${side}Hand`]) {
      const b = gltf.scene.getObjectByName(name);
      if (!b) continue;
      const p = b.getWorldPosition(new THREE.Vector3());
      tips.push({name, signedM: cylSigned(p, origin, axis, radius, half), point: p.toArray()});
    }
  }
  const occupied = new Set();
  const n1 = new THREE.Vector3(0, 1, 0);
  if (Math.abs(axis.dot(n1)) > 0.9) n1.set(0, 0, 1);
  const u = n1.clone().addScaledVector(axis, -n1.dot(axis)).normalize();
  const w = axis.clone().cross(u);
  for (const t of tips) {
    if (t.signedM > 0.03) continue;
    const p = new THREE.Vector3().fromArray(t.point);
    const rel = p.clone().sub(origin).addScaledVector(axis, -p.clone().sub(origin).dot(axis));
    const ang = Math.atan2(rel.dot(w), rel.dot(u));
    occupied.add(Math.floor(((ang + Math.PI) / (2 * Math.PI)) * 8) % 8);
  }
  return {
    tips,
    wrapOccupied: occupied.size,
    skeletalWrap: occupied.size >= 4 && tips.every((t) => t.name.includes('Hand') || t.signedM > -0.002),
  };
}

const RADIUS = 0.024;
const phases = Array.from({length:121},(_,i)=>i/120);
gltf.scene.updateMatrixWorld(true);const handReferenceX=Object.fromEntries(['Left','Right'].map(s=>[s,bone(s+'Hand').getWorldPosition(new THREE.Vector3()).x]));const referenceRotations=new Map();gltf.scene.traverse(o=>{if(o.isBone)referenceRotations.set(o.name,o.quaternion.clone());});const ownership=new Map(meshes.map(m=>{let left=0,right=0;const si=m.geometry.attributes.skinIndex,sw=m.geometry.attributes.skinWeight;for(let i=0;i<si.count;i++)for(let k=0;k<4;k++){const n=m.skeleton.bones[si.array[i*4+k]].name,w=sw.array[i*4+k];if(n.startsWith('Left'))left+=w;if(n.startsWith('Right'))right+=w;}return[m,left>right?'Left':right>left?'Right':null];}));
const report = {handReferenceX,poseSamples:121,qualityScope:'Inherited unconstrained CCD reach, corrected reference-relative finger driver, same-side actual angled grip segments. Not anatomical or skeletal-grasp PASS.',
  inherit: 'PR#21 30 additive finger bones + poseFor/applyToObject3D',
  barRadiusM: RADIUS,
  note: 'Official pulldown-config grips. Isolated reach via CCD on existing 27-bone arm chain. Not a whole-body weight write. G2 rest-height PERSISTENT_INTERSECTION is not reused as success.',
  phases: [],
};

const leftChain = ['LeftClavicle', 'LeftScapula', 'LeftHumerus', 'LeftForearm', 'LeftWrist'];
const rightChain = ['RightClavicle', 'RightScapula', 'RightHumerus', 'RightForearm', 'RightWrist'];

for (const progress of phases) {
  for(const [n,q] of referenceRotations)bone(n).quaternion.copy(q);gltf.scene.updateMatrixWorld(true);
  const frame = latPulldownFrame(progress),segments=officialBarTargets(config,progress,handReferenceX);
  const leftT = new THREE.Vector3(...segments.Left.target);
  const rightT = new THREE.Vector3(...segments.Right.target);
  ccd(leftChain, 'LeftHand', leftT);
  ccd(rightChain, 'RightHand', rightT);
  const hit = applyToObject3D(gltf.scene, {...poseFor('pulldown-bar', 'Left'), ...poseFor('pulldown-bar', 'Right')});
  gltf.scene.updateMatrixWorld(true);
  for (const m of meshes) m.skeleton.update();
  const origin = leftT.clone().add(rightT).multiplyScalar(0.5);
  const axis = rightT.clone().sub(leftT);
  const half = axis.length() * 0.5 + 0.04;
  axis.normalize();
  const leftErr = bone('LeftHand').getWorldPosition(new THREE.Vector3()).distanceTo(leftT);
  const rightErr = bone('RightHand').getWorldPosition(new THREE.Vector3()).distanceTo(rightT);
  const byHand=['Left','Right'].map(side=>{const s=segments[side],a=new THREE.Vector3(...s.from),b=new THREE.Vector3(...s.to),mid=a.clone().add(b).multiplyScalar(.5),ax=b.clone().sub(a);const half=ax.length()/2;ax.normalize();return{side,segment:s,tissue:measureTissue(mid,ax,RADIUS*Math.cos(Math.PI/12),half,side)};});
  const tissue = {minSignedM:Math.min(...byHand.map(x=>x.tissue.minSignedM)),byHand,method:'Conservative inscribed finite12gon cylinder vertex witnesses, not exact penetration depth. Missing vertex witnesses are INCONCLUSIVE, not PASS.'};
  const skeletal = measureBones(origin, axis, RADIUS, half);
  report.phases.push({
    progress,
    barY: frame.barY,
    fingerHits: hit,
    leftReachErrorM: leftErr,
    rightReachErrorM: rightErr,
    tissue,
    skeletal,
    tissueVerdict: tissue.minSignedM != null && tissue.minSignedM <= 0 ? 'TISSUE_INTERSECTION' : 'TISSUE_GAP',
    skeletalVerdict: 'INCONCLUSIVE_BONE_TIP_BINS_ARE_NOT_GRASP',
    boneWorldMatrices:Object.fromEntries([...referenceRotations.keys()].map(n=>[n,bone(n).matrixWorld.toArray()])),
  });
}

const anyTissueHit = report.phases.some((p) => p.tissueVerdict === 'TISSUE_INTERSECTION');
report.overall = {scope:'121 reach/contact samples, not accepted human motion; skinless source topology and unvalidated digit placements retained',
  tissue: anyTissueHit ? 'FAIL_TISSUE_GRASP' : 'GAP_ONLY',
  skeletal: report.phases.every((p) => p.skeletalVerdict === 'SKELETAL_WRAP_CANDIDATE') ? 'SKELETAL_WRAP_ALONG_TRAJECTORY' : 'SKELETAL_INCOMPLETE',
  historicalPulldownFailUnchanged: true,
  g2PersistentIntersectionNotSuccess: true,
};
writeFileSync(path.join(out, 'official-bar-align.json'), JSON.stringify(report, null, 2));
console.log(JSON.stringify({
  phases: report.phases.map((p) => ({
    progress: p.progress,
    reach: [p.leftReachErrorM.toFixed(3), p.rightReachErrorM.toFixed(3)],
    tissue: p.tissue.minSignedM,
    wrap: p.skeletal.wrapOccupied,
    tv: p.tissueVerdict,
    sv: p.skeletalVerdict,
  })),
  overall: report.overall,
}, null, 2));
