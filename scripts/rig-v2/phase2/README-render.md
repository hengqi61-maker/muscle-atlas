# Phase 2 native render evidence

These scripts import the actual GLB into Blender 5.2, preserve its two imported NLA Action slots, and evaluate one clip track at a time. They do not edit source geometry, weights, joints, original fingers, animation channels or production assets. Fixed neutral Clean material, lighting, 512px resolution and 8 EEVEE render samples are identical across assets. This is engineering diagnostic evidence, never anatomy approval.

## Reproduce (fresh output directories required)

```
python3 scripts/rig-v2/phase2/run-render.py --output artifacts/phase2/camera-calibration-v2 --calibrate public/experimental/rig-v2/unified-rig-prototype.glb artifacts/phase2/E01-local-gradient/motion.glb artifacts/phase2/E02-elbow-axis-basis/motion.glb
python3 scripts/rig-v2/phase2/run-render.py --asset public/experimental/rig-v2/unified-rig-prototype.glb --contract artifacts/phase2/camera-calibration-v2/camera-contract.json --output artifacts/phase2/native-camera-smoke --smoke
python3 scripts/rig-v2/phase2/run-render.py --asset public/experimental/rig-v2/unified-rig-prototype.glb --contract artifacts/phase2/camera-calibration-v2/camera-contract.json --output artifacts/phase2/native-baseline-v5
python3 scripts/rig-v2/phase2/run-render.py --asset artifacts/phase2/E01-local-gradient/motion.glb --contract artifacts/phase2/camera-calibration-v2/camera-contract.json --output artifacts/phase2/native-E01
python3 scripts/rig-v2/phase2/run-render.py --asset artifacts/phase2/E02-elbow-axis-basis/motion.glb --contract artifacts/phase2/camera-calibration-v2/camera-contract.json --output artifacts/phase2/native-E02
```

Each complete render produces a new scene.blend, 121 actual world bone matrices per clip, six camera views × five key poses per clip, 31 actual native frames per complete-cycle MP4, tool versions and SHA256 manifests. Nonzero bone-matrix changes are required, not assumed. Source clip timing is imported at 24fps: 96 frames = 4 seconds; video has 31 endpoint-inclusive images at 7.5fps, so encoded duration includes one final frame hold (4.133s). Matrix ordering is explicitly row-major Blender Z-up metres; this is internal evidence, not the Windows interchange schema.

## Fixed camera and exact source boundary

Actual GLB JSON contains **467 mesh nodes / 467 mesh definitions**, each with unique sourceName. Blender additionally creates **Icosphere** as the custom_shape helper for all 27 bones: 42 vertices, 80 triangles, linked to glTF_not_exported collection. Thus bpy.data contains 468 mesh objects; the helper is not source anatomy or a prop and is not rendered. Its collection visibility is preserved. The earlier ad-hoc count 469 also included Blender's default Cube; that was an inspection-state mistake, not a source asset.

Calibration measured 3 assets × 2 clips × 121 evaluated poses in 28.67 seconds. At each clip's first pose, every evaluated mesh bbox was checked against the extrema of its actual evaluated vertices: all errors 0 metres. The contract conservatively includes the importer helper bounds as well as all source anatomy, leaving unnecessary empty space; **this limitation is retained consistently across all three candidates**, not concealed by deleting an object or recentering each asset. camera-contract-notes.json and baseline scope-correction.json clarify the original overly broad wording “visible meshes”.

Global projected union plus fixed 10% margin gives maximum conservative normalized extent 0.9090909 and zero full-body clipping. Front/back/side share scale and target. Local shoulder/elbow views use the baseline joint positions stored per phase in the same immutable contract; candidates never receive their own zoom or recenter. Source input SHA must match one of the three measured assets.

Three actual smoke images were viewed before full rendering. Bright tissue pixel ranges on 512px images: front y40–334, back y31–330, side y30–333. Independent actual all-vertex projection in the saved scene yielded normalized extent 0.8757514. This confirms containment only, not anatomical or visual quality. Source-hand posture remains unchanged.

## Preserved failures and engineering trade-offs

- native-baseline: stopped at mistaken total-mesh==467 assertion; replaced with strict 467 unique sourceName validation.
- native-baseline-v2: Blender 5.2 did not automatically create Principled shader node; explicit node construction/linking fixed original path.
- native-baseline-v3: partial 64-sample high-cost run explicitly stopped by coordinator, not marked complete. Actual factory sample count was queried as 64; images took ~40 seconds under concurrent full-geometry CPU scans. Compared A retaining 64 samples (~4h estimated), B identical 8 samples for every asset (chosen), C reducing resolution (rejected because local detail would weaken). Final baseline-v5 ran in71.59s after competing CPU scans finished, so the whole speedup cannot be attributed solely to samples. Sampling does not change any geometry threshold.
- native-baseline-v4: old camera calculation before individual NLA activation caused framing problems. Preserved as historical output, not final full-body evidence.
- camera-calibration: initial wrapper double-required nonexistent output before any import. Outer fresh-output gate retained; inner mkdir permits the outer-created directory. Original error log retained.
- A transient manual impression that the new smoke back view was clipped was disproved by exact pixels (31px top margin) and direct vertex projection. No camera change was made from that mistaken impression.

Low-sample diagnostic images and conservative empty framing remain limitations for independent reviewers to assess. They may judge visual sufficiency INCONCLUSIVE. Build/render completion never means geometry or biomechanics passed.

## Actual completed runs

- native-baseline-v5: 71.586117667s, original manifest130 files verified by SHA.
- native-E01: 58.538284s, original manifest132 files verified by SHA.
- native-E02: 79.227559625s, original manifest132 files verified by SHA.

Each contains 122 actual PNGs (2 × [30 keyframes +31 sequence frames]), two actual 31-frame H264 videos, and two121-pose trajectories. Every clip sequence has31 distinct PNG file hashes but16 distinct actual pixel arrays, as expected for an endpoint-inclusive symmetric return cycle; nonzero actual bone matrices and changing pixel arrays prove genuine motion. final-inventory-v2.json preserves the initial final snapshot; final-inventory-v3.json additionally includes the lossless sequence-pixel check and previous inventory SHA. Original manifests/reports/digests are unchanged.

The actual full-body videos of E01 are byte-identical to baseline despite the failed internal mesh geometry experiment. Lossless pixel comparison explains why:110/122 PNGs have exactly equal pixel arrays; remaining12 images differ by at most6 pixels and4 channel levels, which H264 quantizes away. PNG file hashes differ because of metadata; they are not used to falsely assert visual motion differences. E02 changes substantial image content (up to33921 pixels,199 channel levels;14/122 pixel-identical). The root-level native-render-comparison.json records each image. A visually unchanged outer surface cannot validate deep muscle attachments or rule out severe internal mesh distortion; numerical all-triangle checks and focused source-mesh evidence remain necessary.
