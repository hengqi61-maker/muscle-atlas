# R1 full-triangle findings

Frozen input: `ef803a4bbb3c644504c124519e39ba0b3b760ec139eaf60d277ef7f7f5d23274`. No source or motion asset was modified. The full-triangle experiment checks **1,092,000 exported triangles** in 467 meshes at 121 actual skinned poses in each diagnostic clip. The exact data and hash are in `attribution-results.json`; the evidence package contains the full report, exact first/worst events and labelled source-mesh closeups.

| Actual measurement | CurlProbe | PulldownProbe |
| --- | ---: | ---: |
| Poses with per-mesh severe compression alarm | 39 / 121 | 91 / 121 |
| Maximum edge stretch | 1.595631367× | 3.988438336× |
| Geometry assessment | FAIL | FAIL |

These full-coverage counts are additional evidence. The historical R1 **42 / 121** PulldownProbe sampled-surface failure remains frozen. Neither threshold nor historical report was changed.

For CurlProbe, the earliest severe sample is frame 41: bilateral brachioradialis BP8244 / BP4833. Bilateral humeral pronator teres BP8015 / BP5568 first alarms at frame 47; long-head biceps BP8816 / BP5566 at frame 54. The full scan catches elbow-region compression omitted by the older sparse triangle sample. Worst compression can occur at different times on left/right tissue, and no biological symmetry is inferred.

For PulldownProbe, both supraspinatus BP8376 / BP4791 and clavicular/spinal deltoid compartments already alarm at sampled frame 0. This is the elevated-arm **animation start**, not the immutable source reference pose. Acromial deltoid begins alarming at frame 17; elbow/forearm tissue adds failures later. A single endpoint or bone-length check would miss these surface failures.

The 3.988438336× peak is localized to **right subscapularis BP4795 / FMA13414**, exported triangle **914**, edge vertices **456–466**, frame **0**. The source edge is 0.001190418797 m. Its actual vertices blend RightScapula / RightHumerus (for vertex 466, 0.731663048 / 0.268336952; vertex 456, 0.714041352 / 0.285958648). This is a reproducible deformation of the shared LBS construction, not a declaration that those weights encode the true attachment. Source triangle 914 is independently matched by exact normalized source coordinates and source connectivity.

Selected event vertices produced 540 unique exact float32 source-position matches, 411 duplicate-position ambiguities and zero unmatched records. Duplicate vertices are kept explicit; a source triangle can still be uniquely located by connectivity. These are source GLB indices, not undocumented upstream authoring IDs.

The report attributes actual triangle collapse to the participating shoulder/arm skin transforms and their numerical blend. It does **not** establish that a particular attachment is anatomically correct or that the original source mesh itself is defective. Exact source-coordinate matches preserve source identity; they do not validate the source asset's biological fidelity.

Stop short of a repair recommendation expressed as new numerical muscle origins. First obtain anatomical landmarks and evaluate attachment-aware segmented weights; then test reusable pose-space corrections against both clips and withheld poses. A rotation-preserving deformation model is a third option, subject to an explicit Blender→GLB→Three.js runtime contract. The current construction fails, but no evidence proves that source preservation and reusable motion are inherently incompatible.
