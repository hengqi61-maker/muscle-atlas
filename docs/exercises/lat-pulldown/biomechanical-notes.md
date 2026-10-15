# Biomechanics authoring notes

Status: reference authoring for current M2, **not release approval**. Reviewed against source commit `9c9c97125c1ea902478894f164669764677d3563` on 2026-10-15. `kinematics.json` is a reusable authoring contract; it does not replace the current rig or certify its anatomy.

## Evidence boundaries

The independently retrieved [Ludewig and Reynolds review](https://pmc.ncbi.nlm.nih.gov/articles/PMC2730194/) describes three-dimensional scapular/clavicular motion during arm elevation. It supports allowing coordinated scapular movement, and cautions against treating internal/external rotation as a single universal pattern. It does not supply a measured seated pulldown trajectory, phase timing, fixed ratio, or a safe joint-angle cutoff. Metadata and retrieval status belong in `sources.json` (`ludewig-reynolds-2009`). No figure is reproduced.

No external demonstration video was measured by this author. The 0/25/50/75/100 phases are proposed capture points over one complete repetition. They are not percentages of activation, load, range of motion, or observed real-world timing. Current four-second cosine timing is an implementation choice.

## Frames before angles

Use canonical glTF model metres with +X toward the subject's left, +Y superior and +Z anterior. Blender authoring metres use +X left, +Y posterior and +Z superior; conversion is `(x, z, -y)`. The builder's `/1000` conversion applies after Blender imports the source, so raw file arrays must not receive the same transformation without checking the import stage. Preserve model-local, Blender and display-scene measurements separately. The current display transform scales distances by 1.45.

A humeral direction is not a full anatomical orientation. Axial rotation needs a transverse reference such as epicondyles; a scapular frame needs bony landmarks and a defined rotation sequence. Muscle extents and current control-bone names are uncalibrated proxies. Null precision is more honest than a numeric medical error bar without calibration.

## Attachment and deformation review

Read `anatomy.md` alongside the kinematics contract. A shoulder-cuff mesh bridges structures that move relative to each other. Attaching an entire mesh to the thorax freezes its relationship to those structures; moving it wholly with the humerus can detach the scapular side. Blended weights can also collapse volume between divergent transforms. These are digital deformation failure modes, not measured human tissue behaviour.

Compare at least these future maker routes before choosing a repair:

1. Landmark-reviewed attachment regions with deforming shoulder/scapular/humeral segments, smooth weights, and independent topology/continuity checks. This can preserve source mesh identity, but requires trustworthy region annotations; proximity or vertex deciles alone are not anatomical insertions.
2. The same verified attachment regions with pose-dependent corrective deformation or an appropriate muscle/tendon deformation method. This can address cross-joint compression that linear blends cannot, but requires reference poses and export/runtime verification; a visually pleasing correction is not a strain model.

Neither route is selected here. Do not tune a passing compression threshold to the current cuff-weighting prototype. First define independent anatomy/geometry expectations, then evaluate candidate methods at all five poses and throughout transitions. Source anatomy mesh identity and plausible static shape do not establish skinning, fibre mechanics, volume preservation or anatomical deformation.

The original anatomical hands, upgraded dumbbell and pulldown linkage remain outside this reference-only edit. Contact-marker alignment cannot prove palm contact or a closed grip. Any future contact assessment must inspect the original hand surfaces.

## Verification contract

The two numeric tolerances in `kinematics.json` are explicitly proposed double-precision coordinate round-trip and identical-state seek checks, measured in metres. They are software reproducibility tolerances only. They cannot accept anatomy, contact, compression, injury risk, or human movement quality. Future shoulder and support views must document occlusion, FOV, viewport, source scale and phase; image silhouettes without calibration cannot recover joint angles.

Remaining evidence: variant-matched external demonstration, bony/attachment landmark annotations with uncertainty, continuous scapular/humeral observations, and independent cuff deformation review. No new production feature, GLB, action, rig restructuring or FPS claim is made.
