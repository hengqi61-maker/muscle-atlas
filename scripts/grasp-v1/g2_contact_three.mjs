import {readFileSync, writeFileSync} from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createRequire} from 'node:module';
import {poseFor, applyToObject3D, cyclePose} from '../../src/grasp-v1/controller.mjs';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const require = createRequire(import.meta.url);
const THREE = require('three');
const {GLTFLoader} = require('three/examples/jsm/loaders/GLTFLoader.js');

const glb = readFileSync(path.join(root, 'artifacts/grasp-v1/grasp-controller.glb'));
const bar = JSON.parse(readFileSync(path.join(root, 'artifacts/grasp-v1/g2/bar-fixture.json'), 'utf8'));
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

const origin = new THREE.Vector3(...(bar.gltfYup?.origin || bar.origin));
const axis = new THREE.Vector3(...(bar.gltfYup?.axis || bar.axis)).normalize();
const radius = bar.radiusM;
const half = bar.halfLengthM;

function cylSigned(p) {
  const rel = p.clone().sub(origin);
  const t = rel.dot(axis);
  const axial = Math.abs(t) - half;
  const radial = rel.clone().addScaledVector(axis, -t).length() - radius;
  if (axial <= 0 && radial <= 0) return Math.max(radial, axial);
  if (axial <= 0) return radial;
  if (radial <= 0) return axial;
  return Math.hypot(radial, axial);
}

function poseScene(pose) {
  applyToObject3D(gltf.scene, pose);
  gltf.scene.updateMatrixWorld(true);
  for (const m of meshes) m.skeleton.update();
}

function measure() {
  const v = new THREE.Vector3();
  let minS = Infinity;
  let inside = 0;
  let tested = 0;
  const byMesh = [];
  for (const m of meshes) {
    const idx = m.geometry.index;
    const count = idx ? idx.count : m.geometry.attributes.position.count;
    const at = (i) => (idx ? idx.getX(i) : i);
    let localMin = Infinity;
    let localIn = 0;
    for (let i = 0; i < count; i += 3) {
      const pts = [0, 1, 2].map((k) => {
        const p = new THREE.Vector3();
        m.getVertexPosition(at(i + k), p);
        return p;
      });
      const samples = [...pts, pts[0].clone().add(pts[1]).add(pts[2]).multiplyScalar(1 / 3)];
      for (const p of samples) {
        const s = cylSigned(p);
        tested += 1;
        if (s < minS) minS = s;
        if (s < localMin) localMin = s;
        if (s <= 0) { inside += 1; localIn += 1; }
      }
    }
    byMesh.push({
      name: m.userData.sourceName || m.name,
      minSignedM: Number.isFinite(localMin) ? localMin : null,
      insideSamples: localIn,
    });
  }
  return {minSignedM: Number.isFinite(minS) ? minS : null, insideSamples: inside, tested, meshes: byMesh};
}

const presets = ['open', 'half', 'closed', 'pulldown-bar'];
const report = {engine: 'three@0.180 skinned boneTransform triangles', bar, presets: {}, cycle: []};
for (const name of presets) {
  poseScene({...poseFor(name, 'Left'), ...poseFor(name, 'Right')});
  report.presets[name] = measure();
}
for (const t of [0, 0.25, 0.5, 0.75, 1]) {
  poseScene({...cyclePose('Left', t), ...cyclePose('Right', t)});
  report.cycle.push({t, ...measure()});
}
const out = path.join(root, 'artifacts/grasp-v1/g2/three-posed-contact.json');
writeFileSync(out, JSON.stringify(report, null, 2));
console.log(JSON.stringify({
  status: 'PASS_MEASURE',
  meshes: meshes.length,
  open: report.presets.open.minSignedM,
  closed: report.presets.closed.minSignedM,
  pulldown: report.presets['pulldown-bar'].minSignedM,
}, null, 2));
