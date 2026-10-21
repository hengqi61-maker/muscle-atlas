# Grasp Controller v2

Development branch is stacked on PR24 (`8b83ed2`), **not main**. PR21/22/24/25 were inspected as OPEN; PR25's rejected weight changes are excluded. Production assets, frozen R1 and original mesh buffers are unchanged.

## Run and architecture

`npm ci --ignore-scripts`; `npm run dev`. Main page → right sidebar → Grasp Controller v2. The existing R3F Canvas, AnimationMixer, timeline and renderer own playback. No standalone demo/player is introduced. `predev`, `prebuild`, `pretest` reproducibly assemble an experimental asset from PR21's 57-joint rig and the existing two shared-rig clips. Source BIN prefix stays byte-identical; only referenced animation buffers are appended. `artifacts/grasp-v2/assembly.json` records hashes and reference-transform compatibility error.

- `HandRigAdapter(root, side)` validates all 15 joints, parent relationships, quaternion/translation validity and nonzero segment lengths. It captures references once and applies `reference × oppositionY × flexX`, matching Blender XYZ with spread zero. `apply`, `clamp`, `preset`, `mirror`, `segments`, `frame`, `convert`, `axisWorld` are reusable across equipment. Original v1 interfaces and presets remain intact.
- `GraspSolver(rig).solve(handle, seed, opposition, maxSweeps)` performs bounded coordinate search. At most 32 sweeps and `1 + 32×maxSweeps` objective evaluations. Every variable is clamped to the authored v1 range. Objective minimizes each digit capsule-to-finite-cylinder gap with a strong nonpenetration penalty using the same bounded SDF minimum as validation; thumb opposition is optimized within its authored bound. It exports explicit projected tip targets on the finite handle surface. Final validation uses bounded capsule SDF minimization. It returns pose, residual in metres, evaluation count and explicit `PROXY_CONTACT`, `PENETRATION`, `UNREACHABLE` or `NOT_CONVERGED`. It never substitutes wrist coincidence for contact.
- `HandPoseLayer` owns finger writes. Call `beforeMixer`, mixer update, `captureAnimation`, solve/set, `afterMixer(..., false)`, then skeleton/bounds update. It restores pre-layer animation before each update, captures no new bind references, interpolates, holds, releases and resets. Runtime captures animated base **before** the solver mutates any bones. Pause/seek/loop use the existing clock. Finite interpolation snaps to target, so unrelated hand edits cannot resume tiny residual motion.
- `ContactValidator` separates capsule/cylinder proxies from actual source tissue triangles. Actual triangles are clipped against the **rendered closed 12-gon grip**, including end caps, using the Windows convex contact algorithm. Gap/depth are conservative witnesses, not exact MTV. Runtime also computes source edge stretch, area collapse and inversion witnesses in a skin-co-moving frame. Missing pad surfaces always prevent a positive tissue-grasp result. Contact tolerance remains 0.1mm; area collapse <0.05 and stretch >2 remain failures.
- `runtime` links these modules to the main scene. Left/right controls and solving remain independent; hand-attached dumbbell/rope targets follow the animated socket frame, with model-specific initial along-palm placement derived from handle radius (not a tissue-contact claim), while actual machine grip targets follow the official bar trajectory. These are explicitly experimental targets; unattainable official grips remain unreachable. Idle work is invalidated by pose/time/control revisions. Full source tissue scans remain enabled for changed states, with reports throttled to one second during motion.

`Handle` describes a **rigid metric** matrix with cylinder axis local Y, radius, halfLength and kind. Arbitrary scale is rejected by the cylinder function. All solver and contact results are world-space metres. The terminal tip and 4mm capsule radius are explicit proxies. Source tissue is never synthesized.

## Native and Windows compatibility

`npm run test:grasp-v2:numeric` writes actual GLB pose inputs and Three world matrices. `scripts/grasp-v1/export_basis_reference.py` runs in actual Blender 5.2 against those same inputs; `node scripts/grasp-v2/compare-native.mjs` compares world origins and deformation matrices `W_pose × inverse(W_rest)`. The importer-local frame difference is cancelled rather than comparing incompatible raw bone orientations.

`npm run test:grasp-v2:contact` exports actual source triangles in Windows packet-v1.1 format and validates against the verbatim upstream schema from `a8247a4ff121c94b038ceccb77f729d30a85073c`. Portable geometry hashes use float64 LE vertices then uint32 LE triangle triples. Calibration frames stay null, `frameStatus:unknown`, `independentlyExported:false`, and evidence kind `legacy-unverified`; producing this packet cannot promote it to independent anatomical evidence.

## Model limits and adaptation

The GLB has no measured anatomical axis metadata. Local X/Y/Z are authored rig axes from `build.py`/`align_roll`, transformed through actual references; they are **not validated anatomical axes**. All existing 30 joints are retained, with equal authored segments of ~20.6667mm. Distal tails are not encoded in glTF, so the terminal tip extrapolates the adjacent authored segment and is labelled a proxy.

14/30 joints have zero source tissue influence (both sides: IndexDIP, MiddleDIP, RingPIP/DIP, LittleMCP/PIP/DIP). The disconnected muscles/tendons have no independently verified finger-pulp surface. Source labels may not match spatial handedness, so tissue side attribution is not anatomical approval. Existing stretch/penetration failures are preserved. Bone control does not establish visible independent tissue deformation.

Subsequent adaptation requires reviewed original-source finger landmarks, axes and attachment/weight evidence. Map these into the adapter, preserve source POSITION and provenance, then rerun native matrix, complete triangle contact, deformation and real-browser gates. No new skin shell, blind weight edits or replacement skeleton is approved by this implementation.

## Reproduction

- `npm run build`
- `npm test` (actual GLB tests plus existing unit regression)
- `npm run test:grasp-v2:browser` (installed real Chrome; records actual main-page interaction)
- `npm run test:grasp-v2:numeric`
- `npm run test:grasp-v2:contact`

See `acceptance.md` for measured outcomes and unresolved criteria. Cursor independent review remains a separate gate; Codex tests do not replace it. No main merge is performed.

`GripAnchor` optionally captures the hand-to-handle transform once and corrects Humerus/Forearm/Wrist after the Mixer with a bounded nine-variable search (≤16 sweeps, ≤289 evaluations). Corrections are limited to ±0.35rad relative to that frame's animation, preserve joint translations/lengths, and return `REFERENCE_HELD`/`REFERENCE_UNREACHABLE`. This is a controller correction budget, **not calibrated physiological ROM**. Its relationship residual never overrides finger or tissue contact failures. Release restores the pre-constraint animation; recapture occurs only when hold is explicitly re-enabled.

For this inherited source label mapping, tissue side attribution is explicitly unverified. Runtime uses source labels for diagnostic grouping and exposes that limitation; no anatomical/spatial side calibration is inferred. Export packets preserve unknown calibration. GLB Validator reports 0 errors and the same 467 pre-existing `NODE_SKINNED_MESH_NON_ROOT` warnings as PR21; these are disclosed rather than suppressed.
