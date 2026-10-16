# V2 R0 — independent legacy architecture audit

Audit source: exact `0914d4fad3fbe107ea90c08473b6d2a448345ba6`, branch `codex/unified-rig-v2`. This is a read-only architecture investigation, not an M2 repair/release review. Production inputs and previous reports were not edited. Raw evidence is `artifacts/rig-v2/r0-audit/legacy-observations.json` (parent publishes an unchanged copy and inspector under `docs/rig-v2/exports/` for GitHub handoff); reproducible extractor is `inspect-legacy.mjs` beside it (`AUDIT_SHA=$(git rev-parse HEAD) node artifacts/rig-v2/r0-audit/inspect-legacy.mjs`). It parses GLB JSON/binary accessors directly and computes actual hierarchical transforms with Three.js Matrix4; it does not infer bones from generator text.

## Handoff boundary

The JSON is a **raw Mac observation**, not a finalized cross-PC exchange schema. Windows branch `codex/opensim-biomechanics` owns biomechanical schemas/kinematics. GitHub is the formal code handoff channel. Coordinate columns below are actual glTF numeric bases; they are **not** OpenSim coordinates, clinical flexion axes, validated scapular frames or anatomical joint conventions. Windows must confirm axis order, sign, model reference frames, units and uncertainty before any retargeting contract is accepted. This report proposes naming/reference-pose questions for agreement only.

## Actual asset inventory

| Asset | SHA256 | Meshes | Skin / actual joints | Skinned primitives | Clip |
|---|---|---:|---|---:|---|
| anatomy.glb | 6e84529b60b64cc8f8d5cef665fda932e359e828b66d0c2dd44ec1bd9d0bd01f |467|0 / 0|0|none|
| anatomy-curl.glb |0b579c7256a0500b51b5f14506813285ebddc04046106451c55e84ccfba1585f|478|1 / 2|55|Scene, 0–4s, 28 channels|
| anatomy-pulldown.glb |1e0af33c14cd74b5b353c0d9e8e2c030d9559e2c561c96ae831c4bf666f4a2ab|469|1 / 16|469|Scene, 0–4s, 58 channels|

SourceName-tagged source nodes are retained separately from equipment/markers in the raw inventory. A skin count is not an anatomy-validity metric. Every actual joint record includes parent, local/world column-major matrix, translation, XYZW quaternion, scale, basis columns, and the actual inverse-bind matrix. Every skinned primitive includes positive influence counts, mean weights, sum range and morph-target count. Animation records include every target/path, interpolation, range and first/last output.

Actual curl hierarchy: `LeftCurlRig -> UpperArm -> Forearm`. There are no thorax, scapular, clavicular, right-arm, hand or finger bones. The hand source meshes use the forearm chain; equipment/palm markers share that chain.

Actual pulldown hierarchy:

```text
PulldownRig
└─ SpineRoot
   ├─ Thorax
   │  ├─ LeftScapula -> UpperArm -> Forearm -> LeftHand
   │  └─ RightScapula -> RightUpperArm -> RightForearm -> RightHand
   ├─ LeftThigh -> LeftShin -> LeftFoot
   └─ RightThigh -> RightShin -> RightFoot
```

No clavicle or fingers exist. Scapula is a single surrogate transform from a manually estimated medial origin to shoulder, not a source skeletal scapula bone or a constrained scapulothoracic articulation. SpineRoot and Thorax share their rest origin; their tail directions/lengths differ in Blender. The exported hierarchy uses a nonconnected Thorax child. Left naming lacks the `Left` prefix on humerus/forearm; right naming has it. Tests depend on those legacy names.

## Actual rest transforms and axes

These are **unanimated GLB default-node values**, not anatomical rest and not frame-0 animation evaluation. The raw observation also separately reconstructs inverse-bind-derived joint world transforms (`inverseBindDerivedWorld` = inverse exported IBM in the asset scene frame); maximum matrix-element discrepancy from default-node world is 1.390e-7 for curl and 1.243e-6 for pulldown. This numerical agreement supports a shared exported bind/default reference within float precision, not a clinically neutral pose. Both are distinct from animation time0; no time0 animation evaluation is claimed here. Pulldown frame0 is already raised/seated and must not be confused with the source bind reference. Positions are metres in exported glTF Y-up coordinates. Complete precision, local transforms, rotations and all right/leg bones are in JSON.

| Joint | curl default-node world origin | pulldown default-node world origin |
|---|---|---|
|SpineRoot|absent|(0,.895,.313)|
|Thorax|absent|(0,.895,.313)|
|LeftScapula|absent|(.055,1.165,.228)|
|UpperArm|(.173,1.305,.067)|(.173,1.250,.280)|
|Forearm|(.213,1.034,.060)|(.213,.979,.273)|
|LeftHand|absent|(.231,.747,.318)|

Pulldown bodyTranslation in Blender is `(0,-.213,-.055)m`; its exported displacement relative to curl is `(0,-.055,+.213)m`. Thus world-origin differences are not changed arm lengths. UpperArm-to-Forearm rest separation is ~.2740255m; forearm-to-hand/wrist ~.237008m. Actual Forearm local translation is approximately `(0,.2740255,0)` in both assets; the parent's +Y follows its rest segment. Local +Y and world +Y are not interchangeable.

Selected actual default-node world bases, rounded (each vector is a **column**, i.e. local axis expressed in asset world):

|Joint|+X|+Y|+Z|
|---|---|---|---|
|curl UpperArm|(.979223,.140764,.145972)|(.145972,-.988959,-.025545)|(.140764,.046322,-.988959)|
|curl Forearm|(.992880,.091765,.075947)|(.075947,-.978868,.189867)|(.091765,-.182747,-.978868)|
|pulldown Thorax|(1,0,0)|(0,1,0)|(0,0,1)|
|pulldown LeftScapula|(.119954,-.633931,.764030)|(.764030,.550360,.336691)|(-.633931,.543355,.550361)|
|pulldown LeftHand|(1,0,0)|(0,-.855915,.517116)|(0,-.517116,-.855915)|

Pulldown humerus/forearm default-node world bases match curl to floating-point export precision despite different ancestors. For example curl UpperArm world XYZW is `(.994628164,.072071193,.072071185,-.018063862)`; Forearm `(.993807898,.042189103,.042189103,.093733775)`. Pulldown LeftScapula is `(-.069341219,-.469053859,-.469053948,.745096410)`. Rest quaternions are not animation deltas. Their signs may be negated without changing rotation. glTF stores XYZW; Blender Quaternion construction takes WXYZ. Directly copying arrays is incorrect.

Generator facts: source import is explicitly reset, each source vertex remapped `(x,z,-y)/1000` into Blender Z-up metres; glTF export has Y-up enabled. The `/1000` is an implemented scale, not independently measured anatomy. Blender edit-bone +Y is head-to-tail; X/Z roll is Blender construction behavior, not annotated anatomical axes. Curl creates global Blender-X flexion and conjugates through forearm rest quaternion. Pulldown creates target directions with shortest-arc rotation differences, then computes local pose against parent. It lacks an independently defined humeral axial rotation reference; direction-only placement does not determine an anatomical three-DOF shoulder frame. Its chest X rotation, scapular Y rotation and hand Y rotation are authored world operations, not named physiological rotations.

## Source geometry, hands, corrections and duplication

Both builders assert the same original source SHA and preserve sourceName/FMA/BP metadata. They independently duplicate import/reset/unit conversion, landmarks, smooth interpolation, weight-region classification, animation sampling, bone binding and export settings. Curl affects only 55 primitives, uses a two-bone elbow transition and 22 corrected muscle primitives: 20 have three ElbowCorrective targets; two biceps have four targets including an artistic bulge. Pulldown skins the entire body and markers, with ten muscle primitives each carrying 21 CuffDQ pose targets. These incompatible morph spaces must not be treated as transferable channels.

Pulldown uses attachment proxy regions for eight cuff muscles, hand/forearm mixed palmaris, whole-hand controls and spatial-side correction for two mislabeled flexor-pollicis meshes. It does not change source identity to repair labels. Actual weighted influences and source names in JSON allow migration comparison; bone renaming without updating JOINTS indices/skin ordering and all animation targets would break it. The current DQ target -> inverse LBS pre-skin correction has a nonsingularity assert, sampled validation and linear adjacent morph blending. It is a portable artist/engineering correction, not tissue strain simulation. Curl's correction is a different quaternion bend envelope with a global-X assumption. Reuse the numerical inversion/check infrastructure only after new bind frames/weights and motion are frozen; old morph deltas cannot simply survive a new skeleton.

Hands are unchanged source anatomical meshes, no surface skin or digits. Curl has no separate wrist articulation; pulldown has rigid whole-hand controls. Rigid hand transforms cannot close an open source hand. The upgraded dumbbell helper and pulldown configuration/machine linkage are reusable; preserve their geometry and common timing, then adapt attachment matrices explicitly. Marker equality is an attachment synchronization test, not real hand contact.

## M2 evidence preserved

Read baseline M1 summary, cycle1 candidate summary and all four final cycle2 reports plus M2 summary. The final candidate is the same pulldown SHA audited here. Final biomechanics and visual verdicts FAIL; science and QA overall INCONCLUSIVE. P1 bilateral source adductor-pollicis triangle116 lies ~.356mm from grip axis versus 24mm handle radius, ~23.645mm deep, across sampled phases. No new grasp verdict is inferred from this structural inspection. Calibrated attachments, axillary strip attribution, loaded support and controlled performance remain evidence gaps. Local palmaris folds persist. Two automatic M2 cycles are exhausted; V2 authorization is not M2 release, a third automatic repair cycle, or permission to change hands. Reports and failing assets must remain as independent references.

## Migration recommendation and routes

1. **Preferred: one source-preserving canonical bind rig plus exercise adapters.** Share import/source identity, metric reference landmarks with uncertainty, hierarchy definitions, equipment anchor interface, weighting utilities, validation and bake/export. Keep animation, weights/correctives, material states and training data separate. Publish Mac numeric observations for Windows to map and approve rather than guessing OpenSim angles. This costs explicit rebind/retarget work, but removes duplicated landmark/axis assumptions and supports both existing actions.
2. **Alternative: retain two legacy rigs behind one runtime adapter.** Lowest short-term asset risk, useful as comparison fixtures. It keeps contradictory controls/morph spaces and cannot substantiate a unified anatomical rig; use only as an explicit transitional compatibility layer.
3. **Avoid: rename nodes and graft a Thorax/Scapula parent onto curl in place.** Existing world bind and local animation deltas are different. Preserving apparent static positions alone does not preserve inverse binds, exported animation, source geometry contact or corrective targets. This offers no durable evidence of anatomical unification.

Proposed discussion names: `root`, `pelvis`, `thorax`, `clavicle_l/r`, `scapula_l/r`, `humerus_l/r`, `forearm_l/r`, `hand_l/r`, `femur_l/r`, `tibia_l/r`, `foot_l/r`; distinct controls and deformation bones if needed. Treat clavicle/pelvis as proposed capabilities absent from legacy, not discovered anatomy. If radius/ulna split, wrist DOFs or fingers are needed, agree anatomy/landmark and user geometry scope before implementation. Keep persistent anatomy IDs untouched; maintain an explicit legacy-name mapping.

Reference-pose proposal: immutable original-source geometry, one agreed metric model-space origin/frame, explicit source-to-model matrix, and a separately stored exercise placement transform. Record each bone parent and global/local rest matrices, landmark provenance and uncertainty; distinguish bind pose, neutral reference and animation initial pose. Do not silently force T/A-pose or fold source fingers. Windows must define biomechanical coordinate frame and rotation semantics; Mac must map them with numeric basis/round-trip fixtures, never name Blender axes as clinical motion by convention alone.

R0 acceptance evidence next: Windows acknowledgment through GitHub of observed frames/schema ownership; shared name/frame contract; source-triangle identity comparison; bind and zero-motion round-trip; exact legacy curl/pulldown comparison fixtures; independently reviewed joint and contact outputs. Build/unit/real browser checks remain mandatory for future functionality claims. This audit itself makes no working-functionality or release claim.

## Task accounting

Completed: actual binary inventory, local/world transforms and basis extraction, weighting/morph/animation inventory, source/generator/report comparison and canonical migration recommendations. Workarounds introduced: none. Permanently resolved debt: none claimed. Deferred/accepted debt: existing M2 failures remain deferred by their owners; this audit creates no acceptance or production workaround. Remaining risks/evidence: Windows frame agreement, calibrated anatomy and contact, preserving existing equipment/hand constraints, correct rebind/retarget and independent V2 milestones. No production file, source geometry, hand, old report or release gate changed.
