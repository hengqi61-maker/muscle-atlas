# Workaround debt · Muscle Atlas · 2026-10-15

## WD-2026-10-15-0001
Status: DEFERRED
Title: MODEL-DOWNLOAD
- Original failure: curl -L --fail https://raw.githubusercontent.com/JohanBellander/BodyExplorer/main/public/anatomy.glb -o public/models/anatomy.glb returns35, recv connection reset, 0 bytes.
- Reproduction: initial exact path and subagent curl -I raw endpoint both reset. API HTTP200; Pages HTTP200; urllib full payload fast.
- Temporary workaround: complete independent prototype; download via upstream Pages/urllib, match GitHub API blob SHA1. Superseded project downloader is now fixed-hash atomic importer (no retries); this does not repair system curl/raw transport.
- Paths compared: fix raw network route (would affect broader system, cause still ambiguous); API large raw response (~50KB/s, interrupted); official Pages + urllib + blob integrity (full25MB verified in seconds, selected project import).
- Evidence: anatomy blob a112885444785a9dd93c5753b46ac790e6e036b3; mapping6e702859c44aa0a36eb3b44d988076c48675c493; script/inspect report. No proxy settings or credentials changed.
- Unresolved cause/impact: client-endpoint transport reset, project works offline with verified bundled assets; raw curl not durably fixed.
- Reason deferred: not required for local runtime; broader system network investigation beyond this delivery.
- Next action: compare curl/urllib TLS/proxy route without secrets, then exact original path and clean trials.
- Reopening trigger: downloader/hash failure or another required raw/curl task. No claim of permanently resolved network debt.

## WD-2026-10-15-0002
Status: RESOLVED
Title: DEPENDENCY-AUDIT
- Original failure/repro: npm audit --json original Vitest3.2.7 found3 vulnerabilities (mocker/tinypool, 2 critical).
- Workaround: none; no test server exposed.
- Cause: initially selected older major-version range.
- Paths: patched Vitest5.0.4 versus overriding incompatible nested dependencies; supported upgrade chosen.
- Durable fix: upgrade direct dependency and lockfile; no forced overrides.
- Evidence: npm audit0 vulnerabilities; unit suite on upgraded version passed; clean browser test server restarted.
- Impact: developer test toolchain; resolved, no retained bypass.

## WD-2026-10-15-0003
Status: RESOLVED
Title: LOADING-DOM
- Original failure/repro: Playwright original test captures removeChild DOM exception when Drei Html Suspense portal unmounts under React StrictMode.
- Workaround: none; error assertion and StrictMode retained.
- Paths compared: disable StrictMode (masks lifecycle); change portal library; DOM-owned loading overlay outside R3F Canvas (chosen).
- Durable fix: Canvas Suspense fallback null; useProgress drives regular React DOM sibling. ErrorBoundary shows explicit model failures.
- Evidence: original browser flow passed with zero pageerrors after clean Vite restart; no mock/skipped assertion.
- Impact: model-loading transition fixed.

## WD-2026-10-15-0004
Status: RESOLVED
Title: BLENDER-PATH
- Original failure/repro: unsaved startup bpy.path.abspath('//public/models/anatomy.glb') had no saved .blend base; importer Please select a file.
- Temporary workaround: MCP script uses verified absolute source path. MCP saveTo follows server's other project workspace; copied resulting .blend to this project's artifacts without deleting source evidence.
- Cause: assumption that relative blend paths / server workspace equalled chat cwd.
- Paths: reconfigure global MCP working directory versus independent root-derived project bpy script. Independent scripts/blender-import.py chosen to avoid changing other project configuration.
- Durable fix: project script resolves root from __file__, asserts input exists, saves artifacts/anatomy-import.blend and docs/blender-inspection.json under this repository.
- Evidence: /Applications/Blender.app/Contents/MacOS/Blender --background --python scripts/blender-import.py clean launch exit0;467 Mesh,0 Armature, saved local .blend. No dependency on MCP workaround remains.

## WD-2026-10-15-0005
Status: DEFERRED
Title: MODEL-RIG
- Original limitation: sourced anatomy GLB contains0 skins/0 animations; imported Blender scene0 armatures. Cannot use native rig/clip that does not exist.
- Temporary workaround: visibly labelled procedural joint prototype, independent meshes; no anatomical skinning claim.
- Paths compared: manual local two-bone independent-muscle skinning (closest goal, unverified joint quality); static anatomy plus separate motion rig (easy but cannot deliver dynamic anatomy); full atlas Rigify auto weights (large scope, not proof of attachment correctness).
- Impact: real anatomy is static; current curl only proves hierarchy joint motion. Prototype satisfies explicitly allowed first-delivery alternative.
- Reason deferred: actual anatomical rigging is next technical stage, not supplied by free asset.
- Next action: single-arm two-bone weight/shape-key experiment and GLB AnimationMixer verification per docs/model-pipeline.md.
- Reopening trigger: start P2 true-rig milestone. No accepted-risk approval or claim of complete dynamic anatomy.
