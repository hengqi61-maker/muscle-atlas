# Muscle Atlas
Local-first personal 3D anatomy and training console, macOS first.

## Start
Node22+ and Python3 for asset tools.
```sh
npm ci
python3 scripts/fetch-models.py --offline
npm run dev
```
Open http://127.0.0.1:5173. No registration, server or Calendar authorization needed.

Explore mode shows the original static anatomy. Exercise mode now loads **actual anatomical meshes with a left-arm two-bone skin and baked biceps morphs**, replacing the ellipsoid prototype. It supports playback, pause, speed, scrubbing,0°/45°/90°/120° checks and independent biceps morph control. The rest of the body remains static. Shape weights are artistic interpolation, not physiological activation. High-flexion elbow pinching and an unposed gripping hand remain documented limitations.

Training records are entered by you, saved in IndexedDB and exportable as JSON. Use a stable localhost port/profile; export before clearing browser storage. Plan editing, backup import, heatmaps and Calendar integration remain future work.

## Verify
```sh
npm run build
npm test
npm run test:assets
npm run test:rig
npm run test:e2e
```
Browser checks use locally installed Google Chrome. `test:rig` runs Khronos glTF Validator and actual Three.js AnimationMixer/SkinnedMesh checks; it writes evidence into docs/evidence.

## Rebuild derived animation
```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --python scripts/build-curl-rig.py
npm run test:rig
```
Produces public/models/anatomy-curl.glb and ignored artifacts/curl-rig.blend. Raw source SHA256 is pinned before transformations. No network is needed when source assets are present. `python3 scripts/fetch-models.py` verifies cache first; use `--offline` to prohibit requests.

See [current rig evidence](docs/rig-verification.md), [download diagnostics](docs/download-diagnostics.md), [roadmap](docs/roadmap.md) and [asset terms](docs/assets-and-licenses.md). Historical first-delivery screenshots/docs describe the superseded procedural prototype and are retained as evidence.
