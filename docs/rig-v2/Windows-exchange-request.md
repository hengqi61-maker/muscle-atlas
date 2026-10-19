# Mac→Windows W2 exchange request · 2026-10-16

Common baseline:0914d4fad3fbe107ea90c08473b6d2a448345ba6. Macbranch codex/unified-rig-v2; Windowsbranch requestedcodex/opensim-biomechanics. GitHub is the sole formal code/data handoff; neither side edits the other side's anatomy assets. Historical M2 FAIL and two-cycle limit remain unchanged.

## Actual Mac observations available now

`exports/legacy-observations.json` is an audited raw observation, NOT the agreed final interchange schema. Reproduce from repo root: `node docs/rig-v2/exports/inspect-legacy.mjs`. It describes actual source/curl/pulldownGLBs, hashes, jointnames/parents, local/world matrices and quaternion/basis values, inversebind data, channels and weights. Blender generators are scripts/build-curl-rig.py and scripts/build-pulldown-rig.py. No clavicle exists in either legacy rig. Curl has2joints; pulldown16joints. Source contains467meshes, no native skin.

Matrix arrays from Three/glTF are column-major, column-vector affine transforms. Numeric default-node pose, inverse-bind-derived bind frame and animationtime0 must remain separately identified; none is automatically a calibrated anatomical reference. Rotations are storedXYZW when noted; they are not OpenSim coordinate values. Source model scale, Blender normalization, glTF basis conversion and display1.45scale must be distinguished. Audit report will identify uncertainties rather than silently assign anatomical axes.

## Windows-owned W2 request

Please publish a versioned JSON schema and executable fixtures on your separate branch/ DraftPR early. Include model/source hashes, units/handedness/worldaxes, referencepose, segment andjoint mapping, parent hierarchy, local/worldtransform semantics, timestamps, rotationstorage and active/passive convention, evidence/confidence and uncertainty. Preserve .osim/.mot/.sto provenance. Do not call a mirrored left arm independently validated.

Need explicit mapping method `T_target = A T_source B` (or your equivalent), reference offset and direction. Tests: axis/basis vectors, metre/mm conversion, non-commuting90deg rotations, transform roundtrip, determinant+1/no accidentalreflection, zero/referencepose alignment, one-sidedmodel coverage flags, absent/mismatched joints rejected. Do not directly copy Euler angles between OpenSim and Blender.

Questions: which real licensed model loads; which clavicle/scapula/humerus DOFs exist; what bony frames/attachment sites are actually supplied; how shoulder-centre/segment-length differences are calibrated; which trajectories are measured vs model-testpostures vs assumptions; what original-hand/finger data are absent. Muscle-surface collision remains Mac's actual geometry responsibility.

Mac is building an isolated canonical pelvis/spine/thorax/clavicle/scapula/arm/wrist/hand+legs skeleton and two diagnosticclips, with finger interfaces only. We will export its actual reference matrices and sampled shoulder poses, then implement Blender read/write adapters against the Windows-owned agreed schema. Until schema is supplied and bilateral fixtures pass, interchange integration is INCONCLUSIVE—not a medical validation or approved migration. Formal production GLBs remain unchanged.
