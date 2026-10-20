# P0–P2 continuation: coordinate correctness, anatomical FAIL retained

Baseline PR22 `12b5a2f56d34eeaee8fb8b7e19499501639a3c85`; executor Codex, not Cursor. See handoff/continuation-recovery.md for all requested PRs, branch separation and reuse. No production source GLB, frozen R1, original POSITION or historical report was edited. Existing PR22 diagnostic/training separation is inherited, not claimed as new work.

## Actual changes

Reuse PR21's 30 finger bones and controls. Correct exported-reference quaternion composition and Blender/Three Euler convention. Zero-delta formerly displaced actual joints37.7099636mm; it now preserves exact reference transforms. Six native Blender poses and121 continuous samples agree with Three within0.580026 micrometres at joint origins. This is coordinate adapter verification, not anatomy verification.

Fix spatial/anatomical target mapping in a separate diagnostic helper: canonical LeftHand has positiveX, while machine viewer leftGrip alias has negativeX. Use actual same-side angled12gon grip segment. Retain inherited unconstrainedCCD as labelled arm-reach probe, not a sitting pulldown. No new fingers, shell, authored full-body clip, weight or original geometry changes.

## Actual results

- BUILD_PASS; Vitest16/16; quality26/26; grasp Node10/10. Actual headless installed Chrome: 15 screenshots, whole4s cycle video, replay and pause assertions; no page errors.
- Native Blender:31 rendered frames/video, saved derived blend; all467 original base geometries unchanged;121-pose bone roundtrip max0.872450 micrometres.
- Both engines121 contact samples: maximum minimum-distance discrepancy0.468178 micrometres. Tissue intersects conservative inscribed finite grip solid: minimum about−23.159mm. FAIL_TISSUE_GRASP.
- Hand-origin reach residual up to4.3371mm. DIP joint bins are not fingertips; skeletal wrap INCONCLUSIVE. No true grasp PASS.
- Full1,092,000 triangles ×121×2 on existing57bone asset with frozenR1 tracks: Curl39/Pull91 severe-compression frames. Legacy and corrected controller both MOTION_GEOMETRY_FAIL. Maximum edge ratio approximately107.6→77.9, still unacceptable. These are hand-weight/tiny-edge diagnostics, not physiological strain estimates. They are distinct from frozen27boneR1 maximum3.988438; original failures unchanged. Numeric details in continuation-results.json and full archived reports.

## Limits and next decision

P2 is incomplete: actual rendered tissue still tears and intersects; no credible visible five-finger grip. P3 remains blocked by calibrated attachment/axis evidence (Windows W-F4 INCONCLUSIVE). No blind weight/axis search, no skin shell, no pose concealment. Native/Three measurements are independent engine checks, not independent expert sign-off. Fresh biomechanics/visual reviewer verdicts and OWNER_APPROVAL remain PENDING; do not merge or replace assets.

Priorities: establish original hand tissue/fingertip representation and attachment evidence; choose one attributable local weight/attachment experiment; repeat full tests and expert review. Existing P21/P22 FAILs are retained. This Draft is a bounded software-correctness result, not completed training motion.

## Reproduction

Use the pinned existing `artifacts/grasp-v1/grasp-controller.glb`, SHA40e3dbcbbe3423381dd2885936dd3f1c7d4355bcc6b4f0c30eb9245537be1dff. Runtime Blender5.2.0 LTS fbe6228777e7; Node26.5.0. Generated files are isolated in ignored artifacts/grasp-v1/p3-basis.

```sh
npm run build
npm test
npm run test:quality
node --test tests/grasp-v1/*.node.mjs
node scripts/grasp-v1/official_sequence.mjs
node scripts/grasp-v1/full_regression.mjs
node scripts/grasp-v1/full_regression_legacy.mjs
# Restore pose-input.json and pinned legacy-controller.mjs from evidence first:
blender -b --python-exit-code 1 --python scripts/grasp-v1/export_basis_reference.py -- artifacts/grasp-v1/p3-basis/native
node scripts/grasp-v1/check_basis_parity.mjs
blender -b --python-exit-code 1 --python scripts/grasp-v1/render_official_sequence.py
blender -b --python-exit-code 1 --python scripts/grasp-v1/render_official_sequence.py -- --measure-only
python3 -m http.server 5194 --bind 127.0.0.1
# In another terminal, actual installed Chrome channel:
node scripts/grasp-v1/official_browser.mjs
```

Evidence directories must be fresh for native exporters. Legacy controller is exact `git show 12b5a2f:src/grasp-v1/controller.mjs`; no hand edits. Viewer is `/src/grasp-v1/official-sequence.html`, explicitly FAIL diagnostic. Basic software pass does not override geometry, grasp, independent review or owner gates.
