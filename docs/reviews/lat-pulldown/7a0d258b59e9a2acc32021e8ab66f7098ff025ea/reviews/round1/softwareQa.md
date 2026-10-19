# Independent blind software QA, first round

Target commit: `7a0d258b59e9a2acc32021e8ab66f7098ff025ea`.
Actual pulldown GLB SHA256 personally recomputed: `56b3ca231dda14100d64233758da2116282547b472afd4fc9b24160f345fee05`.
Evidence packet: `artifacts/blind-review/7a0d258b59e9a2acc32021e8ab66f7098ff025ea/` (below, P/).
No historical evidence, old reviews, debt files, other reviewer findings, or README consulted. No implementation/asset edits. Scope is S01/S02 software behavior; this report makes no anatomical, clinical, or overall milestone PASS claim.

## Bounded verdict

- S01: **PASS**, bounded to GLB load/structure, 467 distinct source mappings, actual production picking/style, shared-time scene transforms, seek/pause, looping, and exercise-switch checks represented below. Endpoint replay inconvenience is P2.
- S02: **PASS for executed functional checks**, with **performance suitability INCONCLUSIVE**. Fresh supplied build/asset/browser runs pass; own unit/browser diagnostics show no page errors. Measured rendering is slow, but no product FPS target or comparable prior baseline exists, so neither a performance regression nor acceptable target-device performance is established.
- P0/P1 software blockers: none established within this scope. This is not permission to merge or mark anatomical acceptance.

## Personally executed

1. Read `src/`, relevant `scripts/` and `tests/`, plus own-role TOML and neutral workflow/contract from P/protocol. Verified mixer uses `setTime(min(time,4))` and updates world matrices (`src/three/Scene.tsx:50-56`); both machine and human inherit the same scale/translation (`:84`). Machine time reads same store (`src/three/LatPulldownMachine.tsx:30-31`). Clock advances after rendering callbacks in the same frame registration order; fresh production transform evidence confirms bounded practical alignment, rather than assuming synchronization from shared variables alone.
2. Parsed actual GLB with Three GLTFLoader and recomputed hash. Result: 467 source meshes, 467 distinct source names, 469 SkinnedMeshes, one 4-second clip with 48 tracks. Actual production React/Fiber scene traversal: 467 source meshes, 467 distinct anatomyIds, zero missing catalogue entries. This validates identity preservation, not anatomy correctness.
3. Ran `npm test` in frozen worktree: exit 0, 2 files / 9 tests passed (2026-10-15 14:26 local).
4. Launched fresh Chrome/Playwright context against production `http://127.0.0.1:5183`. Loaded pulldown, sought to 4, disabled loop, clicked play: time remained 4 and play button returned immediately (finding QA-01). Sought to 0 and exercised .25× and 2× playback/pause: both advanced with zero pageerrors. Timing affected by frame/UI scheduling, so raw slider observations (.4 and 3.25 after requested 800ms waits) are not treated as precise wall-clock speed measurements.
5. Independent production paused full-view rAF probe, 1440×1000 Chrome: 42 frames / approximately 3 sec, mean 72.876ms, p95 83.4ms; 507 draw calls, 1,093,414 triangles. No implementation hooks changed; external Fiber read only. Orchestrator confirmed this probe overlapped active capture; concurrent load was uncontrolled. This is rAF latency, not GPU elapsed time. See QA-02.

## Supplied fresh results personally inspected, not personally rerun

P/checks.json and P/logs: npm ci, build, unit, assets, curl rig, pulldown rig and browser runs supplied by orchestrator; checks exit 0, browser 3/3 passed. I did **not** personally execute build, npm ci, validator scripts or repository browser suite; those scripts write repository docs/evidence, which my assignment prohibited. Unit run above is independent.

P/capture-metadata.json: 50 production frames (2 styles × 5 views × 5 phases), 27 non-monotonic scene seek samples, errors=[], actual latissimus pick produces `z-anatomy:unmapped:left_latissimus_dorsi`, style switch retains same details, pauseStable=true, looping at 2× wraps, non-loop endpoint time=4/stopped=true. Maximum supplied actual skinned **contact-marker** to machine target difference is 0.000041024m in scene coordinates. This is marker alignment only, not original palm clearance or valid grip anatomy. Supplied paused back-view baseline: mean 63.625ms, p95 66.7ms, 475 draw calls, 1,092,338 triangles on ANGLE Apple A18 Pro. P/full-rep.webm exists (12,883,183 bytes) with P/video-timeline.json. Video existence is verified; orchestrator declared EvidenceREADY with finalized 47.32-second native recording, all 50 frames, 27 seeks and 121 trajectory samples. No visual/anatomical approval inferred.

## Findings

### QA-01 — P2: play cannot restart a finished non-loop repetition

Evidence/locations: `src/main.tsx:25` toggles only playing; `src/three/animation.ts:3` clamps time at 4; `src/three/Scene.tsx:67` immediately clears playing at time=4. Personally reproduced in fresh production browser: load pulldown, disable loop, seek 4 (or let repetition finish), click ▶, wait 250ms; slider remains `4`, ▶ is visible again, no replay occurs. Expected usability: replay begins from zero, or a distinct restart control communicates the required action. Current manual seek-to-zero remains functional. Confidence high. Suggested regression: finish non-loop clip, click play, assert time advances from start and scene moves. This is a reproducible inconvenience, not a nonfunctional playback system.

### QA-02 — P2 observation: expensive paused rendering and missing performance acceptance budget

Evidence/locations: `src/three/Scene.tsx:51-56` runs mixer, skeleton update and per-skinned-mesh `computeBoundingSphere()` every frame even when paused; `:25` disables skinned frustum culling. The 469-skinned-mesh asset makes this a plausible CPU cost; no profiler attribution was performed, so exact cause is unproven. Own paused full-view mean 72.876ms/p95 83.4ms; supplied back-view mean 63.625ms/p95 66.7ms. These establish approximately 14–16 rAF frames/sec in those sessions, not a regression or device-independent FPS ceiling. Confidence high in observations, medium in cost attribution. Reproduce: production pulldown at 1440×1000, paused, sample 3–4 seconds rAF intervals and renderer info. Next verification: isolated target-device run with agreed frame budget and profiling; compare paused/moving, identical camera/style/dpr, and mesh/picking correctness. No optimization or fallback introduced by reviewer.

## Coverage limits

Existing browser suite tests screen differences, labels and pause; it does not assert precise speed ratios, loop boundary pose continuity, repeated GLB mount disposal, bilateral individual source-mesh pick correctness, or minimum FPS. Supplied 27 actual-scene nonmonotonic seeks mitigate clock/seek coverage; supplied lat pick/style supplements generic suite. No long-duration memory leak claim, controlled GPU profiling claim, or visual geometry approval is made. Root scale means source-metre trajectories and displayed scene-metre values must remain separately labeled.

Primary goal completed: independent S01/S02 bounded audit of frozen software and fresh packet. Workarounds introduced: none. Permanently resolved debt: none (review only). Deferred/accepted debt: no reviewer debt created; QA-01/QA-02 remain review findings, not fixes or accepted risks. Remaining evidence: controlled performance budget/baseline if smoothness acceptance is required; anatomical/visual gates belong to independent domain reviews. USER APPROVAL: pending.
