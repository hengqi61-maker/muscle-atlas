# Blender MCP Integration (Codex / Mac)

Status: optional interactive observation tool. Does **not** replace the deterministic pipeline:

`Blender CLI → GLB → Three.js → geometry tests → multi-view review → Owner acceptance`.

## Versions (this Mac install)

| Component | Value |
| --- | --- |
| macOS | 27.0.1 (Build 26A434), arm64 |
| Blender | 5.2.0 LTS (`/Applications/Blender.app`), build 2026-07-14 |
| Codex CLI | 0.163.0 |
| uv / uvx | 0.13.1 (Homebrew) |
| mcp-for-blender | **2.2.0** (pinned; not latest) |
| Wheel SHA-256 | `160eb5e075b3933ed70d2de58445e27e08db0d5cc589f8f122d6027998ab9ce1` |
| Addon `blender_mcp.py` SHA-256 | `b4c17eb88e0d4ec2a1cb5ce40b695cef5b9360116ae1707a0cac80fc2f065865` |
| Addon `bl_info.version` | `(1, 8)` / protocol 13 |
| Experimental R1 GLB copy SHA-256 | `ef803a4bbb3c644504c124519e39ba0b3b760ec139eaf60d277ef7f7f5d23274` |

Upstream source: [ahujasid/mcp-for-blender](https://github.com/ahujasid/mcp-for-blender). Install used `uv`/`uvx` isolation; no `curl | sh`.

## Permission boundary

1. Blender MCP listens on **127.0.0.1:9876** only.
2. Upstream Safe Mode stays on (`BLENDER_MCP_SAFE_MODE=1`). Safe Mode is an AST gate on `execute_code`, **not** an OS sandbox; a local socket client that can talk to Blender can still run Python that passes that gate.
3. Telemetry and update checks disabled (`DISABLE_TELEMETRY=true`, `BLENDER_MCP_DISABLE_TELEMETRY=1`, `BLENDERMCP_NO_UPDATE_CHECK=1`).
4. Cloud / paid 3D generation tools are not exposed through the guarded Codex endpoint.
5. Codex and Cursor must not share one live Blender MCP instance (guarded client takes an exclusive `client.lock`).
6. Existing Codex MCP `blender_agent` is **kept**; this integration registers a separate server named `blender`.
7. Formal R1 production assets, weights, and animations are never written by this workflow. Tests use an experimental GLB **copy** only.

### Guarded local policy (required)

Raw `uvx --from mcp-for-blender==2.2.0 mcp-for-blender` is too open for this repo: it can execute arbitrary Safe-Mode-passing Python and still talk to Poly Haven / Meshy style surfaces in the upstream addon.

Muscle Atlas uses a local wrapper:

- `scripts/blender-mcp/guard.py` — token auth + command allowlist + exact SHA registry for scripts
- `scripts/blender-mcp/bootstrap.py` — enables addon in an isolated `BLENDER_USER_*` tree, patches the socket handler, starts 127.0.0.1 server
- `scripts/blender-mcp/server.py` — Codex stdio MCP that only offers scene/object/screenshot + approved scripts
- `scripts/blender-mcp/reviewed-scripts/` — the only `execute_code` payloads accepted

Runtime policy/token stay on the machine under `~/.codex/tools/mcp-for-blender/` and are **not** committed.

## Install / uninstall (operator)

### One-time package + addon

```bash
uvx --from mcp-for-blender==2.2.0 mcp-for-blender install-addon
# or use the audited wheel already cached under ~/.codex/tools/mcp-for-blender/
```

Confirm Blender Preferences → Add-ons lists **MCP for Blender** `(1, 8)` in the isolated user-scripts tree used by the launcher.

### Start disposable Blender (do not attach to an open production scene)

Use a double-fork / `PPID=1` launch so IDE shells do not reap the GUI process. Example shape:

```bash
# sets BLENDER_USER_CONFIG / BLENDER_USER_SCRIPTS / BLENDER_MCP_LOCAL_POLICY
# then: Blender --factory-startup --python bootstrap.py
```

### Register Codex MCP (keep `blender_agent`)

Equivalent registered config (absolute Python from the pinned venv):

```toml
[mcp_servers.blender]
command = "~/.codex/tools/mcp-for-blender/bootstrap/bin/python"
args = ["~/.codex/tools/mcp-for-blender/guarded-client/server.py"]
env = {
  BLENDER_HOST = "127.0.0.1",
  BLENDER_PORT = "9876",
  BLENDER_MCP_SAFE_MODE = "1",
  DISABLE_TELEMETRY = "true",
  BLENDER_MCP_DISABLE_TELEMETRY = "1",
  BLENDERMCP_NO_UPDATE_CHECK = "1",
  BLENDER_MCP_LOCAL_POLICY = "~/.codex/tools/mcp-for-blender/runtime/policy.json",
}
```

CLI used:

```bash
codex mcp add blender --env ... -- <venv-python> <guarded-client/server.py>
codex mcp list   # must show blender + blender_agent
```

`codex mcp list` proving registration is **not** the same as Blender connected. A live listener on `127.0.0.1:9876` is required before tools return scene data. New Codex sessions may be required to discover tools.

### Uninstall / rollback

```bash
codex mcp remove blender          # leaves blender_agent intact
# restore ~/.codex/config.toml from ~/.codex/config.toml.bak-blender-mcp-20261019 if needed
pkill -f '/Applications/Blender.app/Contents/MacOS/Blender'   # only the disposable MCP instance
# disable/remove isolated addon under the dedicated BLENDER_USER_SCRIPTS tree
```

Do not delete the user's normal Blender preferences; this integration uses a dedicated `BLENDER_USER_CONFIG`.

## Connectivity test (executed)

Evidence: `docs/dev/evidence/blender-mcp/connectivity-log.json`.

| Step | Result |
| --- | --- |
| `ping` | `pong: true` |
| `get_scene_info` | factory scene objects listed |
| approved `01_create_test_cube` | `MCP_TEST_CUBE` created |
| approved `02_move_and_material` | location `(1.5, -0.5, 2.0)`, material `MCP_TEST_MAT` |
| `get_object_info` | mesh 8/12/6; materials `["MCP_TEST_MAT"]` |
| `get_viewport_screenshot` | PNG written (offscreen); see screenshot manifest |
| approved `03_save_test_blend` | `mcp-connectivity-test.blend` SHA `665417d278dd7ebd39522421e8ce345c87269f1e4823867f976b53d34bffcf04` |
| reopen blend + query | `MCP_TEST_CUBE` restored with same location/material (**PASS**) |
| unregistered `execute_code` | denied by guard (`Script not in reviewed SHA registry`) |

## Muscle Atlas experimental copy (executed)

Evidence: `docs/dev/evidence/blender-mcp/atlas-inspect-log.json` + screenshots.

Constraints honored: experimental GLB copy only; no writes to formal R1 skeleton/weights.

| Check | Result |
| --- | --- |
| Import | ~470 objects; armature `MuscleAtlasV2Rig` |
| Hierarchy | 27 bones (Pelvis → limbs / scapula / humerus …) |
| `sourceName` | present on muscle meshes (name == sourceName in this GLB) |
| Actions / NLA | `CurlProbe`, `PulldownProbe` (frames 1–97) on the armature |
| BP4795 | **Not stored as a Blender custom property.** Mapped via `mesh_mapping.json` (`bpId: BP4795` → `right subscapularis`). MCP located the mesh by name/`sourceName`. |
| Face 914 | On `right subscapularis` (2092 polys): verts `[466, 456, 468]`, center local ≈ `(−0.0958, −0.0123, 1.1961)` |
| Weights | Vertex groups match rig bones; sample verts on right subscap weighted to `RightHumerus` |
| Screenshots | front/side/back/detail PNGs + hashes in `screenshot-manifest.json` |

### bpy CLI cross-check (numeric truth)

Independent Blender background import of the same experimental copy:

- import+query ≈ **2.35 s** in-process / **~4.0 s** wall
- `right subscapularis` present
- face 914 verts `[466, 468, 456]` — same triangle as MCP (index order only differs)

Treat MCP screenshots as observation aids, **not** numeric ground truth. Face indices and weights came from object data / reviewed scripts, not from pixels.

## MCP vs direct bpy

| Dimension | Guarded Blender MCP | Direct bpy / Blender CLI |
| --- | --- | --- |
| Steps for atlas inspect | Start disposable Blender → Codex/socket tools → approved scripts | One CLI invocation with explicit script |
| Cold import time | Import via MCP ~2–3 s once Blender is already up | ~2.4 s import + ~4 s wall including process start |
| Object/bone ID | Accurate names, counts, `sourceName`, NLA clip names | Same; easier to dump full JSON without allowlist friction |
| Local observation | Useful interactive screenshots + live `get_object_info` | Deterministic renders / measurements already in QA gates |
| Unexpected mutation risk | Reduced by SHA allowlist + experimental-copy-only scripts; still not a sandbox | Explicit script review in PR; production path unchanged |
| Reproducibility | Good for listed tools; camera framing via `get_viewport_screenshot` followed the **3D View matrix**, not the scene camera we set (multi-view hashes differ slightly but matrices matched — tooling limit) | High for CLI scripts and geometry gates |

### Recommendation

**Keep MCP as an optional interactive debugger** for Mac Codex sessions. Do **not** move production export, weighting, or acceptance onto MCP. Geometry gates and Owner review remain authoritative. If the SHA allowlist becomes a bottleneck without adding unique insight beyond CLI scripts, it is acceptable to leave the Codex server registered but unused in day-to-day production work.

## Issues found and mitigations

1. **Cursor/IDE reaps Blender children** → double-fork so Blender `PPID=1`.
2. **`--python` + bad keepalive signature** → timer callback takes no args on Blender 5.2.
3. **Blender 5 Action API** (`Action.fcurves` missing) → pose script updated for slots/NLA.
4. **Upstream default update/telemetry surfaces** → env disables + isolated user prefs + guarded Codex tools omit cloud APIs.
5. **BP4795 not on mesh datablock** → resolve via `mesh_mapping.json`, then MCP object name.
6. **Viewport screenshot ignores scene camera** → documented; use bpy render scripts when exact cameras matter.
7. **Safe Mode ≠ sandbox** → token + SHA registry + localhost + exclusive client lock; still trust the local user account.

## Optional workflow (additive)

```
Codex → Blender MCP (guarded) → interactive scene check
  → localize issue → author a reproducible bpy experiment
  → original quality gates (geometry / multi-view / Owner)
```

Production path unchanged.
