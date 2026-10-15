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
