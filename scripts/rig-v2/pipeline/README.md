# E3 isolated motion production

This pipeline reconstructs a fresh scene from the immutable original GLB, the existing canonical27-bone JSON and all467 explicit per-vertex registry weights. It does not call the earlier hardcoded builder. Both authored R1 clips were observed from the frozen native scene into the versioned input JSON; the original native input has a public release URI, archive SHA and member name. Reproduction needs no external native file.

```sh
python3 scripts/rig-v2/pipeline/build_motion.py --definition config/rig-v2/motions/curl-probe.json --output artifacts/motion-pipeline/run-a
python3 scripts/rig-v2/pipeline/build_motion.py --definition config/rig-v2/motions/curl-probe.json --output artifacts/motion-pipeline/run-b
python3 scripts/rig-v2/pipeline/compare.py artifacts/motion-pipeline/run-a artifacts/motion-pipeline/run-b --output artifacts/motion-pipeline/comparison.json
node --test tests/rig-v2/pipeline.node.mjs
```

Requires Blender5.2 and ffmpeg; change executable locations in the definition for another host. All scientific inputs are repo-relative and fixed by SHA256. Output directories must be fresh. Each build exports GLB/nativeBlend, actual121-frame world transforms, exact source vertex and face proof, five-phase full-triangle area/stretch diagnostics,50 native PNGs (five phases × five views × two materials),31 native video frames and an H264 MP4. `Real` retains original source materials; `Clean` is a plain diagnostic material. Hand views track actual original hand bone positions; they do not demonstrate validated grip.

Predeclared tolerance2e-5 matrix elements/metres; original float32 base geometry and identities require exact hashes. GPU pixel and Blend file byte equality are not promised. Geometry alarms retain area<.05 and severe count>3 OR>1% and stretch>3; five geometry phases are explicitly limited and do not replace the existing121-phase R1 audit. No finger posture change, hidden mesh, geometry repair or biomedical claim is made. BUILD_PASS is separate from geometry and four independent reviews/owner approval.

The first attempt exposed Blender's default successful process exit after a Python exception and an implicit-world-node assumption. Failed output is retained separately. The durable builder explicitly creates the world shader/output nodes and passes `--python-exit-code 1`, so a native exception blocks encoding and PASS manifest creation. This is preferable to relying on a startup template world or grepping log text.
