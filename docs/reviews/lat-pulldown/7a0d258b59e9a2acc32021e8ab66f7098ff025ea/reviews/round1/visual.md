# Frozen blind visual first report

Candidate Git SHA: `7a0d258b59e9a2acc32021e8ab66f7098ff025ea`  
GLB SHA256 supplied for candidate: `56b3ca231dda14100d64233758da2116282547b472afd4fc9b24160f345fee05`  
Role: independent visual reviewer. Final first-report freeze: 2026-10-15. No implementation edits, fixes or merge. No historical records, README, debt records, prior reviewer conclusions or old worktrees were read.

## Evidence actually inspected

Packet root: `artifacts/blind-review/7a0d258b59e9a2acc32021e8ab66f7098ff025ea/` in exact candidate checkout. Read neutral protocol AGENTS, own `.codex/agents/visual_reviewer.toml`, acceptance contract and motion workflow. Inspected all 50 production stills in `frames` and `frames-real`: front, side, back, grip and right-grip at 0/25/50/75/100%. Each original is 1440x1000; coordinates below refer to originals, origin top left. Also enlarged original grip/50, right-grip/0, side/50, real back/50 and real grip/50. Derived contact sheets only in `/tmp`.

Video: final `full-rep.webm`, ffprobe duration 47.32 seconds, decoded with ffmpeg at 2 fps and visually inspected every resulting temporal sample (0.0–47.0 seconds). This is actual production playback evidence, not self-generated animation. Front playback ~2.5–12.5s, side ~13.5–23.5s, back ~24–35s, grip ~36–47s. Video grip camera is fixed and the descending hand leaves part of its frame; tracked stills supply the missing close-up coverage. No claim of inspecting every native video frame or measuring temporal acceleration.

Read actual GLB node names only to establish that named hand meshes exist. No pixel feature is assigned an exact mesh ID without a raycast or mesh-isolation check. Metadata contact-target errors do not prove actual surface grasp.

## Verdicts

| Gate | Verdict | Scope / reason |
|---|---|---|
| V01 | **FAIL** | Required real evidence exists, but a plainly isolated anatomy-colored fragment above the cable/bar is an obvious continuity error (F1). |
| K01 | **INCONCLUSIVE** | Seated arrangement is visible; pelvis appears adjacent to seat. Foot/platform contact and thigh-pad compression cannot be established from these source muscle surfaces and occlusions. Side image shows distal anatomy terminating above the platform. No metre-scale claim from pixels. |
| K02 | **INCONCLUSIVE** | Both hand regions remain near their grip ends, but exposed elongated anatomy and black-grip occlusion prevent reliable palm-facing, thumb opposition and closed finger winding judgments. Do not call either side reversed from these images. F2 records the precise unresolved evidence. |
| K03 | **INCONCLUSIVE** | No gross snap/backward elbow seen in temporal samples; no transform-based segment or joint validation performed by this visual review. |
| K04 | **INCONCLUSIVE** | Bilateral posterior shoulder outline changes, but scapular anatomical orientation and translation cannot be determined from these pixels/highlighting. |
| K05 | **PASS (visual scope only)** | Across side temporal samples torso/pelvis remain controlled, without visible repeated rocking or gross passage through seat. This is not a lumbar-angle validation. |
| K06 | **PASS (visible portion only)** | Visible bar/cable remain attached and stack rises as bar lowers, reverses on return. Hidden pulley routing, cable tension and exact phase are outside pixel verification. |
| K07 | **FAIL** | Detached anatomy-colored fragment persists through motion (F1). Other source anatomical gaps cannot be labeled new tears without mesh-level/source comparison. No muscle ID/picking invariants independently verified. |

## Findings

### F1 — P1: Detached anatomical-looking geometry above bar/cable, high confidence

Actual: `frames/grip/50.png`, rectangle approximately **x370–417, y109–187**, contains a gray tendon/digit-like fan visibly isolated from the body and hands. Same object is red in `frames-real/grip/50.png` at the same location, strongly distinguishing it from machine hardware. Mirrored viewing corroboration: `frames/right-grip/0.png`, approximately **x976–1065, y99–193**, has the same class of isolated anatomical-looking strands above the subject and cable. It is also visible in side/50 near **x549–565, y378–413**, above the bar and forward of the head. It is not a lighting-only artifact.

Temporal corroboration: full-rep video grip samples around **37.5–40.0s** and **41.5–43.5s** show this isolated form beside the central cable while the body and bar move. It persists instead of appearing only during a seek/camera transition.

Expected: anatomy intended to depict the subject stays anatomically connected or is explicitly identified as a separate reference object. An isolated tissue-like fan above the cable is an obvious continuity defect in this teaching view. Exact mesh and cause are **not established** by pixels; do not assume it is an entire extra hand or a specific tendon.

Reproduction: open the frozen production scene, select pulldown, Clean Tech, seek 2.0/4.0s, use packet grip camera; compare Real Anatomy at same phase. Alternatively inspect the exact listed supplied files/video timestamps.

Verification needed: isolate/pick the responsible GLB mesh or vertex component and verify its world-space connection, skin weights and transform across all phases. Preserve original anatomical source geometry; do not prescribe a procedural replacement. Re-review regenerated closeups and complete rep after any fix.

### F2 — P1 acceptance uncertainty: actual bilateral grasp is not demonstrated, medium confidence observation / high confidence limitation

`frames/grip/50.png` near **x700–823, y424–560** and `frames/right-grip/0.png` near **x594–697, y432–558** show long narrow anatomical surfaces draped along the grip region, with much of the black grip unobscured. They do not show a clearly readable opposing thumb plus curled digits around the cylinder. This is **not proof** of a reversed hand, wrong palm normal, a depth gap, or a penetrated grip; depth and surface identity remain ambiguous. Both Real Anatomy counterparts preserve that ambiguity.

Reproduction: inspect both named closeups at all five phases; compare tracked stills with video grip samples. Contact markers alone cannot resolve this.

Verification needed: opposing closeups or isolated original hand meshes with a declared palm normal, thumb/digit identities and actual hand-surface-to-cylinder intersection/contact analysis. Keep K02 INCONCLUSIVE until that exists; no synthetic folding or skin overlay is implied or authorized.

### F3 — P2 observation: support contact remains visually unclear

In `frames/side/50.png`, distal lower-leg/foot-like source anatomy ends around **x480–501, y797–807**, while the platform is around **y825–845**. The thigh pad is largely seen end-on near **x540–596, y614–663**; it does not expose its full relation to both thighs. These images cannot distinguish a missing source foot surface from actual support misplacement. This is a bounded K01 uncertainty, not a verified hovering-body blocker. Verify source foot representation and physical contact coordinates in metres, then capture an unobstructed oblique support view.

## Completion / limitations

Completed primary goal: independent blind visual first report, all supplied stills plus dense actual-video samples inspected; V01 FAIL, K07 FAIL; no P0 asserted. No implementation workarounds introduced and no workaround debt created by this read-only review. No historical debt inspected or adjudicated. No fixes or runtime/assets altered. Remaining evidence: F1 mesh isolation and durable correction; F2 actual hand orientation/contact evidence; K01 support geometry; transform/scapula evaluation by the appropriate reviewer. User approval remains pending and this report cannot approve a milestone.
