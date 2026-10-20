# M3-B technical decision (Cursor TL)

Stamp: 2026-10-20T03:45:00Z  
Coordinator: Mac Cursor (Technical Lead)  
**Authorized next work:** one read-only BP4795 correspondence diagnostic (`D1`).  
**Not authorized:** another weight or axis GLB candidate, production edits, threshold changes, Draft merges, MCP/Skills mutation.

## Independent review of the three deliveries

| Side | Head | What was actually shown | What was not shown |
|---|---|---|---|
| Mac PR #12 | `13ddb46f27c5ffef003b54fb6f128b83cfc2127e` | E01/E02 rejected; E03 published as **rejected continuity control**; full 121×2 triangle scan; independent software / bio / visual reviews | Anatomical attachment; motion PASS; MCP-owned anatomy inspect (lock rejected) |
| Windows PR #16 | `a8247a4ff121c94b038ceccb77f729d30a85073c` | W-F4 engineering axes from serialized GLB; OpenSim 4.6 14-pose rerun; contact-v1.1 + 363-packet **frozen M2** scan; explicit structural mismatch | Measured landmarks; PR12-candidate mesh contact; clinical axes; permission to edit Mac weights |
| Cursor PR #17 | `c6f04a12d48334a51c34b8adaab738a1989ff408` | M3-A FAIL freeze + H1–H8 matrix + Skills/MCP boundary | Did not yet see published E03 or PR #16 (this decision supersedes the “wait then maybe E03” rule) |

Frozen experimental R1 SHA256 remains `ef803a4bbb3c644504c124519e39ba0b3b760ec139eaf60d277ef7f7f5d23274`.  
E03 candidate SHA256 `3deb0d355587950ff212448bff5ef9d92b06f0ed7c5560a173271ac116a35734`.  
E03 evidence zip SHA256 `c0fc2d6d510c7e25e9ca0af5b01bbc10d86ba7fe81f4dac2ef234743b0be9cbf`.

### Verified engineering facts

1. Baseline motion FAIL is unchanged: Curl **39/121**, Pulldown **91/121**, peak edge **3.988438** at right subscapularis BP4795/FMA13414 △914 edge 456–466, Pulldown frame 0.
2. E01 λ=0.5 neighborhood smooth **worsens** peak to **6.469800** and splits originally identical export verts 441/1288 by **3.179553 mm** under the same RightScapula/RightHumerus matrices (weights 0.662202/0.646820 vs 0.337798/0.353180).
3. E03 keeps that operator and adds only equivalence-class projection: 22 selected / 21 classes / 43 rows; **246 WEIGHTS bytes only**; two builds byte-identical; 1785 alias pairs ×121×2 separate **0 m**.
4. E03 does **not** repair original stretch: counts stay 39/91; peak stays **6.469800** now at △953 edge 480–483 (rest 0.361160 mm → 2.336636 mm); △914 remains **3.989352** vs baseline **3.988438**. New/removed severe mesh-poses **0/0**.
5. E02 axis edit is a different family: angle preserved, wrist path moves 24.767 / 21.699 mm, Pulldown 91→93. Rejected.
6. Windows computed Mac default/track engineering axes and OpenSim relative matrices. Forearm principal axes at max basis rotation are published **as engineering frames**. Windows states they must not be copied as clinical axes.
7. Mac Clavicle→Scapula→Humerus plus one Forearm **≠** OpenSim thorax→clavicle / thorax→scapula + AC + ulna/radius. OpenSim is right-only, hand welded, no fingers. Constraint residual 7.02e-17 m proves **model closure**, not anatomy.
8. Contact 363/363 packets are frozen M2 source `0914d4f` / producer `c1d7e20`, **not** PR #12 candidate meshes. 22 topologies UNKNOWN. Contact ≠ motion PASS.
9. Default-world × inverse-bind max matrix residual 1.194e-6 is dimensionless rotation residual at LeftThigh, **not** 1.19 µm translation. Do not invent a gate from it.

### Unconfirmed anatomical hypotheses

- True subscapularis glenoid / lesser-tubercle insertion (H4).
- That △914 or △953 is an attachment landmark rather than a short rest edge under two-bone LBS.
- That scapula/humerus local axes (H5) are the dominant cause of axillary FAIL.
- Any OpenSim path point as a label on 467 source meshes.
- That another λ / ring / smooth on BP4795 will fix stretch after E01/E03 already moved the peak.

## W-F4 gate

**Met as INCONCLUSIVE, not as calibration.**

PR #16 supplies the comparable-axis packet **and** the explicit statement that OpenSim cannot uniquely determine scapulohumeral rhythm or subscapularis insertion. That satisfies the M3-A dual-end gate.

It does **not** unlock an H5 mutation. The only mutation the INCONCLUSIVE path previously allowed was H2 equivalence projection — **E03 already ran and failed as a motion repair.**

## Decision (one experiment)

| Option | Verdict |
|---|---|
| Another BP4795 weight smooth / λ / ring (H1 rerun) | **Rejected** — unsourced tuning; E01/E03 already show neighborhood operators move the peak and leave 39/91 |
| Another H2 projection variant | **Rejected** — alias split is already 0 m; original FAIL remains |
| H5 scapula/humerus axis write | **Rejected** — axes are engineering/model-provided; E02 showed this class moves paths |
| H7 corrective morph | **Forbidden** |
| **D1 read-only BP4795 source/export/weight map + 121-frame LBS attribution** | **Authorized** — evaluates H4/H1 mapping without assuming root cause; is the missing correspondence Windows asked for on this mesh |

D1 writes **no** POSITION / WEIGHTS / animation / bind bytes. It is a packet, not a candidate GLB.

If D1 later isolates one pre-registerable numeric mechanism (for example “these two export rows of a 0.36 mm rest edge carry a two-bone weight split that algebraically yields the 6.47 ratio”), M3-C may name **one** mutation. That is not authorized here.

## D1 specification

See `docs/handoff/m3b-experiment-spec.json`.

**Inputs (immutable)**

| Asset | SHA-256 |
|---|---|
| Frozen R1 / baseline GLB | `ef803a4bbb3c644504c124519e39ba0b3b760ec139eaf60d277ef7f7f5d23274` |
| Rejected E01 | `f7324b003425ae08310ba00e20f303b59734287121eca539ce79dc66edc8b6c1` |
| Rejected E03 | `3deb0d355587950ff212448bff5ef9d92b06f0ed7c5560a173271ac116a35734` |
| Mac code head | `13ddb46f27c5ffef003b54fb6f128b83cfc2127e` |
| Windows evidence head | `a8247a4ff121c94b038ceccb77f729d30a85073c` |

**Single variable:** export scope = **right subscapularis / BP4795 / FMA13414 only** (2092 triangles). No other mesh, no weight edit.

**Required outputs (project-local artifacts + committed manifest/hashes)**

1. Alias classes: original exact same-mesh POSITION+JOINTS_0+WEIGHTS_0 groups; export indices vs source identity; do not weld geometry.
2. Rest + posed world triangles, all **121 samples × CurlProbe + PulldownProbe**, original triangle IDs.
3. Per-vertex WEIGHTS_0 / JOINTS_0 / bone names for vertices of △914 and △953 (and their alias members).
4. Independent recomputation of Pulldown frame-0 edge ratios for △914 (456–466) and △953 (480–483) on all three input SHAs.
5. Packet SHA256 + producer commit + unit/frame convention. Unknown landmarks stay **null**.

**Expected numeric replay (must match published reports or D1 FAIL)**

| SHA | Pulldown f0 △914 edge456–466 | Pulldown f0 △953 edge480–483 | Alias 441/1288 split |
|---|---:|---:|---:|
| baseline `ef803a4b…` | 3.9884383355 | (record actual) | 0 |
| E01 `f7324b00…` | (record; E01 peak was 6.469800 on 914 in E01 isolation) | (record) | 3.179553092 mm |
| E03 `3deb0d35…` | 3.9893524980 | 6.4698000415 | 0 |

**121-frame validation (unchanged gates)**

- Re-run existing `analyze.mjs` on the **same three immutable GLBs** (expect 39/91, E03 MOTION_GEOMETRY_FAIL). This confirms D1 did not mutate inputs.
- `seam-check` / alias LBS: E01 FAIL, baseline+E03 0 m.
- Do **not** treat D1 packet completeness as motion PASS.

**Stop rules**

1. Any byte change in the three input GLBs → abort, restore, report.
2. Recomputed ratios disagree with the table beyond float32 replay → exporter FAIL; no mutation follow-on.
3. Do not expand D1 to all 467 meshes in the same candidate. A later **Windows-consume export** of all meshes is a separate task after D1 replay PASS.
4. Do not start λ/axis writes from visual inspection of the packet.
5. Owner / motion quality remain FAIL / PENDING.

**Review split**

| Role | Charge |
|---|---|
| Mac Codex | Implement D1 exporter in isolated worktree; produce packets + hashes; no production paths |
| Windows Codex | Read-only consume BP4795 packet; do not relabel triangles as attachments; do not scan as if these were M2 source IDs |
| Software reviewer | Independent: input SHA unchanged; triangle 914/953 index+vert identity; replay two edges; alias map closure |
| Biomechanics reviewer | Confirm still INCONCLUSIVE for insertion; no clinical axis claim |
| Visual reviewer | Not required for D1 (no new candidate). Optional: existing E03 stills only |
| Cursor TL | Accept D1 only as correspondence evidence; name M3-C mutation only if a single algebraic variable is pre-registered |
| Owner | No approval implied |

## Missing evidence (assigned, not guessed)

| Gap | Owner | Why it blocks mutation |
|---|---|---|
| Calibrated scapular/humeral attachment regions on **source** anatomy | Windows + Mac jointly, later | H4 still INCONCLUSIVE after PR #16 |
| Common landmark / joint-center registration for exchange A/B | Windows | Stated prerequisite before mapping OpenSim path points |
| PR12-candidate posed triangles for **all 467** meshes | Mac, after D1 | PR #16 contact is M2, not these candidates |
| Measured (not model-provided) scapula/humerus axes | Windows | H5 remains INCONCLUSIVE |
| Guarded MCP ownership handoff | Coordinator | PR #15 inspect pending; not needed for D1 |

## Tooling

PR #14 / #15 stay Draft and observation/fixture-only. D1 must be a pinned CLI script, not an MCP `execute_code` session.
