import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
import {PRESETS, poseFor, applyToObject3D, cyclePose} from './controller.mjs';

const hud = document.getElementById('hud');
const stage = document.getElementById('stage');
const renderer = new THREE.WebGLRenderer({antialias: true, preserveDrawingBuffer: true});
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
renderer.setClearColor(0x10171e);
stage.append(renderer.domElement);

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(40, 1, 0.01, 20);
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
scene.add(new THREE.HemisphereLight(0xe7f1ff, 0x27313b, 1.6));
const key = new THREE.DirectionalLight(0xffffff, 2.2);
key.position.set(0.4, 0.8, 0.5);
scene.add(key);

const HAND_RE = /hand|pollicis|lumbrical|interosse|digiti minimi|retinaculum|finger/i;
const SKIP_RE = /foot|halluc|plantar| of left leg| of right leg/i;
const gltf = await new GLTFLoader().loadAsync('/artifacts/grasp-v1/grasp-controller.glb');
scene.add(gltf.scene);

const bones = [];
const handMeshes = [];
const otherMeshes = [];
gltf.scene.traverse((o) => {
  if (o.isBone) bones.push(o);
  if (o.isMesh) {
    const name = `${o.userData.sourceName || ''} ${o.name}`;
    ((HAND_RE.test(name) && !SKIP_RE.test(name)) ? handMeshes : otherMeshes).push(o);
  }
});

let barFixture = null;
try {
  barFixture = await (await fetch('/artifacts/grasp-v1/g2/bar-fixture.json')).json();
} catch {
  barFixture = {origin: [0, 0.76, 0.14], axis: [1, 0, 0], radiusM: 0.024, halfLengthM: 0.18};
}
const barSpace = barFixture.gltfYup || barFixture;
const barGeom = new THREE.CylinderGeometry(barFixture.radiusM, barFixture.radiusM, barFixture.halfLengthM * 2, 24);
const bar = new THREE.Mesh(barGeom, new THREE.MeshStandardMaterial({color: 0x2a3036, roughness: 0.4, metalness: 0.2}));
const axis = new THREE.Vector3(...barSpace.axis).normalize();
bar.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), axis);
bar.position.fromArray(barSpace.origin);
scene.add(bar);

const left = {curl: 0, thumb: 0, spread: 0.25};
const right = {curl: 0, thumb: 0, spread: 0.25};
const state = {playing: false, loop: true, t: 0, camera: 'left-palm'};

function poseFromParams(side, p) {
  const sign = side === 'Left' ? 1 : -1;
  const out = {};
  const digits = ['Thumb', 'Index', 'Middle', 'Ring', 'Little'];
  const chain = {Thumb: ['CMC', 'MCP', 'IP'], Index: ['MCP', 'PIP', 'DIP'], Middle: ['MCP', 'PIP', 'DIP'], Ring: ['MCP', 'PIP', 'DIP'], Little: ['MCP', 'PIP', 'DIP']};
  const flex = {CMC: 0.35, MCP: 1.15, PIP: 1.25, DIP: 0.85, IP: 1.05};
  digits.forEach((digit, di) => {
    const spread = (di - 2) * 0.12 * p.spread;
    const curl = digit === 'Thumb' ? p.thumb : p.curl;
    chain[digit].forEach((joint) => {
      const opp = digit === 'Thumb' && joint === 'CMC' ? 0.55 * p.thumb : 0;
      out[`${side}${digit}${joint}`] = {x: flex[joint] * curl, y: opp * sign, z: spread * sign};
    });
  });
  return out;
}

function applyHands() {
  applyToObject3D(gltf.scene, {...poseFromParams('Left', left), ...poseFromParams('Right', right)});
  gltf.scene.updateMatrixWorld(true);
  for (const m of handMeshes) if (m.isSkinnedMesh) m.skeleton.update();
}

function setSlider(id, value) {
  const el = document.getElementById(id);
  el.value = String(value);
  el.parentElement.querySelector('span').textContent = Number(value).toFixed(2);
}

function syncSliders() {
  setSlider('L-curl', left.curl); setSlider('L-thumb', left.thumb); setSlider('L-spread', left.spread);
  setSlider('R-curl', right.curl); setSlider('R-thumb', right.thumb); setSlider('R-spread', right.spread);
}

function applyPreset(name) {
  const p = PRESETS[name];
  Object.assign(left, p);
  Object.assign(right, p);
  syncSliders();
  state.playing = false;
  applyHands();
}

function applyCycle(t) {
  state.t = t;
  const L = cyclePose('Left', t);
  const R = cyclePose('Right', t);
  applyToObject3D(gltf.scene, {...L, ...R});
  const u = t <= 0.5 ? t * 2 : (1 - t) * 2;
  left.curl = u; left.thumb = 0.85 * u; left.spread = 0.25 * (1 - u);
  right.curl = u; right.thumb = 0.85 * u; right.spread = 0.25 * (1 - u);
  syncSliders();
  document.getElementById('scrub').value = String(t);
  document.getElementById('scrubVal').textContent = t.toFixed(2);
  gltf.scene.updateMatrixWorld(true);
  for (const m of handMeshes) if (m.isSkinnedMesh) m.skeleton.update();
}

function bonePos(name) {
  const b = gltf.scene.getObjectByName(name);
  return b ? b.getWorldPosition(new THREE.Vector3()) : new THREE.Vector3();
}

function setCamera(name) {
  state.camera = name;
  const leftH = bonePos('LeftHand');
  const rightH = bonePos('RightHand');
  let target = leftH;
  let offset = new THREE.Vector3(0.05, 0.07, 0.20);
  if (name === 'right-palm') { target = rightH; offset = new THREE.Vector3(-0.05, 0.07, 0.20); }
  if (name === 'left-digits') { target = leftH; offset = new THREE.Vector3(0.04, -0.08, 0.14); }
  if (name === 'right-digits') { target = rightH; offset = new THREE.Vector3(-0.04, -0.08, 0.14); }
  if (name === 'bar') { target = new THREE.Vector3().fromArray(barSpace.origin); offset = new THREE.Vector3(0, 0.08, 0.28); }
  camera.position.copy(target).add(offset);
  controls.target.copy(target);
  controls.update();
}

function resize() {
  const w = stage.clientWidth, h = stage.clientHeight;
  renderer.setSize(w, h, false);
  camera.aspect = w / Math.max(h, 1);
  camera.updateProjectionMatrix();
}
addEventListener('resize', resize);
resize();

const presetBox = document.getElementById('presets');
for (const name of Object.keys(PRESETS)) {
  const b = document.createElement('button');
  b.textContent = name;
  b.addEventListener('click', () => applyPreset(name));
  presetBox.append(b);
}
for (const [side, bag] of [['L', left], ['R', right]]) {
  for (const key of ['curl', 'thumb', 'spread']) {
    document.getElementById(`${side}-${key}`).addEventListener('input', (e) => {
      bag[key] = Number(e.target.value);
      e.target.parentElement.querySelector('span').textContent = bag[key].toFixed(2);
      state.playing = false;
      applyHands();
    });
  }
}
document.getElementById('play').addEventListener('click', () => { state.playing = true; });
document.getElementById('pause').addEventListener('click', () => { state.playing = false; });
document.getElementById('loop').addEventListener('click', (e) => {
  state.loop = !state.loop;
  e.target.textContent = state.loop ? 'Loop on' : 'Loop off';
});
document.getElementById('scrub').addEventListener('input', (e) => {
  state.playing = false;
  applyCycle(Number(e.target.value));
});
for (const btn of document.querySelectorAll('[data-cam]')) {
  btn.addEventListener('click', () => setCamera(btn.dataset.cam));
}
document.getElementById('handsOnly').addEventListener('change', (e) => {
  for (const m of otherMeshes) m.visible = !e.target.checked;
});
document.getElementById('showBar').addEventListener('change', (e) => { bar.visible = e.target.checked; });
for (const m of otherMeshes) m.visible = false;

applyPreset('open');
setCamera('left-palm');
hud.textContent = `bones ${bones.length} · hand meshes ${handMeshes.length} · isolated G2 panel`;

let last = performance.now();
function tick(now) {
  const dt = Math.min((now - last) / 1000, 0.05);
  last = now;
  if (state.playing) {
    state.t += dt / 2.4;
    if (state.t >= 1) {
      if (state.loop) state.t = 0;
      else { state.t = 1; state.playing = false; }
    }
    applyCycle(state.t);
  }
  controls.update();
  renderer.render(scene, camera);
  requestAnimationFrame(tick);
}
requestAnimationFrame(tick);

window.__grasp = {
  applyPreset,
  applyCycle,
  applyHands,
  setCamera,
  play() { state.playing = true; },
  pause() { state.playing = false; },
  seek(t) { state.playing = false; applyCycle(t); },
  state() { return {...state, left: {...left}, right: {...right}, bones: bones.length, handMeshes: handMeshes.length}; },
  renderer,
};
