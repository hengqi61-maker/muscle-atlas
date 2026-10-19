# Mac E3 / Windows IK interface readiness

Read-only contract inspection: Windows `ff7fc70` on `codex/opensim-biomechanics`. This report neither changes Windows schema nor merges Windows code into the Mac branch. Windows owns schema maintenance. Historical M2 and R1 failures remain open to owner review.

## Existing numerical exchange

`docs/biomechanics/exchange-v1.md`, `schemas/kinematics/packet-v1.schema.json` and the semantic validator define metre / second, right-handed active rigid matrices, column-major 16-element storage, column vectors. Local/world composition is explicit. Mapping is `T_target = A * U_s(T_source) * B`, with per-frame reference offsets and positive translation-only unit conversion. Axis labels and numerical zero alignment do not establish anatomical axes or calibration.

Mac already publishes genuine native and glTF reference/clip packets in `docs/rig-v2/handoff/v1/`; default, inverse-bind and animation-time0 remain separate. Windows `research/opensim/mac-r1/import-report.json` records 121 numerical frames per clip checked, five exported phases and 27 joints, input SHA256 `cf27f3ff63c5dd73fef0d5ae29657bf296879cd02531f4494ac0d5f173bf117c`, asset SHA256 `ef803a4bbb3c644504c124519e39ba0b3b760ec139eaf60d277ef7f7f5d23274`. Those are Windows-published receipt results, not a new local rerun or anatomy approval.

The complete tree at `ff7fc70` contains **no dedicated prop/contact schema or contact contract**. The existing generic kinematics schema cannot alone certify source-triangle gripping, wrist limits or finger clearance. Consequently an IK contact adapter is **INCONCLUSIVE / pending Windows contract**, not silently implemented against a private incompatible schema. No mock contact samples were created. Existing `measure-source-contacts.mjs` is measurement code, not an agreed exchange schema.

## Requested Windows contact contract fields

| Data | Mac production export / required definition | Verification need |
|---|---|---|
| Provenance | asset/source GLB SHA256, producer commit, sourceName, FMA/BP IDs, topology hash | Windows rejects stale topology and missing real triangle identity |
| Global coordinates | metre/second, right handed, explicit world axes, column-major matrices and time origin | no hidden display scale or implicit reflection |
| Hand frames | left/right wrist, hand local/world reference and sampled matrices; frame ownership | wrist frame differs from anatomical palm plane |
| Palm / thumb | actual source surface landmark indices, derived palm normal / thumb vector, evidence status | landmark availability and uncertainty; no invented calibrated vectors |
| Mirroring | side, independently measured vs mirrored, explicit proper rigid transform or separate geometric reflection step | reflected det -1 matrix cannot masquerade as joint rotation |
| Prop frames | bar and upgraded dumbbell geometry hash, grip-cylinder axes/radius/length, local/world poses | primitive grip proxy is explicitly separate from full actual mesh |
| IK targets | target frame and tolerance in metres/radians, solver iteration/convergence residual | virtual target coincidence alone cannot close grip P1 |
| Source triangles | mesh ID, triangle vertex indices, base and posed positions, actual skinning inputs | compute true segment/triangle or triangle/triangle crossing and signed surface clearance |
| Timeline | exact sample times, interpolation, clip duration, paused/seek states, shared prop clock | complete cycle, not start/end only |
| Contact benchmark | original left/right hands versus bar/dumbbell, known separated/intersecting/tangent fixtures | report units, tolerance, numerical boundary convention and false-negative limits |
| Capability | original fingers unmodified; non-destructive bone sockets only | no genuine finger closure PASS while original adductor tissue crosses grip |

Please publish versioned schema, validator and golden geometric fixtures on Windows branch, with schema hash, code SHA, licence/provenance and expected numeric classifications. Mac will consume read-only, request any changes upstream, then run against actual posed source triangles. No formal source-finger pose change is authorized. A proposed future finger rig requiring original finger motion must go to the owner before integration.

## Structural reuse result

`node scripts/quality/rig-reuse.mjs` writes `reuse-report.json`. Frozen R1 has exactly one skin, 27 joints and 467 unique sourceName mappings. Both clips reference the same joint palette and hierarchy; each has 81 identical node/path targets. All primitive positions, joints, weights, indices and inverse-bind accessor contents are SHA256 recorded. They are one immutable set of buffers, not separately rebound assets per action. No per-clip reweighting is encoded. There are no morph targets or morph animation channels; corrective independence is therefore **absent**, not demonstrated as functioning. This establishes structural reuse only. Existing severe surface deformation, source integrity proof and hand contacts require their own checks.

Reproduce:

```sh
node scripts/quality/rig-reuse.mjs
node --test tests/rig-v2/reuse.node.mjs
git ls-tree -r --name-only ff7fc70
git show ff7fc70:docs/biomechanics/exchange-v1.md
git show ff7fc70:research/opensim/mac-r1/import-report.json
```

Real local result: structural AUTO PASS; four tests PASS (real asset, alternate-skin/non-joint target rejection, duplicate source identity/morph/missing-clip rejection, explicit sparse-accessor rejection). This does not close R1 shoulder/axilla/elbow P1, true gripping, or OWNER_APPROVAL. No asset was edited, and no workaround or test threshold relaxation was introduced.

## Final delivery refresh: Windows fd1701f
The newer Windows commitfd1701fc87ab00787056cb24f4e398d1f04c26c7 now publishes W1/W3 reports and an actual7-node/10prescribed-pose OpenSim packet. Mac read the published packet and reran the existing numerical schema/semantic validator:0issues. This is a data-contract recheck, not a MacOpenSimrun or anatomical calibration. There is still no dedicated contact schema in this revision.

Transport provenance distinction: published GitLF packetSHA242fa6bd38b754e74de1acc32bbcd9fb9949080e9eaeb57d2115ffe6b153c9c5 differs from validation.json exportSHA62e1f48249d78ad4811a2a8b83e420e0e38d3e21c11e9c01b89e73106124c0a8. Exact LF→CRLF reproduction yields the latter; no numeric content difference is inferred. Mac preserves published bytes and records both identities, requesting upstream label clarification rather than rewriting Windows results or silently normalizing. See results/windows-receipt.json.
