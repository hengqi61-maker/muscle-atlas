# Codex → Cursor takeover (2026-10-20)

Not merged. `main` remains `7a0d258`. This branch is `cursor/pulldown-takeover` from PR #19 `1e6dee5`.

## Version map (all Draft)

| PR | Head | Role | Inherit? |
|---|---|---|---|
| #8 | `1b06bf4` | R1 467/27 pipeline, PulldownProbe/CurlProbe | Yes, frozen FAIL |
| #12 | `13ddb46` | E01/E02 rejected; E03 not a motion repair | Evidence only |
| #16 | `a8247a4` | Windows contact / OpenSim W-F4 INCONCLUSIVE | Evidence only |
| #17 | `c6f04a1` | M3-A freeze; no new weight/axis write | Binding |
| #19 | `1e6dee5` | Console wired R1 probes next to 高位下拉 | **P1 base — the product leak** |
| #21 | `420a818` | 30 additive finger bones + G2 `PERSISTENT_INTERSECTION` | **P2 controller, not a PASS** |

Cursor G0–G2 on PR #21 is not a second finger system. Codex did not finish official-bar alignment or the console split.

## What was already done (do not redo)

- 30 FingerSocket children, left/right `curl`/`thumb`/`spread`, presets, Blender/Three posed-contact, isolated panel.
- Diagnostic *labels* on PR #19, but the version dropdown still loaded `PulldownProbe` from the ordinary 高位下拉 path.
- Historical pulldown/curl FAIL numbers, 467 POSITION, production GLBs.

## Conflicts

- PR #21 is based on #8, not #19. This takeover copies grasp sources onto #19 instead of merging stacks.
- Grasp GLB has no PulldownProbe clip (`export_animations=False`).
- R1 is standing 27-bone; seated training GLB is a different asset (`anatomy-pulldown.glb`) without the 30 bones.
- G2 bar was rest-height through the torso — not the official pulldown trajectory.

## Still broken

1. Official seated pulldown remains UNVERIFIED (open hands, tissue in handle).
2. G2 tissue grasp FAIL (`PERSISTENT_INTERSECTION`).
3. Whole-body LBS repair BLOCKED: E01/E02 rejected; W-F4 INCONCLUSIVE; no new weight/axis scan in this PR.
4. No visible five-finger geometry on source meshes. Skeletal wrap ≠ tissue grasp.
