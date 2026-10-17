# Independent R1 shoulder and attachment reference

Source is the official OpenSim-core 4.6 test model at commit `52094cc61c3e795552c658e34a73d083f4662c6b`, path `OpenSim/Tests/shared/ThoracoscapularShoulderModel.osim`, SHA256 `892bd333a1e1e6a2b77902b54218f12727eefd2306ca82bbda81621c926271fe`. OpenSim runtime reports 4.6 (2026-03-31). Model acquisition, attribution and Apache-2.0 repository-level license caveats remain in model-assessment.md; no model geometry is redistributed here.

Machine-readable definitions and numeric rank results: `research/opensim/results/shoulder-reference.json`. Original joint XML preserves offset-frame parent sockets, translation, orientation, custom transform axes/functions, coordinate bounds, and specialized scapulothoracic definitions without silently recoding them as Mac Euler axes. This is source-model evidence; joint offsets are model reference centers, not measured landmarks of the Muscle Atlas mesh.

| Claim | Evidence class | Scope |
|---|---|---|
| Thorax→clavicle is a 2-coordinate CustomJoint | actual model | sternoclavicular offsets/axes/functions retained verbatim |
| Thorax→scapula uses ScapulothoracicJoint with 4 coordinates | actual model | not a generic clavicle-child rigid hinge |
| Scapula→humerus is a 3-coordinate CustomJoint | actual model | plane/elevation/axial coordinate definitions are model-specific |
| Clavicle/scapula AC points coincide | actual model constraint | full local point locations retained in output |
| 17 coordinates, 5 locked, 12 unlocked | actual API state | locked ground translations, elbow flexion and pro_sup |
| AC residual Jacobian rank 3, local tangent dimension 9 | script calculation | assembled default, central differences 1e-5/1e-6/1e-7; rank tolerance 1e-8 |
| Prescribed GH/scapular sweep poses | manual experiment assumption | not captured pulldown, not recommended trajectory |
| Source-mesh cuff origin/insertion calibrated | currently unknown | no such calibration delivered |

Rank is local and includes three free thorax rotations. It is not 17 independent freedoms, nor a global proof that nine coordinates can be prescribed independently. Coordinate ranges and clamped flags are software definitions, not universal human normal ranges. Assembly can move commanded coordinates to satisfy the AC constraint; command/actual values are retained in W3 outputs.

Rotator cuff references include Supraspinatus A/P, Infraspinatus S/I, Subscapularis S/M/I, and TeresMinor. Each path point includes its exact original parent frame and definition. First/last path endpoints are identified separately from intermediate points. These supply candidate proximal/distal references in their original bone frames; intermediate/wrapping points must not be mistaken for origins/insertions. No one-to-one mapping of these aggregated model bundles onto Muscle Atlas 467 individual source meshes has been established. Model has only one upper limb, no independent left validation, a welded wrist, separate ulna/radius, and no articulated fingers.

Mac R1 has bilateral Clavicle/Scapula/Humerus/Forearm/Wrist/Hand/FingerSocket nodes in a 27-node full-body hierarchy. OpenSim thorax→scapula plus AC closure differs from Mac's authored parent chain; OpenSim ulna/radius cannot be silently collapsed into Forearm while preserving pronation. FingerSocket is not a finger chain. The published right-side four-frame diagnostic mapping remains uncalibrated: no anatomical shoulder-center or rest-axis equality is claimed. Different Euler angles alone cannot reject a Mac action.

Literature context (LITERATURE_SUPPORTED): Seth, Dong, Matias & Delp (2019), [Methods: Model of the Human Shoulder](https://pmc.ncbi.nlm.nih.gov/articles/PMC6856649/), explains scapulothoracic modeling and aggregated muscle paths with wrapping geometry. It supports model design context, not patient-specific attachment accuracy or resisted pulldown truth. Full text retrieved 2026-10-17; article CC BY, separate from model/source asset licensing. Reopening the 2016 PMC paper returned a browser challenge in this run; no new unverified claim is derived from that retrieval.

Next useful calibration is a shared anatomical landmark definition and reference pose for thorax, scapula and humeral head, with measured uncertainty. Muscle path length is not muscle force; force requires dynamics/loading and model assumptions; activation estimates require an estimation method. EMG is a separately measured electrical signal, not synonymous with predicted activation.

```powershell
& C:\ProgramData\Anaconda3\Scripts\conda.exe run -p D:\codex\.muscle-atlas-opensim python scripts/biomechanics/shoulder_reference.py D:\codex\muscle-atlas-opensim\artifacts\opensim-models\ThoracoscapularShoulderModel.osim research/opensim/results/shoulder-reference.json
```
