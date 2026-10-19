# Blender Skills isolated pilot · Issue #13

## Candidate scope

Base: Phase 1 PR #8 `1b06bf4`. Upstream: [EL4CTEO/blender-skills](https://github.com/EL4CTEO/blender-skills/tree/71d031dab8bc6729504d11a78cbe91945401045f), pinned `71d031dab8bc6729504d11a78cbe91945401045f` (1.1.0), MIT; full notice in `UPSTREAM-LICENSE`. Registry includes SHA256 of **every installed file**. No global skill installation, shell profile changes or upstream hooks. Exactly three skills installed using the reviewed OpenAI skill-installer helper with `--dest .agents/skills --ref <SHA> --method git`. No runtime network or extra Python packages.

These project skills are fixture-only references/helpers. They do not replace the canonical 27-joint rig, original source anatomy/hands, existing Blender→GLB pipeline, 467-identity preservation checks, 121-frame full-triangle gates or independent owner review. No anatomical fixes were attempted here. Existing Phase 1 motion quality remains FAIL.

## Actual A/B results

Blender **5.2.0 LTS**, build `fbe6228777e7`, identical executable and saved fixture for all four runs. Our fresh disposable fixture contains two closed cubes (24 triangles), one intentionally detached; no borrowed source anatomy. A uses a short custom baseline inventory and the existing project glTF export approach; B **actually invokes** the pinned `batch_process.run(op='report')` and `qa_check.run(profile='render', uv=False)` helpers. Both use exactly the same export statement. Therefore the measured difference is additive automated QA coverage, **not prompt effectiveness, quality improvement of anatomy or a faster exporter**.

| Final run | Actual process exit | Wall time |
|---|---:|---:|
| Baseline 1 | 0 | 1.433 s |
| Skill 1 | 0 | 0.992 s |
| Baseline 2 | 0 | 1.203 s |
| Skill 2 | 0 | 1.186 s |

All four GLBs are byte-identical: `f500f3e1b1429bedb3d803b8420344dcbed6a9a3f195a10deab1e159f16a7a42`. Four inventories match: 2 meshes, 24 triangles, 2 materials, no actions. Saved fixture SHA is in actual `evidence/pilot-final/summary.json`; unchanged before/after execution. No manual intervention inside the runs. Two prior exploratory A/B repeats also produced the same GLB; final runs alone are the reported benchmark. N=2/order/system load do **not** justify a speed claim.

B reports `ok:true` (measurement executed) and **`pass:false`** (detached fixture correctly rejected), with one `PilotFloater`. A has no floating test. This is a controlled negative fixture, not a fabricated production result. No geometry was moved/hidden/deleted to turn the report green. Missing UV checks are deliberately off for this topology-only fixture, documented in the report; production UV/export/medical quality is not certified.

The real CPU Cycles image `evidence/fixture-cpu.png` was inspected and shows both separate cubes. It illustrates the fixture, not an anatomy result; own rendering script is included. Browser smoke shows the untouched existing app. Actual build PASS, Vitest **13/13**, project quality **26/26**, canonical reuse **4/4**, pin/protected-byte tests **2/2**, Chrome smoke **1/1**. Khronos validator final candidate: **0 errors, 0 warnings, 2 informational**. Build's existing >500 kB bundle-size warning is retained; no performance optimization claim.

## Run locally

From repository root, no upstream checkout required:

```sh
python3 -m unittest discover -s tests/blender-skills -v
python3 scripts/blender-skills/run_pilot.py \
  --blender /Applications/Blender.app/Contents/MacOS/Blender \
  --output artifacts/blender-skills/my-fresh-run
node scripts/rig-v2/pipeline/validate.mjs artifacts/blender-skills/my-fresh-run/skill-1
npm ci --ignore-scripts
npm run build
npm test
npm run test:quality
node --test tests/rig-v2/reuse.node.mjs
npx playwright test tests/browser/atlas.spec.ts -g 'real model, joint playback, selection and persistence'
```

Output directory must be new and project-local under `artifacts/`. Registry mismatch or unregistered skill file is rejected before Blender starts. Factory startup, `--disable-autoexec`, `--python-exit-code 1` and a 180 s workload timeout are explicit. No arbitrary third-party `--op script` arguments are forwarded. The fixture is re-opened with `load_ui=False`, inventory checked for exactly one input, all process return codes and reports checked. Runner assertions are test invariants; run normally, not `python -O`. There is no OS network sandbox: absence of network is established by selected code inspection, not packet monitoring.

Native fixture/GLBs, raw logs and JSON are committed under `evidence/pilot-final/`; the command arrays retain original machine paths as actual-run provenance, while the above commands are portable. `executedScriptHashes` binds the final A/B execution to scripts. Registry/file pin and all upstream inventory hashes are separate from geometry provenance.

## Decisions, rollback and remaining limitations

See `security-review.md` for explicit reusable/redundant/conflicting decisions. Three locally discoverable skills are approved **only for isolated fixtures**, not full production execution. Upstream generic auto-binding, vertex cleanup, merge/delete advice, stress poses and export presets remain uninstalled/not approved. No code or schema owned by Windows changed; this pilot has no contact/OpenSim claims or data interface changes.

Rollback is reviewable through Git: revert only this pilot commit/PR, removing `.agents/skills/{blender-core,blender-pipeline-automation,blender-asset-qa}`, `.agents/AGENTS.md`, this pilot's docs/scripts/tests and roadmap entry. Do not run upstream uninstallers and do not remove another agent's `.agents` tree. Current sessions may retain already loaded instructions; reopen the project/session after rollback. No Blender preferences/add-ons were installed or saved.

Workarounds introduced: **none**. Permanently resolved debt: **none in this scoped tooling experiment**. Deferred/accepted debt: no new entry; historical motion/hand/Windows debt unchanged. Remaining evidence: independent root review and Owner approval pending; this candidate is not anatomical, production or product acceptance. Full upstream 22-skill suite was not executed because only three helpers are adopted and unselected modules are not approved; this is scope, not a replacement for required project tests.
