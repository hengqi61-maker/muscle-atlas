# MuscleAtlasV2 R1 canonical source-skin prototype

This isolated experiment does not replace `public/models` or the formal exercise viewer. All motion is an illustrative kinematic probe. The two clips share one 467-mesh skin and one canonical hierarchy. No procedural hands, skin shell, source finger folding, grip-contact claim, invented training history or muscle-force percentages are introduced.

## Reproduction

Invoke Blender Agent `execute_script` with:

```python
import runpy
runpy.run_path('/absolute/path/to/checkout/scripts/rig-v2/build.py', run_name='__main__')
```

Run `evidence.py` and `verify_source.py` the same way, each in a fresh Blender Agent operation. Paths are resolved from each script; no server working-directory dependency. `build.py` writes only the new `config/rig-v2`, `public/experimental/rig-v2`, and `artifacts/rig-v2` outputs. It asserts the original atlas source SHA before importing.

Build output: `public/experimental/rig-v2/unified-rig-prototype.glb`. Native scene: `artifacts/rig-v2/unified-rig-prototype.blend`. Export uses Blender 5.2, glTF NLA tracks, source mesh extras, linear blend skinning and Y-up conversion. The source object names and IDs remain separate from canonical bone names.

`canonical-rig.json` declares units, axes, handedness, hierarchy, roll convention, parent-local/world rest matrices, xyzw quaternions, landmarks and confidence. `attachment-registry.json` provides all467 source identities and per-vertex weights, bones and endpoint vertex regions. Endpoint regions are geometric Z deciles, explicitly not calibrated anatomical origins/insertions. The internal schema is not a final Windows/OpenSim exchange standard.

## Actual evidence and limits

- Fresh original atlas import compared with native base geometry: all467 exact after the specified float32 source-to-canonical transform, with identical polygon vertex index ordering. Test uses zero coordinate tolerance.
- Both clips: actual native renders at31 times, frames0..120 step4, fps30 motion. Encode the PNG sequences with `ffmpeg -framerate 7.5 -i <Clip>-sequence/%03d.png -c:v libx264 -pix_fmt yuv420p <Clip>-native.mp4`.
- `deformation-diagnostics.json`: actual evaluated triangle areas and edge ratios across5 poses per clip. CurlProbe peak42 triangles below5% base area; PulldownProbe endpoint39 such triangles and max edge stretch3.988. These failures remain visible and are not acceptance passes.
- `collision-diagnostics.json`: actual BVH triangle intersection checks, four selected arm/torso mesh pairs across5 poses per clip. Zero tested pair intersections does not establish whole-body clearance or equipment contact.
- `corrective_framework.py` implements reusable clip-independent quaternion skin target and inverse-LBS delta calculation. `corrective-framework-probe.json` numerically exercises real bindings from three meshes, but no corrective has been silently installed. Such corrections require scoped validation and review.
- Source hand surfaces remain unchanged. Hand controls move rigidly with the limb; FingerSocket nodes reserve a nondeforming interface. There is no functional grasp validation or finger animation.
- Standing upper-limb probes do not demonstrate validated seated pulldown, machine linkage, lower-limb movement or biomechanical muscle deformation. Existing upgraded formal equipment remains untouched.

Producer evidence is for four fresh independent reviewers; it does not approve itself.
