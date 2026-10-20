# E01 split diagnosis and rejected E03 continuity control

## Frozen inputs and scope
PR12 E01/E02 failures remain intact. Frozen R1 SHA `ef803a4bbb3c644504c124519e39ba0b3b760ec139eaf60d277ef7f7f5d23274`,467 source identities/27 shared bones retained. No production/main/finger changes. E03 was executed before the owner's subsequent instruction to wait for physical references. It is retained as a **rejected numerical continuity control**, not adopted repair. No further candidates will be implemented before Cursor/Windows publish usable physical evidence.

## Root cause, reproduced
Same-mesh original exact POSITION/JOINTS/WEIGHTS equivalence does not imply all coincident anatomy should be welded. E01 updated export-index triangle neighborhoods independently. Originally identical vertices441/1288 consequently received Scapula weights0.6622020602/0.6468195915 and Humerus0.3377979100/0.3531804085. Both map to the same RightScapula/RightHumerus bones. Under identical actual bone transforms their different LBS sums separate3.179553092mm at Pulldown sample0. Zero-weight Pelvis slots are padding, not extra anatomical attachment. Source equivalents must be preserved without merging base geometry.

`E01-split-121.json/csv` records baseline and rejectedE01 for both clips/all121 times, actual world points, weights, bone names and influencing matrices. Reproduction exits1/AUTO FAIL. Source/export indices must not be confused with upstream Blender vertex IDs.

## Controlled evidence, not an adopted repair
E03 keeps E01 seed/two-ring/lambda. Only added variable is projection onto original exact equivalence classes, not global smoothing or axis tuning.22 selected vertices/21 classes/43 closure rows.246 changed weight bytes only. Two independent builds yield SHA `3deb0d355587950ff212448bff5ef9d92b06f0ed7c5560a173271ac116a35734`. Independent raw-byte review and1785 duplicate-pair actualLBS checks×121×2 give zero separation. Other geometry, identity, bind, matrices, motion and hands byte-identical.

| Full unchanged test | Frozen R1 | E03 |
|---|---:|---:|
| Curl severe frames |39/121|39/121|
| Pulldown severe frames |91/121|91/121|
| Pulldown maximum edge ratio |3.9884383355|6.4698000415|

All1,092,000 triangles checked at121 times per clip. New/removed severe mesh poses0/0 both clips; aggregate counts do not close stretch failures. Worst edge now triangle953,480–483,0.361160497→2.336636198mm. Original triangle914 still3.989352498 versus3.988438336 baseline. **MOTION_GEOMETRY_FAIL**; anatomical attachments uncalibrated.

Independent software PASS limited invariants; biomechanics FAIL/attachment INCONCLUSIVE; visual FAIL for gross shoulder/axillary and elbow deformation. See immutable E03 review files. Visual reviewer actually inspected17 images, did not watch videos; no temporal quality PASS inferred.

## Actual execution
- Phase2 node tests4/4; Vitest13/13; quality26/26; app build PASS with existing bundle warning. Khronos validator PASS; see raw warnings/info in validator.json.
- Real Chrome serial run PASS85.533s:467 meshes, both121-pose clips,100screenshots,two actual cycleWebMs,pause/raycast. Initial concurrent-load navigation timeout retained, root cause DEFERRED; serial pass is not performance acceptance.
- Actual native Blender5.2:122PNGs,two121-pose trajectories,two31-frame4.133sMP4,blend; wall241.856s.8sample diagnostic limits retained. Fresh4asset calibration exactly matches prior camera fields; zero sampled clipping. Two isolated real source-rest/evaluatedLBS comparisons included. No tissue hidden to pass.

## PR14/PR15 tooling receipt
PR14 fixed upstream71d031d: project override limits helper execution to disposable fixtures; no generic merge/delete/auto-weight recommendations applied to anatomy. Fresh actual pinned pilot rerun completed two baseline/two helper builds, expected detached-fixture QA FAIL. Summary in evidence. This does not validate anatomy.

PR15 fixed commit7624e5b9df9ca50e88d2e52b49dbeece50cdd916: guarded MCP read-only client attempt was rejected by exclusive client lock before query. No takeover/restart. Its current interactive anatomy inspection is pending coordinator ownership handoff, not claimed complete. No wholesale PR15 merge (it includes unrelated historical files).

## Next physical evidence required
Cursor/Windows should publish fixed source hashes/schema/coordinates/reference posture, independently supported scapular/humeral attachment regions and joint-axis calibration, correspondence uncertainty, and measured/validated motion constraints. OpenSim model paths alone are not measured source-GLB muscle attachment regions. Requested bilateral/mirror mapping and full-cycle matrices/contact witness remain separately scoped. Choose one attachment or axis variable only after this evidence exists; compare against frozen baseline in both clips, retain original thresholds and independent review. No further unsourced candidate tuning.

## Reproduction
```
node scripts/rig-v2/phase2/seam-diagnostic.mjs --asset artifacts/phase2/E01-local-gradient/motion.glb --output NEW-E01-121.json
node scripts/rig-v2/phase2/derive.mjs E03-equivalence-projection NEW-DIRECTORY
node scripts/rig-v2/attribution/analyze.mjs --asset NEW-DIRECTORY/motion.glb --sha256 3deb0d355587950ff212448bff5ef9d92b06f0ed7c5560a173271ac116a35734 --output NEW-DIRECTORY
node --test tests/rig-v2/phase2.node.mjs
```
Build command documents reproducibility of rejected control only; not authorization for new candidate or production adoption. Source licenses remain original BP3D/ZAnatomy attribution/share-alike, separate from code licensing.

## Debt and approval
Resolved: E03 numerical alias divergence invariant. Deferred: initial browser timeout attribution, unavailable configured Git proxy (delivery used command-local direct route), guarded MCP ownership handoff, existing anatomical/hand/attachment defects. No accepted-risk approval invented. Owner approval PENDING; main unmerged. All physical/anatomical failures remain visible.
