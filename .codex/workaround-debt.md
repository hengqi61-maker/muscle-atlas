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

### Reopened 2026-10-15
- User requested both investigations. Original conclusions retained above; no resolution claimed until exact-path and target-renderer evidence.
- Rig paths reconsidered: actual mesh manual two-bone skinning+morph versus rigid mesh parenting versus Rigify auto-weights. Choose manual localized weights, preserving source topology, IDs and attachment endpoints; morph is illustrative, not physiological simulation.

### WD-2026-10-15-0001 · Reopened investigation outcome
- Observed controllable cause: no proxy env; urllib discovers macOS system HTTPS proxy, unconfigured curl does not use it. Keeping curl+original raw URL constant and specifying the discovered per-process proxy gives HTTP200 twice (25,133,568bytes,2.761s/1.079s), both SHA256 match. Exact unqualified raw command now exits28 timeout/0bytes, not historical35 reset. No evidence identifies the network device behind historical reset.
- Paths compared: global curl/env/network reconfiguration (unnecessary cross-project impact); explicit per-command proxy (verified and documented); project urllib/platform proxy + verified offline cache (selected).
- Project reliability permanently improved: fixed SHA256, cache-valid zero requests, max3 attempts bounded backoff, trustworthy206 range only, final hash then atomic replacement. Partial/retry logs preserved; retries are explicitly recovery, not a route fix.
- Verification:8Python tests, real fresh-directory downloads first attempt for both files, separate offline process passes; docs/download-diagnostics.md has commands and route evidence.
- Remaining impact/status: DEFERRED only for original unqualified curl/direct connectivity and historical reset origin. Application loads bundled cache offline; no global configuration changed. Next/reopen: if required raw CLI operation or project importer fails, investigate direct route with explicit scope rather than silently adding retries. This does not block single-arm rig development.

### WD-2026-10-15-0005 · Reopened investigation outcome
- Original ellipsoid hierarchy workaround removed from runtime. Built from unchanged source SHA256:467 anatomical Mesh +3dumbbell Mesh;1skin shared by47SkinnedMesh, UpperArm/Forearm,44anatomical meshes weighted. Two independent biceps morphs and baked elbow corrective shape targets; one4second clip played via actual Three.js AnimationMixer. No Drivers/fake skin or pre-rendered animation.
- Fixes verified:frame0..120 removes measured1/30second export offset; unparented skinned nodes retain modifier/bind, removes47Validator warnings; skeletal clone, dynamic bounds and StrictMode action lifetime support actual paused mesh picking.
- Paths: rigid-parent (doesn't solve tissue deformation), Rigify/automatic weights (unverified attachment), manual two-bone localized weights (chosen); for pinching compare nativeDQ(nonportable currentGLB), custom runtime shader(extra renderer coupling), baked pose-space corrections(portable,chosen). Corrections improve95th-percentile stretch but do not eliminate local compression.
- Evidence:KhronosValidator0errors0warnings; actualThree skeleton angles0/45.003/90.000/120.000deg,normalized JOINTS/WEIGHTS,929mixed brachioradialis vertices,independent morph displacement;2Chrome workflows and0/45/90/120screenshots. Source/script/report paths:docs/rig-verification.md anddocs/evidence/curl-*.json.
- Remaining cause/impact:estimated landmarks/linear blend weighting and independent source muscle geometry are not calibrated soft-tissue mechanics. Of12000triangle-edge observations for one spanning muscle,105at90deg and57at120deg compress below20%rest length;min~6%. No claim of full continuity/collision quality,skin layer or physiological bulge. Hand grip remains source/rest shape.
- Status:DEFERRED for quality/attachment/contact/grip; minimum rig/GLB/runtime pipeline achieved, not complete dynamic anatomy. Next action:localized weight painting and tendon/contact landmarks,pose corrective evaluation or localretopology,closed-grip pose. Reopen at nextanimation-quality task or visible distortion; rerun four-angle front/side/back and numeric compression measures. NoACCEPTED_RISK or hidden skipped check.

### MODEL-RIG reopened for user-requested grip and pulldown integration
- User identified oversized crude dumbbell and exposed open hand tendons. Source anatomy has no skin surface and no gripping pose; original curl implemented only elbow bones. Need actual grip representation and shared hand/tool anchors, not scale-only replacement.
- Compare sourced skin hand asset with finger rig versus original procedural continuous hand surface with explicit source-hand visualization control. Asset provenance investigation in progress. No permission or validation claim inferred from screenshot.

## WD-2026-10-15-0006
Status: DEFERRED
Title: DUMBBELL-ASSET-IMPORT
- Original failure: public Innerscene CC0 model page exposes download API, but urllib request to https://www.innerscene.com/api/library/hex-weight-dumbbell-32966c1b/download returned HTTP403; no bytes published.
- Exact repro: urllib.request.urlopen(the public download URL,timeout=30).read().
- Workaround: none yet. Continue independent grip and pulldown implementation without substituting unverified asset or claiming download success.
- Cause: not established; browser public page advertises download, server access result differs. Do not bypass authentication or download controls.
- Paths: ordinary public UI download if authorized endpoint works; alternative verifiably licensed asset; original detailed geometry based on measured real references, explicitly identified as original rather than downloaded. Source investigator comparing evidence.
- Impact: real sourced dumbbell geometry not yet imported. Evidence: tool HTTP403 on2026-10-15.

## WD-2026-10-15-0007
Status: RESOLVED
Title: BROWSER-TEST-ISOLATION
- Original failure: pulldown browser flow timed out clicking play after active model reset to default anatomy. During that run the main agent edited main.tsx, triggering shared Vite HMR/page reload; screenshot evidence showed stale UI.
- Reproduction: npm run test:e2e reused interactive5173 while source files were edited mid-run. Failure retained in test output; no assertion skipped.
- Workaround: none yet. Prior passing results do not validate final changed files.
- Paths compared: only retry shared dev server (not durable isolation); separate owned test port and disable test-modeHMR (selected); production-preview tests (future separate coverage, larger test setup change).
- Fix: use dedicated5175 test server, reuseExistingServer=false, Vite test mode disablesHMR; freeze source during final run. Exact original failing test must pass after clean start.

### WD-2026-10-15-0007 subsequent controlled finding
- Dedicated clean test server exposed an existing waitForResponse registration race in atlas.spec.ts: navigation/canvas visibility was awaited before registering the GLB response listener; cached/fast response could already have happened. Pulldown and rig flows passed. This was not model load failure.
- Compared increasing arbitrary sleep/timeout (does not fix lost event) versus registering response promise before navigation (selected). Original assertion retained; no skipped response check. Clean full rerun required.

### MODEL-RIG grip/pulldown outcome
- Completed user-requested functional integration: actual source seated anatomy,13bones including bilateralUpperArm/Forearm/Hand and seatedlegs; no arm stretch. Machine and pose share one4second config.121frame target-renderer samples:contacterror~0.03mm,axiserror<0.001deg,bone-length error<0.001mm. Contact precision is not a claim of full skin/tool collision validation.
- Removed crude cylinder prop and visible open-tendon grasp from default curl. Original detailed hex geometry with28mmknurl,bevels,collars,endcaps; continuous original grip surface with four fingers/thumb/wrist/nails. Originalstaticatlas unchanged. Distal source tissues folded under explicitly labelled,optional presentation skin, not claimed as scanned skin or physiological tendon pose.
- Paths compared: source riggedhandasset(provenance/acquisition notverified),originalcontinuousgrip surface(selected),hidehand entirely(rejected;not a grasp). This surface solves current visual/attachment requirement but is not the full anatomic finger rig; all residual quality limits remain explicit.
- Final verification:3owned-portChrome tests,9Vitest tests,8Python tests,curl/pulldown/equipmentValidator0errors0warnings;actual hand/bar direction and points measured;no skipped assertions. Full clean test server run completed after fixes.
- DEFERRED residual: detailed shoulder/scapular and elbow/hip/legpad soft-tissue quality,fullcollision/individualfingeranatomicalrig and externalphotorealisticsurface. Next:weightpainting,contactchecks,artistqualityreview;reopen on nextanimationqualitywork or visiblepenetration.

### WD-2026-10-15-0006 outcome
- OfficialpublicpageclaimsCC0butordinarydownloadAPIreturned403;no fileobtained,no accesscontrols bypassed. AlternativePolyPizzaCC0lowpolycandidatealsonotacquired;limitedGitHubsearchnoverifiedbetterrealisticasset.
- Reversiblealternative selected:original detailed geometry based on public metric proportions,clearlyidentifiedasoriginal,notasdownloadedasset. EquipmentstandaloneGLBdimensionsmeasured~.3131x.1334x.1178m;Validator0errors0warnings;headscoaxial.
- DEFERRED only for external asset acquisition/inspection. Reason:publishedendpointaccessfailure;applicationusesoriginalpropindependently. EvidenceandURLsdocs/equipment-and-grip.md. Next/reopen:authorizedordinarydownloadbecomesavailableoruserprovideslicensedfile,verifyhash/license/visualqualitythenreplaceatsharedanchor. No claim externalmodelimportsuccessful.

### WD-2026-10-15-0007 durable verification
- Dedicatedowned5175,strictPort,reuseExistingServer=false,test-modeHMRoff isolatefrom5173preview. RegisterGLBresponsebeforepage.goto fixes lost-eventrace;responseandvisualassertionsretained.
- Exactoriginalatlasflow and failingpulldownplayflow passed in fullclean3testChrome run;subsequentfullfinalrun3passed. No retry option,extra timeout,disabledassertionor fallback was used. StatusRESOLVED.

### MODEL-RIG user-directed hand correction
- User rejected procedural hand orientation and explicitly requested original source hands. Removed generated hand/palm/finger/nail surfaces, UI toggle and all distal source-hand folding; rebuilt both motionGLBs. Source anatomical hands remain bound to the motion skeleton; upgraded dumbbell and seatedpulldown retained.
- This supersedes the presentation-hand workaround. Do not mark original openhand as a verified closedgrip or claim skin quality resolution. MODEL-RIG staysDEFERRED for anatomical finger grasp and previous soft-tissue quality; user preference recorded in projectAGENTS.

### MODEL-RIG shoulder/back correctness review
- Reproduction: select high pulldown, seek0/2seconds; lats/rhomboids/trapezius have no skin modifier, shoulder centers are constant. Original renderer screenshots and generator retained in Git. Existing qualitative color can be mistaken for activation; selected and primary colors identical.
- Compared shoulder-girdle plus attachment-aware skinning (selected), appearance-only bulge keys (cannot repair attachment), full calibrated musculoskeletal simulation (requires unavailable subject/load inputs). No workaround introduced; implementing structural rig correction. Original-hand preference remains mandatory. Verification will measure actual Three.js deformed vertices, shoulders and contacts, plus back/side screenshots.
- Structural correction verified in exported GLB/Three runtime:16bones,467source meshes; lat upper insertion mean displacement92.46mm, lower sampled lumbar origin0mm, shoulder excursion41.46mm;121frames max palm marker error0.0284mm, hand-axis error0.000048degrees;Validator0errors/0warnings. This resolves the observed missing back skinning/fixed shoulder cause, not physiological calibration.
- MODEL-RIG remains DEFERRED for uncalibrated shoulder motion, linear-blend/local soft tissue artifacts and original open-hand grasp. Evidence/parameters/alternatives: docs/pulldown-motion-review.md; next: localized weight/pose correction and attachment/collision QA; reopen upon visible distortion or calibrated motion-data availability. No ACCEPTED_RISK. No new workaround.

## WD-2026-10-15-0008
Status: RESOLVED
Title: M0-AUDIT-CAPTURE
- Original failure/repro: frozen a2864e4 production preview5181, run artifact capture.mjs; page.evaluate throws R3F current root not found, no frames generated. Log preserved as logs/capture-initial-failure.log. Application baseline tests pass; this is audit harness failure.
- Cause: Canvas rootState ref is initial snapshot; controls is populated later in current store, so testing ref.controls directly rejects it. Need current store via ref.get().
- Temporary workaround: none; no substitute images or alternate renderer. Candidate paths: read live store through rootState.get() (selected, camera-only instrumentation); UI-only orbit gestures (less reproducible cameras); injecting application exports (would alter audited build, rejected). No production changes.
- Impact: blocks M0 evidence completion and reviewer visual verdict until exact production capture succeeds. Next: durable live-state accessor fix; rerun exact script and verify source hashes unchanged.
- Follow-up same capture path: all50frames+browser measurements succeeded, but Playwright native video context failed because its version-specific ffmpeg dependency is absent. Existing system ffmpeg is separate. Compare installing pinned Playwright ffmpeg dependency (selected exact supported path) versus CDP screencast+system encoder (alternate capture path, unnecessary). Install required runtime dependency without changing project lock/source, then rerun entire original capture from fresh browser and require full video.

- Durable verification forWD0008: live get() accessor plus installed pinned Playwright ffmpeg1013; exact full capture.mjs rerun in freshbrowser exits0,50productionframes,27actualscene seek samples,47.92s native continuous video. No alternate renderer, no asset/source edits; seven frozen file hashes rechecked unchanged. Failure logs preserved in bundle. No implementation workaround or bypass remains.
- M1 audit only, MODEL-RIG remains DEFERRED: independent fixed-SHA reviews confirmed displaced bilateral flexor pollicis brevis and foot-platform penetration; additional cable/grasp findings in docs/reviews/lat-pulldown/a2864e4bdb8716b6fd3bf21e2bd459eac233887c/summary.md. No repair attempted, no risk accepted. Next/reopening trigger: owner approves M2 scope; trace original source transforms/weights and measure actual contact before edits. Audit completion does not close implementation defects.

## WD-2026-10-15-0009
Status: DEFERRED
Title: CODEX-CLI-BINARY
- Reproduction: nvm@24.15.0/bin/codex --version and --help fail ENOENT missing packaged native binary. No install/security setting changes.
- Impact: cannot verify custom-role auto-discovery through broken CLI. Desktop collaboration tools actually spawn isolated contexts successfully.
- Paths compared: repair global CLI/native optional dependency (outside current review scope); actual working desktop subagents plus role instructions and static configuration validation (chosen, not CLI repair).
- Next/reopen: repair correct CLI install when CLI execution is required and scoped. No accepted risk; no CLI-runtime success claim.

## WD-2026-10-15-0010
Status: DEFERRED
Title: OFFICIAL-DOCS-FETCH
- Search succeeded but direct official subagent page open twice returned tool transport connection failed. No third-party mirror used as authoritative evidence.
- Impact: latest custom-role schema documentation not fetched through this tool yet; preserve uncertainty. Compare official URL via system-proxy-aware urllib versus local packaged docs/schema; use only verified official bytes or avoid speculative config edits.
- Next/reopen: official retrieval route test; do not pretend current schema confirmed by search snippets. Primary blind review can proceed using actual desktop child agents.

### Exact7a0d258 blind audit outcome
- Latest user instruction superseded prior M2 approval; rigging agent interrupted before production edits. Current task M0/M1 only. Four NEW fork-none reviewers blocked from old findings until own reports frozen; ledger in exactbaseline artifactpacket.
- Working desktop actualsubagents reused, no pretend CLI loader. WD0009 remainsDEFERRED (global CLI native binary absent); WD0010 remainsDEFERRED (official page/tool transport and urllib TLS failure, no speculative schema changes). TOML syntax/required role fields verified with Python3.12; not runtime auto-discovery. Root-cause alternative compared already, no systeminstall/securityconfig changed. Reopen when CLI/docs route required.
- No new product workaround. Existing MODEL-RIG remainsDEFERRED for actualanatomy/contact/uncalibrated motion; blind reports verify platform/cuff/fragment issues; M2 notstarted and no risk accepted. Workflow gate intentionally rejects release pending owner and unresolvedP1; this negative test is expected, not a workaround.

- System-level WD0009/WD0010 also recorded in ~/.codex/state/workaround-debt.md as WD-GLOBAL-2026-10-15-CLI and WD-GLOBAL-2026-10-15-DOCS; project entries retain task linkage. BothDEFERRED, no product fallback or tool-resolution claim.

## WD-2026-10-15-0011
Status: OPEN
Title: M2-ANATOMICAL-ATTACHMENTS-CONTACT
- Scope/owner: explicit latest approval for B01/B02/V01 and K02 measurement; no main merge, no Face Pull, source hands preserved. Baseline exact7a0d258 and first reports immutable.
- Reproduction/evidence: original eight cuff meshes100%Thorax/static while shoulder moves; foot-platform397interior vertices per side; floating original thumb-muscle fragments visible. Baseline mesh-kinematics and videos preserved in exact7a0 packet.
- Earliest causes found by maker: absent cuff branches fall through attach=0; two flexor pollicis brevis SOURCE labels disagree with source spatial side, name-based assignment chooses opposite hand; foot/platform geometry was placed without evaluated source-foot support constraint.
- Compared durable paths: explicit named cuff attachment-region weights vs handpainted per-mesh landmarks; explicit source-ID spatial-side anomaly correction vs rewriting source labels/auto distance heuristics; derive support height from actual posed feet vs alter fixed-length leg IK. Selected source-preserving explicit cuff origin/insertion blend, documented two-ID binding correction, and measured support geometry if placement fits machine. No source deletion/hiding/vertex folding allowed.
- Temporary workaround: none newly introduced. Existing illustrative LBS/uncalibrated anatomy limits retained and must not be relabeled physiology. Maker corrections require all-vertex/source-ID measurements and four independent new-candidate reviews before closing P1.
- Next: newGLB/hash, real endpoint/edge and foot-solid tests, original hand surface/frame contact, paired before/after images/video. Status OPEN until review or explicit bounded DEFERRED outcome.

## WD-2026-10-15-0012
Status: OPEN
Title: M2-PLAYBACK-PERFORMANCE
- Original failures: nonloop at4s cannot replay; continuous per-frame exact sphere traversal and redundant469shared skeleton updates even paused. Controlled old production matrix measures~15–16actualrenders/sec and~full mainthread occupation, not just rAF proxy.
- Paths compared: shared endpoint transition vs separate restart control; dirty-pose exact sphere updates vs conservative per-influence bone bounds vs lazy per-raycast bounds/demand rendering. Selected shared pure playback transition, dirty pose/cache+renderer-owned skeleton upload, mathematically conservative pulldown bounds from positive normalized LBS influence boxes. Curl morph retains exact bounds.
- No skipped picking or substitute geometry. All source actual vertices must remain enclosed, raycasts and seek/style tested. CPU/performance after must use matched controlled conditions; GPU timer unavailable is not a fake PASS.
- Maker initial checks: build,11unit tests and actual Chrome endpoint/pose containment/picking pass. Independent new-asset review and paired profiling still required. Status OPEN until those results; no accepted-risk approval inferred.


## WD-2026-10-15-0013 — Windows handoff unavailable
Status: DEFERRED
- Original path: `ssh -o BatchMode=yes -o ConnectTimeout=8 win-codex` to deliver asset locations; exited255, `192.168.1.108 port22: Host is down`. Desktop list_threads contained no Windows task.
- Evidence preserved in session command output. No Windows writes or message delivery occurred.
- Temporary alternative: commit retrievable `docs/handoff/windows-assets.md` to the existing GitHub M2 branch; this preserves information but does not repair connectivity or prove receipt.
- Paths compared: existing authorized desktop task message (no matching task), direct existing SSH host (offline), repository handoff (available, selected for preservation). No network/security changes or repeat reconnection attempts.
- Next/reopen: when Windows host reconnects or its task becomes visible, send this handoff and confirm delivery.

## WD-2026-10-15-0014 — M2 agents interrupted by usage limit
Status: DEFERRED
- Three active maker/test turns returned account usage-limit errors. No independent review or successful repair may be inferred.
- Current tracked work checkpointed and pushed; unfinished browser test expansion explicitly marked unverified. No replacement single-context expert review, alternate account, paid credits or scope bypass used.
- Paths compared: resume same authorized makers after quota recovery; preserve and hand off existing version now. Selected preservation now, resume makers when capacity returns.
- Reopen: account capacity restored; rerun exact maker/test tasks, freeze new candidate, perform four fresh independent reviews before claiming M2 completion.

## WD-2026-10-16-0015
Status: RESOLVED
Title: M2 runtime JSON import, mount readiness and camera matrix instrumentation
- Original failure: `npx playwright test tests/browser/runtime.spec.ts tests/browser/supports.spec.ts` aborted during test collection: JSON module needs import attribute type json. No browser checks ran. New supports test used Vite-style JSON import under native Node loader.
- Paths compared: standard JSON import attribute (chosen minimal native ESM fix) versus fs read/parse plus separate type import (more test boilerplate). No workaround or skipped check introduced. Exact original command will be rerun after adding explicit import attribute; evidence in maker session. Impact limited to test collection; production build and13unit checks already pass.
- Exact rerun passed runtime but support test exposed a second new-test readiness defect: loading DOM can be absent before Suspense GLB mount, so SeatPad lookup ran against previous anatomy scene. Durable paths: response/UI waits (insufficient proof of mounted scene) versus actual named scene readiness assertion (selected). Added expect.poll actual SeatPad presence; no arbitrary sleep/retry masking product errors. Original two-test command rerun required.
- Oct16 rerun: runtime PASS; all support geometry/proxy/visibility checks completed, but same-evaluation camera projection test failed with maxX1.98885. Cause: controls.update changes camera pose, while project uses matrixWorldInverse from prior render. Corrected instrumentation by camera.updateMatrixWorld(true) before projection, rather than weakening viewport threshold or enlarging camera blindly. Exact two-test command rerun required.
- Durable verification Oct16: exact original two-test command PASS2/2 in34.1s; fresh clean full Playwright suite PASS5/5 in43.0s. BuildPASS/unit13PASS. Original import, mounted-scene readiness and camera projection paths all exercised without skipped assertions or relaxed thresholds. Evidence artifacts/m2/round2-runtime-maker/{exact-original-browser.log,full-browser.log,build.log,unit.log,maker-summary.md}. No retained workaround.
- Ledger checker limitation: stock check-workaround-debt.sh rejects existing historical ledger headings/status structure before ID selection; no global/other task entries were modified. This task entry has exactly one terminal RESOLVED status and verified original/full-suite evidence above; checker success is not claimed.
