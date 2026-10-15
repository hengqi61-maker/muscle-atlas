# Independent software QA — FAIL for milestone; functional regression checks PASS

Target commit: `baa407752cb46ac3b83f85b75262cebb08529e65`.
GLB SHA256: `44109e516dc44ee1767beec7a5cb61504c804c83b952fee92e9d1120c9021cea`.
Reviewer: fresh independent software QA session; no implementation/test authorship and no other reviewer reports or historical review findings read. No owner acceptance or merge authorization.

## Evidence and verification

- Independently verified HEAD, both live/frozen GLB hashes, and all 62 paths/hashes in `freeze.json`: zero mismatches. Working tree is not clean: root browser capture updated tracked delivery PNGs. These do not alter frozen production source, model or test bytes.
- Independently ran `npm test`: 13/13 PASS; `npm run test:quality`: 18/18 PASS; `node scripts/validate-pulldown.mjs`: PASS, validator zero errors and zero warnings, 467 source meshes, 469 skinned meshes, one four-second clip and 121 samples. The validator command writes evidence: its only new tracked diff was `docs/evidence/pulldown-validator.json` validatedAt timestamp. Runtime JSON was unchanged. This incidental output is disclosed; no production/history/test file changed by reviewer.
- Read `browser-full.log`: actual Chrome, four tests PASS (27.5 s). Read assertions rather than infer correctness from names. Tests cover source-model loading, exercise switches, endpoint restart, slow loop wrap, paused nonmonotonic seeking, style changes, actual bounds containing every source vertex at nine seek points, and repeated left-lat picking. Browser was not rerun by reviewer to avoid duplicate heavy capture and additional delivery-output changes.
- Build and install success are maker-provided, not independently rerun here. No new npm ci claim. Browser test route is Vite test mode, not installed macOS packaging.
- Read source runtime `Scene.tsx`, `skinnedBounds.ts`, playback tests, geometry helpers and motion-quality generator; inspected frozen motion-quality JSON/log and capture metadata. Geometry units are model metres; production applies 1.45 scale and translation. Ratios are scale-independent.

## Findings

### P1 — K07: unresolved engineering geometry alarm on bilateral palmaris longus

`motion-quality/motion-quality.json` records 13 collapsed triangles at peak for each of `left palmaris longus` and `right palmaris longus` (4000 eligible triangles each); minimum deformed/source triangle-area ratios are 0.00304984 and 0.00169612. More than three triangles lose over 95% area throughout approximately 0.7–3.3 seconds. `scripts/quality/motion-quality.mjs:23-30,35,44-46` computes actual skinned vertices against each mesh unskinned source triangles and intentionally exits 1 for this GEOMETRY AUTO FAIL. The area helper and absolute/relative alarm unit tests pass.

Expected: no unexplained severe deformation degeneracy on preserved source anatomy. Actual: frozen packet retains a deterministic non-cuff alarm while ordinary structural/runtime tests pass. This blocks a clean motion-quality claim; it does not by itself establish tearing visible on screen, unsafe anatomy, or an invalid GLB. Confidence high in recorded engineering alarm, limited for anatomical interpretation. Verify by locating offending triangle indices on actual frames, distinguishing pre-existing source/rig artifacts from new deformation, then rerun the same 121-sample diagnostic after any repair. Do not hide it by accepting the marker-only validator or raising thresholds without evidence.

### P2 — S02: current candidate performance remains INCONCLUSIVE

`capture-metadata.json.performance` is one paused Real Anatomy/back-view rAF sample (241 frames, mean 16.61 ms, p95 16.70 ms), about 475 draw calls and 1,092,338 triangles. It is not controlled playing/paused performance across styles/views and does not measure GPU duration. `artifacts/m2/performance-baseline/summary.json` identifies older commit `7a0d258b...` and different GLB `56b3ca23...`; it cannot certify this frozen candidate. Timer-query support is not a timer measurement. No performance regression is proven, and no current performance PASS is justified. Next evidence: bounded repeatable current-candidate CPU/render/GPU observations with stated environment, duration, style, view and playing state, if performance acceptance is requested.

### P2 — test coverage limits must remain explicit

`validate-pulldown.mjs` measures deformed synthetic palm markers and expected hand-axis math; its ~28 micrometre positional error cannot establish original palm/thumb/finger grasp. Browser runtime checks all source bounds but only repeatedly clicks left latissimus. They do not independently validate every source pick, actual source hand orientation, seat/thigh contact, shoulder anatomy, calibrated muscle attachment, or runtime cable continuity at every numerical sample. Motion-quality records 62 selected regions, not all 467 deformations; its V01 identity scan covers all 467 metadata identities but is deliberately INCONCLUSIVE on side binding. `npm test` does not run `test:motion-quality`; release evidence must retain that separate exit status. No false anatomy PASS was found in the new diagnostic output.

## Gate assessment

- S01 software structure/ID mapping/seeking/style regression: PASS within the sampled Chrome evidence and inspected tests. No verified P0 software defect.
- S02 build/unit/browser functional subset: PASS from supplied build plus independently rerun units/structural validator and inspected browser log. Performance portion INCONCLUSIVE.
- K07/overall milestone: FAIL pending disposition of retained geometry alarm. K01–K05/anatomical interpretation and visual fidelity are outside this software review; software assertions cannot approve them.
- Local data safety: no new destructive operation or remote-service requirement identified in inspected runtime change. Full persistence migration/security audit was not in scope.

## Completion and debt accounting

Completed: frozen-candidate independent software QA and this report. Workarounds introduced: none. Permanently resolved debt: none claimed. Deferred/accepted debt: no debt records edited or accepted by reviewer; geometry and performance remain unresolved evidence items above. Remaining risks: sampled interaction coverage, absent current controlled/GPU performance, and unverified anatomical meaning of geometry flags. No owner acceptance, release readiness, or merge approval is granted.
