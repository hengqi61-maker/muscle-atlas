# Phase2 controlled experiments: no repair candidate accepted

Baseline PR8 `1b06bf4`; immutable source R1 GLB `ef803a4bbb3c644504c124519e39ba0b3b760ec139eaf60d277ef7f7f5d23274`. Source467/canonical27/two diagnostic clips121poses unchanged. These are authored diagnostic motions, not normative training trajectories. No production GLB, original hand posture, frozen report, Windows file or main changed.

## Actual measurements

| Candidate | Curl severe poses | Pulldown severe poses | Pulldown maximum edge ratio | Decision |
|---|---:|---:|---:|---|
| Frozen baseline, freshly reproduced |39|91|3.9884383355|FAIL|
| E01 local22-exported-vertex weight smooth, lambda0.5 |39|91|6.4698000415|FAIL; new seam regression|
| E02 Forearm basis-axis direction to localX, alpha1 |39|93|3.9884383355|FAIL; held-out regression|

Every actual exported triangle (1,092,000) at121inclusive times per clip was measured, with original area<.05, mesh count>3 OR fraction>.01, edge>2 thresholds. Reports preserve local triangle IDs, weight/vertex evidence, first failure, left/right results and exact new/removed mesh-poses. Old Phase1 sampled42/121 record is not overwritten. These gates are engineering screens, not medical tissue-strain limits.

E01 modifies only the specified right-subscapularis WEIGHTS accessor; geometry/topology/bind/animations remain byte-identical. Baseline peak BP4795/FMA13414 triangle914 edge456–466 length1.190418797mm becomes4.747911965mm with humeral weight difference0.017621696. Isolated two-point calculations identify gradient×bone differential motion, not anatomical attachment. Full topological smoothing did not remove the target gradient, moved distortion elsewhere, and split11 originally equivalent groups/19 point pairs. Pair441/1288 separates3.179553mm in Pulldownframe0 versus baseline0. The new `seam-check.mjs` rejects it with exit1; original area/edge tests alone do not detect every seam.

E02 changes only four Forearm rotation accessors. Actual inverse-bind reference removal/recomposition keeps basis angles within float32 error (~7.6e-8rad) while changing axis4.69869degrees. Bone localX is uncalibrated. Curl brachioradialis maximum compressed triangles24→14, but biceps long head5→6 and first severe54→51; Curl has21 new/6 removed severe mesh-poses. Pulldown has12 new/0 removed. Actual GLTFLoader wrist position changes atframe60 are up to24.76703mm Curl/21.69937mm Pulldown. This does not preserve grip or apparatus paths. Raw121 trajectories and source/candidate positions are in `trajectory-comparison.json`.

Both derivations were repeated in fresh directories and produced exact same bytes: E01 `f7324b003425ae08310ba00e20f303b59734287121eca539ce79dc66edc8b6c1`; E02 `d60a589aff96eea65fe84da64f288af231e95b3b278fcb428c1c6fb0747bf55d`. An early E02 mistaken whole-local-quaternion experiment is preserved INVALID, excluded from scans, and fixed by independent inverse-bind/basis verification before candidate execution.

## Actual visual evidence

Three actual Chrome/GLTFLoader consumers each completed two clips,242poses,100screenshots, full-cycle WebM, pause/pick checks. Native Blender5.2 builds each generated122PNGs, two121-pose joint trajectories, native Blend and two H264512x512/31frame/4.133s videos: baseline71.59s, E01 58.54s, E02 79.23s. This is measured workload time, not controlled rendering/FPS benchmarking.

The original GLB has467meshes. Blender importer creates an Icosphere custom_shape used by27bones in its glTF_not_exported collection (importer-default hidden); this is not an extra source asset or a mesh hidden by the experiment. All467 source objects remain visible. Shared conservative full-cycle camera contract includes that helper's bounds, causing spare whitespace; smoke images and independent true-vertex projection demonstrate no clipping. No third-party hand shell or source-finger fold was introduced.

All native sets use fixed8samples/512px Clean diagnostic material. Gross deformation is visible; bright/noisy micro-detail is INCONCLUSIVE. Initial64-sample partial output and old-framing output are preserved. Different concurrent CPU/GPU loads mean no sample-count-only speed attribution. E01 has110/122pixel-identical images with baseline; the remaining12 differ at most6pixels/channel difference4, and both compressed videos match exactly. Deep-source geometry is largely occluded, so wholebody video is not a test for subscapularis repair. Isolated real-source/rest versus actual evaluated-pose diagnostics supplement it; no fullbody source mesh is deleted/hidden to fake success.

## Independent review

| Role | Verdict | Evidence boundary |
|---|---|---|
| Biomechanics reviewer | E01FAIL/E02FAIL; anatomical calibrationINCONCLUSIVE | Actual weights, matrices, relative axes, full geometry and independently computed wrist displacement |
| Software QA reviewer | Byte/repeat invariantsPASS; E01continuityFAIL | Independently parsed protected accessors, actual121LBS seam and actualfloat32 axis preservation |
| Visual reviewer | Gross shoulder/axilla/elbowFAIL/P1 | Actual Three views and baseline+both variants' native shoulders/dual elbows; micro-seamsINCONCLUSIVE |
| Owner | PENDING | No automatic release/merge |

Reviewers did not modify production files and did not read each other's conclusions. They inspected actual still evidence; video existence/codec/frame counts were verified, not falsely described as a watched full dynamic review. Playback software checks do not confer biomechanics approval.

## Windows and tooling

Read-only Windows PR9 `c1d7e209901390bfb73f784e0f1f48c8337f2e17`:21published Git-byte hashes verified, three schema fixtures checked, both real triangle subsets replayed. contact-v1 1.0.0 is now available; previous missing-schema status is superseded. No Mac OpenSim rerun or full121real-hand-contact acceptance is claimed. OpenSim model-specific shoulder constraints cannot calibrate these GLB attachments or elbow axes; unknown palm/wrist frames remainnull. Current diagnostic GLB has no apparatus, so no synthetic contact PASS.

Issue13 tooling is isolated DraftPR14, not merged into this branch: three pinned fixture-only project skills, actual A/B plus independent rerun, no global installer or production changes.

## Reproduce

```sh
npm ci --ignore-scripts
node scripts/rig-v2/attribution/analyze.mjs --output artifacts/phase2/my-baseline
node scripts/rig-v2/phase2/derive.mjs E01-local-gradient artifacts/phase2/my-E01
node scripts/rig-v2/phase2/derive.mjs E02-elbow-axis artifacts/phase2/my-E02
# Use each actual derived SHA with analyze.mjs --asset ... --sha256 ... --output ...
node scripts/rig-v2/phase2/seam-check.mjs --asset artifacts/phase2/E01-local-gradient/motion.glb --output artifacts/phase2/E01-local-gradient/seam-report-new.json # expected exit1
node scripts/rig-v2/phase2/trajectory-diff.mjs
node --test tests/rig-v2/phase2.node.mjs
```

See `scripts/rig-v2/phase2/README-render.md` for exact shared calibration/native commands. Output paths must be fresh. Existing input/attribution/render/consumer code versions and snapshots are retained in evidence; new metadata is not retroactively attributed to old builds.

## Stop point and debt

Completed: reproducible localization, two preregistered one-variable experiments, full geometry, actual renders/Chrome, independent reviews, Windows read-only interface consumption. No successful anatomical repair is claimed. Existing app build/13unit/26quality pass; new three regression tests pass while preserving expected E01 geometry/seamFAIL.

Retained workaround: diagnostic8sample visual budget is explicit and deferred for high-fidelity micro-detail. Permanently resolved task debts:0025reference-basis edit,0027identity count/import helper interpretation,0028explicit shader nodes,0030full-cycle framing. Deferred:0026intermittent TLS investigation (delivery succeeded),0029high-sample visual verification,0031failed experimental seam/attachment mechanism plus historical motion/contact limitations. No accepted risk; no task OPEN entry may be used to claim completion.

Next possible routes, requiring Owner scope decision: (A) new explicitly numbered source-equivalence-preserving local weight experiment using source identity/topology provenance, still not real attachment calibration; (B) reference landmark/joint-center/axis registration with Windows before another trajectory change. Pose-space correction remains design-only and must not conceal underlying attachment/seam errors. Both current candidates remain rejected; no FacePull, production replacement or merge.

## Import-space numeric limit

The isolated Blender rest-world diagnostic comparison observes up to1.1920929e-7m residual for E01 subscapularis, despite exact serialized GLB POSITION/topology/bind bytes. This supplemental world-coordinate exact assertion was not silently turned green or used to relax source geometry gates. Import/decomposition floating provenance is INCONCLUSIVE; source preservation proof remains the original immutable binary accessor/hash check.
