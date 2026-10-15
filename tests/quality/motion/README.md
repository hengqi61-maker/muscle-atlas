# Independent motion constraints

Run from repository root after `npm ci`:

```
node --test tests/quality/motion/*.node.mjs
node scripts/quality/motion-quality.mjs --source /absolute/source/tree --asset /absolute/candidate.glb --ref COMMIT --out /absolute/evidence/directory
```

`--source` supplies model-specific machine configuration, `--asset` defaults to that source's pulldown GLB, `--ref` labels immutable provenance, and `--out` receives machine-readable evidence. The tool never writes source assets or historical review files. A confirmed constraint violation exits 1. Otherwise it exits 0 **without converting INCONCLUSIVE into PASS**. Consumers must read each rule status. It is supplemental to build, Vitest, GLB validator, and real Playwright checks.

B01 inspects all actual weights in all eight cuff meshes, actual selected scapula/humerus-region source vertices, and 121 actual deformed samples. An all-Thorax cuff with moving attachment bones is a confirmed defect. Triangle collapse compares actual skinning against unskinned source-rest geometry, rather than a potentially already-bad initial pose. Engineering alarms reject over 95% triangle area loss affecting more than 1% or three triangles; these are conservative mesh degeneracy thresholds, not human movement limits. An absent collapse alarm cannot establish valid attachment anatomy.

B02 preserves strict interior-vertex evidence and adds Three's triangle/AABB separating-axis intersection. Unit coverage includes a triangle crossing the box with all vertices outside. SAT includes touching; it is reported separately and is never falsely labelled deep penetration. Named foot muscle/tendon proxies are original anatomy, not a sole skin surface. Seat and thigh interfaces need independent source contact regions before claiming support.

V01 preserves all 467 IDs and exports BP/FMA/source metadata, index components, unskinned rest bounds and declared name side. These are descriptions, not independent source-rest anatomical binding. Anatomical multi-mesh bundles and duplicated seam vertices can be disconnected legitimately. No component is deleted/hidden. Precise abnormal-space assessment and screenshots remain INCONCLUSIVE until reference anatomy and real browser evidence are supplied.

K02 uses actual original source vertices near handle surfaces, never contact markers. Nearest vertex radial gaps cannot prove a palm/thumb winding, wrist basis or supported finger grasp, so K02 stays INCONCLUSIVE. Source hands are unchanged.

KINEMATICS records 121 actual joint positions and actual segment distances with 10 micrometres tolerance for invariant rigid lengths/cycle closure, separately from 1 micrometre point-interior precision. It reports maximum intersample displacement without unsourced medical cutoffs. Bar/stack curves share sample times but are analytic; production common-clock verification requires the separate browser probe. Units are model metres, seconds, no production parent scale.

Known limits are deliberately visible as INCONCLUSIVE. The test author does not release or independently approve their own suite.

Schema v2 separates **B01 cuff-specific** frozen/collapse constraints from **GEOMETRY**, which reports severe collapse across every sampled source region, including palmaris longus. A non-cuff collapse does not acquire a cuff label.

`npm run test:quality` includes all motion math tests; the existing core-quality CI already runs this command. `npm run test:motion-quality -- --source ... --asset ... --ref ... --out ...` runs asset constraints and deliberately fails on confirmed geometric defects. It is not installed as a green-only CI bypass for the known-bad prototype. Both commands supplement the existing build, Vitest and real browser checks.

`spatialFlags` localizes original hand/thumb/carpal meshes at 0/25/50/75/100% by exact source name, BP/FMA ID, node, connected-component index, actual centroid/bounds and distances to joint origins. This includes ordinary left/right flexor pollicis brevis (BP7575/BP8958). A component nearer a non-hand joint receives `NEARER_NON_HAND_JOINT` (or `NEARER_OPPOSITE_HAND_JOINT` for the opposite wrist); every spatial observation remains INCONCLUSIVE. Disconnected source anatomy is retained. These diagnostics help reviewers find a suspicious mesh and pose; nearest-joint proximity is not a proof of anatomical side or wrong binding.

Optional `--interfaces /absolute/interfaces.json` accepts an array of explicit source-bound solid AABBs, for example:

```json
[{"id":"seat","sourceIds":["CONFIRMED_SOURCE_NAME_OR_BP_ID"],"min_m":[-0.26,0.5975,0.13],"max_m":[0.26,0.6825,0.55]}]
```

The example box follows the current seat dimensions, but its placeholder source must be replaced by an independently verified contact region. Thigh-pad solids can use the same interface. Matching source meshes are actually sampled across all 121 poses; strict interior-vertex and triangle/SAT counts are emitted separately. Supplied AABBs and source binding are preserved in evidence, and interface verdicts stay INCONCLUSIVE until reviewed. No artificial skin, fabricated contact region or marker substitute is introduced. Seat/thigh support is explicitly unmeasured when no descriptor is supplied.

Prior v1 red/prototype packets are preserved. Follow-up runs use a separate `artifacts/motion-quality-v2/` directory.

## Round 2 shared-production support diagnostics

The legacy `scripts/quality/measure-attachments-support.mjs` has hardcoded seat `.64` / thigh-pad `.80` dimensions and is **round 1 geometry evidence only**. Do not reuse its support measurements as round 2 evidence. This independent replacement consumes only the actual shared `config.supports` definitions and has no legacy geometry fallback:

```
npm run test:motion-support -- --source /absolute/candidate/tree --asset /absolute/candidate.glb --ref COMMIT --out /absolute/new/evidence
```

It hashes the **complete configuration**, runtime machine source and GLB independently, so changed supports remain traceable even when the GLB hash is unchanged. It samples all original source meshes across 121 poses. Explicit `supportContactRegions` source names and BP IDs are preserved, resolved against the actual GLB metadata and reported with unmatched bindings. Selected proxy face gaps are recalculated from actual triangle polygons clipped to the current seat/pad XZ footprint. Positive gaps remain INCONCLUSIVE; there is no invented skin thickness, force or contact PASS.

Boxes use actual strict interior vertices and triangle SAT against the box inset by the unchanged 1 micrometre precision tolerance. Crossing triangles with all vertices outside are covered by calibration tests. Actual oriented finite capped cylinders use strict vertex depth, analytic segment crossings and axis/triangle intersections. A conservative cylinder AABB candidate alone never fails. Some interior-only cylinder/triangle intersections can evade these sufficient tests, so no detections is INCONCLUSIVE and cannot prove clearance. Reports preserve exact source IDs, solid IDs, poses and distinct candidate/interior counts.

A support-connection graph records exact sufficient geometric witnesses among the current boxes/cylinders. No witness path is INCONCLUSIVE, never proof of disconnection; the graph does not validate frame strength, floor anchorage or physical support. Production-render geometry agreement still requires the separate real browser probe. Math calibration tests include positive 20 micrometre gaps, negative 10 micrometre overlaps, crossing triangles, oriented-cylinder AABB false positives and cap/box connection witnesses. Thresholds do not adapt to candidate dimensions or observed results.
