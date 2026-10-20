# M3-A failure freeze and coordination (Cursor TL)

Stamp: 2026-10-20T03:30:00Z  
Coordinator: Mac Cursor (Technical Lead)  
Authorization: freeze FAIL baseline, publish a root-cause hypothesis matrix, review Blender Skills/MCP boundaries, coordinate Mac/Windows.  
**Not authorized:** production asset edits, Draft PR merges, threshold relaxation, Face Pull, write-permission expansion, or a new anatomical repair candidate.

## Frozen heads (do not assume merged)

| Artifact | Ref | Head SHA | State |
|---|---|---|---|
| Phase 1 motion pipeline PR #8 | `codex/rig-v2-motion-pipeline` | `1b06bf4d94169868acdca5f3a430bc964f2cafa0` | OPEN draft; M3-A comparison base |
| Phase 2 experiments PR #12 | `codex/rig-v2-phase2` | `7214f3ffbf5c1315323d976b62f73a5b100faaf9` | OPEN draft; **both variants REJECTED** |
| Windows bio PR #9 | `codex/biomechanics-validation-v2` | `c1d7e209901390bfb73f784e0f1f48c8337f2e17` | OPEN draft; contact-v1 + shoulder **model** refs |
| Blender skills PR #14 | `codex/blender-skills-pilot` | `da9a947aa60f60329f8b6a62294d2f8462fa1aa9` | OPEN draft; fixture-only tooling |
| Blender MCP PR #15 | `codex/blender-mcp-integration` | `7624e5b9df9ca50e88d2e52b49dbeece50cdd916` | OPEN draft; guarded observation |
| Default `main` | — | — | **does not** carry these heads |

Evidence package for the rejected Phase 2 candidates: release `evidence-phase2-8dc8661`, ZIP SHA256 `43c93433f328972c05771fc306f6c5e72af6c3adcf6137c7e17d26310e8ca990`. Frozen experimental R1 copy SHA256 `ef803a4bbb3c644504c124519e39ba0b3b760ec139eaf60d277ef7f7f5d23274`.

## Frozen motion FAIL (authoritative)

Thresholds unchanged: area `<0.05`; per-mesh count `>3` OR fraction `>1%`; edge `>2`. Full-triangle 121 samples × two diagnostic clips. Engineering screens, not medical strain limits.

| Candidate | Curl severe | Pulldown severe | Pulldown max edge | Continuity / path | Decision |
|---|---:|---:|---:|---|---|
| Fresh frozen baseline | 39 | 91 | 3.988438 | peak BP4795/FMA13414 △914 edge 456–466, Pulldown frame 0 | FAIL |
| E01 local-weight λ=0.5 | 39 | 91 | 6.469800 | 11 source-equivalent groups split; pair 441/1288 **3.179553 mm** Pulldown frame 0 | REJECTED |
| E02 Forearm axis α=1 | 39 | 93 | 3.988438 | wrist path Δ Curl 24.767 mm / Pulldown 21.699 mm; 12 new Pulldown mesh-poses | REJECTED |

Independent reviews on PR #12: biomechanics FAIL; visual gross FAIL / micro INCONCLUSIVE; software invariants PASS with E01 continuity FAIL. Owner **PENDING**. Structural reuse AUTO PASS (467/27) is **not** motion PASS.

## What M3-A is investigating (read-only)

Four coupled failure families. None is uniquely proven as *the* anatomical cause.

1. **Bone axes** — E02 showed a 4.69869° Forearm localX vs rest-world-X driver is geometrically real, but changing it moves the wrist and worsens held-out Pulldown. Scapula/humerus axes are untested. OpenSim on PR #9 is rank 3 over 12 unlocked coordinates (local tangent 9), **model ≠ anatomy**.
2. **Attachments** — peak remains right subscapularis BP4795 △914. Spatial neighborhoods used by E01 are engineering rings, not glenoid/humerus landmarks. MCP (PR #15) can name the mesh and read polygon 914 (`verts [466,456,468]`); it cannot certify attachment.
3. **Continuity / export aliases** — E01 proved originally coincident same-mesh POSITION+JOINTS+WEIGHTS rows can diverge after independent weight writes. New `seam-check.mjs` is now a required negative detector (exit 1 on E01).
4. **Weight mapping** — E01 two-point calc: rest edge 1.190419 mm → 4.747912 mm with humeral weight Δ 0.017622. Gradient × bone differential motion is a mechanism for *this edge*, not a calibrated subscapularis insertion.

Windows Issue #11 (2026-10-19): 363/363 source-triangle packets locally scanned; adductor-pollicis intrusion vs convex grip remains; 22 exercise/source topologies UNKNOWN. That packet is **not yet a published PR**. Contact ≠ motion PASS ≠ grasp PASS.

## Dual-end gate before any new experiment

A single minimal experiment is **not authorized in this freeze**. It may be proposed only after **both**:

- Mac: this freeze + hypothesis IDs remain unchanged; no extra variable mixed in.
- Windows: publish W-F4 comparable-axis / landmark packet **or** an explicit INCONCLUSIVE that OpenSim cannot constrain Mac attachments, with Git-byte hashes and LF/CRLF labels. Do not map model angles onto the GLB.

Until that packet exists, parked local E03-style equivalence projection (uncommitted on the PR #12 worktree, software-only note, no published 121-frame motion scan in PR #12) is **not** the M3-A candidate and must not be merged.

## Tooling boundary (parallel, non-blocking)

See `docs/dev/blender-tooling-boundary.md`. Skills (PR #14) and MCP (PR #15) stay **observation / fixture QA**. They must not write frozen R1, weights, or production GLB. `blender_agent` remains a separate Codex server; do not share one Blender MCP socket with Cursor. Agent Bridge C1 network isolation is still BLOCKED; W-F5 is not a prerequisite.

## Owner decisions still required

- Whether any later experimental candidate may enter OWNER_APPROVAL after PASS geometry + independent reviews.
- Whether Bridge C3 writable mode may turn on (separate from Muscle Atlas merges).
- Formal model replacement / protected-branch merge.

## Next actions

| ID | Owner | Now |
|---|---|---|
| M3-A-TL | Cursor | This freeze + matrix; Draft PR docs only |
| M3-A-WIN | Windows Codex | W-F4 comparable axes/landmarks or explicit INCONCLUSIVE; keep contact-v1 unknown frames as null |
| M3-A-MAC | Mac Codex | Do **not** start a new weight/axis candidate until W-F4 lands; keep E01/E02 FAIL assets immutable |
| M3-A-TOOL | Mac Codex | Keep PR #14/#15 Draft; no production skill/MCP write path |
