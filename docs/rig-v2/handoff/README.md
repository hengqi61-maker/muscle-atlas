# Initial Mac observation handoff v0.1

This is a versioned **initial Mac producer observation format**, not the agreed Windows exchange standard. Windows owns the final schema and adapter contract. The JSON contains observations of the committed GLB, not invented sample motion, anatomical joint angles, or an OpenSim validation result.

Asset commit: `b904b4b200fc838cb7fabbf4ed2ef346faa73b53`.
GLB SHA-256: `ef803a4bbb3c644504c124519e39ba0b3b760ec139eaf60d277ef7f7f5d23274`.
Source: `public/experimental/rig-v2/unified-rig-prototype.glb`. The JSON also records the canonical configuration SHA. Source model provenance/license remains in the source asset documentation; this handoff does not grant a new model license.

Run from repository root with installed package dependencies:

```sh
node scripts/rig-v2/export-handoff.mjs
node --test tests/rig-v2/handoff.node.mjs
```

The exporter uses Three.js GLTFLoader and AnimationMixer. `reference` records default glTF node transforms before animation evaluation. `skins` records actual inverse bind matrices independently; default reference is not silently substituted for bind pose. `bones` preserves traversal/topological order and actual node and bone parent names. Each clip has 121 inclusive samples at `duration * index / 120`; fixed phases 0/25/50/75/100 percent correspond to indices 0/30/60/90/120. The endpoint is evaluated with LoopOnce and clampWhenFinished. These are **authored diagnostic trajectories**, not measured human motion or validated physiological ranges.

All glTF matrices are flat column-major arrays acting on column vectors; `world = parentWorld * local`. Translations are metres, up is +Y, quaternions are xyzw, handedness is right. Local and world affine transforms and quaternions are exported at every frame. `parentWorldMatrix` includes non-bone parent transforms, including the armature/root conversion. Matrix columns 0..2 provide actual numeric local basis vectors in the parent frame; world columns provide basis vectors in the scene frame. They are not calibrated anatomical axes. No Euler sequence or OpenSim joint-coordinate interpretation is asserted.

`blenderReference` embeds the separately sourced canonical configuration, including actual rest matrices and heads/tails. `attachmentRegistry` separately embeds the actual committed attachment registry. Its nested row-major matrices use Blender Z-up/right-handed coordinates, local +Y longitudinal bone convention, and metres. Do not reinterpret these nested rows as glTF column-major storage. Z-up to Y-up basis conversion uses the proper rotation Rx(-pi/2); transform conversion requires conjugation `C T C^-1`, with translations scaled separately for millimetres. Local Blender rest bases remain uncalibrated geometry estimates.

Tests check exact source hash and deterministic regeneration, hierarchy order, finite samples, quaternion norms, proper rotation determinants for both sides, parent/world multiplication, unit conversion, basis conjugation round trip and noncommuting rotation fixtures. These are mathematical and serialization checks. No external OpenSim data is available; no adapter is claimed validated.

Questions for the Windows owner:

- Which final schema/version, naming map, root frame and bind/reference semantics should be adopted?
- Which anatomical axis calibration, Euler sequence and sign conventions will the OpenSim adapter require?
- Which independently sourced reference datasets and numerical tolerances will establish adapter validity?
- Should transport retain dense affine samples or select quaternions plus translations and explicit scale?

The schema draft describes this producer output only. It is deliberately not branded a Windows standard. This package is experimental and does not replace the production asset.
