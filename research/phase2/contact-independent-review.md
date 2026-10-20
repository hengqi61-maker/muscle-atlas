# Independent contact-v1.1 review · 2026-10-18

Read-only review by the shoulder-analysis worker. Reviewed `contact_v11.py`, `contact_surface.py`, `scan_phase2_contacts.py`, `export_phase2_contacts.mjs`, `packet-v1.1.schema.json` and `test_contact_v11.py`. Did not edit implementation, run the 363-frame scan, modify assets or approve anatomy. This is a bounded algorithm/source audit, not an external security audit.

## Actual checks

Windows native CPython: `D:\codex\.muscle-atlas-biomechanics\Scripts\python.exe -m pytest tests/biomechanics/test_contact_v11.py -q`: **13 passed in 0.48s**.

Two additional read-only probes were actually executed:

1. `triangle_pair([[-1,-1,0],[1,-1,0],[0,1,0]], [[-.5,-.5,5e-9],[.5,-.5,5e-9],[0,.5,8e-9]], 1e-8)` returns **disjoint**. The second triangle projects inside the first and lies only 5–8nm above its plane, below tolerance. The near-parallel but nonparallel early-return path does not implement the declared tolerance contact band.
2. A migrated actual fixture with prop kind `actual-triangle-surface`, `frameStatus=provided`, and `wristWorldMatrix=[0]*16` is **accepted by run()** (one output row). The convex legacy path would reject that nonrigid wrist frame. Schema alone only verifies matrix length and numeric types.

## Findings

**P2 · Surface tolerance-band false separation.** The nonparallel branch returns disjoint when there is no exact edge/plane witness, even if the triangles lie within the declared tolerance. This does not prove a false-negative exact interpenetration, but contradicts tolerance-band semantics and can mislabel near contact as separation. Add the probe as a golden fixture; either implement a triangle-distance boundary band or return unknown for unresolved near-plane candidates. Do not claim exact clearance from that branch.

**P2 · Surface mode bypasses wrist/palm validation.** `contact_v11.validate()` validates prop/hand transforms but omits provided wrist/palm matrices and frameStatus consistency; only run_v10 supplies those checks, and surface mode bypasses it. Validate all provided reference matrices and missing-frame status before dispatch. This is an interface validation issue, not evidence that actual exporter data were wrong.

**P2 · Cache and final writes are not atomic/resumable under interruption.** Frame cache and summary use direct write_bytes; a cancelled process can leave truncated JSON. A later cache read raises rather than recomputes. Cache key includes contact source code but not schema bytes, manifest SHA or associated frame metadata. Hit occurs before packet time validation. Use same-directory temporary file plus atomic replace, tolerate invalid/incomplete cache as miss, include schema hashes and frame identity in cache validation. Do not certify cancellation/restart correctness from ordinary completed scans.

**P2 · Manifest identity is not fully bound to packet identity.** Full manifest verifies the 363 exercise/side/frame labels, hashes and file time, but does not verify exercise/side/frame metadata against each packet's variant/clip, actual side list and frame-derived time; cached entries bypass packet identity validation. An erroneously relabelled manifest can still satisfy the set-completeness check. Bind side/exercise/frame/time metadata to payload and cache; add corrupted-side/frame tests before claiming an adversarially robust complete timeline.

No P1 exact-surface-crossing defect was established in this bounded review. No inference is made from passing synthetic tests to every real triangle pair.

## Sound boundaries retained

- Nonconvex dumbbell geometry uses actual posed equipment triangles and reports surface-crossing separately; overall volume state remains unknown. It does not manufacture penetration depth or treat surface-disjoint as enclosed-volume clearance.
- Frozen exporter checks original vertex count and exact triangle index ordering; topology mismatches are excluded and recorded unknown. Matching indices/count alone does not prove each anatomical vertex correspondence or source selection completeness; source hashes and frozen producer make this auditable, not medically calibrated.
- Left/right exported source identity and actual per-side bone frames are independent. Curl hand frames and anatomical wrist/palm frames explicitly unknown; hand-local roundtrip is checked when available. This does not validate anatomical handedness from matrix determinants alone.
- Source-triangle hashing has an explicit binary format; input bytes are hash-identified separately. Validator checks posed hash, but originalMeshSha256 and asset/provenance labels remain producer assertions unless checked against trusted source bytes/registry. Never describe a shape-valid SHA as independently verified file identity.
- Existing v1 schema/kernel remain unchanged. Explicit v1-to-v1.1 migration marks unknown provenance and does not promote legacy evidence into actual contact. New enum/version acceptance is an explicit new contract, not a claim that old parsers consume v1.1.
- 121 samples per pair/exercise establish discrete sampling only; between-frame collision, enclosing-volume state, force, grip stability and anatomical wrist/finger correctness remain unproven.

## Release gates

Suitable now for a Draft PR: versioned research interface, frozen source export evidence, known-truth tests, actual discrete intersection observations with unknown/limitations retained. Not suitable for a universal grip PASS, runtime contact certification, continuous collision guarantee, cancellation-safe cache claim or unrestricted AI executor enabling. Findings above should be resolved or explicitly tracked before treating the scanner as a stable reusable acceptance gate.

Review findings were sent to the parent worker before publication so it can fix them and add tests. This report records the reviewed pre-fix behavior; subsequent fixes require an appended recheck, rather than rewriting historical observations as if no defect existed.
