# Phase 2 contact-v1.1 discrete scan — 2026-10-19

Independent source-triangle scan; no GLB, finger pose, weight or production runtime was changed. This is engineering geometry evidence, not anatomical or medical certification.

The exporter freezes source commit `0914d4fad3fbe107ea90c08473b6d2a448345ba6` and producer `c1d7e209901390bfb73f784e0f1f48c8337f2e17`. See `research/phase2/contact/input-manifest.json` for asset SHA256, original asset identity and each compressed/payload byte hash. `scan-compact.json` contains code/schema hashes, 90 exercise/source/side aggregates and source-triangle witnesses. Local full summary SHA256: `ca51c29938a292b492a7e80b63be02dcc76c5cd454713021f77edc27340f2d7c` (12,233,085 bytes). Generated meshes are retained locally under ignored artifacts, not committed.

Completed 363/363 input packets: 121 times for each pulldown hand and 121 curl packets containing both hands, from 0 to 4 seconds inclusive. This is complete discrete coverage, not continuous collision clearance. Across these triangle/time observations: 10,237,443 separating observations; 1,728,606 convex-prop interior penetration candidates; 18,275 actual dumbbell surface crossings. These are triangle/time counts, not people, unique defects or independent clinical measurements.

Pulldown adductor pollicis oblique-head maximum interior witness lower bound: left/right 0.0109158803 m. Transverse-head: left 0.0228080236 m, right 0.0228079362 m. These bounds are relative to exported finite convex grip geometry, not exact global penetration depth or tissue compression. Both sides retain original triangle identities. Palm/IK agreement does not negate these observations.

Curl adductor pollicis surface-crossing observations: left oblique 264 and transverse 1464; right oblique/transverse zero. A zero crossing count does not prove the hand clear or a successful grasp: nonconvex containment, closed volume and anatomical coverage remain unproven. Nonconvex actual-surface results keep final volume state UNKNOWN.

22 exercise/source rows have unproven original indexed topology and are explicitly excluded/UNKNOWN. Measured anatomical wrist/palm axes, skin and finger-bone coverage are unavailable. Reference frames are engineering export frames. No claim of Mac 27-joint anatomical alignment is made.

## Reproduction

Use the existing biomechanics Python environment (numpy/jsonschema/pytest), preserve existing lockfiles:

```powershell
node scripts/biomechanics/export_phase2_contacts.mjs artifacts/phase2/contact-frames-new
python -B scripts/biomechanics/scan_phase2_contacts.py artifacts/phase2/contact-frames artifacts/phase2/scan
python -B -m pytest -q tests/biomechanics --basetemp=artifacts/phase2/pytest-final-20261019
```

The exporter reads frozen Git assets and writes only its explicit output directory. Use a fresh output directory and the recorded producer checkout to reproduce original provenance; a different checkout records a different producerCommit. Do not overwrite the retained evidence directory or original assets. The scanner validates all gzip/payload hashes and frame identities before accepting cache hits, whose keys include code/schema/manifest identity. Final native Python suite: 66 passed in 1.94s. Actual shoulder OpenSim runs and simulated synthetic geometry tests are separate evidence.

2026-10-20: migration now emits null unknown original IDs; actual-source declarations require verified IDs. Mixed convex/surface timelines are explicitly rejected. Independent review confirmed both fixes and default/bind naming correction. Mac anatomical frame calibration remains pending. Version 1.0 schema/kernel remain unchanged. This report does not mark the full Phase 2 deliverable or motion quality accepted.

Historical363-packet scan uses exact7files in research/phase2/contact/executed; all SHA match scan-compact.codeHashes. Current code/schema differ after null migration and routing repairs. Actual24,040-result right frame0 replay before/after null repair was exactly equal; migration-actual-replay.json identifies that specific pre-routing-fix hash. No new full363 scan is claimed.
