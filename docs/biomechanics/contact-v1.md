# E2 independent contact interface 1.0.0

This is a separate additive contract, not a change to exchange-v1. Existing seven Mac kinematics packets remain valid and retain their field meanings. Contact input schema: `schemas/contact/packet-v1.schema.json`; runnable fixture: `research/contact/example.contact.json`; expected output: `example.report.json` beside it.

All coordinates use right-handed metres, seconds, active proper rigid column-major transforms. Source vertices are actual posed world-space triangles, with stable source IDs, original topology and original-mesh geometry hash. Exporters must state their hash serialization. Prop vertices are local; its world matrix places them. Dimensions are descriptive; collision uses supplied triangles. Wrist/palm matrices are metadata, never geometric collision proxies. Missing calibrated frames are null with `frameStatus: unknown`, not invented identities. Side labels require producer provenance; a proper determinant alone does not prove anatomical laterality.

Each time sample supplies a prop ID/transform/dimensions, actual closed convex prop mesh, hands with skeleton/source IDs and variant at packet level. Prop must be convex, full-dimensional and closed after coincident-vertex welding; concave props must be split into separately identified convex pieces. Winding is normalized using interior centroid. Degenerate/nonmanifold geometry is rejected. Tolerance is explicit and bounded at 0.1 mm maximum; this is a numerical interface limit, not an anatomical allowance.

Algorithm clips each original triangle against all actual convex prop face planes, including finite caps. Broad-phase separation is mathematically conservative. A clipped witness strictly inside all planes yields `penetration-candidate`; boundary-only intersection yields `surface-contact`; no intersection yields `disjoint`. Every result retains original source ID, original triangle index, side, prop ID and real sample time. Witness position is returned in world coordinates. Depth is the minimum distance from an interior witness to prop support planes: a conservative lower bound on that witness's distance to the prop boundary, **not** the minimum translation needed to separate entire meshes. Disjoint gap is a separating-plane lower bound, not exact closest distance.

This detects surface intrusion, not force, tissue deformation, grasp stability or continuous-time clearance. A small prop completely enclosed in a closed hand volume can have no surface intersection. A discrete sample cannot clear the interval between samples. No contact report gives global grip PASS. PalmContact/IK error near zero cannot close a real source-mesh intersection.

```powershell
& D:\codex\.muscle-atlas-biomechanics\Scripts\python.exe -m pytest tests/biomechanics -q
& D:\codex\.muscle-atlas-biomechanics\Scripts\python.exe scripts/biomechanics/contact_packet.py research/contact/example.contact.json artifacts/example.report.json
node scripts/biomechanics/export_m2_contact.mjs artifacts/v2/m2
& D:\codex\.muscle-atlas-biomechanics\Scripts\python.exe scripts/biomechanics/contact_packet.py artifacts/v2/m2/left.contact.json artifacts/v2/m2/left.final.report.json
& D:\codex\.muscle-atlas-biomechanics\Scripts\python.exe scripts/biomechanics/contact_packet.py artifacts/v2/m2/right.contact.json artifacts/v2/m2/right.final.report.json
```

Use any Python environment matching the existing locked biomechanics dependencies; paths above record the actual Windows environment. No new physics engine is needed. Generated full M2 packets/reports stay ignored in artifacts; compact audit summaries and selected real triangle evidence are published. The adapter freezes M2 commit 0914d4f, verifies original source topology, reads production machine/config at that same commit, and constructs the exact Three.js 12-sided finite grip. Both source and equipment are measured before their shared presentation scale 1.45 and translation; this preserves intersection classification, while distances are model-root metres. It does not replace frozen assets or reports.

Mac can immediately export into this interface. Required follow-up: calibrated wrist/palm frames where available; actual original posed hand triangles; exact prop triangles including caps; stable source mesh ID/hash and topology; clip/time/variant/coordinate provenance. Missing frames must remain explicit. The test fixture's synthetic skeleton and identity frames are defined synthetic data, not anatomy.
