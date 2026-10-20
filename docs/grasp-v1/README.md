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

## G2 — posed bar contact (Blender 5.2.0 `fbe6228777e7` + Three.js)

Posed contact is no longer UNKNOWN. Packet: `docs/grasp-v1/g2-posed-contact.md`. Topology limit: `docs/grasp-v1/topology-limit.md`. Isolated panel: `src/grasp-v1/panel.html`.

| Check | Result |
|---|---|
| Sole solid | pulldown-diameter cylinder, r=24 mm, rest-pose hand height |
| 38 hand-region meshes | thenar / hypothenar / lumbrical-interosseous sets / long thumb tendons / retinaculum. **No finger skin.** |
| Blender evaluated triangles | open −23.97 mm / closed −23.54 mm, 8/8 bins already at open → **PERSISTENT_INTERSECTION** |
| Three.js skinned triangles | open −23.71 mm / closed −23.51 mm (same fixture, glTF Y-up) |
| Seams on closed | lumbricals 244 flipped tris, stretch max ~14×; retinaculum ~10.8×; thenar 6–12× |
| O→C→O video | `g2/open-closed-open.mp4` SHA256 `d8983e59d4ec398fdc5dce762b8236a718ddc6fb81468f0819f735f22302758c` |
| Three panel transport | Playwright `PANEL_TRANSPORT_PASS` (play / pause / scrub / loop) |
| Controller unit tests | 6/6 PASS |

G1 rest-space prop table remains invalid as posed contact. G1 GLB SHA unchanged `40e3dbc…`.

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
node --test tests/grasp-v1/controller.node.mjs tests/grasp-v1/cycle.node.mjs
npm ci --ignore-scripts
node scripts/grasp-v1/three-smoke.mjs
/Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup --python scripts/grasp-v1/g2_verify.py
node scripts/grasp-v1/g2_contact_three.mjs
python3 -m http.server 8766 --bind 127.0.0.1
node scripts/grasp-v1/g2_panel_playwright.mjs
```

## Next

1. Do not retune weights to fake fingers. If Owner wants recognizable digits, implement the additive overlay in `docs/grasp-v1/topology-limit.md` on a new isolated copy.
2. Call the same `poseFor(preset, side)` from new exercises; do not rebuild a hand per motion.
3. Pulldown/curl FAIL numbers stay. Do not start Face Pull from this packet.
