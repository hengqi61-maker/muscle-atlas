# Motion pipeline phase one — authorized isolated experiment

Branch codex/rig-v2-motion-pipeline, base PR5 fcb27068232ed1204786fd901bb8c58aa575a686. Research document imported unchanged from PR7 commit4c52d01403104b6690d78a0b39675f9897f3cdda; historical text is retained, while this new task separately authorizes E3 engineering.

Priorities: M-A two clean CurlProbe builds and evidence generation; M-B real GLB triangle/weight/pose attribution of known shoulder/axilla/elbow failures; M-C same frozen skin/inverse-bind/identity across both diagnostic clips; M-D data requirements and Windows-owned contract coordination; M-E reproducible evidence/reviewer/owner gates. No formal finger movement, production replacement, whole-body weight repaint, new exercise or main merge.

Immutable source: anatomy.glb SHA2566e84529b60b64cc8f8d5cef665fda932e359e828b66d0c2dd44ec1bd9d0bd01f. R1 model SHA256ef803a4bbb3c644504c124519e39ba0b3b760ec139eaf60d277ef7f7f5d23274. Original review candidate58f5d6b and historical M2 failures/cycle cap unchanged.

Architecture: existing canonical reference matrices and attachment weights are build inputs, never re-inferred from current animation. Registry geometric proxies are not anatomical footprints. Reproducibility compares structure, exact source identities/base geometry, weights/inversebind and121sample numeric trajectories; any allowed float tolerance must be predeclared with units. Bytewise GLB identity is measured, not assumed across exporter timestamps/order.

BUILD_PASS and SOFTWARE_TEST_PASS cannot override MOTION_GEOMETRY_FAIL or INCONCLUSIVE. Independent biomechanics, visual, exercise science and software reviews require a fixed candidate SHA and identical asset hashes. Owner approval stays PENDING until the human explicitly decides. Known failures are deliverable evidence, not exceptions to silently waive.

If preservation/continuity/reuse conflict, stop related asset mutation and present anatomical landmark/weight calibration versus reusable pose-space corrections with evidence; do not choose wholesale source geometry edits or concealed tissue.
