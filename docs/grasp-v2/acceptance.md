# Grasp Controller v2 acceptance — 2026-10-21

**Controller/software acceptance and tissue/exercise acceptance are separate.** This is a stacked Draft on PR24, not a main merge or a claim that the historical exercise quality failures are repaired.

| Requested item | Measured software result | Physical/model boundary |
|---|---|---|
| 1. Left/right mirror and axes | PASS: original bilateral 30-bone hierarchy, mirrored controls, reference neutral invariance, world/hand/handle conversion and real bone-axis transforms | Anatomical axis calibration BLOCKED: asset encodes authored local frames, no measured axes |
| 2. Independent fingers and opposition | PASS: per-digit and per-joint controls; independent sides; bounded thumb opposition; real Chrome opposite-side equality | Visible independent tissue deformation BLOCKED for 14 unweighted joints |
| 3. Different cylinder radii | PASS: actual GLB left and right at 8/16/24mm radius, all five digits proxy contact, no capsule penetration at unchanged 0.1mm threshold | 40mm example returns NOT_CONVERGED (~2.56mm residual), never fabricated success; proxy contact does not prove force closure |
| 4. Moving handle correction | PASS: geometry-based continuous finger solve and optional bounded captured arm/handle reference constraint; source hand frame follows upper-limb motion | Official bar trajectory remains unreachable where the inherited arm trajectory is not registered to machine. No artificial wrist teleport |
| 5. Limits and unreachable | PASS: joint clamp, missing/zero-length/invalid-reference checks, invalid-budget/invalid-handle rejection, explicit unreachable and nonconvergence | Authored v1 ranges/correction bounds are not calibrated physiological ROM |
| 6. Post-Mixer hold | PASS: restore → Mixer → capture animated base → arm/finger constraint → skin/bounds, no accumulated delta or repeated bind capture | Hand/finger relation residual never overrides tissue contact failure |
| 7. Play/pause/seek/loop/reset | PASS: actual main-page Chrome controls and source matrix tests; pause freeze and nonmonotonic seeks; release/reset; original scene restoration | Shared player/clock/Canvas only |
| 8. Blender/Three matrices | PASS: actual Blender 5.2 vs actual v2 GLB adapter, 5 bilateral presets plus 8 solver outputs; maximum world-origin error 0.571185 micrometres; maximum deformation-matrix component error 1.492127e-6 | Existing 64×float32 epsilon numerical allowance unchanged; not an anatomy tolerance |
| 9. Real geometry contact/deformation | PASS detector: actual posed source triangles, finite closed rendered 12-gon clips/caps, source edge/area/normal witnesses; Windows v1.1 schema export validated | **FAIL_TISSUE_GRASP / GEOMETRY_INSUFFICIENT**. No verified pads; severe tissue deformation and penetration remain; no tissue PASS possible |
| 10. Pulldown/curl regression | PASS software: real Chrome seated machine timeline, upgraded original curl/dumbbell scene, 467 source meshes, paused picking and scene switches | Whole-body motion/anatomy approval remains FAIL/pending; experimental finger asset does not replace production GLBs |

## Evidence

- Build passes; 27 unit tests pass (11 v2 actual-GLB tests plus 16 existing tests).
- Real Chrome Playwright suite: v2 integrated main page, existing pulldown/curl scenario switching, runtime/picking regression. Final JSON/complete interaction video/screenshots are in `evidence/`.
- `trajectory-audit.json`: 2 clips ×121 sampled poses ×2 hands =484. All484 proxy contacts; **0 tissue passes**. Maximum selected-source edge ratio 77.75065895. These are discrete samples, not continuous collision proof or full-body geometry clearance.
- `asset-audit.json`: all original POSITION accessor bytes unchanged; 467 source identities; zero GLB Validator errors. 467 `NODE_SKINNED_MESH_NON_ROOT` warnings are inherited unchanged from the original rig and disclosed.
- `contact-schema.json`: verbatim Windows packet-v1.1 schema from `a8247a4ff121c94b038ceccb77f729d30a85073c`, PASS. Unknown frames and non-independent provenance remain explicit.
- `assembly.json`: source SHA256 `40e3dbcbbe3423381dd2885936dd3f1c7d4355bcc6b4f0c30eb9245537be1dff`; animation donor `ef803a4bbb3c644504c124519e39ba0b3b760ec139eaf60d277ef7f7f5d23274`; generated asset `7c5b9ec06acc6c232456abdda6a5fc96aaf06ff256d9c814d4de1b0cfe118852`. The original BIN prefix is byte-identical.

## Debt and review gates

Resolved: semantic assembly reference comparison; declared Node type dependency; finite transition/idle invalidation and exact bilateral independence; solver objective/validator distance consistency; stale inherited scene-label assertion; project-owned schema validator.

Workarounds introduced: independent worktree initially reused dependencies through a symlink; replaced with its own declared installation. Heavy browser recordings/tests run serially after one concurrent timeout; no timeout or motion/contact threshold was relaxed. Existing installed Chrome is explicitly selected by the inherited Playwright config.

Deferred: missing pad/axis/attachment evidence, source side calibration and unweighted tissue joints; concurrent browser/GPU resource attribution (serial original tests pass); Cursor independent review. No accepted-risk waiver was requested or granted. No production asset replacement, original POSITION edits, skin shell, blind weight fix or main merge.

The complete source SHA and evidence file SHA256 values are recorded in `evidence/manifest.json` and the Draft PR. See `review-handoff.md` for Cursor's independent review scope and `README.md` for reproducible commands and adaptation path.
