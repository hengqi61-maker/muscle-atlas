# Blender Skills / MCP project-level boundary (M3-A)

Read-only coordination note. Does not merge PR #14 or #15. Does not enlarge write permissions.

## What is in scope

| Surface | Draft | Head | Allowed use | Forbidden on Muscle Atlas anatomy |
|---|---|---|---|---|
| Pinned blender-skills (3 of 22) | PR #14 | `da9a947aa60f60329f8b6a62294d2f8462fa1aa9` | Isolated fixture QA / inventory | Heat bind, Rigify, merge/delete, generic GLTF_BASE export, production UV/medical claims |
| Guarded mcp-for-blender 2.2.0 | PR #15 | `7624e5b9df9ca50e88d2e52b49dbeece50cdd916` | localhost scene/object/screenshot + SHA-reviewed scripts on an **experimental copy** | Arbitrary `execute_code`, cloud/Meshy/Poly Haven, writing frozen R1/weights, treating screenshots as numeric truth |
| Existing `blender_agent` | user Codex config | unchanged | Separate stdio server | Sharing port 9876 with the guarded `blender` server or Cursor |
| Canonical pipeline | PR #8 / #12 | bpy CLI → GLB → Three → geometry gates → Owner | Authoritative quality | Replacement by Skills or MCP |

Upstream Skills pin: `EL4CTEO/blender-skills@71d031dab8bc6729504d11a78cbe91945401045f` (MIT).  
Upstream MCP pin: `mcp-for-blender==2.2.0` wheel SHA256 `160eb5e075b3933ed70d2de58445e27e08db0d5cc589f8f122d6027998ab9ce1`.

## Measured facts (not new runs)

- Skills A/B: four fixture GLBs byte-identical `f500f3e1…7a42`; helper correctly FAILs an intentional floater (`ok:true`, `pass:false`). N=2 is not a speed claim. Anatomy FAIL unchanged.
- MCP: ping, cube mutate/save/reopen, experimental R1 copy inspect. Armature `MuscleAtlasV2Rig` 27 bones; actions `CurlProbe`/`PulldownProbe`; BP4795 resolved via `mesh_mapping.json` then object name; face 914 cross-checked with bpy CLI. Viewport capture followed the 3D View matrix, not the posed scene camera.
- Safe Mode / Skills runners are AST/process gates, **not OS sandboxes**.

## Integration rule for M3-A

```
Codex → (optional) guarded MCP or fixture Skills
      → localize names / screenshots
      → author a reviewed bpy/node experiment in an isolated worktree
      → original 121-frame geometry + seam-check + independent reviews
```

If a proposed M3-A experiment cannot be expressed as a SHA-pinned CLI script, it is not ready. MCP/Skills must not become the mutation path for H1–H5.

## Rollback

Revert only the corresponding Draft PR. Do not run upstream uninstallers. Do not delete unrelated `.agents` trees or the user's normal Blender preferences. Keep `blender_agent`.
