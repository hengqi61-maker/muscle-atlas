# P2 official-bar alignment (isolated)

Reuses PR #21 `poseFor` / 30 additive bones. Does not add a skin shell. Does not rewrite 467 POSITION.

## Method

1. Load `artifacts/grasp-v1/grasp-controller.glb`.
2. CCD-reach existing `Clavicle→Scapula→Humerus→Forearm→Wrist` so `LeftHand` / `RightHand` chase `latPulldownFrame` grips (radius 24 mm, half-width 0.37 m).
3. Apply the `pulldown-bar` finger preset every phase.
4. Measure **tissue** triangles and **bone-tip** wrap separately.

G2 rest-height `PERSISTENT_INTERSECTION` is not treated as success.

## Measured (this PR)

`artifacts/grasp-v1/p2/official-bar-align.json`

| progress | hand reach error | tissue min signed | wrap bins | tissue | skeletal |
|---:|---:|---:|---:|---|---|
| 0 | 34 mm | −23.6 mm | 2 | TISSUE_INTERSECTION | NO_WRAP |
| 0.25 | ~0 | −21.9 mm | 1 | TISSUE_INTERSECTION | NO_WRAP |
| 0.5 | 3 mm | −23.7 mm | 1 | TISSUE_INTERSECTION | NO_WRAP |
| 0.75 | ~0 | −23.5 mm | 1 | TISSUE_INTERSECTION | NO_WRAP |

**Overall: `FAIL_TISSUE_GRASP` + `SKELETAL_INCOMPLETE`.** Official-bar reach of the 27-bone chain is possible; 30 finger bones still do not wrap the cylinder, and palmar muscle remains ~24 mm inside it. No skin shell was added. Historical pulldown FAIL unchanged.
