# R0/R1 milestone: isolated unified rig and Mac–Windows exchange

Status: research prototype delivered; NOT product accepted. Formal animation replacement is blocked pending Owner approval and unresolved deformation. M2 failure reports and its two-cycle limit remain unchanged.

## Fixed versions
- Base0914d4fad3fbe107ea90c08473b6d2a448345ba6 (M2PR3).
- Reviewed R1 candidate58f5d6b65e07eba476843b76ac45cca36e3089f4. Subsequent commits add exchange adapters/data and review documentation, not new mesh/rig/animation.
- GLB SHA256 ef803a4bbb3c644504c124519e39ba0b3b760ec139eaf60d277ef7f7f5d23274.
- Mac published exchange b62b286d4b3ec575d3aa813d1fddc07b30510371; Windows contract pinned c12e30eed644e797206fe1296010b252c9325de3.
- MacDraftPR5; WindowsDraftPR6. No main merge or changes to peer assets.

## Actual completed work
R0 compared source, curl and pulldown skeletons/weights/transforms and migration paths. R1 builds one27joint skeleton/skin shared by467original anatomical mesh nodes, two embedded diagnostic clips and isolated Three.js viewer. Fresh Blender source comparison finds467/467exact float32 canonical base coordinates and unchanged polygon ordering. Native source scene and actual renders/recordings are evidence artifacts, not formal replacement. Original hands remain unchanged and open; digit interfaces are only reserved nodes.

Windows-owned v1 contract is used directly from its independent checkout. Seven real27node packets separately preserve native rest, glTF default/bind and both diagnostics; v0.1 retains121samples per clip, while native/v1 comparisons use five phases. Per-bone numeric A/B alignment, units/handedness and root-ancestor transform handling are explicit. Actual inverse-mapped glTF pose was written to bpy, saved, reopened and read. Source blend hash unchanged. No human motion capture, anatomical calibration or OpenSim equivalence claimed.

## Actual checks
- npm build PASS; Vitest13PASS; existing quality test26PASS.
- R1 handoff/quality Node tests8PASS; Mac exchange3PASS; Windows contract22PASS.
- RealChrome complete suite7PASS in52.9s, including original anatomy/pulldown and isolatedR1; actual frames/videos archived.
- Khronos GLB Validator0errors/0warnings; one informational empty node at/nodes/37.
- Numeric exchange max native/glTF matrix element error6.998322887863395e-7; actual Blender write/save/reopen/read2.384185791015625e-7; predeclared tolerance2e-5. These element errors are not anatomical angle/clinical tolerances.
- Geometry quality audit correctly AUTOFAILS PulldownProbe:42/121poses trip unchanged M2 severe area-count alarm, maxstretch3.988438x. Nearzero numerical threshold passing does not override the5%area alarm.

## Independent review and unresolved issues
Four independent review roles are recorded under reviews/58f5d6b. Reports are coordinator transcriptions of separate read-only Agent returns, not producer self-approval.
- P1 shoulder/cuff/axillary deformation: actual collapse/stretch and poor shoulder-arm continuity.
- P1 elbow compression/folds during curl.
- P1 anatomical attachment locations and shoulder joint coordination uncalibrated; global decile masks do not prove origin/insertion.
- P1 actual grip, seated equipment contacts and machine linkage unvalidated in this standing no-equipment diagnostic. Old M2 failures are not closed.
- P2 registry method metadata does not match cuff X-quantile algorithm; retained as known issue, no hidden asset rebuild.
- P2 full-body frames insufficient for deep-tissue/hand closeup acceptance; collision checks cover only four selected pairs/five poses, not whole-body collision clearance.
- Documentation-only hand authorization inconsistency corrected after review; original ES05 preserved.

## Debt and next owner gate
Primary exchange goal completed with real GitHub data and executable adapters. No retained workaround introduced by the exchange. V2 temporary disabled culling WD0017 permanently removed using validated posed bounds; float precision verifier WD0018 permanently corrected by exact float32 conversion model. Ledger checker reports0OPEN. Existing MODEL-RIG, grip/anatomical calibration and historical download/other deferred entries remain deferred; no new ACCEPTED_RISK.

Durable paths for deformation: calibrate attachment/shoulder landmarks with independent references, redistribute shared weights and evaluate reusable clip-independent corrections; avoid more one-action patches. Windows should first assess reference frames/model applicability and independent landmarks. No formal replacement, finger animation integration or face-pull starts without Owner decision. This report does not grant approval.
