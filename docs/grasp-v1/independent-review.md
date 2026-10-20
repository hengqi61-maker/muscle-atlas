# Independent engineering review — Grasp v1

Reviewer: Cursor TL on the same machine, after the build, using raw outputs (not the README first). Not a Codex substitute review and not Owner approval.

**PASS (limited): controller drives real skinned vertices on an isolated copy.**

- Re-read `verify-deform.json`: imported export GLB has 30 finger bones; left lumbrical weight mass on new bones is nonzero; evaluated max displacement 0.0485 m after +1.1 rad.
- `three-smoke.json`: `GLTFLoader.parse` found 30 finger bones; `applyToObject3D` hit 30 for open and closed.
- `build-report.json` identity: 467 source POSITION SHA unchanged.
- Unit tests 3/3.

**FAIL / UNKNOWN (must stay visible)**

- Build-time prop distances did not use evaluated meshes; identical across presets. Cannot claim posed bar/rope grasp contact.
- Source has no finger skin; visible “fingers” are tendon/muscle strands. Gross curl is modest in the published stills because of camera and topology.
- Historical pulldown/curl geometry FAIL is untouched.

No production file was modified by this review.
