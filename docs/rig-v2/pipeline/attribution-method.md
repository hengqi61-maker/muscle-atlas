# Frozen R1 mesh-level attribution

This experiment reads the immutable R1 GLB with SHA256 `ef803a4bbb3c644504c124519e39ba0b3b760ec139eaf60d277ef7f7f5d23274`. It does not save Blender, change weights, edit source geometry or introduce fingers.

## Reproduce

```sh
node scripts/rig-v2/attribution/analyze.mjs
node scripts/rig-v2/attribution/capture-views.mjs
node scripts/rig-v2/attribution/trace-stretch.mjs
node scripts/rig-v2/attribution/map-source.mjs
node scripts/rig-v2/attribution/render.mjs
node --test tests/rig-v2/attribution.node.mjs
```

Outputs: `artifacts/motion-pipeline/attribution/report.json`, render input and labelled comparison PNGs. The Chrome renderer projects the actual source mesh triangle surfaces in an explicit isolated view; these are diagnostic software orthographic renders, not production whole-body lighting frames. The production pipeline owns the latter.

All exported triangles of all 467 skinned meshes are checked at 121 inclusive time samples per diagnostic clip. The original R1 report sampled at most 1,024 priority triangles per mesh. Therefore new full-coverage counts must not replace or retrospectively reinterpret its recorded **42/121** sampled PulldownProbe failure poses. Both measurements remain valid for their documented coverage.

The unchanged severe engineering screen is area ratio `< 0.05`, with per-mesh alarm `count > 3 OR count / eligible > 0.01`. Source triangles with area at most `1e-14 m²` are excluded from the ratio denominator. Edge ratios ignore source edges at most `1e-8 m`. These numerical guards and alarms are engineering diagnostics, not measured physiological strain tolerances.

Canonical rest means the immutable mesh POSITION reference, not animation time zero. PulldownProbe starts with elevated arms; a failure at frame 0 identifies the first sampled animated pose and does not establish that the original source mesh was defective.

Every detailed event reports GLB triangle index, exported vertex indices, BP/FMA/source identity, immutable canonical coordinates, posed world coordinates, four actual skin influences, and contributing joint world matrices (Three.js column-major 16, column vectors, glTF +Y up/right-handed/metres). Export splits vertices: GLB indices are **not** falsely labelled original Blender polygon IDs. The frozen independent source-preservation proof establishes unchanged source geometry in canonical float32 space; the source correspondence step independently checks selected original source GLB vertex positions and triangle connectivity using exact reproduced float32 normalization. Duplicate-position candidates remain AMBIGUOUS; unmatched points are INCONCLUSIVE. Source GLB indices still do not assert upstream authoring polygon IDs.

## Root-cause hypotheses and durable routes

1. **Reference-calibrated attachment regions and segmented weights.** Locate true scapular and humeral attachment landmarks against licensed anatomical reference; constrain endpoints to the appropriate bone, then use smooth regional transition weights through the muscle belly. This tackles the missing anatomical attachment evidence and can be reused by all clips. It requires independent landmark annotation, bilateral validation and a source-to-export index map; geometric quantiles alone are insufficient. Piecewise rigid transforms can still create folds at boundaries.
2. **Reusable pose-space correction layered over unchanged base geometry.** After attachment-aware weights, author bounded corrections keyed to shoulder elevation/elbow flexion on the same canonical rig, not one arbitrary clip time. Preserve base mesh identity, make correction provenance explicit and test both clips plus interpolated poses. This can improve the axilla/elbow crease but can conceal bad endpoints, overfit probes and produce extrapolation artifacts. It does not establish tissue-force or anatomy correctness.
3. **Rotation-preserving deformation model.** Compare dual-quaternion skinning or a volume-aware deformation solver in an isolated Blender/Three.js roundtrip. This addresses LBS collapse under mixed rotations but changes runtime/export semantics and still needs correct attachments. Do not silently ship Blender-only deformation that glTF/Three.js cannot reproduce.

Choose route 1 with independent Windows/anatomical evidence first, then evaluate route 2 against frozen all-triangle diagnostics and withheld poses. Route 3 needs an explicit runtime/export contract before adoption. No route is implemented here, because current evidence is insufficient to assert anatomical attachment locations. A single shared skin is structurally reusable while failing geometry quality: source identity, two clips and one rig alone do not imply acceptable continuity.

## Remaining limits

Finite-time samples can miss between-sample events. Area compression is not mesh collision, and surface expansion is not muscle activation. This report cannot declare real hand grip, medical correctness, tendon continuity or global collision clearance PASS. No source geometry/continuity/reuse incompatibility is proven: the current LBS construction fails quality, and a non-destructive improvement may still exist.
