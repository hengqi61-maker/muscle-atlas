# Isolated real Three.js consumer

From repository root after a fresh Blender pipeline output exists:

```sh
E3_BROWSER_ASSET=artifacts/motion-pipeline/run-a/motion.glb E3_BROWSER_OUT=artifacts/motion-pipeline/run-a/three-consumer E3_BROWSER_TIMEOUT_MS=300000 node --test tests/rig-v2/pipeline-browser.node.mjs
```

Use run-b for the independent second build. A two-clip frozen protocol may use a 600000 ms harness deadline. The deadline is a workload budget, not FPS, geometry or medical acceptance. No fallback renderer or anatomy replacement is used. Chrome is explicitly selected; missing Chrome or invalid GLB fails.

The thin native Three page consumes that exact derived GLB through GLTFLoader and AnimationMixer. Per clip it samples 121 actual seeks; midpoint bounds are compared against standard Three SkinnedMesh box/sphere computations within 1e-12 m. Exact posed bounds use each actual skinned vertex once, preserving stock box.expandByPoint and sphere.expandByPoint order; identical pose/camera/material updates reuse the exact result. Frustum culling remains enabled.

It saves 50 PNGs: five phases × front/side/back/left-hand/right-hand × source/clean materials. Source hands are not repositioned or replaced. The actual complete-cycle WebM uses canvas.captureStream and MediaRecorder while AnimationMixer executes the full timeline, and the separate Playwright WebM records the whole test. Wall-clock playback may exceed clip duration under exact bounds checks; no realtime-FPS conclusion follows. Real canvas clicks return original sourceName/FMA/BP plus triangle faceIndex. This proves source-triangle picking, not anatomical grip quality.

Reports record asset/test/viewer SHA256, Node/Chrome versions, 121 seek count, paused freeze, terminal playback time, actual pick and relative video path. Startup logs freeze exact test/viewer hashes before browser launch. Cancellation closes browser resources and cannot emit a late PASS report. Historical failed experiments remain in evidence; only a zero-exit test plus its matching report is accepted.
