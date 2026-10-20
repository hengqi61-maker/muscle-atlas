# Grasp Controller v1 (isolated experiment)

Issue #20 option B. Branch `codex/grasp-controller-v1` from PR #8 `1b06bf4`. Frozen R1 POSITION / 467 identities / production GLBs are not replaced.

## G0 — existing hands cannot independently flex

Inspected experimental copy SHA256 `ef803a4bbb3c644504c124519e39ba0b3b760ec139eaf60d277ef7f7f5d23274`.

| Fact | Value |
|---|---|
| Source meshes | 467 identities unchanged |
| Canonical bones | 27; digit-like names = `Left/RightFingerSocket` only |
| Skin shell | **Absent.** Coverage is muscle/tendon sets |
| Independent digits on frozen 27 | **No** |

Therefore G1 adds **reversible child bones** under FingerSocket and spatially partitions existing Hand-dominated weights. This is a geometric proxy, not clinical CMC/MCP/PIP/DIP.

## G1 — controller

- Schema: `config/grasp-v1/schema.json`
- JS API: `src/grasp-v1/controller.mjs` (`poseFor`, `lerpPose`, `applyToObject3D`)
- Per hand: `curl`, `thumb`, `spread` in `[0,1]`
- Presets: `open`, `half`, `closed`, `pulldown-bar`, `rope-end`
- 15 bones/hand × 2 = 30 additive bones
- 36 hand-region meshes received extra groups; **POSITION SHA unchanged**

## G2 — real runs (Blender 5.2.0 `fbe6228777e7`)

| Check | Result |
|---|---|
| Build | `artifacts/grasp-v1/grasp-controller.glb` SHA256 `40e3dbcbbe3423381dd2885936dd3f1c7d4355bcc6b4f0c30eb9245537be1dff` |
| Evaluated left lumbricals, Index/Middle/Thumb +1.1 rad | max Δ **48.5 mm**, p50 15.0 mm, p90 42.1 mm |
| Three.js `GLTFLoader.parse` + controller | 57 bones, **30 finger hits** open and closed |
| Controller unit tests | 3/3 PASS |
| Interpolation video | `grasp-open-to-closed.mp4` SHA256 `2f8c26ac766f2e949db39b80eb289be05a2eae7690a880c6bd9555caecc575ae` |
| Rest-space prop table | **not posed contact** (same numbers every preset). Rope rest overlap ~8.4 mm / 132 verts; bar rest gap ~210 mm. Fail closed: posed penetration UNKNOWN |

Close-up PNG cameras framed forearm tendon fans more than palm pads. Use `verify-deform.json` as numeric deformation proof; pixels are observation only.

## What this is not

- Not pulldown/curl motion PASS. Those FAIL numbers stay.
- Not a real skin grasp or Owner anatomy approval.
- Not a production hand replacement.

## Reproduce

```sh
# from this worktree
/Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup --python scripts/grasp-v1/inspect_hands.py
/Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup --python scripts/grasp-v1/build.py
/Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup --python scripts/grasp-v1/verify_deform.py
node --test tests/grasp-v1/controller.node.mjs
npm ci --ignore-scripts
node scripts/grasp-v1/three-smoke.mjs
```

## Next

1. Palm-locked cameras and posed (evaluated) contact-v1.1 packets.
2. Optional later: a disposable skin shell if Owner wants visible phalanges; do not invent anatomy on frozen source.
3. Call the same `poseFor(preset, side)` from new exercises; do not rebuild a hand per motion.
