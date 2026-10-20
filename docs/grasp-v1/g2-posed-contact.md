# G2 posed contact — pulldown bar only

Draft PR #21 / Issue #20. Isolated experimental copy. Pulldown/curl historical FAIL unchanged.

## Fixture

One finite cylinder, historical lat-pulldown grip radius **24 mm**, rest-pose hand height, world +X, half-length 0.34 m. Not overhead pulldown travel. No rope this round.

- Blender Z-up origin `(0, -0.1349, 0.7572)`
- glTF Y-up origin `(0, 0.7572, 0.1349)` (`export_yup=True`)

## What the 38 hand-region meshes actually are

| Class | Count | What it is | Not |
|---|---:|---|---|
| thenar | 12 | thumb-eminence muscle bellies | finger pulps |
| hypothenar | 6 | little-finger eminence | fifth-digit skin |
| digit-muscle-set | 6 | lumbrical / palmar / dorsal interosseous **sets** | five separate phalanx surfaces |
| long-tendon-thumb | 8 | FPL / EPL / EPB / APL | digits 2–5 |
| wrist-retinaculum | 2 | wrist flexor retinaculum | palm skin |
| accidental-forearm | 2 | interosseous membrane of forearm (G1 name-key leak) | hand contact tissue |

Foot / leg hits from G1’s `interosse` / `digiti minimi` keys were excluded here. There is **no finger skin shell**.

## Evaluated triangle contact (Blender 5.2 depsgraph + Three.js `getVertexPosition`)

| Preset | Blender min signed | Blender inside samples | Three min signed | Verdict |
|---|---:|---:|---:|---|
| open | −23.97 mm | 102140 | −23.71 mm | PERSISTENT_INTERSECTION |
| half | −23.94 mm | 96368 | (measured) | PERSISTENT_INTERSECTION |
| closed | −23.54 mm | 83397 | −23.51 mm | PERSISTENT_INTERSECTION |
| pulldown-bar | −23.57 mm | 89018 | −23.91 mm | PERSISTENT_INTERSECTION |

Nearest tissue at open is `set of lumbricals` (both sides), already almost on the cylinder axis. Closing **reduces** inside-sample count but does not leave the solid. Open already occupies 8/8 angular bins because the bar is embedded in the palmar cloud — that is impalement, not a formed grip.

Context stills (`shot-context-*.png`) show two tendon/muscle tufts hanging on the bar. Digit stills show disconnected green slips, not five fingers.

## Skinning defects on closed vs open

Closed-pose edge/winding vs bind (same 38 meshes):

- `set of lumbricals` L/R: 244 flipped triangles, stretch max ≈ 14×, 127 edges >2×
- `flexor retinaculum` L/R: 50 flips, stretch max ≈ 10.8×
- thenar group (APB / FPB / opponens / adductor): 14–22 flips, stretch max 6–12×
- `set of palmar interossei`: almost rigid (max stretch ≈ 1.009) — they barely follow the new bones

These are real LBS tears, not camera artifacts. Do not retune weights to fake phalanges.

## Continuity

Blender 36-frame open→closed→open (`g2/open-closed-open.mp4`) and the isolated Three panel (`src/grasp-v1/panel.html`) both return to the open thenar/hypothenar silhouette. Playwright: `PANEL_TRANSPORT_PASS` (play, pause, scrub 0.5 / 1.0, loop off). Sliders drive left/right `curl` / `thumb` / `spread` independently.

## Reproduce

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup --python scripts/grasp-v1/g2_verify.py
ffmpeg -y -framerate 12 -i artifacts/grasp-v1/g2/frames/frame-%03d.png -c:v libx264 -pix_fmt yuv420p artifacts/grasp-v1/g2/open-closed-open.mp4
node scripts/grasp-v1/g2_contact_three.mjs
python3 -m http.server 8766 --bind 127.0.0.1
node scripts/grasp-v1/g2_panel_playwright.mjs
node --test tests/grasp-v1/controller.node.mjs tests/grasp-v1/cycle.node.mjs
```
