# Windows Codex asset handoff — 2026-10-15

Repository: https://github.com/hengqi61-maker/muscle-atlas

Use branch `codex/lat-pulldown-m2-reviewed`, checkpoint `cc4a83c` (this handoff is a later documentation commit). Do not use main as the latest M2. Main remains the immutable old baseline `7a0d258b59e9a2acc32021e8ab66f7098ff025ea`. No merge or product acceptance is authorized.

## Assets available directly through Git

Paths below are relative to the checkout on Windows; a Mac absolute path is not a Windows path.

| Path | Purpose | SHA256 |
| --- | --- | --- |
| public/models/anatomy.glb | Original anatomical source | 6e84529b60b64cc8f8d5cef665fda932e359e828b66d0c2dd44ec1bd9d0bd01f |
| public/models/anatomy-pulldown.glb | Current M2 prototype, NOT accepted | c4109d53fdcb679dda6358eb9f5d9595b9ae51ad670679eca02dce6d107d1b67 |
| public/models/anatomy-curl.glb | Existing curl asset | 0b579c7256a0500b51b5f14506813285ebddc04046106451c55e84ccfba1585f |
| public/models/equipment/detailed-hex-dumbbell.glb | Dumbbell | 920acfacdbb0156ce30e73d9c2a7791abb8e9030515ca51c05ca21b336430e68 |

Mapping: `src/data/mesh_mapping.json`, `public/models/mesh_mapping.json`.
Pulldown production: `scripts/build-pulldown-rig.py`, `src/data/pulldown-config.json`, `src/three/pulldownMotion.ts`. Machine is constructed by source code, not a separate presumed external machine GLB.
Reference package: `docs/exercises/lat-pulldown/`; source access limitations explicitly documented.
Independent new tests: `scripts/quality/motion-quality.mjs`, `tests/quality/motion/README.md`.

## Mac-only material not yet uploaded as an evidence release

- Active M2 checkout: `/Users/qi-heng/Documents/ChatGPT/muscle-atlas-m2`.
- Immutable baseline checkout: `/Users/qi-heng/Documents/ChatGPT/muscle-atlas-baseline-7a0d258`.
- Baseline media/data: baseline checkout `artifacts/blind-review/7a0d258b59e9a2acc32021e8ab66f7098ff025ea/`.
- Current prototype media: M2 checkout `artifacts/m2/prototype-c749261/`.
- Independent red/new numeric evidence: M2 checkout `artifacts/m2/independent-motion-tests/`.
- Blender imported source file: `/Users/qi-heng/Documents/blender操控/blender-agent/public/models/anatomy-import.blend`. This local file is not a certified matching authoring source for the current GLB and is not tracked in Git.

Do not assume ignored artifacts or this local blend are present after cloning.

## Current quality status and boundaries

Old baseline tests reproduce frozen eight cuff meshes and foot-platform penetration. Current prototype still fails severe cuff collapse tests; true original-hand grasp, calibrated anatomical attachment and complete visual review remain INCONCLUSIVE. The 15 passing test-unit/gate checks do not certify the motion. Latest browser test expansion is saved but not run after expansion. Performance diagnostics saved as unfinished tooling; no new FPS specialty work authorized.

Preserve all 467 source mesh identities and original hand geometry. No replacement hands, hiding source anatomy, unified skeleton rebuild, face-pull production or main merge. Root coordinator alone integrates concurrent work. At most two complete repair/review cycles; no final M2 cycle completed yet.

## Delivery status

The Windows host `win-codex` was contacted once via SSH but returned `Host is down`; no message was delivered and no Windows filesystem was modified. Desktop task listing showed no Windows task to message. This committed document is the retrievable handoff. Current maker/test agent turns hit an account usage limit; unfinished work must not be represented as accepted.
