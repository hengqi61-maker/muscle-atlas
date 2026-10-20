# Windows → Cursor / Mac PR12 handoff — 2026-10-20

Frozen Mac PR12 `7214f3ffbf5c1315323d976b62f73a5b100faaf9` is read-only. Both E01/E02 remain rejected. Windows adds independent references, not a deformation fix or permission to modify Mac assets.

## Evidence categories

| Evidence | Actual observation | Unknown / limit |
|---|---|---|
| Mac serialized GLB | SHA256 `ef803a4bbb3c644504c124519e39ba0b3b760ec139eaf60d277ef7f7f5d23274`, 27 joint IDs/default matrices/inverse binds, two 121-key diagnostic tracks | Default node pose is not universally a bind pose; axes are engineering frames |
| Windows computed Mac axes | `R_default.T @ R_track`, principal angle and axis in default local frame; Curl Forearm maxima100.0000119°, Pulldown90.0000223° | Not anatomical elbow flexion limits or evidence of correct attachments |
| Native OpenSim4.6 rerun | 14 prescribed model poses; full joint XML/frames/axes, actual coordinates and relative matrices; AC maximum7.0165e-17m | Right-only reference, hand welded, no finger joints, no source-mesh calibration |
| Original source triangles | Frozen M2/procedural source0914d4f, 363 discrete input packets; source IDs, triangle IDs, witnesses and byte hashes | These are NOT PR12 candidate GLB scans;22 exercise/source rows unproven topology remain UNKNOWN |
| Mac PR12 review | E01 introduces source-equivalent seam, E02 changes wrist trajectories; both failed per published report | Mac observations retained as external evidence, not independently rerun candidate deformation results |

Curl left Forearm axis at maximum basis rotation: `[0.9966392725,-0.0802500465,0.0164344293]`; right `[0.9966392725,0.0802500465,-0.0164344293]`. Sign depends on principal rotation and chosen reference; never copy these into OpenSim as clinical axes. Null axis near zero/pi means extraction undefined/unsupported, not absence of rotation.

Default-world times inverse-bind maximum matrix-entry residual1.1942543e-6 occurs at LeftThigh in the frozen GLB, predominantly off-diagonal rotation entries (dimensionless); it is NOT1.194micrometres translation. The initial new test guessed a1e-6 bound and failed; raw log retained. The final test records frozen numerical observations rather than inventing an anatomy acceptance threshold. No source/runtime or existing quality gate was changed.

## Structural mismatch before comparison

Mac serial Clavicle→Scapula→Humerus differs from OpenSim thorax→clavicle and thorax→scapula with AC closure. OpenSim elbow is one coordinate with separate ulna/radius; Mac single Forearm merges structures. Model default elbow lock is retained for shoulder experiments; elbow sensitivity explicitly changes the in-memory default lock before initSystem.17coordinates are not17independent degrees of freedom. Full joint definitions and coordinate actual values are in model-sweeps-20261020.json. No anatomical registration matrix is known.

Existing exchange-v1 remains unchanged: `T_target=A*U_s(T_source)*B`. Units affect translation only. A/B require sourced common landmarks, joint centers, reference posture and axis definition. Anatomical path points from OpenSim are model-provided references, not calibrated attachment labels for467 meshes. Geometry artifacts do not establish muscle force, activation or EMG. No fixed scapulohumeral ratio or physiological threshold is invented.

## Reproduce locally

```powershell
python -B scripts/biomechanics/mac_rig_reference.py 7214f3ffbf5c1315323d976b62f73a5b100faaf9 research/phase2/shoulder/mac-pr12-bind-axes.json
C:\ProgramData\Anaconda3\Scripts\conda.exe run -p D:\codex\.muscle-atlas-opensim python scripts/biomechanics/phase2_shoulder.py research/phase2/shoulder/model-sweeps-20261020.json --model D:\codex\muscle-atlas-opensim\artifacts\opensim-models\ThoracoscapularShoulderModel.osim
python -B -m pytest -q tests/biomechanics --basetemp=artifacts/phase2/pytest-fresh
```

Model official OpenSim-core4.6 source `52094cc61c3e795552c658e34a73d083f4662c6b`; modelSHA256 `892bd333a1e1e6a2b77902b54218f12727eefd2306ca82bbda81621c926271fe`. Source/credits/license and applicability remain in previous model-assessment, not assumed to transfer anatomical calibration. No model binary redistribution.

Contact1.1 is additive to published1.0. Verified IDs remain arrays; unknown identity is null. A legacy packet's local triangleIndex never becomes an originalTriangleId. Split mixed surface/convex timelines into separate packets. For original full-scan reproduction, use frozen executed snapshots and retained inputs identified in input-manifest, not pretend current code performed the historical scan. Windows locally retains generated geometry; no large models inGit.

## Requested next Mac export

For each rejected candidate/baseline provide exact asset bytes SHA, original467 source IDs, original-vertex/triangle correspondence (including seam duplicates), posed world triangles for all121samples/both clips, per-side wrist/palm frames with evidence category, canonical joint hierarchy/default and inverse-bind matrices, coordinate/unit convention, prop actual/proxy geometry, producer SHA. Unknown landmark registration stays null. This allows independent candidate scans without touching weights or finger poses.

Bridge PR10 stays independent: no remote writable tools or production Blender. AppContainer network denial and full corrected-cleanup rerun have NOT passed; no new profile experiment is implied by this data delivery.
