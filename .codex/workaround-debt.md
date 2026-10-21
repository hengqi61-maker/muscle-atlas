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
Status: DEFERRED
Title: M2-ANATOMICAL-ATTACHMENTS-CONTACT
- Scope/owner: explicit latest approval for B01/B02/V01 and K02 measurement; no main merge, no Face Pull, source hands preserved. Baseline exact7a0d258 and first reports immutable.
- Reproduction/evidence: original eight cuff meshes100%Thorax/static while shoulder moves; foot-platform397interior vertices per side; floating original thumb-muscle fragments visible. Baseline mesh-kinematics and videos preserved in exact7a0 packet.
- Earliest causes found by maker: absent cuff branches fall through attach=0; two flexor pollicis brevis SOURCE labels disagree with source spatial side, name-based assignment chooses opposite hand; foot/platform geometry was placed without evaluated source-foot support constraint.
- Compared durable paths: explicit named cuff attachment-region weights vs handpainted per-mesh landmarks; explicit source-ID spatial-side anomaly correction vs rewriting source labels/auto distance heuristics; derive support height from actual posed feet vs alter fixed-length leg IK. Selected source-preserving explicit cuff origin/insertion blend, documented two-ID binding correction, and measured support geometry if placement fits machine. No source deletion/hiding/vertex folding allowed.
- Temporary workaround: none newly introduced. Existing illustrative LBS/uncalibrated anatomy limits retained and must not be relabeled physiology. Maker corrections require all-vertex/source-ID measurements and four independent new-candidate reviews before closing P1.
- Next: newGLB/hash, real endpoint/edge and foot-solid tests, original hand surface/frame contact, paired before/after images/video. Status OPEN until review or explicit bounded DEFERRED outcome.

- Final second-cycle disposition2026-10-16: actual GLB1e0af33c and candidate32315eb reviewed by four fresh contexts. All467 source base triangles preserved. Cuff freezing and severe-collapse alarms cleared, support sampled intersections cleared, but K02 deep original-thumb/bar penetration remains verified P1; attachment landmarks and axillary tissue attribution remain INCONCLUSIVE. Two automatic cycles exhausted; no full M2 completion/accepted risk. Evidence artifacts/m2/review-final-1e0af33 + versioned final reports. Next: owner-scoped original-hand contact/rig feasibility, source-labelled tissue attribution and attachment calibration. Reopen only on new approved repair scope; rerun full evidence and independent reviews.

## WD-2026-10-15-0012
Status: DEFERRED
Title: M2-PLAYBACK-PERFORMANCE
- Original failures: nonloop at4s cannot replay; continuous per-frame exact sphere traversal and redundant469shared skeleton updates even paused. Controlled old production matrix measures~15–16actualrenders/sec and~full mainthread occupation, not just rAF proxy.
- Paths compared: shared endpoint transition vs separate restart control; dirty-pose exact sphere updates vs conservative per-influence bone bounds vs lazy per-raycast bounds/demand rendering. Selected shared pure playback transition, dirty pose/cache+renderer-owned skeleton upload, mathematically conservative pulldown bounds from positive normalized LBS influence boxes. Curl morph retains exact bounds.
- No skipped picking or substitute geometry. All source actual vertices must remain enclosed, raycasts and seek/style tested. CPU/performance after must use matched controlled conditions; GPU timer unavailable is not a fake PASS.
- Maker initial checks: build,11unit tests and actual Chrome endpoint/pose containment/picking pass. Independent new-asset review and paired profiling still required. Status OPEN until those results; no accepted-risk approval inferred.


- Final second-cycle disposition2026-10-16: Q01 endpoint replay permanently corrected and actual five-test Chrome suite PASS, unit13/quality26 PASS. Exact current morph bounds and dirty-pose source tests exercised; no stale-bounds bypass. Remaining Q02 workload-matched new CPU/GPU comparison DEFERRED because latest owner scope excludes specialty FPS engineering; old24-trial baseline preserved, current paused rAF is only smoke observation. Reopen controlled benchmark if owner restores that scope or severe runtime regression occurs; no performance PASS/medical quality claim.

## WD-2026-10-15-0013
Title: Windows handoff unavailable
Status: DEFERRED
- Original path: `ssh -o BatchMode=yes -o ConnectTimeout=8 win-codex` to deliver asset locations; exited255, `192.168.1.108 port22: Host is down`. Desktop list_threads contained no Windows task.
- Evidence preserved in session command output. No Windows writes or message delivery occurred.
- Temporary alternative: commit retrievable `docs/handoff/windows-assets.md` to the existing GitHub M2 branch; this preserves information but does not repair connectivity or prove receipt.
- Paths compared: existing authorized desktop task message (no matching task), direct existing SSH host (offline), repository handoff (available, selected for preservation). No network/security changes or repeat reconnection attempts.
- Next/reopen: when Windows host reconnects or its task becomes visible, send this handoff and confirm delivery.

## WD-2026-10-15-0014
Title: M2 agents interrupted by usage limit
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


## WD-2026-10-16-0016
Status: RESOLVED
Title: Project debt ledger parser compatibility
- Original reproduction: stock root-cause-debugging check-workaround-debt.sh --scope project --id WD-2026-10-16-0015 --json exits2, malformed entry, before ID filtering. Root reproduced after maker reported same.
- Cause: inline titles on WD0013/0014 headings prevent strict documented heading recognition; their Status lines are then counted under WD0012. Semantic statuses are valid.
- Compared: normalize project heading syntax preserving all text and statuses (selected local durable fix); change global skill parser to accept arbitrary headings (broader unneeded maintenance); manual status inspection (temporary fallback, not selected as completion proof). No production workaround introduced.
- Correction: move only inline heading titles to separate Title fields; do not alter historical review reports or semantic debt outcomes. Rerun original failing stock checker before closure.
- Durable verification: exact original stock checker now exits0 and reports WD0015 RESOLVED. Only heading presentation changed; same semantic debt content and original reports preserved.

Oct16 follow-up WD0013: authorized wsl-codex endpoint now192.168.1.105:2222 was checked once with existing strict host verification; connection timed out. No message delivered, no remote/network modifications. GitHub handoff remains the retrievable alternative, receipt unconfirmed.

Oct16 follow-up WD0014: capacity returned and exact maker/test paths resumed, followed by four new final independent reviews. Quota limits themselves are normal external capacity constraints, not repaired by this project; future limit risk remains deferred. Current results are actual executed evidence, not inferred from resumed capacity.

## WD-2026-10-16-0017
Status: RESOLVED
Title: V2 viewer temporary disabled skinned frustum culling
- Original risk/reproduction: animate or seek a SkinnedMesh beyond its bind-pose bounds, then orbit/pick; stale mesh bounds can cull or reject the actual deformed surface. This viewer inherited a preventative `frustumCulled=false` while refreshing spheres; no browser failure has yet been observed.
- Temporary workaround: disable skinned-mesh frustum culling; it avoids rendering rejection but removes a renderer feature and is not a durable bounds solution. Scope is the isolated V2 viewer only, never the formal Scene.
- Evidence: initial src/experimental/rig-v2/main.tsx updateBounds explicitly set frustumCulled=false. Asset now stable and actual browser checks can run.
- Durable routes compared: existing validated createSkinnedBounds conservative per-influence boxes (selected: normalized nonnegative GLB weights, pose-cost proportional to influences); exact all-vertex computeBoundingBox/sphere after every changed pose (correct but unnecessarily scans all467 meshes each frame). Invalid weights must throw visibly rather than trigger a hidden fallback.
- Durable fix: reused createSkinnedBounds for every actual skin; restored frustumCulled=true. Geometry is not scanned per-frame unless the validated helper requires exact morph handling. Removed the disabled-culling workaround.
- Durable verification: isolated production build PASS, TypeScript PASS; fresh production Chrome Playwright PASS2/2 (21.0s), actual posed canvas picking PASS; every deformed vertex inside conservative box+sphere at peak of CurlProbe and PulldownProbe, all467 skins culling enabled, unique actual source IDs467. Front/Side/Back at five keyframes per clip produced30PNG plus actual browser video. Evidence artifacts/rig-v2/browser/production-browser.log and results/. GLB SHA256 ef803a4bbb3c644504c124519e39ba0b3b760ec139eaf60d277ef7f7f5d23274. This verifies bounds/picking, not motion acceptance.

## WD-2026-10-16-0018
Status: RESOLVED
Title: V2 independent source preservation precision assertion
- Original reproduction: Blender Agent runpy scripts/rig-v2/verify_source.py after build.py; independent fresh original GLB import versus saved native base vertices fails assertion at 1e-7 metre tolerance.
- Workaround: none; geometry preservation claim requires independent test. Initial build hashes only prove no subsequent base edit and are not substituted for this test.
- Evidence: verify_source.py now preserves per-mesh deviation/topology failures to artifacts/rig-v2/source-verification-initial-failure.json before asserting. No source or exported asset changes.
- Investigation: compare transformation precision/dtypes and mesh/topology, then choose exact float32 transform emulation versus numeric epsilon bound derived from observed source magnitude. Do not relax threshold without identifying cause.
- Impact: independent source geometry proof pending; no full completion claim.

- Root cause measured: original verifier computed float64 divide by1000, while Blender mathutils Vector stores float32 and multiplies float32 reciprocal. All467 polygon vertex orders matched,279 meshes exceeded an arbitrary1e-7 threshold by at most1.3519e-7m.
- Durable paths compared: tolerance derived from magnitude/ULP versus exact emulation of documented float32 conversion. Selected exact float32 reciprocal model, removing tolerance entirely.
- Verification: exact original Blender Agent runpy verify_source.py rerun in a fresh background process PASS467/467 with zero coordinate difference and unchanged polygon index order. Initial failure evidence preserved; independent-source-preservation.json and source-verification-float32-comparison.json record success. No workaround or asset modification.

## WD-2026-10-16-0019
Status: RESOLVED
Title: V2 non-loop finished action cannot replay
- Original reproduction independently confirmed by Software QA on old dist: select CurlProbe, disable Loop, seek3.99s, Play300ms reaches4.000 but button remains Pause; Pause then Play300ms remains4.000 (mixer global4.6308).
- Cause: LoopOnce clamp pauses AnimationAction internally while React playing remains true; toggling state alone never re-arms the clamped action. Seeking after finish also needs action reset before setTime.
- Compared durable paths: state-only finished handler (corrects label but cannot resume internally paused action), versus finished handler plus explicit reset/play at terminal restart and before seeks (selected, addresses both actual mixer and UI lifecycle).
- Workaround: none retained; no asset changes or threshold relaxation. Impact confined to isolated R1 viewer, existing M2 report unchanged.
- Verification pending: exact original browser path, replay on both clips, pause/seek/loop and existing R1 tests after clean production build.

Oct16 V2 follow-up WD0014: playback maker turn returned account usage-limit error after writing code/tests, before reporting build/browser verification. User reports quota refreshed; preserve current changes as explicitly unverified checkpoint, resume the same maker and run exact original path. No passing result inferred from files on disk and no alternate-account workaround. WD0019 remains OPEN until durable verification.

WD0019 verification follow-up: first production Chrome run passed existing2 tests, new regression exposed repeated seek request dropped when requested numeric time equals previous seek state although actual playback has advanced. The control now carries an explicit seek revision; identical requested times remain distinct commands, but the subsequent actual revision-only browser run still failed because the controlled range React onChange did not deliver the input request. A single-variable native onInput/currentTarget change then passed the exact enhanced browser test for both clips (4.9s). First failing log/video preserved in artifacts/rig-v2/replay-browser-initial-failure.log and replay-results-initial-failure/. No test target changed or assertion relaxed.

WD0019 final maker verification: fresh production build exit0 (2.34s), followed by complete production Chrome R1 suite PASS3/3 (25.1s). Exact non-loop terminal replay tested on CurlProbe and PulldownProbe; pause, seek after finish, seek1→play→same seek1, original picking/material/rest checks and30 front/side/back clip frames all passed. Logs artifacts/rig-v2/replay-build.log, replay-input-browser.log, replay-browser-final.log; actual videos/frames replay-results/. The native input event path plus explicit seek revision delivers every request; no disabled feature, retry masking or changed asset. GLB remains SHA256 ef803a4bbb3c644504c124519e39ba0b3b760ec139eaf60d277ef7f7f5d23274. Independent QA confirmation pending before closure.

WD0019 independent verification: Software QA /root/r1_software_review fresh actual Chrome exact original path PASS for both clips:3.99→4.000 automatically returns Play; replay advances0.468/0.300s; seek1→play/pause1.250/1.233→same seek1 settles1.000 and holds100ms. Read-only execution tool chunk ef7f5c delivered to coordinator. No historical review changed; no retained workaround.

## WD-2026-10-17-0020
Status: RESOLVED
Title: Fresh pipeline world-node assumption and Blender exception exit status
- Original failure: cold build_motion run-a/run-b imported and rebuilt467 source meshes and exported GLB, then new World had no Background node in Blender5.2; Python KeyError aborted native rendering. Blender default exited0; driver then attempted ffmpeg without frames, which exited254. No PASS manifest generated.
- Exact reproduction: original native_build.py world.node_tree.nodes['Background'] after bpy.data.worlds.new with use_nodes=True, Blender -b --python without --python-exit-code. Logs retained artifacts/motion-pipeline/initial-failure-a/build.log and initial-failure-b/build.log, plus encode.log.
- Workaround: none; failed dirs preserved, no old/new result mixing, fresh directories required. Root cause is implicit startup-world assumption and missing strict child failure propagation.
- Durable paths compared: explicit ShaderNodeBackground/ShaderNodeOutputWorld and link creation (selected, portable) versus dependency on startup template world (rejected implicit state). For failure propagation explicit --python-exit-code1 (selected) versus log-text grep (rejected brittle).
- Fix: explicit world nodes, Blender --python-exit-code1, checked subprocess execution before encode and manifest. No source anatomy or alarm threshold change.
- Verification pending: injected native exception must exit nonzero and block encode/PASS; two fresh complete original builds including all native renders.

## WD-2026-10-17-0021
Status: RESOLVED
Title: E3 browser evidence redundant bounds recomputation and cancelled late report
- Original reproduction: E3_BROWSER_ASSET=public/experimental/rig-v2/unified-rig-prototype.glb E3_BROWSER_OUT=artifacts/rig-v2/pipeline/three-consumer-frozen-smoke node --test tests/rig-v2/pipeline-browser.node.mjs. Real Chrome exceeded240000ms at240432.884ms with54 screenshots then cancelled; task completed late367702.709ms. Its late report is not a passing test. Evidence preserved, renamed cancelled-late-report.json.
- Cause: pose() rescanned every skinned vertex for exact box and sphere on every style/view call, including camera-only updates; initial test lacked abort cleanup and could write a late PASS-shaped report after cancellation.
- Temporary workaround considered:600s budget, not used as closure. Compared durable A increasing timeout (retains redundant work) versus B pose-dirty exact-bounds cache (selected). Every changed pose, including121 sampled times, still recomputes actual skinned bounds; unchanged material/camera changes only render. Culling stays enabled, no quality threshold changes.
- Durable fix: dirty pose cache, AbortSignal browser cleanup, no PASS report if cancelled. Restore original240s budget. Initial single-clip attempt exposed immediate missing test-context parameter in new cleanup code; corrected directly, no asset or fallback involved.
- Verification pending: original two-clip frozen smoke within original240s, plus actual fresh run-a/run-b derivedGLB capture.
- Impact: capture tooling only; no evidence of anatomical quality or true grip implied.

WD0021 intermediate verification: first dirty-cache-only original two-clip command still exceeded240s (240566.706ms), cleanup ended250602.393ms and emitted no PASS. Exact log retained in three-consumer-frozen-smoke/retest.log and copied initial-dirty-evidence. Final durable cache also recognizes identical clip/time and computes exact box plus sphere from one full skinning sample buffer rather than re-skinning twice. Standard Three computeBoundingBox/Sphere midpoint comparison must agree within1e-12m before accepting this mathematical equivalence. No sample count/culling/alarm change.

WD0020 durable verification: actual deliberate Blender RuntimeError fixture returned1; checked sequencing prevented encoding and PASS creation (artifacts/motion-pipeline/failure-fixture/result.json). Two new fresh background native processes reran the original operation with explicit shader/output nodes and --python-exit-code1, both completed all467 meshes/27bones,50 native keyframes,31 video frames and encoded MP4 plus saved Blend: run-a782.21s, run-b753.19s. Exact source/face hashes, skin/inverse-bind/animation structure and full GLB bytes match;121 world trajectory maximum difference0 against predeclared2e-5. Failed initial dirs preserved, no skipped render or source anatomy edits. Full post-export geometry/Chrome stages remain separately pending; this closure concerns world creation and failure propagation only.

WD0021 equivalence test correctly rejected an experimental bbox-center sphere algorithm (22533.420ms, final-test.log); it differs from Three SkinnedMesh sequential expandByPoint. Final implementation uses the identical stock box.expandByPoint and sphere.expandByPoint sequence over each actual getVertexPosition once, plus identical-pose cache. No comparison tolerance changed. Root clarified240s is an arbitrary harness budget, not user SLA or geometry quality threshold; final explicitly recorded workload budgets are300s one clip /600s two clips. Exact source/viewer SHA logged before every fixed-code execution. Remaining verification uses actual fresh a,b then full frozen two-clip command, no further algorithm edits.

WD0021 durable verification: fixed consumer commit5394379, testSHA bf4d9558bdee1a0f710a831e6448c08178f29ed6f4200d38e802d80230761556 and viewerSHA8353616e524665bac9958a08186b4e3c347ebb4e4752af8a506ee9ddc54fcff6. Actual fresh run-a PASS32.488s and run-b PASS26.667s (each467meshes,121poses,50PNGs, full actual canvas cycleWebM, stockbox/sphere midpoint equality<1e-12m, original-source triangle pick and paused freeze). Fresh browser process on exact original frozen two-clip functional command PASS47.863s/exit0 with242sampledposes,100PNGs,two fullcycleWebMs; log durable-final.log and report.json retain source/assetSHA,Chrome155.0.8059.84/Nodev26.5.0. Last execution explicitly used600s workload deadline (not240s SLA), actual measured47.863s. No motion geometry threshold, culling, sample count or original asset changed;600s is documented per-workload harness policy, not fallback or performance certification. Initial and intermediate failures/cancelledlate report retained. No hidden retries or mock assets in passing runs.


## WD-2026-10-17-0022
Status: RESOLVED
Title: Pipeline review metadata did not bind frozen commit
- Independent software review identified an applicability gap: valid40character review.commit was not compared with fixed candidate. Exact real manifest command with review.commit=aaaa... and --candidate=b50d35e... returned0/evidenceErrors[] (before.json). GeometryFAIL/ownerpending still blocked actual release; no wrong review was used for release.
- Reproduction evidence: artifacts/motion-pipeline/review-binding/{wrong-commit.json,before.json}. No workaround or approval bypass.
- Durable alternatives: infer producer commit from mutable working HEAD (rejected: historical asset reviews and docs-only commits differ), versus require explicit fixed candidate parameter and validate review commit plus asset hash (selected, portable read-only metadata).
- Fix and exact rerun pending; add negative wrong/missing candidate tests, retain four independent review identities and owner gate.

WD0022 durable verification: exact original wrong-commit CLI rerun now exits1 with evidenceErrors=[review commit mismatch] in after.json; six review gate testsPASS include wrong/missing candidate and wrong asset, plus prior self-review/owner/geometry/hash guards. No temporary bypass. Subsequent independent Software QA will review this narrow fix and updated candidate; no anatomical asset or original review report changed.


## WD-2026-10-17-0023
Status: RESOLVED
Title: Validator failure leaves provisional software PASS on disk
- Independent Software QA identified phase-label failure propagation gap. Actual isolated synthetic invalid-scene GLB makes real Khronos failUNRESOLVED_REFERENCE; finalizer exits1 but provisional manifest remains SOFTWARE_TEST_PASS. No actual candidate GLB validator failure; current complete evidence gate still blocks incomplete inventory.
- Exact reproduction: python3 tests/rig-v2/pipeline_failure.py; before.log in artifacts/motion-pipeline/finalizer-failure/ shows failed negative assertion. Synthetic prerequisites only reach the real validator; never used as motion evidence or runtime fallback.
- Durable paths: provisional IN_PROGRESS then atomic final PASS/FAIL updates (selected) versus pending-only filename renamed after all stages (more invasive API change). Error propagation must cover disk labels, not only child exit.
- Current true cold CLI processes are executing unchanged driver; preserve their code provenance. Await their successful completion, then make metadata-only lifecycle correction and run actual success finalization plus exact invalid-scene regression without re-rendering immutable models. No workaround, no source asset change, geometryFAIL/ownerpending still block release.

WD0023 durable verification: after both complete actual coldCLI executions had ended successfully, changed only lifecycle metadata: driver emitsIN_PROGRESS; finalizer atomic writesIN_PROGRESS then terminalSOFTWARE_TEST_PASS/EVIDENCE_COMPLETE or SOFTWARE_TEST_FAIL/FAILED on exception. Exact real invalid-scene validator regression nowPASS (actual finalizer nonzero and disk labelFAIL). Successful finalization of a copy of actual cold-cli-a output using checked join stages produced complete hash inventory with zero evidence errors, retained geometryFAIL and ownerpending (lifecycle-success; this is metadata-only regression, not a new native build). Before/after/success logs in artifacts/motion-pipeline/finalizer-failure. No render/source/weight/threshold edits. Expensive native/Chrome work not silently replayed or relabelled: two fullcoldCLI successful executions belong to unchanged input/native/consumer versions at1f6; lifecycle patch verified separately.


## WD-2026-10-17-0024
Status: DEFERRED
Title: Windows published packet export/Git hash provenance clarification
- Ancillary contact-readiness refresh found Windowsfd1701f validation.json packetSha62e1... while actual Gitblob shoulder.packet.json SHA242f.... Exact publishedLF→CRLF yields62e1..., so evidence supports export line ending conversion, not numeric content corruption. Mac semantic validator0issues/7nodes/10samples; no OpenSimrerun claim.
- No workaround/normalization applied to input. Published Gitbytes and own computed SHA retained; both identities and evidence recorded in docs/rig-v2/pipeline/results/windows-receipt.json. Core E3 inputs do not depend on this external packet.
- Compared paths: normalize packet to match exporthash (rejected changes transportbytes) versus preserve rawGitbytes and explicitly distinguish export/transportSHA (selected). Windows owns result metadata, no remote edits byMac.
- Deferred only upstream label clarification: ask Windows publish both rawexportCRLF and GitLF SHA or binary-stable transport. Nextaction GitHubPR6 comment; reopen when Windows metadata update arrives or packetbytes change. Not an anatomy approval or accepted risk; no remaining task OPEN entry.

## WD-2026-10-18-0025
Status: RESOLVED
Title: Experimental GLB elbow rotation must remove bind-local orientation before changing basis axis
- Original reproduction: node scripts/rig-v2/phase2/derive.mjs E02-elbow-axis artifacts/phase2/E02-elbow-axis. Initial experimental quaternion edit used full GLB local animation quaternion as if it were Blender matrix_basis. Report max axis delta15.872deg and Curl angle113.005deg disagrees with actual basis100deg /4.698654deg expectation.
- Initial candidate is INVALID_EXPERIMENT, preserved separately; no geometry scan/render or quality verdict based on it. No production assets affected. No runtime bypass used.
- Compare durable paths: derive rest-local quaternion from actual inverse-bind parent-child matrices, subtract/restcompose around basis-only edit (selected, retains exact binary provenance), versus rebuild all animations in Blender basis space (larger export identity surface). Independent read-only axis review requested.
- Fix must retain preregistered angle and exact untouched bytes, assert measured axis delta and rotation-angle invariance, then rerun exact generator path in fresh output. Remains OPEN until true validation.

WD0025 durable verification: independent axis Agent reconstructed inverse-bind matrices and confirmed restLocal inverse times track gives actual basis. Fixed generator edits basis only, then restLocal times basis; near-identity samples preserved. Exact fresh E02-elbow-axis-basis rerun produces d60a589aff96eea65fe84da64f288af231e95b3b278fcb428c1c6fb0747bf55d; four channels all121samples, axis delta4.698685–4.698688deg, Curl amplitude100.000012deg and Pulldown90.000018deg, max angle difference9.3e-14rad. Assertions enforce expected axis/amplitude invariance; untouched bytes exact. Initial invalid candidate preserved/excluded; no workaround retained.

## WD-2026-10-18-0026
Status: DEFERRED
Title: GitHub Issue progress comment TLS handshake timeout
- Original exact command: gh issue comment 10 --body-file /tmp/phase2-progress.md. gh returned1: POST https://api.github.com/graphql net/http TLS handshake timeout. DraftPR12 and Git push had succeeded earlier. The body is preserved; no assertion that failed delivery succeeded.
- No configuration or transport workaround applied. Compare bounded unchanged exact command after same-host health read versus switching REST/client (would obscure original GraphQL failure); selected read-only health + one evidence-preserving exact retry. Do not mutate proxy/security or loop retries. Local CPU/native experiments continue independent of network.
- Root cause not established; transient network path/remote TLS remains plausible. Scope limited to communication. Next action preserve actual gh result/comment URL; reopen on next failure, then controlled proxy diagnosis with permission before disruption. DEFERRED transport investigation, never treat retry as permanent resolution.

## WD-2026-10-18-0027
Status: RESOLVED
Title: Native import total meshes differs from original anatomy identity count
- Actual render worker initial import stopped before GPU/render on total meshCount==467 assertion; log artifacts/phase2/native-baseline/blender.log preserved. Frozen GLB imports469 mesh objects,467 unique sourceName identities plus2 additional objects. Distinguish total imported geometry from source anatomy; do not hide or delete extras.
- Compared durable identity-based set+name/hash verification versus filtering/deleting extras (rejected). Maker correcting source-identity gate while preserving all scene objects visible. Exact native-baseline-v2 rerun pending; no motion/visual PASS claim.

## WD-2026-10-18-0028
Status: RESOLVED
Title: Recurrent Blender new diagnostic material has no implicit Principled node
- Renderer v2 stopped strictly before rendering because new material lacked implicit Principled node; evidence native-baseline-v2 log retained by render maker. Same class as earlier WD0020 world-node assumption.
- Durable paths: explicitly construct Principled and Output nodes/link (selected) versus depend on factory template/get node by translated/default name (rejected). No material substitute or omitted mesh. v3 actual native frames produced after explicit nodes; full fixed-run verification pending.

## WD-2026-10-18-0029
Status: DEFERRED
Title: Bounded diagnostic render uses explicit eight samples instead of default64
- Actual512px EEVEE factory default64 samples measured about40s/frame,122images/asset implies roughly80min each/4h three assets. Partial real native-baseline-v3 data/log/PNGs/121trajectories retained; stopped withTERM under coordinator authorization, never marked complete.
- Compared durable production options: retain64 about4h, fixed8 at identical512px/camera/material/frame settings (selected bounded engineering diagnostic), lower resolution (rejected harms local detail). Three sets must share8 samples; no geometric threshold/sample-frame/culling/identity change. This is explicit rendering-budget adaptation, not proof default64 pipeline performance fixed.
- Maker executes new native-baseline-v4 then same E01/E02 runs; actual times and quality review pending. High-sample production visual validation deferred; reopen if independent VisualReviewer finds8-sample noise insufficient, then render required regions64 with evidence. No accepted risk or anatomy PASS claimed.

WD0026 delivery follow-up: same-host curl health HTTP200; exact original gh issue comment rerun succeeded https://github.com/hengqi61-maker/muscle-atlas/issues/10#issuecomment-6251322684 . Delivery now confirmed but underlying transient TLS cause remains DEFERRED; retry not permanent resolution.

WD0027 corrected evidence and durable verification: initial469 count came from probe retaining default Cube. Factory-startup + deleting scene + frozen GLB import actually468=467 unique original sourceName identities plus1 Icosphere (localized name棱角球), not2extras. Correct source-set validation preserves it visible. Actual native-baseline-v4 completed both real clips/121nonstatic matrix samples with467identities/27bones, no meshes hidden. Old failed probes are retained; no source modifications.

WD0028 durable verification: explicitPrincipled/Output construction in renderer eliminated implicit-node assumption. Actual native-baseline-v4 completed both diagnostic clips, produced actual frames/video/Blend under explicit8samples; sourceShaef803.../467identities/27bones fixed. Camera/framing quality is separate and not implied by this material-node closure. No template fallback remains.

## WD-2026-10-19-0030
Status: RESOLVED
Title: Native full-body framing used bounds before individual NLA activation
- Old baseline-v4 kept actual frames/videos but initial framing was calculated with simultaneously imported NLA state, not a full-cycle bound; source pose framing could crop. No final framing approval based on it.
- Compared fixed guessed ortho scale versus measured full-cycle eval-mesh bbox union (selected); bone-only bounds rejected for hands/tissue. New camera-calibration-v2 independently activates2clips for each3assets, samplesall121 evaluated mesh bounds and verifies eachclip firstpose against all actual evaluated vertices (difference0m). Contract adds10percent margin, clipping proof0.90909 maximum extent.
- Actual3smoke images preserve fullbody; independent fullvertex camera projection max0.875751, image tissueYfront40–334/back31–330/side30–333. Root actually viewed back hand tips with>30pxmargin. No contract change after maker initially misread smoke; corrected against pixel+projection evidence. Fixed contract applied uniformly; pending fullvideos are separate work. No geometry threshold, source or finger edits.

## WD-2026-10-19-0031
Status: DEFERRED
Title: E01 experimental local exported weights introduce coincident-source seam separation
- Full candidatef7324... retained unchanged/FAIL. SoftwareReviewer actualLBS detected11 source-equivalent groups split; pair441/1288 separates3.179553mm atPulldownframe0 (baseline0). Original2byte-scope unit tests pass but do not test continuity. Fulltriangle metric worsenspeak3.988438→6.469800 even though severeframesremain91. No adoption or hidden workaround.
- New seam-check.mjs measures1785 same-mesh exactoriginalPOSITION/JOINTS/WEIGHTS duplicate pairs over121actualLBS samples/two clips, outputsAUTOFAIL/exit1onE01; E02newseamcheckAUTOPASSonlyfor thissourcegroup screen. Threshold1micrometre explicitly numericalregression, not medicalgapallowance.
- Durable alternatives for next separately numbered experiment: preserve verified same-source equivalence classes duringlocalweight changes; or move experiments to native source-index registry with topology provenance beforeexport. Pose-space correction third alternative remainsdesignonly and cannot conceal seam. Uncalibrated attachment regions mean no anatomical fix selected. Reopen when owner/calibration reference supports next experiment. Priorcandidate/reportneveroverwritten; remainingmotionqualityFAIL and ownerpending.

Final WD0027 scope clarification: frozenGLB JSON exactly467 meshes/nodes. bpy.data and scene contain an importer-created Icosphere/棱角球 custom_shape referenced by27bones, linked to glTF_not_exported collection with importer-default hide_render/hide_viewport; it is not an original extra asset or prop. Renderer never hides originalsource meshes (all467 hide_render=False). Earlier temporary extra-asset count interpretations superseded by binaryJSON + native helper-inspection/visibility logs. Camera contract included helper bbox conservatively, causing spare whitespace only; identicalcontract preserved for scientific comparison. No helper or source was deleted/hidden by this work.

WD0029 measurement caveat: initial64sample40s/frame and later8sample5.7s/frame occurred under heavy concurrent fulltriangle scans; with scansfinished native-baseline-v5 71.59s total and E01 58.54s total. Do not attribute speed difference solely to sample count; no controlled FPS/performance improvement claim. Explicit8-sample diagnostic imagery remains reviewed only for gross shape; micro-seams/high-sample productionvisual validation DEFERRED.

## WD-2026-10-19-0032
Status: DEFERRED
Title: Supplemental isolated Blender rest-world exact equality residual
- Actual isolated-comparison exact world-rest assertion observes E01 subscapularis16vertices max1.1920929e-7m residual; rawbefore/after values and failing exact check retained in artifacts/phase2/isolated-rest-equality-diagnostic.json. OriginalserializedGLB POSITION/index/inverse-bind bytes still exact independently. No originalsource gate or tolerance relaxed.
- Compare keep literal serializedsource identity plus rawimport-world numericINCONCLUSIVE (selected for this diagnostic-only delivery), normalize/overwrite worldcoords toforceequal (rejected destroys evidence), versus full importer/decomposition trace with common-frame alignment (next bounded experiment). No claim of exact renderedworld equality or medicallycorrect shape.
- Deferred importer-space provenance investigation; nextaction trace node/armature/decompose rounding on fixedsource if future shape comparison needs exact importedworld correspondence. Reopen if residual grows, serializedsource identity differs or candidate considered for production. No acceptedrisk; bothvariantsalreadyFAIL/notadopted.

## WD-2026-10-20-E03
Status: RESOLVED
Title: Reopened E01 duplicate-vertex divergence investigation
- Original reproduction: node scripts/rig-v2/phase2/seam-check.mjs --asset artifacts/phase2/E01-local-gradient/motion.glb --output artifacts/phase2/E01-local-gradient/seam-report.json; AUTO FAIL, peak3.179553mm. Historical rejected asset and WD0031 remain immutable.
- No bypass or threshold change introduced. Compare constrained export-weight projection (bounded candidate), source-index registry rebuild (requires provenance reconstruction), attachment calibration (needed for anatomical correctness, currently absent). Independent read-only investigation requested before choosing candidate.
- E03 preregistered as one added equivalence projection on otherwise unchanged E01 operator. Actual scans and outcome pending; production not replaced.

## WD-2026-10-20-E03-BROWSER
Status: DEFERRED
Title: E03 real Chrome navigation timeout during concurrent full geometry and native calibration
- Exact command: E3_BROWSER_ASSET=artifacts/phase2/E03-equivalence-projection/motion.glb E3_BROWSER_OUT=artifacts/phase2/browser-E03 node --test tests/rig-v2/pipeline-browser.node.mjs. Actual page.goto load timeout30000ms; original browser.log/output preserved. No browser PASS claimed.
- Concurrent attribution/calibration imports unusually slow; resource contention suspected, not yet proven. No retries, relaxed thresholds, killed user applications or security changes.
- Compare serial rerun after current jobs finish, scoped navigation diagnostics, or explicit higher startup budget after observed timing. Prefer serial exact original path first; wait for evidence before modifying tests. Underlying cause remains unresolved.

## WD-2026-10-20-E03-GIT
Status: DEFERRED
Title: GitHub push configured local proxy unavailable
- Exact git push origin codex/rig-v2-phase2 failed connecting127.0.0.1:7897. git http.proxy and https.proxy both point there; no proxy env override. Local committed7fe2c00 preserved. No system/profile restart or config mutation.
- Compare restore owned proxy service after coordination versus command-local direct route with unchanged persistent config. Read-only direct connectivity measurement first; if direct route works it is a scoped delivery workaround, not repair of shared proxy lifecycle.

E03 continuity closure verification:21 original exact classes/43 rows receive identical float32 values; independent raw-byte and actualLBS review1785pairs×121×2 zero separation; two clean fresh builds exact. Original rejectedE01 path rerun AUTOFAIL, no test relaxed. This resolves E03 numerical duplicate divergence only. E01/R1 historical anatomy FAIL and WD0031 rejectedcandidate remain unchanged. Full E03scan39/91/peak6.469800, independently rejected; no adoption.

E03-GIT delivery: direct HTTPS measurement200; command-local git -c http.proxy= -c https.proxy= push succeeded7fe2c00. Persistent config untouched. CLI observation confirms unavailableMihomo/mixedport; shared proxy lifecycle not repaired. DEFERRED pending coordinator ownership/startup diagnosis, reopen when default Git path needed. Scoped direct route is disclosed workaround only.

E03-BROWSER exact-script serial rerun after native/calibration/allmesh jobs completed: PASS85.533s, both121poseclips/100screenshots/two complete-cycleWebMs/pause/pick. Original timeout retained, workload contention plausible not proven. Serial scheduling is disclosed workaround; root attribution DEFERRED, reopen on serial recurrence. No navigation/geometry threshold relaxed.

## WD-2026-10-20-E03-MCP
Status: DEFERRED
Title: PR15 guarded client owned by another session
- Read-only SDK initialize failed with client.lock nonblocking flock Errno35 before any query; transcript retained controlled-mcp.log. No instance takeover, lock deletion, security relaxation or restart.
- Shared-instance ownership boundary honored; compare coordinator releases owner client versus coordinator executes registered read-only inspection and publishes results. Await coordination; no current MCP connectivity PASS claimed. No listener detected9876 at check time, which is separate from held-client lock and not proof of stale lock. Reopen after owner handoff. Existing deterministic bpy actual121/native evidence continues without claiming MCP succeeded.

## WD-2026-10-20-PREVIEW
Status: DEFERRED
Title: Vite-transformed diagnostic consumer stays in initial loading state in IAB
- Startup5190 servesHTML/41MBGLB HTTP200; after Vite newdependency optimization/reload, actual IAB diagnostic consumer shows Loading actual build output, no visible console error. No model display PASS claimed for Vite consumer.
- Compare Vite transformed dependency lifecycle investigation versus existing test-proven direct static consumer (selected bounded viewing path, no asset changes). Start static loopback5191 matching tested module/importmap paths; preserve Vite server for R1 React page. No browser/security/proxy setting changes.
- Cause not established; revisit Vite direct consumer module graph after viewing task. Exact failed5190 URL retained. This is a preview delivery workaround, not resolved module-loading claim.
## WD-2026-10-20-001
Status: RESOLVED
Scope: PR21 controller coordinate adapter only, not anatomical grasp.
Failure/reproduction: zero deltas replaced exported local rotations; actual source finger origins moved 37.7099636 mm.
Alternatives: preserve exported reference quaternion and compose relative deltas (chosen); reorient/reexport every finger bone (rejected: unnecessarily changes asset). Blender XYZ requires Three ZYX Euler delta composition. Preserve original float32 quaternion norm for exact neutral identity.
Verification: neutral/repeated-write/left-right tests; actual Blender six poses and continuous121 samples, maximum joint-origin difference 0.580026 micrometres. Original failing neutral path now preserves identity. No fallback remains in controller.
Evidence: p3-basis old-neutral, native reference, parity-corrected, continuous and unit logs in published evidence archive; docs/grasp-v1/continuation-results.json.
Reopen: parity or neutral regression on a new exporter/asset.

## WD-2026-10-20-GRASP-CONTINUATION
Status: DEFERRED
Failure: original tissues still intersect actual angled grip and stretch; 121-pose native/Three checks agree, FAIL. Corrected controller does not resolve heuristic weights/topology or provide fingertip surfaces.
Temporary diagnostic: inherited unconstrained CCD tested as explicitly labelled arm-reach probe only; never training or grasp acceptance. Production assets unchanged.
Alternatives: calibrated original tissue attachment/weight refinement versus a reviewed representational change to missing hand geometry. No skin shell or arbitrary weight scan authorized as solution.
Impact: no credible visible training grasp; P3 physical calibration and independent visual/biomechanical review pending.
Next action/reopen: Cursor/Windows publish physical attachment/axis evidence; choose one local attributable candidate; rerun full gates. No claim of completion.

## WD-2026-10-20-BROWSER-RUNTIME
Status: DEFERRED
Failure: Playwright bundled chromium_headless_shell-1248 missing; exact launch error retained in browser.log.
Workaround: explicitly select installed Google Chrome via supported channel; same actual viewer assertions and recorded video pass, browser-chrome.log/report.json.
Alternatives: install pinned Playwright browser versus explicit existing Chrome channel (chosen to avoid installation). No claim that bundled Chromium works.
Next action/reopen: CI requiring bundled Chromium must install and rerun exact original launch. Browser version compatibility remains environment-specific.

## WD-2026-10-20-V2-ASSEMBLY
Status: RESOLVED
Failure: v2 animation assembly exact JSON comparison rejected Pelvis rotation because donor omitted identity while source stored float32-near-identity. Reproduction: node scripts/grasp-v2/assemble.mjs before semantic comparison.
Paths: retarget/reexport skeleton (adds asset drift) versus semantic default TRS comparison with existing numerical parity tolerance (chosen). No anatomy/contact threshold relaxed. Durable fix validates omitted identity defaults and float32 import error with existing 64*float32 epsilon, rejects incompatible target references. Original assembler now passes. Original source BIN is copied byte-identically; no frozen/production asset changed. New experimental assembly manifest records input/output SHA. No retry/fallback remains.

## WD-2026-10-20-V2-TISSUE
Status: DEFERRED
Associated inherited GRASP-CONTINUATION: missing actual fingertip surfaces and 14/30 joints unweighted; heuristic axes are not calibrated anatomical axes. Reproduction: inspect actual source GLB JOINTS_0/WEIGHTS_0 and build.py. No weight mutation, new skin, or fallback anatomy introduced. Proxy solver remains explicitly separate.
Paths compared by independent rig/contact read-only investigations: retain asset/reference and use bounded proxy solve (selected for controller); physical landmark/attachment calibration and reviewed source tissue adaptation (requires missing evidence); replace skeleton/skin (excluded by user). Complete visible tissue grasp blocked. Next action: obtain independently reviewed finger-surface and attachment/axis data, adapt manifest then rerun mesh/Blender/browser gates. Reopen on new source geometry or calibration. Existing deformation/penetration FAIL must persist.

## WD-2026-10-21-V2-NODE-TYPES
Status: RESOLVED
Failure: npm run build after actual-GLB Vitest tests were added: TS2307 node:fs types absent. Test runtime passes but typecheck fails. No skipped test/typecheck.
Paths: add proper @types/node development dependency (chosen) versus moving actual-asset tests out of TypeScript typecheck (reject hides coverage from typecheck). Shared node_modules symlink was initial dependency reuse, now replace with worktree-owned install before dependency changes to preserve other checkout.
Verified: declared @types/node in worktree-owned install; exact build and27 tests pass. No exclusions or dependency symlink remain.

## WD-2026-10-21-V2-IDLE
Status: RESOLVED
Failure: second Chrome recording generated report/screenshots but context.close remained pending while owned renderer/GPU busy; paused v2 still solves and scans unchanged full source geometry each second. Original: node scripts/grasp-v2/browser.mjs; browser-run.log and video retained. No PASS for completion of second run.
Paths: move full checks into worker (better concurrency, still redundant work) versus revision/time/pose convergence invalidation (chosen first because unchanged paused pose requires no recomputation). Preserve all full geometry checks on changed poses; mark report pose/time. Remove idle repeated solve rather than drop thresholds or skip contact. Reopen if original browser close still hangs after invalidation.
V2-IDLE evidence-preserving stop: own second recording process80084/Chrome80093 stopped after >5min pending close; partial203fee9f video retained, never counted as passing recording. Clean server/browser restart required to load fix (test mode disables HMR). Compare page/renderer teardown diagnostics if recurrence. No user browser processes touched.
V2-IDLE correctness extension: real test found unchanged opposite hand drifted ~3e-7 quaternion components after another control event. Finite transition completion now snaps to target at existing internal interpolation epsilon; idle invalidation no longer pauses an asymptotic interpolation then resumes it on unrelated edits. Tests await actual transition completion and retain exact opposite-side equality. No contact/geometry threshold changed.

## WD-2026-10-21-V2-REGRESSION-LABEL
Status: RESOLVED
Inherited browser test expected 'SEATED LAT PULLDOWN · 坐姿联动', while PR22/24 sceneLabel already intentionally says 'SEATED LAT PULLDOWN · UNVERIFIED'. Original failure captured in playwright.json/error-context. Compared restoring obsolete UI label (reject loses quality warning) versus updating assertion to documented baseline contract (chosen). Source playback.ts unchanged; matrix/source/actual playback assertions retained. No functionality gate skipped. Final exact regression rerun required below.

V2-NODE-TYPES verification: declared @types/node installed into worktree-owned node_modules; exact build and26unit tests pass. No typecheck exclusion remains.
V2-IDLE closure: clean server5186/fresh real Chrome reran original node scripts/grasp-v2/browser.mjs, exit0,97d618ab completeWebM. Exact opposite-side equality, pause/seek/loop and release pass. Finite transition completion and idle invalidation replace repeated unchanged computation. Failed videos preserved locally. No geometry threshold changed. Reopen on idle/teardown recurrence.

## WD-2026-10-21-V2-TEST-LOAD
Status: DEFERRED
Failure: existing pulldown regression exceeded unchanged30s timeout during a concurrent high-resolution Chrome recording. Other two tests passed. Compared serial heavy-browser scheduling (selected verification), GPU/load diagnostics, worker geometry evaluation. No timeout/quality threshold changed; no user apps stopped. Original report preserved locally. Next: exact serial three-test run, reopen on serial recurrence. Resource-contention cause remains an inference.

## WD-2026-10-21-V2-SCHEMA-RUNTIME
Status: RESOLVED
System Python lacked jsonschema. Compared isolated Python dependency versus worktree-owned Ajv2020. Selected Node project dependency; Windows schema unchanged and packet validates using npm run test:grasp-v2:contact. No global Python install, skipped schema gate or claim to repair system Python. Ajv validation is maintained project path.

## WD-2026-10-21-V2-SOLVER-OBJECTIVE
Status: RESOLVED
Original: reach-probe.ts with actual rig, y.055/z.02/radius.024 returned PENETRATION although sampled objective had low residual. Final continuous capsule validation correctly refused PASS.
Compared increasing sample density/penalty (still discretization mismatch) versus sharing bounded capsule-cylinder minimum between objective and validator (selected). Prepared rigid transform removes repeated inversions; objective enforces nonpenetration and per-digit contact. No tolerance changed (0.0001m). Original probe now PROXY_CONTACT for .008/.016/.024 reachable targets, no penetrating segments; exact numerical/actual bilateral tests retained. Tissue remains separate FAIL/GEOMETRY_INSUFFICIENT. Reopen if objective and validation diverge on another shape.
V2-TEST-LOAD final serial original three-test run PASS (46.479s total, all3, no skipped/flaky). Serial scheduling is disclosed verification scheduling, not proof that underlying concurrent GPU contention is fixed. DEFERRED diagnostic attribution reopens on a serial timeout.
V2-REGRESSION-LABEL durable verification: same original pulldown/curl regression with corrected UNVERIFIED contract passes; playback.ts and quality semantics unchanged.
