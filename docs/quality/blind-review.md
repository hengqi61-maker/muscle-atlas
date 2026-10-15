# Frozen motion audit / reusable pilot commands

Production candidates are immutable Git worktrees. Infrastructure lives on a separate branch. PR#2 is the starting protocol, not permission to merge. Its13 changed files were inspected; its runtime/model tree matches7a0d258 exactly.

## Roles and isolation

Orchestrator, Rigging Engineer and four reviewers have project TOML definitions. Actual review execution in this desktop session uses real `collaboration.spawn_agent` calls, `fork_turns=none`, with corresponding role files/instructions. This is not in-context roleplay. Only3children may run simultaneously, so schedule the fourth later. Role instructions are not OS-enforced read-only sandboxes.

TOML syntax/required role fields were parsed with Python3.12. The system CLI fails ENOENT for its packaged native binary; configuration auto-discovery in that CLI has NOT been runtime verified. Official docs direct fetch also failed. Do not claim these uncertain settings are validated or silently change global installs. The desktop-native child-agent mechanism actually works.

Before first report freeze, allow only source code/assets, the new evidence packet and neutral acceptance contract. Exclude old docs/evidence, reviews, workaround-debt findings, README historical narratives and other reviewers' results. Each reviewer declares inspected inputs; preserve a SHA256 of the first report. Only after all four reports are frozen does the orchestrator compare historical records. Preserve original reports verbatim; disagreements and corroborations go into a separate reconciliation document.

## Commands

Run infrastructure tools while passing the immutable candidate directory. All paths below are placeholders supplied by the operator; use full40-character SHA.

```sh
node scripts/quality/motion-audit.mjs freeze --worktree /absolute/candidate --ref FULL_SHA --out /absolute/evidence --asset public/models/anatomy-pulldown.glb
node scripts/quality/motion-audit.mjs measure --worktree /absolute/candidate --ref FULL_SHA --out /absolute/evidence --adapter lat-pulldown
node scripts/quality/motion-audit.mjs mesh-kinematics --worktree /absolute/candidate --ref FULL_SHA --out /absolute/evidence --adapter lat-pulldown
```

After a fresh `npm ci` and `npm run build` in candidate, start Vite production preview with a dedicated strict port. Actual video capture requires the installed Chrome channel and the Playwright-version-matched ffmpeg runtime. Do not replace a failed capture with interpolated imagery.

```sh
node scripts/quality/motion-audit.mjs capture --worktree /absolute/candidate --ref FULL_SHA --out /absolute/evidence --adapter lat-pulldown --url http://127.0.0.1:PORT
node scripts/quality/validate-review-bundle.mjs /absolute/evidence/manifest.json
node scripts/quality/gate.mjs /absolute/evidence/manifest.json
node scripts/quality/gate.mjs /absolute/evidence/manifest.json --release
npm run test:quality
```

Freeze checks working file hashes against Git blobs and copies the animatedGLB plus source code archive. Missing tracked authoring.blend is recorded, not invented. Mesh measurement evaluates all467source meshes at21times; records actual deformed bounds/centroids/vertex displacement, skin-bone weight means and point-inside-platform tests. Joints are sampled121times. A zero point-intersection count does not prove triangle clearance; displacement is not activation. Quaternions need anatomical calibration before pronation/scapula validity claims.

Capture uses the unchanged production renderer. External camera-only access to the live R3F state gives reproducible poses; UI interactions drive native seeking, styles, picking and playback. Videos are actual screen recording, not frame interpolation. Metadata records the camera, occlusion presets, pageerrors, controls and rAF latency. Browser console warnings and full active-frame speed fidelity are not presently exhaustively covered; mark limitations honestly. A paused/capture-contended rAF baseline is not a controlled GPU benchmark.

The supplied adapter is specific to seated lat pulldown. New actions require a new adapter defining source asset, exercise selector, timeline, cameras, joint landmarks and equipment/contact targets, plus their own neutral acceptance contract. Common freezing, provenance, review schema and release gates are reusable. No Face Pull animation or unimplemented adapter is claimed.

## Gate semantics

A completed audit may contain FAIL/INCONCLUSIVE. Release additionally requires four PASS, distinct reviewer sessions, no producer self-review, no unresolvedP0/P1, owner approval and evidence reference, and no more than two rework cycles. A JSON field is not authentication: humans must verify that the owner approval reference is real. The software cannot manufacture or substitute that approval.

PR creation, public upload and merging are separate actions. This pilot does not merge PR#2 or main. After M1 stop for owner scope approval. Test output is evidence, never automatic professional signoff.

`node scripts/quality/next-action.mjs manifest.json` emits the authorized next step: M1 always waits for owner, approved M2 may assign scoped production then freeze/review a new candidate, two cycles force escalation, clean candidate still waits for M3 approval. Actual agent dispatch is by the working desktop collaboration runtime; the broken global CLI is not silently used as an automation backend. The recorded repair scope must come from the human, not a producer-written flag. No repair was run in this blind audit.
