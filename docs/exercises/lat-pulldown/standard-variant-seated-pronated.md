# Standard variant: seated front-of-head pronated pulldown

Locked for this takeover. Coaching text from ACE Seated Lat Pulldown and NASM lat-pulldown biomechanics (links only). Not motion capture.

## Definition

| Phase | Required |
|---|---|
| Setup | Seated; thigh pad firm; spine braced; no extra lumbar arch |
| Grip | Pronated, both hands on the bar; this project’s machine uses `gripHalfWidth` 0.37 m, radius 24 mm |
| Start | Arms overhead; scapulae depressed/retracted; lean ≤ 30° |
| Concentric | Scapular depression first; elbows drive down to the torso; bar to upper/mid chest **in front of the head** |
| Stop | When elbows stop going down and start going back — do not keep pulling into the joint |
| Eccentric | Controlled rise to full elbow extension, then allow scapulae to elevate slightly |
| Sync | Bar, cable, and weight stack share `latPulldownFrame(progress)` |

Not this variant: behind-the-neck, standing probe, PulldownProbe, or any clip without seat/bar.

## Current assets vs the variant

| Asset | Match |
|---|---|
| `anatomy-pulldown.glb` + machine | Seated + shared timeline. Hands do not close. Historical tissue/handle FAIL. **UNVERIFIED training entry.** |
| R1 `PulldownProbe` | Standing, no seat/bar. **Diagnostic only.** |
| PR #21 grasp GLB | 30 finger bones on rest-pose R1. G2 rest-height bar = `PERSISTENT_INTERSECTION`. |

## P3 block

E01/E02 were rejected (PR #12 / #17). W-F4 is INCONCLUSIVE (PR #16). This PR does **not** write new whole-body weights or axes. Pulldown/curl FAIL remains. Next authorized anatomy step stays read-only BP4795 correspondence unless Owner opens a new single-variable experiment.
