# Seated Lat Pulldown · first milestone acceptance contract

**Status: DRAFT / NOT AUDITED**. This is a checklist, not a claim that the current Blender model is correct.

## Baseline being reviewed
- `src/three/Scene.tsx`: loads `/models/anatomy-pulldown.glb` and controls `AnimationMixer` using the shared store clock.
- `src/three/LatPulldownMachine.tsx`, `src/three/pulldownMotion.ts`, `src/data/pulldown-config.json`: procedural cable machine/bar/weight.
- `src/data/latPulldown.ts`: anatomical source mesh ID/qualitative role relations.
- Record the frozen Git SHA and GLB SHA256; the two may update independently.
- Original palm and digit geometry is kept by default per user feedback; do not reinstate reversed generated grip overlays without owner signoff.

## Reference/variant
Seated, front-of-head wide/comfortable-grip lat pulldown toward upper chest; bilateral neutral/symmetric repetition with the torso supported and controlled return. Validate against at least two named trustworthy exercise/biomechanics sources. This is a visualization of a representative movement, not individualized medical advice or direct EMG activation measurement.

## Acceptance matrix
| ID | Gate | What to inspect | Reject when |
|---|---|---|---|
| K01 | Coordinate/scale | Human pelvis-seat contact, thigh pad, feet/platform, arm reach and bar position in metres | Machine scale incompatible, hovering or deep intersections |
| K02 | Grip/handedness | Both wrist transforms and original hands at 0/25/50/75/100% in front/side/close-up | Grip reversed, palms face wrong way, clear loss of bar contact |
| K03 | Elbow & shoulder | Upper/forearm anatomical segment lengths and humeral orientation trajectories from rig joint transforms | Limb stretches, snaps, unnatural dislocation, elbow bending backwards |
| K04 | Scapula | Plausible bilateral scapular orientation/translation as arms raise/lower; shoulder mechanics documented | Scapular region effectively locked while gross humeral pose demands movement or visible clipping |
| K05 | Torso/pelvis | Controlled trunk without unwanted repeated lumbar flexion/rocking | Excessive displacement, body passing through seat |
| K06 | Cable | Bar displacement, moving stack, cable endpoint positions on same timeline; endpoint continuity; tension assumptions stated | Bar/weight out of phase, cables detach or pass through impossible route |
| K07 | Muscular deformation | Lats, teres major, upper arm and shoulder meshes in motion; topology and picking, stable ID | Mesh clipping/tearing, left-right swapping, invisible or disconnected muscle bundles |
| K08 | Muscle roles | Primary/secondary/stabilizer role map on source mesh IDs; English original names remain traceable | fabricated intensity percentages or qualitative classification displayed as measured activation |
| V01 | Visual | Camera front/left side/back/grip close-up; 0/25/50/75/100% frames, real and clean style | Missing evidence or obvious anatomical geometry error |
| S01 | Regression | GLB opens, animations/skins are nonzero, independent muscle pick and style switch still work | Loss of 467-source ID mapping or broken animation/seeking |
| S02 | Stability | build/unit/browser tests, console warnings, performance baseline | Runtime error, untracked failure or regression |

## Measurement rules
- Report in **metres**, **degrees**, and **seconds**, using rig/world transforms from the same coordinate frame; do not derive grip precision solely from hand IK target positions.
- Sample at least 21 evenly spaced times for numerical trajectories. Screenshots at minimum 0/25/50/75/100% from the specified views.
- Report hand-to-bar **position distance** and **orientation** separately; also examine palm/thumb/finger winding by visual inspection.
- A fixed bone length is a kinematic constraint, not a proof of valid shoulder/scapula coordination. No rigid universally correct joint-angle cutoff is assumed; ranges require reference or documented model-specific justification.
- Record major mesh intersections and report whether they are gross geometry collisions, original anatomical model limitations or deliberate artistic approximations.
- Report phase alignment in source time units for animation clip vs machine curve. If `AnimationMixer` retiming changes, recompute measurements rather than infer from the UI slider.
- User acceptance requires a real full-rep video + frame sheet + individual reviewer verdicts. A passed test suite **never** implies medical-grade biomechanics.

## Reviewer deliverable
Write report in `docs/reviews/lat-pulldown/<sha>/` or attach review artifact to PR:
- `biomechanics.md`, `visual.md`, `exercise-science.md`, `software-qa.md`.
- Each: target SHA, evidence paths, K/V/S IDs, severity (P0/P1/P2), verdict PASS/FAIL/INCONCLUSIVE, reproducible findings, citations where required.
- A `summary.md` must enumerate unresolved blockers, any proposed exception, and **USER APPROVAL: pending / approved**.
- No auto-approval based purely on counts; reviewer may stop for missing evidence.
